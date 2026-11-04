# Ravn — Valkyria Revolution PS4RT for Windows

A Windows port of [HekamiAeon, valkyria-revolution-ps4rt](https://github.com/HekamiAeon/valkyria-revolution-ps4rt), from its `main` branch after v1.2. Published by [DiamondDogz](https://github.com/DiamondDogz). The launcher is `Ravn.exe`.

Unofficial. Not affiliated with SEGA. The game is not included.

This is a test build. The upstream project is tested on Linux. Its Windows build was inherited and unverified, and v1.2 removed it; this port restores it and builds it again. Expect rough edges.

Version française : [README.fr.md](README.fr.md).

## What you need

1. Windows 10 or 11, x86-64, with Microsoft Edge WebView2.
2. A graphics card with a current Vulkan driver.
3. Your own extracted copy of Valkyria Revolution, CUSA06810: the folder with `eboot.bin`, `sce_sys` and `sce_module`.
4. Optional: your own extracted update folder.

The details are in [INSTALL.md](INSTALL.md).

## Launcher

`Ravn.exe` opens the launcher. It does not open your browser.

- Paths: the game folder, and the update folder if you have one. Neither folder is changed.
- Settings: output, window, a 30 or 60 FPS limit, anisotropic filtering, sharpness. The game draws its own 1080p scene at its own pace: there is no resolution or frame rate patch for it yet. They are written to `ps4rt.ini`, the file the in-game menu uses, so a change made in game shows here too.
- Trophies: read from `trophy00.trp` in your game folder. Nothing is sent. When the game earns one, a card shows for a few seconds and does not take the controller.
- The globe button: the game language. Only the languages your game folder carries are listed.
- EN/FR: the launcher's own language.

In game, Insert, or L2 + R3, opens the overlay.

## What is not included

The upstream repository has a menu portrait and menu sounds taken from the game. They are not in this archive. The overlay works without them.

## AI

A large part of this port was written with Claude, by Anthropic. See [AI.md](AI.md).

## Credits

The runtime is [HekamiAeon's valkyria-revolution-ps4rt](https://github.com/HekamiAeon/valkyria-revolution-ps4rt). See [CREDITS.md](CREDITS.md).

## Licence

GPL-2.0-or-later, as the runtime this is built from. Bundled components keep their notices, in `licenses/`.

No warranty.
