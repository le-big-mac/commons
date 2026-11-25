"""The graded patch beyond the sealed range, and at fixed peak loads.   usage: python after2.py"""
import numpy as np
from scipy.optimize import minimize_scalar
from helpers import fd_modes, graded, tied, NINE, NEXT
print("The graded patch at fixed peak loads: the best radius k and the largest miss there (finite differences, 2,000 cells)")
for s in (5, 10, 15, 20, 30, 40, 60, 80, 120, 160, 240, 320, 640):
    best = min((tied(fd_modes(graded(float(s), float(k)), N=800)), float(k)) for k in np.arange(0.30, 0.901, 0.02))
    r = minimize_scalar(lambda k: tied(fd_modes(graded(float(s), float(k)))), bounds=(max(0.3, best[1] - 0.03), min(0.9, best[1] + 0.03)), method="bounded", options=dict(xatol=1e-4))
    w = fd_modes(graded(float(s), float(r.x)), NINE + NEXT); print(f"   s = {s:4d}: k = {r.x:.3f}; largest miss {100 * r.fun:.2f}%; added mass {(s - 1) * r.x ** 2 / 2:6.2f} times the bare skin; (2,1) and (0,2) differ by {100 * abs(w[2] / w[3] - 1):.2f}%, (3,1) and (1,2) by {100 * abs(w[4] / w[5] - 1):.2f}%")
