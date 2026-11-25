"""Independent verification of the certificates written by family.py.  (Noon = agent2, 21 November 2026)
Nothing is imported from plp.py or family.py.  For every pattern with a certificate (category b, R, T, U, N, H) the basic
solutions are recomputed from the stored basis with sympy matrices, and every sign condition is checked on [T, oo) by
counting real roots with Sturm sequences (Poly.count_roots) and evaluating at t = T:
  primal feasibility and dual feasibility of the stored basis (so v(t) is the optimum for every real t >= T);
  b: k - D > 0;   R, T, U: the second basis gives a feasible point with the same value and the stated property;
  N: D/k = quotient + remainder with 0 < |c * remainder| < 1, or a polynomial that is never an integer at integers prime to c;
  H: D = pq or p^2 q identically, M a zero, and the zeros that Lemma M asks for.
usage: verify.py c side"""
import sys, pickle, math, time
import sympy as sp
c0, side = int(sys.argv[1]), sys.argv[2]
res = pickle.load(open(f"family_{c0}_{side}.pkl", "rb")); T = max(r.get('T', 0) for r in res.values())
t = sp.symbols('t'); p, q = (sp.Integer(c0), t) if side == 'q' else (t, sp.Integer(c0)); M = p**3 * q**2
cls = [(i, j) for i in range(4) for j in range(3)]; ords = [o for o in cls if o != (0, 0)]; ci = {cl: k for k, cl in enumerate(cls)}; n = 12
def ram(pp, nn, l, i):
    if i == nn: return sp.Integer(1)
    return (pp ** (nn - i) if l <= i else 0) - (pp ** (nn - i - 1) if l <= i + 1 else 0)
C = {(o, cl): sp.expand(ram(p, 3, o[0], cl[0]) * ram(q, 2, o[1], cl[1])) for o in cls for cl in cls}
tot = [C[((0, 0), cl)] for cl in cls]; e = lambda k0: [sp.Integer(1) if k == k0 else sp.Integer(0) for k in range(n)]
def positive_from_T(expr, strict=True):
    """is the rational function > 0 (or identically 0 when not strict) at every real t >= T?"""
    expr = sp.cancel(expr)
    if expr == 0: return not strict
    num, den = sp.fraction(expr); pn, pd = sp.Poly(num, t), sp.Poly(den, t)
    for P in (pn, pd):
        if P.degree() >= 1 and P.count_roots(T, sp.oo) != 0: return False
    return (pn.eval(T) / pd.eval(T)) > 0
def solve(rows, rhs, cost, basis):
    m = len(rows)
    B = sp.Matrix(m, m, lambda i, k: rows[i][basis[k]] if basis[k] < n else (1 if i == basis[k] - n else 0))
    xb = B.LUsolve(sp.Matrix(rhs)); cb = sp.Matrix([cost[j] if j < n else 0 for j in basis]); y = B.T.LUsolve(cb)
    x = [sp.Integer(0)] * n
    for k, j in enumerate(basis):
        v = sp.cancel(xb[k])
        if j < n: x[j] = v
        elif v != 0: return None, None
    return x, [sp.cancel(v) for v in y]
bad = []; done = 0; t0 = time.time()
for Z, r in res.items():
    cat = r['cat']
    if cat in ('L2', 'a'):
        t2 = all((l, m) in Z for l in range(1, 4) for m in range(1, 3) if (l, 0) in Z and (0, m) in Z); orph = any((l, 0) not in Z and (0, m) not in Z for (l, m) in Z if l and m)
        if not ((cat == 'L2' and (1, 0) not in Z and (0, 1) not in Z) or (cat == 'a' and t2 and not orph)): bad.append((sorted(Z), 'L2/a'))
        continue
    done += 1
    rows = [e(ci[(3, 2)])] + [[C[(o, cl)] for cl in cls] for o in ords if o not in Z]; rhs = [sp.Integer(1)] + [sp.Integer(0)] * (len(rows) - 1)
    x, y = solve(rows, rhs, tot, r['basis'])
    ok = x is not None and all(positive_from_T(v, strict=False) for v in x)
    if ok:
        red = [sp.cancel(tot[j] - sum(y[i] * rows[i][j] for i in range(len(rows)))) for j in range(n)]
        ok = all(positive_from_T(v, strict=False) for v in red)
    if ok:
        v = sp.cancel(sum(tot[j] * x[j] for j in range(n))); ok = sp.cancel(v - sp.sympify(r['v'], locals={'t': t})) == 0
    if not ok: bad.append((sorted(Z), 'optimum')); continue
    D = sp.cancel(M / v); k = p ** sum(1 for l in range(1, 4) if (l, 0) in Z) * q ** sum(1 for m in range(1, 3) if (0, m) in Z); top = (3, 2) in Z
    if cat == 'b': ok = positive_from_T(k - D)
    elif cat in ('R', 'T', 'U'):
        kind = r['kind']; rows2, rhs2, cost2 = list(rows), list(rhs), tot
        if cat == 'T': rows2 = rows + [e(ci[(2, 2)] if kind == 'TP' else ci[(3, 1)])]; rhs2 = rhs + [sp.Integer(1)]; ok = not top
        if cat == 'U': rows2 = rows + [tot]; rhs2 = rhs + [v]; cost2 = [-vv for vv in e(ci[(2, 2)] if kind == 'UP' else ci[(3, 1)])]; ok = top
        x2, _ = solve(rows2, rhs2, cost2, r['basis2'])
        ok = ok and x2 is not None and all(positive_from_T(vv, strict=False) for vv in x2) and sp.cancel(sum(tot[j] * x2[j] for j in range(n)) - v) == 0
        if ok and cat == 'R': ok = all(x2[kk] == 0 for kk, cl in enumerate(cls) if (cl[0] == 0 if kind == 'Rp' else cl[1] == 0))
        if ok and cat == 'T': ok = x2[ci[(2, 2)] if kind == 'TP' else ci[(3, 1)]] == 1
        if ok and cat == 'U': ok = positive_from_T(x2[ci[(2, 2)] if kind == 'UP' else ci[(3, 1)]])
    elif cat == 'H':
        ok = top and ((r['kind'] == 'M0' and sp.cancel(D - p * q) == 0) or (r['kind'] == 'M2' and sp.cancel(D - p * p * q) == 0 and {(1, 0), (3, 1), (2, 2)} <= Z)
                      or (r['kind'] == 'M4' and sp.cancel(D - p * p * q) == 0 and {(0, 1), (1, 2)} <= Z))
    elif cat == 'N':
        num, den = sp.fraction(sp.cancel(D / k)); quo, rem = sp.div(sp.Poly(num, t, domain='QQ'), sp.Poly(den, t, domain='QQ'))
        cd = int(sp.ilcm(1, 1, *[sp.Rational(cf).q for cf in quo.all_coeffs()])) if not quo.is_zero else 1
        if not rem.is_zero:
            g = sp.cancel(cd * rem.as_expr() / den)
            ok = (positive_from_T(g) or positive_from_T(-g)) and positive_from_T(1 - g) and positive_from_T(1 + g)
        else:
            cq = sp.Poly(cd * quo.as_expr(), t); ok = T > cd and all(cq.eval(u) % cd != 0 for u in range(cd) if math.gcd(u, cd) == 1)
    else: ok = False
    if not ok: bad.append((sorted(Z), cat))
name = f"(p, q) = ({c0}, t)" if side == 'q' else f"(p, q) = (t, {c0})"
print(f"{name}: {done} certificates re-derived and checked on [T, oo) with T = {T}; failures {len(bad)}   [{time.time() - t0:.0f} s]")
for b in bad[:10]: print("   FAILED:", b)
