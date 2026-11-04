"""Ravn icon: an ivory R in Playfair Display with the gold rule, on near black.

Writes a multi-size Windows .ico (16 to 256 px). Drawn by this program, like the logo.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

GF, OUT = sys.argv[1], sys.argv[2]
IVORY, GOLD, INK = (236, 226, 206, 255), (214, 172, 92, 255), (16, 16, 16, 255)
S = 1024
im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
d.rounded_rectangle([0, 0, S - 1, S - 1], radius=S // 6, fill=INK)
font = ImageFont.truetype(f"{GF}/ofl/playfairdisplay/PlayfairDisplay[wght].ttf", 760)
try:
    font.set_variation_by_axes([500])
except Exception:
    pass
d.text((S / 2, S * 0.74), "R", font=font, fill=IVORY, anchor="ms")
d.rectangle([S * 0.24, S * 0.82, S * 0.76, S * 0.82 + 26], fill=GOLD)
im.save(OUT, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
im.resize((256, 256), Image.LANCZOS).save(OUT.rsplit(".", 1)[0] + "-preview.png")
print("saved", OUT)
