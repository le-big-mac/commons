"""windows.py -- window means of my open-reach runs: L/dist, L/LX, distance between the ends.
usage: python -I windows.py run.out [...]"""
import sys, numpy as np
for f in sys.argv[1:]:
    r = np.array([[float(v) for v in l.split()] for l in open(f) if l.strip() and not l.startswith("#")])
    t = r[:, 0]
    out = []
    for lo, hi in ((12.5, 125), (125.5, 250), (250, 500)):
        m = (t >= lo - 1e-9) & (t <= hi + 1e-9)
        if m.sum() == 0 or t[-1] < hi - 1e-9: continue
        out.append("t %g-%g: L/dist %.3f  L/LX %.3f  dist mean %.0f (min %.0f max %.0f)" % (lo, hi, r[m, 3].mean(), r[m, 6].mean(), r[m, 2].mean(), r[m, 2].min(), r[m, 2].max()))
    print(f, "| last t %.1f dist %.1f end (%.0f, %.0f)" % (t[-1], r[-1, 2], r[-1, 7], r[-1, 8]))
    for o in out: print("    ", o)
