# Referee's own library (written from the definitions, not from prover/lib.py).
# Exact integer arithmetic.  "bad at d" is decided by the remainder of the signed mask modulo Phi_d.
import numpy as np
from functools import lru_cache
from math import gcd


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def factorint(n):
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


def phi(n):
    r = n
    for p in factorint(n):
        r = r // p * (p - 1)
    return r


def polydiv_exact(num, den):
    """num / den for integer polynomials (lists, low degree first), den monic; asserts remainder 0."""
    num = list(num)
    dd = len(den) - 1
    q = [0] * (len(num) - dd)
    for i in range(len(num) - 1, dd - 1, -1):
        c = num[i]
        if c:
            q[i - dd] = c
            for j in range(dd + 1):
                num[i - dd + j] -= c * den[j]
    assert all(v == 0 for v in num), "inexact division"
    return q


@lru_cache(maxsize=None)
def cyclo(d):
    """Phi_d as a tuple of integers, low degree first: (X^d - 1) divided by all Phi_d', d' | d, d' < d."""
    num = [-1] + [0] * (d - 1) + [1]
    for dd in divisors(d):
        if dd < d:
            num = polydiv_exact(num, cyclo(dd))
    assert len(num) - 1 == phi(d) and num[-1] == 1
    return tuple(num)


@lru_cache(maxsize=None)
def table(n, d):
    """int64 array T of shape (n, phi(d)): row x = X^x mod Phi_d."""
    P = cyclo(d)
    deg = len(P) - 1
    T = np.zeros((n, deg), dtype=np.int64)
    r = [0] * deg
    if deg == 0:
        return T
    r[0] = 1
    low = list(P[:-1])
    for x in range(n):
        T[x, :] = r
        top = r[-1]
        r = [0] + r[:-1]
        if top:
            for j in range(deg):
                r[j] -= top * low[j]
    return T


@lru_cache(maxsize=None)
def signmat(m, fix_first=False):
    """all sign vectors of length m as an int64 matrix of +-1; row index s has bit i set iff element i has sign -.
    With fix_first, only the rows with element 0 positive (bit 0 clear)."""
    idx = np.arange(1 << m, dtype=np.int64)
    if fix_first:
        idx = idx[(idx & 1) == 0]
    M = np.empty((len(idx), m), dtype=np.int64)
    for i in range(m):
        M[:, i] = 1 - 2 * ((idx >> i) & 1)
    return M


def bad_levels(B, n, ds=None, fix_first=False):
    """B: list of residues mod n.  Returns dict d -> boolean array over sign vectors (True = Phi_d | signed mask)."""
    m = len(B)
    S = signmat(m, fix_first)
    out = {}
    for d in (ds if ds is not None else divisors(n)):
        T = table(n, d)
        R = T[np.array(B, dtype=np.int64) % n, :]          # m x phi(d)
        V = S @ R
        out[d] = ~V.any(axis=1)
    return out


def bad_one(B, signs, n, d):
    """exact test for one signed multiset: Phi_d | sum signs[i] X^B[i] ?"""
    T = table(n, d)
    v = np.zeros(T.shape[1], dtype=np.int64)
    for x, s in zip(B, signs):
        v += s * T[x % n]
    return not v.any()


def bad_one_complex(B, signs, n, d, tol=1e-9):
    """floating check, for comparison only"""
    import cmath
    z = cmath.exp(2j * cmath.pi / d)
    return abs(sum(s * z ** (x % d) for x, s in zip(B, signs))) < tol


def multisets_with_zero(n, m):
    """all multisets of m elements of Z_n containing 0 (as sorted tuples starting with 0)."""
    from itertools import combinations_with_replacement
    for rest in combinations_with_replacement(range(n), m - 1):
        yield (0,) + rest


def v2(x):
    assert x != 0
    v = 0
    while x % 2 == 0:
        x //= 2
        v += 1
    return v


def split2(n):
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k, n


def is_exceptional_pair(B, n):
    k, _ = split2(n)
    return len(B) == 2 and (B[0] - B[1]) % (1 << k) != 0


# ---------- polynomials over F_2 as Python ints (bit i = coefficient of Y^i) ----------

def f2_deg(a):
    return a.bit_length() - 1


def f2_mod(a, f):
    df = f2_deg(f)
    while a and f2_deg(a) >= df:
        a ^= f << (f2_deg(a) - df)
    return a


def f2_mul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def f2_mulmod(a, b, f):
    return f2_mod(f2_mul(a, b), f)


def f2_powmod(a, e, f):
    r = 1
    a = f2_mod(a, f)
    while e:
        if e & 1:
            r = f2_mulmod(r, a, f)
        a = f2_mulmod(a, a, f)
        e >>= 1
    return r


def f2_inv(a, f):
    """inverse in F_2[Y]/(f), f irreducible of degree t: a^(2^t - 2)."""
    t = f2_deg(f)
    r = f2_powmod(a, (1 << t) - 2, f)
    assert f2_mulmod(r, a, f) == 1
    return r


def cyclo_mod2(e):
    P = cyclo(e)
    return sum(1 << i for i, c in enumerate(P) if c % 2)


def ord2(e):
    if e == 1:
        return 1
    t, x = 1, 2 % e
    while x != 1:
        x = x * 2 % e
        t += 1
    return t


@lru_cache(maxsize=None)
def factors_mod2(e):
    """the irreducible factors of Phi_e modulo 2 (e odd): all have degree ord_e(2); found by trial division by
    every polynomial of that degree with constant term 1.  Checked: product = Phi_e mod 2, number = phi(e)/ord."""
    assert e % 2 == 1
    F = cyclo_mod2(e)
    t = ord2(e)
    if e == 1:
        return (0b11,)
    fs = []
    for mid in range(1 << (t - 1)):
        g = (1 << t) | (mid << 1) | 1
        if f2_mod(F, g) == 0:
            fs.append(g)
    assert len(fs) == phi(e) // t, (e, len(fs))
    prod = 1
    for g in fs:
        prod = f2_mul(prod, g)
    assert prod == F
    return tuple(fs)


def f2_rank(vecs):
    """rank over F_2 of a list of ints (bit vectors)."""
    basis = []
    for v in vecs:
        for b in basis:
            v = min(v, v ^ b)
        if v:
            basis.append(v)
    return len(basis)


def D_rank(W, e):
    """D_e: the F_2-rank of the vectors Y^w mod (2, Phi_e), w in W (a list of residues, with repetitions allowed)."""
    F = cyclo_mod2(e)
    pw = powers_mod2(e)
    return f2_rank([pw[w % e] for w in W])


@lru_cache(maxsize=None)
def powers_mod2(e):
    F = cyclo_mod2(e)
    out = []
    r = f2_mod(1, F) if e > 1 else 1
    if e == 1:
        return (1,)       # Z[1]/2 = F_2, Y = 1
    for _ in range(e):
        out.append(r)
        r = f2_mod(r << 1, F)
    return tuple(out)


def live_level(W, p, i):
    """level i of the p-tree is live for the residues W: some class c mod p^(i-1) has all p subclasses mod p^i occupied."""
    occ = set(w % p ** i for w in W)
    q = p ** (i - 1)
    for c in range(q):
        if all((c + t * q) in occ for t in range(p)):
            return True
    return False


def live_levels(W, p, amax):
    return [i for i in range(1, amax + 1) if live_level(W, p, i)]
