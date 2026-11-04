# Ravn — Valkyria Revolution PS4RT for Windows

A Windows port of [HekamiAeon, valkyria-revolution-ps4rt](https://github.com/HekamiAeon/valkyria-revolution-ps4rt), from its `main` branch after v1.2. Published by [DiamondDogz](https://github.com/DiamondDogz). The launcher is `Ravn.exe`.

Unofficial. Not affiliated with SEGA. The game is not included.

This is a test build. The upstream project is tested on Linux. Its Windows build was inherited and unverified, and v1.2 removed it; this port restores it and builds it again. Expect rough edges.

Version française : [README.fr.md](README.fr.md).

## What you need

1. Windows 10 or 11, x86-64, with Microsoft Edge WebView2.
2. A graphics card with a current Vulkan driver.
3. Your own extracted copy of Valkyria Revolution, CUSA06810: the folder with `eboot.bin`, `sce_sys` and `sce_module`.

The details are in [INSTALL.md](INSTALL.md).

## Launcher

`Ravn.exe` opens the launcher. It does not open your browser.

- Paths: your game folder, the base game CUSA06810 as the Linux release runs it. It is not changed. No update is needed.
- Settings: the ones of the Linux release's in-game menu. Output resolution, window, upscaling (Off / Original, FSR 3.1, FSR 4 v07), anisotropic filtering and sharpening. The game renders its 1080p scene at its own frame rate and FSR rebuilds it at the output size; FSR 4 needs a recent GPU and falls back to FSR 3.1. The settings are written to `ps4rt.ini`, the file the in-game menu uses, so a change made in game shows here too.
- Trophies: read from `trophy00.trp` in your game folder. Nothing is sent. The panel shows your progress and can sort by game order, earned first or grade. When the game earns one, a card shows for a few seconds and does not take the controller. Trophies are in the language of your game edition.
- EN/FR: the launcher's own language.

In game, Insert, or L2 + R3, opens the overlay.

## What is not included

The upstream repository has a menu portrait and menu sounds taken from the game. They are not in this archive. The overlay works without them. If you have them, put `valkyria_overlay.png` and the `sounds` folder in `gpu\assets\` next to `Ravn.exe`, as in the Linux release, and Ravn uses them.

## AI

A large part of this port was written with Claude, by Anthropic. See [AI.md](AI.md).

## Credits

The runtime is [HekamiAeon's valkyria-revolution-ps4rt](https://github.com/HekamiAeon/valkyria-revolution-ps4rt). See [CREDITS.md](CREDITS.md).

## Licence

GPL-2.0-or-later, as the runtime this is built from. Bundled components keep their notices, in `licenses/`.

No warranty.
