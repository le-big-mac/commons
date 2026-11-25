# Wider circle search for the three big circles of plate I; also outer-edge least-squares fit.
import sys
import numpy as np
from PIL import Image
p = sys.argv[1]
a = np.asarray(Image.open(p).convert('L')).astype(float)
H, W = a.shape
dark = (a < 150).astype(float)
d = dark.copy()
for dy in (-1, 0, 1):
    for dx in (-1, 0, 1):
        d = np.maximum(d, np.roll(np.roll(dark, dy, 0), dx, 1))

def score(cx, cy, r, use, th0=12, th1=168):
    th = np.radians(np.arange(th0, th1, 0.2))
    x = cx + r * np.cos(th); y = cy - r * np.sin(th)
    ok = (x >= 0) & (x < W - 1) & (y >= 0) & (y < H - 1)
    if ok.sum() < 50: return 0.0
    return use[np.rint(y[ok]).astype(int), np.rint(x[ok]).astype(int)].mean()

def search(r0, use, c0=(774., 1338.), sc=14, sr=14, step=1.0):
    best = (0, None)
    for cx in np.arange(c0[0] - sc, c0[0] + sc + .01, step):
        for cy in np.arange(c0[1] - sc, c0[1] + sc + .01, step):
            for r in np.arange(r0 - sr, r0 + sr + .01, step):
                s = score(cx, cy, r, use)
                if s > best[0]: best = (s, (cx, cy, r))
    s, (cx, cy, r) = best
    for cx2 in np.arange(cx - 1, cx + 1.01, 0.25):
        for cy2 in np.arange(cy - 1, cy + 1.01, 0.25):
            for r2 in np.arange(r - 1, r + 1.01, 0.25):
                s2 = score(cx2, cy2, r2, use)
                if s2 > best[0]: best = (s2, (cx2, cy2, r2))
    return best

for r0 in map(float, sys.argv[2:]):
    s, (cx, cy, r) = search(r0, d)
    print(f'r0={r0:6.1f}: dilated-map fit cx={cx:.2f} cy={cy:.2f} r={r:.2f}  arc fraction={s:.3f}')
