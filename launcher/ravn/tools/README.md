# How the Ravn pictures and music were made

Everything in `../brand/` and `../media/` was made by the three programs in this folder. No image, video or music model was used, nobody was recorded, nothing was sampled, and no SEGA artwork, logo or music is a source.

- `make_logo.py` draws `brand/logo.png` (1792 × 1008, transparent). It needs Pillow and two fonts from the Google Fonts repository, both under the SIL Open Font License (`OFL-*.txt`): Playfair Display for **Ravn**, Noto Sans Runic for **ᚼᚱᛅᚠᚾ**. The runes spell *hrafn*, Old Norse for raven, in Younger Futhark: h, r, a, f, n. The feather is drawn line by line.
- `make_loop.py` renders `brand/fond-loop.mp4` (1280 × 720, 24 fps, 10 s). Feathers and snow fall at three depths. Every motion repeats exactly once per loop, so the video loops without a seam. It needs Pillow, NumPy and ffmpeg with libx264.
- `make_theme.py` synthesizes `media/theme.mp3`. The melody is original, in D Dorian, written for this launcher. A plucked string (Karplus-Strong, tuned with an allpass) plays it over a soft open-fifth drone, with a simple reverb. It needs NumPy and ffmpeg with libmp3lame.

```
python make_logo.py <google-fonts-checkout> ../brand/logo.png
python make_loop.py ../brand/fond-loop.mp4
python make_theme.py ../media/theme.mp3
python make_icon.py <google-fonts-checkout> ../ravn.ico
```

`make_icon.py` draws `ravn.ico`, the icon of Ravn.exe and of the runtime executables: an ivory R in Playfair Display with the gold rule.

You can replace any of these files. Keep the names.
