# Small facts used in result.md, all signings, exact:
#  (1) Remark 3.2: for 3 or 5 elements on Z_27 (all multisets containing 0), every signing that is bad at 3, 9 or 27
#      has signs adding up to +3 or -3;
#  (2) three elements on an odd modulus: every bad signing has all signs equal; four elements: every bad signing has
#      signs adding up to 0  (all multisets containing 0 on Z_15, Z_21, Z_35, Z_45, Z_63, Z_75, Z_105);
#  (3) "the root of the shapes": for three elements, bad at d (signs equal) happens only for 3 | d.
from itertools import combinations_with_replacement, product
import numpy as np
from badlib import divisors, mat_d

def bad_signings(n, B):
    """list of (eps, set of d at which eps is bad)"""
    m = len(B)
    E = np.array(list(product((1, -1), repeat=m)), dtype=np.int64)
    out = {}
    for d in divisors(n):
        M = mat_d(d, [b % n for b in B])
        z = ~((E @ M).any(axis=1))
        for idx in np.nonzero(z)[0]:
            out.setdefault(idx, set()).add(d)
    return [(E[i], ds) for i, ds in out.items()]

n1 = 0
for m in (3, 5):
    for rest in combinations_with_replacement(range(27), m - 1):
        B = (0,) + rest
        for eps, ds in bad_signings(27, B):
            assert abs(int(eps.sum())) == 3, (B, eps, ds)
        n1 += 1
print('(1) Remark 3.2 on Z_27: %d multisets of 3 or 5 elements, every bad signing has sum +3 or -3' % n1)

n2 = 0; n3 = 0
for n in (15, 21, 35, 45, 63, 75, 105):
    for m in (3, 4):
        for rest in combinations_with_replacement(range(n), m - 1):
            B = (0,) + rest
            for eps, ds in bad_signings(n, B):
                if m == 3:
                    assert abs(int(eps.sum())) == 3, (n, B, eps, ds)
                    assert all(d % 3 == 0 for d in ds), (n, B, eps, ds)
                    n3 += 1
                else:
                    assert int(eps.sum()) == 0 and 1 in ds, (n, B, eps, ds)
            n2 += 1
print('(2) %d multisets of 3 or 4 elements on Z_15, 21, 35, 45, 63, 75, 105: three elements bad => all signs equal; '
      'four elements bad => signs add up to 0' % n2)
print('(3) %d bad signings of three elements met, each bad only at multiples of 3' % n3)
