"""My own check of Lemma W of the fourth result: W = sum over odd d > 1 of 2^(-mu(d)), mu(d) = max_p v_p(d)(p-1).
Two ways: (1) by the count A(t) = #{odd d : mu(d) <= t} = prod_p (1 + floor(t/(p-1))), exact fractions;
(2) by direct enumeration of every odd d with mu(d) <= T (built prime by prime), summing 2^(-mu(d)) exactly."""
from fractions import Fraction
from math import comb
def primes_upto(n):
    s = [True] * (n + 1); s[0:2] = [False, False]
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = [False] * len(s[i * i::i])
    return [i for i in range(3, n + 1) if s[i]]
def A(t):
    r = 1
    for p in primes_upto(t + 1): r *= 1 + t // (p - 1)
    return r
part = Fraction(0); prev = A(0)
for t in range(2, 202, 2):
    a = A(t); part += Fraction(a - prev, 2 ** t); prev = a
    if t in (2, 4, 6, 8, 10, 12, 40, 60, 100, 200): print('t <=', t, 'A =', a if t <= 40 else '...', 'partial sum =', float(part), part if t <= 12 else '')
# (2) direct enumeration for mu <= T
T = 16
ps = primes_upto(T + 1)
tot = Fraction(0); cnt = 0
def rec(i, mu):
    global tot, cnt
    if i == len(ps):
        if mu > 0: tot += Fraction(1, 2 ** mu); cnt += 1
        return
    p = ps[i]
    for v in range(0, T // (p - 1) + 1): rec(i + 1, max(mu, v * (p - 1)))
rec(0, 0)
part16 = Fraction(0); prev = A(0)
for t in range(2, T + 2, 2):
    a = A(t); part16 += Fraction(a - prev, 2 ** t); prev = a
print('direct enumeration, mu <=', T, ':', cnt, 'values of d, sum', float(tot), '; by A(t):', A(T) - 1, float(part16), 'equal:', tot == part16)
# crude tail: A(t) 2^-t <= ? check the ratio numerically
import math
print('A(t)/2^t at t = 100, 200, 400:', [float(Fraction(A(t), 2 ** t)) for t in (100, 200, 400)])
c = lambda k: Fraction(comb(k, k // 2), 2 ** k)
W = float(part) + 1e-9
print('even m: c_m + W_m (plain) and with the level 3 as 5/32, for m = 2..30')
for m in range(2, 32, 2):
    Wm = Fraction(0); prev = A(0)
    for t in range(2, m, 2):
        a = A(t); Wm += Fraction(a - prev, 2 ** t); prev = a
    plain = c(m) + Wm
    sharp = plain - Fraction(1, 4) + Fraction(5, 32) if m >= 14 else plain
    print(m, float(plain), float(sharp))
