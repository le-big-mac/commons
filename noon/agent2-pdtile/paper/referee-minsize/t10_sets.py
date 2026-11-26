"""Section 1.3: "No unbalanced set has F = [1,n] != E", by plain enumeration of all subsets of small groups.
Also: for each pattern, the least size of a set against the least size of a multiset (Theorem 1's formula)."""
import sys, itertools
import numpy as np
from lib import root_pattern, theorem_value
for (p, q, n) in [(2, 3, 1), (3, 2, 1), (2, 3, 2), (3, 2, 2), (2, 5, 2)]:
    M = p ** n * q
    full = frozenset(range(1, n + 1))
    viol = 0
    least = {}
    for bits in range(1, 1 << M):
        A = np.array([(bits >> i) & 1 for i in range(M)], dtype=np.int64).reshape(p ** n, q)
        E, F, bal = root_pattern(A, p, n)
        if (not bal) and F == full and E != full:
            viol += 1
        k = (E, F, bal)
        s = int(A.sum())
        if k not in least or s < least[k]:
            least[k] = s
    same = sum(1 for (E, F, bal), s in least.items() if s == theorem_value(p, q, n, E, F, bal))
    smaller = sum(1 for (E, F, bal), s in least.items() if s < theorem_value(p, q, n, E, F, bal))
    print(f"p={p} q={q} n={n} Z_{M}: all {2**M - 1} nonempty subsets; unbalanced sets with F=[1,n] != E: {viol}; "
          f"patterns that some set has: {len(least)} of {2**(2*n+1)}; least set = Theorem 1's value in {same}; least set smaller than Theorem 1's value in {smaller}")
