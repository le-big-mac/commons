#!/usr/bin/env python
"""Exact check of ONE example (item (v) of the brief): which cyclotomic polynomials Phi_d, d | M, divide
the mask polynomial of a given multiset in Z_M.  Integer arithmetic only (no floating point).

usage: python -I check_example_v.py
Reads no file.  It checks the single example and its reduction mod 18; it searches for nothing.
"""


def polymul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return out


def polydivmod(a, b):
    """a, b integer coefficient lists (lowest degree first), b monic. Returns (quotient, remainder)."""
    a = a[:]
    q = [0] * max(1, len(a) - len(b) + 1)
    for k in range(len(a) - len(b), -1, -1):
        c = a[k + len(b) - 1]
        if c:
            q[k] = c
            for j, y in enumerate(b):
                a[k + j] -= c * y
    rem = a[: len(b) - 1]
    return q, rem


def cyclotomic(n, cache={}):
    if n in cache:
        return cache[n]
    num = [-1] + [0] * (n - 1) + [1]          # X^n - 1
    for d in range(1, n):
        if n % d == 0:
            num, rem = polydivmod(num, cyclotomic(d))
            assert not any(rem)
    cache[n] = num
    return num


def divisors_pattern(A, M):
    mask = [0] * M
    for x in A:
        mask[x % M] += 1
    out = []
    for d in range(2, M + 1):
        if M % d == 0:
            _, rem = polydivmod(mask, cyclotomic(d))
            if not any(rem):
                out.append(d)
    return out


def report(name, A, M, p, q, n):
    Z = divisors_pattern(A, M)
    E = [a for a in range(1, n + 1) if p ** a in Z]
    F = [a for a in range(0, n + 1) if p ** a * q in Z]
    print(name)
    print("  A =", sorted(x % M for x in A), "in Z_%d;" % M, "a set" if len({x % M for x in A}) == len(A) else "a multiset")
    print("  d | M, d > 1, with Phi_d | A(X):", Z)
    print("  E =", E, " F =", F, " |A| =", len(A), " p^2 + q =", p * p + q)


if __name__ == "__main__":
    A = list(range(0, 18, 2)) + [9, 18]
    report("item (v), in Z_54 (p = 3, q = 2, n = 3)", A, 54, 3, 2, 3)
    report("the same reduced mod 18 (p = 3, q = 2, n = 2)", A, 18, 3, 2, 2)
