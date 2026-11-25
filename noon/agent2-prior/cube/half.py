"""The cube of density one half, to ten figures: the energy of an attitude n is half the mean of |x.n| over the cube.
The integral over one coordinate is done by hand; the other two by Gauss-Legendre quadrature on a grid split at the kinks' scale.
usage: python -I half.py"""
import numpy as np
from scipy.optimize import minimize
gx, gw = np.polynomial.legendre.leggauss(600); x = gx / 2; w = gw / 2; XX, YY = np.meshgrid(x, x, indexing='ij'); WW = np.outer(w, w)
def E(n):
    a, b, c = np.abs(n) / np.linalg.norm(n); a, b, c = sorted((a, b, c)); u = a * XX + b * YY          # integrate by hand over the coordinate with the largest weight c
    inner = np.where(np.abs(u) >= c / 2, np.abs(u), (u * u + c * c / 4) / c); return 0.5 * float((inner * WW).sum())
for name, n in (("face up", (0, 0, 1)), ("edge up", (0, 1, 1)), ("corner up", (1, 1, 1)), ("(0.975, 1, 1)", (0.975, 1, 1)), ("(0.95, 0.95, 1)", (0.95, 0.95, 1)), ("(0.9, 1, 1)", (0.9, 1, 1)), ("(0.8, 0.9, 1)", (0.8, 0.9, 1))):
    print(f"{name}: {E(np.array(n, float)):.10f}")
print("exact values for comparison: face 1/8 = 0.125; edge sqrt(2)/12 =", 2 ** 0.5 / 12, "; corner 0.40625/(2 sqrt 3) =", 0.40625 / (2 * 3 ** 0.5))
best = None
for s in ((0.9, 0.95), (0.5, 0.8), (0.2, 0.6), (0.99, 0.99), (0.3, 0.3), (0.05, 0.9)):
    r = minimize(lambda v: E(np.array([v[0], v[1], 1.0])), s, method='Nelder-Mead', options=dict(xatol=1e-7, fatol=1e-13)); print(f"   from ({s[0]}, {s[1]}, 1): ends at ({r.x[0]:.5f}, {r.x[1]:.5f}, 1) with {r.fun:.10f}")
