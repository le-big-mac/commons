"""Exact tools, written for this reading and from nothing else: cyclotomic polynomials by integer division, and the
test 'Phi_d divides the mask of a multiset on Z_M' by the exact integer remainder.

Phi_d | A(X)  iff  the remainder of A(X) modulo Phi_d is 0.  Because Phi_d | X^d - 1, the remainder of X^y is that of
X^(y mod d); so with REM[d][c] = the remainder of X^c modulo Phi_d (an integer vector of length phi(d)),
Phi_d | A  iff  sum_y A(y) * REM[d][y mod d] = 0.  All in Python integers (or int64 for small cases): no rounding."""
from functools import lru_cache


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def poly_divmod_monic(a, b):
    """a, b integer coefficient lists, low degree first; b monic.  Returns (quotient, remainder)."""
    a = list(a)
    db = len(b) - 1
    assert b[-1] == 1
    q = [0] * max(1, len(a) - db)
    for i in range(len(a) - 1, db - 1, -1):
        c = a[i]
        if c:
            q[i - db] = c
            for j in range(db + 1):
                a[i - db + j] -= c * b[j]
    return q, a[:db] if db > 0 else []


@lru_cache(maxsize=None)
def cyclo(d):
    """coefficients of Phi_d, low degree first, by X^d - 1 = prod_{e | d} Phi_e"""
    num = [-1] + [0] * (d - 1) + [1]
    for e in divisors(d):
        if e < d:
            num, rem = poly_divmod_monic(num, cyclo(e))
            assert not any(rem)
    while len(num) > 1 and num[-1] == 0:
        num.pop()
    return tuple(num)


@lru_cache(maxsize=None)
def rem_table(d):
    """REM[c] = remainder of X^c modulo Phi_d, c = 0..d-1, each a tuple of length phi(d)"""
    phi = cyclo(d)
    deg = len(phi) - 1
    out = []
    for c in range(d):
        a = [0] * c + [1]
        _, r = poly_divmod_monic(a, phi) if c >= deg else (None, a + [0] * (deg - len(a)))
        r = list(r) + [0] * (deg - len(r))
        out.append(tuple(r[:deg]))
    return tuple(out)


def remainder(mult, d):
    """mult: dict x -> weight (integers); returns the remainder of the mask modulo Phi_d as a tuple"""
    T = rem_table(d)
    deg = len(T[0])
    acc = [0] * deg
    for x, w in mult.items():
        if w:
            row = T[x % d]
            for i in range(deg):
                if row[i]:
                    acc[i] += w * row[i]
    return tuple(acc)


def divides(d, mult):
    return not any(remainder(mult, d))


def pattern(mult, M):
    """the set of d > 1 dividing M with Phi_d | mask"""
    return frozenset(d for d in divisors(M) if d > 1 and divides(d, mult))


def selftest():
    # Phi_d has degree phi(d), is monic, and prod_{e | n} Phi_e = X^n - 1; known small ones
    from math import gcd
    assert cyclo(1) == (-1, 1) and cyclo(2) == (1, 1) and cyclo(3) == (1, 1, 1) and cyclo(4) == (1, 0, 1)
    assert cyclo(6) == (1, -1, 1) and cyclo(12) == (1, 0, -1, 0, 1) and cyclo(9) == (1, 0, 0, 1, 0, 0, 1)
    assert cyclo(18) == (1, 0, 0, -1, 0, 0, 1)
    for n in range(1, 130):
        assert len(cyclo(n)) - 1 == sum(1 for a in range(1, n + 1) if gcd(a, n) == 1)
        prod = [1]
        for e in divisors(n):
            b = cyclo(e)
            new = [0] * (len(prod) + len(b) - 1)
            for i, x in enumerate(prod):
                for j, y in enumerate(b):
                    new[i + j] += x * y
            prod = new
        assert prod == [-1] + [0] * (n - 1) + [1]
    # Phi_105 has a coefficient -2
    assert min(cyclo(105)) == -2
    # the division test against a direct long division of the mask
    import random
    rnd = random.Random(7)
    for _ in range(300):
        M = rnd.choice([6, 12, 18, 20, 30, 36, 45])
        mult = {rnd.randrange(M): rnd.randint(1, 4) for _ in range(rnd.randint(1, 8))}
        a = [0] * M
        for x, w in mult.items():
            a[x] += w
        for d in divisors(M):
            _, r = poly_divmod_monic(a, cyclo(d))
            assert (not any(r)) == divides(d, mult)
    # a fibre is divisible exactly as it should be: mask of {0, M/p, ..} = Phi_s for s | M, s not | M/p
    for M, p in [(12, 2), (12, 3), (18, 3), (36, 2), (45, 5)]:
        fib = {j * (M // p): 1 for j in range(p)}
        assert pattern(fib, M) == frozenset(s for s in divisors(M) if (M // p) % s != 0)
    return True


if __name__ == '__main__':
    print('selftest', selftest())
