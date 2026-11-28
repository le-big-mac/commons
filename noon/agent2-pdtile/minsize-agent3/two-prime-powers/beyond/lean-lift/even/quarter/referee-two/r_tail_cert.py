#!/usr/bin/env python3
"""Referee: Univ(43, 30) of Theorem B with exact fractions and 2^(-1/2) replaced by the rational upper bound
70710678119/10^11 (its square is larger than 1/2), so that the result is a certified upper bound close to the
floating-point value of tail.py."""
from fractions import Fraction as F
import r_tables as RT
import r_tail as T

M, t = 43, 30
r = F(70710678119, 10 ** 11)
assert r * r > F(1, 2)
ps = RT.primes_upto(t + 1)
val = {}
for p in ps:
    for j in range(1, t // (p - 1) + 1):
        e = M + p - 1
        two = F(1, 2 ** (e // 2)) * (r if e % 2 else 1)
        val[(p, j)] = max(T.phi(p, j, M), two)
tot = F(0); n = 0


def rec(i, mn, nonempty):
    global tot, n
    if i == len(ps):
        if nonempty:
            tot += mn; n += 1
        return
    rec(i + 1, mn, nonempty)
    for j in range(1, t // (ps[i] - 1) + 1):
        rec(i + 1, min(mn, val[(ps[i], j)]), True)


rec(0, F(10), False)
univ = RT.c(M) + tot + (T.Wpart(60) + F(34, 10 ** 7) - T.Wpart(t))
print("d*: %d; certified Univ(43, 30) <= %.9f; < 0.36242: %s; < 0.3625: %s; < 3/8: %s" % (n, float(univ), univ < F(36242, 100000), univ < F(3625, 10000), univ < F(3, 8)))
