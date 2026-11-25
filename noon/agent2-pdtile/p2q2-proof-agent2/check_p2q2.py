"""Checker for the linear-programming part of  'weak tiles of Z_{p^2 q^2} are tiles'.   (sympy only; no solver)

Setting.  M = p^2 q^2, p < q primes.  A step function f on Z_M is given by nine numbers gamma[i,j], i,j in {0,1,2}:
f(x) = gamma[i,j] when x = (u,w) in Z_{p^2} x Z_{q^2} has min(v_p(u),2) = i and min(v_q(w),2) = j.  Its Fourier transform
at a frequency of order p^l q^m is
        Lambda[l,m] = sum_{i,j} gamma[i,j] * c_p(l,i) * c_q(m,j),
        c_p(0,.) = (p^2-p, p-1, 1),   c_p(1,.) = (-p, p-1, 1),   c_p(2,.) = (0, -1, 1)        (same with q).
A zero pattern is  Z = {(l,0): l in Ep} u {(0,m): m in Eq} u F.  The programme LP(Z):
        gamma >= 0,  gamma[2,2] = 1,  Lambda[l,m] = 0 for (l,m) not in Z, (l,m) != (0,0);   minimise sigma = Lambda[0,0].
If A is a weak tile with zero set Z then its step complements are exactly the optimal points, and |A| = M / sigma_min.

What is checked, for each of the 192 patterns in which p or q is a zero (the other 64 are settled by Lemma 2) and for each regime
(A: p < q < p^2,  B: q > p^2), from the file certificates_p2q2.json:

  dual  y (one number per equality constraint):  r[c] = cost[c] - sum_rows y[row]*coef[row][c] >= 0 for the nine classes c.
        Then sigma >= y[norm] for every feasible gamma.
  cat a : (T2) holds for the pattern and it has no orphan.        (nothing to check here)
  cat b : y[norm] > M/k            (so |A| <= M/y[norm] < k, impossible since k divides |A|)
  cat RP, RQ : a feasible gamma supported in pZ (gamma[0,j] = 0), resp. qZ (gamma[i,0] = 0), with sigma = y[norm]
  cat H : y[norm] = M/k, k = pq, 1 in Ep, (2,2) in F, (1,2) not in F     (then Lemma Y' applies)
  cat N : a feasible gamma with sigma = y[norm] = (p^2(q-1) + q^2(p-1))/(pq-1)   (then |A| would not be an integer)

Identities are checked by exact simplification.  Signs are checked factor by factor: a polynomial factor g(p,q) is
accepted as positive (negative) on a regime if, after the substitution
        regime B:  p = 2+s,  q = p^2+1+t                         (s,t >= 0)
        regime A:  p = 2+s,  q = ((p+1) + (p^2-1) z)/(1+z)       (s,z >= 0;  multiplied by (1+z)^deg)
all coefficients have one sign.  (For p > 2 the endpoint q = p^2-1 is not prime; for p = 2 the interval is {3}.)
A factor that cannot be decided this way makes the check fail, and so does a denominator factor whose sign is
only weak (it could vanish at a prime pair of the regime).
"""
import json, sys, itertools, sympy as sp

p, q = sp.symbols('p q', positive=True)
s, t, z = sp.symbols('s t z', nonnegative=True)
CLS = [(i, j) for i in range(3) for j in range(3)]
ORDS = [(l, m) for l in range(3) for m in range(3)]


def c(P, l, i):
    return [[P**2 - P, P - 1, 1], [-P, P - 1, 1], [0, -1, 1]][l][i]


def coef(o, cl):
    return sp.Integer(1) * c(p, o[0], cl[0]) * c(q, o[1], cl[1])


def sign_poly(g, regime):
    if regime == 'B':
        e = sp.expand(g.subs({q: p**2 + 1 + t}).subs({p: 2 + s})); gens = (s, t)
    else:
        d = sp.degree(g, q)
        e = sp.expand(sp.cancel(g.subs({q: ((p + 1) + (p**2 - 1) * z) / (1 + z)}) * (1 + z)**d).subs({p: 2 + s})); gens = (s, z)
    co = sp.Poly(e, *gens).coeffs()
    const = e.subs({x: 0 for x in gens})
    if all(x > 0 for x in co): return '+' if const > 0 else '+0'
    if all(x < 0 for x in co): return '-' if const < 0 else '-0'
    return '?'


def sign(expr, regime):
    """'+', '-' (strict), '+0', '-0' (weak), '0', or '?'."""
    expr = sp.together(sp.simplify(expr))
    if expr == 0: return '0'
    num, den = sp.fraction(expr)
    sg, strict = 1, True
    for part in (num, den):
        k0, facs = sp.factor_list(part)
        if k0 < 0: sg = -sg
        for g, mult in facs:
            r = sign_poly(g, regime)
            if r == '?': return '?'
            if r.endswith('0') and part is den: return '?'      # a denominator must not vanish anywhere on the regime
            if r[0] == '-' and mult % 2 == 1: sg = -sg
            if r.endswith('0'): strict = False
    return ('+' if sg > 0 else '-') + ('' if strict else '0')


def nonneg(expr, regime): return sign(expr, regime) in ('+', '+0', '0')


def survivors():
    sub = lambda S: itertools.chain.from_iterable(itertools.combinations(S, r) for r in range(len(S) + 1))
    for Ep in sub((1, 2)):
        for Eq in sub((1, 2)):
            for F in sub([(1, 1), (1, 2), (2, 1), (2, 2)]):
                Z = {(l, 0) for l in Ep} | {(0, m) for m in Eq} | set(F)
                if 1 not in Ep and 1 not in Eq: continue          # these 64 patterns are settled by Lemma 2 (A lies in pZ or qZ)
                yield Ep, Eq, F, Z


def check(entry):
    Ep, Eq, F = tuple(entry['Ep']), tuple(entry['Eq']), tuple(tuple(x) for x in entry['F'])
    Z = {(l, 0) for l in Ep} | {(0, m) for m in Eq} | set(F)
    regime, cat = entry['regime'], entry['cat']
    t2 = all((l, m) in F for l in Ep for m in Eq)
    orphan = any(l not in Ep and m not in Eq for (l, m) in F)
    if cat == 'a': return t2 and not orphan
    k = p**len(Ep) * q**len(Eq); Mk = p**2 * q**2 / k
    rows = ['norm'] + ['%d,%d' % o for o in ORDS if o != (0, 0) and o not in Z]
    if set(entry['y']) != set(rows): return False
    y = {r: sp.sympify(entry['y'][r], locals={'p': p, 'q': q}) for r in rows}
    def rowcoef(r, cl):
        if r == 'norm': return sp.Integer(1) if cl == (2, 2) else sp.Integer(0)
        return coef(tuple(int(x) for x in r.split(',')), cl)
    for cl in CLS:                                        # dual feasibility
        red = coef((0, 0), cl) - sum(y[r] * rowcoef(r, cl) for r in rows)
        if not nonneg(red, regime): return False
    y0 = y['norm']
    if cat == 'b': return sign(y0 - Mk, regime) == '+'
    g = {cl: sp.Integer(0) for cl in CLS}
    for key, val in entry.get('gamma', {}).items():
        g[tuple(int(x) for x in key.split(','))] = sp.sympify(val, locals={'p': p, 'q': q})
    feasible = (sp.simplify(g[(2, 2)] - 1) == 0 and all(nonneg(g[cl], regime) for cl in CLS)
                and all(sp.simplify(sum(g[cl] * coef(o, cl) for cl in CLS)) == 0 for o in ORDS if o != (0, 0) and o not in Z)
                and sp.simplify(sum(g[cl] * coef((0, 0), cl) for cl in CLS) - y0) == 0)
    if cat == 'RP': return feasible and all(g[(0, j)] == 0 for j in range(3))
    if cat == 'RQ': return feasible and all(g[(i, 0)] == 0 for i in range(3))
    if cat == 'H':
        return (sp.simplify(y0 - Mk) == 0 and Ep == (1,) and len(Eq) == 1 and (2, 2) in F and (1, 2) not in F)
    if cat == 'N':
        return feasible and Ep == (1,) and Eq == (1,) and sp.simplify(y0 - (p**2 * (q - 1) + q**2 * (p - 1)) / (p * q - 1)) == 0
    return False


if __name__ == '__main__':
    assert sign(q - p, 'A') == '+' and sign(q - p, 'B') == '+' and sign(p**2 - q, 'B') == '-' and sign(p - 2, 'A') == '+0'
    assert sign(p**2 - q, 'A') in ('+', '+0') and sign(q - p**2 + p, 'A') == '?' and sign((p - q) / (q - 1), 'B') == '-'
    assert sign(1 / (p - 2), 'A') == '?' and sign(1 / (q - p - 1), 'A') == '?' and sign(1 / (q - p**2 - 1), 'B') == '?'
    entries = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'certificates_p2q2.json'))
    index = {(e['regime'], tuple(e['Ep']), tuple(e['Eq']), tuple(tuple(x) for x in e['F'])): e for e in entries}
    from collections import Counter
    for regime in 'AB':
        cnt = Counter(); fails = []
        for Ep, Eq, F, Z in survivors():
            e = index.get((regime, Ep, Eq, F))
            ok = e is not None and check(e)
            cnt[e['cat'] if ok else 'FAIL'] += 1
            if not ok: fails.append((Ep, Eq, F))
        print('regime', regime, ' patterns:', sum(cnt.values()), dict(cnt), ' failures:', fails, flush=True)
