"""The shares of Corollary 3 of theorem-twice.md with the sum W(no 3) cut off at mu <= m - 1.
p_m = 1/3 + (2/3)(-1/2)^m: the share of signings of m elements whose signs add up to a multiple of 3.
A(t) = prod over primes 5 <= p <= t + 1 of (1 + floor(t/(p - 1))): the number of e* >= 1 with all prime factors >= 5
and mu(e*) = max_q v_q(e*)(q - 1) <= t (Lemma L3 (c) of even-result-2.md).  b(u) = A(u) - A(u - 1).
W_m = sum over 1 <= u <= m - 1 of b(u) / 2^u.   s_m = 1 - 2 p_m - 2 W_m: lower bound for the share of good signings.
Also checks A(t) against a direct list of the e* for t <= 24."""
from fractions import Fraction as F
from sympy import primerange, factorint
def A(t):
    r = 1
    for p in primerange(5, t + 2): r *= 1 + t // (p - 1)
    return r
def mu(e): return max((v * (q - 1) for q, v in factorint(e).items()), default=0)
def direct(t):
    # all e* >= 1 with prime factors >= 5 and mu <= t: exponents v_q <= t // (q - 1)
    c = 1
    for p in primerange(5, t + 2): c *= 1 + t // (p - 1)
    # brute list for a cross-check, small t only
    es = [1]
    for p in primerange(5, t + 2):
        es = [e * p ** v for e in es for v in range(t // (p - 1) + 1)]
    assert all(mu(e) <= t for e in es) and len(set(es)) == len(es)
    return len(es)
for t in range(0, 25): assert A(t) == direct(t), t
W = F(0); rows = []
for m in range(2, 61):
    u = m - 1
    if u >= 1: W += F(A(u) - A(u - 1), 2 ** u)
    p = F(1, 3) + F(2, 3) * F(-1, 2) ** m
    s = 1 - 2 * p - 2 * W
    rows.append((m, p, W, s))
print("b(u) for u = 1..20:", [A(u) - A(u - 1) for u in range(1, 21)])
for m, p, Wm, s in rows:
    if 5 <= m <= 16 or m in (20, 30, 40, 60):
        print(f"m = {m:2d}  p_m = {str(p):>12s}  W_m = {str(Wm) if m <= 12 else format(float(Wm), '.10f'):>14s}  1 - 2 p_m - 2 W_m = {str(s) if m <= 12 else format(float(s), '.10f'):>12s} = {float(s):.6f}")
print("least value for 5 <= m <= 60:", min((float(s), m) for m, p, Wm, s in rows if m >= 5))
print("for m > 60: p_m <= 1/3 + (2/3)/2^61 and W_m < 0.118569, so the bound is more than", float(1 - 2 * (F(1, 3) + F(2, 3) / 2 ** 61) - 2 * F(118569, 10 ** 6)))
