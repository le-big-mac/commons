"""noise2.py -- window means of the author's quiet open reach with noise 1e-9 a step (my copy open_noise.c).  usage: python -I noise2.py"""
import glob, numpy as np
for f in sorted(glob.glob("nz9*_s*.out")):
    r = np.array([[float(v) for v in l.split()] for l in open(f) if l.strip() and not l.startswith("#")]); t = r[:, 0]
    s = "%s last t %.1f:" % (f, t[-1])
    for lo, hi in ((12.5, 125), (250, 500)):
        if t[-1] < hi - 1e-6: continue
        m = (t >= lo) & (t <= hi); s += "  t %g-%g: L/dist %.3f, L/LX %.3f, dist %.0f;" % (lo, hi, r[m, 5].mean(), r[m, 2].mean(), r[m, 6].mean())
    print(s, " dist at last %.0f" % r[-1, 6])
