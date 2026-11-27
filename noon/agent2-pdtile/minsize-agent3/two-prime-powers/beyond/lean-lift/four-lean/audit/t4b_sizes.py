"""sizes_eq_two_all: for N and every set P of divisors of N, the sizes s (0 < s <= S) of the multisets on Z_{2N} whose
mask is divisible by Phi_d, among the d | 2N with d != 1, exactly for d in P, against the sizes of the multisets on Z_N
whose mask is divisible by Phi_d, among the d | N with d != 1, exactly for d in P.

A complete census of both groups up to size S (multisets that contain 0: the set of cyclotomic divisors does not change
under translation).  For each multiset its pattern {d | M, d != 1 : Phi_d divides the mask} is computed exactly.  A
multiset on Z_{2N} whose pattern has a member that does not divide N belongs to the left-hand set of no P that satisfies
the hypothesis hP; those are counted apart.
usage: t4b_sizes.py N S"""
import os
import sys
import time
from itertools import combinations_with_replacement, islice, chain
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import core
from t3_a1 import big_table


def census(M, S, batch_cells=24_000_000):
    """pattern (frozenset of divisors > 1) -> set of sizes"""
    ds = [d for d in core.divisors(M) if d != 1]
    res = {}
    count = 0
    if not ds:                       # M = 1: no d != 1; the pattern is empty for every size
        return {frozenset(): set(range(1, S + 1))}, S
    Tall, sl = big_table(M, ds)
    B = max(1000, batch_cells // M)
    for m in range(1, S + 1):
        it = combinations_with_replacement(range(M), m - 1)
        while True:
            flat = np.fromiter(chain.from_iterable(islice(it, B)), dtype=np.int32)
            if flat.size == 0 and m > 1:
                break
            E = np.zeros((flat.size // (m - 1) if m > 1 else 1, m), dtype=np.int32)
            if m > 1:
                E[:, 1:] = flat.reshape(-1, m - 1)
            count += E.shape[0]
            R = np.zeros((E.shape[0], Tall.shape[1]), dtype=np.int16)
            for k in range(m):
                R += Tall[E[:, k]]
            bits = np.zeros(E.shape[0], dtype=np.int64)
            for j, d in enumerate(ds):
                a, b = sl[d]
                bits |= (~R[:, a:b].any(axis=1)).astype(np.int64) << j
            for v in np.unique(bits):
                pat = frozenset(d for j, d in enumerate(ds) if (int(v) >> j) & 1)
                res.setdefault(pat, set()).add(m)
            if m == 1:
                break
    return res, count


if __name__ == '__main__':
    N, S = int(sys.argv[1]), int(sys.argv[2])
    t0 = time.time()
    small, c1 = census(N, S)
    big, c2 = census(2 * N, S)
    divN = set(core.divisors(N))
    left = {P: s for P, s in big.items() if P <= divN}
    outside = {P: s for P, s in big.items() if not P <= divN}
    pats = set(left) | set(small)
    diff = [P for P in pats if left.get(P, set()) != small.get(P, set())]
    print('N = %d S = %d multisets %d on Z_N and %d on Z_2N; patterns P (sets of divisors > 1 of N) with a nonempty side: %d; '
          'DIFFERENT sets of sizes: %d %s; patterns on Z_2N with a divisor not dividing N: %d (%.0f s)'
          % (N, S, c1, c2, len(pats), len(diff), [(sorted(P), sorted(left.get(P, [])), sorted(small.get(P, []))) for P in diff[:3]],
             len(outside), time.time() - t0), flush=True)
