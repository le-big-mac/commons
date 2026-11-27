"""A question behind lifting along the prime 2.  For odd n and a nonempty multiset B on Z_n: is there a choice of signs, one for each
element, such that the signed mask is divisible by NO Phi_d, d | n (d = 1 included: the signs do not add up to 0)?
Exhaustive over multisets up to a size, up to translation; exact arithmetic (remainders of integer polynomials).
usage: sign_lemma.py"""
import itertools, sys
import numpy as np
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X')
def remainder_maps(n):
    """for each d | n the matrix R_d with R_d @ v = coefficients of (sum v_i X^i) mod Phi_d"""
    out = {}
    for d in range(1, n + 1):
        if n % d: continue
        phi = Poly(cyclotomic_poly(d, X), X, domain=ZZ); deg = phi.degree()
        R = np.zeros((deg, n), dtype=np.int64)
        for i in range(n):
            c = Poly(X**i, X, domain=ZZ).rem(phi).all_coeffs()[::-1]
            for j, cj in enumerate(c): R[j, i] = int(cj)
        out[d] = R
    return out
for n, smax in [(3, 8), (5, 7), (7, 6), (9, 7), (15, 6), (21, 5), (25, 5), (27, 5), (45, 4), (105, 3)]:
    RM = remainder_maps(n); total = 0; fails = []
    for s in range(1, smax + 1):
        for comb in itertools.combinations_with_replacement(range(n), s):
            if comb[0] != 0: continue
            total += 1; good = False
            for signs in itertools.product((1, -1), repeat=s - 1):
                v = np.zeros(n, dtype=np.int64); v[0] += 1
                for x, t in zip(comb[1:], signs): v[x] += t
                if all((R @ v).any() for R in RM.values()): good = True; break
            if not good: fails.append(comb)
    print(f'n = {n}, multisets with at most {smax} elements (up to translation): {total}; with no good signing: {len(fails)} {fails[:5]}', flush=True)
