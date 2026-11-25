# Fit circles to the ring boundaries in the upper half of plate I (n402.jpg).
import sys
import numpy as np
from PIL import Image, ImageFilter
p = sys.argv[1]
im = Image.open(p).convert('L')
a = np.asarray(im).astype(float)
H, W = a.shape
ink = (255 - a) / 255.0
dark = (a < 150).astype(float)
# dilate dark by 1 px (3x3 max) to tolerate sub-pixel misfit
d = dark.copy()
for dy in (-1, 0, 1):
    for dx in (-1, 0, 1):
        d = np.maximum(d, np.roll(np.roll(dark, dy, 0), dx, 1))

def score(cx, cy, r, th0=12, th1=168, use=d):
    th = np.radians(np.arange(th0, th1, 0.2))
    x = cx + r * np.cos(th)
    y = cy - r * np.sin(th)
    ok = (x >= 0) & (x < W - 1) & (y >= 0) & (y < H - 1)
    xi = np.rint(x[ok]).astype(int)
    yi = np.rint(y[ok]).astype(int)
    if ok.sum() < 50:
        return 0.0
    return use[yi, xi].mean()

cx0, cy0 = 774.0, 1340.0
# coarse radial profile
rs = np.arange(20, 830, 1.0)
prof = np.array([score(cx0, cy0, r) for r in rs])
cand = []
for i in range(2, len(rs) - 2):
    if prof[i] > 0.6 and prof[i] >= prof[i-2:i+3].max():
        cand.append((rs[i], round(prof[i], 3)))
print('coarse candidates (r px, arc fraction):', cand)

def refine(r0, use=dark, span=8):
    best = (0, None)
    for cx in np.arange(cx0 - span, cx0 + span + .01, 1.0):
        for cy in np.arange(cy0 - span, cy0 + span + .01, 1.0):
            for r in np.arange(r0 - span, r0 + span + .01, 0.5):
                s = score(cx, cy, r, use=use)
                if s > best[0]:
                    best = (s, (cx, cy, r))
    s, (cx, cy, r) = best
    # finer
    for cx2 in np.arange(cx - 1, cx + 1.01, 0.25):
        for cy2 in np.arange(cy - 1, cy + 1.01, 0.25):
            for r2 in np.arange(r - 1, r + 1.01, 0.25):
                s2 = score(cx2, cy2, r2, use=use)
                if s2 > best[0]:
                    best = (s2, (cx2, cy2, r2))
    return best

if len(sys.argv) > 2:
    for r0 in map(float, sys.argv[2:]):
        s, (cx, cy, r) = refine(r0)
        print(f'r0={r0:6.1f}: fit cx={cx:.2f} cy={cy:.2f} r={r:.2f} px  arc fraction={s:.3f}')
