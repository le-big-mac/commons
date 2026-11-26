"""Self-test of upset_lib.py: the fast layer against the slow literal layer and against sympy.

1. cyclotomic polynomials against sympy.cyclotomic_poly, d = 1 .. 150;
2. divisibility of a mask by Phi_d: long division here against sympy's division over Z, on random multisets;
3. enum_le / enum_le_chunks: counts and distinctness;
4. div_flags (linear remainder map) against the long division, on every multiset of small size in some groups;
5. solutions_lattice against plain enumeration + division, where both are feasible;
6. sums_of_periodic against exists_g (exhaustive search for the family g), on every multiset of small size;
7. IsUpSet / corners literal against the 'intended' versions of check_table_defs.py.
"""
import random
import sys
from math import comb

import numpy as np
import sympy

from upset_lib import *
import check_table_defs as intended

random.seed(12345)
X = sympy.symbols('X')

# 1
for d in range(1, 151):
    ref = sympy.Poly(sympy.cyclotomic_poly(d, X), X).all_coeffs()[::-1]
    assert [int(c) for c in ref] == cyclotomic(d), d
print('1. cyclotomic(d) equals sympy.cyclotomic_poly for d = 1..150')

# 2
n2 = 0
for M in (4, 6, 8, 9, 12, 18, 36, 100):
    for _ in range(150):
        kind = random.random()
        if kind < 0.5:
            w = [random.randint(0, 3) for _ in range(M)]
        else:                                    # a sum of cosets, so that divisibility does happen
            w = [0] * M
            for _ in range(random.randint(1, 3)):
                c = random.choice(nat_divisors(M))
                s = random.randrange(M)
                for x in range(M):
                    if (x - s) % c == 0:
                        w[x] += 1
        pw = sympy.Poly(sum(int(w[a]) * X**a for a in range(M)), X, domain='ZZ')
        for d in nat_divisors(M):
            pd = sympy.Poly(sympy.cyclotomic_poly(d, X), X, domain='ZZ')
            q, r = sympy.div(pw, pd, domain='ZZ')
            assert (r.is_zero) == cyc_divides_mask(d, w)
            n2 += 1
print('2. long division agrees with sympy.div over ZZ on %d (multiset, d) pairs' % n2)

# 3
for (k, S) in [(1, 5), (3, 4), (6, 6), (12, 5), (9, 9)]:
    A = enum_le(k, S)
    assert len(A) == comb(k + S, k) and len(np.unique(A, axis=0)) == len(A) and A.sum(axis=1).max() <= S
    Bc = np.concatenate(list(enum_le_chunks(k, S, chunk=1000)), axis=0)
    assert same_rows(A, Bc) and len(Bc) == len(A)
print('3. enum_le and enum_le_chunks give comb(k + S, k) distinct vectors of sum <= S')

# 4, 5, 6
n4 = n5 = n6 = 0
for (M, S) in [(1, 6), (2, 6), (3, 6), (4, 7), (5, 5), (6, 6), (8, 5), (9, 5), (10, 4), (12, 4), (18, 3)]:
    W = enum_le(M, S)
    dv = nat_divisors(M)
    fl = div_flags(W, M, dv)
    slow = {d: np.array([cyc_divides_mask(d, w) for w in W]) for d in dv}
    for d in dv:
        assert np.array_equal(fl[d], slow[d]), (M, d)
        n4 += len(W)
    for D in all_upsets(M):
        cs = corners_lean(M, D)
        L_slow = np.ones(len(W), dtype=bool)
        for d in D:
            L_slow &= slow[d]
        L = solutions_lattice(M, D, S, chunk=5000)
        assert same_rows(L, W[L_slow]), (M, D)
        n5 += 1
        Rset = sums_of_periodic(M, cs, S)
        assert len(np.unique(Rset, axis=0)) == len(Rset)
        R_slow = np.array([exists_g(w, M, cs) is not None for w in W])
        assert same_rows(Rset, W[R_slow]), (M, D)
        # the family found by the search really is a family as in the Lean text
        for w in W[R_slow][:50]:
            g = exists_g(w, M, cs)
            assert set(g) == set(cs) and all(periodic(g[c], M, c) and min(g[c]) >= 0 for c in cs)
            assert [sum(g[c][a] for c in cs) for a in range(M)] == [int(x) for x in w]
        n6 += 1
print('4. div_flags agrees with long division on %d (multiset, d) pairs' % n4)
print('5. solutions_lattice agrees with enumeration + long division for %d (M, D) pairs' % n5)
print('6. sums_of_periodic agrees with the exhaustive search for g for %d (M, D) pairs' % n6)

# 7
n7 = 0
for M in list(range(1, 41)) + [72, 100, 108]:
    dv = nat_divisors(M)
    assert dv == intended.divisors(M)
    import itertools
    subsets = itertools.chain.from_iterable(itertools.combinations(dv, k) for k in range(len(dv) + 1))
    for D in subsets:
        if len(dv) > 9 and random.random() > 0.2:
            continue
        assert is_upset_lean(M, D) == intended.is_upset_intended(M, set(D))
        assert corners_lean(M, D) == intended.corners_intended(M, set(D))
        n7 += 1
print('7. literal IsUpSet / corners agree with the intended ones on %d (M, D) pairs' % n7)
print('selftest passed')
