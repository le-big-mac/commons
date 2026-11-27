"""A' and B for 0, 1 and 2 elements (where the statements do not apply): which families have no 3-good / good signing?
Expected: the empty family; no one-element family; among the pairs exactly those with a - b of even additive order
in Z_n (the exceptional pairs).  Every multiset on Z_n, no reduction; all signings; for a list of moduli.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from itertools import combinations_with_replacement
import numpy as np
from ecore import bad, bad3, divisors


def add_order(x, n):
    t, y = 1, x % n
    while y:
        y = (y + x) % n
        t += 1
    return t


def no_good(e, n, mode):
    m = len(e)
    U = np.zeros(1 << m, dtype=bool)
    for d in divisors(n):
        U |= bad3(e, d) if mode == 'A' else bad(e, d)
    return bool(U.all())


rows = []
for mode, ns in (('A', [1, 2, 4, 5, 7, 8, 10, 14, 16, 20, 22, 25, 28, 32, 35, 40, 44, 50, 56, 64, 70, 80, 100, 140]),
                 ('B', [1, 2, 3, 4, 6, 8, 9, 10, 12, 15, 18, 20, 24, 28, 30, 36, 40, 42, 48, 60, 72, 84, 90, 120])):
    tot_pairs = tot_exc = 0
    for n in ns:
        assert no_good([], n, mode)
        assert not any(no_good([a], n, mode) for a in range(n))
        fail = {(a, b) for a, b in combinations_with_replacement(range(n), 2) if no_good([a, b], n, mode)}
        exc = {(a, b) for a, b in combinations_with_replacement(range(n), 2) if add_order(a - b, n) % 2 == 0}
        assert fail == exc, (mode, n)
        tot_pairs += n * (n + 1) // 2
        tot_exc += len(exc)
    rows.append((mode, ns, tot_pairs, tot_exc))
    print(f"{mode}: n in {ns}: the empty family has no {'3-good' if mode == 'A' else 'good'} signing; every one-element "
          f"family has one; of the {tot_pairs} pairs exactly the {tot_exc} with a - b of even order have none")
