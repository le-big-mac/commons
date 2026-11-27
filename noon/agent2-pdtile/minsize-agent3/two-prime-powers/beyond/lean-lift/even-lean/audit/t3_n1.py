"""N1' (sum_half_pow_mu_lt): for every finite set T of numbers t > 1 with 2 and 3 not dividing t,
sum over T of (1/2)^mu(t) < 1/8.   Exact rational arithmetic.

The supremum over all allowed T is W := the sum over ALL t > 1 prime to 6 (T is a finite set of distinct such t and
every term is positive).  So the statement is true iff W <= 1/8 (W itself is not attained).

A(s) := #{t >= 1 prime to 6 : mu(t) <= s} = prod over the primes p >= 5 with p - 1 <= s of (1 + floor(s / (p - 1)))
(mu(t) <= s iff v_p(t) <= s / (p - 1) for every prime p).  W = sum_{s >= 1} (A(s) - A(s-1)) / 2^s.

Tail, proved here (not taken from the plan):  the primes >= 5 are 6k - 1 or 6k + 1, so with K = floor(s / 6)
  A(s) <= prod_{k=1..K} (1 + floor(K/k)) * (1 + s/4) * prod_{k'=1..K} (1 + floor(K/k'))  <= (1 + s/4) * C(2K, K)^2
       <= (1 + s/4) * 16^K <= (1 + s/4) * 2^(2s/3),
and by summation by parts  sum_{s > S} (A(s) - A(s-1)) / 2^s <= (1/2) sum_{s > S} A(s) / 2^s
       <= (1/2) sum_{s > S} (1 + s/4) (4/5)^s        (2^(-1/3) <= 4/5 because (4/5)^3 = 0.512 >= 1/2)
        = (1/2) (4/5)^(S+1) (5 (1 + (S+1)/4) + 5).
The inequality A(s) <= (1 + s/4) 2^(2s/3) is also checked numerically for s <= 4000 (as integers, cubed).
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from math import comb
from ecore import factor, mu


def primes_upto(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b'\x00\x00'
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


PR = primes_upto(5000)


def A(s):
    r = 1
    for p in PR:
        if p < 5:
            continue
        if p - 1 > s:
            break
        r *= 1 + s // (p - 1)
    return r


# 1. mu as Lean has it, on the values the skeleton's check file uses
assert [mu(t) for t in [5, 7, 25, 35, 175]] == [4, 6, 8, 6, 8]
vals = [sum(Fraction(1, 2) ** mu(t) for t in T) for T in ([5], [5, 7, 35], [5, 7, 25, 35, 175])]
assert vals == [Fraction(1, 16), Fraction(3, 32), Fraction(13, 128)]
print("1. mu(5, 7, 25, 35, 175) = 4, 6, 8, 6, 8; sums for {5}, {5, 7, 35}, {5, 7, 25, 35, 175}: 1/16, 3/32, 13/128 "
      "(the values CheckEven.lean expects)")

# 2. the counting formula against a list of all t <= X prime to 6 (mu from the factorisation of each t)
X = 2_000_000
spf = list(range(X + 1))
for i in range(2, int(X ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, X + 1, i):
            if spf[j] == j:
                spf[j] = i


def mu_fast(t):
    best = 0
    while t > 1:
        p = spf[t]
        a = 0
        while t % p == 0:
            t //= p
            a += 1
        best = max(best, (p - 1) * a)
    return best


count = {}
partial_list = Fraction(0)
terms = 0
for t in range(5, X + 1):
    if t % 2 == 0 or t % 3 == 0:
        continue
    m = mu_fast(t)
    count[m] = count.get(m, 0) + 1
    terms += 1
for t in range(1, 3001):
    assert mu_fast(t) == mu(t)
assert all(m % 2 == 0 for m in count)
# for s <= 12 every t with mu(t) <= s is below X (the largest is 5^3 * 7^2 * 11 * 13 = 875875)
cum = 1
for s in range(0, 13):
    cum += count.get(s, 0)
    assert cum == A(s), (s, cum, A(s))
print(f"2. A(s) by the product formula equals the number of t <= {X} prime to 6 with mu(t) <= s, for s = 0..12: "
      f"{[A(s) for s in range(0, 13)]}; mu is even for every t prime to 6 below {X}")
low = sum(Fraction(c, 2 ** m) for m, c in count.items() if m <= 200)
rest = sum(c for m, c in count.items() if m > 200)
print(f"   sum over the numbers t in (1, {X}] prime to 6 with mu(t) <= 200 of (1/2)^mu(t) = {float(low):.12f} (a lower "
      f"bound for W; {terms} numbers in all, the {rest} with mu > 200 add less than {rest} / 2^200)")

# 3. W with a rigorous tail
S = 400
partial = Fraction(0)
prev = A(0)
assert prev == 1
for s in range(1, S + 1):
    a = A(s)
    partial += Fraction(a - prev, 2 ** s)
    prev = a
tail = Fraction(1, 2) * Fraction(4, 5) ** (S + 1) * (5 * (1 + Fraction(S + 1, 4)) + 5)
upper = partial + tail
for s in range(0, 4001):
    a = A(s)
    # a <= (1 + s/4) 2^(2s/3)  <=>  (4a)^3 <= (4 + s)^3 4^s
    assert (4 * a) ** 3 <= (4 + s) ** 3 * 4 ** s, s
    K = s // 6
    assert 4 * a <= (4 + s) * comb(2 * K, K) ** 2, s
print(f"3. W: partial sum up to mu = {S}: {float(partial):.15f}; tail after it at most {float(tail):.3e}; so "
      f"{float(partial):.13f} <= W <= {float(upper):.13f}")
print(f"   1/8 - (upper bound of W) = {float(Fraction(1, 8) - upper):.13f}  (> 0: {Fraction(1, 8) - upper > 0}); "
      f"W / (1/8) = {float(upper * 8):.6f}")
assert upper < Fraction(1, 8)
assert Fraction(118564, 10 ** 6) < partial and upper < Fraction(118565, 10 ** 6)
print("   so 0.118564 < W < 0.118565: no allowed T reaches 1/8; the margin is 0.006435...")
print("   A(s) <= (1 + s/4) 2^(2s/3) and A(s) <= (1 + s/4) C(2K, K)^2, K = floor(s/6), checked for s <= 4000")

# 4. the hypotheses are needed
print(f"4. needed hypotheses: (1/2)^mu(1) = {Fraction(1, 2) ** mu(1)} (so 1 < t), (1/2)^mu(3) = "
      f"{Fraction(1, 2) ** mu(3)} (so 3 not dividing t; also 9: {Fraction(1, 2) ** mu(9)}, 15: "
      f"{Fraction(1, 2) ** mu(15)}), (1/2)^mu(2) = {Fraction(1, 2) ** mu(2)} (so 2 not dividing t; 10: "
      f"{Fraction(1, 2) ** mu(10)}).  The largest single term allowed is (1/2)^mu(5) = {Fraction(1, 2) ** mu(5)}; "
      f"the terms with mu = 4, 6, 8, 10, 12: {[count.get(m, 0) for m in (4, 6, 8, 10, 12)]} numbers")

# 5. the numbers of the plan's route for Lean
b = [A(2 * u) for u in range(0, 20)]
plan_b = [1, 1, 2, 4, 6, 12, 48, 48, 120, 320, 576, 1152, 2520, 2520, 5760, 18432, 31104, 31104, 161280, 161280]
W6 = sum(Fraction(b[u] - b[u - 1], 4 ** u) for u in range(1, 20))
tail_plan = Fraction(5, 2) * Fraction(5, 7) ** 19
print(f"5. plan's route: b(0..19) equal to the plan's list: {b == plan_b}; W6(19) = {W6} (plan: 63653689/536870912: "
      f"{W6 == Fraction(63653689, 536870912)}) = {float(W6):.10f}; (5/2)(5/7)^19 = {float(tail_plan):.6f} (< 0.0042: "
      f"{tail_plan < Fraction(42, 10000)}); total {float(W6 + tail_plan):.6f} (< 0.1228: "
      f"{W6 + tail_plan < Fraction(1228, 10000)}; < 1/8: {W6 + tail_plan < Fraction(1, 8)})")
# b(u) <= a(u), a(u) = prod over odd primes p <= 2u + 1 of (1 + u // ((p - 1) // 2))  (SumAux.a of SignSum.lean)
def a_all(u):
    r = 1
    for p in PR:
        if p == 2:
            continue
        if p >= 2 * u + 2:
            break
        r *= 1 + u // ((p - 1) // 2)
    return r
ok = all(A(2 * u) <= a_all(u) and A(2 * u) * (1 + u) == a_all(u) for u in range(0, 400))
ok2 = all(Fraction(a_all(u), 4 ** u) <= Fraction(5, 7) ** u for u in range(0, 400))
print(f"   b(u) * (1 + u) = a(u) (the factor of the prime 3) for u < 400: {ok}; a(u)/4^u <= (5/7)^u for u < 400: {ok2}")
