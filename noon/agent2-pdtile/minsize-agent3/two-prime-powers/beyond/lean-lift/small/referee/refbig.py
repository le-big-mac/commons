"""Referee's exact test of 'good' for a signed multiset of few elements on Z_n with n very large (n given by its
factorisation), by exact division of integer polynomials.

For d | n put r = rad(d), e = d / r.  Then Phi_d(X) = Phi_r(X^e).  Reduce the signed mask S modulo X^d - 1 (Phi_d divides
X^d - 1) and split it by the residue c of the exponent modulo e:  S = sum_c X^c f_c(X^e), f_c of degree < r.  Because
Phi_r(X^e) is a polynomial in X^e,   Phi_d | S   iff   Phi_r(Y) | f_c(Y) for every c.   (Plain polynomial algebra; it
is compared with dense long division by Phi_d on small groups in ref_big_selftest.py.)

Phi_r | f_c is decided exactly in one of two ways:
   'ld'  : long division of f_c (dense, degree < r) by Phi_r; divisible iff the remainder is 0;
   'psi' : with Psi_r = (Y^r - 1) / Phi_r:  Phi_r | f  iff  Y^r - 1 | f * Psi_r,  i.e. the cyclic product is 0.
A class f_c that is a single monomial is never divisible by Phi_r (with 'ld' it is divided all the same).
"""
import math
from functools import lru_cache
from itertools import product
import numpy as np


def npdivmod(f, g):
    """f, g int64 arrays, low degree first, g monic.  Exact quotient and remainder."""
    f = f.copy()
    dg = len(g) - 1
    q = np.zeros(max(1, len(f) - dg), dtype=np.int64)
    for i in range(len(f) - 1, dg - 1, -1):
        c = f[i]
        if c:
            q[i - dg] = c
            f[i - dg:i + 1] -= c * g
    assert np.abs(f).max(initial=0) < 2 ** 50 and np.abs(q).max(initial=0) < 2 ** 50
    return q, f[:dg]


def prime_factors_squarefree(r):
    out = []
    p = 2
    while p * p <= r:
        if r % p == 0:
            out.append(p); r //= p
            assert r % p != 0
        p += 1
    if r > 1:
        out.append(r)
    return out


@lru_cache(None)
def Phi(r):
    """Phi_r for squarefree r, int64 array: Phi_(r0 p)(Y) = Phi_r0(Y^p) / Phi_r0(Y)."""
    if r == 1:
        return np.array([-1, 1], dtype=np.int64)
    p = max(prime_factors_squarefree(r))
    A = Phi(r // p)
    num = np.zeros((len(A) - 1) * p + 1, dtype=np.int64)
    num[::p] = A
    q, rem = npdivmod(num, A)
    assert not rem.any()
    return q


@lru_cache(None)
def Psi(r):
    """(Y^r - 1) / Phi_r, padded to length r."""
    f = np.zeros(r + 1, dtype=np.int64)
    f[0] = -1; f[r] = 1
    q, rem = npdivmod(f, Phi(r))
    assert not rem.any()
    out = np.zeros(r, dtype=np.int64)
    out[:len(q)] = q
    return out


def phi_divides(r, terms, method):
    """terms: list of (exponent in [0, r), nonzero integer coefficient), exponents distinct."""
    if not terms:
        return True
    if method == 'ld':
        f = np.zeros(r, dtype=np.int64)
        for y, s in terms:
            f[y] += s
        if r == 1:
            return int(f[0]) == 0
        q, rem = npdivmod(f, Phi(r))
        return not rem.any()
    if len(terms) == 1:
        return False
    P = Psi(r)
    acc = np.zeros(r, dtype=np.int64)
    for y, s in terms:
        if y == 0:
            acc += s * P
        else:
            acc[y:] += s * P[:r - y]
            acc[:y] += s * P[r - y:]
    return not acc.any()


def all_divisors(f):
    """f: dict prime -> exponent.  Yields (d, rad d)."""
    ps = sorted(f)
    for ex in product(*[range(f[p] + 1) for p in ps]):
        d = 1; r = 1
        for p, k in zip(ps, ex):
            d *= p ** k
            if k: r *= p
        yield d, r


class Tester:
    """prepared for one multiset: for every d | n the classes of the exponents modulo d / rad(d)."""

    def __init__(self, f, elems):
        self.f = dict(f); self.elems = list(elems)
        self.n = math.prod(p ** a for p, a in f.items())
        self.levels = []                         # (d, r, classes) ; classes: list of lists of (index, exponent)
        for d, r in all_divisors(f):
            e = d // r
            cl = {}
            for j, x in enumerate(self.elems):
                y = x % d
                cl.setdefault(y % e, []).append((j, y // e))
            classes = sorted(cl.values(), key=len)
            self.levels.append((d, r, classes))
        # a divisor d can divide some signed mask only if no class is a single element
        self.danger = [L for L in self.levels if len(L[2][0]) >= 2]

    @staticmethod
    def _terms(cls, signs):
        t = {}
        for j, y in cls:
            t[y] = t.get(y, 0) + signs[j]
        return [(y, s) for y, s in t.items() if s]

    def divides(self, level, signs, method='psi'):
        d, r, classes = level
        for cls in classes:
            if not phi_divides(r, self._terms(cls, signs), method):
                return False
        return True

    def bad_divisors(self, signs, method='psi'):
        return [L[0] for L in self.danger if self.divides(L, signs, method)]

    def good(self, signs, method='psi'):
        for L in self.danger:
            if self.divides(L, signs, method):
                return False
        return True

    def confirm_by_long_division(self, signs):
        """for EVERY d | n: divide one class polynomial by Phi_rad(d) (long division) and find a nonzero remainder.
        Returns (number of divisors d, number of long divisions made, True if every d has a class with nonzero remainder)."""
        ndiv = 0; ok = True
        for d, r, classes in self.levels:
            found = False
            for cls in classes:
                ndiv += 1
                if not phi_divides(r, self._terms(cls, signs), 'ld'):
                    found = True
                    break
            ok = ok and found
        return len(self.levels), ndiv, ok

    def numeric_min(self, signs):
        """least |S(exp(2 pi i / d))| over d | n, in floating point (a check, not a proof)."""
        best = None
        for d, r, classes in self.levels:
            v = 0j
            for j, x in enumerate(self.elems):
                ang = 2 * math.pi * ((x % d) / d)
                v += signs[j] * complex(math.cos(ang), math.sin(ang))
            if best is None or abs(v) < best[0]:
                best = (abs(v), d)
        return best
