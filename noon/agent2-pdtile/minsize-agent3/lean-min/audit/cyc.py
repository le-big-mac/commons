"""Exact integer polynomial arithmetic and cyclotomic polynomials, written for this audit.

A polynomial is a list of Python ints, lowest degree first, with no trailing zeros ([] is 0).
Nothing here uses floating point.
"""
from math import gcd


def trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def mul(a, b):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return trim(r)


def divmod_monic(a, b):
    """Long division of a by the MONIC polynomial b over the integers: a = quo*b + rem, deg rem < deg b."""
    assert b and b[-1] == 1
    a = list(a)
    db = len(b) - 1
    quo = [0] * max(0, len(a) - db)
    for i in range(len(a) - 1, db - 1, -1):
        c = a[i]
        if c:
            quo[i - db] = c
            for j in range(db + 1):
                a[i - db + j] -= c * b[j]
    return trim(quo), trim(a[:db])


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


_cache = {}


def cyclotomic(n):
    """Phi_n by its defining recursion: X^n - 1 = product of Phi_d over d | n."""
    if n in _cache:
        return _cache[n]
    num = [-1] + [0] * (n - 1) + [1]
    for d in divisors(n):
        if d < n:
            num, rem = divmod_monic(num, cyclotomic(d))
            assert rem == [], (n, d)
    _cache[n] = num
    return num


def phi(n):
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def mask_poly(w):
    """w: list of multiplicities indexed by the residue 0..M-1 -> the mask polynomial sum w(a) X^a."""
    return trim(w)


def divides(n, w):
    """Does Phi_n divide sum w(a) X^a ?  By long division."""
    _, rem = divmod_monic(mask_poly(w), cyclotomic(n))
    return rem == []


def pattern(M, w):
    """The set of d | M, d > 1, with Phi_d | sum w(a) X^a, by long division."""
    return frozenset(d for d in divisors(M) if d > 1 and divides(d, w))


def self_test(maxn=200):
    import sympy
    X = sympy.Symbol('X')
    for n in range(1, maxn + 1):
        c = cyclotomic(n)
        assert c[-1] == 1 and len(c) - 1 == phi(n), n
        s = sympy.Poly(sympy.cyclotomic_poly(n, X), X).all_coeffs()[::-1]
        assert [int(t) for t in s] == c, n
        # product over divisors is X^n - 1
        pr = [1]
        for d in divisors(n):
            pr = mul(pr, cyclotomic(d))
        assert pr == [-1] + [0] * (n - 1) + [1], n
    # known small ones
    assert cyclotomic(1) == [-1, 1]
    assert cyclotomic(2) == [1, 1]
    assert cyclotomic(3) == [1, 1, 1]
    assert cyclotomic(4) == [1, 0, 1]
    assert cyclotomic(6) == [1, -1, 1]
    assert cyclotomic(12) == [1, 0, -1, 0, 1]
    assert cyclotomic(5) == [1, 1, 1, 1, 1]
    assert cyclotomic(10) == [1, -1, 1, -1, 1]
    assert cyclotomic(8) == [1, 0, 0, 0, 1]
    assert cyclotomic(9) == [1, 0, 0, 1, 0, 0, 1]
    assert cyclotomic(18) == [1, 0, 0, -1, 0, 0, 1]
    assert cyclotomic(15) == [1, -1, 0, 1, -1, 1, 0, -1, 1]
    assert cyclotomic(20) == [1, 0, -1, 0, 1, 0, -1, 0, 1]
    assert cyclotomic(24) == [1, 0, 0, 0, -1, 0, 0, 0, 1]
    return maxn


if __name__ == '__main__':
    n = self_test()
    print(f"cyclotomic polynomials 1..{n}: monic, degree phi(n), equal to sympy's, product over d | n is X^n - 1: ok")
