"""Where the plain signing fails (some Phi_d divides B), which single flips work?  Exhaustive small cases.   usage: sign_which.py"""
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
for n, smax in [(9, 8), (15, 7), (21, 6), (27, 6), (45, 5), (105, 4)]:
    RM = remainder_maps(n); c = collections.Counter(); ex = []
    for s in range(1, smax + 1):
        for comb in itertools.combinations_with_replacement(range(n), s):
            if comb[0] != 0: continue
            base = np.zeros(n, dtype=np.int64)
            for x in comb: base[x] += 1
            if all((R @ base).any() for R in RM.values()): continue
            pts = sorted(set(comb)); good = []
            for x in pts:
                v = base.copy(); v[x] -= 2
                if all((R @ v).any() for R in RM.values()): good.append(x)
            mx = max(base); mn = min(base[x] for x in pts)
            c['plain fails'] += 1
            c['every flip good'] += (len(good) == len(pts))
            c['some flip good'] += (len(good) > 0)
            c['every point of largest multiplicity good'] += all(x in good for x in pts if base[x] == mx)
            c['every point of least multiplicity good'] += all(x in good for x in pts if base[x] == mn)
            if len(good) < len(pts) and len(ex) < 4:
                badx = [x for x in pts if x not in good]
                why = {x: [d for d, R in RM.items() if not (R @ (base - 2 * np.eye(n, dtype=np.int64)[x])).any()] for x in badx}
                ex.append((comb, 'plain fails at', [d for d, R in RM.items() if not (R @ base).any()], 'bad flips and where', why))
    print(f'n = {n}, up to {smax}: {dict(c)}'); [print('    ', e) for e in ex]
