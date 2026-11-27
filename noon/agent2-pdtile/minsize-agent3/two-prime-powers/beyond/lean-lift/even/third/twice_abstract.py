"""Test (mine) of Theorem T in the abstract: elements with positions in Z_(2^k) and nonzero values in an abelian group
V without 2-torsion; Q = P(some level 0..k bad) <= 2 z, z = P(level 0 bad).  Brute force over all signings.
V = Z^2 (pairs of small integers) or V = (Z/3)^2 or Z/9 or Z/5.
usage: twice_abstract.py K MMAX COUNT SEED"""
import sys, itertools, random
from fractions import Fraction
import numpy as np
K, MMAX, COUNT, SEED = (int(x) for x in sys.argv[1:5]); N = 1 << K; rng = random.Random(SEED)
def run(pos, val, mod):
    m = len(pos); S = np.array(list(itertools.product((1, -1), repeat=m)), dtype=np.int64).reshape(-1, m)
    pos = np.array(pos); val = np.array(val, dtype=np.int64)             # val: m x dim
    def zero(M):                                                          # rows that are 0 in V
        return ~np.any(M % mod if mod else M, axis=1)
    lev0 = zero(S @ val); union = lev0.copy()
    for j in range(1, K + 1):
        half = 1 << (j - 1); bad = np.ones(len(S), bool)
        for c in range(half):
            i0 = np.nonzero(pos % (1 << j) == c)[0]; i1 = np.nonzero(pos % (1 << j) == c + half)[0]
            if len(i0) == 0 and len(i1) == 0: continue
            bad &= zero(S[:, i0] @ val[i0] - S[:, i1] @ val[i1])
        union |= bad
    return int(union.sum()), int(lev0.sum())
fails = 0; maxratio = Fraction(0); n = 0; eq = 0
for _ in range(COUNT):
    m = rng.randint(1, MMAX); kind = rng.choice(['Z2', 'F3sq', 'Z9', 'Z5', 'Zsmall'])
    pos = [rng.randrange(N) for _ in range(m)]
    if rng.random() < 0.4:                                                # few positions, to get atoms and pairs
        base = [rng.randrange(N) for _ in range(rng.randint(1, 3))]; pos = [rng.choice(base) for _ in range(m)]
    if kind == 'Z2':   mod = 0; val = [rng.choice([(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (2, 0), (0, 2)]) for _ in range(m)]
    elif kind == 'Zsmall': mod = 0; val = [(rng.choice([1, -1, 2, 1, 1, 3]),) for _ in range(m)]
    elif kind == 'F3sq': mod = 3; val = [rng.choice([(1, 0), (0, 1), (1, 1), (1, 2), (2, 0), (0, 2)]) for _ in range(m)]
    elif kind == 'Z9': mod = 9; val = [(rng.choice([1, 2, 3, 4, 6, 8]),) for _ in range(m)]
    else: mod = 5; val = [(rng.choice([1, 2, 3, 4]),) for _ in range(m)]
    q, z = run(pos, val, mod); n += 1
    if q > 2 * z: fails += 1; print('FAILS', kind, pos, val, q, z, flush=True)
    if z: maxratio = max(maxratio, Fraction(q, z)); eq += (q == 2 * z)
print(f'K={K} (positions on Z_{N}), up to {MMAX} elements, {n} valued multisets (seed {SEED}): failures {fails}; largest ratio Q/z {maxratio}; Q = 2z in {eq} cases')
