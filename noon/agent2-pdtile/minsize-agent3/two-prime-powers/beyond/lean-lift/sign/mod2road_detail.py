"""Detail for the mod 2 road: list the sets E (containing 0) for which neither G = empty nor any single point works,
with D2(E), the ranks r_d of span{X^x mod (2,Phi_d): x in E}, and which d defeat each single point.   usage: mod2road_detail.py n [limit]"""
import sys, itertools, collections
from sympy import Poly, cyclotomic_poly, symbols
X = symbols('X')
def rems(n):
    out = {}
    for d in range(1, n + 1):
        if n % d: continue
        phi = Poly(cyclotomic_poly(d, X), X, modulus=2); r = []
        for i in range(n):
            c = Poly(X**i, X, modulus=2).rem(phi).all_coeffs()[::-1]
            r.append(sum((int(cj) % 2) << j for j, cj in enumerate(c)))
        out[d] = r
    return out
def rank(vs):
    basis = []
    for v in vs:
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    return len(basis)
n = int(sys.argv[1]); limit = int(sys.argv[2]) if len(sys.argv) > 2 else 30
R = rems(n); divs = sorted(R); half = pow(2, -1, n); shown = 0; cnt = 0
def rem(mask, d):
    r = 0; Rd = R[d]; i = 0
    while mask:
        if mask & 1: r ^= Rd[i]
        mask >>= 1; i += 1
    return r
for E in range(1, 1 << n, 2):
    pts = [i for i in range(n) if E >> i & 1]
    D2 = [d for d in divs if rem(E, d) == 0]
    if not D2: continue
    M = 0
    for a, b in itertools.combinations(pts, 2): M ^= 1 << ((a + b) * half % n)
    md = {d: rem(M, d) for d in D2}
    zero_bad = [d for d in D2 if md[d] == 0]
    if not zero_bad: continue
    single_bad = {x: [d for d in D2 if R[d][x] == md[d]] for x in pts}
    if all(single_bad.values()):
        cnt += 1
        if shown < limit:
            shown += 1
            print(pts, 'D2', D2, 'ranks', {d: rank([R[d][x] for x in pts]) for d in D2}, 'empty fails at', zero_bad, 'single x fails at', single_bad)
print('count', cnt)
