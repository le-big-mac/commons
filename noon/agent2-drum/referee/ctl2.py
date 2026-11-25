# Last controls: comparisons at the even disc's own added mass; the staircase in the author's search objective.  Run: python -I -B ctl2.py
import sys, time, json
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent2/drum/referee'); sys.path.insert(1, '/home/agent2/drum')
import numpy as np
from scipy.optimize import minimize
from mem import *
import helpers
t0 = time.time(); P = print
M0 = (9.938 - 1) * 0.4004 ** 2
# (a) two layers with total added mass M0
def two(p, N=800):
    a1, k1, k2 = p
    if not (0.05 <= k2 < k1 <= 0.95 and a1 >= 0): return 9.0
    a2 = (M0 - a1 * k1 * k1) / (k2 * k2)
    if a2 < 0: return 9.0
    return miss(ratios(layers([a1, a2], [k1, k2]), [k1, k2], N))
b = None
for x0 in [(6, 0.42, 0.23), (5, 0.45, 0.25), (7, 0.40, 0.2), (4, 0.5, 0.3), (8, 0.38, 0.15), (3, 0.55, 0.35), (6.5, 0.43, 0.24)]:
    r = minimize(two, x0, method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-9, maxiter=600))
    r = minimize(two, r.x, method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-9, maxiter=600))
    if b is None or r.fun < b.fun: b = r
a1, k1, k2 = b.x
P('(a) two layers held at the disc\'s added mass %.3f: least miss found %.4f (N=3000: %.4f) : +%.2f inside %.3f and +%.2f inside %.3f'
  % (M0, b.fun, two(b.x, 3000), a1, k1, (M0 - a1 * k1 * k1) / k2 / k2, k2))
# (b) flat top with straight taper at added mass M0
def trap(s, k1, k2):
    return lambda x: np.where(x < k1, s, np.where(x < k2, s + (1 - s) * (x - k1) / (k2 - k1), 1.0))
def tr(p, N=800):
    k1, k2 = p
    if not (0.05 <= k1 < k2 - 1e-3 and k2 <= 0.95): return 9.0
    s = 1 + 3 * M0 / (k1 * k1 + k1 * k2 + k2 * k2)
    return miss(ratios(trap(s, k1, k2), [k1, k2], N))
b = None
for x0 in [(0.3, 0.48), (0.35, 0.45), (0.25, 0.55), (0.2, 0.6), (0.38, 0.42), (0.3, 0.5)]:
    r = minimize(tr, x0, method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-9, maxiter=400))
    if b is None or r.fun < b.fun: b = r
k1, k2 = b.x
P('(b) flat top with a straight taper, held at the same added mass: least miss %.4f (N=3000: %.4f) at s=%.2f, flat to %.3f, tapering to %.3f' % (b.fun, tr(b.x, 3000), 1 + 3 * M0 / (k1 * k1 + k1 * k2 + k2 * k2), k1, k2))
# (c) parabola at the same added mass, refined
g = lambda s, N=2000: miss(ratios(graded(s, np.sqrt(2 * M0 / (s - 1))), [np.sqrt(2 * M0 / (s - 1))], N))
ss = np.arange(10.0, 15.01, 0.1); v = [g(s) for s in ss]; j = int(np.argmin(v))
P('(c) parabola at the same added mass: least miss %.4f at peak %.1f over %.3f ; author code there: %.4f' % (v[j], ss[j], np.sqrt(2 * M0 / (ss[j] - 1)),
  helpers.tied(helpers.fd_modes(helpers.graded(ss[j], np.sqrt(2 * M0 / (ss[j] - 1))), N=2000))))
# (d) the author's search objective (600 cells, density sampled at cell centres) as the outer radius moves in steps of 0.0003
J = json.load(open('/home/agent2/drum/layers-2.json')); a = J['a']; k = J['k']
P('(d) layers-2 answer, outer radius moved; author objective at 600 cells | at 3000 cells | referee (mesh node on the edge)')
for d in np.arange(0, 0.00361, 0.0004):
    rho = lambda r: 1.0 + a[0] * (r < k[0] + d) + a[1] * (r < k[1])
    P('    k1=%.4f  %.5f | %.5f | %.5f' % (k[0] + d, helpers.tied(helpers.fd_modes(rho, N=600)), helpers.tied(helpers.fd_modes(rho, N=3000)), miss(ratios(layers(a, [k[0] + d, k[1]]), [k[0] + d, k[1]], 3000))))
P('(e) best even disc: (2,2) over (0,3) = %.1f cents; (2,1)/(0,2) %.1f; (3,1)/(1,2) %.1f' % (1200 * np.log2(5.1579 / 4.8421), 1200 * np.log2(3.0541 / 2.9467), 1200 * np.log2(4.1029 / 3.9653)))
P('time %.0fs' % (time.time() - t0))
