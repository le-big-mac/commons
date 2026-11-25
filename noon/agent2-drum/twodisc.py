"""Two even discs, one on the other, with both edges on ring edges and a fixed added mass: the least largest miss, on the same 40 rings
and 2,000 cells as the piled discs of exact5.py, so that the two can be compared at equal weight on equal terms.
usage: python -u twodisc.py WEIGHT     (one weight a run; prints one line; unregistered)"""
import sys, json
import numpy as np
from scipy.optimize import minimize_scalar
src = open(__file__.replace("twodisc.py", "exact.py")).read(); ns = {}; exec(src[:src.index("rng = np.random.default_rng(40)")], ns)
EDGE, AREA, discs = ns['EDGE'], ns['AREA'], ns['discs']; miss = lambda a: float(np.abs(ns['misses'](a)).max()); out = []
for M in (float(sys.argv[1]),):
    best = None
    for j2 in range(8, 29):                                        # the wider disc's edge, 0.2 to 0.7
        for j1 in range(2, j2):                                    # the narrower disc's edge
            k1, k2 = EDGE[j1], EDGE[j2]; f = lambda p: miss(discs([p * M / k1 ** 2, (1 - p) * M / k2 ** 2], [k1, k2]))     # p: the share of the added mass in the upper, narrower disc
            ps = np.linspace(0, 1, 11); v = [f(p) for p in ps]; i = int(np.argmin(v)); r = minimize_scalar(f, bounds=(ps[max(i - 1, 0)], ps[min(i + 1, 10)]), method='bounded', options=dict(xatol=1e-4)); p, t = (r.x, r.fun) if r.fun < v[i] else (ps[i], v[i])
            if best is None or t < best[0]: best = (t, k1, k2, p)
    t, k1, k2, p = best; out.append(dict(weight=M, miss=t, k1=float(k1), k2=float(k2), upper_share=float(p)))
    print(f"added mass {M:5.2f}: two discs on ring edges, least largest miss {100 * t:.3f}% (+{(1 - p) * M / k2 ** 2:.1f} inside {k2:.3f} and +{p * M / k1 ** 2:.1f} more inside {k1:.3f})", flush=True)
