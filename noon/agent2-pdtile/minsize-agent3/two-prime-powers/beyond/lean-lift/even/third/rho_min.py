"""Exploration (mine, 27 Nov 2026): rho_2(B) = share of signings of a multiset B on Z_{2^k} that are 3-bad at no 2^j, j <= k.
3-bad at 2^0: the signed count is 0 mod 3.  3-bad at 2^j, j >= 1: in every class c mod 2^(j-1) the signed counts of the
two halves mod 2^j are congruent mod 3.  Brute force over all signings; every multiset given by its counts on Z_{2^k}
(up to translation: the least element is 0).  Prints the least rho_2 for each m, the p_(m-1) it is compared with, and
the multisets at which the least and the second least value are taken.
usage: rho_min.py K MMAX"""
import sys, itertools
from fractions import Fraction
import numpy as np
K, MMAX = int(sys.argv[1]), int(sys.argv[2]); N = 1 << K
def p(r):   # P(sum of r signs = 0 mod 3)
    return Fraction(sum(1 for s in itertools.product((1, -1), repeat=r) if sum(s) % 3 == 0), 2 ** r) if r <= 16 else None
def signs(m):
    a = np.array(list(itertools.product((1, -1), repeat=m)), dtype=np.int8); return a
def rho(elems, S):
    m = len(elems); e = np.array(elems)
    good = (S.sum(axis=1) % 3 != 0)
    for j in range(1, K + 1):
        half = 1 << (j - 1)
        bad = np.ones(len(S), bool)
        for c in range(half):
            i0 = np.nonzero(e % (1 << j) == c)[0]; i1 = np.nonzero(e % (1 << j) == c + half)[0]
            if len(i0) == 0 and len(i1) == 0: continue
            d = S[:, i0].sum(axis=1) - S[:, i1].sum(axis=1)
            bad &= (d % 3 == 0)
        good &= ~bad
    return Fraction(int(good.sum()), len(S))
for m in range(3, MMAX + 1):
    S = signs(m); vals = {}
    for rest in itertools.combinations_with_replacement(range(N), m - 1):
        el = (0,) + rest
        r = rho(el, S); vals.setdefault(r, []).append(el)
    ks = sorted(vals)
    print(f'm={m} on Z_{N}: {sum(len(v) for v in vals.values())} multisets containing 0; least rho_2 = {ks[0]} (p_(m-1) = {p(m-1)}), at {len(vals[ks[0]])} multisets, e.g. {vals[ks[0]][:3]}')
    for q in ks[1:4]: print(f'      next: {q} = {float(q):.4f} at {len(vals[q])}, e.g. {vals[q][:2]}')
    sys.stdout.flush()
