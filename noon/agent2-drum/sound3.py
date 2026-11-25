"""A second sound file: the best even disc and the ringed load of the same weight, stroke by stroke, then a slow phrase on ringed skins.
usage: python sound3.py results.json chain-free-up.json drum2.wav
The same invented decay times and stroke as sound2.py; the frequencies and the strength of each mode at the striking point are the model's."""
import sys, json, math
import numpy as np
src = open(__file__.replace("sound3.py", "sound2.py")).read(); ns = {}; exec(src[:src.index("R = json.load(open(sys.argv[1]))")], ns)
modes_of, stroke, save, SR, D3 = ns['modes_of'], ns['stroke'], ns['save'], ns['SR'], ns['D3']
R = json.load(open(sys.argv[1])); a = np.array(next(r for r in json.load(open(sys.argv[2])) if abs(r['weight'] - 1.43) < 1e-9)['a'])
SKINS = [("disc", lambda r: np.where(r < R['best_k'], R['best_s'], 1.0)), ("rings", lambda r: 1.0 + a[np.minimum((r * 40).astype(int), 39)])]
# 2,000 cells for the rings, so that every ring's edge falls on a cell's edge
M = {name: modes_of(f, N=1500 if name == 'disc' else 2000) for name, f in SKINS}; G = {name: 1 / np.abs(stroke(M[name], D3)).max() for name in M}
for name in M:
    st = sorted(((abs(a_ / math.sqrt(r) * math.exp(-(r / 7.0) ** 2)), r) for r, a_, m in M[name]), reverse=True)[:8]
    print(f"{name:6s} {len(M[name]):2d} modes up to 6.6 times the lowest; the eight strongest when struck at half the radius: " + ", ".join(f"{r:.3f}" for v, r in sorted(st, key=lambda z: z[1])))
SCALE = [D3 * 2 ** (n / 12) for n in (0, 2, 4, 7, 9, 12, 14, 16)]; ev = []
for i in range(3): ev.append((0.5 + 2.0 * i, "disc", D3, 0.8))
for i in range(3): ev.append((7.0 + 2.0 * i, "rings", D3, 0.8))
for i in range(3): ev.append((13.5 + 2.4 * i, "disc", D3, 0.8)); ev.append((14.7 + 2.4 * i, "rings", D3, 0.8))
rng = np.random.default_rng(1947); t0 = 22.0; idx = 2; beat = 1.05
for bar in range(8):
    ev.append((t0 + bar * 4 * beat, "rings", D3, 0.55))
    for b in range(4):
        if bar == 7 and b > 0: break
        if rng.random() < 0.82 or b == 0:
            idx = int(np.clip(idx + rng.choice([-2, -1, -1, 0, 1, 1, 2]), 0, len(SCALE) - 1)); ev.append((t0 + (bar * 4 + b) * beat + (0.5 * beat if rng.random() < 0.18 else 0), "rings", SCALE[idx], 0.5))
end = max(e[0] for e in ev) + 5.0; y = np.zeros(int(end * SR))
for t, name, f0, g in ev:
    x = stroke(M[name], f0, gain=g * G[name]); i = int(t * SR); y[i:i + len(x)] += x[:len(y) - i]
y *= 0.85 / np.abs(y).max(); fade = int(2.5 * SR); y[-fade:] *= np.linspace(1, 0, fade); save(sys.argv[3], np.stack([y, y], axis=1), ch=2)
print(f"{len(ev)} strokes; {end:.1f} seconds: the even disc from 0.5 s, the ringed load of the same weight from 7 s, the two by turns from 13.5 s, a slow pentatonic phrase on ringed skins from 22 s")
