"""The seven-element multiset {0, 3, 9, 12, 32, 36, 97} on Z_105 has 7/32 of its signings bad (the largest share for
seven elements on an odd modulus, by the first and third texts on Conjecture Q).  Its lifts to Z_210 (each element b
or b + 105) and to Z_420: the share of good signings of each; is 1 - 2*(7/32) = 9/16 attained?
Exact integers, all signings with the first sign +."""
import itertools, sys
from fractions import Fraction
import numpy as np
from minshare import red_matrix
base = [0, 3, 9, 12, 32, 36, 97]; m = len(base)
E = np.array([[1] + [1 if (s >> i) & 1 else -1 for i in range(m - 1)] for s in range(2 ** (m - 1))], dtype=np.int64).T
def good_share(R, blocks, xs):
    V = R[:, np.array(xs, dtype=np.int64)] @ E
    bad = np.zeros(V.shape[1], dtype=bool)
    for (start, k, d) in blocks: bad |= ~np.any(V[start:start + k] != 0, axis=0)
    return Fraction(int((~bad).sum()), 2 ** (m - 1))
R, bl = red_matrix(105); print("on Z_105: good share", good_share(R, bl, base), "(bad", 1 - good_share(R, bl, base), ")")
for n, mult in ((210, 2), (420, 4)):
    R, bl = red_matrix(n); best = None; cnt = {}
    for lift in itertools.product(range(mult), repeat=m):
        xs = [b + 105 * t for b, t in zip(base, lift)]
        g = good_share(R, bl, xs); cnt[g] = cnt.get(g, 0) + 1
        if best is None or g < best[0]: best = (g, xs)
    print(f"on Z_{n}: {mult**m} lifts; least good share {best[0]} at {best[1]}; distribution:", sorted(cnt.items()))
