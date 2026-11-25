# Blind item 4: two concentric discs, each adding a load a (0..40) inside radius k (0.05..0.95).
# Run: python -I blind4.py seed [nlayers]
import sys, time
sys.path.insert(0, '/home/agent2/drum/referee')
import numpy as np
from scipy.optimize import differential_evolution, minimize
from mem import *

seed = int(sys.argv[1])
L = int(sys.argv[2]) if len(sys.argv) > 2 else 2
maxit = int(sys.argv[3]) if len(sys.argv) > 3 else 120
t0 = time.time()
lo = np.array([0.0] * L + [0.05] * L)
hi = np.array([40.0] * L + [0.95] * L)


def obj(p, N=300):
    p = np.asarray(p)
    if np.any(p < lo) or np.any(p > hi):
        return 9.0
    a, k = p[:L], p[L:]
    return miss(ratios(layers(a, k), list(k), N))


de = differential_evolution(obj, list(zip(lo, hi)), seed=seed, popsize=18, maxiter=maxit, tol=1e-9, polish=False, init='sobol')
best = de
for N in (800, 2000):
    nm = minimize(lambda p: obj(p, N), best.x, method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-9, maxiter=600 if N == 800 else 250,
                  initial_simplex=best.x + np.vstack([np.zeros(2 * L), np.diag([0.3] * L + [0.01] * L)])))
    best = nm
a, k = best.x[:L], best.x[L:]
rb = ratios(layers(a, k), list(k), 3000, rich=True)
print('seed %d layers %d: DE miss(N=300)=%.5f after %d evals; polished miss=%.5f (Richardson %.5f); loads %s radii %s; ratios %s; time %.0fs'
      % (seed, L, de.fun, de.nfev, best.fun, miss(rb), np.round(a, 3), np.round(k, 4), np.round(rb, 4), time.time() - t0))
