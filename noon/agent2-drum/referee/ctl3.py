# Two layers held at a given total added mass M (in bare skins): differential evolution, then polish.  Run: python -I -B ctl3.py M seed
import sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent2/drum/referee')
import numpy as np
from scipy.optimize import differential_evolution, minimize
from mem import *
M0 = float(sys.argv[1]); seed = int(sys.argv[2]); t0 = time.time()
def two(p, N=300):
    f, k1, k2 = p                       # f = share of the added mass in the outer (wider) disc
    if not (0 <= f <= 1 and 0.05 <= k2 and k2 + 1e-3 < k1 <= 0.95): return 9.0
    a1 = f * M0 / k1 ** 2; a2 = (1 - f) * M0 / k2 ** 2
    return miss(ratios(layers([a1, a2], [k1, k2]), [k1, k2], N))
de = differential_evolution(two, [(0, 1), (0.05, 0.95), (0.05, 0.95)], seed=seed, popsize=25, maxiter=120, tol=1e-9, polish=False, init='sobol')
r = minimize(lambda p: two(p, 1500), de.x, method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-10, maxiter=400, initial_simplex=de.x + np.vstack([np.zeros(3), np.diag([0.02, 0.004, 0.004])])))
f, k1, k2 = r.x
print('two layers, added mass %.3f skins: least miss %.4f (DE at 300: %.4f; N=3000: %.4f): +%.2f inside %.4f and +%.2f inside %.4f   [%d evals, %.0fs]'
      % (M0, r.fun, de.fun, two(r.x, 3000), f * M0 / k1 ** 2, k1, (1 - f) * M0 / k2 ** 2, k2, de.nfev, time.time() - t0))
