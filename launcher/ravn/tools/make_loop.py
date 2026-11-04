"""Ravn background: dark feathers and snow drifting on black, a seamless 10 s loop.

Every motion is periodic in the loop length, so frame 240 equals frame 0.
Drawn by this program; no image or video model, no game art.
"""
import math, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter

OUT = sys.argv[1]
W, H, FPS, SECONDS = 1280, 720, 24, 10
N = FPS * SECONDS
TAU = 2 * math.pi
rng = random.Random(1849)


def feather_sprite(length, width, tone, curl):
    """A soft contour feather, pointing up: bare quill, down at the base,
    an asymmetric vane with a rounded tip and a few ragged splits."""
    K = 3
    lr = random.Random(int(length * 1000 + width * 7))
    w, h = int(width * 3.0 * K), int(length * 1.15 * K)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, base, tip = w * 0.5, h * 0.96, h * 0.05
    def shaft(t):
        return (cx + curl * width * K * 0.5 * math.sin(math.pi * t * 0.9), base + (tip - base) * t)
    r, g, b = tone
    vane0 = 0.24
    for side, wide in ((1, 1.0), (-1, 0.58)):
        splits = {lr.randint(8, 40) for _ in range(2)}
        for j in range(64):
            u = j / 63
            t = vane0 + (0.985 - vane0) * u
            # Broad body, rounded tip: the half width eases off only near the end.
            half = width * K * wide * (math.sin(math.pi * min(1.0, 0.12 + u)) ** 0.35) * (1 - 0.85 * u ** 4)
            if any(abs(j - k) < 2 for k in splits):
                half *= 0.7
            x0, y0 = shaft(t)
            lean = 0.13 * length * K * (0.8 + 0.4 * u)
            x1 = x0 + side * half * lr.uniform(0.92, 1.04)
            y1 = y0 - lean
            mid = ((x0 + x1) / 2 + side * 1.5 * K, (y0 + y1) / 2 + lean * 0.12)
            alpha = int(120 + 90 * (1 - u) * (0.7 + 0.3 * lr.random()))
            d.line([(x0, y0), mid, (x1, y1)], fill=(r, g, b, alpha), width=max(1, int(1.3 * K)), joint="curve")
    # Down: short, loose, curling barbs on the lower vane and quill.
    for j in range(26):
        t = 0.08 + 0.2 * j / 25
        x0, y0 = shaft(t)
        for side in (1, -1):
            ln = width * K * lr.uniform(0.5, 1.0) * (0.6 if side < 0 else 1.0)
            ang = math.radians(lr.uniform(25, 70))
            x1, y1 = x0 + side * ln * math.sin(ang), y0 - ln * math.cos(ang)
            x2, y2 = x1 + side * ln * 0.3 * lr.uniform(-1, 1), y1 + ln * 0.25
            d.line([(x0, y0), (x1, y1), (x2, y2)], fill=(r, g, b, 70), width=max(1, int(1.0 * K)), joint="curve")
    d.line([shaft(i / 50) for i in range(51)], fill=(min(255, r + 30), min(255, g + 30), min(255, b + 30), 225),
           width=max(1, int(1.6 * K)), joint="curve")
    im = im.filter(ImageFilter.GaussianBlur(0.7 * K))
    return im.resize((w // K, h // K), Image.LANCZOS)


# Three depths: far (small, blurred, dim), middle, near (large, soft focus).
layers = [
    dict(count=22, size=(30, 46), blur=2.0, alpha=0.40, fall=(1, 1), flakes=45),
    dict(count=12, size=(64, 96), blur=0.4, alpha=0.82, fall=(1, 1), flakes=25),
    dict(count=4, size=(140, 190), blur=7.0, alpha=0.50, fall=(1, 1), flakes=6),
]
TONES = [(205, 207, 214), (186, 188, 198), (222, 220, 214), (150, 152, 164)]

particles = []
for depth, layer in enumerate(layers):
    for i in range(layer["count"]):
        length = rng.uniform(*layer["size"])
        sprite = feather_sprite(length, length * 0.24, rng.choice(TONES), rng.uniform(-0.6, 0.6))
        if layer["blur"]:
            sprite = sprite.filter(ImageFilter.GaussianBlur(layer["blur"]))
        particles.append(dict(
            kind="feather", sprite=sprite, alpha=layer["alpha"] * rng.uniform(0.75, 1.0),
            x=rng.uniform(-60, W + 60), y=rng.uniform(0, 1),
            loops=rng.randint(*layer["fall"]),           # whole screen crossings per loop
            sway=rng.uniform(18, 55) * (1 + depth * 0.4), sway_k=rng.randint(1, 3), sway_p=rng.uniform(0, TAU),
            spin=rng.uniform(25, 70), spin_k=rng.randint(1, 3), spin_p=rng.uniform(0, TAU), tilt=rng.uniform(-40, 40),
            flip_k=rng.randint(1, 2), flip_p=rng.uniform(0, TAU), depth=depth))
    for i in range(layer["flakes"]):
        particles.append(dict(
            kind="flake", r=rng.uniform(0.8, 1.8) * (1 + depth * 1.6), alpha=layer["alpha"] * rng.uniform(0.35, 0.8),
            x=rng.uniform(0, W), y=rng.uniform(0, 1), loops=rng.randint(1, 2 + (depth == 1)),
            sway=rng.uniform(6, 20), sway_k=rng.randint(1, 3), sway_p=rng.uniform(0, TAU),
            blur=layer["blur"] + 0.6, depth=depth))
particles.sort(key=lambda p: p["depth"])

# Background: near black with a faint cold glow low in the frame, and a vignette.
# Smooth analytic gradients plus a little fixed grain, so no bands show.
import numpy as np
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
nx, ny = (xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)
glow = np.exp(-((nx / 0.75) ** 2 + ((ny - 0.85) / 0.6) ** 2))
vig = np.clip(1.0 - 0.55 * (nx ** 2 * 0.6 + ny ** 2 * 0.8), 0, 1) ** 1.4
base = np.array([9, 9, 11], np.float32)
cold = np.array([30, 34, 44], np.float32)
img = (base + (cold - base) * glow[..., None]) * vig[..., None]
img += np.random.default_rng(7).normal(0, 0.9, img.shape).astype(np.float32)
bg = Image.fromarray(np.clip(img + 0.5, 0, 255).astype(np.uint8), "RGB")

flake_cache = {}
def flake(r, blur):
    key = (round(r, 1), round(blur, 1))
    if key not in flake_cache:
        s = int(r * 4 + blur * 6 + 6)
        im = Image.new("L", (s, s), 0)
        ImageDraw.Draw(im).ellipse([s / 2 - r, s / 2 - r, s / 2 + r, s / 2 + r], fill=255)
        flake_cache[key] = im.filter(ImageFilter.GaussianBlur(blur))
    return flake_cache[key]

ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                       "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
                       "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
span = H + 200
for f in range(N):
    ph = f / N                                       # 0..1, periodic
    frame = bg.copy().convert("RGBA")
    for p in particles:
        y = ((p["y"] + p["loops"] * ph) % 1.0) * span - 100
        x = p["x"] + p["sway"] * math.sin(TAU * p["sway_k"] * ph + p["sway_p"])
        if p["kind"] == "flake":
            m = flake(p["r"], p["blur"])
            layer = Image.new("RGBA", m.size, (226, 230, 238, 0))
            layer.putalpha(m.point(lambda v, a=p["alpha"]: int(v * a)))
            frame.alpha_composite(layer, (int(x - m.size[0] / 2), int(y - m.size[1] / 2)))
            continue
        angle = p["tilt"] + p["spin"] * math.sin(TAU * p["spin_k"] * ph + p["spin_p"])
        squash = 0.55 + 0.45 * abs(math.cos(TAU * p["flip_k"] * ph + p["flip_p"]))   # turning in the air
        s = p["sprite"]
        s = s.resize((max(1, int(s.size[0] * squash)), s.size[1]), Image.BICUBIC).rotate(angle, Image.BICUBIC, expand=True)
        a = s.getchannel("A").point(lambda v, k=p["alpha"]: int(v * k))
        s.putalpha(a)
        frame.alpha_composite(s, (int(x - s.size[0] / 2), int(y - s.size[1] / 2)))
    ff.stdin.write(frame.convert("RGB").tobytes())
ff.stdin.close()
ff.wait()
print("frames", N, "->", OUT)
