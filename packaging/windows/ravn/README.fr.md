# Ravn — Valkyria Revolution PS4RT pour Windows

Portage Windows de [HekamiAeon, valkyria-revolution-ps4rt](https://github.com/HekamiAeon/valkyria-revolution-ps4rt), d'après sa branche `main` après la v1.2. Publié par [DiamondDogz](https://github.com/DiamondDogz). Le lanceur est `Ravn.exe`.

Non officiel. Aucun lien avec SEGA. Le jeu n'est pas inclus.

C'est un build de test. Le projet d'origine est testé sous Linux. Son build Windows était hérité et non vérifié, et la v1.2 l'a retiré ; ce portage le restaure et le compile à nouveau. Attendez-vous à des aspérités.

## Ce qu'il faut

1. Windows 10 ou 11, x86-64, avec Microsoft Edge WebView2.
2. Une carte graphique avec un pilote Vulkan à jour.
3. Votre propre copie extraite de Valkyria Revolution, CUSA06810 : le dossier avec `eboot.bin`, `sce_sys` et `sce_module`.
4. Facultatif : votre propre dossier de mise à jour extrait.

Le détail est dans [INSTALL.md](INSTALL.md).

## Lanceur

`Ravn.exe` ouvre le lanceur. Il n'ouvre pas le navigateur.

- Chemins : le dossier du jeu, et le dossier de mise à jour si vous en avez un. Aucun des deux n'est modifié.
- Réglages : sortie, fenêtre, limite à 30 ou 60 images par seconde, filtrage anisotrope, netteté. Le jeu dessine sa propre scène en 1080p à son propre rythme : il n'existe pas encore de patch de résolution ou de cadence pour lui. Ils sont écrits dans `ps4rt.ini`, le fichier du menu en jeu : un changement fait en jeu se retrouve ici.
- Trophées : lus dans le `trophy00.trp` de votre dossier de jeu. Rien n'est envoyé. Quand le jeu en obtient un, une carte s'affiche quelques secondes, sans prendre la manette.
- Le bouton globe : la langue du jeu. Seules les langues présentes dans votre dossier de jeu sont proposées.
- EN/FR : la langue du lanceur lui-même.

En jeu, Insert, ou L2 + R3, ouvre l'incrustation.

## Ce qui n'est pas inclus

Le dépôt d'origine a un portrait et des sons de menu tirés du jeu. Ils ne sont pas dans cette archive. L'incrustation fonctionne sans eux.

## IA

Une bonne part de ce portage a été écrite avec Claude, d'Anthropic. Voir [AI.md](AI.md).

## Crédits

Le runtime est [valkyria-revolution-ps4rt de HekamiAeon](https://github.com/HekamiAeon/valkyria-revolution-ps4rt). Voir [CREDITS.md](CREDITS.md).

## Licence

GPL-2.0-or-later, comme le runtime dont il dérive. Les composants fournis gardent leur notice, dans `licenses/`.

Aucune garantie.
