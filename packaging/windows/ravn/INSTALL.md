# Install

English first. La version française suit.

## What you need

- Windows 10 or Windows 11, 64-bit.
- A GPU with a current Vulkan driver.
- Microsoft Edge WebView2. It is already installed with Edge on current Windows 10 and 11. The launcher does not bundle it.
- Your own copy of Valkyria Revolution, PlayStation 4, title id CUSA06810, already extracted. The folder must contain `eboot.bin`, `sce_sys` and `sce_module`.

This project does not provide the game, keys, firmware, or saves.

## Unpack

1. Unzip the archive.
2. Do not run the program from inside the zip.
3. Open `Ravn.exe`, at the root of the folder.
4. Windows SmartScreen may warn you. The executable is not signed. Choose More info, then Run anyway. Do not turn off Microsoft Defender for this.

## Paths

Game folder: the extracted CUSA06810 directory, not a PKG. It is not changed. As in the Linux release, Ravn runs the base game: no update is needed.

## Play

Play writes your choices to `ps4rt.ini`, then starts `run.py`. A console window keeps the log; leave it open while you play.

The first start prepares the game in `out/`. It takes longer than the next ones.

Saves, shader caches and trophies stay in `user/`, next to `Ravn.exe`. Saves are backed up before each start.

In game, Insert, or L2 + R3, opens the overlay. It has the same graphics settings, and more.

## If it does not start

Send the text of the console window, with your Windows version and graphics card. If the launcher itself does not open, send `launcher-error.txt`.

---

# Installation

## Ce qu'il faut

- Windows 10 ou Windows 11, 64 bits.
- Une carte graphique avec un pilote Vulkan à jour.
- Microsoft Edge WebView2. Il est déjà installé avec Edge sur Windows 10 et 11 à jour. Le lanceur ne l'embarque pas.
- Votre propre copie de Valkyria Revolution, PlayStation 4, CUSA06810, déjà extraite. Le dossier contient `eboot.bin`, `sce_sys` et `sce_module`.

Ce projet ne fournit ni le jeu, ni clés, ni firmware, ni sauvegardes.

## Décompresser

1. Décompressez l'archive.
2. Ne lancez pas le programme depuis le zip.
3. Ouvrez `Ravn.exe`, à la racine du dossier.
4. Windows SmartScreen peut avertir. L'exécutable n'est pas signé. Choisissez Informations complémentaires, puis Exécuter quand même. Ne désactivez pas Microsoft Defender pour ça.

## Chemins

Dossier du jeu : le dossier CUSA06810 extrait, pas un PKG. Il n'est pas modifié. Comme la version Linux, Ravn lance le jeu de base : aucune mise à jour n'est nécessaire.

## Jouer

Jouer écrit vos choix dans `ps4rt.ini`, puis démarre `run.py`. Une console garde le journal ; laissez-la ouverte pendant la partie.

Le premier démarrage prépare le jeu dans `out/`. Il est plus long que les suivants.

Les sauvegardes, les caches de shaders et les trophées restent dans `user/`, à côté de `Ravn.exe`. Les sauvegardes sont copiées avant chaque démarrage.

En jeu, Insert, ou L2 + R3, ouvre l'incrustation. Elle a les mêmes réglages graphiques, et d'autres.

## Si ça ne démarre pas

Envoyez le texte de la console, avec votre version de Windows et votre carte graphique. Si le lanceur lui-même ne s'ouvre pas, envoyez `launcher-error.txt`.
