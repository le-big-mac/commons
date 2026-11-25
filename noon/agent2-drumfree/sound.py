"""A sound file: a skin with its lowest mode tuned, and a two-disc skin with its lowest mode left free, heard two ways.
usage: python sound.py drumfree.wav
The recipe is that of ../drum/sound2.py (invented decay times and stroke; frequencies and strengths from the model), with modes up to 7.6
times the note. For the free skins "the note" is half the second mode's frequency. In the third voice the lowest mode alone is made to
die in 0.04 s, because Yonder found that in real strokes it "dies within a few hundredths of a second"; that number is put in by hand."""
import sys, json, math
import numpy as np
src = open("../drum/sound2.py").read(); ns = {}; exec(src[:src.index("R = json.load(open(sys.argv[1]))")], ns)
modes_of, save, SR, D3 = ns['modes_of'], ns['save'], ns['SR'], ns['D3']
nine = np.array(next(r for r in json.load(open("../drum/chain-free-up.json")) if abs(r['weight'] - 1.43) < 1e-9)['a']); two = json.load(open("shape-two-five-1.43.json")); ko, ki = two['radii']; lo = two['share'] * two['used'] / ko ** 2; li = (1 - two['share']) * two['used'] / ki ** 2
skins = {"tuned": (lambda r: 1.0 + nine[np.minimum((r * 40).astype(int), 39)], 2000), "free": (lambda r: np.where(r < ki, 1 + lo + li, np.where(r < ko, 1 + lo, 1.0)), 2000)}
M = {}
for name, (f, N) in skins.items():
    md = modes_of(f, top=8.6, N=N); second = min(r for r, a, m in md if m == 1); unit = 1.0 if name == "tuned" else second / 2          # the note: the lowest mode, or half the second
    M[name] = [(r / unit, a, m) for r, a, m in md if r / unit <= 7.6]
def stroke(modes, f0, dur=3.2, gain=1.0, cut=None):
    t = np.arange(int(dur * SR)) / SR; x = np.zeros_like(t); lowest = min(r for r, a, m in modes)
    for ratio, a, m in modes:
        f = f0 * ratio
        if f > 9000: continue
        tau = cut if (cut is not None and ratio == lowest) else 1.3 * ratio ** -0.8
        x += a / math.sqrt(ratio) * math.exp(-(ratio / 7.0) ** 2) * np.exp(-t / tau) * np.sin(2 * math.pi * f * t)
    return gain * x * np.minimum(1.0, t / 0.004)
VOICE = {"tuned": ("tuned", None), "free": ("free", None), "free, lowest cut": ("free", 0.04)}; G = {v: 1 / np.abs(stroke(M[s], D3, cut=c)).max() for v, (s, c) in VOICE.items()}
for name in M: print(f"{name}: {len(M[name])} modes up to 7.6 times the note; in units of the note: " + ", ".join(f"{r:.3f}" for r, a, m in M[name][:10]) + " ...")
SCALE = [D3 * 2 ** (n / 12) for n in (0, 2, 4, 7, 9, 12, 14, 16)]; ev = []
for i in range(3): ev.append((0.5 + 2.0 * i, "tuned", D3, 0.8))
for i in range(3): ev.append((7.0 + 2.0 * i, "free", D3, 0.8))
for i in range(3): ev.append((13.5 + 2.0 * i, "free, lowest cut", D3, 0.8))
for i in range(3): ev.append((20.5 + 3.6 * i, "tuned", D3, 0.8)); ev.append((21.7 + 3.6 * i, "free", D3, 0.8)); ev.append((22.9 + 3.6 * i, "free, lowest cut", D3, 0.8))
rng = np.random.default_rng(2311); t0 = 32.5; idx = 2; beat = 1.05
for bar in range(8):
    ev.append((t0 + bar * 4 * beat, "free, lowest cut", D3, 0.55))
    for b in range(4):
        if bar == 7 and b > 0: break
        if rng.random() < 0.82 or b == 0:
            idx = int(np.clip(idx + rng.choice([-2, -1, -1, 0, 1, 1, 2]), 0, len(SCALE) - 1)); ev.append((t0 + (bar * 4 + b) * beat + (0.5 * beat if rng.random() < 0.18 else 0), "free, lowest cut", SCALE[idx], 0.5))
end = max(e[0] for e in ev) + 5.0; y = np.zeros(int(end * SR))
for t, v, f0, g in ev:
    s, c = VOICE[v]; x = stroke(M[s], f0, gain=g * G[v], cut=c); i = int(t * SR); y[i:i + len(x)] += x[:len(y) - i]
y *= 0.85 / np.abs(y).max(); fade = int(2.5 * SR); y[-fade:] *= np.linspace(1, 0, fade); save(sys.argv[1], np.stack([y, y], axis=1), ch=2)
print(f"{len(ev)} strokes; {end:.1f} seconds: the ringed skin with its lowest mode tuned from 0.5 s; the two-disc skin with its lowest mode free from 7 s; the same with the lowest mode dying in 0.04 s from 13.5 s; the three by turns from 20.5 s; a slow pentatonic phrase on the last from 32.5 s")
