"""Referee's own evaluation of the recursion Gamma of section 5 of sign-all-result.md, written from the text of that
section (not from coverage2.py), on the shapes

    n'_m = product over odd primes p <= m of p^floor((m-1)/(p-1)).

Definition used (section 5 and Lemmas T, S of sign-all-result.md):
    omega(p)   = 2^(1-p),   lambda(p, a) = omega + omega^2 + ... + omega^a
    single(p,a)= 1/2 if a = 1 or p >= 5;  5/8 - lambda(3, a) if p = 3 and a >= 2
    Gamma({(p,a)}) = single(p,a)
    Gamma(S), |S| >= 2 = max over (p,a) in S with G' = Gamma(S - {(p,a)}) > 0 of
            min( single(p,a)*G' , 3/4*G' - L'*lambda(p,a) ),  and if a = 1 also of  min( G'/2 , G' - L'*2^(1-p) ),
       L' = product of (c+1) over (r,c) in S - {(p,a)};   Gamma(S) = -1 if there is no such pair.
Theorem 7 applies to n = m' * q^b (q an odd prime not dividing m', b >= 0) or n = m' when Gamma(m') > 0.

For each m the program takes q = none and q = each prime of n'_m in turn and prints Gamma(n'_m without the q-part),
as exact fractions.  Exact arithmetic (fractions) throughout.
usage: ref_gamma.py MMIN MMAX
"""
import sys
from fractions import Fraction as Fr

def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]

def lam(p, a):
    w = Fr(1, 2 ** (p - 1))
    s = Fr(0)
    t = Fr(1)
    for _ in range(a):
        t *= w
        s += t
    return s

def single(p, a):
    if a == 1 or p >= 5:
        return Fr(1, 2)
    assert p == 3 and a >= 2
    return Fr(5, 8) - lam(3, a)

def gamma_all(trees):
    """trees: list of (p, a), distinct odd primes.  Returns Gamma of the whole set, by subsets (bit masks), bottom up."""
    k = len(trees)
    G = {}
    for mask in range(1, 1 << k):
        idx = [i for i in range(k) if mask >> i & 1]
        if len(idx) == 1:
            G[mask] = single(*trees[idx[0]])
            continue
        best = Fr(-1)
        found = False
        for i in idx:
            rest = mask & ~(1 << i)
            g1 = G[rest]
            if g1 <= 0:
                continue
            p, a = trees[i]
            L = 1
            for j in idx:
                if j != i:
                    L *= trees[j][1] + 1
            cand = min(single(p, a) * g1, Fr(3, 4) * g1 - L * lam(p, a))
            if a == 1:
                cand = max(cand, min(g1 / 2, g1 - Fr(L, 2 ** (p - 1))))
            if not found or cand > best:
                best = cand
                found = True
        G[mask] = best if found else Fr(-1)
    return G[(1 << k) - 1]

def shape(m):
    return [(p, (m - 1) // (p - 1)) for p in primes_upto(m) if p >= 3 and (m - 1) // (p - 1) >= 1]

if __name__ == '__main__':
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    last_ok = None
    first_bad = None
    prev = (None, None)
    for m in range(lo, hi + 1):
        f = shape(m)
        sh = ' * '.join(f'{p}^{a}' if a > 1 else f'{p}' for p, a in f)
        if len(f) <= 2:
            print(f'm={m}: n\'_m = {sh if sh else 1}: at most two primes')
            continue
        if prev[0] == f:                     # n'_m = n'_(m-1) for even m: same shape, same values
            res = prev[1]
        else:
            res = []
            for q in [None] + [p for p, _ in f]:
                rest = [(p, a) for p, a in f if p != q]
                g = gamma_all(rest)
                res.append((q, g))
            prev = (f, res)
        pos = [(q, g) for q, g in res if g > 0]
        line = f'm={m}: n\'_m = {sh}: '
        if pos:
            line += 'Gamma > 0 for q in ' + ', '.join(f'{q}: {g} (~{float(g):.3g})' for q, g in pos)
            if first_bad is None:
                last_ok = m
        else:
            line += 'Gamma <= 0 for q = none and for every prime q of n\'_m (values: ' + ', '.join(f'{q}: {g}' for q, g in res) + ')'
            if first_bad is None:
                first_bad = m
        print(line, flush=True)
    print(f'last m in the range with some Gamma > 0 before the first failure: {last_ok}; first m with Gamma <= 0 for every choice: {first_bad}')
