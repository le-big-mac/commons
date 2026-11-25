"""Referee: pointwise test of every certificate at very many prime pairs of a piece (integer arithmetic only at the pairs).
For each leaf the basic solutions x(p, q), reduced costs, and (R, T, U) the second point x2(p, q) are recomputed from the stored
bases against my own rows (Moebius form) over QQ(p, q); the identities are checked symbolically (artificial variables zero, x2 has
the optimal value, x2 vanishes outside the subgroup / equals 1 on P or Q, D = pq or p^2 q); then AT EVERY PRIME PAIR of a large set
(walking the tree by the signs of the split factors at the pair) the inequalities are evaluated exactly:
  no denominator vanishes; x >= 0; reduced costs >= 0; b: D < k; R/T/U: x2 >= 0 (U: x2 > 0 on P\\0 or Q\\0); N: D/k not an integer.
A pair that lands in a leaf 'empty' or '?' is reported.     usage: masscheck.py PIECE [bound on the fixed prime]"""
import sys, pickle, random, time
import sympy as sp
from sympy import QQ, primerange, nextprime, prevprime
from sympy.polys.matrices import DomainMatrix
piece = sys.argv[1]; D_ = '/home/agent2/p3q2/referee2/orig/'
res = pickle.load(open(D_ + ('region_' if piece in ('C3', 'Cp') else 'split_') + piece + '.pkl', 'rb'))
p, q = sp.symbols('p q'); random.seed(11)
rng = {'A1a': ('p', 5, lambda p: (p + 2, 2 * p - 3)), 'A1b': ('p', 5, lambda p: (2 * p - 1, p * p - p)), 'A2': ('p', 3, lambda p: (p * p - p + 1, p * p - 2)),
 'B1': ('p', 5, lambda p: (p * p + 1, p * p + p - 1)), 'B2': ('p', 3, lambda p: (p * p + p + 1, p**3 - p * p + p - 2)), 'B3': ('p', 3, lambda p: (p**3 - p * p + p, p**3 - 2)),
 'C3': ('p', 3, lambda p: (p**3 + 1, 30 * p**3)), 'Ap1': ('q', 3, lambda q: (q + 1, q * q - q)), 'Ap2': ('q', 3, lambda q: (q * q - q + 1, q * q - 2)),
 'Cp': ('q', 2, lambda q: (q * q + 1, 30 * q * q))}[piece]
fixedname, f0, bounds = rng
FMAX = int(sys.argv[2]) if len(sys.argv) > 2 else {'A1a': 400, 'A1b': 300, 'Ap1': 300, 'A2': 500, 'Ap2': 500, 'B1': 500, 'B2': 120, 'B3': 150, 'C3': 150, 'Cp': 250}[piece]
PER = {'A1a': 60, 'A1b': 60, 'Ap1': 60}.get(piece, 45)
pairs = []
for f in primerange(f0, FMAX):
    L, U = bounds(f)
    if L > U: continue
    allp = None
    if U - L < 1500: others = list(primerange(L, U + 1))
    else:
        others = set(); x = L - 1
        for _ in range(PER // 3): x = int(nextprime(x)); others.add(x)
        x = U + 1
        for _ in range(PER // 3): x = int(prevprime(x)); others.add(x)
        for _ in range(PER // 3): others.add(int(nextprime(random.randint(L, U - 100))))
        others = sorted(o for o in others if L <= o <= U)
    if f < 60 and U - L < 250000: others = list(primerange(L, U + 1))               # small fixed primes: every prime of the band
    for o in others:
        if o != f: pairs.append((f, o) if fixedname == 'p' else (o, f))
# and every pair of distinct primes below BOTH that lies in the piece
BOTH = 300; small = list(primerange(2, BOTH))
def in_piece(pv, qv):
    f, o = (pv, qv) if fixedname == 'p' else (qv, pv)
    return f >= f0 and bounds(f)[0] <= o and (piece in ('C3', 'Cp') or o <= bounds(f)[1])        # C3 and Cp are unbounded
nsmall = [(a, b) for a in small for b in small if a != b and in_piece(a, b)]
pairs = list(dict.fromkeys(pairs + nsmall))
cls = [(i, j) for i in range(4) for j in range(3)]; ords = [o for o in cls if o != (0, 0)]; ci = {c: k for k, c in enumerate(cls)}; n = 12
def lam_coeff(o, c):
    (l, m), (i, j) = o, c; tot = 0
    for di, dj, sg in ((0, 0, 1), (1, 0, -1), (0, 1, -1), (1, 1, 1)):
        i2, j2 = i + di, j + dj
        if i2 <= 3 and j2 <= 2 and i2 >= l and j2 >= m: tot += sg * p**(3 - i2) * q**(2 - j2)
    return sp.expand(tot)
C = {(o, c): lam_coeff(o, c) for o in cls for c in cls}; tot = [C[((0, 0), c)] for c in cls]; e = lambda k0: [sp.Integer(1) if k == k0 else sp.Integer(0) for k in range(n)]
KK = QQ.frac_field(p, q); toK = lambda v: KK.from_sympy(sp.sympify(v))
def solve(rows, rhs, cost, basis):
    m = len(rows)
    B = DomainMatrix([[toK(rows[i][basis[k]]) if basis[k] < n else (KK.one if i == basis[k] - n else KK.zero) for k in range(m)] for i in range(m)], (m, m), KK)
    Rm = DomainMatrix([[toK(v)] for v in rhs], (m, 1), KK); Cm = DomainMatrix([[toK(cost[j]) if j < n else KK.zero] for j in basis], (m, 1), KK)
    xbK = B.lu_solve(Rm); yK = B.transpose().lu_solve(Cm)
    # the linear algebra itself, as identities in the field QQ(p, q): B x_B = rhs and B^T y = c_B (so rows.x = rhs once the artificial components are 0)
    assert (B * xbK - Rm).to_Matrix().is_zero_matrix and (B.transpose() * yK - Cm).to_Matrix().is_zero_matrix, 'lu_solve gave a wrong solution'
    xb = xbK.to_Matrix(); y = yK.to_Matrix()
    x = [sp.Integer(0)] * n
    for k, j in enumerate(basis):
        v = sp.cancel(xb[k])
        if j < n: x[j] = v
        else: assert v == 0, 'artificial variable not identically zero'
    return x, [sp.cancel(v) for v in y]
def leaves(rec, path=()):
    if rec['cat'] == 'split': yield from leaves(rec['pos'], path + ((rec['factor'], 1),)); yield from leaves(rec['neg'], path + ((rec['factor'], -1),))
    else: yield path, rec
def fracs(exprs):
    """one function returning the numerators and denominators (integers at integer points) of a list of rational functions; zeros dropped"""
    nd = []
    for ex in exprs:
        ex = sp.cancel(ex)
        if ex == 0: continue
        a, b = sp.fraction(ex); ca = sp.Poly(a, p, q).coeffs() + sp.Poly(b, p, q).coeffs()
        assert all(c.is_integer for c in ca); nd += [a, b]
    return sp.lambdify((p, q), nd, modules='math') if nd else (lambda p_, q_: [])
LAM = {}
def fval(s, pv, qv):
    if s not in LAM: LAM[s] = sp.lambdify((p, q), sp.sympify(s, locals={'p': p, 'q': q}), modules='math')
    return LAM[s](pv, qv)
t0 = time.time(); items = []; symfail = []
for Z, rec in res.items():
    if rec['cat'] in ('L2', 'a'): continue
    rows = [e(ci[(3, 2)])] + [[C[(o, c)] for c in cls] for o in ords if o not in Z]; rhs = [sp.Integer(1)] + [sp.Integer(0)] * (len(rows) - 1)
    k = p ** sum(1 for l in range(1, 4) if (l, 0) in Z) * q ** sum(1 for m in range(1, 3) if (0, m) in Z); top = (3, 2) in Z
    t2 = all((l, m) in Z for l in range(1, 4) for m in range(1, 3) if (l, 0) in Z and (0, m) in Z)
    for path, lf in leaves(rec):
        cat = lf['cat']
        if cat in ('empty', '?', 'empty?'): items.append((Z, path, cat, None, None, None)); continue
        x, y = solve(rows, rhs, tot, lf['basis'])
        red = [tot[j] - sum(y[i] * rows[i][j] for i in range(len(rows))) for j in range(n)]
        v = sp.cancel(sum(tot[j] * x[j] for j in range(n))); Dk = sp.cancel(p**3 * q**2 / (v * k)); D = sp.cancel(p**3 * q**2 / v)
        weak = fracs(x + red); strict = []; nonint = None; symok = True
        if cat in ('T', 'U', 'H') and t2: symok = False
        if cat == 'b': strict = [k - D]
        elif cat in ('R', 'T', 'U'):
            kind = lf['kind']; rows2, rhs2, cost2 = rows, rhs, tot
            if cat == 'T': rows2 = rows + [e(ci[(2, 2)] if kind == 'TP' else ci[(3, 1)])]; rhs2 = rhs + [sp.Integer(1)]; symok &= not top
            if cat == 'U': rows2 = rows + [tot]; rhs2 = rhs + [v]; cost2 = [-vv for vv in e(ci[(2, 2)] if kind == 'UP' else ci[(3, 1)])]; symok &= top
            x2, _ = solve(rows2, rhs2, cost2, lf['basis2'])
            symok &= sp.cancel(sum(tot[j] * x2[j] for j in range(n)) - v) == 0
            if cat == 'R': symok &= kind in ('Rp', 'Rq') and all(x2[kk] == 0 for kk, c in enumerate(cls) if (c[0] == 0 if kind == 'Rp' else c[1] == 0))
            if cat == 'T': symok &= x2[ci[(2, 2)] if kind == 'TP' else ci[(3, 1)]] == 1
            if cat == 'U': strict = [x2[ci[(2, 2)] if kind == 'UP' else ci[(3, 1)]]]
            weak2 = fracs(x + red + x2); weak = weak2
        elif cat == 'H':
            symok &= top and ((lf['kind'] == 'M0' and sp.cancel(D - p * q) == 0) or (lf['kind'] == 'M2' and sp.cancel(D - p * p * q) == 0 and {(1, 0), (3, 1), (2, 2)} <= Z)
                              or (lf['kind'] == 'M4' and sp.cancel(D - p * p * q) == 0 and {(0, 1), (1, 2)} <= Z))
        elif cat == 'N': nonint = fracs([Dk])
        else: symok = False
        if not symok: symfail.append((sorted(Z), path, cat))
        items.append((Z, path, cat, weak, fracs(strict), nonint))
tsym = time.time() - t0; t0 = time.time(); bad = []; nev = 0; reached = {}
byZ = {}
for it in items: byZ.setdefault(it[0], []).append(it)
for (pv, qv) in pairs:
    for Z, its in byZ.items():
        hit = [it for it in its if all(sg * fval(F, pv, qv) >= 0 for F, sg in it[1])]
        if not hit: bad.append((pv, qv, sorted(Z), 'no branch contains the pair')); continue
        for (Z_, path, cat, weak, strict, nonint) in hit:          # a pair on a curve F = 0 lies in both branches: both must hold there
            nev += 1; reached[cat] = reached.get(cat, 0) + 1
            if cat in ('empty', '?', 'empty?'): bad.append((pv, qv, sorted(Z), 'pair in a leaf ' + cat)); continue
            w = weak(pv, qv)
            if any(w[i + 1] == 0 or w[i] * w[i + 1] < 0 for i in range(0, len(w), 2)): bad.append((pv, qv, sorted(Z), cat, 'feasibility fails')); continue
            s_ = strict(pv, qv)
            if any(s_[i + 1] == 0 or s_[i] * s_[i + 1] <= 0 for i in range(0, len(s_), 2)): bad.append((pv, qv, sorted(Z), cat, 'strict property fails')); continue
            if nonint is not None:
                a, b = nonint(pv, qv)
                if b == 0 or a % b == 0: bad.append((pv, qv, sorted(Z), cat, 'D/k is an integer')); continue
print(f"piece {piece}: {len(items)} leaves, symbolic identities failing: {len(symfail)}; {len(pairs)} prime pairs (incl. all {len(nsmall)} pairs of the piece with both primes < {BOTH}; {fixedname} < {FMAX}; all primes of the band for {fixedname} < 60 where the band has < 250000 integers), "
      f"{nev} leaf evaluations {dict(sorted(reached.items()))}; FAILURES {len(bad)}   [symbolic {tsym:.0f} s, numeric {time.time() - t0:.0f} s]")
for b in symfail[:5]: print("   SYMBOLIC:", b)
for b in bad[:10]: print("   FAIL:", str(b)[:300])
