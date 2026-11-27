# check_interval.py -- the interval {0, .., m-1} on the groups of the author's test "All signings, 14 to 18 elements"
# (the first multiset of each of his "interval" runs is this interval): which levels d have a bad signing at all?
# All 2^m signings, exact division (rfast.py), after contraction with my routine.
import sys, math
from fractions import Fraction
import numpy as np
from rlib import divisors, contract_all, mu, all_levels_full
from rfast import bad_fast

for n, m in ((315, 18), (675, 16), (675, 18), (1575, 18), (3465, 16), (4725, 16)):
    B = list(range(m))
    Bf, nf, steps = contract_all(B, n, "deep")
    assert all_levels_full(Bf, nf)
    full = 1 << m
    anybad = np.zeros(full, dtype=bool)
    live = {}
    only_gt1 = np.zeros(full, dtype=bool)
    for d in divisors(nf):
        v = bad_fast(Bf, d)
        k = int(v.sum())
        if k:
            live[d] = k
        assert k << mu(d) <= full or d == 1
        anybad |= v
        if d > 1:
            only_gt1 |= v
    bad1 = bad_fast(Bf, 1)
    good = full - int(anybad.sum())
    print("Z_%d, {0..%d}: n_flat = %d (%d divisors); good %d/%d = %s = %.4f; 1 - c_m = %.4f; signings bad at some d > 1 and not at d = 1: %d"
          % (n, m - 1, nf, len(divisors(nf)), good, full, Fraction(good, full), good / full, 1 - math.comb(m, m // 2) / full, int((only_gt1 & ~bad1).sum())))
    print("     levels with a bad signing (d: number of signings):", live)
