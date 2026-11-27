"""Least share of good signings, by exhaustion.  For a modulus n and a size m: every multiset of m elements of Z_n that
contains 0 (translation does not change the share), every signing with the first sign + (a global sign does not change
goodness).  A signing is bad if its signed mask is divisible by Phi_d for some d | n; tested exactly, in integers, by
reducing X^x modulo Phi_d.  Prints, for each (n, m): the number of multisets, the least share of good signings, how many
multisets have it, and up to three of them.
usage: minshare.py M N [N ...]"""
import sys, itertools
from fractions import Fraction
import numpy as np
from sympy import cyclotomic_poly, Poly, symbols, divisors, ZZ
X = symbols('X')
def red_matrix(n):
    rows = []; blocks = []
    for d in divisors(n):
        phi = Poly(cyclotomic_poly(d, X), X, domain=ZZ); k = phi.degree()
        M = np.zeros((k, n), dtype=np.int64)
        for x in range(n):
            r = Poly(X**(x % d), X, domain=ZZ).rem(phi)
            c = r.all_coeffs()[::-1]
            for i, v in enumerate(c): M[i, x] = int(v)
        blocks.append((len(rows) and sum(b[1] for b in blocks) or 0, k, d)); rows.append(M)
    return np.vstack(rows), blocks
def run(n, m, batch=20000):
    R, blocks = red_matrix(n)
    E = np.array([[1] + [1 if (s >> i) & 1 else -1 for i in range(m - 1)] for s in range(2 ** (m - 1))], dtype=np.int64).T  # m x 2^(m-1)
    best = None; ex = []; count = 0; nbest = 0
    it = itertools.combinations_with_replacement(range(n), m - 1)
    while True:
        chunk = list(itertools.islice(it, batch))
        if not chunk: break
        XS = np.zeros((len(chunk), m), dtype=np.int64); XS[:, 1:] = np.array(chunk, dtype=np.int64)
        A = R[:, XS]                      # rows x batch x m
        V = A @ E                         # rows x batch x 2^(m-1)
        bad = np.zeros(V.shape[1:], dtype=bool)
        for (start, k, d) in blocks:
            bad |= ~np.any(V[start:start + k] != 0, axis=0)
        good = (~bad).sum(axis=1)
        count += len(chunk)
        g = int(good.min())
        if best is None or g < best: best = g; ex = []; nbest = 0
        if g == best:
            idx = np.nonzero(good == g)[0]; nbest += len(idx)
            for i in idx[:3]:
                if len(ex) < 3: ex.append(tuple(int(v) for v in XS[i]))
    return count, Fraction(best, 2 ** (m - 1)), nbest, ex
if __name__ == '__main__':
    m = int(sys.argv[1])
    for n in map(int, sys.argv[2:]):
        c, sh, nb, ex = run(n, m)
        print(f"m = {m}  n = {n:4d}  multisets {c:10d}  least share {str(sh):>7s} = {float(sh):.4f}  attained by {nb:7d}  e.g. {ex}", flush=True)
