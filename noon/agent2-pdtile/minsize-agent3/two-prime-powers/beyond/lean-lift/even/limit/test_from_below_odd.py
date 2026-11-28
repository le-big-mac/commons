"""The display of limits.md, "from below", for an odd number of elements: h odd copies of 0 beside a decoration with an
even number of elements; share of bad signings against c_h * K_other(D).  Exact."""
import sys, math
from fractions import Fraction
sys.path.insert(0, '/home/agent3/lean/lift-check/even/shares'); sys.path.insert(0, '/home/agent3/lean/lift-check/even/asym')
from minshare import red_matrix
from kdec import K
from heavy import share
def c(r): return Fraction(math.comb(r, r // 2), 2 ** r)
for (L, D, name) in ((3, [1, 2], "one element in each nonzero class modulo 3, on Z_3"), (15, [10, 5, 3, 6, 9, 12], "one element in each nonzero class modulo 3 and 5, on Z_15"), (3, [1, 1, 2, 2], "pairs at 1 and 2 on Z_3")):
    R, blocks = red_matrix(L); r = len(D); ks, ko = K(R, blocks, D)
    mult = [(b, D.count(b)) for b in sorted(set(D))]
    for h in (1, 21, 201, 2001):
        s, m = share(R, blocks, [(0, h)] + mult)
        print(f"from below, odd: {name}: h = {h:5d} (m = {m}, {'even' if m % 2 == 0 else 'odd'}): share / c_h = {float(s / c(h)):.5f}; K_other = {ko} = {float(ko):.5f}; share <= c_h K: {s <= c(h) * ko}", flush=True)
