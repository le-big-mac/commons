"""Full support: every residue of Z_n once.  a(n) = number of signings bad on Z_n (the number of singular n x n circulants
with entries +-1, OEIS A144926); F(n) = number of signings bad for the reduction modulo the odd part of n.
All 2^n signings (computed as twice the count with the first sign +); exact integer arithmetic.
usage: full_support.py N [N ...]"""
import sys
import numpy as np
from minshare import red_matrix
def counts(n):
    n1 = n
    while n1 % 2 == 0: n1 //= 2
    R, blocks = red_matrix(n); R1, blocks1 = red_matrix(n1)
    m = n; tot = 2 ** (m - 1); bad = bad1 = 0; step = 1 << 14
    xs = np.arange(n)
    A = R[:, xs]; A1 = R1[:, xs % n1]
    for s0 in range(0, tot, step):
        s = np.arange(s0, min(tot, s0 + step), dtype=np.int64)
        E = np.ones((m, len(s)), dtype=np.int64)
        for i in range(m - 1): E[i + 1] = np.where((s >> i) & 1, 1, -1)
        for (AA, bl, which) in ((A, blocks, 0), (A1, blocks1, 1)):
            V = AA @ E
            b = np.zeros(len(s), dtype=bool)
            for (start, k, d) in bl: b |= ~np.any(V[start:start + k] != 0, axis=0)
            if which == 0: bad += int(b.sum())
            else: bad1 += int(b.sum())
    return 2 * bad, 2 * bad1
for n in map(int, sys.argv[1:]):
    a, F = counts(n)
    print(f"n = {n:3d}  a(n) = {a:10d}  F(n) = {F:10d}  2 F(n) = {2*F:10d}  a(n) <= 2 F(n): {a <= 2*F}", flush=True)
