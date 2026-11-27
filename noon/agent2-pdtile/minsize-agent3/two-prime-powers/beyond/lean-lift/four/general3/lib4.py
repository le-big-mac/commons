"""Common code for the tests of sign-four-result.md.  Exact integer arithmetic throughout.

Written from the definitions; nothing is imported from the earlier programs.
"""
from fractions import Fraction as Fr
from math import comb
import numpy as np


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


def divisors(n):
    ds = [1]
    for p, a in factor(n).items():
        ds = [d * p ** e for d in ds for e in range(a + 1)]
    return sorted(ds)


def mu(d):
    """max over primes p | d of v_p(d) * (p - 1); 0 for d = 1"""
    return max([a * (p - 1) for p, a in factor(d).items()], default=0)


_cyc = {}


def cyclotomic(d):
    """coefficients of Phi_d, lowest first (python ints)"""
    if d in _cyc:
        return _cyc[d]
    # X^d - 1 divided by the Phi_e, e | d, e < d
    num = [-1] + [0] * (d - 1) + [1]
    for e in divisors(d):
        if e < d:
            den = cyclotomic(e)
            # exact division of num by monic den
            q = [0] * (len(num) - len(den) + 1)
            num = num[:]
            for i in range(len(q) - 1, -1, -1):
                c = num[i + len(den) - 1]
                q[i] = c
                if c:
                    for j, dj in enumerate(den):
                        num[i + j] -= c * dj
            assert all(v == 0 for v in num)
            num = q
    _cyc[d] = num
    return num


_pow = {}


def powers_mod_phi(d):
    """array R of shape (d, phi(d)): row x = X^x mod Phi_d (exact integers)"""
    if d in _pow:
        return _pow[d]
    phi = cyclotomic(d)
    deg = len(phi) - 1
    low = np.array(phi[:-1], dtype=np.int64)
    R = np.zeros((d, deg), dtype=np.int64)
    r = np.zeros(deg, dtype=np.int64)
    if deg == 0:
        _pow[d] = R
        return R
    r[0] = 1
    for x in range(d):
        R[x] = r
        top = r[-1]
        r = np.roll(r, 1)
        r[0] = 0
        if top:
            r = r - top * low
    _pow[d] = R
    return R


def all_signs(m, fix_first=True):
    """matrix of all sign vectors (first sign +1 if fix_first), shape (2^(m-1) or 2^m, m), int64"""
    k = m - 1 if fix_first else m
    idx = np.arange(1 << k, dtype=np.int64)
    E = np.ones((1 << k, m), dtype=np.int64)
    off = 1 if fix_first else 0
    for j in range(k):
        E[:, j + off] = 1 - 2 * ((idx >> j) & 1)
    return E


def bad_table(B, n, E):
    """dict d -> boolean array over the rows of E: Phi_d divides the signed mask"""
    out = {}
    Barr = np.array(B, dtype=np.int64)
    for d in divisors(n):
        if d == 1:
            out[d] = (E.sum(axis=1) == 0)
            continue
        R = powers_mod_phi(d)
        M = R[Barr % d]                 # (m, phi(d))
        V = E @ M
        out[d] = ~V.any(axis=1)
    return out


# ---------- trees, fullness, contraction

def digits(x, p, a):
    return [(x // p ** i) % p for i in range(a)]


def full_levels(B, n):
    """dict p -> list over levels t = 1..a of True if some group at level t has all p subclasses occupied"""
    res = {}
    for p, a in factor(n).items():
        lv = []
        for t in range(1, a + 1):
            groups = {}
            for x in B:
                groups.setdefault(x % p ** (t - 1), set()).add((x // p ** (t - 1)) % p)
            lv.append(any(len(s) == p for s in groups.values()))
        res[p] = lv
    return res


def all_full(B, n):
    return all(all(v) for v in full_levels(B, n).values())


def crt(residues):
    """residues: list of (r, modulus), pairwise coprime moduli -> (x, M)"""
    x, M = 0, 1
    for r, q in residues:
        # solve x + M*k = r mod q
        k = ((r - x) * pow(M, -1, q)) % q
        x += M * k
        M *= q
    return x, M


def contract(B, n):
    """canonical contraction (deepest level first, every prime): returns (B_flat, n_flat).
    Elements keep their order, so a signing of B is a signing of B_flat."""
    f = factor(n)
    dig = {p: [digits(x % p ** a, p, a) for x in B] for p, a in f.items()}
    for p, a in f.items():
        D = dig[p]
        t = a
        while t >= 1:
            groups = {}
            for dg in D:
                groups.setdefault(tuple(dg[:t - 1]), set()).add(dg[t - 1])
            if not any(len(s) == p for s in groups.values()):
                for dg in D:
                    del dg[t - 1]
            t -= 1
    nf = 1
    for p in f:
        nf *= p ** len(dig[p][0])
    Bf = []
    for k in range(len(B)):
        res = []
        for p in f:
            dg = dig[p][k]
            if dg:
                res.append((sum(v * p ** i for i, v in enumerate(dg)), p ** len(dg)))
        Bf.append(crt(res)[0] if res else 0)
    return Bf, nf


def c_even(m):
    return Fr(comb(m, m // 2), 2 ** m) if m % 2 == 0 else Fr(0)


# ---------- exact test of "Phi_d divides" by the slice criterion (for large n)

def vanishes(f, d):
    """f: dict x -> integer weight (x any integers); True iff sum f(x) zeta^x = 0 for zeta of order d (d odd).
    Lemma 1 of the note (slice criterion), applied prime by prime."""
    f = {x: w for x, w in f.items() if w}
    if d == 1:
        return sum(f.values()) == 0
    if not f:
        return True
    p = min(factor(d))
    i = factor(d)[p]
    d2 = d // p ** i
    # classes modulo p^(i-1); subclasses by the next digit; slices as functions of x mod d2
    groups = {}
    for x, w in f.items():
        g = groups.setdefault(x % p ** (i - 1), {})
        s = g.setdefault((x // p ** (i - 1)) % p, {})
        y = x % d2
        s[y] = s.get(y, 0) + w
    for g in groups.values():
        s0 = g.get(0, {})
        for j in range(1, p):
            sj = g.get(j, {})
            diff = dict(sj)
            for y, w in s0.items():
                diff[y] = diff.get(y, 0) - w
            if not vanishes(diff, d2):
                return False
    return True


def good_big(B, eps, n, divs=None):
    """True iff the signing eps of B is good on Z_n (exact, by the slice criterion)"""
    if divs is None:
        divs = divisors(n)
    for d in divs:
        f = {}
        for x, e in zip(B, eps):
            y = x % d
            f[y] = f.get(y, 0) + e
        if vanishes(f, d):
            return False
    return True
