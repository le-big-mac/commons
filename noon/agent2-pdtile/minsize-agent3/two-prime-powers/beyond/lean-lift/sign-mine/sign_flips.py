"""How many signs must be flipped?  For odd n and a multiset B on Z_n: the least number of elements whose sign is turned so that the
signed mask is divisible by no Phi_d, d | n.  Exhaustive up to a size, up to translation.   usage: sign_flips.py"""
import itertools, collections
import numpy as np
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X')
def remainder_maps(n):
    out = {}
    for d in range(1, n + 1):
        if n % d: continue
        phi = Poly(cyclotomic_poly(d, X), X, domain=ZZ); deg = phi.degree(); R = np.zeros((deg, n), dtype=np.int64)
        for i in range(n):
            for j, cj in enumerate(Poly(X**i, X, domain=ZZ).rem(phi).all_coeffs()[::-1]): R[j, i] = int(cj)
        out[d] = R
    return out
for n, smax in [(3, 8), (5, 7), (9, 7), (15, 6), (21, 5), (27, 5), (45, 4)]:
    RM = list(remainder_maps(n).values()); hist = collections.Counter(); worst = None
    for s in range(1, smax + 1):
        for comb in itertools.combinations_with_replacement(range(n), s):
            if comb[0] != 0: continue
            base = np.zeros(n, dtype=np.int64)
            for x in comb: base[x] += 1
            need = None
            for k in range(0, s // 2 + 1):
                for flip in itertools.combinations(range(s), k):
                    v = base.copy()
                    for i in flip: v[comb[i]] -= 2
                    if all((R @ v).any() for R in RM): need = k; break
                if need is not None: break
            hist[need] += 1
            if need is not None and need >= 2 and worst is None: worst = comb
    print(f'n = {n}, up to {smax} elements: least number of flips needed -> number of multisets: {dict(sorted(hist.items(), key=lambda t: (t[0] is None, t[0])))}; a multiset needing two or more: {worst}', flush=True)
