"""Is `hd : not 2 | d` needed for the TRUTH of L?  The inequality of L for even d (prime to 3), all signings:
#{signings 3-bad at 2^j d for some j <= K} <= 2 #{signings 3-bad at d}.   (Not a statement of the skeleton.)"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import random
import numpy as np
from ecore import bad3

random.seed(8)
inst = viol = eq = zpos = 0
ex = None
for d in [2, 4, 8, 10, 14, 20, 28, 40]:
    for trial in range(1500):
        m = random.randint(0, 9)
        top = 8 * d
        kind = trial % 3
        if kind == 0:
            e = [random.randrange(0, top) for _ in range(m)]
        elif kind == 1:
            base = [random.randrange(0, top) for _ in range(2)]
            e = [random.choice(base) + random.choice([0, d // 2, d, 2 * d]) for _ in range(m)]
        else:
            r = random.randrange(0, d)
            e = [r + (d // 2) * random.randrange(0, 16) for _ in range(m)]
        z = int(bad3(e, d).sum())
        acc = np.zeros(1 << m, dtype=bool)
        inst += 1
        zpos += z > 0
        for j in range(0, 4):
            if 2 ** j * d > 330:
                break
            acc |= bad3(e, 2 ** j * d)
            q = int(acc.sum())
            if q > 2 * z:
                viol += 1
                ex = ex or (d, j, e, q, z)
            eq += (z > 0 and q == 2 * z)
print(f"L for even d in [2, 4, 8, 10, 14, 20, 28, 40]: instances {inst} ({zpos} with a signing 3-bad at d), violations "
      f"{viol}, equalities {eq}; first violation: {ex}")

# `hd : not p | d` is needed in S0' and S1': p = 2, i = 1, d = 2, the family (0, 2), all signs +
from ecore import class_sums3
e = [0, 2]
s = 3                                   # signing number 3: both signs +
b4 = bool(bad3(e, 4)[s])
cs = class_sums3(e, 2, 2)[s]            # class sums modulo 2 at a root of unity of order 2, in Z[x]/(Phi_2, 3)
b2 = bool(bad3(e, 2)[s])
print(f"S0'/S1' without `not p | d`: e = {e}, all +, p = 2, i = 1, d = 2: 3-bad at p^i d = 4: {b4}; class sums of the "
      f"classes 0 and 1 modulo 2 at eta = -1: {cs[0].tolist()} and {cs[1].tolist()} (unequal: {not (cs[0] == cs[1]).all()}); "
      f"level 1 of 2 is not live, and 3-bad at p^(i-1) d = 2: {b2}")
# `hlive` is needed in S1': e = (0, 1), all +, p = 2, i = 1, d = 1
e = [0, 1]
print(f"S1' without `hlive`: e = {e}, all +, p = 2, i = 1, d = 1: 3-bad at 2: {bool(bad3(e, 2)[3])}; 3-bad at 1: "
      f"{bool(bad3(e, 1)[3])}")
