"""Reader's own pattern tests for a multiset on Z_M (exact integers; nothing imported from the note's programs, no sympy).

Three separate routes:
  cuboid(v, M, d)    Phi_d | A  iff  A(X) * prod_{primes r | d} (1 - X^{d/r}) = 0 mod X^d - 1   (folded to Z_d)
  remainder(v, M, d) Phi_d | A  iff  the remainder of A(X) on long division by Phi_d is zero; Phi_d is built here by
                     dividing X^d - 1 by the Phi_e, e | d, e < d (integer long division by monic polynomials)
  numeric(v, M, d)   |A(exp(2 pi i / d))| < 1e-7   (floating point, used only as a cross-check)
pattern(v, M) returns the sorted list of d > 1, d | M, with Phi_d | A, and stops with an error if the routes disagree.
"""
import cmath, math
from functools import lru_cache


def divisors(M):
    return [d for d in range(1, M + 1) if M % d == 0]


def primes_of(n):
    out, r = [], 2
    while r * r <= n:
        if n % r == 0:
            out.append(r)
            while n % r == 0:
                n //= r
        r += 1
    if n > 1:
        out.append(n)
    return out


def parse(ms, M):
    """'3 7^2 10' -> count vector of length M"""
    v = [0] * M
    for tok in ms.split():
        if '^' in tok:
            a, w = tok.split('^')
            a, w = int(a), int(w)
        else:
            a, w = int(tok), 1
        assert 0 <= a < M and w >= 1, tok
        assert v[a] == 0, ('element listed twice', tok)
        v[a] += w
    return v


def fold(v, d):
    b = [0] * d
    for x, w in enumerate(v):
        if w:
            b[x % d] += w
    return b


def cuboid(v, M, d):
    b = fold(v, d)
    for r in primes_of(d):
        s = d // r
        b = [b[t] - b[(t + s) % d] for t in range(d)]
    return not any(b)


def polydivmod(a, m):
    """a, m lists of integers, lowest degree first; m monic.  Returns (quotient, remainder)."""
    a = a[:]
    dm = len(m) - 1
    assert m[-1] == 1
    q = [0] * max(len(a) - dm, 1)
    for i in range(len(a) - 1, dm - 1, -1):
        c = a[i]
        if c:
            q[i - dm] = c
            for j in range(dm + 1):
                a[i - dm + j] -= c * m[j]
    return q, a[:dm]


@lru_cache(None)
def cyclo(d):
    """Phi_d as a tuple of integers, lowest degree first."""
    num = [-1] + [0] * (d - 1) + [1]
    for e in divisors(d):
        if e < d:
            num, rem = polydivmod(num, list(cyclo(e)))
            assert not any(rem)
            while len(num) > 1 and num[-1] == 0:
                num.pop()
    return tuple(num)


def remainder(v, M, d):
    q, rem = polydivmod(list(v), list(cyclo(d)))
    return not any(rem)


def numeric(v, M, d):
    z = sum(w * cmath.exp(2j * math.pi * x / d) for x, w in enumerate(v) if w)
    return abs(z) < 1e-7


def pattern(v, M, routes=3):
    out = []
    for d in divisors(M):
        if d == 1:
            continue
        a = cuboid(v, M, d)
        b = remainder(v, M, d)
        assert a == b, ('routes disagree', d, a, b)
        if routes == 3:
            c = numeric(v, M, d)
            assert a == c, ('numeric route disagrees', d, a, c)
        if a:
            out.append(d)
    return out


if __name__ == '__main__':
    # self-test on cases known by hand
    assert cyclo(1) == (-1, 1) and cyclo(2) == (1, 1) and cyclo(6) == (1, -1, 1) and cyclo(12) == (1, 0, -1, 0, 1)
    assert sum(cyclo(9)) == 3 and sum(cyclo(25)) == 5 and sum(cyclo(15)) == 1 and len(cyclo(225)) == 121
    M = 36
    v = [0] * M
    for x in range(0, 36, 4): v[x] += 1                 # coset of 4Z_36: divisors of 36 not dividing 4
    assert pattern(v, M) == [3, 6, 9, 12, 18, 36]
    v = [0] * M
    v[0] = 1
    assert pattern(v, M) == []
    v = [1] * M
    assert pattern(v, M) == [2, 3, 4, 6, 9, 12, 18, 36]
    v = [0] * M
    for x in (0, 18, 0, 12, 24): v[x] += 1              # Lam-Leung: order-2 coset plus order-3 coset: Phi_36 only
    assert pattern(v, M) == [36]
    # planted fault: move one point
    v[1] += 1; v[0] -= 1
    assert pattern(v, M) == []
    print('self-test passed')
