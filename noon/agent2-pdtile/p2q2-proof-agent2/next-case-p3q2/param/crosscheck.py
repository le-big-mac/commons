"""Check the one-parameter certificates of family.py at particular values of t with an independent exact simplex
(exact_ref.simplex_min: the code used for the pair-by-pair classification; no basis is reused).
For each pattern and each test value t >= T: the certified formula v(t) equals the optimum; and the property claimed by the
category holds (b: D < k; R: the restricted programme has the same optimum; T: likewise with the extra equation; U: the
maximum of the class value on the optimal face is positive; N: D/k is not an integer; H: D = pq or p^2 q).
usage: crosscheck.py c side t1 [t2 ...]          (Noon = agent2, 21 November 2026)"""
import sys, pickle
from fractions import Fraction as Fr
import sympy as sp
from exact_ref import simplex_min
from steplp import ram
c, side = int(sys.argv[1]), sys.argv[2]; tests = [int(v) for v in sys.argv[3:]]
res = pickle.load(open(f"family_{c}_{side}.pkl", "rb")); T0 = max(r.get('T', 0) for r in res.values())
t = sp.symbols('t'); cls = [(i, j) for i in range(4) for j in range(3)]; ords = [o for o in cls if o != (0, 0)]; ci = {cl: k for k, cl in enumerate(cls)}
bad = 0; checked = 0
for tv in tests:
    assert tv >= T0, (tv, T0)
    p, q = (c, tv) if side == 'q' else (tv, c); M = p**3 * q**2
    C = {(o, cl): ram(p, 3, o[0], cl[0]) * ram(q, 2, o[1], cl[1]) for o in cls for cl in cls}
    tot = [C[((0, 0), cl)] for cl in cls]; e = lambda k0: [1 if k == k0 else 0 for k in range(12)]
    for Z, r in res.items():
        if r['cat'] in ('L2', 'a'): continue
        checked += 1
        rows = [e(ci[(3, 2)])] + [[C[(o, cl)] for cl in cls] for o in ords if o not in Z]; rhs = [1] + [0] * (len(rows) - 1)
        v = simplex_min(rows, rhs, tot)[1]
        vf = sp.sympify(r['v'], locals={'t': t}).subs(t, tv)
        ok = (sp.Rational(v.numerator, v.denominator) == vf)
        D = Fr(M) / v; k = p ** sum(1 for l in range(1, 4) if (l, 0) in Z) * q ** sum(1 for m in range(1, 3) if (0, m) in Z)
        face = (rows + [tot], rhs + [v])
        if r['cat'] == 'b': ok &= D < k
        elif r['cat'] == 'R':
            out = [tot[kk] if (cl[0] == 0 if r['kind'] == 'Rp' else cl[1] == 0) else 0 for kk, cl in enumerate(cls)]
            ok &= simplex_min(face[0], face[1], out)[1] == 0
        elif r['cat'] == 'T':
            ok &= (3, 2) not in Z and -simplex_min(face[0], face[1], [-x for x in e(ci[(2, 2)] if r['kind'] == 'TP' else ci[(3, 1)])])[1] == 1
        elif r['cat'] == 'U':
            ok &= (3, 2) in Z and -simplex_min(face[0], face[1], [-x for x in e(ci[(2, 2)] if r['kind'] == 'UP' else ci[(3, 1)])])[1] > 0
        elif r['cat'] == 'N': ok &= (D / k).denominator != 1
        elif r['cat'] == 'H':
            ok &= (3, 2) in Z and (D == p * q if r['kind'] == 'M0' else D == p * p * q)
            if r['kind'] == 'M2': ok &= {(1, 0), (3, 1), (2, 2)} <= Z
            if r['kind'] == 'M4': ok &= {(0, 1), (1, 2)} <= Z
        else: ok = False
        if not ok: bad += 1; print("   MISMATCH at t =", tv, sorted(Z), r['cat'], r.get('kind'))
print(f"family c = {c}, side {side}, T = {T0}: {checked} pattern checks at t in {tests}: mismatches {bad}")
