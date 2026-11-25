# Sanity check of the parenthetical remark (note's definition of "unsupported"): in Z_36, is there a tile A with a
# zero d>1 such that no s in S_A divides d exactly and every prime of d divides |A| ?  By (T1) for tiles such an A
# has |A| = 6 (see report), so enumerate all 6-subsets containing 0.
import numpy as np, sys
from itertools import combinations
from math import gcd
from sympy import divisors
from brute import prime_powers, exact
M = int(sys.argv[1]); K = int(sys.argv[2])
divs = [d for d in divisors(M) if d > 1]; PP = prime_powers(M)
combos = np.array([(0,) + c for c in combinations(range(1, M), K - 1)], dtype=np.int64)
print(len(combos), "sets")
Z = np.zeros((len(combos), len(divs)), dtype=bool)
for j, d in enumerate(divs):
    xi = M // d
    val = np.exp(2j * np.pi * xi * combos / M).sum(axis=1)
    Z[:, j] = np.abs(val) < 1e-9
def tiles(A):
    k = len(A)
    if M % k: return False
    full = (1 << M) - 1
    trans = [sum(1 << ((a + b) % M) for a in A) for b in range(M)]
    def rec(cov):
        if cov == full: return True
        v = (~cov & full); v = (v & -v).bit_length() - 1
        for b in range(M):
            t = trans[b]
            if (t >> v) & 1 and not (t & cov):
                if rec(cov | t): return True
        return False
    return rec(0)
pats = {}
for i in range(len(combos)):
    key = tuple(Z[i]); pats.setdefault(key, []).append(i)
ntile = 0; found = 0; orphan_tiles = 0
for key, idx in pats.items():
    z = [d for d, b in zip(divs, key) if b]
    sa = [s for (s, p, a) in PP if s in z]
    orph = [d for d in z if not any(exact(s, d) for s in sa)]
    uns = [d for d in orph if all(K % p == 0 for p in set(p for (s, p, a) in PP if d % p == 0))]
    for i in idx:
        A = [int(x) for x in combos[i]]
        if tiles(A):
            ntile += 1
            if orph: orphan_tiles += 1
            if uns:
                found += 1
                if found <= 3: print("tile with unsupported zero:", A, z, uns)
print(f"M={M}, |A|={K}: tiles {ntile}, tiles with an orphan zero {orphan_tiles}, tiles with an unsupported zero (note's sense) {found}")
