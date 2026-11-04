#!/usr/bin/env bash
# Assembles dist/Ravn-windows-<version>.zip: Ravn.exe, run.py and the scripts, the runtime in
# bin/ with the CLANG64 DLLs it loads, the Ravn page in ravn/, and an embedded Python with
# Pillow and iced-x86. Run from an MSYS2 CLANG64 shell after build.sh and build_ravn.sh.
#   RAVN_VERSION    archive version (default: dev)
#   WINPYTHON       a Windows CPython 3.12 used only to install the wheels (pip --target)
#   PYTHON_VERSION  the python.org embeddable package to bundle (3.12.x, same minor as WINPYTHON)
set -euo pipefail
cd -- "$(dirname -- "$0")/../.."
source ./msys2-env.sh
version=${RAVN_VERSION:-dev}
python_version=${PYTHON_VERSION:-3.12.10}
name=Ravn-windows-$version
dest=out/stage/$name
for file in out/Ravn.exe out/ps4rt-probe.exe out/ps4rt-gpu-capabilities.exe; do
    [[ -f $file ]] || { echo "Build first: $file is missing" >&2; exit 1; }
done
[[ -n ${WINPYTHON:-} && -x $WINPYTHON ]] || { echo 'Set WINPYTHON to a Windows python.exe 3.12' >&2; exit 1; }

rm -rf out/stage
mkdir -p "$dest/bin" "$dest/ravn" "$dest/python" "$dest/licenses"
cp out/Ravn.exe "$dest/"
for exe in ps4rt-probe.exe ps4rt-gpu-capabilities.exe; do
    llvm-strip --strip-debug -o "$dest/bin/$exe" "out/$exe"
done
# Every DLL the runtime loads from the CLANG64 tree (SDL3, FFmpeg, Vulkan loader, libc++ ...).
ldd "$dest/bin/ps4rt-probe.exe" "$dest/bin/ps4rt-gpu-capabilities.exe" |
    awk '/\/clang64\/bin\// {print $3}' | sort -u | while read -r dll; do
        cp -u "$dll" "$dest/bin/"
    done
# The Vulkan loader comes with the graphics driver; never ship one that could shadow it.
rm -f "$dest/bin/vulkan-1.dll"

cp run.py LICENSE "$dest/"
cp -r scripts "$dest/"
cp launcher/ravn/launcher_host.py launcher/ravn/index.html "$dest/ravn/"
cp -r launcher/ravn/brand launcher/ravn/media "$dest/ravn/"
cp launcher/ravn/tools/OFL-*.txt "$dest/licenses/"
for doc in README.md README.fr.md INSTALL.md AI.md CREDITS.md; do
    cp "packaging/windows/ravn/$doc" "$dest/"
done
cp docs/UPSTREAM_CREDITS.md "$dest/UPSTREAM_CREDITS.md"
# Third-party notices of the runtime, as in the Linux player archive.
for notice in gpu/shadps4/LICENSE gpu/third_party/fonts/LICENSE-DejaVu.txt gpu/third_party/fsr-vulkan/LICENSE.txt \
              gpu/third_party/fsr-vulkan/NOTICE.md gpu/third_party/half/LICENSE.txt gpu/third_party/imgui/LICENSE.txt \
              gpu/third_party/magic_enum/LICENSE gpu/third_party/miniz/LICENSE gpu/third_party/sirit/LICENSE.txt \
              gpu/third_party/xbyak/COPYRIGHT third_party/LibAtrac9/LICENSE docs/licenses/GPL-3.0.txt; do
    if [[ -f $notice ]]; then
        flat=${notice//\//_}
        cp "$notice" "$dest/licenses/$flat"
    fi
done
# MSYS2 package licences for the DLLs that ship (FFmpeg, SDL3, ...).
clang64=$(dirname "$(command -v clang)")/..
if [[ -d $clang64/share/licenses ]]; then
    for dll in "$dest"/bin/*.dll; do
        package=$(pacman -Qoq "$(cygpath -u "$clang64/bin/$(basename "$dll")")" 2>/dev/null || true)
        [[ -n $package && -d $clang64/share/licenses/${package#mingw-w64-clang-x86_64-} ]] &&
            cp -r "$clang64/share/licenses/${package#mingw-w64-clang-x86_64-}" "$dest/licenses/msys2-${package#mingw-w64-clang-x86_64-}"
    done
fi

# Embedded Python: the python.org package, its path file pointed at the scripts and the wheels.
curl -fsSL -o out/python-embed.zip "https://www.python.org/ftp/python/$python_version/python-$python_version-embed-amd64.zip"
(cd "$dest/python" && unzip -q ../../../python-embed.zip)
pth=$(ls "$dest"/python/python3*._pth)
printf 'python312.zip\n.\nLib\\site-packages\n..\\scripts\n' > "$pth"
"$WINPYTHON" -m pip install -q --disable-pip-version-check --no-compile \
    --target "$(cygpath -w "$dest/python/Lib/site-packages")" pillow iced-x86==1.21.0
find "$dest" -name __pycache__ -prune -exec rm -r {} +

# No game files and nothing a player made, and no game-derived media.
forbidden=$(find "$dest" \( -iname eboot.bin -o -iname sce_module -o -iname sce_sys -o -iname savedata \
    -o -iname user -o -iname '*.log' -o -iname ps4rt.ini -o -iname launcher-state.json \
    -o -iname '*.spv' -o -iname '*.pkg' -o -iname '*.sprx' -o -iname '*.prx' -o -iname '*.trp' \
    -o -iname valkyria_overlay.png -o -iname 'Valkyria_*.wav' \) -print)
if [[ -n $forbidden ]]; then
    echo "Package holds files that must not ship:" >&2
    echo "$forbidden" >&2
    exit 1
fi
mkdir -p dist
rm -f "dist/$name.zip" "dist/$name.zip.sha256"
(cd out/stage && zip -qr -9 "../../dist/$name.zip" "$name")
(cd dist && sha256sum "$name.zip" > "$name.zip.sha256" && cat "$name.zip.sha256")
du -sh "$dest" "dist/$name.zip"
