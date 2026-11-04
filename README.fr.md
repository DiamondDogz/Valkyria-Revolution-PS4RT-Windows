# Valkyria-Revolution-PS4RT-Windows

Portage Windows de [valkyria-revolution-ps4rt](https://github.com/HekamiAeon/valkyria-revolution-ps4rt) de HekamiAeon, compilé depuis le `main` d'origine, commit `635e142aa7fe36c54926b3f624a1fcb59d58acd1`. Ce commit correspond au tag **v1.2** plus un commit de documentation. Publié par [DiamondDogz](https://github.com/DiamondDogz). Le lanceur s'appelle **Ravn** : `Ravn.exe`.

Non officiel. Aucun lien avec SEGA. Le jeu n'est pas inclus.

Téléchargement : [windows-1.2](https://github.com/DiamondDogz/Valkyria-Revolution-PS4RT-Windows/releases/tag/windows-1.2). Il faut votre propre copie extraite du jeu de base, **CUSA06810**, sans mise à jour, comme pour la version Linux.

Testé sur Windows 11 Professionnel pour les Stations de travail, version 26H2, un Intel Core i9-12900KF, 128 Go de DDR5 à 4000 MT/s, une NVIDIA GeForce RTX 3090 24 Go avec le pilote Studio 617.42 (6 octobre 2026), et un SSD NVMe de 4 To (PCI Express 4.0). C'est la machine de test, pas un minimum. Le jeu a démarré et a tourné jusqu'à la fin de la campagne de Molda ; des trophées se sont débloqués. Une partie complète n'a pas été vérifiée.

English version: [README.md](README.md). Le README Linux d'origine est [README.linux.md](README.linux.md).

## Ravn

- **Chemins** : votre dossier CUSA06810 extrait. Il n'est pas modifié.
- **Réglages** : ceux du menu en jeu de la version Linux.
  - Résolution de sortie : 1920 × 1080, 2560 × 1440 ou 3840 × 2160.
  - Fenêtre : fenêtré, sans bordure ou plein écran.
  - Upscaling : Désactivé / Original, FSR 3.1 ou FSR 4 v07. Le jeu calcule l'image en 1080p et FSR la reconstruit à la taille de sortie. FSR 4 demande un GPU récent et se replie sur FSR 3.1.
  - Filtrage anisotrope, appliqué au redémarrage.
  - Netteté.

  Ravn les écrit dans `ps4rt.ini`, le fichier du menu en jeu.
- **Trophées** : locaux, lus dans le `trophy00.trp` de votre dossier de jeu. Rien n'est envoyé. Le panneau montre votre progression, le compte par rang et chaque trophée, et se trie par ordre du jeu, obtenus d'abord ou rang. En jeu, une carte s'affiche quelques secondes quand un trophée se débloque, sans prendre la manette.
- **Thème et visuels** : un thème original et des visuels générés par programme. Aucune image ni aucun son de SEGA dans l'archive.

En jeu, Insert, ou L2 + R3, ouvre l'incrustation.

Installation et premier lancement : [INSTALL.md](packaging/windows/ravn/INSTALL.md) (anglais puis français).

## Ce qui change par rapport à l'original

- Le build Windows restauré. La v1.2 l'avait retiré ; il était hérité et non vérifié.
- Des trophées locaux avec une carte en jeu, comme dans [Sakura-Wars-PS4RT-Windows](https://github.com/DiamondDogz/Sakura-Wars-PS4RT-Windows). La clé des trophées vient du `sce_sys/npbind.dat` du jeu.
- `scripts/link_libc.py` ignore les symboles libc à nom simple (comme `__start__Ztext`) au lieu de s'arrêter. Certains dumps en contiennent.
- Le lanceur Ravn, dans `launcher/ravn/`.

## Compiler

GitHub Actions compile tout sur une machine Windows avec MSYS2 CLANG64 : [.github/workflows/windows.yml](.github/workflows/windows.yml). Le workflow lance ces scripts dans l'ordre :

1. `build.sh` compile le runtime.
2. `packaging/windows/build_ravn.sh` compile `Ravn.exe`.
3. `packaging/windows/package_ravn.sh` crée `Ravn-windows-<version>.zip`.

Les paquets nécessaires sont listés dans le workflow. Un tag `windows-<version>` produit `Ravn-windows-<version>.zip`.

## Non inclus

Le dépôt d'origine a un portrait et des sons de menu tirés du jeu. Ils ne sont pas dans l'archive. L'incrustation fonctionne sans eux. Si vous les avez, placez `valkyria_overlay.png` et le dossier `sounds` dans `gpu\assets\`, à côté de `Ravn.exe`, et Ravn les utilise.

## IA

Une bonne part de ce portage a été écrite avec Claude, d'Anthropic. Voir [AI.md](packaging/windows/ravn/AI.md).

## Crédits et licence

Le runtime est [valkyria-revolution-ps4rt](https://github.com/HekamiAeon/valkyria-revolution-ps4rt) de HekamiAeon, sous GPL ; voir [LICENSE](LICENSE) et [docs/UPSTREAM_CREDITS.md](docs/UPSTREAM_CREDITS.md). Les crédits de Ravn : [CREDITS.md](packaging/windows/ravn/CREDITS.md).
