"""Audit of the even skeleton: exact integer tools, written for this audit (nothing imported from other audits).

Polynomials are lists of Python integers, lowest coefficient first.  Phi_d is obtained from X^d - 1 by dividing out
Phi_e for the proper divisors e of d (exact long division, remainder checked to be 0).
"Bad at d" (Phi_d divides sum_k sg_k X^{e_k} over Z) and "3-bad at d" (the remainder of the signed mask modulo Phi_d
has all coefficients divisible by 3; used only for 3 not dividing d) are decided for all 2^m signings at once from the
table of the remainders of X^x modulo Phi_d, x = 0..d-1 (X^x mod Phi_d depends only on x mod d).
The definitions live, rank, IsPivot, mu are transcribed from Pnq/SignDefs.lean as Lean has them (natural subtraction:
i - 1 is 0 for i = 0).  Signing number s gives the element k the sign +1 if bit k of s is 1, else -1.
"""
from functools import lru_cache
from math import gcd
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
    return [d for d in range(1, n + 1) if n % d == 0]


def phi(n):
    return sum(1 for a in range(1, n + 1) if gcd(a, n) == 1)


def pdivmod(a, b):
    """long division of a by a monic b: (quotient, remainder)"""
    a = list(a)
    db = len(b) - 1
    assert b[-1] == 1
    if len(a) - 1 < db:
        return [0], a
    q = [0] * (len(a) - db)
    for k in range(len(a) - db - 1, -1, -1):
        c = a[k + db]
        q[k] = c
        if c:
            for j in range(db + 1):
                a[k + j] -= c * b[j]
    r = a[:db] if db > 0 else [0]
    return q, r


@lru_cache(maxsize=None)
def cyclo(d):
    """coefficients of Phi_d, lowest first"""
    a = [-1] + [0] * (d - 1) + [1]
    for e in divisors(d):
        if e < d:
            a, r = pdivmod(a, list(cyclo(e)))
            assert not any(r)
    assert len(a) - 1 == phi(d) and a[-1] == 1
    return tuple(a)


@lru_cache(maxsize=None)
def rem_table(d):
    """array (d, phi(d)): row x is the remainder of X^x modulo Phi_d"""
    c = cyclo(d)
    f = len(c) - 1
    t = np.zeros((d, f), dtype=np.int64)
    cur = [0] * f
    cur[0] = 1
    if f == 0:
        return t
    for x in range(d):
        t[x] = cur
        top = cur[-1]
        cur = [0] + cur[:-1]
        if top:
            for j in range(f):
                cur[j] -= top * c[j]
    return t


@lru_cache(maxsize=None)
def signs(m):
    """array (2^m, m) of +1/-1: row s, column k is +1 iff bit k of s is set"""
    s = np.arange(1 << m, dtype=np.int64)[:, None]
    k = np.arange(m, dtype=np.int64)[None, :]
    return (((s >> k) & 1) * 2 - 1).astype(np.int64)


def remainders(e, d):
    """array (2^m, phi(d)): the remainder of the signed mask modulo Phi_d, for every signing"""
    t = rem_table(d)
    rows = t[[x % d for x in e]] if len(e) else np.zeros((0, t.shape[1]), dtype=np.int64)
    return signs(len(e)) @ rows


def bad(e, d):
    """boolean vector over the signings: Phi_d divides the signed mask (over Z)"""
    return ~np.any(remainders(e, d) != 0, axis=1)


def bad3(e, d):
    """boolean vector over the signings: 3-bad at d, for 3 not dividing d"""
    assert d % 3 != 0
    return ~np.any(remainders(e, d) % 3 != 0, axis=1)


def class_sums3(e, d, M):
    """array (2^m, M, phi(d)) modulo 3: entry [s, r] is the class sum of the class r modulo M at a root of unity of
    order d, as an element of Z[x]/(Phi_d, 3) (so equality here is equality at every primitive d-th root of the
    algebraic closure of F_3, Phi_d being squarefree modulo 3 for 3 not dividing d)"""
    assert d % 3 != 0
    t = rem_table(d)
    m = len(e)
    out = np.zeros((1 << m, M, t.shape[1]), dtype=np.int64)
    sg = signs(m)
    for k, x in enumerate(e):
        out[:, x % M, :] += sg[:, k][:, None] * t[x % d][None, :]
    return out % 3


# ---- definitions of Pnq/SignDefs.lean, literally ----

def live(e, p, i):
    L = p ** max(i - 1, 0)
    N = p ** i
    occ = {x % N for x in e}
    return any(all((c + t * L) in occ for t in range(p)) for c in range(L))


def rank(e, p, i):
    return sum(1 for j in range(1, i + 1) if live(e, p, j))


def is_pivot(e, p, i, J):
    """J a collection of indices into e"""
    L = p ** max(i - 1, 0)
    N = p ** i
    cl = [e[k] % N for k in J]
    if len(set(cl)) != len(cl):
        return False
    s = set(cl)
    # for all c there is t < p with no element of J in the class c % L + t L; c ranges over all naturals, c % L over 0..L-1
    return all(any((r + t * L) not in s for t in range(p)) for r in range(L))


def max_pivot(e, p, i):
    """the largest size of a pivot set, by trying all subsets (small m)"""
    m = len(e)
    best = 0
    for s in range(1 << m):
        J = [k for k in range(m) if (s >> k) & 1]
        if len(J) > best and is_pivot(e, p, i, J):
            best = len(J)
    return best


def max_pivot_formula(e, p, i):
    """occupied classes modulo p^i minus the number of full groups (checked against max_pivot in the self-test)"""
    L = p ** max(i - 1, 0)
    N = p ** i
    occ = {x % N for x in e}
    full = sum(1 for c in range(L) if all((c + t * L) in occ for t in range(p)))
    return len(occ) - full


def mu(t):
    """the largest (p - 1) * v_p(t) over the primes p dividing t; 0 for t = 0, 1"""
    if t == 0:
        return 0
    return max([(p - 1) * a for p, a in factor(t).items()], default=0)


# ---- the literal definition of Bad3 in a finite field GF(3^r) that holds all primitive d-th roots ----

def _pmod3(a, g):
    """a modulo the monic polynomial g, coefficients modulo 3"""
    a = [x % 3 for x in a]
    dg = len(g) - 1
    for k in range(len(a) - 1, dg - 1, -1):
        c = a[k]
        if c:
            for j in range(dg + 1):
                a[k - dg + j] = (a[k - dg + j] - c * g[j]) % 3
    a = a[:dg]
    return a + [0] * (dg - len(a))


def _pmul3(a, b, g):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return _pmod3(r, g)


@lru_cache(maxsize=None)
def irreducible_factor3(d):
    """a monic factor g of Phi_d modulo 3 of degree r = the order of 3 modulo d (such a factor is irreducible:
    every root of Phi_d mod 3 is a primitive d-th root, which generates GF(3^r) and no smaller field).
    Found with sympy; that it divides Phi_d modulo 3 and has degree r is checked here."""
    assert d % 3 != 0
    import sympy
    X = sympy.symbols('X')
    c = cyclo(d)
    f = sympy.Poly(sum(int(ci) * X ** i for i, ci in enumerate(c)), X, modulus=3)
    r = 1
    while pow(3, r, d) != 1 % d:
        r += 1
    fac = [g for g, _ in f.factor_list()[1]]
    g = fac[0]
    coeffs = [int(x) % 3 for x in reversed(g.all_coeffs())]
    assert len(coeffs) - 1 == r and coeffs[-1] == 1, (d, r, coeffs)
    assert not any(_pmod3(list(c), coeffs)), d
    return tuple(coeffs), r


@lru_cache(maxsize=None)
def gf_powers(d):
    """array (d, r) over F_3: row x is zeta^x in GF(3^r) = F_3[y]/(g), zeta = y a primitive d-th root of unity.
    Checked: zeta^d = 1 and zeta^(d/q) != 1 for every prime q of d."""
    g, r = irreducible_factor3(d)
    g = list(g)
    one = [1] + [0] * (r - 1) if r >= 1 else []
    y = _pmod3([0, 1], g)
    pw = [one]
    for x in range(1, d + 1):
        pw.append(_pmul3(pw[-1], y, g))
    assert pw[d] == one
    for q in factor(d):
        assert pw[d // q] != one
    return np.array(pw[:d], dtype=np.int64).reshape(d, r)


def bad3_literal(e, d):
    """boolean vector over the signings, from the definition as Lean has it: the signed sum of zeta^(e_k) is 0 in
    GF(3^r) for EVERY primitive d-th root zeta (the powers zeta0^a, gcd(a, d) = 1, of one of them)"""
    assert d % 3 != 0
    pw = gf_powers(d)
    sg = signs(len(e))
    ok = np.ones(1 << len(e), dtype=bool)
    for a in range(1, d + 1):
        if gcd(a, d) != 1:
            continue
        rows = pw[[(a * x) % d for x in e]] if len(e) else np.zeros((0, pw.shape[1]), dtype=np.int64)
        v = (sg @ rows) % 3
        ok &= ~np.any(v != 0, axis=1)
    return ok


def bad3_literal_one(e, d, a):
    """the same at the single root zeta0^a: vector over the signings of 'the signed mask vanishes there'"""
    pw = gf_powers(d)
    sg = signs(len(e))
    rows = pw[[(a * x) % d for x in e]]
    v = (sg @ rows) % 3
    return ~np.any(v != 0, axis=1)
