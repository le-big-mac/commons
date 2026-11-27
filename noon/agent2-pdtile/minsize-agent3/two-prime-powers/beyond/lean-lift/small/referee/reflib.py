"""Referee's tools (exact integer arithmetic), written without reading the author's test programs' logic.

good signing of a multiset B on Z_n  :=  the signed mask S(X) = sum of (+-1) X^x is divisible by no Phi_d, d | n.

Two exact tests are provided and compared with each other in ref_selftest.py:
  good_plain : S as a dense integer polynomial of degree < n, long division by Phi_d for every d | n (the definition).
  good_all   : for every d | n the remainder of S modulo Phi_d, computed as  sum of signs * (X^(x mod d) mod Phi_d),
               for all 2^(m-1) signings at once (the first element keeps +; a global change of sign changes nothing).
"""
import numpy as np
from functools import lru_cache
from itertools import product


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def factor(n):
    f = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def poly_divmod(f, g):
    """f, g integer lists, low degree first, g monic.  Returns (quotient, remainder)."""
    f = list(f)
    dg = len(g) - 1
    q = [0] * max(0, len(f) - dg)
    for i in range(len(f) - 1, dg - 1, -1):
        c = f[i]
        if c:
            q[i - dg] = c
            for j in range(dg + 1):
                f[i - dg + j] -= c * g[j]
    return q, f[:dg]


@lru_cache(None)
def cyclo(d):
    """Phi_d as a tuple of integers, low degree first: (X^d - 1) divided by Phi_e for all e | d, e < d."""
    f = [-1] + [0] * (d - 1) + [1]
    for e in divisors(d):
        if e < d:
            f, r = poly_divmod(f, list(cyclo(e)))
            assert not any(r)
    return tuple(f)


@lru_cache(None)
def rem_matrix(d):
    """(phi(d) x d) integer matrix whose column j is X^j modulo Phi_d."""
    phi = cyclo(d)
    k = len(phi) - 1
    R = np.zeros((k, d), dtype=np.int64)
    cur = [0] * k
    cur[0] = 1
    for j in range(d):
        R[:, j] = cur
        top = cur[-1]
        cur = [0] + cur[:-1]
        if top:
            for i in range(k):
                cur[i] -= top * phi[i]
    return R


@lru_cache(None)
def sign_matrix(m):
    """all sign vectors of length m with first entry +1, as rows."""
    rows = [(1,) + s for s in product((1, -1), repeat=m - 1)]
    return np.array(rows, dtype=np.int64)


def good_all(n, elems):
    """boolean vector over the rows of sign_matrix(len(elems)): is the signing good on Z_n ?"""
    m = len(elems)
    sg = sign_matrix(m)
    bad = np.zeros(len(sg), dtype=bool)
    for d in divisors(n):
        R = rem_matrix(d)
        cols = R[:, [x % d for x in elems]]            # phi(d) x m
        V = sg @ cols.T                                 # signings x phi(d): remainders modulo Phi_d
        bad |= ~V.any(axis=1)
    return ~bad


def bad_levels(n, elems, signs):
    """the divisors d of n with Phi_d | signed mask (remainder method)."""
    out = []
    sv = np.array(signs, dtype=np.int64)
    for d in divisors(n):
        R = rem_matrix(d)
        v = R[:, [x % d for x in elems]] @ sv
        if not v.any():
            out.append(d)
    return out


def good_plain(n, elems, signs):
    """the definition: dense S, long division by Phi_d for every d | n."""
    S = [0] * n
    for x, s in zip(elems, signs):
        S[x % n] += s
    for d in divisors(n):
        q, r = poly_divmod(S, list(cyclo(d)))
        if not any(r):
            return False
    return True


def crt(r1, m1, r2, m2):
    """x mod m1*m2 with x = r1 mod m1, x = r2 mod m2 (m1, m2 coprime)."""
    if m1 == 1:
        return r2 % m2
    if m2 == 1:
        return r1 % m1
    inv = pow(m1, -1, m2)
    return (r1 + m1 * (((r2 - r1) * inv) % m2)) % (m1 * m2)


def contractible(elems, p, a, t):
    """level t of the p-tree (p^a || n): every class modulo p^(t-1) that holds an element has a class modulo p^t
    inside it that holds none."""
    occ = {}
    for x in elems:
        u = x % p ** a
        occ.setdefault(u % p ** (t - 1), set()).add((u // p ** (t - 1)) % p)
    return all(len(v) < p for v in occ.values())


def branches(elems, p, a, t):
    occ = {}
    for x in elems:
        u = x % p ** a
        occ.setdefault(u % p ** (t - 1), set()).add((u // p ** (t - 1)) % p)
    return any(len(v) >= 2 for v in occ.values())


def contract(elems, n, p, a, t):
    """delete the base-p digit of index t-1 of (x mod p^a); x mod n'' is kept.  Returns the list on Z_(n/p), in the
    same order (so that a signing of the one is a signing of the other)."""
    n2 = n // p ** a
    out = []
    for x in elems:
        u = x % p ** a
        w = x % n2
        low = u % p ** (t - 1)
        high = u // p ** t
        ub = low + p ** (t - 1) * high                   # in [0, p^(a-1))
        out.append(crt(ub, p ** (a - 1), w, n2))
    return out
