# Valkyria-Revolution-PS4RT-Windows

Windows port of [valkyria-revolution-ps4rt](https://github.com/HekamiAeon/valkyria-revolution-ps4rt) by HekamiAeon, built from upstream `main`, commit `635e142aa7fe36c54926b3f624a1fcb59d58acd1`. That commit is tag **v1.2** plus one documentation commit. Published by [DiamondDogz](https://github.com/DiamondDogz). The launcher is **Ravn**, `Ravn.exe`.

Unofficial. Not affiliated with SEGA. The game is not included.

Download: [windows-1.2](https://github.com/DiamondDogz/Valkyria-Revolution-PS4RT-Windows/releases/tag/windows-1.2). It needs your own extracted copy of the base game, **CUSA06810**, with no update, as the Linux release does.

Tested on Windows 11 Pro for Workstations, version 26H2, an Intel Core i9-12900KF, 128 GB of DDR5 at 4000 MT/s, an NVIDIA GeForce RTX 3090 24 GB with Studio driver 617.42 (6 October 2026), and a 4 TB NVMe SSD (PCI Express 4.0). That is the test machine, not a minimum. The game started and played through the Molda campaign; trophies unlocked. A complete playthrough is not verified.

Version française : [README.fr.md](README.fr.md). The upstream Linux README is [README.linux.md](README.linux.md).

## Ravn

- **Paths**: your extracted CUSA06810 folder. It is not changed.
- **Settings**: those of the Linux release's in-game menu.
  - Output resolution: 1920 × 1080, 2560 × 1440 or 3840 × 2160.
  - Window: windowed, borderless or fullscreen.
  - Upscaling: Off / Original, FSR 3.1 or FSR 4 v07. The game renders 1080p and FSR rebuilds it at the output size. FSR 4 needs a recent GPU and falls back to FSR 3.1.
  - Anisotropic filtering, applied on restart.
  - Sharpening.

  Ravn writes them to `ps4rt.ini`, the file of the in-game menu.
- **Trophies**: local, read from `trophy00.trp` in your game folder. Nothing is sent. The panel shows your progress, the grade counts and every trophy, and sorts by game order, earned first or grade. In game, a card shows for a few seconds when one unlocks and does not take the controller.
- **Theme and visuals**: an original theme and procedural visuals. No SEGA art or sound is in the archive.

In game, Insert, or L2 + R3, opens the overlay.

Installation and first launch: [INSTALL.md](packaging/windows/ravn/INSTALL.md).

## What changed from upstream

- The Windows build restored. v1.2 removed it; it was inherited and unverified.
- Local trophies with an in-game card, as in [Sakura-Wars-PS4RT-Windows](https://github.com/DiamondDogz/Sakura-Wars-PS4RT-Windows). The trophy key comes from the game's `sce_sys/npbind.dat`.
- `scripts/link_libc.py` skips plain-named libc symbols (such as `__start__Ztext`) instead of stopping. Some dumps carry them.
- The Ravn launcher, in `launcher/ravn/`.

## Building

GitHub Actions builds everything on a Windows runner with MSYS2 CLANG64: [.github/workflows/windows.yml](.github/workflows/windows.yml). It runs these scripts in turn:

1. `build.sh` builds the runtime.
2. `packaging/windows/build_ravn.sh` builds `Ravn.exe`.
3. `packaging/windows/package_ravn.sh` builds `Ravn-windows-<version>.zip`.

The packages the build needs are listed in the workflow. A tag `windows-<version>` builds `Ravn-windows-<version>.zip`.

## Not included

The upstream repository has a menu portrait and menu sounds taken from the game. They are not in the archive. The overlay works without them. If you have them, put `valkyria_overlay.png` and the `sounds` folder in `gpu\assets\` next to `Ravn.exe`, and Ravn uses them.

## AI

A large part of this port was written with Claude, by Anthropic. See [AI.md](packaging/windows/ravn/AI.md).

## Credits and licence

The runtime is HekamiAeon's [valkyria-revolution-ps4rt](https://github.com/HekamiAeon/valkyria-revolution-ps4rt), under the GPL; see [LICENSE](LICENSE) and [docs/UPSTREAM_CREDITS.md](docs/UPSTREAM_CREDITS.md). Ravn's credits: [CREDITS.md](packaging/windows/ravn/CREDITS.md).
