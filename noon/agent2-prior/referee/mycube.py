"""Referee's own floating-cube energy, by a different route from cube/half.py and cube/cube.py.
S = a X + b Y + c Z with X, Y, Z uniform on [-1/2, 1/2] (n = (a,b,c) unit, 'up').  S has a closed-form spline law:
  CDF(t) = (1/abc) sum_eps prod(eps) (t + eps.n/2)_+^3 / 6
  M(t)   = E[S; S<t] = t CDF(t) - (1/abc) sum_eps prod(eps) (t + eps.n/2)_+^4 / 24
The cube of density rho floats with the lowest fraction rho submerged: CDF(t) = rho.  Energy per unit volume and g:
  E(n, rho) = rho_body * (z_G - z_B) * 1 = rho * (0 - M(t)/rho) = -M(t).
usage: python -I mycube.py"""
import itertools, numpy as np
from scipy.optimize import brentq, minimize
EPS = np.array(list(itertools.product((-1, 1), repeat=3)), float); SG = EPS.prod(1)
def parts(n):
    n = np.abs(np.asarray(n, float)); n = n / np.linalg.norm(n); n = np.maximum(n, 2e-4); n = n / np.linalg.norm(n); return n, EPS @ n / 2
def cdf(t, n, h): return float((SG * np.clip(t + h, 0, None) ** 3).sum() / 6 / n.prod())
def E(n, rho):
    n, h = parts(n); T = np.abs(n).sum() / 2
    t = brentq(lambda t: cdf(t, n, h) - rho, -T, T, xtol=1e-15)
    return -(t * cdf(t, n, h) - float((SG * np.clip(t + h, 0, None) ** 4).sum() / 24 / n.prod()))
print("density 1/2, closed form: face %.10f edge %.10f corner %.10f" % (E((0, 0, 1), .5), E((0, 1, 1), .5), E((1, 1, 1), .5)))
print("   exact: 1/8 = 0.125, sqrt(2)/12 = %.10f, 13/(64 sqrt 3) = %.10f" % (2 ** .5 / 12, 13 / 64 / 3 ** .5))
rng = np.random.default_rng(7); P = rng.random((4_000_000, 3)) - .5
for nm, n in (("face", (0, 0, 1)), ("edge", (0, 1, 1)), ("corner", (1, 1, 1)), ("(0.8,0.9,1)", (.8, .9, 1))):
    v = np.array(n, float); v /= np.linalg.norm(v); print("   Monte Carlo 4e6, %s: %.5f  (closed form %.5f)" % (nm, .5 * np.abs(P @ v).mean(), E(n, .5)))
M = 80
for rho in (0.15, 0.2, 0.21, 0.22, 0.225, 0.23, 0.25, 0.3, 0.4, 0.5):
    g = sorted((E((i / M, j / M, 1), rho), i / M, j / M) for i in range(M + 1) for j in range(i, M + 1))
    f, e, c = E((0, 0, 1), rho), E((0, 1, 1), rho), E((1, 1, 1), rho)
    r = minimize(lambda v: E((v[0], v[1], 1), rho), (g[0][1], g[0][2]), method='Nelder-Mead', options=dict(xatol=1e-8, fatol=1e-14))
    print("rho %.3f: face %.8f edge %.8f corner %.8f | grid min %.8f at (%.4f, %.4f, 1) | polished %.8f at (%.4f, %.4f, 1)" % (rho, f, e, c, g[0][0], g[0][1], g[0][2], r.fun, abs(r.x[0]), abs(r.x[1])), flush=True)
# is corner up a strict local minimum at rho = 1/2?  second differences around (1,1,1) in two directions
for d in ((1, 0), (0, 1), (1, 1), (1, -1)):
    hstep = 1e-3; e0 = E((1, 1, 1), .5); ep = E((1 + hstep * d[0], 1 + hstep * d[1], 1), .5); em = E((1 - hstep * d[0], 1 - hstep * d[1], 1), .5)
    print("   rho 0.5, second difference at corner along %s: %.3e (positive = minimum)" % (d, (ep + em - 2 * e0) / hstep ** 2))
# random starts at rho = 1/2 over the whole fundamental region, 40 of them
ends = set()
for s in rng.random((40, 2)):
    r = minimize(lambda v: E((v[0], v[1], 1), .5), s, method='Nelder-Mead', options=dict(xatol=1e-7, fatol=1e-13)); ends.add((round(abs(r.x[0]), 3), round(abs(r.x[1]), 3), round(r.fun, 9)))
print("   rho 0.5, 40 random starts end at:", sorted(ends))
