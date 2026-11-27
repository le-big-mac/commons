"""Audit of the statements on signs: exact integer tools, written for this audit.

Polynomials are lists of Python integers, lowest coefficient first.  Phi_d is computed from
prod_{e | d} (X^e - 1)^{mobius(d/e)} by exact long division.  "Bad at d" (Phi_d divides sum_k sg_k X^{e_k}) is decided
for all 2^m signings at once from the table of the remainders of X^x modulo Phi_d (integer vectors of length phi(d)).
The definitions live, rank, IsPivot, mu, lhsN1 are transcribed literally from Pnq/SignDefs.lean (natural subtraction:
i - 1 is 0 for i = 0)."""
from fractions import Fraction
from functools import lru_cache
from math import comb
import numpy as np


def factor(n):
    f = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def divisors(n):
    ds = [1]
    for p, a in factor(n).items():
        ds = [d * p ** j for d in ds for j in range(a + 1)]
    return sorted(ds)


def mobius(n):
    f = factor(n)
    if any(a > 1 for a in f.values()):
        return 0
    return -1 if len(f) % 2 else 1


def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return r


def pdivmod(a, b):
    """long division of a by b, b with leading coefficient 1 or -1; returns (quotient, remainder)"""
    a = list(a)
    db = len(b) - 1
    lead = b[-1]
    assert lead in (1, -1)
    if len(a) - 1 < db:
        return [0], a
    q = [0] * (len(a) - db)
    for k in range(len(a) - db - 1, -1, -1):
        c = a[k + db] * lead
        q[k] = c
        if c:
            for j, y in enumerate(b):
                a[k + j] -= c * y
    return q, a[:db]


@lru_cache(None)
def cyclo(d):
    """coefficients of Phi_d, lowest first"""
    assert d >= 1
    num, den = [1], [1]
    for e in divisors(d):
        mu = mobius(d // e)
        if mu == 0:
            continue
        f = [-1] + [0] * (e - 1) + [1]
        if mu == 1:
            num = pmul(num, f)
        else:
            den = pmul(den, f)
    q, r = pdivmod(num, den)
    assert not any(r)
    return tuple(q)


@lru_cache(None)
def xtab(d):
    """row x (0 <= x < d): the coefficients of X^x modulo Phi_d"""
    phi = cyclo(d)
    deg = len(phi) - 1
    T = np.zeros((d, deg), dtype=np.int64)
    cur = [0] * deg
    cur[0] = 1
    for x in range(d + 1):
        if x == d:
            assert cur == [1] + [0] * (deg - 1), d      # X^d = 1 modulo Phi_d
            break
        T[x] = cur
        top = cur[-1]
        nxt = [0] + cur[:-1]
        if top:
            for j in range(deg):
                nxt[j] -= top * phi[j]
        cur = nxt
    return T


@lru_cache(None)
def signs(m):
    """all 2^m signings as rows of +1/-1; bit k of the row number set means element k has the sign +"""
    j = np.arange(2 ** m, dtype=np.int64)[:, None]
    return ((j >> np.arange(m)) & 1) * 2 - 1


def bad(e, d):
    """boolean vector over all signings: Phi_d divides sum_k sg_k X^{e_k}"""
    T = xtab(d)[np.array(e, dtype=np.int64) % d]
    return ~np.any(signs(len(e)) @ T, axis=1)


def bad_literal(e, sg, d):
    """the same for one signing, by building the polynomial and dividing it by Phi_d"""
    P = [0] * (max(e) + 1)
    for x, s in zip(e, sg):
        P[x] += s
    _, r = pdivmod(P, list(cyclo(d)))
    return not any(r)


# ---- the definitions of Pnq/SignDefs.lean, literally ----

def nsub1(i):
    return i - 1 if i >= 1 else 0


def nmod(x, M):
    """Lean's x % M on natural numbers: x % 0 = x"""
    return x if M == 0 else x % M


def live(e, p, i):
    q = p ** nsub1(i)
    M = p ** i
    occ = {nmod(x, M) for x in e}
    return any(all((c + t * q) in occ for t in range(p)) for c in range(q))


def rank(e, p, i):
    return sum(1 for j in range(1, i + 1) if live(e, p, j))


def is_pivot(e, p, i, J):
    """J: a collection of indices into e"""
    q = p ** nsub1(i)
    M = p ** i
    cls = [nmod(e[k], M) for k in J]
    if len(set(cls)) != len(cls):
        return False
    s = set(cls)
    # "for every c" in Lean ranges over all natural numbers, but only c % q occurs (q >= 1 for p >= 1)
    return all(any((c + t * q) not in s for t in range(p)) for c in range(q))


def mu(t):
    if t <= 1:
        return 0
    return max((p - 1) * a for p, a in factor(t).items())


def lhsN1(m, T):
    T = set(T)
    r = Fraction(comb(m, m // 2), 2 ** m) if m % 2 == 0 else Fraction(0)
    r += sum(Fraction(1, 2 ** mu(t)) for t in T)
    if m % 2 == 0 and 3 in T and 14 <= m:
        r -= Fraction(1, 16)
    return r
