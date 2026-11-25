"""The ruler, before the search: does this code give the nine-mode numbers of ../drum, and do the two solvers agree for the higher modes?
usage: python -u ruler.py > ruler.out"""
import json, sys, time
import numpy as np
import lib12 as L
a143 = np.array(json.load(open("../drum/rings2-free-1.43.json"))['rings']['40']['a']); a12 = np.array(json.load(open("../drum/rings2-free-12.json"))['rings']['40']['a'])
s9 = L.Skin(40, L.NINE); print(f"nine modes, the published 40-ring loads: {100 * s9.miss(a143):.4f}% and {100 * s9.miss(a12):.4f}% by finite differences (published 0.7657% and 0.5288%); {100 * L.exact_miss(a143, L.NINE):.4f}% and {100 * L.exact_miss(a12, L.NINE):.4f}% by exact matching (published 0.7668% and 0.5297%)")
t = time.time(); a, f = L.slp(s9, L.disc(s9, 1.43 / 0.16, 0.4), 1.43); print(f"nine modes, a search from one disc at 1.43 skins: {100 * f:.4f}% in {time.time() - t:.0f} s (published 0.7657%)")
s16 = L.Skin(40, L.SIXTEEN)
for name, load in (("plain", np.zeros(40)), ("ringed, 1.43 skins", a143), ("ringed, 12 skins", a12)):
    fd = np.concatenate([[1.0], (s16.solve(load, grad=False) + 1) * s16.T[1:]]); ex = L.exact_ratios(load, L.SIXTEEN) if name != "plain" else None
    print(f"{name}: the sixteen ratios by finite differences: " + ", ".join(f"{x:.4f}" for x in fd) + ("" if ex is None else f"; largest difference from exact matching {np.abs(fd - ex).max():.1e}"))
print("plain skin, exact (zeros of Bessel functions over 2.404826): (5,1) 3.6475, (3,2) 4.0589, (1,3) 4.2304, (6,1) 4.1317, (4,2) 4.6010, (2,3) 4.8319, (0,4) 4.9033 are what I remember; the line above is the test")
# gradient against differences, for the sixteen-mode misses
c, J = s16.solve(a143); e = np.zeros(40); e[7] = 1e-4; c2 = s16.solve(a143 + e, grad=False); print(f"derivative of the fifteen misses with respect to ring 8's load: largest difference from a finite difference {np.abs((c2 - c) / 1e-4 - J[:, 7]).max():.1e}")
