#!/usr/bin/env bash
# Builds out/Ravn.exe, the WebView2 window of the Ravn launcher (launcher/ravn/ravn.cc).
# Run from an MSYS2 CLANG64 shell. It fetches two header-only sources into out/:
#   webview (MIT, https://github.com/webview/webview) at WEBVIEW_REF
#   Microsoft.Web.WebView2 (NuGet) at WEBVIEW2_VERSION, for WebView2.h and EventToken.h
set -euo pipefail
# CI has no terminal: never let git or unzip wait for an answer, and trace each command.
export GIT_TERMINAL_PROMPT=0
exec </dev/null
set -x
cd -- "$(dirname -- "$0")/../.."
source ./msys2-env.sh
WEBVIEW_REF=${WEBVIEW_REF:-0.12.0}
WEBVIEW2_VERSION=${WEBVIEW2_VERSION:-1.0.3179.45}
mkdir -p out
if [[ ! -f out/webview/core/include/webview/webview.h ]]; then
    rm -rf out/webview
    timeout 600 git clone -q --depth 1 --branch "$WEBVIEW_REF" https://github.com/webview/webview out/webview ||
        timeout 600 git clone -q --depth 1 https://github.com/webview/webview out/webview
fi
if [[ ! -f out/webview2/build/native/include/WebView2.h ]]; then
    rm -rf out/webview2 && mkdir -p out/webview2
    curl -fsSL --retry 3 --max-time 300 -o out/webview2.nupkg "https://www.nuget.org/api/v2/package/Microsoft.Web.WebView2/$WEBVIEW2_VERSION"
    (cd out/webview2 && unzip -o -q ../webview2.nupkg 'build/native/include/*')
fi
# WebView2.h includes EventToken.h, a Windows SDK header that the NuGet package does not carry.
# Use the MinGW-w64 one when the toolchain has it, else declare the one struct it holds.
if [[ ! -f out/webview2/build/native/include/EventToken.h ]]; then
    cat > out/webview2/build/native/include/EventToken.h <<'HDR'
#pragma once
#if defined(__has_include_next) && __has_include_next(<eventtoken.h>)
#include_next <eventtoken.h>
#else
typedef struct EventRegistrationToken { __int64 value; } EventRegistrationToken;
#endif
HDR
fi
llvm-windres -I launcher/ravn launcher/ravn/ravn.rc -O coff -o out/ravn-icon.o
clang++ -std=c++17 -O2 -static -mwindows \
    -Iout/webview/core/include -Iout/webview2/build/native/include \
    launcher/ravn/ravn.cc out/ravn-icon.o -o out/Ravn.exe \
    -lws2_32 -lole32 -lshell32 -lshlwapi -luser32 -lversion -luuid -ladvapi32
llvm-strip out/Ravn.exe
echo "Built $PWD/out/Ravn.exe ($(stat -c %s out/Ravn.exe) bytes)"
