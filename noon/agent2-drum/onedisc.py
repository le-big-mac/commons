"""The best one even disc at each added mass, by exact matching of Bessel functions (drum.py): the radius is searched, the load follows.
usage: python onedisc.py onedisc.json     (unregistered; the third column of the weight table)"""
import sys, json
import numpy as np
from scipy.optimize import minimize_scalar
import drum
out = []
for M in (1.0, 1.1, 1.2, 1.3, 1.36, 1.4, 1.43, 1.46, 1.5, 1.6, 1.7, 2.0, 2.79, 4.0, 6.0, 9.6, 12.0):
    f = lambda k: drum.miss(1 + M / k ** 2, k); ks = np.arange(0.25, 0.6501, 0.005); v = [f(k) for k in ks]; j = int(np.argmin(v))
    r = minimize_scalar(f, bounds=(ks[max(j - 1, 0)], ks[min(j + 1, len(ks) - 1)]), method='bounded', options=dict(xatol=1e-6)); k, t = (r.x, r.fun) if r.fun < v[j] else (ks[j], v[j])
    out.append(dict(weight=M, miss=float(t), k=float(k), s=float(1 + M / k ** 2))); print(f"added mass {M:5.2f}: the best one even disc is {1 + M / k ** 2:6.2f} times the skin over {k:.3f} of the radius; largest miss {100 * t:.3f}%", flush=True)
json.dump(out, open(sys.argv[1], "w"))
