"""Referee's recomputation of W(no 3) = sum over the integers e* > 1 with all prime factors >= 5 of 2^(-mu(e*)),
mu(e*) = max over primes q | e* of v_q(e*) * (q - 1).  Exact rational arithmetic.

1. From the definition: enumerate every e* with mu(e*) <= T0 (as exponent vectors over the primes 5 <= q <= T0 + 1),
   compute mu for each, add 2^(-mu).  T0 = 40 (443,519 integers).
2. By counting: A(t) = #{e* >= 1 : mu(e*) <= t} = prod over primes 5 <= q <= t + 1 of (1 + floor(t / (q - 1)));
   the number with mu = t is A(t) - A(t-1).  Checked against 1 for t <= T0, then used up to T1 = 3000.
3. Tail beyond T1, proved here and not borrowed: sum_{t > T1} (A(t) - A(t-1)) 2^(-t) <= sum_{t > T1} A(t) 2^(-t).
   log2 A(t) = sum_q log2(1 + floor(t/(q-1))) = sum_{j >= 1} log2(1 + 1/j) * #{primes q >= 5 : q - 1 <= t / j}.
   A prime q >= 5 is 5 or is prime to 30; among any 30 consecutive integers 8 are prime to 30, so
   #{primes 5 <= q <= x} <= 1 + 8 * (x / 30 + 1) = 4x/15 + 9.  Only j <= t/4 contribute (q - 1 >= 4).  Hence
   log2 A(t) <= sum_{j <= t/4} log2(1+1/j) * (4t/(15j) + 4/15 + 9) <= a*t + (9 + 4/15) * log2(t/4 + 1) =: B(t),
   a = (4/15) * sum_{j>=1} log2(1+1/j)/j < 0.4840 < 1.  The program checks A(t) <= 2^B(t) for t <= T1 (a check of
   the algebra; the inequality is proved for all t) and bounds the tail by a geometric series.
"""
from fractions import Fraction
import math, sys

def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b'\x00\x00'
    for i in range(2, int(n ** .5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]

T0 = 40
PR = [q for q in primes_upto(T0 + 1) if q >= 5]

# 1. from the definition
count_by_mu = {}
def rec(i, mu):
    if i == len(PR):
        count_by_mu[mu] = count_by_mu.get(mu, 0) + 1
        return
    q = PR[i]
    v = 0
    while v * (q - 1) <= T0:
        rec(i + 1, max(mu, v * (q - 1)))
        v += 1
rec(0, 0)
assert count_by_mu[0] == 1          # e* = 1
total_enum = sum(c for mu, c in count_by_mu.items() if mu > 0)
W_def = sum(Fraction(c, 2 ** mu) for mu, c in count_by_mu.items() if mu > 0)
print(f"1. definition, mu <= {T0}: {total_enum} integers e* > 1; partial sum = {float(W_def):.12f}")
print("   first terms (mu: number of e*):", {mu: count_by_mu[mu] for mu in sorted(count_by_mu) if 0 < mu <= 16})

# 2. product formula
def A(t, primes):
    r = 1
    for q in primes:
        if q - 1 > t:
            break
        r *= 1 + t // (q - 1)
    return r
T1 = 3000
P1 = [q for q in primes_upto(T1 + 1) if q >= 5]
cum = 0
for t in range(0, T0 + 1):
    cum += count_by_mu.get(t, 0)
    assert A(t, P1) == cum, t
print(f"2. A(t) = prod (1 + floor(t/(q-1))) agrees with the enumeration for every t <= {T0}; A({T0}) = {A(T0, P1)}")
W_T1 = Fraction(0)
prev = A(0, P1)
partial40 = None
for t in range(1, T1 + 1):
    a = A(t, P1)
    W_T1 += Fraction(a - prev, 2 ** t)
    prev = a
    if t == T0:
        partial40 = W_T1
assert partial40 == W_def
print(f"   partial sum up to t = {T0}: {float(partial40):.12f}   (the text: 0.118564492)")
for t in (60, 100, 200, 400, 1000, T1):
    s = Fraction(0); p = 1
    for u in range(1, t + 1):
        a = A(u, P1); s += Fraction(a - p, 2 ** u); p = a
    print(f"   partial sum up to t = {t}: {float(s):.15f}")

# 3. tail
# sum_{j>=1} log2(1+1/j)/j : upper bound = partial sum to J plus sum_{j>J} (1/(j ln 2))/j <= 1/(J ln 2)
J = 100000
c0 = sum(math.log2(1 + 1 / j) / j for j in range(1, J + 1)) + 1 / (J * math.log(2)) + 1e-9
a_coef = 4 / 15 * c0
print(f"3. sum_j log2(1+1/j)/j <= {c0:.6f}; a = (4/15) * that <= {a_coef:.6f}")
def Bbound(t):
    # #{primes 5 <= q <= x} <= 4x/15 + 9 with x = t/j + 1:  <= 4t/(15 j) + 4/15 + 9
    # log2 A(t) <= sum_{j=1}^{floor(t/4)} log2(1+1/j) * (4t/(15j) + 9 + 4/15)
    #           <= a*t + (9 + 4/15) * log2(floor(t/4) + 1)
    return a_coef * t + (9 + 4 / 15) * math.log2(t / 4 + 1)
worst = max(math.log2(A(t, P1)) - Bbound(t) for t in range(4, T1 + 1))
print(f"   check: max over 4 <= t <= {T1} of log2 A(t) - B(t) = {worst:.3f} (must be <= 0)")
assert worst <= 0
# tail: sum_{t > T1} 2^(B(t) - t).  For t >= T1: B(t) - t <= -(1 - a) t + 9.27*log2(t/4+1), and
# 9.27*log2(t/4 + 1) <= 9.27*log2(T1/4+1) + 9.27*(t - T1)/((T1/4+1)*4*ln 2)  (concavity), so the terms decay
# at least geometrically with ratio 2^(-(1 - a) + slope).
slope = (9 + 4 / 15) / ((T1 / 4 + 1) * 4 * math.log(2))
ratio = 2 ** (-(1 - a_coef) + slope)
log2_tail = (Bbound(T1 + 1) - (T1 + 1)) - math.log2(1 - ratio)
print(f"   tail beyond t = {T1}: at most 2^({log2_tail:.1f})")
assert log2_tail < -1000
print(f"RESULT: W(no 3) = {float(W_T1):.15f} + (tail < 2^-1000);  claimed: < 0.119134;  2 W = {2*float(W_T1):.12f} (claimed < 0.2383)")
print(f"        tail of the definition beyond t = 40 is {float(W_T1 - partial40):.3e} (the text borrows the bound 5.7e-4)")
assert float(W_T1) + 1e-12 < 0.119134

# the numbers p_r
p = [Fraction(1)]
for r in range(60):
    p.append((1 - p[-1]) / 2)
# from the definition as well
import itertools
for r in range(0, 13):
    cnt = sum(1 for s in itertools.product((1, -1), repeat=r) if sum(s) % 3 == 0)
    assert Fraction(cnt, 2 ** r) == p[r]
    assert p[r] - Fraction(1, 3) == Fraction(2, 3) * Fraction(-1, 2) ** r
print("p_r, r = 0..8:", ", ".join(str(x) for x in p[:9]))
print("max p_r, r >= 5:", max(p[5:]), " min p_r, r >= 4:", min(p[4:]), " (checked to r = 60; the deviation (2/3)(-1/2)^r decreases)")
Wf = W_T1 + Fraction(1, 10 ** 100)
print("m = 3: 1 - 2 p_3 =", 1 - 2 * p[3], "; m = 4: 1 - 2 p_4 =", 1 - 2 * p[4])
print("m >= 5: least of p_(m-1) - 2W over m = 5..60:", min(float(p[m - 1] - 2 * Wf) for m in range(5, 61)),
      "at m =", min(range(5, 61), key=lambda m: p[m - 1] - 2 * Wf))
print("2*(11/32) + 0.2383 =", 2 * 11 / 32 + 0.2383, "; 5/16 - 0.2383 =", 5 / 16 - 0.2383)
