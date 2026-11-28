"""Own routines for the tests of result.md (exact integer arithmetic; nothing imported from the other folders).
A multiset on Z_n is a list of items (b, a): the element b with multiplicity a.  The signed sum s of the a copies takes
the values -a, -a+2, ..., a with weights C(a, (a+s)/2); a grid point is a vector of such sums, its weight the product."""
import math, itertools
from fractions import Fraction
import numpy as np

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def factor(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def mobius(n):
    f = factor(n)
    return 0 if any(e > 1 for e in f.values()) else (-1) ** len(f)
def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i + j] += x * y
    return r
def pdiv_exact(a, b):                       # a / b, b monic, coefficients low -> high
    a = list(a); q = [0] * (len(a) - len(b) + 1)
    for i in range(len(q) - 1, -1, -1):
        q[i] = a[i + len(b) - 1]
        if q[i]:
            for j, y in enumerate(b): a[i + j] -= q[i] * y
    assert not any(a)
    return q
def cyclo(d):                               # Phi_d, coefficients low -> high
    num = [1]; den = [1]
    for e in divisors(d):
        mu = mobius(d // e)
        if mu == 0: continue
        f = [-1] + [0] * (e - 1) + [1]
        if mu == 1: num = pmul(num, f)
        else: den = pmul(den, f)
    return pdiv_exact(num, den)
_red = {}
def red(d):
    """phi(d) x d integer matrix: column x = coefficients of X^x modulo Phi_d."""
    if d in _red: return _red[d]
    phi = cyclo(d); k = len(phi) - 1
    M = np.zeros((k, d), dtype=np.int64)
    r = [1] + [0] * (k - 1) if k >= 1 else []
    for x in range(d):
        M[:, x] = r
        top = r[-1]; r = [0] + r[:-1]       # times X
        if top:
            for i in range(k): r[i] -= top * phi[i]
    _red[d] = M
    return M
def c(r):
    """c_r = C(r, floor(r/2)) / 2^r, and 1 for r <= 0."""
    return Fraction(1) if r <= 0 else Fraction(math.comb(r, r // 2), 2 ** r)
def grid(items):
    """sums (k x G int64), weights (G python ints), m."""
    gs = [np.arange(-a, a + 1, 2, dtype=np.int64) for _, a in items]
    S = np.array(np.meshgrid(*gs, indexing='ij')).reshape(len(items), -1)
    W = np.array([1], dtype=object)
    for (_, a), g in zip(items, gs):
        w = np.array([math.comb(a, (a + int(s)) // 2) for s in g], dtype=object)
        W = np.multiply.outer(W, w).reshape(-1)
    return S, W, sum(a for _, a in items)
def bad_mask(d, items, S):
    """boolean over grid points: the signed mask vanishes at the roots of unity of order d."""
    M = red(d)[:, [b % d for b, _ in items]]; G = S.shape[1]; out = np.empty(G, dtype=bool)
    step = max(1, 4_000_000 // max(1, M.shape[0]))
    for i in range(0, G, step):
        out[i:i + step] = ~np.any(M @ S[:, i:i + step] != 0, axis=0)
    return out
def live_levels(p, a, elems):
    """the live levels i (1..a) of the p-tree of the set of elements: some class modulo p^(i-1) has all p subclasses."""
    out = []
    for i in range(1, a + 1):
        sub = {}
        for b in elems: sub.setdefault(b % p ** (i - 1), set()).add(b % p ** i)
        if any(len(s) == p for s in sub.values()): out.append(i)
    return out
def fully_live(d, elems):
    """None if d is not fully live for the set of elements; else dict p -> rank j_p(d).  From the definition:
    cells = classes modulo d0 = d / rad(d); a cell is p-full if k_b = (b mod d - c)/d0 covers all residues modulo p."""
    f = factor(d); g = 1
    for p in f: g *= p
    d0 = d // g
    cells = {}
    for b in elems: cells.setdefault(b % d0, []).append(((b % d) - (b % d0)) // d0)
    for p in f:
        if not any(len({k % p for k in ks}) == p for ks in cells.values()): return None
    ranks = {}
    for p, a in f.items():
        ll = live_levels(p, a, elems)
        assert a in ll
        ranks[p] = len(ll)
    return ranks
def kappa(ranks):
    return max((j - 1) * (p - 1) for p, j in ranks.items()) + max(ranks) - 1
def mu_star(ranks):
    return max(j * (p - 1) for p, j in ranks.items())
