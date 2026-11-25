"""A smooth load from the literature (Sathej and Adhikari, arXiv:0809.1320, eq. 1 with no eccentricity), put through this study's solver:
mass per area 1 + (sigma^2 - 1)/2 * (1 - tanh((r - k)/xi)).   usage: python -u smooth.py smooth.json"""
import sys, json, math
import numpy as np
from scipy.optimize import minimize
import lib12 as L
N = 2000; sk = {name: L.Skin(N, modes, per=1) for name, modes in L.SETS.items()}; r = sk['nine'].r
def load(sigma, k, xi): return (sigma ** 2 - 1) / 2 * (1 - np.tanh((r - k) / xi))
def report(label, sigma, k, xi):
    a = load(sigma, k, xi); c = sk['sixteen'].solve(a, grad=False); ratios = np.concatenate([[1.0], (c + 1) * sk['sixteen'].T[1:]]); out = dict(label=label, sigma=sigma, k=k, xi=xi, mass=sk['nine'].mass(a), ratios=ratios.tolist(), miss={name: s.miss(a) for name, s in sk.items()}, D=L.D(a, per=1))
    print(f"{label}: sigma = {sigma}, k = {k}, xi = {xi} (centre {1 + a[0]:.2f} times the skin; added mass {out['mass']:.2f} skins): largest miss over nine modes {100 * out['miss']['nine']:.2f}%, twelve {100 * out['miss']['twelve']:.2f}%, sixteen {100 * out['miss']['sixteen']:.2f}%; D = {out['D']:.1f} cents", flush=True)
    print("   ratios to the lowest: " + ", ".join(f"{x:.3f}" for x in ratios) + "; to half the second mode, as the paper normalises: " + ", ".join(f"{2 * x / ratios[1]:.4f}" for x in ratios[:9]), flush=True); return out
A = dict(cases=[report("the paper's like-for-like case (its Table I, 'Smooth' column)", 3.125, 0.4, 0.091), report("the paper's most harmonic case (its Fig. 6)", 2.57, 0.492, 0.091), report("the step, for comparison (xi nearly 0: the composite membrane of 1954)", 3.125, 0.4, 0.0005)])
print("the paper's Table I, 'Smooth' column, normalised by the first overtone: 1.0345, 2.0000, 3.0393, 3.0534, 4.0086, 4.1463, 4.7784, 5.0023, 5.2491 in the order (0,1), (1,1), (2,1), (0,2), (3,1), (1,2), (0,3), (4,1), (2,2); 'Composite': 1.0309, 2.0000, 3.0412, 3.1546, 4.0928, 4.2268, 4.9794, 5.1134, 5.3093")
# the best of this three-parameter family by this study's measure, for nine, twelve and sixteen modes
A['best'] = {}
for name in ("nine", "twelve", "sixteen"):
    f = lambda x: sk[name].miss(load(max(1.01, x[0]), min(0.95, max(0.05, x[1])), max(0.003, x[2]))); best = None
    for x0 in ((2.57, 0.492, 0.091), (3.125, 0.4, 0.091), (3.0, 0.45, 0.2), (4.0, 0.5, 0.15), (2.5, 0.6, 0.3), (5.0, 0.45, 0.05)):
        res = minimize(f, x0, method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-9, maxiter=1500))
        if best is None or res.fun < best.fun: best = res
    s, k, xi = max(1.01, best.x[0]), min(0.95, max(0.05, best.x[1])), max(0.003, best.x[2]); a = load(s, k, xi); A['best'][name] = dict(sigma=float(s), k=float(k), xi=float(xi), miss=float(best.fun), mass=sk['nine'].mass(a), D=L.D(a, per=1), all={n: sk[n].miss(a) for n in sk})
    print(f"the best smooth step for {name} modes (six starts, Nelder-Mead): sigma = {s:.3f} (centre {s * s:.2f} times the skin), k = {k:.3f}, xi = {xi:.3f}, added mass {A['best'][name]['mass']:.2f} skins: largest miss {100 * best.fun:.2f}% (nine {100 * A['best'][name]['all']['nine']:.2f}%, twelve {100 * A['best'][name]['all']['twelve']:.2f}%, sixteen {100 * A['best'][name]['all']['sixteen']:.2f}%); D = {A['best'][name]['D']:.1f}", flush=True)
json.dump(A, open(sys.argv[1], "w"))
