"""The Tracy-Widom comparison again, with no fitted constant, and for the frozen region as the papers define it.
usage: python -I tw0.py > tw0.out      (numpy, scipy; tw.py and referee/ref_Kkraw.py beside it)   Added 26 November 2026.
tw.py reported the largest difference D between the exact law of K and the Tracy-Widom form at the best shift.
A reader pointed out that the page's sentence gave that D as if no shift had been fitted, and that my K (a block
holding exactly one dimer counts as frozen) is the papers' north polar region one order earlier: the polar region's
depth at order n has the law of my K at order n + 1."""
import os, sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'referee'))
import numpy as np
import tw
from ref_Kkraw import K_law

if __name__ == '__main__':
    grid = np.linspace(-9, 6, 3001); cdf = np.array([tw.F(s) for s in grid])
    Fi = lambda s: np.interp(s, grid, cdf, left=0.0, right=1.0)
    a = (1 - 1 / math.sqrt(2)) / 2; b = 2 ** (-11 / 6)
    def D(surv, n, shift):
        ks = np.arange(len(surv)); return float(np.abs(surv - Fi((a * n - ks + shift) / (b * n ** (1 / 3)))).max())
    def best(surv, n):
        return min((D(surv, n, s), float(s)) for s in np.arange(-1, 1.0001, 0.01))
    print("order n | my K: D with no shift; D at the best shift | the polar region (my K at order n + 1, set against the form at n): D with no shift; D at the best shift")
    for n in (100, 400, 1600, 6400):
        k1 = K_law(n)['surv']; k2 = K_law(n + 1)['surv']
        b1 = best(k1, n); b2 = best(k2, n)
        print(f"{n:6d} | {D(k1, n, 0.0):.5f}; {b1[0]:.5f} at {b1[1]:+.2f} | {D(k2, n, 0.0):.5f}; {b2[0]:.5f} at {b2[1]:+.2f}")
