"""Check of one fact in the caution added to section 6 after the referee's report:
"for the interval {0, .., 17} only the levels 1, 3, 9 have a bad signing".

The interval {0, .., 17} on Z_315 and on Z_675 (contracted first, with the routine of lib4), all 2^17 signings
with the first sign fixed; for every d | n_flat the number of signings with Phi_d | S, and the number of good ones
(even_exact.py reports 102951 of 131072 for the multisets with 18 elements).  Exact integers.

usage: check_interval18.py
"""
import numpy as np
from lib4 import all_signs, bad_table, contract, all_full

m = 18
E = all_signs(m)
for n0 in (315, 675):
    B, n = contract(list(range(m)), n0)
    assert all_full(B, n)
    tab = bad_table(B, n, E)
    bad = np.zeros(E.shape[0], dtype=bool)
    counts = {}
    for d, b in sorted(tab.items()):
        counts[d] = int(b.sum())
        bad |= b
    print(f"interval {{0..{m - 1}}} on Z_{n0}: n_flat = {n}; signings (first sign fixed) {E.shape[0]}; good {int((~bad).sum())}")
    print("  number of signings bad at d, for every d | n_flat:", counts)
    print("  levels with a bad signing:", [d for d, c in counts.items() if c])
