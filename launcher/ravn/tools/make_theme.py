"""Ravn theme: an original slow melody in D Dorian, synthesized here.

A plucked string (Karplus-Strong, a lyre-like tone) over a soft open-fifth
drone, with a simple room reverb. Nobody was recorded, nothing was sampled,
and no music model was used. The melody was written for this launcher.
"""
import subprocess, sys
import numpy as np

OUT = sys.argv[1]
SR = 44100
BPM = 58
BEAT = 60 / BPM
rng = np.random.default_rng(1874)

NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def hz(name):
    letter, octave = name[0], int(name[-1])
    shift = 1 if "#" in name else (-1 if name[1:-1] == "b" else 0)
    midi = 12 * (octave + 1) + NOTE[letter] + shift
    return 440.0 * 2 ** ((midi - 69) / 12)

# (note, beats). "-" is a rest. Four phrases of four bars, then a closing bar.
MELODY = [
    # A: rising call
    ("D4", 1.5), ("E4", 0.5), ("F4", 1), ("A4", 1),
    ("G4", 2), ("F4", 1), ("E4", 1),
    ("D4", 1), ("F4", 1), ("A4", 1.5), ("C5", 0.5),
    ("A4", 4),
    # B: reaching up, B natural for the Dorian colour
    ("A4", 1), ("B4", 1), ("C5", 1.5), ("D5", 0.5),
    ("E5", 2), ("D5", 1), ("C5", 1),
    ("A4", 1.5), ("G4", 0.5), ("F4", 1), ("G4", 1),
    ("A4", 4),
    # A': the call again, answered lower
    ("D4", 1.5), ("E4", 0.5), ("F4", 1), ("A4", 1),
    ("C5", 2), ("A4", 1), ("G4", 1),
    ("F4", 1), ("E4", 1), ("C4", 1.5), ("E4", 0.5),
    ("D4", 4),
    # C: a quiet coda
    ("A3", 1), ("D4", 1), ("E4", 1), ("F4", 1),
    ("E4", 1.5), ("C4", 0.5), ("D4", 2),
    ("-", 4),
]

def pluck(freq, seconds, bright=0.5):
    """Karplus-Strong with an allpass for the fractional delay (Jaffe and Smith),
    so every note is in tune, not only those whose period is a whole sample count."""
    n = int(seconds * SR)
    period = SR / freq
    N = int(np.floor(period - 0.5 - 1e-3))       # the two-point average adds 0.5 sample
    frac = period - 0.5 - N
    C = (1 - frac) / (1 + frac)
    buf = rng.uniform(-1, 1, N)
    for _ in range(2):                            # a warm, lyre-like excitation
        buf = 0.5 * (buf + np.roll(buf, 1))
    buf -= buf.mean()
    decay = 0.996 + 0.0025 * bright
    out = np.zeros(n)
    prev = 0.0
    ap_x = ap_y = 0.0
    for i in range(n):
        val = buf[i % N]
        out[i] = val
        avg = decay * 0.5 * (val + prev)
        prev = val
        ap = C * avg + ap_x - C * ap_y           # first-order allpass
        ap_x, ap_y = avg, ap
        buf[i % N] = ap
    env = np.minimum(1, np.arange(n) / (0.004 * SR))
    return out * env

def drone(seconds):
    t = np.arange(int(seconds * SR)) / SR
    wave = np.zeros_like(t)
    for f, amp in ((hz("D2"), 1.0), (hz("A2"), 0.7), (hz("D3"), 0.35)):
        for k, ak in ((1, 1.0), (2, 0.25), (3, 0.08)):
            wave += amp * ak * np.sin(2 * np.pi * f * k * t + rng.uniform(0, 6.28))
    swell = 0.55 + 0.45 * np.sin(2 * np.pi * t / (16 * BEAT) - np.pi / 2)
    fade = np.minimum(1, t / 3.0) * np.minimum(1, (t[-1] - t) / 4.0)
    return wave * swell * fade

total_beats = sum(b for _, b in MELODY)
length = total_beats * BEAT + 3.0
mel = np.zeros(int(length * SR) + SR)
pos = 0.0
for name, beats in MELODY:
    if name != "-":
        ring = beats * BEAT + 1.8
        tone = pluck(hz(name), ring, bright=0.4)
        tone *= 0.9 if name[-1] == "4" else 0.75
        start = int(pos * SR)
        mel[start:start + len(tone)] += tone
        # A soft octave-lower ghost on long notes, like a second string.
        if beats >= 2:
            low = pluck(hz(name) / 2, ring, bright=0.1) * 0.28
            mel[start + 300:start + 300 + len(low)] += low[: len(mel) - start - 300]
    pos += beats * BEAT
mel = mel[: int(length * SR)]

dr = drone(length) * 0.09
dry = mel * 0.5 + dr

# Room reverb: decaying noise impulse, separate for each ear.
def reverb(x, seed):
    r = np.random.default_rng(seed)
    n = int(2.6 * SR)
    ir = r.normal(0, 1, n) * np.exp(-np.arange(n) / (0.55 * SR))
    ir[: int(0.012 * SR)] = 0
    ir /= np.sqrt(np.sum(ir ** 2))
    m = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[: len(x)]
    return y

left = dry + 0.42 * reverb(dry, 1)
right = dry + 0.42 * reverb(dry, 2)
stereo = np.stack([left, right], axis=1)
stereo /= np.max(np.abs(stereo)) / 0.8
fade = np.minimum(1, np.arange(len(stereo)) / (0.05 * SR))[:, None] * \
       np.minimum(1, (len(stereo) - np.arange(len(stereo))) / (2.5 * SR))[:, None]
stereo *= fade
pcm = (stereo * 32767).astype("<i2").tobytes()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-",
                "-c:a", "libmp3lame", "-b:a", "128k", OUT], input=pcm, check=True)
print(f"{length:.1f} s ->", OUT)
