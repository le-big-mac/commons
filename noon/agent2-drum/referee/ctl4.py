# Two layers at fixed added mass, followed downward in mass from the mass-2.0 answer (continuation).  Run: python -I -B ctl4.py
import sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent2/drum/referee')
import numpy as np
from scipy.optimize import minimize
from mem import *
t0 = time.time()
def two(p, M0, N=800):
    f, k1, k2 = p
    if not (0 <= f <= 1 and 0.05 <= k2 and k2 + 1e-3 < k1 <= 0.95): return 9.0
    return miss(ratios(layers([f * M0 / k1 ** 2, (1 - f) * M0 / k2 ** 2], [k1, k2]), [k1, k2], N))
x = np.array([9.93 * 0.427 ** 2 / 2.0, 0.427, 0.223])
for M0 in [2.0, 1.9, 1.8, 1.7, 1.6, 1.5, 1.433, 1.3, 1.2, 1.0]:
    for rep in range(3):
        r = minimize(lambda p: two(p, M0), x, method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-10, maxiter=500, initial_simplex=x + np.vstack([np.zeros(3), np.diag([0.02, 0.004, 0.004])])))
        x = r.x
    f, k1, k2 = x
    rr = ratios(layers([f * M0 / k1 ** 2, (1 - f) * M0 / k2 ** 2], [k1, k2]), [k1, k2], 3000, rich=True)
    print('added mass %.3f: miss %.4f : +%.2f inside %.4f and +%.2f inside %.4f ; cents %s' % (M0, miss(rr), f * M0 / k1 ** 2, k1, (1 - f) * M0 / k2 ** 2, k2, np.round(1200 * np.log2(rr[1:] / TARGET[1:]), 0)))
print('time %.0fs' % (time.time() - t0))
