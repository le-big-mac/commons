# Referee's recount of some shares of section 4 (largest share of bad signings on odd n, least share of good
# signings on even n), every multiset containing 0, ALL signings.  Imports nothing of the author's.
# usage: least.py m n [n ...]
import sys, itertools
from fractions import Fraction as Fr
import numpy as np
from cyc import divisors, xpow_mod

def run(n, m):
    dn = divisors(n)
    rows = [np.array(xpow_mod(d, n), dtype=np.int64).reshape(n, -1) for d in dn]
    T = np.concatenate(rows, axis=1)
    starts = np.cumsum([0] + [r.shape[1] for r in rows])[:-1]
    S = 1 << m
    sg = np.array([[-1 if (s >> i) & 1 else 1 for i in range(m)] for s in range(S)], dtype=np.int64)
    most, ex, cnt, nmost = -1, None, 0, 0
    for c in itertools.combinations_with_replacement(range(n), m - 1):
        B = [0] + list(c)
        R = sg @ T[B]
        Z = np.add.reduceat((R != 0).astype(np.int32), starts, axis=1) == 0
        bad = int(Z.any(axis=1).sum())
        cnt += 1
        if bad > most:
            most, ex, nmost = bad, tuple(B), 0
        if bad == most:
            nmost += 1
    return cnt, Fr(most, S), nmost, ex

m = int(sys.argv[1])
for n in map(int, sys.argv[2:]):
    cnt, sh, nmost, ex = run(n, m)
    print(f"m={m} n={n:3d} multisets {cnt:7d}  largest share of bad signings {sh}  (least share of good {1 - sh})  "
          f"at {nmost} multisets, e.g. {ex}", flush=True)
