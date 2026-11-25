"""near.py -- how much river lies within R of the first node, and the turning of the river's direction over its first 60 D of length.
usage: python -I near.py file.xy [...]"""
import sys, numpy as np
for f in sys.argv[1:]:
    a = np.loadtxt(f); x, y = a[:, 0] - a[0, 0], a[:, 1] - a[0, 1]
    d = np.hypot(np.diff(x), np.diff(y)); r = np.hypot(x, y)[1:]
    th = np.unwrap(np.arctan2(np.diff(y), np.diff(x))); s = np.cumsum(d)
    ang = np.unwrap(np.arctan2(y[1:], x[1:]))
    print(f, " river within 10, 20, 40 D of the first node: %.0f, %.0f, %.0f;  greatest winding of the river about the first node: %.2f turns" % (d[r < 10].sum(), d[r < 20].sum(), d[r < 40].sum(), (ang.max() - ang.min()) / (2 * np.pi)))
