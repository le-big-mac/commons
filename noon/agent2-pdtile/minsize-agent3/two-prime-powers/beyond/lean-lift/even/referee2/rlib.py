# rlib.py -- the referee's own library. Exact integer arithmetic.
# A signed multiset B = (b_1..b_m) on Z_n with signs eps has the mask S(X) = sum eps_k X^{b_k}.
# "bad at d"  : Phi_d | S, i.e. the remainder of S modulo Phi_d is 0.
# "3-bad at d": every coefficient of that remainder is divisible by 3 (this is S(zeta) in 3 Z[zeta],
#               because 1, zeta, ..., zeta^(phi(d)-1) is a Z-basis of Z[zeta]).
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np
from functools import lru_cache
from fractions import Fraction
from itertools import combinations_with_replacement


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


def vp(x, p):
    v = 0
    while x % p == 0:
        x //= p
        v += 1
    return v


def _divexact(num, den):
    # num, den integer coefficient lists (low to high), den monic; exact division
    num = list(num)
    dd = len(den) - 1
    q = [0] * (len(num) - dd)
    for i in range(len(num) - 1, dd - 1, -1):
        c = num[i]
        if c:
            q[i - dd] = c
            for j in range(dd + 1):
                num[i - dd + j] -= c * den[j]
    assert not any(num), "division not exact"
    return q


@lru_cache(None)
def cyclo(d):
    num = [-1] + [0] * (d - 1) + [1]
    for g in divisors(d):
        if g < d:
            num = _divexact(num, cyclo(g))
    return tuple(num)


@lru_cache(None)
def powtable(d):
    # row b: coefficients of X^b mod Phi_d, b = 0..d-1 (int32 array d x phi(d))
    phi = cyclo(d)
    deg = len(phi) - 1
    T = np.zeros((d, deg), dtype=np.int64)
    cur = [0] * deg
    cur[0] = 1
    for b in range(d):
        T[b] = cur
        c = cur[-1]
        cur = [0] + cur[:-1]
        if c:
            cur = [cur[i] - c * phi[i] for i in range(deg)]
    assert np.abs(T).max() < 2 ** 20
    return T.astype(np.int32)


@lru_cache(None)
def signs(m, half=True):
    # all sign vectors (first sign + if half), as int32 array S x m
    k = m - 1 if half else m
    S = 1 << k
    a = np.ones((S, m), dtype=np.int32)
    idx = np.arange(S)
    for i in range(k):
        col = m - 1 - i
        a[:, col] = 1 - 2 * ((idx >> i) & 1)
    return a


def residues(B, d, half=True):
    # B: list of m residues; returns array S x phi(d): remainders of all signed masks modulo Phi_d
    T = powtable(d)
    M = T[np.asarray(B) % d]            # m x phi
    return signs(len(B), half) @ M


def bad_at(B, d, half=True):
    R = residues(B, d, half)
    return ~R.any(axis=1)


def bad3_at(B, d, half=True):
    R = residues(B, d, half)
    return ~(R % 3).any(axis=1)


def good_mask(B, n, half=True):
    # boolean array over the signings: good on Z_n
    S = signs(len(B), half).shape[0]
    g = np.ones(S, dtype=bool)
    for d in divisors(n):
        g &= ~bad_at(B, d, half)
        if not g.any():
            break
    return g


def good3_mask(B, n3, half=True):
    # boolean array over the signings: 3-good on Z_{n3} (3 must not divide n3)
    assert n3 % 3 != 0
    S = signs(len(B), half).shape[0]
    g = np.ones(S, dtype=bool)
    for d in divisors(n3):
        g &= ~bad3_at(B, d, half)
    return g


# ---- batch versions: E is an integer array N x m of residues ----------------------------------

def batch_res(E, d, half=True):
    # returns N x S x phi(d)
    T = powtable(d)
    M = T[E % d]                         # N x m x phi
    Sg = signs(E.shape[1], half)         # S x m
    return np.einsum('sm,nmf->nsf', Sg, M, optimize=True)


def batch_bad(E, d, half=True):
    return ~batch_res(E, d, half).any(axis=2)          # N x S


def batch_bad3(E, d, half=True):
    return ~(batch_res(E, d, half) % 3).any(axis=2)    # N x S


def multisets(n, m, with0=False):
    if with0:
        for c in combinations_with_replacement(range(n), m - 1):
            yield (0,) + c
    else:
        yield from combinations_with_replacement(range(n), m)


def chunks(it, size):
    buf = []
    for x in it:
        buf.append(x)
        if len(buf) == size:
            yield np.array(buf, dtype=np.int64)
            buf = []
    if buf:
        yield np.array(buf, dtype=np.int64)


# ---- trees -----------------------------------------------------------------------------------

def live_levels(B, p, a):
    # list of the levels i in 1..a of the p-tree of B (on Z_{p^a * rest}) that are live:
    # some class modulo p^(i-1) has all its p subclasses modulo p^i occupied
    out = []
    for i in range(1, a + 1):
        occ = {}
        for b in set(x % (p ** i) for x in B):
            occ.setdefault(b % (p ** (i - 1)), set()).add(b)
        if any(len(s) == p for s in occ.values()):
            out.append(i)
    return out


def is_exceptional(B, n):
    if len(B) != 2:
        return False
    k = vp(n, 2)
    return (B[0] - B[1]) % (2 ** k) != 0


def frac(a, b):
    return Fraction(int(a), int(b))
