"""What the reach m = 36 rests on inside the recursion Gamma (same recursion as ref_gamma.py, exact fractions).
Variant 'full'  : as in section 5 of sign-all-result.md (Lemma 3T, and Lemma 3' when a = 1).
Variant 'no3p'  : without the candidate of Lemma 3' (min(G'/2, G' - L' 2^(1-p)) for a = 1), i.e. Lemma 3T only.
For each m the largest Gamma over the choices of q (none, or a prime of n'_m) is printed for both variants.
usage: ref_gamma_variants.py MMIN MMAX"""
import sys
from fractions import Fraction as Fr
from ref_gamma import lam, single, shape

def gamma(trees, use3p):
    k = len(trees); G = {}
    for mask in range(1, 1 << k):
        idx = [i for i in range(k) if mask >> i & 1]
        if len(idx) == 1:
            G[mask] = single(*trees[idx[0]]); continue
        best = None
        for i in idx:
            g1 = G[mask & ~(1 << i)]
            if g1 <= 0: continue
            p, a = trees[i]; L = 1
            for j in idx:
                if j != i: L *= trees[j][1] + 1
            cand = min(single(p, a) * g1, Fr(3, 4) * g1 - L * lam(p, a))
            if a == 1 and use3p:
                cand = max(cand, min(g1 / 2, g1 - Fr(L, 2 ** (p - 1))))
            if best is None or cand > best: best = cand
        G[mask] = best if best is not None else Fr(-1)
    return G[(1 << k) - 1]

lo, hi = int(sys.argv[1]), int(sys.argv[2])
last = {True: None, False: None}
for m in range(lo, hi + 1):
    f = shape(m)
    if len(f) <= 2: continue
    out = []
    for use3p in (True, False):
        best = max(gamma([(p, a) for p, a in f if p != q], use3p) for q in [None] + [p for p, _ in f])
        out.append(best)
        if best > 0: last[use3p] = m
    print(f'm={m}: full: {float(out[0]):.6g}   without Lemma 3\': {float(out[1]):.6g}')
print(f'last m with Gamma > 0: full recursion {last[True]}; without the candidate of Lemma 3\' {last[False]}')
