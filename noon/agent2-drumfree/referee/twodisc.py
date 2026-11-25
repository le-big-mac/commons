import sys
sys.path.insert(0, "/home/agent2/drumfree/referee")
import numpy as np
from scipy.optimize import minimize
from sol import *
def val(x, mass=1.43):
    so, ko, ki = x
    if not (0.05 < ki < ko < 0.95 and so >= 1): return 1.0
    si = so + (mass - (so - 1) * ko ** 2) / ki ** 2
    if si < so: return 1.0
    f = exact_freqs([ki, ko, 1.0], [si, so, 1.0], N=800)
    return np.abs(misses(f)[0]).max()
r = minimize(val, [6.304, 0.4933, 0.2768], method='Nelder-Mead', options={'xatol': 1e-6, 'fatol': 1e-10, 'maxiter': 400})
so, ko, ki = r.x; si = so + (1.43 - (so - 1) * ko ** 2) / ki ** 2
f = exact_freqs([ki, ko, 1.0], [si, so, 1.0]); ms, pl = misses(f)
print('two discs, exact matching, 1.43 skins, polished from the author\'s: miss %.4f%% outer %.4f times to %.4f, inner %.4f times inside %.4f, place %.4f' % (100 * np.abs(ms).max(), so, ko, si, ki, pl))
