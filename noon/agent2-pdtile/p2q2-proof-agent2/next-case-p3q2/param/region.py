"""Z_{p^3 q^2} with BOTH primes symbolic: certificates for every zero pattern on a region of the (p, q) plane.
usage: region.py NAME            NAME in: C (q >= p^3 + 1), C3 (the same with p >= 3), Cp (p >= q^2 + 1), A (p + 1 <= q <= p^2 - 1), B (p^2 + 1 <= q <= p^3 - 1),
                                           Ap (q + 1 <= p <= q^2 - 1)
A sign is certified on a region by substituting a parametrisation with parameters >= 0 and finding all coefficients of one
sign with a nonzero constant term (so the sign holds at every real point of the region, not only at primes).
Categories and their order as in family.py.  (Noon = agent2, 21 November 2026)"""
import sys, pickle, time, math
from collections import Counter
from fractions import Fraction as Fr
import sympy as sp
from sympy import QQ
from sympy.polys.matrices import DomainMatrix
from plp import simplex_full, ram_sym
P, Q = sp.symbols('p q'); r_, s_, z_ = sp.symbols('r s z', nonnegative=True)
K2 = QQ.frac_field(P, Q); toK = lambda e: K2.from_sympy(sp.sympify(e))
cls = [(i, j) for i in range(4) for j in range(3)]; ords = [o for o in cls if o != (0, 0)]; ci = {c: k for k, c in enumerate(cls)}; n = 12; top = (3, 2)
C = {(o, c): sp.expand(ram_sym(P, 3, o[0], c[0]) * ram_sym(Q, 2, o[1], c[1])) for o in cls for c in cls}
tot = [C[((0, 0), c)] for c in cls]; Msym = P**3 * Q**2
e_ = lambda k0: [sp.Integer(1) if kk == k0 else sp.Integer(0) for kk in range(n)]

REGIONS = {
 # name: (substitution for sign tests, sample points for finding bases)
 'C':  (lambda g: g.subs({Q: P**3 + 1 + s_}).subs({P: 2 + r_}), [(13, 2203), (11, 1361), (7, 347), (5, 127), (3, 29), (2, 11), (13, 20011)]),
 'C3': (lambda g: g.subs({Q: P**3 + 1 + s_}).subs({P: 3 + r_}), [(13, 2203), (11, 1361), (7, 347), (5, 127), (3, 29), (13, 20011), (3, 1009)]),
 'Cp': (lambda g: g.subs({P: Q**2 + 1 + s_}).subs({Q: 2 + r_}), [(173, 13), (127, 11), (53, 7), (29, 5), (11, 3), (5, 2), (20011, 13)]),
 'A':  (lambda g: sp.numer(sp.together(g.subs({Q: ((P + 1) + (P**2 - 1) * z_) / (1 + z_)}))).subs({P: 2 + r_}), [(101, 103), (101, 1009), (101, 5003), (101, 9973), (11, 13), (11, 113), (5, 7), (5, 23), (3, 5), (3, 7), (2, 3), (1009, 1013)]),
 'B':  (lambda g: sp.numer(sp.together(g.subs({Q: ((P**2 + 1) + (P**3 - 1) * z_) / (1 + z_)}))).subs({P: 2 + r_}), [(11, 127), (11, 701), (11, 1327), (101, 10211), (101, 500009), (101, 1030297), (3, 11), (3, 23), (2, 5), (2, 7), (5, 29), (5, 113)]),
 'Ap': (lambda g: sp.numer(sp.together(g.subs({P: ((Q + 1) + (Q**2 - 1) * z_) / (1 + z_)}))).subs({Q: 2 + r_}), [(103, 101), (1009, 101), (5003, 101), (9973, 101), (13, 11), (113, 11), (7, 5), (23, 5), (5, 3), (7, 3), (3, 2), (1013, 1009)]),
}
def band(fixed, lo, up, p0, samples):
    """the band lo(fixed) <= other <= up(fixed), fixed >= p0: other = (lo + up z)/(1 + z), fixed = p0 + r, with r, z >= 0"""
    other = Q if fixed == P else P
    return (lambda g: sp.numer(sp.together(g.subs({other: (lo + up * z_) / (1 + z_)}))).subs({fixed: p0 + r_}), samples)
def pts(fixed, lo, up, p0s):
    """sample points of a band: for a few values of the fixed prime, primes near the lower end, the middle and the upper end"""
    out = []
    for pv in p0s:
        L, U = int(lo.subs(fixed, pv)), int(up.subs(fixed, pv))
        if L > U: continue
        for x in sorted({L, (2 * L + U) // 3, (L + U) // 2, (L + 2 * U) // 3, U}):
            c = int(sp.nextprime(x - 1)) if sp.nextprime(x - 1) <= U else int(sp.prevprime(U + 1)) if U >= 2 and sp.prevprime(U + 1) >= L else None
            if c is None or c == pv: continue
            out.append((pv, c) if fixed == P else (c, pv))
    return list(dict.fromkeys(out))
PS = [101, 31, 11, 7, 5, 3]
REGIONS.update({   # inner bands, all from 3 on: the inner pairs with p = 2 (or q = 2) are (2,3), (2,5), (2,7), (3,2), settled directly
 'B1':  band(P, P**2 + 1, P**2 + P, 5, pts(P, P**2 + 1, P**2 + P, PS[:-1])),          # from p = 5: the pairs (3, q) are settled directly
 'B2':  band(P, P**2 + P + 1, P**3 - P**2 + P - 1, 3, pts(P, P**2 + P + 1, P**3 - P**2 + P - 1, PS)),
 'B3':  band(P, P**3 - P**2 + P, P**3 - 1, 3, pts(P, P**3 - P**2 + P, P**3 - 1, PS)),
 'Ap1': band(Q, Q + 1, Q**2 - Q + 1, 3, pts(Q, Q + 1, Q**2 - Q + 1, PS)),
 'Ap2': band(Q, Q**2 - Q + 1, Q**2 - 1, 3, pts(Q, Q**2 - Q + 1, Q**2 - 1, PS)),
 'A1a': band(P, P + 2, 2 * P - sp.Rational(5, 2), 5, pts(P, P + 2, 2 * P - 3, [101, 53, 31, 23, 17, 13, 11, 7, 5])),   # p >= 5; p + 2 <= q < 2p - 5/2, so q = 2p - 3 is inside (p + 1 and 2p - 2 are even)
 'A1b': band(P, 2 * P - 1, P**2 - P + 1, 5, pts(P, 2 * P - 1, P**2 - P + 1, PS[:-1])),
 'A2':  band(P, P**2 - P + 1, P**2 - 1, 3, pts(P, P**2 - P + 1, P**2 - 1, PS)),
})
SIGN_CACHE = {}
def sign_factor(g, region):
    key = (region, g)
    if key in SIGN_CACHE: return SIGN_CACHE[key]
    sub = REGIONS[region][0]; e = sp.expand(sub(g))
    if e == 0: res = '0'
    else:
        gens = [v for v in (r_, s_, z_) if e.has(v)]
        if not gens: res = '+' if e > 0 else '-'
        else:
            co = sp.Poly(e, *gens).coeffs(); const = e.subs({v: 0 for v in gens})
            if all(c > 0 for c in co) and const > 0: res = '+'
            elif all(c < 0 for c in co) and const < 0: res = '-'
            elif all(c >= 0 for c in co) and const > 0: res = '+'
            elif all(c <= 0 for c in co) and const < 0: res = '-'
            elif all(c >= 0 for c in co): res = '+0'
            elif all(c <= 0 for c in co): res = '-0'
            else: res = '?'
    SIGN_CACHE[key] = res; return res
def sign(expr_K, region):
    """sign of an element of QQ(p, q) on the region: '+', '-', '0', '+0', '-0' or '?' (with the factor that failed)"""
    if expr_K == K2.zero: return '0', None
    num, den = sp.fraction(sp.cancel(K2.to_sympy(expr_K))); sg = 1; strict = True
    for part in (num, den):
        cst, facs = sp.factor_list(part)
        if cst < 0: sg = -sg
        for f, mult in facs:
            rr = sign_factor(f, region)
            if rr == '?': return '?', f
            if rr == '0': return '?', f
            if part is den and rr.endswith('0'): return '?', f     # a weakly signed factor may not sit in a denominator (second referee, point a3)
            if rr.startswith('-') and mult % 2 == 1: sg = -sg
            if rr.endswith('0'): strict = False
    return (('+' if sg > 0 else '-') + ('' if strict else '0')), None

def rows_for(Z, extra=()):
    R = [e_(ci[top])] + [[C[(o, c)] for c in cls] for o in ords if o not in Z]; rhs = [sp.Integer(1)] + [sp.Integer(0)] * (len(R) - 1)
    for rr, vv in extra: R.append(list(rr)); rhs.append(vv)
    return R, rhs
def numeric(M_, pv, qv): return [[Fr(int(sp.Integer(v).subs({P: pv, Q: qv}) if not isinstance(v, sp.Expr) else int(v.subs({P: pv, Q: qv})))) for v in row] for row in M_]
def numvec(v_, pv, qv): return [Fr(sp.Rational(sp.sympify(v).subs({P: pv, Q: qv})).p, sp.Rational(sp.sympify(v).subs({P: pv, Q: qv})).q) for v in v_]
def basic_solution(R, rhs, cost, basis):
    m = len(R)
    B = DomainMatrix([[toK(R[i][basis[k]]) if basis[k] < n else (K2.one if i == basis[k] - n else K2.zero) for k in range(m)] for i in range(m)], (m, m), K2)
    xb = B.lu_solve(DomainMatrix([[toK(v)] for v in rhs], (m, 1), K2)).to_Matrix()
    y = B.transpose().lu_solve(DomainMatrix([[toK(cost[j]) if j < n else K2.zero] for j in basis], (m, 1), K2)).to_Matrix()
    return {j: toK(xb[k]) for k, j in enumerate(basis)}, [toK(v) for v in y]

def analyse(Z, region):
    samples = REGIONS[region][1]; top_in = top in Z; R, rhs = rows_for(Z); out = {}; tried = set(); fails = []
    # ---- 1. a basis valid on the whole region ----
    found = None
    for (pv, qv) in samples:
        st, val, x, basis, y = simplex_full(numeric(R, pv, qv), numvec(rhs, pv, qv), numvec(tot, pv, qv))
        if tuple(basis) in tried: continue
        tried.add(tuple(basis))
        try: xs, ys = basic_solution(R, rhs, tot, basis)
        except Exception as ex: fails.append(('singular', str(ex)[:40])); continue
        if any(xs[j] != K2.zero for j in xs if j >= n): fails.append(('artificial', None)); continue
        ok = True
        for j in xs:
            if j < n:
                sg, f = sign(xs[j], region)
                if sg not in ('+', '0', '+0'): ok = False; fails.append(('primal', str(f) if f is not None else sg)); break
        if not ok: continue
        for j in range(n):
            red = toK(tot[j]) - sum(ys[i] * toK(R[i][j]) for i in range(len(R)))
            sg, f = sign(red, region)
            if sg not in ('+', '0', '+0'): ok = False; fails.append(('dual', str(f) if f is not None else sg)); break
        if ok: found = (basis, xs, (pv, qv), val); break
    if not found: return dict(cat='?', why='no basis valid on the region', fails=fails[:6])
    basis, xs, (pv, qv), val = found
    v = sum(toK(tot[j]) * xs[j] for j in xs if j < n); D = toK(Msym) / v
    kexp = (sum(1 for l in range(1, 4) if (l, 0) in Z), sum(1 for m in range(1, 3) if (0, m) in Z)); k = toK(P**kexp[0] * Q**kexp[1])
    out.update(basis=basis, sample=(pv, qv), v=str(sp.factor(K2.to_sympy(v))), D=str(sp.factor(K2.to_sympy(D))))
    # ---- b ----
    if D != k:
        sg, f = sign(k - D, region)
        if sg == '+': out['cat'] = 'b'; return out
    # ---- a second point with the same value and a property ----
    def restricted(forbid=(), extra=(), objective=None, positive=None):
        Rr, rr = rows_for(Z, extra); cost = tot if objective is None else objective
        seen = set()
        for (pv2, qv2) in samples:
            st, val2, x2, basis2, y2 = simplex_full(numeric(Rr, pv2, qv2), numvec(rr, pv2, qv2), numvec(cost, pv2, qv2), forbid=forbid)
            if st != 'optimal' or tuple(basis2) in seen: continue
            seen.add(tuple(basis2))
            if positive is not None and x2[positive] <= 0: continue
            try: xs2, _ = basic_solution(Rr, rr, cost, basis2)
            except Exception: continue
            if any(xs2[j] != K2.zero for j in xs2 if j >= n): continue
            if any(j in forbid for j in xs2 if j < n and xs2[j] != K2.zero): continue
            if sum(toK(tot[j]) * xs2[j] for j in xs2 if j < n) != v: continue
            if not all(sign(xs2[j], region)[0] in ('+', '0', '+0') for j in xs2 if j < n): continue
            if positive is not None and sign(xs2.get(positive, K2.zero), region)[0] != '+': continue
            return basis2
        return None
    Pc, Qc = ci[(2, 2)], ci[(3, 1)]
    for name, forbid in (('Rp', [ci[c] for c in cls if c[0] == 0]), ('Rq', [ci[c] for c in cls if c[1] == 0])):
        b2 = restricted(forbid=forbid)
        if b2: out.update(cat='R', kind=name, basis2=b2); return out
    if not top_in:
        for name, cl in (('TP', Pc), ('TQ', Qc)):
            b2 = restricted(extra=[(e_(cl), sp.Integer(1))])
            if b2: out.update(cat='T', kind=name, basis2=b2); return out
    else:
        for name, cl in (('UP', Pc), ('UQ', Qc)):
            b2 = restricted(extra=[(tot, K2.to_sympy(v))], objective=[-vv for vv in e_(cl)], positive=cl)
            if b2: out.update(cat='U', kind=name, basis2=b2); return out
    # ---- H ----
    if top_in and D == toK(P * Q): out.update(cat='H', kind='M0'); return out
    if top_in and D == toK(P * P * Q):
        if {(1, 0), (3, 1), (2, 2)} <= Z: out.update(cat='H', kind='M2'); return out
        if {(0, 1), (1, 2)} <= Z: out.update(cat='H', kind='M4'); return out
    # ---- N: D/k = p^i q^j G / H with H prime to p and to q (as integers, for primes p != q) and 0 < |G - c H| < |H| for an integer c ----
    rr = sp.cancel(K2.to_sympy(D / k)); num, den = sp.fraction(rr)
    out.update(r=str(sp.factor(rr)))
    # (iii) strictly between two consecutive integers on the whole region
    c0 = int(sp.floor(rr.subs({P: pv, Q: qv})))
    if sign(toK(rr - c0), region)[0] == '+' and sign(toK(c0 + 1 - rr), region)[0] == '+':
        out.update(cat='N', kind=f'{c0} < D/k < {c0 + 1}'); return out
    # (ii) a prime divides the denominator and the numerator is prime to it: q | den and num(p, 0) = +-p^e (or the same with p, q exchanged)
    pn, pd = sp.Poly(num, P, Q), sp.Poly(den, P, Q)
    assert all(cf.is_integer for cf in pn.coeffs() + pd.coeffs())
    for var, other in ((Q, P), (P, Q)):
        if pd.eval(var, 0).is_zero:
            n0 = sp.Poly(pn.eval(var, 0).as_expr(), other)
            if not n0.is_zero and n0.is_monomial and abs(n0.LC()) == 1:
                out.update(cat='N', kind=f'{var} divides the denominator, numerator = {n0.as_expr()} mod {var}'); return out
    def strip(g):
        g = sp.Poly(g, P, Q); i = j = 0
        while g.eval(P, 0).is_zero: g = sp.Poly(sp.cancel(g.as_expr() / P), P, Q); i += 1
        while g.eval(Q, 0).is_zero: g = sp.Poly(sp.cancel(g.as_expr() / Q), P, Q); j += 1
        return g, i, j
    G, i1, j1 = strip(num); H, i2, j2 = strip(den)
    if i2 or j2: return dict(out, cat='?', why='denominator divisible by p or q')
    # (i) D/k = p^i q^j G/H.  For each of the two primes x (y the other one): H = +-y^e u(y) modulo x.  Then x does not divide H if u is
    # constant, or if m x < u(y) < (m + 1) x on the region for an integer m; and if only m x < u(y) < (m + 2) x can be shown, x | H forces
    # u(y) = (m + 1) x, a curve.  Off the curves H is prime to p and q, so H | G, which 0 < |G - cH| < |H| excludes; on a curve D/k is a
    # rational function of one variable, shown not to be an integer from some point on (quotient plus a small remainder) and checked below it.
    def one_var_nonint(r1, var):
        n1, d1 = sp.fraction(sp.cancel(r1)); quo, rem = sp.div(sp.Poly(n1, var, domain='QQ'), sp.Poly(d1, var, domain='QQ'))
        if rem.is_zero: return None
        cden = int(sp.ilcm(1, 1, *[sp.Rational(cf).q for cf in quo.all_coeffs()])) if not quo.is_zero else 1
        g = sp.cancel(cden * rem.as_expr() / d1); T1 = 2
        for ex in (g, 1 - g, 1 + g):
            nn, dd = sp.fraction(sp.cancel(ex))
            for pol in (sp.Poly(nn, var), sp.Poly(dd, var)):
                if pol.degree() >= 1:
                    ivs = pol.intervals()
                    if ivs: T1 = max(T1, int(sp.floor(max(iv[0][1] for iv in ivs))) + 1)
        if not ((1 - g).subs(var, T1) > 0 and (1 + g).subs(var, T1) > 0 and g.subs(var, T1) != 0): return None
        if any(sp.Rational(r1.subs(var, xx)).q == 1 for xx in range(2, T1) if d1.subs(var, xx) != 0): return None
        return T1
    notes = []; ok = True
    for x, y in ((P, Q), (Q, P)):
        u = sp.Poly(sp.expand(H.as_expr().subs(x, 0)), y)
        while u.eval(0) == 0: u = sp.Poly(sp.cancel(u.as_expr() / y), y)
        if u.LC() < 0: u = -u
        if u.degree() == 0:
            if abs(u.LC()) != 1: ok = False; notes.append(f'H = {u.as_expr()} y^e mod {x}')
            continue
        ue = u.as_expr(); done_ = False
        for m in range(0, 5):
            if sign(toK(ue - m * x), region)[0] == '+' and sign(toK((m + 1) * x - ue), region)[0] == '+':
                notes.append(f'{m}{x} < {ue} < {m + 1}{x}'); done_ = True; break
        if done_: continue
        for m in range(0, 5):
            if sign(toK(ue - m * x), region)[0] == '+' and sign(toK((m + 2) * x - ue), region)[0] == '+':
                if u.degree() != 1: break
                yc = sp.solve(sp.Eq(ue, (m + 1) * x), y)[0]                  # the curve u(y) = (m + 1) x, y as a function of x
                T1 = one_var_nonint(rr.subs(y, yc), x)
                if T1 is None: break
                notes.append(f'{x} | H only if {ue} = {m + 1}{x}; there D/k = {sp.factor(sp.cancel(rr.subs(y, yc)))}, not an integer (checked below {T1})'); done_ = True; break
        if not done_: ok = False; notes.append(f'cannot decide whether {x} divides H = +-{ue} y^e mod {x}')
    if not ok: return dict(out, cat='?', why='; '.join(notes))
    Hk, Gk = toK(H.as_expr()), toK(G.as_expr())
    for cc in (0, 1, -1, 2, -2):                           # H | G  iff  H | G - cc H; excluded if 0 < |G - cc H| < |H|
        d = Gk - cc * Hk
        for sH in (1, -1):
            for sd in (1, -1):
                if sign(sH * Hk, region)[0] == '+' and sign(sd * d, region)[0] == '+' and sign(sH * Hk - sd * d, region)[0] == '+':
                    out.update(cat='N', kind='(i) ' + '; '.join(notes) + f'; H | G - {cc}H impossible'); return out
    return dict(out, cat='?', why='integrality not excluded: ' + '; '.join(notes))

def run(region):
    res = {}; cnt = Counter(); t0 = time.time()
    for mask in range(1 << len(ords)):
        Z = frozenset(o for i, o in enumerate(ords) if mask >> i & 1)
        if (1, 0) not in Z and (0, 1) not in Z: res[Z] = dict(cat='L2'); cnt['L2'] += 1; continue
        t2 = all((l, m) in Z for l in range(1, 4) for m in range(1, 3) if (l, 0) in Z and (0, m) in Z)
        orph = any((l, 0) not in Z and (0, m) not in Z for (l, m) in Z if l and m)
        if t2 and not orph: res[Z] = dict(cat='a'); cnt['a'] += 1; continue
        r = analyse(Z, region); r['t2'] = t2; res[Z] = r; cnt[r['cat']] += 1
    return res, cnt, time.time() - t0

if __name__ == '__main__':
    region = sys.argv[1]; limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
    if limit:                                             # a quick trial on the first few patterns that need a certificate
        done = 0; t0 = time.time()
        for mask in range(1 << len(ords)):
            Z = frozenset(o for i, o in enumerate(ords) if mask >> i & 1)
            if (1, 0) not in Z and (0, 1) not in Z: continue
            t2 = all((l, m) in Z for l in range(1, 4) for m in range(1, 3) if (l, 0) in Z and (0, m) in Z); orph = any((l, 0) not in Z and (0, m) not in Z for (l, m) in Z if l and m)
            if t2 and not orph: continue
            r = analyse(Z, region); done += 1
            print(sorted(Z), r['cat'], r.get('kind', ''), r.get('why', ''), str(r.get('fails', ''))[:150], flush=True)
            if done >= limit: break
        print(f"{done} patterns in {time.time() - t0:.0f} s"); sys.exit()
    res, cnt, dt = run(region)
    print(f"region {region}: " + ", ".join(f"{k} {v}" for k, v in sorted(cnt.items())) + f";  T, U, H patterns with (T2): {sum(1 for r in res.values() if r['cat'] in ('T', 'U', 'H') and r['t2'])}   [{dt:.0f} s]")
    for Z, r in res.items():
        if r['cat'] == '?': print("   UNSETTLED:", sorted(Z), r.get('why'), str(r.get('fails', ''))[:200], r.get('r', ''))
    pickle.dump(res, open(f"region_{region}.pkl", "wb"))
