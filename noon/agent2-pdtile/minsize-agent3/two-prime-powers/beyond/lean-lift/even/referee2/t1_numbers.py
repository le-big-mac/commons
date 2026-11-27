# t1_numbers.py -- every constant of even-result-2.md, recomputed from the definitions (exact fractions).
from fractions import Fraction as Fr
from math import log, exp
import sys

def primes_upto(N):
    s = [True] * (N + 1)
    s[0:2] = [False, False]
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]:
            for j in range(i * i, N + 1, i):
                s[j] = False
    return [i for i in range(N + 1) if s[i]]

def fl(x, d=9):   # float, for printing only
    return f"{float(x):.{d}f}"

# ---- W(no 3) from the definition: sum over e* > 1 with all prime factors >= 5 of 2^(-mu(e*)),
#      mu(e*) = max_q v_q(e*) (q - 1).  Direct enumeration of every e* with mu <= T (as exponent vectors).
def enum_by_mu(T, minprime=5):
    ps = [p for p in primes_upto(T + 1) if p >= minprime]
    counts = {}
    def rec(i, mu):
        if i == len(ps):
            counts[mu] = counts.get(mu, 0) + 1
            return
        p = ps[i]
        v = 0
        while v * (p - 1) <= T:
            rec(i + 1, max(mu, v * (p - 1)))
            v += 1
    rec(0, 0)
    return counts          # counts[t] = number of e* (1 included, at t = 0) with mu = t

T = 40
cnt = enum_by_mu(T)
tot = sum(cnt.values())
print("e* with all primes >= 5 and mu <= 40, listed one by one:", tot, "(1 included)")
part40 = sum(Fr(c, 2 ** t) for t, c in cnt.items() if t > 0)
print("W(no 3), terms with mu <= 40 (direct enumeration):", fl(part40, 12))

def A(t, minprime=5):
    r = 1
    for p in primes_upto(t + 1):
        if p >= minprime:
            r *= 1 + t // (p - 1)
    return r
# product formula against the enumeration
acc = 0
for t in range(0, T + 1, 2):
    acc += cnt.get(t, 0)
    assert acc == A(t), t
assert all(t % 2 == 0 for t in cnt)
print("product formula A(t) = prod_{5<=p<=t+1}(1+floor(t/(p-1))) agrees with the enumeration for every even t <= 40")
def partial(Tmax, minprime=5):
    return sum(Fr(A(t, minprime) - A(t - 2, minprime), 2 ** t) for t in range(2, Tmax + 1, 2))
assert partial(40) == part40
for Tm in (40, 60, 120, 400):
    print(f"  partial sum up to t = {Tm}: {fl(partial(Tm), 15)}")

# the tail bound of Lemma W (all odd d), recomputed: K = sum ln(1+1/k)/k ; x = e^(2K/3)/4 ; tail after t = 2u0-2 is
# sum_{u >= u0} (u+1) x^u = x^u0 ((u0+1) - u0 x)/(1-x)^2
Kpart = sum(log(1 + 1 / k) / k for k in range(1, 2000))
Kup = Kpart + 1 / 1999
x = exp(2 * Kup / 3) / 4
def tail(u0):
    return x ** u0 * ((u0 + 1) - u0 * x) / (1 - x) ** 2
print(f"K < {Kup:.7f}, x < {x:.6f}; Lemma W's tail after t = 40: {tail(21):.6e}; after t = 60: {tail(31):.3e}; after t = 400: {tail(201):.3e}")
print(f"  0.118564492 + 5.7e-4 = {0.118564492 + 5.7e-4:.9f}   (the text's two numbers; its claim is '< 0.119134')")
print(f"  partial(40) + tail(21) = {float(part40) + tail(21):.9f}")
W3up = float(partial(400)) + tail(201) + 1e-15
print(f"  W(no 3) < partial(400) + tail = {W3up:.12f}")
# check the all-odd count against Lemma W's table (A(12) = 336 etc.), same code with minprime = 3
assert [A(t, 3) for t in (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)] == [2, 6, 16, 30, 72, 336, 384, 1080, 3200, 6336]
print("  W (all odd), partial to t = 40:", fl(partial(40, 3), 9), " (Lemma W: 0.844468895)")

W3text = Fr(119134, 10 ** 6)
print()
print("numbers p_r:", " ".join(str(p) for p in [Fr(1)] + [None] * 0), end="")
p = [Fr(1)]
for r in range(60):
    p.append((1 - p[-1]) / 2)
print(" ".join(str(q) for q in p[:9]))
# p_r directly: number of sign vectors of length r with sum = 0 mod 3
from itertools import product
for r in range(0, 15):
    c = sum(1 for s in product((1, -1), repeat=r) if sum(s) % 3 == 0)
    assert Fr(c, 2 ** r) == p[r]
    assert p[r] - Fr(1, 3) == Fr(2, 3) * Fr(-1, 2) ** r
print("p_r equals the direct count for r <= 14, and p_r - 1/3 = (2/3)(-1/2)^r")
assert all(Fr(1, 4) <= p[r] <= Fr(1, 2) for r in range(2, 60))
assert all(p[r] <= Fr(3, 8) for r in range(3, 60))
assert all(p[r] <= Fr(11, 32) for r in range(5, 60))
print("1/4 <= p_r <= 1/2 (r >= 2), p_r <= 3/8 (r >= 3), p_r <= 11/32 (r >= 5): ok to r = 59")
print("Proposition H: m=3:", 1 - p[3], " m=4:", 1 - p[4], " m>=5: 1 - 11/32 - W(no 3) >", fl(1 - Fr(11, 32) - W3text, 6),
      " (with the true W(no 3):", f"{1 - 11/32 - W3up:.6f})")
print("Theorem G: 2h-1: m=3:", 2 * (1 - p[3]) - 1, " m=4:", 2 * (1 - p[4]) - 1, " m>=5: >", fl(2 * (1 - Fr(11, 32) - W3text) - 1, 6))
# the Remark of section 3
best = None
for a in range(0, 41):
    for b in range(a, 41):
        if (a, b) in ((0, 0), (1, 1)):
            continue
        v = p[a] + p[b] - 2 * p[a] * p[b]
        if best is None or v < best[0]:
            best = (v, a, b)
print("least p_E + p_D - 2 p_E p_D over sizes <= 40 except (0,0), (1,1):", best, "; 1/4 - 2*0.119134 =", fl(Fr(1, 4) - 2 * W3text, 6))
print("2*W(no 3) < ", fl(2 * W3text, 6), " (text: 0.238269);  3*W(no 3) =", fl(3 * W3text, 4))

# ---- section 5 ----
d3 = sum(Fr(1, 2 ** (2 * 3 ** (l - 1) - 1)) for l in range(1, 7))
print("delta_3 =", fl(d3, 9), "(text: < 0.531258)")
sA = sum(Fr(1, 2 ** (3 ** (l - 1))) for l in range(1, 7))
print("sum_l 2^(-3^(l-1)) =", fl(sA, 9), "(text: < 0.62696)")
sB = 1 + sum(Fr(1, 2 ** (1 + 2 * 3 ** (l - 1))) for l in range(1, 7))
print("1 + sum_l 2^(-1-2*3^(l-1)) =", fl(sB, 9), "(text: < 1.13282)")
tails = Fr(1, 2 ** 100)
tot = Fr(531258, 10 ** 6) + Fr(113282, 10 ** 5) * Fr(238269, 10 ** 6)
print("0.531258 + 1.13282*0.238269 =", fl(tot, 9), "(text: < 0.80118)")
tot_true = float(d3) + float(sB) * 2 * W3up
print("  with the true constants:", f"{tot_true:.9f}")
print("m = 9: 0.80118 + 3/16 =", fl(Fr(80118, 10 ** 5) + Fr(3, 16), 6), "(text: < 0.9887); with the true constants:", f"{tot_true + 3/16:.6f}")
# m = 9 sharper: with nine elements D_{e2} <= 8, so only e2* with mu <= 8 occur
c8 = enum_by_mu(8)
s8 = sum(Fr(c, 2 ** t) for t, c in c8.items() if t > 0)
print("  (sum of 2^-mu over e2* with mu <= 8, primes >= 5:", s8, "=", fl(s8, 6), ")")
# e2* with mu <= 6
c6 = enum_by_mu(6)
print("e2* with primes >= 5 and mu <= 6: counts by mu:", {t: c for t, c in c6.items() if t > 0}, "(5: mu 4; 7 and 35: mu 6)")
# Theorem J arithmetic
print("Theorem J: 5/16 - 1/8 =", Fr(5, 16) - Fr(1, 8), "; 21/64 - (5/32 + 1/32) =", Fr(21, 64) - Fr(5, 32) - Fr(1, 32))
# first result's constants cited
print("74/225 =", fl(Fr(74, 225), 6))
