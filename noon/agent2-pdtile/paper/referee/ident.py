"""Referee check of Lemma 'ident' (I0), (Ix), (Ixy), (Cxy) of weak-pqr.tex.

Independent derivation from the definitions only:
  gamma_T = sum_{S subset T} mu_S          (T = set of coordinates that AGREE)
  Lambda_S = sum_{T superset S} mu_T prod_{i not in T} p_i
The gamma_T are the free symbols; mu is obtained by Moebius inversion.
Also: all coordinate permutations of the identities, and the 'group language'
claims (Lambda_S = fhat on class S; Poisson; pairing with D (x) delta_0) for
concrete primes.
"""
import itertools
import sympy as sp

coords = ('x', 'y', 'z')
subsets = [frozenset(c) for r in range(4) for c in itertools.combinations(coords, r)]
p = {c: sp.Symbol('p_' + c, positive=True) for c in coords}
g = {T: sp.Symbol('g_' + (''.join(sorted(T)) or '0')) for T in subsets}

# Moebius inversion on the Boolean lattice
mu = {S: sum((-1) ** (len(S) - len(R)) * g[R] for R in subsets if R <= S) for S in subsets}
for T in subsets:  # sanity: gamma_T = sum_{S<=T} mu_S
    assert sp.expand(sum(mu[S] for S in subsets if S <= T) - g[T]) == 0

def Lam(S):
    S = frozenset(S)
    return sum(mu[T] * sp.Mul(*[p[i] for i in coords if i not in T]) for T in subsets if S <= T)

def G(s):
    return g[frozenset(s)]

M = p['x'] * p['y'] * p['z']

def I0():
    lhs = M * G('xyz')
    rhs = sum(sp.Mul(*[(p[i] - 1) for i in S]) * Lam(S) for S in subsets)
    return sp.expand(lhs - rhs)

def Ix(x, y, z):
    lhs = p[y] * p[z] * (G('xyz') + (p[x] - 1) * G(y + z))
    rhs = Lam('') + (p[y] - 1) * Lam(y) + (p[z] - 1) * Lam(z) + (p[y] - 1) * (p[z] - 1) * Lam(y + z)
    return sp.expand(lhs - rhs)

def Ixy(x, y, z):
    lhs = p[z] * (G('xyz') + (p[x] - 1) * G(y + z) + (p[y] - 1) * G(x + z) + (p[x] - 1) * (p[y] - 1) * G(z))
    rhs = Lam('') + (p[z] - 1) * Lam(z)
    return sp.expand(lhs - rhs)

def Cxy(x, y, z):
    lhs = p[z] * (p[x] * G('xyz') + (p[y] - p[x]) * G(x + z) + (p[x] * p[y] - p[y]) * G(z))
    rhs = (Lam('') + (p[z] - 1) * Lam(z) + (p[x] - 1) * Lam(x + y)
           + (p[x] - 1) * (p[z] - 1) * Lam(x + y + z))
    return sp.expand(lhs - rhs)

print('(I0)  residual:', I0())
for perm in itertools.permutations(coords):
    print('perm', perm, ' (Ix):', Ix(*perm), ' (Ixy):', Ixy(*perm), ' (Cxy):', Cxy(*perm))

# --- 'group language' parenthetical, checked numerically for (px,py,pz)=(2,3,5),(3,2,5),(5,3,2)
import cmath, random
def fhat_check(px, py, pz):
    random.seed(1)
    gam = {T: random.randint(0, 9) for T in subsets}
    def f(v):
        return gam[frozenset(c for c, t in zip(coords, v) if t == 0)]
    P = (px, py, pz)
    pts = list(itertools.product(range(px), range(py), range(pz)))
    def chi(s, v):
        return cmath.exp(2j * cmath.pi * sum(si * vi / pi for si, vi, pi in zip(s, v, P)))
    subs = {c: n for c, n in zip(coords, P)}
    vals = {g[T]: gam[T] for T in subsets}
    vals.update({p[c]: subs[c] for c in coords})
    worst = 0
    for s in pts:
        S = frozenset(c for c, t in zip(coords, s) if t != 0)
        fh = sum(f(v) * chi(s, v) for v in pts)
        worst = max(worst, abs(fh - complex(Lam(S).subs(vals))))
    return worst
for P in [(2, 3, 5), (3, 2, 5), (5, 3, 2)]:
    print('fhat(chi of class S) = Lambda_S, max error for sizes', P, ':', fhat_check(*P))

# D (x) delta_0: D>=0 on X x Y, D(0,0)=1, row sums py/px (row = fixed x), column sums 1.
def D_check(px, py):
    d1 = sp.Rational(py - px, px * (py - 1))      # D(0,y), y != 0
    c = sp.Rational(py, px * (py - 1))            # D(x,y), x,y != 0
    D = [[(1 if (a, b) == (0, 0) else 0 if b == 0 else d1 if a == 0 else c) for b in range(py)] for a in range(px)]
    rows = {sum(r) for r in D}
    cols = {sum(D[a][b] for a in range(px)) for b in range(py)}
    nonneg = all(e >= 0 for r in D for e in r)
    pairing = G('xyz') + sum(D[0][b] for b in range(1, py)) * G('xz') + sum(D[a][0] for a in range(1, px)) * G('yz') \
        + sum(D[a][b] for a in range(1, px) for b in range(1, py)) * G('z')
    lhs = (p['z'] * (p['x'] * G('xyz') + (p['y'] - p['x']) * G('xz') + (p['x'] * p['y'] - p['y']) * G('z'))).subs({p['x']: px, p['y']: py})
    return rows, cols, nonneg, sp.expand(px * p['z'] * pairing - lhs)
for (px, py) in [(2, 3), (3, 5), (2, 7), (3, 2), (5, 3)]:
    print('D for (px,py)=', (px, py), ' row sums, col sums, D>=0, px*pz*<f,D(x)delta0> - LHS(Cxy):', D_check(px, py))
