"""Z_{p^3 q^2} with one prime fixed (c) and the other a variable t: a certificate for every zero pattern, valid for all t >= T.
usage: family.py c side [sample]      side = q: (p, q) = (c, t), M = c^3 t^2;   side = p: (p, q) = (t, c), M = t^3 c^2
Categories, tested in this order (L2 and a need nothing):
  b : D^w(t) < k(t) for t >= T
  R : an optimal point vanishing outside pZ (Rp) or outside qZ (Rq)
  T : M not a zero, an optimal point equal to 1 on P (TP) or on Q (TQ)
  U : M a zero, an optimal point positive on P\\0 (UP) or on Q\\0 (UQ)
  H : D^w(t) = pq or p^2 q identically, M a zero, and Lemma M applies (M0, M2, M4)
  N : D^w(t)/k(t) is not an integer for any integer t >= T
  ? : none of these (reported)
For every pattern the optimal value is certified by a basis whose primal and dual basic solutions, as rational functions of
t, are feasible for all t >= T (sign of every component decided by exact isolation of real roots).
(Noon = agent2, 21 November 2026)"""
import sys, pickle, time, math
from collections import Counter
from plp import *

def analyse(F, Z, tv):
    n = len(F.cls); ci = {c: k for k, c in enumerate(F.cls)}; top_in = F.top in Z
    tot = F.tot(); R, rhs = F.rows(Z)
    numr = lambda rows: [[F.num(v, tv) for v in row] for row in rows]
    numv = lambda vec: [F.num(v, tv) for v in vec]
    out = {'T': 0}
    def bump(T): out['T'] = max(out['T'], T)
    def need_nonneg(e, what):
        """e in K must be >= 0 for all large t: returns False if its sign at infinity is negative"""
        if e == K.zero: return True
        sgn, T = last_change(e)
        if sgn < 0: return False
        bump(T); return True
    # ---- 1. the optimal value, with a basis valid for all large t ----
    st, val, x, basis, y = simplex_full(numr(R), numv(rhs), numv(tot)); assert st == 'optimal'
    xs, ys = basic_solution(R, rhs, tot, basis, n)
    if any(xs[j] != K.zero for j in xs if j >= n): return dict(cat='?', why='artificial variable not identically zero')
    if not all(need_nonneg(xs[j], 'primal') for j in xs if j < n): return dict(cat='retry', why='primal sign')
    red = [to_K(tot[j]) - sum(ys[i] * to_K(R[i][j]) for i in range(len(R))) for j in range(n)]
    if not all(need_nonneg(e, 'dual') for e in red): return dict(cat='retry', why='dual sign')
    v = sum(to_K(tot[j]) * xs[j] for j in xs if j < n)
    assert K.to_sympy(v).subs(t, tv) == sp.Rational(val.numerator, val.denominator)
    D = to_K(F.M) / v; k = to_K(F.k(Z)); out.update(basis=basis, v=str(K.to_sympy(v)), D=str(sp.factor(K.to_sympy(D))), k=str(F.k(Z)))
    # ---- 2. b ----
    if D != k:
        sgn, T = last_change(k - D)
        if sgn > 0: bump(T); out['cat'] = 'b'; return out
    # ---- restricted programmes: a feasible point with the same value and a further property ----
    def restricted(forbid=(), extra=(), objective=None, positive=None):
        Rr, rr = F.rows(Z, extra); cost = tot if objective is None else objective
        st, val2, x2, basis2, y2 = simplex_full(numr(Rr), numv(rr), numv(cost), forbid=forbid)
        if st != 'optimal': return None
        if objective is None and val2 != val: return None
        if positive is not None and x2[positive] <= 0: return None
        xs2, _ = basic_solution(Rr, rr, cost, basis2, n)
        if any(xs2[j] != K.zero for j in xs2 if j >= n): return None
        if any(j in forbid for j in xs2 if j < n and xs2[j] != K.zero): return None
        Ts = [0]
        for j in xs2:
            if j < n and xs2[j] != K.zero:
                sgn, T = last_change(xs2[j])
                if sgn < 0: return None
                Ts.append(T)
        if sum(to_K(tot[j]) * xs2[j] for j in xs2 if j < n) != v: return None
        if positive is not None:
            e = xs2.get(positive, K.zero)
            if e == K.zero: return None
            sgn, T = last_change(e)
            if sgn < 0: return None
            Ts.append(T)
        return max(Ts), basis2
    Pcls, Qcls = ci[(2, 2)], ci[(3, 1)]
    for name, forbid in (('Rp', [ci[c] for c in F.cls if c[0] == 0]), ('Rq', [ci[c] for c in F.cls if c[1] == 0])):
        r = restricted(forbid=forbid)
        if r: bump(r[0]); out.update(cat='R', kind=name, basis2=r[1]); return out
    e = lambda k0: [sp.Integer(1) if kk == k0 else sp.Integer(0) for kk in range(n)]
    if not top_in:
        for name, cl in (('TP', Pcls), ('TQ', Qcls)):
            r = restricted(extra=[(e(cl), sp.Integer(1))])
            if r: bump(r[0]); out.update(cat='T', kind=name, basis2=r[1]); return out
    else:
        for name, cl in (('UP', Pcls), ('UQ', Qcls)):
            r = restricted(extra=[(tot, K.to_sympy(v))], objective=[-vv for vv in e(cl)], positive=cl)
            if r: bump(r[0]); out.update(cat='U', kind=name, basis2=r[1]); return out
    # ---- H or N ----
    p, q = to_K(F.p), to_K(F.q)
    if top_in and D == p * q: out.update(cat='H', kind='M0'); return out
    if top_in and D == p * p * q:
        if {(1, 0), (3, 1), (2, 2)} <= Z: out.update(cat='H', kind='M2'); return out
        if {(0, 1), (1, 2)} <= Z: out.update(cat='H', kind='M4'); return out
    r = D / k; num, den = sp.fraction(sp.cancel(K.to_sympy(r))); pn, pd = Poly(num, t, domain='QQ'), Poly(den, t, domain='QQ')
    quo, rem = sp.div(pn, pd)
    cden = int(sp.ilcm(1, 1, *[sp.Rational(cf).q for cf in quo.all_coeffs()])) if not quo.is_zero else 1
    if not rem.is_zero:                                   # r = quo + rem/den with rem/den -> 0: c r(t) is an integer plus a nonzero number of size < 1
        g = to_K(cden * rem.as_expr() / pd.as_expr())
        for expr in (g, K.one - g, K.one + g):
            sgn, T = last_change(expr)
            if expr is not g and sgn < 0: return dict(cat='?', why='remainder bound')
            bump(T)
        out.update(cat='N', kind='remainder', r=str(sp.factor(K.to_sympy(r)))); return out
    cq = Poly(cden * quo.as_expr(), t)                    # integer coefficients; r(t) integer iff cden | cq(t)
    bad = [u for u in range(cden) if math.gcd(u, cden) == 1 and cq.eval(u) % cden == 0]
    if not bad: bump(cden + 1); out.update(cat='N', kind='congruence', r=str(quo.as_expr())); return out
    out.update(cat='?', why=f'D/k = {quo.as_expr()} is an integer for t = {bad} mod {cden}', r=str(quo.as_expr())); return out

def run_family(c, side, samples=(211, 2003, 20011)):
    F = Family(c, side); res = {}; cnt = Counter(); t0 = time.time()
    for mask in range(1 << len(F.ords)):
        Z = frozenset(o for i, o in enumerate(F.ords) if mask >> i & 1)
        if (1, 0) not in Z and (0, 1) not in Z: res[Z] = dict(cat='L2', T=0); cnt['L2'] += 1; continue
        t2 = all((l, m) in Z for l in range(1, 4) for m in range(1, 3) if (l, 0) in Z and (0, m) in Z)
        orph = any((l, 0) not in Z and (0, m) not in Z for (l, m) in Z if l and m)
        if t2 and not orph: res[Z] = dict(cat='a', T=0); cnt['a'] += 1; continue
        for tv in samples:
            r = analyse(F, Z, tv)
            if r['cat'] != 'retry': break
        r['sample'] = tv; r['t2'] = t2; res[Z] = r; cnt[r['cat'] + ('' if r['cat'] not in ('H',) else ':' + r['kind'])] += 1
    return F, res, cnt, time.time() - t0

if __name__ == '__main__':
    c, side = int(sys.argv[1]), sys.argv[2]
    F, res, cnt, dt = run_family(c, side)
    T = max(r.get('T', 0) for r in res.values())
    name = f"(p, q) = ({c}, t), M = {c**3} t^2" if side == 'q' else f"(p, q) = (t, {c}), M = {c**2} t^3"
    print(f"{name}:  " + ", ".join(f"{k} {v}" for k, v in sorted(cnt.items())) + f";  certificates valid for all t >= {T};  T, U, H patterns with (T2): "
          f"{sum(1 for r in res.values() if r['cat'] in ('T', 'U', 'H') and r['t2'])}   [{dt:.0f} s]")
    for Z, r in res.items():
        if r['cat'] in ('?', 'retry'): print("   UNSETTLED:", sorted(Z), r)
    worst = sorted(((r.get('T', 0), r['cat'], sorted(Z)) for Z, r in res.items()), reverse=True)[:3]
    print("   largest thresholds:", [(T_, c_) for T_, c_, _ in worst])
    pickle.dump(res, open(f"family_{c}_{side}.pkl", "wb"))
