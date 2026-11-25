"""Emptiness of a branch, and signs implied by a branch.  (Noon = agent2, 21 November 2026)
A branch of a band is given by assumptions  s_i F_i >= 0.  It contains no point if some combination
    T = sum_i m_i s_i F_i     with multipliers m_i = polynomials in p, q with coefficients >= 0  (so m_i >= 0 on the band)
is negative at every point of the band.  The multipliers are found by a linear programme in floating point, rounded to
rationals, and the conclusion is then checked exactly: after the band's substitution and multiplication by one common power of
(1 + z), all coefficients of T are <= 0 and its value at the corner is < 0."""
import numpy as np, sympy as sp
from scipy.optimize import linprog
P, Q = sp.symbols('p q'); r_, z_ = sp.symbols('r z', nonnegative=True)
MONO = [sp.Integer(1), P, Q, P * Q, P**2, Q**2]
def cleared(expr, fixed, lo, up, p0, deg):
    """expr(p, q) on the band, times (1 + z)^deg: a polynomial in r, z"""
    other = Q if fixed == P else P
    return sp.expand(sp.cancel(expr.subs(other, (lo + up * z_) / (1 + z_)) * (1 + z_) ** deg).subs(fixed, p0 + r_))
def refute(assume, fixed, lo, up, p0):
    """Returns a list of (multiplier, F, sign) proving that no point of the band satisfies all assumptions, or None."""
    other = Q if fixed == P else P
    terms = [(m, F, sg) for (F, sg) in assume for m in MONO]
    deg = max(sp.Poly(m * F, P, Q).degree(other) for m, F, sg in terms)
    def proves(lam):
        T = sum(l * m * sg * F for l, (m, F, sg) in zip(lam, terms))
        if T == 0: return False
        e = sp.Poly(cleared(T, fixed, lo, up, p0, deg), r_, z_)
        return all(c <= 0 for c in e.coeffs()) and e.coeff_monomial((0, 0)) < 0
    out = lambda lam: [(str(l * m), str(F), sg) for l, (m, F, sg) in zip(lam, terms) if l != 0]
    # 1. the plain sum of the assumed quantities
    lam = [sp.Integer(1) if m == 1 else sp.Integer(0) for m, F, sg in terms]
    if proves(lam): return out(lam)
    # 1b. small multipliers on one or two of the assumptions: a m1 X1 + b m2 X2 with m in MONO and a, b in {1, 2, 3}
    import itertools
    idx = {(i, k): i * len(MONO) + k for i in range(len(assume)) for k in range(len(MONO))}
    for i in range(len(assume)):
        for k in range(len(MONO)):
            lam = [sp.Integer(0)] * len(terms); lam[idx[(i, k)]] = sp.Integer(1)
            if proves(lam): return out(lam)
    for i, j in itertools.combinations(range(len(assume)), 2):
        for k1, k2 in itertools.product(range(len(MONO)), repeat=2):
            for a_, b_ in ((1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)):
                lam = [sp.Integer(0)] * len(terms); lam[idx[(i, k1)]] = sp.Integer(a_); lam[idx[(j, k2)]] = sp.Integer(b_)
                if proves(lam): return out(lam)
    # 2. a linear programme: all coefficients <= -t (where the row is not empty), corner <= -1, t as large as possible; then the smallest sum
    exps = [sp.Poly(cleared(m * sg * F, fixed, lo, up, p0, deg), r_, z_) for m, F, sg in terms]
    monos = sorted({mon for e in exps for mon in e.monoms()})
    if (0, 0) not in monos: return None
    A = np.array([[float(e.coeff_monomial(mon)) for e in exps] for mon in monos]); n = len(terms)
    scale = np.abs(A).max(axis=0); scale[scale == 0] = 1.0; As = A / scale
    b = np.array([-1.0 if mon == (0, 0) else 0.0 for mon in monos])
    cands = []
    res = linprog(np.r_[np.zeros(n), -1.0], A_ub=np.c_[As, np.ones(len(monos))], b_ub=b, A_eq=np.r_[np.ones(n), 0.0].reshape(1, -1) * 0 + np.r_[np.ones(n), 0.0].reshape(1, -1),
                  b_eq=[float(n)], bounds=[(0, None)] * n + [(0, 1e6)], method='highs')
    if res.status == 0: cands.append(res.x[:n] / scale)
    res = linprog(np.ones(n), A_ub=As, b_ub=b, bounds=[(0, None)] * n, method='highs')
    if res.status == 0: cands.append(res.x / scale)
    for lam0 in cands:
        if lam0.max() <= 0: continue
        lam0 = lam0 / lam0.max()
        for den in (1, 2, 4, 12, 60, 1000, 10**6, 10**9, 10**12):
            lam = [sp.Rational(int(round(v * den)), den) for v in lam0]
            if any(lam) and proves(lam): return out(lam)
    return None
