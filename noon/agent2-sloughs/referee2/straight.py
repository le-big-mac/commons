"""straight.py -- how far from the first node does the river stay within tol of the straight line through its first two nodes?
usage: python -I straight.py file.xy [...]"""
import sys, numpy as np
for f in sys.argv[1:]:
    a = np.loadtxt(f)
    x, y = a[:, 0], a[:, 1]
    d = np.hypot(np.diff(x), np.diff(y)); s = np.concatenate([[0], np.cumsum(d)])
    # line through first node and the node about 5 D downstream
    j = np.searchsorted(s, 5.0)
    tx, ty = x[j] - x[0], y[j] - y[0]; n = np.hypot(tx, ty); tx, ty = tx / n, ty / n
    off = np.abs(-(x - x[0]) * ty + (y - y[0]) * tx)
    out = []
    for tol in (1e-9, 1e-6, 1e-3, 0.1, 1.0):
        k = np.argmax(off > tol) if (off > tol).any() else len(off) - 1
        out.append("%g: %.1f" % (tol, s[k]))
    dist = np.hypot(x[-1] - x[0], y[-1] - y[0])
    print("%s: nodes %d, length %.1f, end-to-end %.1f, ratio %.3f; arc length before the river leaves its first tangent by more than  %s" % (f, len(x), s[-1], dist, s[-1] / dist, ";  ".join(out)))
