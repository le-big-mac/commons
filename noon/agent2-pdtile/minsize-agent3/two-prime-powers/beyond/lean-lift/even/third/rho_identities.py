"""Test (mine, 27 Nov 2026) of the three identities behind the induction for  rho_2(B) >= p_(m-1):
 (A)  B has an atom y of multiplicity t >= 2:  rho(B) = (1 - p_t) rho(B with y^t -> y) + p_t rho(B without y^t)   [rho(empty) = 0]
 (B1) B a set, r its deepest split level, kappa = {y, z} a pair class at depth r-1, and some class at depth r-1 is a
      single element:  rho(B) = ( rho(B without z) + rho(B without y, z) ) / 2
 (B2) B a set all of whose classes at depth r-1 are pairs, B~ the set of the pairs on Z_(2^(r-1)):
      rho(B) = 2^(-n) * sum over the PROPER subsets U of B~ of rho(U)      [rho(empty) = 0]
and of the conclusion rho(B) >= p_(m-1).  rho by brute force over all signings, exact fractions.
usage: rho_identities.py K MMAX"""
import sys, itertools
from fractions import Fraction
from functools import lru_cache
from collections import Counter
import numpy as np
K, MMAX = int(sys.argv[1]), int(sys.argv[2]); N = 1 << K
def p(r): return Fraction(1, 3) + Fraction(2, 3) * Fraction(-1, 2) ** r
_S = {}
def signs(m):
    if m not in _S: _S[m] = np.array(list(itertools.product((1, -1), repeat=m)), dtype=np.int8).reshape(-1, m)
    return _S[m]
@lru_cache(maxsize=None)
def rho(el):
    m = len(el)
    if m == 0: return Fraction(0)
    S = signs(m); e = np.array(el)
    good = (S.sum(axis=1) % 3 != 0)
    for j in range(1, K + 1):
        half = 1 << (j - 1); bad = np.ones(len(S), bool)
        for c in range(half):
            i0 = np.nonzero(e % (1 << j) == c)[0]; i1 = np.nonzero(e % (1 << j) == c + half)[0]
            if len(i0) == 0 and len(i1) == 0: continue
            bad &= ((S[:, i0].sum(axis=1) - S[:, i1].sum(axis=1)) % 3 == 0)
        good &= ~bad
    return Fraction(int(good.sum()), len(S))
cnt = Counter(); worst = {}
for m in range(1, MMAX + 1):
    for el in itertools.combinations_with_replacement(range(N), m):
        r0 = rho(el); cnt['multisets'] += 1
        assert r0 >= p(m - 1), ('BOUND FAILS', el, r0)
        if r0 == p(m - 1): cnt['equality in the bound'] += 1
        c = Counter(el); rep = [y for y in c if c[y] >= 2]
        if rep:
            for y in rep:
                t = c[y]; rest = tuple(x for x in el if x != y); Bp = tuple(sorted(rest + (y,)))
                assert r0 == (1 - p(t)) * rho(Bp) + p(t) * rho(rest), ('A FAILS', el, y)
                cnt['(A) checked'] += 1
            continue
        if m == 1: continue
        # a set: deepest split level r = the least r with all elements distinct mod 2^r
        r = next(j for j in range(1, K + 1) if len(set(x % (1 << j) for x in el)) == m)
        cls = {}
        for x in el: cls.setdefault(x % (1 << (r - 1)), []).append(x)
        pairs = [v for v in cls.values() if len(v) == 2]; singles = [v for v in cls.values() if len(v) == 1]
        assert pairs and all(len(v) <= 2 for v in cls.values())
        if singles:
            for (y, z) in pairs:
                a = tuple(x for x in el if x != z); b = tuple(x for x in el if x not in (y, z))
                assert r0 == (rho(a) + rho(b)) / 2, ('B1 FAILS', el, y, z)
                cnt['(B1) checked'] += 1
        else:
            Bt = sorted(cls); n = len(Bt); tot = Fraction(0)
            for u in range(0, n):
                for U in itertools.combinations(Bt, u): tot += rho(tuple(U))
            assert r0 == tot / 2 ** n, ('B2 FAILS', el)
            cnt['(B2) checked'] += 1
    print(f'Z_{N}, up to m = {m}:', dict(cnt), flush=True)
print('no identity failed; no multiset below p_(m-1)')
