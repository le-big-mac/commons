"""The fitted constant again, on a grid of 0.0001 of a block.   Added 26 November 2026, after a reader's check.
usage: python -I twfine.py 100 400 1600 > twfine.out ; python -I twfine.py 6400 >> twfine.out
        (numpy, scipy; tw.py and referee/ref_Kkraw.py beside it; order 6,400 takes about three minutes)
tw.py and tw0.py looked for the best constant c in steps of 0.01, which is too coarse to find the least distance.
For each order: the largest difference D between the exact law and the Tracy-Widom form at the best c, for my
depth K and for the papers' depth (my K at order n + 1, set against the form at n), and the two constants."""
import os, sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'referee'))
import numpy as np
import tw
from ref_Kkraw import K_law

if __name__ == '__main__':
    grid = np.linspace(-9, 6, 6001); cdf = np.array([tw.F(s) for s in grid])
    Fi = lambda s: np.interp(s, grid, cdf, left=0.0, right=1.0)
    a = (1 - 1 / math.sqrt(2)) / 2; b = 2 ** (-11 / 6)
    def best(surv, n, lo, hi):
        ks = np.arange(len(surv)); out = (9.0, 0.0)
        for c in np.arange(lo, hi + 1e-9, 0.001):
            d = float(np.abs(surv - Fi((a * n - ks + c) / (b * n ** (1 / 3)))).max())
            if d < out[0]: out = (d, float(c))
        for c in np.arange(out[1] - 0.002, out[1] + 0.002 + 1e-9, 0.0001):      # then in steps of 0.0001 round the best
            d = float(np.abs(surv - Fi((a * n - ks + c) / (b * n ** (1 / 3)))).max())
            if d < out[0]: out = (d, float(c))
        return out
    for n in [int(x) for x in sys.argv[1:]]:
        d1, c1 = best(K_law(n)['surv'], n, -0.1, 0.2); d2, c2 = best(K_law(n + 1)['surv'], n, 0.0, 0.4)
        print(f"n = {n:5d}: my depth, D = {d1:.6f} at c = {c1:+.4f}; the papers' depth, D = {d2:.6f} at c = {c2:+.4f}; difference of the two constants {c2 - c1:.4f}"
              f"; 0.1464 + (0.497/3) n^(-2/3) = {a + 0.497 / 3 * n ** (-2 / 3):.4f}", flush=True)
