"""Referee's own tools (exact integer arithmetic) for limits.md.
Cyclotomic polynomials by division, X^b mod Phi_d as integer vectors, counts of bad signings with multiplicities
(the largest block is solved for, the others are listed), K_pi(D), and a brute force over all signings that tests
S(zeta_d) = 0 in floating point (a different road from the reduction, used as a cross-check for small m)."""
import itertools, math, cmath
from fractions import Fraction
import numpy as np

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]

def polydiv_exact(num, den):
    num = num[:]; q = [0] * (len(num) - len(den) + 1)
    for i in range(len(q) - 1, -1, -1):
        c = num[i + len(den) - 1] // den[-1]
        q[i] = c
        if c:
            for j, dj in enumerate(den): num[i + j] -= c * dj
    assert not any(num), "inexact division"
    return q

_PHI = {}
def phi_poly(d):
    """coefficients of Phi_d, lowest degree first"""
    if d not in _PHI:
        p = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d: p = polydiv_exact(p, phi_poly(e))
        _PHI[d] = p
    return _PHI[d]

_RED = {}
def red(d):
    """integer matrix phi(d) x d: column b is X^b mod Phi_d"""
    if d not in _RED:
        P = phi_poly(d); deg = len(P) - 1
        v = [0] * deg; v[0] = 1
        cols = []
        for b in range(d):
            cols.append(v[:])
            top = v[-1]; w = [0] + v[:-1]
            if top:
                for j in range(deg): w[j] -= top * P[j]
            v = w
        assert v == cols[0], "X^d is not 1 mod Phi_d"
        _RED[d] = np.array(cols, dtype=np.int64).T
        assert all(c == 0 for c in _RED[d][1:, 0]) and _RED[d][0, 0] == 1
    return _RED[d]

def c(r): return Fraction(1) if r <= 0 else Fraction(math.comb(r, r // 2), 2 ** r)

def merge(n, items):
    acc = {}
    for b, a in items:
        if a > 0: acc[b % n] = acc.get(b % n, 0) + a
    return sorted(acc.items())

def grid_blocks(items, maxblock=120000):
    """items: list of (b, a).  Yields (outer residues, outer sums, outer weight, inner residues, S (k x G), W (G, object))."""
    k = len(items)
    grids = [np.arange(-a, a + 1, 2, dtype=np.int64) for _, a in items]
    wts = [[math.comb(a, j) for j in range(a + 1)] for _, a in items]
    split = k; prod = 1
    while split > 0 and prod * len(grids[split - 1]) <= maxblock:
        split -= 1; prod *= len(grids[split])
    if split < k:
        S = np.array(np.meshgrid(*grids[split:], indexing='ij')).reshape(k - split, -1)
        W = np.array([1], dtype=object)
        for i in range(split, k): W = np.multiply.outer(W, np.array(wts[i], dtype=object)).reshape(-1)
    else:
        S = np.zeros((0, 1), dtype=np.int64); W = np.array([1], dtype=object)
    inner_res = [items[i][0] for i in range(split, k)]; outer_res = [items[i][0] for i in range(split)]
    for idx in itertools.product(*[range(len(grids[i])) for i in range(split)]):
        ow = 1
        for i, j in enumerate(idx): ow *= wts[i][j]
        yield outer_res, [int(grids[i][j]) for i, j in enumerate(idx)], ow, inner_res, S, W

def _values(n, divs, outer_res, outer_s, inner_res, S):
    """for each d in divs: (ok, v) with ok[g] true iff sum s_i X^(b_i) + v is 0 mod Phi_d for the integer v[g]"""
    out = []
    G = S.shape[1]
    for d in divs:
        M = red(d)
        g = np.zeros((M.shape[0], G), dtype=np.int64)
        if inner_res: g += M[:, [b % d for b in inner_res]] @ S
        if outer_res: g += (M[:, [b % d for b in outer_res]] @ np.array(outer_s, dtype=np.int64))[:, None]
        ok = ~np.any(g[1:] != 0, axis=0) if M.shape[0] > 1 else np.ones(G, dtype=bool)
        out.append((ok, -g[0]))
    return out

def bad_count(n, items, divs=None):
    """exact number of signings bad at some d in divs (default: all divisors of n, 1 included); returns (count, m).
    items: (residue, multiplicity).  The block of largest multiplicity is moved to 0 and solved for."""
    items = merge(n, items)
    divs = divisors(n) if divs is None else divs
    hb, ha = max(items, key=lambda t: t[1])
    rest = [((b - hb) % n, a) for b, a in items if b != hb]
    m = ha + sum(a for _, a in rest)
    binom = np.array([math.comb(ha, j) for j in range(ha + 1)], dtype=object)
    total = 0
    for outer_res, outer_s, ow, inner_res, S, W in grid_blocks(rest):
        seen = []; sub = 0
        for ok, T in _values(n, divs, outer_res, outer_s, inner_res, S):
            valid = ok & (np.abs(T) <= ha) & ((T - ha) % 2 == 0)
            new = valid.copy()
            for (v2, T2) in seen: new &= ~(v2 & (T2 == T))
            seen.append((valid, T))
            if new.any():
                sub += int((W[new] * binom[(T[new] + ha) // 2]).sum())
        total += ow * sub
    return total, m

def share(n, items, divs=None):
    cnt, m = bad_count(n, items, divs)
    return Fraction(cnt, 2 ** m), m

def K(L, D):
    """D: list of residues (with repetition) on Z_L.  Returns (K_0, K_1): expected number of even / odd integer values."""
    items = merge(L, [(b, 1) for b in D]); r = len(D)
    tot = [0, 0]
    for outer_res, outer_s, ow, inner_res, S, W in grid_blocks(items):
        seen = []
        for ok, v in _values(L, divisors(L), outer_res, outer_s, inner_res, S):
            new = ok.copy()
            for (o2, v2) in seen: new &= ~(o2 & (v2 == v))
            seen.append((ok, v))
            for par in (0, 1):
                sel = new & ((v % 2) == par)
                if sel.any(): tot[par] += ow * int(W[sel].sum())
    return Fraction(tot[0], 2 ** r), Fraction(tot[1], 2 ** r)

def brute_share(n, xs, divs=None):
    """all 2^m signings; bad at d iff |S(exp(2 pi i/d))| < 1e-9.  Returns Fraction."""
    m = len(xs); divs = divisors(n) if divs is None else divs
    E = np.array(list(itertools.product((1, -1), repeat=m)), dtype=np.int8).T.astype(np.float64)
    bad = np.zeros(E.shape[1], dtype=bool)
    for d in divs:
        z = np.array([cmath.exp(2j * math.pi * (b % d) / d) for b in xs])
        bad |= np.abs(z @ E) < 1e-9
    return Fraction(int(bad.sum()), 2 ** m)
