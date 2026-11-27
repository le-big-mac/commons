#!/usr/bin/env python3
"""One multiset, slowly and apart from cor3_check.py's tables: the signed mask is divided by Phi_d by long division
(Python integers) for every signing; prints the shares of good and of 3-good signings and the shares 3-bad at each d.

usage: verify_example.py <n> <b1> <b2> ...
"""
import sys
from fractions import Fraction


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return out


def rem(a, b):
    a = a[:]
    db = len(b) - 1
    for i in range(len(a) - 1, db - 1, -1):
        c = a[i]
        if c:
            for j, y in enumerate(b):
                a[i - db + j] -= c * y
    return a[:db]


def quo_exact(a, b):
    a = a[:]
    db = len(b) - 1
    q = [0] * (len(a) - db)
    for i in range(len(a) - 1, db - 1, -1):
        c = a[i]
        q[i - db] = c
        if c:
            for j, y in enumerate(b):
                a[i - db + j] -= c * y
    assert not any(a)
    return q


def cyclo(n):
    """Phi_d for d | n, here by the product over the proper divisors (another route than cor3_check.py's)."""
    Phi = {}
    for d in divisors(n):
        prod = [1]
        for e in divisors(d):
            if e < d:
                prod = mul(prod, Phi[e])
        Phi[d] = quo_exact([-1] + [0] * (d - 1) + [1], prod)
    return Phi


def main():
    n = int(sys.argv[1])
    B = [int(x) % n for x in sys.argv[2:]]
    m = len(B)
    Phi = cyclo(n)
    n3 = n
    while n3 % 3 == 0:
        n3 //= 3
    good = good3 = 0
    cnt3 = {d: 0 for d in divisors(n3)}
    cnt = {d: 0 for d in divisors(n)}
    for s in range(1 << m):
        S = [0] * n
        for j, b in enumerate(B):
            S[b] += -1 if (s >> j) & 1 else 1
        g = g3 = True
        for d in divisors(n):
            r = rem(S, Phi[d])
            if not any(r):
                g = False
                cnt[d] += 1
            if n3 % d == 0 and all(x % 3 == 0 for x in r):
                g3 = False
                cnt3[d] += 1
        good += g
        good3 += g3
    tot = 1 << m
    print("n = %d, B = %s, %d signings" % (n, B, tot))
    print("  share of good signings:   %s" % Fraction(good, tot))
    print("  share of 3-good signings: %s  (= %.6f)" % (Fraction(good3, tot), good3 / tot))
    print("  share bad at d:   " + ", ".join("%d: %s" % (d, Fraction(c, tot)) for d, c in cnt.items() if c))
    print("  share 3-bad at d: " + ", ".join("%d: %s" % (d, Fraction(c, tot)) for d, c in cnt3.items() if c))


if __name__ == "__main__":
    main()
