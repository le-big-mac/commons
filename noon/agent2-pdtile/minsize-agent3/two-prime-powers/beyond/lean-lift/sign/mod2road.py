"""The 'mod 2 road' for SETS E in Z_n, n odd.
D2(E) = {d | n : E = 0 mod (2, Phi_d)};  M(E) = multiset of midpoints (x+y)/2, x<y in E, taken mod 2.
Question: is there a subset G of E with  G + M(E) != 0 mod (2, Phi_d)  for every d in D2(E)?
(If yes, the signing that turns exactly G is good, because S(zeta_d)/2 = -(G + M(E)) mod 2 for d in D2.)
Exhaustive over sets containing 0.   usage: mod2road.py n [n ...]"""
import sys, itertools, collections
from sympy import Poly, cyclotomic_poly, symbols, GF
X = symbols('X')
def rems(n):
    out = {}
    for d in range(1, n + 1):
        if n % d: continue
        phi = Poly(cyclotomic_poly(d, X), X, modulus=2)
        r = []
        for i in range(n):
            c = Poly(X**i, X, modulus=2).rem(phi).all_coeffs()[::-1]
            r.append(sum((int(cj) % 2) << j for j, cj in enumerate(c)))
        out[d] = r
    return out
def run(n):
    R = rems(n); divs = sorted(R); half = pow(2, -1, n)
    hist = collections.Counter(); fails = []
    def rem(mask, d):
        r = 0; Rd = R[d]; i = 0
        while mask:
            if mask & 1: r ^= Rd[i]
            mask >>= 1; i += 1
        return r
    for E in range(1, 1 << n, 2):            # contains 0
        pts = [i for i in range(n) if E >> i & 1]
        D2 = [d for d in divs if rem(E, d) == 0]
        if not D2: hist['D2 empty'] += 1; continue
        M = 0
        for a, b in itertools.combinations(pts, 2): M ^= 1 << ((a + b) * half % n)
        md = {d: rem(M, d) for d in D2}
        found = None
        for k in range(0, len(pts) + 1):
            for G in itertools.combinations(pts, k):
                if all(rem(sum(1 << g for g in G), d) != md[d] for d in D2): found = k; break
            if found is not None: break
        hist[f'least |G| = {found}'] += 1
        if found is None: fails.append(pts)
    print(f'n = {n}: {dict(sorted(hist.items()))}; sets where the mod 2 road fails: {len(fails)} {fails[:6]}', flush=True)
for a in sys.argv[1:]: run(int(a))
