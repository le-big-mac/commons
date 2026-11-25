"""Check certificates with case distinctions (split.py) at particular prime pairs with the independent exact simplex:
walk down the tree by the sign of each factor at the pair, then compare the leaf's formula and category as crosscheck2.py does.
usage: crosscheck3.py BAND p,q [p,q ...]         (Noon = agent2, 21 November 2026)"""
import sys, pickle
from fractions import Fraction as Fr
import sympy as sp
from exact_ref import simplex_min
from steplp import ram
band = sys.argv[1]; pts = [tuple(int(v) for v in a.split(',')) for a in sys.argv[2:]]
res = pickle.load(open(f"split_{band}.pkl", "rb")); P, Q = sp.symbols('p q')
# every band is half-open at the top: the parametrisation other = (lo + up z)/(1 + z), z >= 0, reaches lo and never reaches up
inside = {'B1': lambda p, q: p >= 5 and p*p + 1 <= q < p*p + p, 'B2': lambda p, q: p >= 3 and p*p + p + 1 <= q < p**3 - p*p + p - 1, 'B3': lambda p, q: p >= 3 and p**3 - p*p + p <= q < p**3 - 1,
          'Ap1': lambda p, q: q >= 3 and q + 1 <= p < q*q - q + 1, 'Ap2': lambda p, q: q >= 3 and q*q - q + 1 <= p < q*q - 1,
          'A1a': lambda p, q: p >= 5 and p + 2 <= q and 2 * q < 4 * p - 5, 'A1b': lambda p, q: p >= 5 and 2*p - 1 <= q < p*p - p + 1, 'A2': lambda p, q: p >= 3 and p*p - p + 1 <= q < p*p - 1}[band]
cls = [(i, j) for i in range(4) for j in range(3)]; ords = [o for o in cls if o != (0, 0)]; ci = {cl: k for k, cl in enumerate(cls)}
bad = checked = skipped = 0
for (p, q) in pts:
    assert inside(p, q), (band, p, q)
    M = p**3 * q**2; C = {(o, cl): ram(p, 3, o[0], cl[0]) * ram(q, 2, o[1], cl[1]) for o in cls for cl in cls}
    tot = [C[((0, 0), cl)] for cl in cls]; e = lambda k0: [1 if k == k0 else 0 for k in range(12)]
    for Z, r in res.items():
        if r['cat'] in ('L2', 'a'): continue
        while r['cat'] == 'split':
            val = sp.sympify(r['factor'], locals={'p': P, 'q': Q}).subs({P: p, Q: q}); r = r['pos'] if val >= 0 else r['neg']
        if r['cat'] in ('?', 'empty?'): skipped += 1; continue
        checked += 1
        if r['cat'] == 'empty': bad += 1; print("   A PAIR IN A BRANCH CLAIMED EMPTY:", (p, q), sorted(Z)); continue
        rows = [e(ci[(3, 2)])] + [[C[(o, cl)] for cl in cls] for o in ords if o not in Z]; rhs = [1] + [0] * (len(rows) - 1)
        v = simplex_min(rows, rhs, tot)[1]
        ok = sp.Rational(v.numerator, v.denominator) == sp.sympify(r['v'], locals={'p': P, 'q': Q}).subs({P: p, Q: q})
        D = Fr(M) / v; k = p ** sum(1 for l in range(1, 4) if (l, 0) in Z) * q ** sum(1 for m in range(1, 3) if (0, m) in Z)
        face = (rows + [tot], rhs + [v])
        if r['cat'] == 'b': ok &= D < k
        elif r['cat'] == 'R':
            out = [tot[kk] if (cl[0] == 0 if r['kind'] == 'Rp' else cl[1] == 0) else 0 for kk, cl in enumerate(cls)]
            ok &= simplex_min(face[0], face[1], out)[1] == 0
        elif r['cat'] == 'T': ok &= (3, 2) not in Z and -simplex_min(face[0], face[1], [-x for x in e(ci[(2, 2)] if r['kind'] == 'TP' else ci[(3, 1)])])[1] == 1
        elif r['cat'] == 'U': ok &= (3, 2) in Z and -simplex_min(face[0], face[1], [-x for x in e(ci[(2, 2)] if r['kind'] == 'UP' else ci[(3, 1)])])[1] > 0
        elif r['cat'] == 'N': ok &= (D / k).denominator != 1
        elif r['cat'] == 'H':
            ok &= (3, 2) in Z and (D == p * q if r['kind'] == 'M0' else D == p * p * q)
            if r['kind'] == 'M2': ok &= {(1, 0), (3, 1), (2, 2)} <= Z
            if r['kind'] == 'M4': ok &= {(0, 1), (1, 2)} <= Z
        else: ok = False
        if not ok: bad += 1; print("   MISMATCH at", (p, q), sorted(Z), r['cat'], r.get('kind'))
print(f"band {band}: {checked} pattern checks at {pts}: mismatches {bad}; without a certificate at that pair {skipped}")
