"""What sizes_eq_mul_all would say without hP: for small N, s and a set P with a member that divides N*s but not N,
the two sets of sizes (up to S) from the census.  And P with a member that divides neither (no effect)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core
from t4b_sizes import census

for N, s, S in ((1, 2, 10), (3, 4, 8), (2, 6, 8), (15, 4, 4)):
    small, _ = census(N, S)
    big, _ = census(N * s, S)
    divN = set(core.divisors(N))
    shown = 0
    for Q, sizes in sorted(big.items(), key=lambda x: sorted(x[0])):
        if not Q <= divN and shown < 2:
            # P = Q: left = sizes; right = sizes on Z_N of the pattern Q restricted to the divisors of N
            right = small.get(frozenset(d for d in Q if d in divN), set())
            print('N = %d, s = %d, P = %s (not all divisors of N): sizes on Z_%d %s, on Z_%d %s -> %s'
                  % (N, s, sorted(Q), N * s, sorted(sizes), N, sorted(right), 'EQUAL' if sizes == right else 'different'))
            shown += 1
