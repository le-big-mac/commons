# Referee's brute force: exact integer arithmetic, all signings (first sign fixed +1; every event tested is
# invariant under negating all signs, so shares are counts / 2^(m-1)).
# "bad at d" is tested as: the remainder of the signed mask modulo Phi_d is the zero polynomial.
import numpy as np
from fractions import Fraction as Fr
from math import comb

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

def factor(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def polydivexact(a, b):
    # a / b for integer polynomials (lists, low degree first), b monic, exact division
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        q[i] = a[i + len(b) - 1]
        for j, bj in enumerate(b):
            a[i + j] -= q[i] * bj
    assert all(x == 0 for x in a)
    return q

_cyc = {}
def cyclo(d):
    if d in _cyc: return _cyc[d]
    p = [-1] + [0] * (d - 1) + [1]      # X^d - 1
    for e in divisors(d):
        if e < d:
            p = polydivexact(p, cyclo(e))
    _cyc[d] = p
    return p

_pt = {}
def powtable(n, d):
    # rows: X^b mod Phi_d, b = 0..n-1
    key = (n, d)
    if key in _pt: return _pt[key]
    phi = cyclo(d); deg = len(phi) - 1
    T = np.zeros((n, deg), dtype=np.int64)
    cur = [0] * deg
    if deg >= 1:
        cur[0] = 1
    else:
        raise ValueError
    for b in range(n):
        T[b] = cur
        # multiply by X and reduce
        top = cur[-1]
        cur = [0] + cur[:-1]
        if top:
            for j in range(deg):
                cur[j] -= top * phi[j]
    # X^n mod Phi_d must be 1
    one = [0] * deg; one[0] = 1
    assert cur == one
    _pt[key] = T
    return T

_sg = {}
def signs(m):
    if m in _sg: return _sg[m]
    S = np.ones((2 ** (m - 1), m), dtype=np.int64)
    idx = np.arange(2 ** (m - 1))
    for j in range(1, m):
        S[:, j] = 1 - 2 * ((idx >> (j - 1)) & 1)
    _sg[m] = S
    return S

def bad_events(n, Bs):
    """Bs: K x m integer array of residues mod n. Returns dict d -> K x 2^(m-1) boolean array 'bad at d'."""
    Bs = np.asarray(Bs, dtype=np.int64) % n
    K, m = Bs.shape
    S = signs(m)
    out = {}
    for d in divisors(n):
        T = powtable(n, d)[Bs]              # K x m x phi
        R = np.einsum('sm,kmf->ksf', S, T, optimize=True)
        out[d] = ~R.any(axis=2)
    return out

def largest_prime(d):
    return max(factor(d)) if d > 1 else 1

def vp(d, p):
    k = 0
    while d % p == 0:
        d //= p; k += 1
    return k

def tree_levels(n, B, q):
    """for prime q | n: dict level i -> list of (sizes of the q subclasses (occupied ones, sorted desc), full?, group size)"""
    a = vp(n, q)
    res = {}
    for i in range(1, a + 1):
        groups = {}
        for b in B:
            groups.setdefault(b % q ** (i - 1), {}).setdefault(b % q ** i, 0)
            groups[b % q ** (i - 1)][b % q ** i] += 1
        res[i] = [(tuple(sorted(g.values(), reverse=True)), len(g) == q) for g in groups.values()]
    return res
