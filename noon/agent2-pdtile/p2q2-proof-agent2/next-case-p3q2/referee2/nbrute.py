"""Referee: category N by brute force.  For every leaf of category N of a piece, evaluate D^w/k = M/(v k) (v = the leaf's certified
formula) at very many prime pairs of the piece (walking the tree by the signs of the split factors) and look for an integer value.
Also re-derives, per leaf, which integrality argument applies, with the congruence facts checked numerically at each pair for (i):
gcd(H, pq) = 1 off the stated curve and 0 < |G - cH| < |H|.
usage: nbrute.py PIECE"""
import sys, pickle, random, time, math
import sympy as sp
from sympy import primerange, nextprime, prevprime
piece = sys.argv[1]; D_ = '/home/agent2/p3q2/referee2/orig/'
res = pickle.load(open(D_ + ('region_' if piece in ('C3', 'Cp') else 'split_') + piece + '.pkl', 'rb'))
P, Q = sp.symbols('p q'); random.seed(3)
rng = {   # fixed prime, lower bound, range of the other prime as integers [L, U]
 'A1a': ('p', 5, lambda p: (p + 2, 2 * p - 3)), 'A1b': ('p', 5, lambda p: (2 * p - 1, p * p - p)), 'A2': ('p', 3, lambda p: (p * p - p + 1, p * p - 2)),
 'B1': ('p', 5, lambda p: (p * p + 1, p * p + p - 1)), 'B2': ('p', 3, lambda p: (p * p + p + 1, p**3 - p * p + p - 2)), 'B3': ('p', 3, lambda p: (p**3 - p * p + p, p**3 - 2)),
 'C3': ('p', 3, lambda p: (p**3 + 1, 40 * p**3)), 'Ap1': ('q', 3, lambda q: (q + 1, q * q - q)), 'Ap2': ('q', 3, lambda q: (q * q - q + 1, q * q - 2)),
 'Cp': ('q', 2, lambda q: (q * q + 1, 40 * q * q))}[piece]
fixedname, f0, bounds = rng
FMAX = {'B2': 200, 'B3': 200, 'C3': 300, 'Cp': 600}.get(piece, 1500); PER = 150
pairs = []
for f in primerange(f0, FMAX):
    L, U = bounds(f)
    if L > U: continue
    if U - L < 4000: others = [o for o in primerange(L, U + 1)]
    else:
        others = set(); x = L - 1
        for _ in range(PER // 3): x = int(nextprime(x)); others.add(x)
        x = U + 1
        for _ in range(PER // 3): x = int(prevprime(x)); others.add(x)
        for _ in range(PER // 3): others.add(int(nextprime(random.randint(L, U - 200))))
        others = [o for o in others if L <= o <= U]
    for o in others:
        if o != f: pairs.append((f, o) if fixedname == 'p' else (o, f))
def leaves(rec, path=()):
    if rec['cat'] == 'split': yield from leaves(rec['pos'], path + ((rec['factor'], 1),)); yield from leaves(rec['neg'], path + ((rec['factor'], -1),))
    else: yield path, rec
LAM = {}
def lam(s):
    if s not in LAM: LAM[s] = sp.lambdify((P, Q), sp.sympify(s, locals={'p': P, 'q': Q}), modules='math')
    return LAM[s]
items = []
for Z, rec in res.items():
    for path, lf in leaves(rec):
        if lf['cat'] != 'N': continue
        v = sp.cancel(sp.sympify(lf['v'], locals={'p': P, 'q': Q})); vn, vd = sp.fraction(v)
        k = P ** sum(1 for l in range(1, 4) if (l, 0) in Z) * Q ** sum(1 for m in range(1, 3) if (0, m) in Z)
        num, den = sp.fraction(sp.cancel(P**3 * Q**2 * vd / (vn * k)))
        assert all(c.is_integer for c in sp.Poly(num, P, Q).coeffs() + sp.Poly(den, P, Q).coeffs())
        items.append((Z, path, lf, sp.lambdify((P, Q), num, modules='math'), sp.lambdify((P, Q), den, modules='math'), sp.factor(num / den)))
t0 = time.time(); nev = 0; hits = []; denzero = 0
for (p, q) in pairs:
    for Z, path, lf, fn, fd, expr in items:
        if any(sg * lam(F)(p, q) < 0 for F, sg in path): continue          # the pair is not in this branch
        n_, d_ = fn(p, q), fd(p, q); nev += 1
        if d_ == 0: denzero += 1; continue
        if n_ % d_ == 0: hits.append((p, q, sorted(Z), lf.get('kind'), str(expr)))
print(f"piece {piece}: {len(items)} leaves of category N, {len(pairs)} prime pairs ({fixedname} < {FMAX}), {nev} evaluations of D/k; zero denominators {denzero}; INTEGER VALUES {len(hits)}   [{time.time() - t0:.0f} s]")
for h in hits[:10]: print("    INTEGER:", h)
if '-v' in sys.argv:
    seen = set()
    for Z, path, lf, fn, fd, expr in items:
        key = (str(expr), lf.get('kind'))
        if key in seen: continue
        seen.add(key); print("   ", lf.get('kind'), "| D/k =", expr)
