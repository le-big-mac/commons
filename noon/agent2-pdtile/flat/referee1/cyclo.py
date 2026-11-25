"""Referee's own helpers: cyclotomic polynomials and remainders, exact integer arithmetic.
Written from scratch; does not import anything from the author's folder."""
import cmath
import math
from functools import lru_cache

import numpy as np


def divisors(n):
    return [k for k in range(1, n + 1) if n % k == 0]


def phi(n):
    return sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)


def poly_mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return out


def poly_divexact_monic(num, den):
    """num / den for monic den, coefficients low->high; asserts zero remainder."""
    num = list(num)
    dn = len(den) - 1
    assert den[-1] == 1
    q = [0] * (len(num) - dn)
    for k in range(len(num) - 1, dn - 1, -1):
        c = num[k]
        q[k - dn] = c
        if c:
            for j, y in enumerate(den):
                num[k - dn + j] -= c * y
    assert all(v == 0 for v in num), "non-exact division"
    return q


@lru_cache(maxsize=None)
def cyclotomic(d):
    """Phi_d as a tuple of integer coefficients, low degree first."""
    num = [-1] + [0] * (d - 1) + [1]  # X^d - 1
    den = [1]
    for k in divisors(d):
        if k < d:
            den = poly_mul(den, list(cyclotomic(k)))
    q = poly_divexact_monic(num, den)
    assert len(q) - 1 == phi(d)
    # numerical self-check: vanishes at primitive d-th roots, not at the others
    for k in range(d):
        z = cmath.exp(2j * cmath.pi * k / d)
        val = sum(c * z ** i for i, c in enumerate(q))
        if math.gcd(k, d) == 1:
            assert abs(val) < 1e-7, (d, k, val)
        else:
            assert abs(val) > 1e-7, (d, k, val)
    return tuple(q)


@lru_cache(maxsize=None)
def _xpow_table(M, d):
    ph = cyclotomic(d)
    n = len(ph) - 1
    T = np.zeros((M, n), dtype=np.int64)
    cur = [0] * n
    if n == 0:
        return T
    cur[0] = 1
    for x in range(M):
        T[x] = cur
        top = cur[-1]
        nxt = [0] + cur[:-1]
        if top:
            for j in range(n):
                nxt[j] -= top * ph[j]
        cur = nxt
    return T


def xpow_table(M, d):
    """T[x] = coefficient vector of (X^x mod Phi_d), x = 0..M-1."""
    return _xpow_table(M, d)


def divides_exact(A, M, d):
    """Phi_d | A(X) for the set/multiset A (iterable of residues mod M), exact."""
    assert M % d == 0
    T = xpow_table(M, d)
    return not np.any(T[np.asarray(list(A), dtype=np.int64) % M].sum(axis=0))


def divides_numeric(A, d, tol=1e-8):
    """Independent floating-point test: A vanishes at every primitive d-th root of unity."""
    A = np.asarray(list(A), dtype=np.float64)
    for k in range(d):
        if math.gcd(k, d) == 1:
            if abs(np.exp(2j * np.pi * k * A / d).sum()) > tol:
                return False
    return True


def zero_set(A, M):
    return [d for d in divisors(M) if d > 1 and divides_exact(A, M, d)]


def rank_mod(Mat, P=2147483629):
    """Rank of an integer matrix over GF(P) (a lower bound for the rank over Q)."""
    A = np.array(Mat, dtype=np.int64) % P
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        if r == rows:
            break
        piv = None
        nz = np.nonzero(A[r:, c])[0]
        if len(nz) == 0:
            continue
        piv = r + nz[0]
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), P - 2, P)
        A[r] = (A[r] * inv) % P
        below = np.nonzero(A[:, c])[0]
        below = below[below != r]
        if len(below):
            f = A[below, c][:, None]
            A[below] = (A[below] - (f * A[r][None, :]) % P) % P
        r += 1
    return r


if __name__ == "__main__":
    # tiny self-test
    assert cyclotomic(1) == (-1, 1)
    assert cyclotomic(6) == (1, -1, 1)
    assert cyclotomic(12) == (1, 0, -1, 0, 1)
    assert zero_set(range(12), 144) == [2, 3, 4, 6, 12]
    assert zero_set(range(0, 144, 12), 144) == [d for d in divisors(144) if 12 % d != 0]
    for d in divisors(144)[1:]:
        for A in (range(12), range(0, 144, 12), [0, 1, 5, 77, 100]):
            assert divides_exact(A, 144, d) == divides_numeric(A, d)
    print("cyclo self-test ok")
