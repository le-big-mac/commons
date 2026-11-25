"""A patch laid on in layers: concentric discs, each adding a load inside its radius.   usage: python layers.py N layers-N.json [SEED STARTS]
60 random starts, each followed downhill; the best kept. Sealed measure: the largest miss of the eight ratios to the lowest mode."""
import sys, json
import numpy as np
from scipy.optimize import minimize
from helpers import fd_modes, tied, NINE, NEXT
n = int(sys.argv[1]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 100 + n; STARTS = int(sys.argv[4]) if len(sys.argv) > 4 else 60; rng = np.random.default_rng(seed)      # the sealed search: seed 100 + n, 60 starts
def unpack(x):
    a = np.clip(x[:n], 0.0, 40.0); k = np.sort(np.clip(x[n:], 0.05, 0.95))[::-1]; return a, k
def rho(x):
    a, k = unpack(x); return lambda r: 1.0 + sum(ai * (r < ki) for ai, ki in zip(a, k))
f = lambda x, N=600: tied(fd_modes(rho(x), N=N))
best = (9.0, None); trail = []
for start in range(STARTS):
    x0 = np.concatenate([rng.uniform(0.5, 15.0, n), rng.uniform(0.1, 0.8, n)]); r = minimize(f, x0, method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-6, maxiter=1500)); trail.append(float(r.fun))
    if r.fun < best[0]: best = (float(r.fun), r.x)
r = minimize(lambda x: f(x, 1500), best[1], method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-8, maxiter=4000)); a, k = unpack(r.x); w = fd_modes(rho(r.x), NINE + NEXT, N=3000); ratios = w / w[0]; miss = tied(w[:9])
print(f"{n} layers: largest miss {100 * miss:.3f}% (3,000 cells); layers (added load inside radius): " + "; ".join(f"{ai:.2f} inside {ki:.3f}" for ai, ki in zip(a, k)))
print("   ratios: " + ", ".join(f"{x:.4f}" for x in ratios[:9]) + "; the next three: " + ", ".join(f"{x:.3f}" for x in ratios[9:]))
print("   in cents from the harmonic: " + ", ".join(f"{1200 * np.log2(x / t):+.0f}" for x, t in zip(ratios[1:9], [2, 3, 3, 4, 4, 5, 5, 5])))
tr = np.sort(trail); print(f"   the {STARTS} starts (seed {seed}) ended at misses from {100 * tr[0]:.2f}% to {100 * tr[-1]:.2f}%; the best five: " + ", ".join(f"{100 * v:.2f}%" for v in tr[:5]) + f"; added mass {sum(ai * ki * ki for ai, ki in zip(a, k)):.2f} times the bare skin's")
json.dump(dict(n=n, a=a.tolist(), k=k.tolist(), miss=miss, ratios=ratios.tolist(), trail=trail), open(sys.argv[2], "w"))
