"""Referee's own helpers (written from scratch; nothing imported from the author's scripts).

Exact integer arithmetic only: cyclotomic polynomials by exact division, residues X^i mod Phi_d.
"""
import numpy as np


def divisors(M):
    return [d for d in range(1, M + 1) if M % d == 0]


def poly_divexact(a, b):
    """a / b for integer coefficient lists (low -> high), b monic; asserts zero remainder."""
    a = list(a)
    db = len(b) - 1
    assert b[-1] == 1
    out = [0] * (len(a) - db)
    for k in range(len(a) - 1, db - 1, -1):
        c = a[k]
        if c:
            out[k - db] = c
            for t in range(db + 1):
                a[k - db + t] -= c * b[t]
    assert all(v == 0 for v in a), "inexact division"
    return out


_cyc = {}


def cyclo(d):
    """Phi_d as a list of Python ints, low -> high."""
    if d in _cyc:
        return _cyc[d]
    a = [-1] + [0] * (d - 1) + [1]  # X^d - 1
    for e in divisors(d):
        if e < d:
            a = poly_divexact(a, cyclo(e))
    _cyc[d] = a
    return a


def residues(M, d):
    """Rows i = 0..M-1: coefficients of X^i mod Phi_d (integers), shape (M, phi(d))."""
    phi = cyclo(d)
    deg = len(phi) - 1
    rows = []
    cur = [0] * deg
    cur[0] = 1 if deg > 0 else 0
    for i in range(M):
        rows.append(list(cur))
        # multiply by X and reduce
        top = cur[-1]
        cur = [0] + cur[:-1]
        if top:
            for t in range(deg):
                cur[t] -= top * phi[t]
    return rows


def zero_set_exact(M, A):
    """Set of d | M, d > 1 with Phi_d | A(X), by exact integer remainder. A: iterable of residues mod M."""
    Z = set()
    A = sorted(set(x % M for x in A))
    for d in divisors(M):
        if d == 1:
            continue
        R = residues(M, d)
        deg = len(R[0])
        tot = [0] * deg
        for x in A:
            r = R[x]
            for t in range(deg):
                tot[t] += r[t]
        if all(v == 0 for v in tot):
            Z.add(d)
    return Z


def EF_from_zero_set(Z, p, n, q):
    E = frozenset(l for l in range(1, n + 1) if p ** l in Z)
    F = frozenset(l for l in range(0, n + 1) if p ** l * q in Z)
    return E, F


def crt_table(p, n, q):
    """x -> (u, w) and inverse dict."""
    M = p ** n * q
    fwd = [(x % p ** n, x % q) for x in range(M)]
    inv = {uw: x for x, uw in enumerate(fwd)}
    assert len(inv) == M
    return fwd, inv


def subset_sum_table(rows, dtype):
    """rows: (k, K) integer array. Returns T of shape (2^k, K) with T[m] = sum of rows[i] over bits i of m."""
    rows = np.asarray(rows)
    K = rows.shape[1]
    T = np.zeros((1, K), dtype=dtype)
    for r in rows:
        T = np.concatenate([T, T + r.astype(dtype)], axis=0)
    return T


def popcount8(a):
    a = a.astype(np.uint16)
    c = np.zeros(a.shape, dtype=np.uint8)
    for b in range(16):
        c += ((a >> b) & 1).astype(np.uint8)
    return c
