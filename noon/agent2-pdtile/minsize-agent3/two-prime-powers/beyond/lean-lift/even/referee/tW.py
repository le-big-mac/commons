# The constants of Proposition P (3) and Theorem D, from the definition of mu; exact fractions.
#   W_Pi = sum over e* > 1 with all prime factors in Pi of 2^(-mu(e*)),  mu(e*) = max_p v_p(e*) (p - 1).
# (1) direct enumeration of the e* with mu <= T (depth-first over the exponents), counted by the value of mu;
# (2) the product formula; (3) the tail: the estimate of Lemma W checked again and carried to subsets of the primes;
# (4) the sums of Theorem D (i), (ii), (iii) and the two figures 1.32 and 1.03.
from fractions import Fraction as F
from math import log, exp
import sys

def primes_upto(N):
    return [p for p in range(3, N + 1, 2) if all(p % q for q in range(3, int(p ** 0.5) + 1, 2))]

def count_by_mu(Pi, T):
    """number of e* >= 1 with prime factors in Pi (those <= T+1 matter) and mu(e*) = t, for t = 0..T, by DFS"""
    ps = [p for p in Pi if p - 1 <= T]
    cnt = [0] * (T + 1)
    def rec(i, cur):
        if i == len(ps):
            cnt[cur] += 1
            return
        p = ps[i]
        v = 0
        while v * (p - 1) <= T:
            rec(i + 1, max(cur, v * (p - 1)))
            v += 1
    rec(0, 0)
    return cnt

def A_formula(Pi_filter, t):
    r = 1
    for p in primes_upto(t + 1):
        if Pi_filter(p):
            r *= 1 + t // (p - 1)
    return r

def W_partial(Pi_filter, T):
    s = F(0)
    for t in range(2, T + 1, 2):
        s += F(A_formula(Pi_filter, t) - A_formula(Pi_filter, t - 2), 2 ** t)
    return s

sets = [("all odd primes", lambda p: True), ("no 3", lambda p: p != 3), ("no 5", lambda p: p != 5),
        ("no 7", lambda p: p != 7), ("{3}", lambda p: p == 3), ("{3,5}", lambda p: p in (3, 5)),
        ("{3,5,7}", lambda p: p in (3, 5, 7)), ("{3,5,11}", lambda p: p in (3, 5, 11))]

# (1) against (2)
T = 26
for name, flt in sets:
    Pi = [p for p in primes_upto(T + 1) if flt(p)]
    cnt = count_by_mu(Pi, T)
    assert all(cnt[t] == 0 for t in range(1, T + 1, 2))
    for t in range(2, T + 1, 2):
        assert cnt[t] == A_formula(flt, t) - A_formula(flt, t - 2), (name, t)
    direct = sum(F(cnt[t], 2 ** t) for t in range(2, T + 1, 2))
    assert direct == W_partial(flt, T)
print("product formula = direct enumeration of the e* by the value of mu, up to mu = %d, for all eight sets of primes" % T)
# a second direct check straight from the definition of mu on integers: odd e <= 200000
def mu(e):
    m, p = 0, 3
    while p * p <= e:
        v = 0
        while e % p == 0:
            e //= p; v += 1
        m = max(m, v * (p - 1)); p += 2
    if e > 1:
        m = max(m, e - 1)
    return m
c = {}
for e in range(3, 15001, 2):          # the largest e with mu <= 8 is 3^4 * 5^2 * 7 = 14175
    t = mu(e)
    if t <= 8:
        c[t] = c.get(t, 0) + 1
assert [c[t] for t in (2, 4, 6, 8)] == [A_formula(lambda p: True, t) - A_formula(lambda p: True, t - 2) for t in (2, 4, 6, 8)]
print("numbers of odd e with mu = 2, 4, 6, 8 (all such e are at most 14175):", [c[t] for t in (2, 4, 6, 8)])

# (3) the tail.  Lemma W: A(t) 2^(-t) <= (u+1) x^u, u = t/2, x = e^(2K/3)/4, K = sum ln(1+1/k)/k.
Kpart = sum(log(1 + 1 / k) / k for k in range(1, 2000001))
K_upper = Kpart + 1 / (2000000)          # sum_{k > N} 1/k^2 < 1/N
x = exp(2 * K_upper / 3) / 4
print("K < %.7f (the text of Lemma W: < 1.2578);  x = e^(2K/3)/4 < %.6f (text: < 0.5783)" % (K_upper, x))
assert K_upper < 1.2578 and x < 0.5783
# pi'(y) <= 1 + (y-1)/3 for integers y >= 3 (checked to 200000), the inequality behind the estimate
ps = set(primes_upto(200000))
cntp = 0
for y in range(3, 200001):
    if y in ps:
        cntp += 1
    assert 3 * cntp <= 3 + (y - 1)
# the estimate itself for every even t <= 600
xx = 0.5783
for t in range(2, 601, 2):
    u = t // 2
    assert A_formula(lambda p: True, t) <= (u + 1) * (4 * xx) ** u, t      # exact integer against float with huge room
tail = lambda U: xx ** U * (U + 1 - U * xx) / (1 - xx) ** 2      # sum_{u >= U} (u+1) x^u
print("tail after t = 40: sum_{u>=21} (u+1) x^u = %.3e (text: < 5.7e-4);  after t = 400: %.3e" % (tail(21), tail(201)))
assert tail(21) < 5.7e-4
# For a subset Pi of the primes every term (number of e* with mu = t and primes in Pi) is at most the term for all
# primes, so the same tail bound holds: checked here term by term up to t = 400.
for name, flt in sets:
    for t in range(2, 401, 2):
        assert A_formula(flt, t) - A_formula(flt, t - 2) <= A_formula(lambda p: True, t) - A_formula(lambda p: True, t - 2)
print("terms for the subsets <= terms for all primes, every t <= 400")
res = {}
for name, flt in sets:
    w40, w400 = W_partial(flt, 40), W_partial(flt, 400)
    res[name] = (w40, w400)
    print("%-15s partial sum to t=40: %.8f ; to t=400: %.10f ; upper bound (t=40 plus 5.7e-4): %.6f ; (t=400 plus %.1e): %.10f"
          % (name, float(w40), float(w400), float(w40) + 5.7e-4, tail(201), float(w400) + tail(201)))
assert float(res["no 3"][0]) + 5.7e-4 < 0.11914
assert float(res["no 5"][0]) + 5.7e-4 < 0.43241
assert res["{3}"][1] < F(1, 3) and F(1, 3) - res["{3}"][1] < F(1, 2 ** 300)
print()
print("Theorem D (i):  2 W(no 3) < %.6f ;  3/4 + 2 W(no 3) < %.6f  (with the true value of W(no 3): %.6f)"
      % (2 * (float(res["no 3"][0]) + 5.7e-4), 0.75 + 2 * (float(res["no 3"][0]) + 5.7e-4), 0.75 + 2 * float(res["no 3"][1])))
print("Theorem D (ii): 2 W(no 5) < %.6f ;  2 W({3}) = 2/3" % (2 * (float(res["no 5"][0]) + 5.7e-4)))
# (4) Theorem D (iii)
def delta(p):
    # sum over l >= 1 of 2^(1 - (p-1) p^(l-1)); the terms with exponent above 4000 are left out (below 2^-4000 in all)
    s, l = F(0), 1
    while (p - 1) * p ** (l - 1) <= 4000:
        s += F(2, 2 ** ((p - 1) * p ** (l - 1)))
        l += 1
    return s
d3, d5 = delta(3), delta(5)
print("delta_3 = %.9f (text < 0.53126), delta_5 = %.9f (text < 0.12501); the neglected terms are below 2^-4000" % (float(d3), float(d5)))
mixed = sum(F(2, 2 ** max(2 * a, 4 * b)) for a in range(1, 400) for b in range(1, 200))
print("mixed: sum_{a,b>=1} 2^(1-max(2a,4b)) = %.12f ; 74/225 = %.12f ; difference %.1e" % (float(mixed), 74 / 225, float(F(74, 225) - mixed)))
closed = sum((4 * b + F(2, 3)) * F(1, 16 ** b) for b in range(1, 200))
assert abs(float(closed - F(74, 225))) < 1e-30 and abs(float(mixed - F(74, 225))) < 1e-30
print("total (iii): %.6f (text: less than 0.98516)" % (float(d3 + d5) + 74 / 225))
assert float(d3) < 0.53126 and float(d5) < 0.12501 and float(d3 + d5) + 74 / 225 < 0.98516
for P in ((3, 5), (3, 5, 7), (3, 5, 11), (3, 7), (3, 5, 13), (3, 5, 17)):
    Pi = list(P)
    T = 60
    cnt_all = count_by_mu(Pi, T)
    # mixed e*: at least two primes; pure: one prime
    pure = sum(delta(p) for p in P)
    Wp = sum(F(cnt_all[t], 2 ** t) for t in range(2, T + 1, 2))
    pure_w = sum(sum(F(1, 2 ** (l * (p - 1))) for l in range(1, T // (p - 1) + 1)) for p in P)
    mixedP = 2 * (Wp - pure_w)
    print("Pi = %s: sum_p delta_p = %.6f, mixed (as in (3)) = %.6f, total = %.6f   [2 W_Pi = %.6f]" % (P, float(pure), float(mixedP), float(pure + mixedP), float(2 * Wp)))
print("OK")
