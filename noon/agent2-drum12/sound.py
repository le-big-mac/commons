"""A sound file: the even disc, the nine-mode ringed skin and a sixteen-mode skin, stroke by stroke, then a slow phrase on the last.
usage: python sound.py drum3.wav     (the same invented decay times and stroke as ../drum/sound2.py; frequencies and strengths are the model's)"""
import sys, json, math
import numpy as np
src = open("../drum/sound2.py").read(); ns = {}; exec(src[:src.index("R = json.load(open(sys.argv[1]))")], ns)
modes_of, stroke, save, SR, D3 = ns['modes_of'], ns['stroke'], ns['save'], ns['SR'], ns['D3']
R = json.load(open("../drum/results.json")); nine = np.array(next(r for r in json.load(open("../drum/chain-free-up.json")) if abs(r['weight'] - 1.43) < 1e-9)['a']); sixteen = np.array(json.load(open("s-sixteen-4.json"))['rings']['40']['a'])
ring = lambda a: (lambda r: 1.0 + a[np.minimum((r * 40).astype(int), 39)])
SKINS = [("disc", lambda r: np.where(r < R['best_k'], R['best_s'], 1.0), 1500), ("nine", ring(nine), 2000), ("sixteen", ring(sixteen), 2000)]
TOP = 7.6          # modes up to 7.6 times the lowest, so that the seventh family is in the sound (the earlier files stopped at 6.6)
M = {name: modes_of(f, top=TOP, N=N) for name, f, N in SKINS}; G = {name: 1 / np.abs(stroke(M[name], D3)).max() for name in M}
for name in M:
    st = sorted(((abs(a_ / math.sqrt(r) * math.exp(-(r / 7.0) ** 2)), r) for r, a_, m in M[name]), reverse=True)[:10]; seven = [(r, m) for r, a_, m in M[name] if 6.5 < r < 7.6]
    print(f"{name:8s} {len(M[name]):2d} modes up to {TOP} times the lowest; the ten strongest when struck at half the radius: " + ", ".join(f"{r:.3f}" for v, r in sorted(st, key=lambda z: z[1])) + "; modes between 6.5 and 7.6: " + (", ".join(f"{r:.3f} (m = {m})" for r, m in seven) if seven else "none"))
SCALE = [D3 * 2 ** (n / 12) for n in (0, 2, 4, 7, 9, 12, 14, 16)]; ev = []
for i in range(3): ev.append((0.5 + 2.0 * i, "disc", D3, 0.8))
for i in range(3): ev.append((7.0 + 2.0 * i, "nine", D3, 0.8))
for i in range(3): ev.append((13.5 + 2.0 * i, "sixteen", D3, 0.8))
for i in range(3): ev.append((20.5 + 3.6 * i, "disc", D3, 0.8)); ev.append((21.7 + 3.6 * i, "nine", D3, 0.8)); ev.append((22.9 + 3.6 * i, "sixteen", D3, 0.8))
rng = np.random.default_rng(2207); t0 = 32.5; idx = 2; beat = 1.05
for bar in range(8):
    ev.append((t0 + bar * 4 * beat, "sixteen", D3, 0.55))
    for b in range(4):
        if bar == 7 and b > 0: break
        if rng.random() < 0.82 or b == 0:
            idx = int(np.clip(idx + rng.choice([-2, -1, -1, 0, 1, 1, 2]), 0, len(SCALE) - 1)); ev.append((t0 + (bar * 4 + b) * beat + (0.5 * beat if rng.random() < 0.18 else 0), "sixteen", SCALE[idx], 0.5))
end = max(e[0] for e in ev) + 5.0; y = np.zeros(int(end * SR))
for t, name, f0, g in ev:
    x = stroke(M[name], f0, gain=g * G[name]); i = int(t * SR); y[i:i + len(x)] += x[:len(y) - i]
y *= 0.85 / np.abs(y).max(); fade = int(2.5 * SR); y[-fade:] *= np.linspace(1, 0, fade); save(sys.argv[1], np.stack([y, y], axis=1), ch=2)
print(f"{len(ev)} strokes; {end:.1f} seconds: the even disc from 0.5 s, the nine-mode ringed skin from 7 s, the sixteen-mode skin from 13.5 s, the three by turns from 20.5 s, a slow pentatonic phrase on sixteen-mode skins from 32.5 s")
