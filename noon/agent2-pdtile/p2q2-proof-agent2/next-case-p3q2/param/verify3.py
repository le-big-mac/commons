"""Independent verification of the two-parameter certificates written by region.py and split.py (bands and case
distinctions included).  (Noon = agent2, 21 November 2026)
Nothing is imported from region.py, family.py or plp.py.  For every pattern with a certificate the basic solutions are
recomputed from the stored basis, and every sign condition is re-proved on the region by this script's own test:
substitute the parametrisation (parameters >= 0), clear the positive denominator by multiplying with the right power of
(1 + z), expand, and require all coefficients of one sign with a nonzero value at the corner.  Then:
  the stored basis is primal and dual feasible on the region, so its value v(p, q) is the optimum there;
  b: k - D > 0;   R, T, U: the second basis gives a feasible point with the same value and the stated property;
  H: D = pq or p^2 q identically, M a zero, and the zeros Lemma M needs;
  N: D/k is not an integer for primes p != q in the region, by one of three arguments re-established here:
     (iii) c < D/k < c + 1 for an integer c;  (ii) a prime (p or q) divides the denominator and the numerator is +-(a power of
     the other prime) modulo it;  (i) D/k = p^i q^j G/H with H = +-(power of q) mod p and +-(power of p) mod q, and
     0 < |G - cH| < |H| for an integer c.
A certificate with case distinctions is a tree: at a node the factor F is assumed >= 0 on one branch and <= 0 on the other
(every point lies in one of them); on a branch an assumed factor counts as weakly signed and may not occur in a denominator.
usage: verify3.py REGION [pickle prefix: region or split]"""
import sys, pickle, time
import sympy as sp
from sympy import QQ
from sympy.polys.matrices import DomainMatrix
region = sys.argv[1]; prefix = sys.argv[2] if len(sys.argv) > 2 else "region"; res = pickle.load(open(f"{prefix}_{region}.pkl", "rb"))
p, q = sp.symbols('p q'); r, s, z = sp.symbols('r s z')
def band(fixed, lo, up, p0):
    other = q if fixed == p else p
    return ({fixed: p0 + r, other: ((lo + up * z) / (1 + z)).subs(fixed, p0 + r)}, other)
PARAM = {   # p and q in terms of parameters >= 0, and the variable whose degree gives the power of (1 + z) that clears denominators
 'C':  ({p: 2 + r, q: (2 + r)**3 + 1 + s}, None), 'C3': ({p: 3 + r, q: (3 + r)**3 + 1 + s}, None),
 'Cp': ({q: 2 + r, p: (2 + r)**2 + 1 + s}, None),
 'B1': band(p, p**2 + 1, p**2 + p, 5), 'B2': band(p, p**2 + p + 1, p**3 - p**2 + p - 1, 3), 'B3': band(p, p**3 - p**2 + p, p**3 - 1, 3),
 'Ap1': band(q, q + 1, q**2 - q + 1, 3), 'Ap2': band(q, q**2 - q + 1, q**2 - 1, 3),
 'A1a': band(p, p + 2, 2 * p - sp.Rational(5, 2), 5), 'A1b': band(p, 2 * p - 1, p**2 - p + 1, 5), 'A2': band(p, p**2 - p + 1, p**2 - 1, 3),
}[region]
ASSUME = []                                               # (polynomial, +1 or -1): sign * polynomial >= 0 on the current branch
cls = [(i, j) for i in range(4) for j in range(3)]; ords = [o for o in cls if o != (0, 0)]; ci = {c: k for k, c in enumerate(cls)}; n = 12
def ram(pp, nn, l, i):
    if i == nn: return sp.Integer(1)
    return (pp ** (nn - i) if l <= i else 0) - (pp ** (nn - i - 1) if l <= i + 1 else 0)
C = {(o, c): sp.expand(ram(p, 3, o[0], c[0]) * ram(q, 2, o[1], c[1])) for o in cls for c in cls}
tot = [C[((0, 0), c)] for c in cls]; M = p**3 * q**2; e = lambda k0: [sp.Integer(1) if k == k0 else sp.Integer(0) for k in range(n)]
CACHE = {}
def poly_sign(g):
    """+1 / -1 if the polynomial g(p, q) is > 0 / < 0 at every point of the region, 2 / -2 if only >= 0 / <= 0 is shown, 0 if not shown"""
    for F, sg in ASSUME:
        if sp.expand(g - F) == 0: return 2 * sg
        if sp.expand(g + F) == 0: return -2 * sg
    if g in CACHE: return CACHE[g]
    sub, var = PARAM
    if var is None: ex = sp.expand(g.subs(sub, simultaneous=True))
    else: ex = sp.expand(sp.cancel(g.subs(sub, simultaneous=True) * (1 + z) ** sp.Poly(g, p, q).degree(var)))
    gens = [v for v in (r, s, z) if ex.has(v)]
    if not gens: out = 1 if ex > 0 else (-1 if ex < 0 else 0)
    else:
        co = sp.Poly(ex, *gens).coeffs(); corner = ex.subs({v: 0 for v in gens})
        if all(c >= 0 for c in co): out = 1 if corner > 0 else 2
        elif all(c <= 0 for c in co): out = -1 if corner < 0 else -2
        else: out = 0
    CACHE[g] = out; return out
def rat_sign(expr):
    """sign of a rational function on the region: 1, -1 (strict), 2, -2 (weak), 0 (identically zero), None (not shown)"""
    expr = sp.cancel(expr)
    if expr == 0: return 0
    num, den = sp.fraction(expr); sg = 1; strict = True
    for part, is_den in ((num, False), (den, True)):
        cst, facs = sp.factor_list(part)
        if cst < 0: sg = -sg
        for f, mult in facs:
            v = poly_sign(f)
            if v == 0 or (is_den and abs(v) == 2): return None
            if v < 0 and mult % 2: sg = -sg
            if abs(v) == 2: strict = False
    return sg if strict else 2 * sg
nonneg = lambda ex: rat_sign(ex) in (0, 1, 2); pos = lambda ex: rat_sign(ex) == 1
KK = QQ.frac_field(p, q); toK = lambda v: KK.from_sympy(sp.sympify(v))
def solve(rows, rhs, cost, basis):
    m = len(rows)
    B = DomainMatrix([[toK(rows[i][basis[k]]) if basis[k] < n else (KK.one if i == basis[k] - n else KK.zero) for k in range(m)] for i in range(m)], (m, m), KK)
    xb = B.lu_solve(DomainMatrix([[toK(v)] for v in rhs], (m, 1), KK)).to_Matrix()
    y = B.transpose().lu_solve(DomainMatrix([[toK(cost[j]) if j < n else KK.zero] for j in basis], (m, 1), KK)).to_Matrix()
    x = [sp.Integer(0)] * n
    for k, j in enumerate(basis):
        v = sp.cancel(xb[k])
        if j < n: x[j] = v
        elif v != 0: return None, None
    y = [sp.cancel(v) for v in y]
    # (added after the second referee's report) the solution is checked, not trusted: A x = b on every row; B^T y = c_B, that is, zero
    # reduced cost on every basic column and y = 0 on a row whose artificial variable is basic; and no component of x or y has a pole on
    # the piece: every irreducible factor of every denominator is strictly signed there, without using a branch assumption
    if any(sp.cancel(sum(rows[i][j] * x[j] for j in range(n)) - rhs[i]) != 0 for i in range(m)): return None, None
    for j in basis:
        if j < n and sp.cancel(cost[j] - sum(y[i] * rows[i][j] for i in range(m))) != 0: return None, None
        if j >= n and y[j - n] != 0: return None, None
    for val in x + y:
        for f, mult in sp.factor_list(sp.fraction(val)[1])[1]:
            if any(sp.expand(f - F) == 0 or sp.expand(f + F) == 0 for F, sg in ASSUME) or abs(poly_sign(f)) != 1: return None, None
    return x, y
def not_integer(rr, sample):
    num, den = sp.fraction(sp.cancel(rr)); pn, pd = sp.Poly(num, p, q), sp.Poly(den, p, q)
    if not all(c.is_integer for c in pn.coeffs() + pd.coeffs()): return False
    c0 = int(sp.floor(rr.subs({p: sample[0], q: sample[1]})))
    if pos(rr - c0) and pos(c0 + 1 - rr): return True                                             # (iii)
    for var, other in ((q, p), (p, q)):                                                            # (ii)
        if pd.eval(var, 0).is_zero:
            n0 = sp.Poly(pn.eval(var, 0).as_expr(), other)
            if not n0.is_zero and n0.is_monomial and abs(n0.LC()) == 1: return True
    def strip(g):
        i = j = 0
        while sp.Poly(g, p, q).eval(p, 0).is_zero: g = sp.cancel(g / p); i += 1
        while sp.Poly(g, p, q).eval(q, 0).is_zero: g = sp.cancel(g / q); j += 1
        return g, i, j
    G, _, _ = strip(num); H, i2, j2 = strip(den)
    if i2 or j2: return False
    # (i): for each prime x (y the other), H = +-y^e u(y) modulo x; x does not divide H if u is +-1, or if m x < u < (m + 1) x on the region;
    # if only m x < u < (m + 2) x, then x | H forces u(y) = (m + 1) x, and on that curve D/k must be shown not to be an integer.
    for x, y in ((p, q), (q, p)):
        u = sp.Poly(sp.expand(H.subs(x, 0)), y)
        while u.eval(0) == 0: u = sp.Poly(sp.cancel(u.as_expr() / y), y)
        if u.LC() < 0: u = -u
        if u.degree() == 0:
            if abs(u.LC()) != 1: return False
            continue
        ue = u.as_expr()
        if any(pos(ue - m * x) and pos((m + 1) * x - ue) for m in range(5)): continue
        okc = False
        for m in range(5):
            if pos(ue - m * x) and pos((m + 2) * x - ue) and u.degree() == 1:
                yc = sp.solve(sp.Eq(ue, (m + 1) * x), y)[0]; r1 = sp.cancel(rr.subs(y, yc))
                n1, d1 = sp.fraction(r1); quo, rem = sp.div(sp.Poly(n1, x, domain='QQ'), sp.Poly(d1, x, domain='QQ'))
                if rem.is_zero: break
                cd = int(sp.ilcm(1, 1, *[sp.Rational(cf).q for cf in quo.all_coeffs()])) if not quo.is_zero else 1
                g = sp.cancel(cd * rem.as_expr() / d1); T1 = 2
                while T1 < 10**6:                             # from T1 on: g, 1 - g, 1 + g have no real root (Sturm), 1 +- g > 0, g != 0
                    good = True
                    for ex, need_pos in ((g, None), (1 - g, True), (1 + g, True)):
                        nn, dd = sp.fraction(sp.cancel(ex))
                        for pol in (sp.Poly(nn, x), sp.Poly(dd, x)):
                            if pol.degree() >= 1 and pol.count_roots(T1, sp.oo) != 0: good = False
                        if need_pos and not ex.subs(x, T1) > 0: good = False
                        if need_pos is None and ex.subs(x, T1) == 0: good = False
                    if good: break
                    T1 *= 2
                if T1 < 10**6 and not any(sp.Rational(r1.subs(x, xx)).q == 1 for xx in range(2, T1) if d1.subs(x, xx) != 0): okc = True
                break
        if not okc: return False
    for cc in (0, 1, -1, 2, -2):
        d = sp.expand(G - cc * H)
        for sH in (1, -1):
            for sd in (1, -1):
                if pos(sH * H) and pos(sd * d) and pos(sH * H - sd * d): return True
    return False
bad = []; done = 0; t0 = time.time(); skipped = 0; nleaves = 0
def check_leaf(Z, rec, t2):
    """True if the certificate rec for the pattern Z holds on the current branch"""
    cat = rec['cat']
    rows = [e(ci[(3, 2)])] + [[C[(o, c)] for c in cls] for o in ords if o not in Z]; rhs = [sp.Integer(1)] + [sp.Integer(0)] * (len(rows) - 1)
    x, y = solve(rows, rhs, tot, rec['basis'])
    if x is None or not all(nonneg(v) for v in x): return False
    if not all(nonneg(tot[j] - sum(y[i] * rows[i][j] for i in range(len(rows)))) for j in range(n)): return False
    v = sp.cancel(sum(tot[j] * x[j] for j in range(n)))
    if sp.cancel(v - sp.sympify(rec['v'], locals={'p': p, 'q': q})) != 0: return False
    D = sp.cancel(M / v); k = p ** sum(1 for l in range(1, 4) if (l, 0) in Z) * q ** sum(1 for m in range(1, 3) if (0, m) in Z); top = (3, 2) in Z
    if cat in ('T', 'U', 'H') and t2: return False
    if cat == 'b': return pos(k - D)
    if cat in ('R', 'T', 'U'):
        kind = rec['kind']; rows2, rhs2, cost2 = list(rows), list(rhs), tot; ok = True
        if cat == 'T': rows2 = rows + [e(ci[(2, 2)] if kind == 'TP' else ci[(3, 1)])]; rhs2 = rhs + [sp.Integer(1)]; ok = not top
        if cat == 'U': rows2 = rows + [tot]; rhs2 = rhs + [v]; cost2 = [-vv for vv in e(ci[(2, 2)] if kind == 'UP' else ci[(3, 1)])]; ok = top
        x2, _ = solve(rows2, rhs2, cost2, rec['basis2'])
        ok = ok and x2 is not None and all(nonneg(vv) for vv in x2) and sp.cancel(sum(tot[j] * x2[j] for j in range(n)) - v) == 0
        if ok and cat == 'R': ok = all(x2[kk] == 0 for kk, c in enumerate(cls) if (c[0] == 0 if kind == 'Rp' else c[1] == 0))
        if ok and cat == 'T': ok = x2[ci[(2, 2)] if kind == 'TP' else ci[(3, 1)]] == 1
        if ok and cat == 'U': ok = pos(x2[ci[(2, 2)] if kind == 'UP' else ci[(3, 1)]])
        return ok
    if cat == 'H':
        return top and ((rec['kind'] == 'M0' and sp.cancel(D - p * q) == 0) or (rec['kind'] == 'M2' and sp.cancel(D - p * p * q) == 0 and {(1, 0), (3, 1), (2, 2)} <= Z)
                        or (rec['kind'] == 'M4' and sp.cancel(D - p * p * q) == 0 and {(0, 1), (1, 2)} <= Z))
    if cat == 'N': return not_integer(sp.cancel(D / k), rec['sample'])
    return False
def walk(Z, rec, t2, assume):
    """verify a certificate tree; returns the list of failing leaves"""
    global ASSUME, nleaves
    if rec['cat'] == 'split':
        F = sp.sympify(rec['factor'], locals={'p': p, 'q': q})
        return walk(Z, rec['pos'], t2, assume + [(F, 1)]) + walk(Z, rec['neg'], t2, assume + [(F, -1)])
    nleaves += 1
    if rec['cat'] in ('?', 'empty?'): return [(rec['cat'], [(str(F), sg) for F, sg in assume])]
    if rec['cat'] == 'empty':
        # the branch is claimed to contain no point: T = sum of (multiplier with coefficients >= 0) * sign * F over assumed factors, and T < 0 on the band
        T = sp.Integer(0); ok = True
        for ms, Fs, sg in rec['proof']:
            m = sp.sympify(ms, locals={'p': p, 'q': q}); F = sp.sympify(Fs, locals={'p': p, 'q': q})
            ok = ok and all(c > 0 for c in sp.Poly(m, p, q).coeffs()) and any(sp.expand(F - G) == 0 and sg == s2 for G, s2 in assume)
            T += m * sg * F
        ASSUME = []; CACHE.clear()
        return [] if ok and poly_sign(sp.expand(T)) == -1 else [('empty', [(str(F), sg) for F, sg in assume])]
    ASSUME = list(assume); CACHE.clear()
    return [] if check_leaf(Z, rec, t2) else [(rec['cat'], [(str(F), sg) for F, sg in assume])]
ALL = [frozenset(o for i, o in enumerate(ords) if mask >> i & 1) for mask in range(1 << len(ords))]
assert len(res) == 2048 and all(Z in res for Z in ALL), "the pickle does not hold exactly the 2,048 patterns"
for Z, rec in res.items():
    cat = rec['cat']
    t2 = all((l, m) in Z for l in range(1, 4) for m in range(1, 3) if (l, 0) in Z and (0, m) in Z); orph = any((l, 0) not in Z and (0, m) not in Z for (l, m) in Z if l and m)
    if cat in ('L2', 'a'):
        if not ((cat == 'L2' and (1, 0) not in Z and (0, 1) not in Z) or (cat == 'a' and t2 and not orph)): bad.append((sorted(Z), 'L2/a'))
        continue
    done += 1
    fails = walk(Z, rec, t2, [])
    if fails: bad.append((sorted(Z), fails))
print(f"region {region} ({prefix}): all 2,048 patterns present; {done} patterns, {nleaves} leaves re-derived and re-proved (solutions checked, no pole of x or y on the piece); patterns with a failing or missing leaf: {len(bad)}   [{time.time() - t0:.0f} s]")
for b in bad[:12]: print("   FAILED:", str(b)[:300])
