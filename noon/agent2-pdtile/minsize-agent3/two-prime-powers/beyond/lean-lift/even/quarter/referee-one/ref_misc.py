"""Referee: (1) the two multisets of the other text (two/result.md, section 7), by the definition and through every
check of ref_odd.analyse; (2) the least share of good signings on small even n for 5 and 6 elements (the text's
Corollary says 1/2 and 5/16 are attained, citing data it did not recompute)."""
import sys, itertools
from fractions import Fraction as Fr
import numpy as np
from cyc import divisors, signs, bad_at
from ref_odd import analyse

for n, B, claim in [(225, [19, 19, 22, 22, 36, 36, 110, 110, 133, 133], Fr(73, 256)),
                    (675, [17, 17, 66, 66, 106, 106, 384, 384, 558, 558, 665, 665], Fr(269, 1024)),
                    (45, [0, 1, 1, 3, 12, 20, 24, 27, 29, 33], Fr(73, 256)),
                    (135, [0, 0, 1, 1, 2, 29, 33, 54, 57, 57, 87, 108], Fr(269, 1024))]:
    s_bad, s_3, s_rest, where = analyse(n, B)
    print(f"Z_{n} m={len(B)} {B}: bad {s_bad}, claimed {claim}, equal {s_bad == claim}; at a power of 3: {s_3}; by d: " +
          ", ".join(f"{d}: {v}" for d, v in where.items()), flush=True)

for m, ns, claim in [(5, (6, 10, 12, 18, 30), Fr(1, 2)), (6, (6, 12, 18), Fr(5, 16))]:
    E = signs(m)
    for n in ns:
        divs = divisors(n); best = None; ex = None; cnt = 0
        for rest in itertools.combinations_with_replacement(range(n), m - 1):
            B = [0] + list(rest)
            bad = np.zeros(2 ** m, dtype=bool)
            for d in divs:
                bad |= bad_at(n, B, d, E)
            g = 2 ** m - int(bad.sum()); cnt += 1
            if best is None or g < best:
                best = g; ex = B
        print(f"even n = {n}, m = {m}: {cnt} multisets with 0; least share of good signings {Fr(best, 2 ** m)} at {ex}; the text's value {claim}: attained here: {Fr(best, 2 ** m) == claim}; never below: {Fr(best, 2 ** m) >= claim}", flush=True)
