"""noise.py -- the author's open.c (copied, with a -noise option added by me), quiet inlet, seed 1, to t = 125:
mean of length/distance over t = 12.5 to 125, and the length of the straight head at t = 125, against the noise given.
usage: python -I noise.py"""
import numpy as np
for nz in ("0", "1e-12", "1e-9", "1e-6"):
    r = np.array([[float(v) for v in l.split()] for l in open("nz_%s.out" % nz) if l.strip() and not l.startswith("#")]); t = r[:, 0]
    m = (t >= 12.5) & (t <= 125)
    xy = None
    for line in open("nz_%s.snap" % nz):
        f = line.split()
        if abs(float(f[0]) - 125) < 1e-6: xy = np.array(f[2:], float).reshape(-1, 2)
    x, y = xy[:, 0] - xy[0, 0], xy[:, 1] - xy[0, 1]
    s = np.concatenate([[0], np.cumsum(np.hypot(np.diff(x), np.diff(y)))])
    j = np.searchsorted(s, 5.0); tx, ty = x[j], y[j]; n = np.hypot(tx, ty)
    off = np.abs(-x * ty + y * tx) / n
    k = np.argmax(off > 1.0)
    print("noise sd %-6s per step: last t %.1f; mean L/dist over 12.5-125 = %.3f (L/LX %.3f); at t = 125 L/dist = %.2f, dist = %.0f; straight head (within 1 D of its first tangent) = %.0f D of river" % (
        nz, t[-1], r[m, 5].mean(), r[m, 2].mean(), r[-1, 5], r[-1, 6], s[k]))
