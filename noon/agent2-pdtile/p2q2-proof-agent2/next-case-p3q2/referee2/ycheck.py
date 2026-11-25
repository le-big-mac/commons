"""Referee: are the DUAL basic solutions y(p, q) themselves free of poles on each piece?
verify3.py signs the reduced costs c_j - y.A_j (after cancellation) but never looks at the denominators of y.  If y had a pole at a
point of the piece where all reduced costs are regular, the duality argument would not be justified there (the rows of the
programme can lose rank at such a point).  This script recomputes x and y from every stored basis (own code, own sign test) and
requires every irreducible factor of every denominator of y_i (and of x_j, and of det B) to be strictly signed on the piece,
without using any branch assumption.
usage: ycheck.py PIECE"""
import sys, pickle, time, collections
import sympy as sp
from sympy import QQ
from sympy.polys.matrices import DomainMatrix
piece = sys.argv[1]; D = '/home/agent2/p3q2/referee2/orig/'
res = pickle.load(open(D + ('region_' if piece in ('C3', 'Cp') else 'split_') + piece + '.pkl', 'rb'))
p, q, r, s, z = sp.symbols('p q r s z')
BANDS = {'B1': (p, p**2 + 1, p**2 + p, 5), 'B2': (p, p**2 + p + 1, p**3 - p**2 + p - 1, 3), 'B3': (p, p**3 - p**2 + p, p**3 - 1, 3),
         'Ap1': (q, q + 1, q**2 - q + 1, 3), 'Ap2': (q, q**2 - q + 1, q**2 - 1, 3), 'A1a': (p, p + 2, 2 * p - sp.Rational(5, 2), 5),
         'A1b': (p, 2 * p - 1, p**2 - p + 1, 5), 'A2': (p, p**2 - p + 1, p**2 - 1, 3)}
def cleared(g):
    """g(p, q) on the piece as a polynomial in the parameters (all >= 0), after multiplication by a positive power of (1 + z)"""
    if piece == 'C3': return sp.Poly(sp.expand(g.subs(q, p**3 + 1 + s).subs(p, 3 + r)), r, s)
    if piece == 'Cp': return sp.Poly(sp.expand(g.subs(p, q**2 + 1 + s).subs(q, 2 + r)), r, s)
    fixed, lo, up, p0 = BANDS[piece]; other = q if fixed == p else p
    P_ = sp.Poly(g, other); d = P_.degree()                      # homogenise by hand: sum_k g_k(fixed) (lo + up z)^k (1 + z)^(d - k)
    ex = sum(P_.coeff_monomial(other**k) * (lo + up * z)**k * (1 + z)**(d - k) for k in range(d + 1))
    return sp.Poly(sp.expand(ex.subs(fixed, p0 + r)), r, z)
CACHE = {}
def strict_sign(g):
    if g not in CACHE:
        P_ = cleared(g); co = P_.coeffs(); corner = P_.eval({v: 0 for v in P_.gens})
        CACHE[g] = 1 if all(c >= 0 for c in co) and corner > 0 else -1 if all(c <= 0 for c in co) and corner < 0 else 0
    return CACHE[g]
cls = [(i, j) for i in range(4) for j in range(3)]; ords = [o for o in cls if o != (0, 0)]; ci = {c: k for k, c in enumerate(cls)}; n = 12
def lam_coeff(o, c):
    """coefficient of f_c in Lambda_o, from the Moebius form Lambda_{l m} = sum_{i >= l, j >= m} mu_{ij} p^(3-i) q^(2-j), mu = Moebius inverse of f"""
    (l, m), (i, j) = o, c; tot = 0
    for di, dj, sg in ((0, 0, 1), (1, 0, -1), (0, 1, -1), (1, 1, 1)):
        i2, j2 = i + di, j + dj
        if i2 <= 3 and j2 <= 2 and i2 >= l and j2 >= m: tot += sg * p**(3 - i2) * q**(2 - j2)
    return sp.expand(tot)
C = {(o, c): lam_coeff(o, c) for o in cls for c in cls}; tot = [C[((0, 0), c)] for c in cls]
KK = QQ.frac_field(p, q); toK = lambda v: KK.from_sympy(sp.sympify(v))
def leaves(rec, path=()):
    if rec['cat'] == 'split':
        yield from leaves(rec['pos'], path + ((rec['factor'], 1),)); yield from leaves(rec['neg'], path + ((rec['factor'], -1),))
    else: yield path, rec
badden = collections.Counter(); nleaf = 0; t0 = time.time(); examples = {}
for Z, rec in res.items():
    if rec['cat'] in ('L2', 'a'): continue
    rows = [[sp.Integer(1) if k == ci[(3, 2)] else sp.Integer(0) for k in range(n)]] + [[C[(o, c)] for c in cls] for o in ords if o not in Z]
    rhs = [sp.Integer(1)] + [sp.Integer(0)] * (len(rows) - 1); m = len(rows)
    for path, lf in leaves(rec):
        if 'basis' not in lf: continue
        nleaf += 1; basis = lf['basis']
        B = DomainMatrix([[toK(rows[i][basis[k]]) if basis[k] < n else (KK.one if i == basis[k] - n else KK.zero) for k in range(m)] for i in range(m)], (m, m), KK)
        y = B.transpose().lu_solve(DomainMatrix([[toK(tot[j]) if j < n else KK.zero] for j in basis], (m, 1), KK)).to_Matrix()
        xb = B.lu_solve(DomainMatrix([[toK(v)] for v in rhs], (m, 1), KK)).to_Matrix()
        for what, vec in (('y', y), ('x', xb)):
            for v in vec:
                den = sp.fraction(sp.cancel(v))[1]
                for f, mult in sp.factor_list(den)[1]:
                    if strict_sign(f) == 0:
                        badden[(what, str(f))] += 1; examples.setdefault((what, str(f)), (sorted(Z), path, lf['cat']))
print(f"piece {piece}: {nleaf} leaves; denominator factors of y or x that are NOT strictly signed on the piece: {len(badden)}   [{time.time() - t0:.0f} s]")
for (what, f), c in sorted(badden.items(), key=lambda kv: -kv[1]): print(f"   {what}: factor {f}  in {c} leaf-components; e.g. {examples[(what, f)]}")
