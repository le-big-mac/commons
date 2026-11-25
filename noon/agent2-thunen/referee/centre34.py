# Fit the outer circle of plate III (left half) and plate IV (right half) on n404.jpg
import sys
import numpy as np
from PIL import Image
a = np.asarray(Image.open(sys.argv[1]).convert('L')).astype(float)
H, W = a.shape
dark = (a < 150).astype(float)
d = dark.copy()
for dy in (-1, 0, 1):
    for dx in (-1, 0, 1):
        d = np.maximum(d, np.roll(np.roll(dark, dy, 0), dx, 1))
def score(cx, cy, r, th0, th1):
    th = np.radians(np.arange(th0, th1, 0.25))      # measured from straight up, clockwise
    x = cx + r * np.sin(th); y = cy - r * np.cos(th)
    ok = (x >= 0) & (x < W - 1) & (y >= 0) & (y < H - 1)
    if ok.sum() < 100: return 0
    return d[np.rint(y[ok]).astype(int), np.rint(x[ok]).astype(int)].mean()
for name, c0, th in (('III', (776, 1329), (-170, -10)), ('IV', (797, 1329), (10, 170))):
    best = (0, None)
    for cx in np.arange(c0[0] - 12, c0[0] + 12.1, 1):
        for cy in np.arange(c0[1] - 14, c0[1] + 14.1, 1):
            for r in np.arange(755, 800, 1):
                s = score(cx, cy, r, *th)
                if s > best[0]: best = (s, (cx, cy, r))
    print(name, 'outer circle: centre', best[1][:2], 'radius', best[1][2], 'px; arc fraction', round(best[0], 3))
