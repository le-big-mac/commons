"""Referee: the family (p, q) = (2, t).  From every stored basis recompute x(t), y(t) over QQ(t) with own rows (Moebius form) and require
(1) no denominator of x_j or y_i has a real root in [T0, oo), T0 = 9 (Sturm);  (2) x_j >= 0 and the reduced costs >= 0 on [T0, oo), by an
own test: no root of the numerator or denominator in [T0, oo) and a positive value at T0 (or identically zero);
(3) N: D/k is not an integer at any prime t >= 11 -- re-derived, and brute force over all primes 11 <= t < 200000."""
import sys, pickle, time, collections
import sympy as sp
from sympy import QQ, primerange
from sympy.polys.matrices import DomainMatrix
T0 = 9; D = '/home/agent2/p3q2/referee2/orig/'; res = pickle.load(open(D + 'family_2_q.pkl', 'rb'))
t = sp.symbols('t'); p, q = sp.Integer(2), t
cls = [(i, j) for i in range(4) for j in range(3)]; ords = [o for o in cls if o != (0, 0)]; ci = {c: k for k, c in enumerate(cls)}; n = 12
def lam_coeff(o, c):
    (l, m), (i, j) = o, c; tot = 0
    for di, dj, sg in ((0, 0, 1), (1, 0, -1), (0, 1, -1), (1, 1, 1)):
        i2, j2 = i + di, j + dj
        if i2 <= 3 and j2 <= 2 and i2 >= l and j2 >= m: tot += sg * p**(3 - i2) * q**(2 - j2)
    return sp.expand(tot)
C = {(o, c): lam_coeff(o, c) for o in cls for c in cls}; tot = [C[((0, 0), c)] for c in cls]
KK = QQ.frac_field(t); toK = lambda v: KK.from_sympy(sp.sympify(v))
def noroot(pol): return pol.degree() < 1 or pol.count_roots(T0, sp.oo) == 0
def nonneg_from_T0(expr):
    expr = sp.cancel(expr)
    if expr == 0: return True
    num, den = sp.fraction(expr); pn, pd = sp.Poly(num, t), sp.Poly(den, t)
    return noroot(pn) and noroot(pd) and pn.eval(T0) * pd.eval(T0) > 0
badpole = 0; badsign = 0; nN = 0; hits = 0; nleaf = 0; t0 = time.time(); primes = list(primerange(11, 200000)); maxT = 0
for Z, rec in res.items():
    if rec['cat'] in ('L2', 'a'): continue
    nleaf += 1; maxT = max(maxT, rec.get('T', 0))
    rows = [[sp.Integer(1) if k == ci[(3, 2)] else sp.Integer(0) for k in range(n)]] + [[C[(o, c)] for c in cls] for o in ords if o not in Z]
    rhs = [sp.Integer(1)] + [sp.Integer(0)] * (len(rows) - 1); m = len(rows); basis = rec['basis']
    B = DomainMatrix([[toK(rows[i][basis[k]]) if basis[k] < n else (KK.one if i == basis[k] - n else KK.zero) for k in range(m)] for i in range(m)], (m, m), KK)
    y = [sp.cancel(v) for v in B.transpose().lu_solve(DomainMatrix([[toK(tot[j]) if j < n else KK.zero] for j in basis], (m, 1), KK)).to_Matrix()]
    xb = [sp.cancel(v) for v in B.lu_solve(DomainMatrix([[toK(v)] for v in rhs], (m, 1), KK)).to_Matrix()]
    for v in y + xb:
        if not noroot(sp.Poly(sp.fraction(v)[1], t)): badpole += 1
    x = [sp.Integer(0)] * n
    for kk, j in enumerate(basis):
        if j < n: x[j] = xb[kk]
        elif xb[kk] != 0: badsign += 1
    red = [sp.cancel(tot[j] - sum(y[i] * rows[i][j] for i in range(m))) for j in range(n)]
    if not all(nonneg_from_T0(v) for v in x + red): badsign += 1
    if rec['cat'] == 'N':
        nN += 1; v = sp.cancel(sum(tot[j] * x[j] for j in range(n))); k = p ** sum(1 for l in range(1, 4) if (l, 0) in Z) * q ** sum(1 for mm in range(1, 3) if (0, mm) in Z)
        num, den = sp.fraction(sp.cancel(p**3 * q**2 / (v * k))); fn = sp.lambdify(t, num, modules='math'); fd = sp.lambdify(t, den, modules='math')
        for tv in primes:
            d_ = fd(tv)
            if d_ != 0 and fn(tv) % d_ == 0: hits += 1; print("   INTEGER D/k at t =", tv, sorted(Z))
        print("   N:", sorted(Z), "D/k =", sp.factor(num / den))
print(f"family (2, t): {nleaf} certificates; largest stored threshold {maxT}; components of x or y with a pole in [{T0}, oo): {badpole}; certificates with a sign failure on [{T0}, oo): {badsign}; "
      f"N: {nN} patterns, integer values of D/k at the {len(primes)} primes 11 <= t < 200000: {hits}   [{time.time() - t0:.0f} s]")
