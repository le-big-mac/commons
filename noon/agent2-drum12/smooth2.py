"""The best smooth step (the tanh form of arXiv:0809.1320) at a given added mass, by this study's measure, for nine, twelve and sixteen modes.
usage: python -u smooth2.py smooth2.json     (Nelder-Mead from five starts each, 1,000 cells)"""
import sys, json, math
import numpy as np
from scipy.optimize import minimize
import lib12 as L
N = 1000; sk = {name: L.Skin(N, modes, per=1) for name, modes in L.SETS.items()}; r = sk['nine'].r; A = sk['nine'].A; out = []
def load(k, xi, mass):
    shape = 0.5 * (1 - np.tanh((r - k) / xi)); return shape * mass / float(shape @ A)
for M in (1.43, 4.0, 12.0):
    for name in ("nine", "twelve", "sixteen"):
        def f(x):
            k, xi, frac = min(0.95, max(0.05, x[0])), min(1.0, max(0.003, x[1])), min(1.0, max(0.05, x[2])); return sk[name].miss(load(k, xi, frac * M))
        best = None
        for x0 in ((0.4, 0.09, 1.0), (0.49, 0.09, 1.0), (0.45, 0.2, 0.9), (0.5, 0.05, 1.0), (0.42, 0.01, 1.0)):
            res = minimize(f, x0, method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-9, maxiter=500))
            if best is None or res.fun < best.fun: best = res
        k, xi, frac = min(0.95, max(0.05, best.x[0])), min(1.0, max(0.003, best.x[1])), min(1.0, max(0.05, best.x[2])); a = load(k, xi, frac * M)
        out.append(dict(weight=M, set=name, miss=float(best.fun), k=float(k), xi=float(xi), used=float(frac * M), centre=float(1 + a[0]), D=L.D(a, per=1)))
        print(f"{M:g} skins allowed, {name} modes: the best smooth step misses by {100 * best.fun:.2f}% (centre {1 + a[0]:.1f} times the skin, half-way radius {k:.3f}, width {xi:.3f}, {frac * M:.2f} skins used); D = {out[-1]['D']:.1f} cents", flush=True)
json.dump(out, open(sys.argv[1], "w"))
