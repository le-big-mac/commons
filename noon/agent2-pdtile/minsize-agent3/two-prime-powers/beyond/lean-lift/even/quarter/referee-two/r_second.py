#!/usr/bin/env python3
"""Referee, second look.  (a) Univ(43, 30) certified in fractions, compared exactly with the numbers now in the text.
(b) Lemma 8 on computed values over the AUTHOR's ranges (ranks up to what sixty elements allow, m from 1 on), with the
referee's phi.  (c) PP_p(m) of the referee's program (the definition now worded in Proposition 7) against the
author's lo_union2.py, prime by prime, EVERY prime p <= m <= 46 (the author's module is imported read-only, run
with -B so that nothing is written beside it)."""
import sys
from fractions import Fraction as F
import r_tables as RT
import r_tail as T

# ---- (a)
M, t = 43, 30
r = F(70710678119, 10 ** 11)
assert 2 * 70710678119 ** 2 >= 10 ** 22
ps = RT.primes_upto(t + 1)
val = {}
for p in ps:
    for j in range(1, t // (p - 1) + 1):
        e = M + p - 1
        val[(p, j)] = max(T.phi(p, j, M), F(1, 2 ** (e // 2)) * (r if e % 2 else 1))
tot = F(0)


def rec(i, mn, nonempty):
    global tot
    if i == len(ps):
        if nonempty:
            tot += mn
        return
    rec(i + 1, mn, nonempty)
    for j in range(1, t // (ps[i] - 1) + 1):
        rec(i + 1, min(mn, val[(ps[i], j)]), True)


rec(0, F(10), False)
univ = RT.c(M) + tot + (T.Wpart(60) + F(34, 10 ** 7) - T.Wpart(t))
digits = (univ.numerator * 10 ** 15) // univ.denominator
print("(a) certified Univ(43, 30), exact fraction, first 15 decimals (truncated): 0.%015d" % digits)
for a, b in ((362413084, 10 ** 9), (3624131, 10 ** 7), (36242, 10 ** 5), (3625, 10 ** 4), (3, 8)):
    print("    Univ <= %d/%d: %s   Univ < %d/%d: %s" % (a, b, univ <= F(a, b), a, b, univ < F(a, b)))

# ---- (b)
R = 60
n = grow = fail = 0
for p in RT.primes_upto(31):
    Gcap = max(1, (R - p) // 2 + 1)
    j = 1
    while 1 + (j - 1) * (p - 1) <= Gcap:
        for m in range(1, R):
            a, b = T.phi(p, j, m + 1), T.phi(p, j, m)
            n += 1
            if a > b:
                grow += 1
                if a * a > F(1, 2 ** (m + p - 1)):
                    fail += 1
        j += 1
print("(b) Lemma 8 over the author's ranges (primes <= 31, ranks while 1+(j-1)(p-1) <= (60-p)//2+1, m = 1..59): %d cases, phi grows in %d, failures %d  (text: 2,301 and 39)" % (n, grow, fail))

# ---- (c)
sys.path.insert(0, "/home/agent3/lean/lift-check/even/quarter/two")
import lo_union2 as L
MM = 46
Tb = L.Tab(MM, True); zero = Tb.zero
ncmp = ndiff = 0
for p in L.primes_upto(MM):
    Gmax = max(1, (MM - p) // 2 + 1)
    Ef, Vf = L.integer_level(p, Tb, False, Gmax)
    Eb, Vb = L.integer_level(p, Tb, True, Gmax)
    for m in range(p, MM + 1):
        sE, sV = L.suffix_max(Ef, Gmax, m, zero), L.suffix_max(Vf, Gmax, m, zero)
        bE, bV = L.suffix_max(Eb, Gmax, m, zero), L.suffix_max(Vb, Gmax, m, zero)
        last, nonlast = [], []
        j = 1
        while 1 + (j - 1) * (p - 1) <= Gmax:
            G = 1 + (j - 1) * (p - 1)
            last.append(min(sE[G], sV[G])); nonlast.append(min(bE[G], bV[G])); j += 1
        v = zero; acc = zero
        for l in range(len(last)):
            v = max(v, acc + last[l]); acc += nonlast[l]
        ncmp += 1
        if v != RT.PP(p, m):
            ndiff += 1; print("    PP differs p=%d m=%d: author's module %s, referee %s" % (p, m, v, RT.PP(p, m)))
print("(c) PP_p(m), every odd prime p <= m <= 46 (13 primes), author's module against the referee's program: %d pairs, %d differences" % (ncmp, ndiff))
