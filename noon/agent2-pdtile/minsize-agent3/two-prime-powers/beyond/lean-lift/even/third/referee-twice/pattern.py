"""Share of 3-good signings of {0 (a times), 1, 2, 4, 13} on Z_20 and of a few relatives, by remainders."""
from fractions import Fraction
import numpy as np
import cyc_check as cc
ctx = cc.Ctx(20)
def share(B):
    m = len(B)
    bad, bad3 = ctx.flags(np.array([B], dtype=np.int64))
    any3 = np.zeros(1 << (m - 1), dtype=bool)
    for d in bad3: any3 |= bad3[d][0]
    return Fraction(int((~any3).sum()), 1 << (m - 1))
for a in range(1, 13):
    B = [0] * a + [1, 2, 4, 13]
    print(f"m = {len(B)}: {{0 x {a}, 1, 2, 4, 13}} on Z_20: share 3-good = {share(B)} = {float(share(B)):.5f}")
