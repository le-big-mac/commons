"""The yardstick of Sathej and Adhikari (arXiv:0809.1320, eq. 11): Q = the sum, over the first 15 eigenvalues in rising order, of the
squared distance from the nearest whole number. The paper does not say in the text how the eigenvalues are scaled or whether a mode with
nodal diameters counts once or twice (its solver is two-dimensional and finds each such mode twice), so both are tried against its two
published values: Q = 0.027 for its smooth load (sigma 2.57, k 0.492, xi 0.091) and 0.074 for the composite membrane (sigma 3.125, k 0.4).
usage: python -u quality.py quality.json"""
import sys, json, math
import numpy as np
from scipy.linalg import eigh_tridiagonal
def spectrum(rho_cells):
    N = len(rho_cells); h = 1.0 / N; r = (np.arange(N) + 0.5) * h; re = np.arange(N + 1) * h; sc = np.sqrt(r * rho_cells); out = []
    for m in range(12):
        d = (re[:-1] + re[1:]) / (h * h) + m * m / r; d[-1] += re[-1] / (h * h); w = np.sqrt(eigh_tridiagonal(d / sc ** 2, -re[1:-1] / (h * h) / (sc[:-1] * sc[1:]), select='i', select_range=(0, 5))[0]); out += [(w[j], m, j + 1) for j in range(6)]
    return sorted(out)
def Q(rho_cells, twice, scale, nmax=15):
    sp = spectrum(rho_cells); w = {(m, n): x for x, m, n in sp}; unit = w[(0, 1)] if scale == "the lowest mode" else w[(1, 1)] / 2; vals = []
    for x, m, n in sp: vals += [x / unit] * (2 if (twice and m > 0) else 1)
    vals = vals[:nmax]; return float(sum((v - round(v)) ** 2 for v in vals))
N = 4000; r = (np.arange(N) + 0.5) / N; smooth = lambda s, k, xi: 1 + (s * s - 1) / 2 * (1 - np.tanh((r - k) / xi)); step = lambda s, k: np.where(r < k, s * s, 1.0); rings = lambda a: 1 + np.repeat(np.array(a), N // len(a))
B = json.load(open("best.json")); nine143 = json.load(open("../drum/rings2-free-1.43.json"))['rings']['40']['a']
cases = [("the paper's smooth load (published Q = 0.027)", smooth(2.57, 0.492, 0.091)), ("the composite membrane, sigma 3.125, k 0.4 (published Q = 0.074)", step(3.125, 0.4)), ("a plain skin", np.ones(N)),
         ("rings tuned for nine modes, 1.43 skins", rings(nine143)), ("rings tuned for twelve modes, 2.79 skins", rings(B["twelve|2.79|40"]['a'])), ("rings tuned for sixteen modes, 4 skins", rings(B["sixteen|4|40"]['a'])), ("rings tuned for sixteen modes, 12 skins", rings(B["sixteen|12|40"]['a']))]
A = {}
for name, rho in cases:
    row = {f"{'twice' if t else 'once'}, scaled by {s}": Q(rho, t, s) for t in (False, True) for s in ("the lowest mode", "half the second mode")}; A[name] = row
    print(f"{name}: " + "; ".join(f"{k}: {v:.3f}" for k, v in row.items()), flush=True)
json.dump(A, open(sys.argv[1], "w"))
