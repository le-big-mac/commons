"""Small controls on discs: place against weight at a fixed radius; the tuned disc in this study's measure."""
import sys
sys.path.insert(0, "/home/agent2/drumfree/referee")
import numpy as np
from scipy.optimize import minimize
from sol import *

print('A. one disc: the lowest mode\'s place (and overtone miss) against weight at a fixed radius')
for k in (0.40, 0.45, 0.50, 0.55):
    row = []
    for s in (2.5, 4.34, 6.25, 8, 10, 16):
        f = exact_freqs([k, 1.0], [s, 1.0], N=800)
        ms, pl = misses(f)
        row.append('s=%g: %.3f (%.1f%%)' % (s, pl, 100 * np.abs(ms).max()))
    print('  k=%.2f  ' % k + '; '.join(row))

print('B. named discs in this study\'s measure (seven overtones against half the second mode), and all eight with the lowest at 1')
for nm_, s, k in [('9.94 over 0.400', 9.94, 0.400), ('9.77 over 0.4', 9.77, 0.4), ('4.343 over 0.5042', 4.343, 0.5042)]:
    f = exact_freqs([k, 1.0], [s, 1.0])
    ms, pl = misses(f)
    m8, _ = misses(f, with_low=True)
    low = f[(0, 1)]
    first = max(abs(f[kk] / (t * low) - 1) for kk, t in [((1, 1), 2)] + SEVEN)
    print('  %-18s seven overtones %.3f%%; eight with the lowest at 1: %.3f%%; first study\'s measure (lowest is the note): %.3f%%; place %.4f' % (nm_, 100 * np.abs(ms).max(), 100 * np.abs(m8).max(), 100 * first, pl))

print('C. the best one disc with the lowest mode tuned, in this study\'s measure (largest of eight misses, note = half the second)')
fem = Fem(400)
res = []
for s in np.arange(1, 60.01, 0.5):
    for k in np.arange(0.05, 0.9501, 0.0125):
        f = fem_freqs(fem, rho_elements(fem, [k, 1.0], [s, 1.0]))
        res.append((np.abs(misses(f, with_low=True)[0]).max(), s, k))
res.sort()


def obj(x):
    s, k = x
    if not (1 <= s <= 60 and 0.05 <= k <= 0.95):
        return 1.0
    return np.abs(misses(exact_freqs([k, 1.0], [s, 1.0], N=800), with_low=True)[0]).max()


r = minimize(obj, [res[0][1], res[0][2]], method='Nelder-Mead', options={'xatol': 1e-5, 'fatol': 1e-9})
f = exact_freqs([r.x[1], 1.0], [r.x[0], 1.0])
ms, pl = misses(f)
print('  grid best %.3f%% at (%.2f, %.4f); polished %.4f%% at %.3f times over %.4f; its seven overtones alone %.3f%%; place %.4f' % (
    100 * res[0][0], res[0][1], res[0][2], 100 * r.fun, r.x[0], r.x[1], 100 * np.abs(ms).max(), pl))
