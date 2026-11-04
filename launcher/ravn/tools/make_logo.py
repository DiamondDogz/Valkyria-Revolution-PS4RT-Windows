"""Ravn wordmark: same lockup as Kagekidan, drawn by this program.

Ravn in Playfair Display, a thin gold rule, the Old Norse word hrafn (raven)
in Younger Futhark runes, and a line-drawn feather. All fonts are SIL OFL.
"""
import math, sys
from PIL import Image, ImageDraw, ImageFont

GF = sys.argv[1]
OUT = sys.argv[2]
W, H, K = 1792, 1008, 4          # final size, supersampling factor
IVORY = (236, 226, 206, 255)
GOLD = (214, 172, 92, 255)

big = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 0))
d = ImageDraw.Draw(big)

def font(path, size, weight=None):
    f = ImageFont.truetype(path, size * K)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f

# Wordmark, sized so Ravn spans about as wide as Kagekidan's lockup.
word = font(f"{GF}/ofl/playfairdisplay/PlayfairDisplay[wght].ttf", 400, 400)
x0, baseline = 108, 590
d.text((x0 * K, baseline * K), "Ravn", font=word, fill=IVORY, anchor="ls")
wb = d.textbbox((x0 * K, baseline * K), "Ravn", font=word, anchor="ls")

# Thin gold rule under the word, as on Kagekidan.
rule_y = 662
d.rectangle([x0 * K, rule_y * K, (x0 + 590) * K, rule_y * K + 2 * K], fill=GOLD)

# hrafn in Younger Futhark: h r a f n.
runes = font(f"{GF}/ofl/notosansrunic/NotoSansRunic-Regular.ttf", 112)
rx = wb[2] / K + 30
d.text((rx * K, 740 * K), "ᚼᚱᛅᚠᚾ", font=runes, fill=GOLD, anchor="ls")
rb = d.textbbox((rx * K, 740 * K), "ᚼᚱᛅᚠᚾ", font=runes, anchor="ls")

def feather(base, tip, widths, splits):
    """Line-drawn feather: a curved shaft, fine barbs swept to the tip."""
    bx, by = base; tx, ty = tip
    L = math.hypot(tx - bx, ty - by)
    ux, uy = (tx - bx) / L, (ty - by) / L
    nx, ny = -uy, ux
    def shaft(t):                      # t: 0 base .. 1 tip, gentle bow
        bow = 0.045 * L * math.sin(math.pi * t)
        return (bx + ux * t * L + nx * bow, by + uy * t * L + ny * bow)
    def at(t, s):                      # s across the shaft, in px
        x, y = shaft(t)
        return ((x + nx * s) * K, (y + ny * s) * K)
    d.line([at(i / 120, 0) for i in range(121)], fill=GOLD, width=int(2.4 * K), joint="curve")
    vane0 = 0.22                       # bare quill below this
    for side, width in zip((1, -1), widths):
        n = 24
        for j in range(n):
            t = vane0 + (1 - vane0 - 0.015) * j / (n - 1)
            u = (t - vane0) / (1 - vane0)
            half = width * (math.sin(math.pi * min(1.0, u * 0.92 + 0.08)) ** 0.7) * (1 - 0.55 * u ** 3)
            if u < 0.06:
                half *= 0.35 + 0.65 * u / 0.06
            sweep = 0.17 + 0.05 * u   # barbs lean toward the tip
            gap = 1.0
            for (side_s, u0, u1) in splits:
                if side == side_s and u0 <= u <= u1:
                    gap = 0.78
            pts = []
            for k in range(13):
                f = k / 12
                pts.append(at(t + sweep * f * (1.0 - 0.25 * f) * gap ** 2, side * half * f * gap))
            d.line(pts, fill=GOLD, width=int(1.25 * K), joint="curve")
    # Small down tufts on the bare quill.
    for side in (1, -1):
        for j in range(4):
            t = 0.12 + 0.025 * j
            d.line([at(t, 0), at(t + 0.035, side * (9 - j))], fill=GOLD, width=int(1.1 * K))

cx = (rb[0] + rb[2]) / 2 / K + 120
feather(base=(cx - 80, 440), tip=(cx + 50, 150), widths=(44, 31), splits=[(1, 0.42, 0.50), (-1, 0.62, 0.68)])

im = big.resize((W, H), Image.LANCZOS)
im.save(OUT)
print("saved", OUT, im.getbbox())
