# Controls on the layered and graded patches.  Run: python -I -B ctl.py
import sys, time, json
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent2/drum/referee')
import numpy as np
from scipy.optimize import minimize
from mem import *

t0 = time.time()
P = print
np.set_printoptions(precision=4, suppress=True, linewidth=200)


def lay(p, N=600, top=40.0):
    p = np.asarray(p, float)
    L = len(p) // 2
    a, k = p[:L], p[L:]
    if np.any(a < 0) or np.any(a > top) or np.any(k < 0.05) or np.any(k > 0.95):
        return 9.0
    return miss(ratios(layers(a, k), list(k), N))


# (i) my two-layer answer, and the author's answers, by the AUTHOR's finite differences (helpers.fd_modes, N=3000) and by mine
sys.path.insert(1, '/home/agent2/drum')
import helpers
mine = [39.996, 20.965, 0.4558, 0.2489]
best2 = minimize(lambda p: lay(p, 2000), mine, method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-10, maxiter=400,
                 initial_simplex=np.array(mine) + np.vstack([np.zeros(4), np.diag([-0.3, 0.3, 0.003, 0.003])]))).x
rho = lambda r: 1.0 + sum(a * (r < k) for a, k in zip(best2[:2], best2[2:]))
w = helpers.fd_modes(rho, N=3000)
P('(i) two layers, referee optimum %s : author code (fd_modes N=3000) miss %.5f ; referee code (Richardson) %.5f'
  % (np.round(best2, 4), helpers.tied(w), miss(ratios(layers(best2[:2], best2[2:]), list(best2[2:]), 3000, rich=True))))
P('    cents from harmonic (author code):', np.round(1200 * np.log2(w[1:] / w[0] / TARGET[1:]), 1), ' added mass %.2f skins' % (best2[0] * best2[2] ** 2 + best2[1] * best2[3] ** 2))
for f in ['layers-2.json', 'layers-2-s201.json', 'layers-3.json', 'layers-3-s301.json', 'layers-4-s401.json']:
    J = json.load(open('/home/agent2/drum/' + f))
    P('    %-20s author miss %.5f ; referee code at the same loads %.5f' % (f, J['miss'], miss(ratios(layers(J['a'], J['k']), list(J['k']), 3000, rich=True))))

# (ii) is the two-layer miss still falling beyond the sealed load range of 40?  fix the outer load at A, optimise the rest
P('(ii) two layers with the outer load fixed at A (inner load, radii free, no upper bound on the inner load):')
x = np.array([20.0, 0.4558, 0.2489])
for A in [10, 15, 20, 30, 40, 80, 160, 640]:
    x = np.array([A * 0.52, 0.455, 0.249])
    for N in (600, 2000):
        r = minimize(lambda q: lay([A, q[0], q[1], q[2]], N, top=1e9), x, method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-10, maxiter=500,
                     initial_simplex=x + np.vstack([np.zeros(3), np.diag([0.05 * A, 0.004, 0.004])])))
        x = r.x
    P('    A=%4g: inner load %.2f, radii %.4f %.4f, miss %.5f, added mass %.2f skins' % (A, x[0], x[1], x[2], r.fun, A * x[1] ** 2 + x[0] * x[2] ** 2))

# (iii) graded patch at the even disc's own added mass (s-1)k^2/2 = (9.938-1)*0.4004^2
M0 = (9.938 - 1) * 0.4004 ** 2
ss = np.exp(np.linspace(np.log(4.3), np.log(2000), 90))
v = [miss(ratios(graded(s, np.sqrt(2 * M0 / (s - 1))), [np.sqrt(2 * M0 / (s - 1))], 800)) for s in ss]
j = int(np.argmin(v))
P('(iii) graded patch held at the disc\'s added mass %.3f skins: least miss over the peak load = %.4f at s=%.1f, k=%.3f ; (at s=10: %.4f)'
  % (M0, v[j], ss[j], np.sqrt(2 * M0 / (ss[j] - 1)), miss(ratios(graded(10, np.sqrt(2 * M0 / 9)), [np.sqrt(2 * M0 / 9)], 800))))
# where does the graded patch (best k) first beat the disc's 3.157%?
for s in [20, 21, 22, 23, 24]:
    kk = np.arange(0.50, 0.60, 0.002)
    vv = [miss(ratios(graded(s, q), [q], 800)) for q in kk]
    q = kk[int(np.argmin(vv))]
    P('    graded s=%d best k=%.3f miss %.4f added mass %.2f' % (s, q, min(vv), (s - 1) * q * q / 2))

# (iv) another shape that thins towards its edge: flat at s inside k1, falling in a straight line to the bare skin at k2
def trap(s, k1, k2):
    return lambda x: np.where(x < k1, s, np.where(x < k2, s + (1 - s) * (x - k1) / (k2 - k1), 1.0))
def tobj(p, N=600):
    s, k1, k2 = p
    if not (1 <= s <= 40 and 0.05 <= k1 < k2 - 1e-3 and k2 <= 0.95):
        return 9.0
    return miss(ratios(trap(s, k1, k2), [k1, k2], N))
bt = None
for x0 in [(10, 0.35, 0.45), (12, 0.3, 0.5), (15, 0.25, 0.55), (20, 0.2, 0.6), (30, 0.2, 0.55), (10, 0.39, 0.41), (25, 0.3, 0.5), (38, 0.25, 0.5)]:
    r = minimize(tobj, x0, method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-9, maxiter=500))
    if bt is None or r.fun < bt.fun:
        bt = r
s, k1, k2 = bt.x
am = (s - 1) * (k1 * k1 + k1 * k2 + k2 * k2) / 3
P('(iv) flat-topped patch with a straight taper (s inside k1, down to 1 at k2), s<=40, 8 starts: least miss %.4f at s=%.2f k1=%.3f k2=%.3f, added mass %.2f skins (Richardson %.4f)'
  % (bt.fun, s, k1, k2, am, miss(ratios(trap(s, k1, k2), [k1, k2], 3000, rich=True))))
# the same taper held to modest weight: s <= 12
bt = None
for x0 in [(10, 0.35, 0.45), (11, 0.3, 0.5), (9, 0.25, 0.55), (8, 0.3, 0.6), (11.5, 0.2, 0.55)]:
    r = minimize(lambda p: 9.0 if p[0] > 12 else tobj(p), x0, method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-9, maxiter=500))
    if bt is None or r.fun < bt.fun:
        bt = r
s, k1, k2 = bt.x
P('     the same with s <= 12: least miss %.4f at s=%.2f k1=%.3f k2=%.3f, added mass %.2f skins' % (bt.fun, s, k1, k2, (s - 1) * (k1 * k1 + k1 * k2 + k2 * k2) / 3))
P('time %.0fs' % (time.time() - t0))
