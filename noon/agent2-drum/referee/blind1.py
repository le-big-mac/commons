# Blind items 1-3.  Run: python -I blind1.py
import sys, time
sys.path.insert(0, '/home/agent2/drum/referee')
import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.special import jn_zeros
from mem import *

t0 = time.time()
np.set_printoptions(precision=5, suppress=True, linewidth=200)
P = print

# 1. even skin
one = lambda x: np.ones_like(x)
r = ratios(one, [], 2000, rich=True)
ex = np.array([jn_zeros(m, n)[n - 1] for m, n in MODES])
ex = ex / ex[0]
P('ITEM 1 even skin, nine ratios (FE, Richardson):', r)
P('        exact Bessel zeros                   :', ex)
P('        max |FE - exact| = %.2e ; largest miss even skin = %.4f' % (np.abs(r - ex).max(), miss(ex)))

# 2a. ratio of (1,1) at s=4
P('ITEM 2a ratio of (1,1), s=4:  k, FE, Bessel-matching')
for k in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]:
    fe = ratios(step(4, k), [k], 2000, modes=[(1, 1)], rich=True)[0]
    bs = bessel_step(4, k, 1, 1)[0] / bessel_step(4, k, 0, 1)[0]
    P('   k=%.1f  %.5f  %.5f' % (k, fe, bs))

# 2b. scan s, k
best = []
ss = np.arange(1, 40.01, 0.5)
ks = np.arange(0.05, 0.9501, 0.01)
G = np.zeros((len(ss), len(ks)))
for i, s in enumerate(ss):
    for j, k in enumerate(ks):
        G[i, j] = miss(ratios(step(s, k), [k], 300))
np.save('/home/agent2/drum/referee/grid_step.npy', G)
order = np.argsort(G.ravel())[:5]
P('ITEM 2b coarse grid (N=300) five best cells: ', [(ss[o // len(ks)], round(ks[o % len(ks)], 2), round(G.ravel()[o], 5)) for o in order])
# local minima of the grid (to see whether there are rival basins)
lm = []
for i in range(len(ss)):
    for j in range(len(ks)):
        nb = G[max(i - 1, 0):i + 2, max(j - 1, 0):j + 2]
        if G[i, j] <= nb.min():
            lm.append((G[i, j], ss[i], ks[j]))
lm.sort()
P('   grid local minima (miss, s, k), best 8:', [(round(a, 4), b, round(c, 2)) for a, b, c in lm[:8]])


def obj(p, N=1500):
    s, k = p
    if not (1 <= s <= 40 and 0.05 <= k <= 0.95):
        return 9.0
    return miss(ratios(step(s, k), [k], N))


res = None
for o in order[:3]:
    x0 = [ss[o // len(ks)], ks[o % len(ks)]]
    rr = minimize(obj, x0, method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-8, maxiter=400))
    if res is None or rr.fun < res.fun:
        res = rr
s, k = res.x
rb = ratios(step(s, k), [k], 3000, rich=True)
P('   best: s=%.4f k=%.5f  largest miss=%.5f (Richardson N=3000/6000: %.5f)' % (s, k, res.fun, miss(rb)))
P('   nine ratios there:', rb)
P('   ratio/target - 1 :', rb / TARGET - 1)
xb = ratios(step(s, k), [k], 3000, modes=EXTRA, rich=True)
P('   (5,1),(3,2),(1,3):', xb, ' /6 - 1:', xb / 6 - 1)
bz = np.array([bessel_step(s, k, m, n)[n - 1] for m, n in MODES + EXTRA])
P('   same by Bessel matching:', bz / bz[0])
P('   (2,1)/(0,2) gap %.4f ; (3,1)/(1,2) gap %.4f' % (rb[2] / rb[3] - 1, rb[4] / rb[5] - 1))
# how sharp: miss along k at best s, and along s at best k
P('   miss vs k at best s:', [(round(kk, 2), round(obj([s, kk], 600), 4)) for kk in np.arange(0.30, 0.501, 0.02)])
P('   miss vs s at best k:', [(ss_, round(obj([ss_, k], 600), 4)) for ss_ in [4, 6, 8, 9, 10, 11, 12, 14, 18, 25, 40]])
P('   best k for fixed s (miss): ', end='')
for s_ in [5, 7, 10, 14, 20, 30, 40]:
    i = int(round((s_ - 1) / 0.5))
    P('s=%g: k=%.2f %.4f; ' % (s_, ks[G[i].argmin()], G[i].min()), end='')
P()
P('   area of grid with miss < 5%%: %d cells of %d; < 4%%: %d' % ((G < 0.05).sum(), G.size, (G < 0.04).sum()))

# 3. graded patch
P('ITEM 3 graded patch 1+(s-1)(1-(r/k)^2): least largest miss over k')
for s in [5, 10, 20, 40, 80, 160, 320, 1280]:
    kk = np.arange(0.05, 0.9501, 0.01)
    v = [miss(ratios(graded(s, q), [q], 600)) for q in kk]
    j = int(np.argmin(v))
    rr = minimize_scalar(lambda q: miss(ratios(graded(s, q), [q], 3000)), bounds=(max(0.05, kk[j] - 0.02), min(0.95, kk[j] + 0.02)), method='bounded', options=dict(xatol=1e-6))
    q = rr.x
    m3 = miss(ratios(graded(s, q), [q], 3000, rich=True))
    added = (s - 1) * q * q / 2  # added mass / pi  (int 2 r (s-1)(1-(r/k)^2) dr = (s-1)k^2/2)
    P('   s=%5g  k=%.4f  miss=%.5f (Richardson %.5f)   added mass/pi=%.3f   [even disc of same radius would need s=%.2f]' % (s, q, rr.fun, m3, added, 1 + added / q / q))
P('   best even disc added mass/pi = (s-1)k^2')
P('time %.1fs' % (time.time() - t0))
