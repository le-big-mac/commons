#!/usr/bin/env python3
"""Two multisets met in the tests whose bad share is above the brief's list, recounted from the definition:
every signing, the signed mask reduced modulo Phi_d for every d | n (integers).
Added after the referee's report (its item (v)): the referee's multiset of twelve elements on Z_45."""
import itertools
from fractions import Fraction
import test_cells as TC

for n, B in ((225, (19, 19, 22, 22, 36, 36, 110, 110, 133, 133)),
             (675, (17, 17, 66, 66, 106, 106, 384, 384, 558, 558, 665, 665)),
             (45, (5, 5, 22, 22, 26, 26, 27, 27, 29, 29, 38, 38))):
    m = len(B)
    bad = 0
    where = {}
    tabs = {d: TC.powtable(d) for d in TC.divisors(n)}
    for eps in itertools.product((1, -1), repeat=m):
        hit = []
        for d, tab in tabs.items():
            v = [0] * tab.shape[1]
            for e, b in zip(eps, B):
                row = tab[b % d]
                for j in range(len(v)):
                    v[j] += e * int(row[j])
            if not any(v):
                hit.append(d)
        if hit:
            bad += 1
            for d in hit:
                where[d] = where.get(d, 0) + 1
    print("Z_%d, m=%d, B=%s: bad signings %d of %d = %s; bad at d: %s" % (n, m, B, bad, 2 ** m, Fraction(bad, 2 ** m), dict(sorted(where.items()))), flush=True)
