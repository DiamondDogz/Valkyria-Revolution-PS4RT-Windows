# Credits

## Game

*Valkyria Revolution* is © SEGA, developed by Media.Vision. It is not included.

## Runtime

The game runtime is [HekamiAeon, valkyria-revolution-ps4rt](https://github.com/HekamiAeon/valkyria-revolution-ps4rt), GPL-2.0-or-later. Its own lineage (gow3_pc, bloodborne_pc, shadPS4 and others) and its third-party notices are in [UPSTREAM_CREDITS.md](UPSTREAM_CREDITS.md). Credit for that program stays with HekamiAeon and the people named there.

The Windows build files this port restores (`packaging/windows/`, `msys2-env.sh`, the MSYS2 CLANG64 paths of `build.sh` and `gpu/CMakeLists.txt`) are the upstream project's own, as they were before v1.2.

## Windows port

Published and tested by [DiamondDogz](https://github.com/DiamondDogz). Written with [Claude](https://claude.ai) (Anthropic); the Kagekidan launcher it follows was written with [Grok](https://grok.com) (xAI). See [AI.md](AI.md).

The Ravn launcher, its page and `Ravn.exe` follow the Kagekidan launcher of [Sakura-Wars-PS4RT-Windows](https://github.com/DiamondDogz/Sakura-Wars-PS4RT-Windows). The local trophy list and the in-game trophy card come from that port's windows-1.1.3.

`Ravn.exe` uses [webview](https://github.com/webview/webview) (MIT) and the Microsoft Edge WebView2 runtime, which is not bundled.

## Bundled components

- The runtime DLLs from MSYS2 CLANG64 (SDL3, FFmpeg, fmt, xxHash, Zydis, Boost, libc++ and others). Their licences are in `licenses/msys2-*`.
- The python.org embeddable Python 3.12, with [Pillow](https://python-pillow.org) and [iced-x86](https://github.com/icedland/iced). Their licences are in `python/`.
- Fonts in the launcher logo: Playfair Display and Noto Sans Runic, SIL Open Font License, in `licenses/`.

The Vulkan loader is not bundled. It comes with your graphics driver.
