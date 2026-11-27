"""What S0, S1, S2 would say without the hypothesis hd (p does not divide d): small searches.
S0/S1: the example e = (0, 3, 6), all signs +, p = 3, i = 1, d = 3.  S2: every multiset of at most 7 residues modulo 27
with level 1 of 3 live, "d" = 3 and 9 (so the modulus is 3^1 * d = 9, 27)."""
import os
import sys
from itertools import combinations_with_replacement
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import core

e = [0, 3, 6]
allplus = 2 ** 3 - 1
print('e = (0, 3, 6), all +: bad at 9:', bool(core.bad(e, 9)[allplus]), '; level 1 of 3 live:', core.live(e, 3, 1),
      '; bad at 3 (what S1 would claim with d = 3):', bool(core.bad(e, 3)[allplus]))
# class sums modulo 3 with eta of order 3: classes 0, 1, 2 hold 3, 0, 0 elements; eta^0 + eta^3 + eta^6 = 3
T = core.xtab(3)[np.array(e) % 3]
print('   class sums modulo 3 at a root of order 3, as remainders modulo Phi_3: class 0 ->', T.sum(axis=0).tolist(), ', classes 1, 2 -> [0, 0]')
fails = 0; n = 0; worst = None
for m in range(3, 8):
    for e in combinations_with_replacement(range(27), m):
        if not core.live(e, 3, 1):
            continue
        rk = core.rank(e, 3, 1)
        for d in (3, 9):
            cnt = int(core.bad(list(e), 3 * d).sum())
            n += 1
            if cnt * 2 ** (2 * rk) > 2 ** m:
                fails += 1
                worst = worst or (e, d, cnt)
print('S2 with p = 3, i = 1 and d = 3, 9 (hd violated): %d instances, inequality fails in %d %s' % (n, fails, worst or ''))
