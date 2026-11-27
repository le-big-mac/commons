# w_check.py -- Lemma W of sign-four-result.md, recomputed from the definition of mu.
#   mu(d) = max over primes p | d of v_p(d)*(p-1);  W = sum over odd d > 1 of 2^(-mu(d)).
# Part 1: every odd d <= D, mu from the definition by a sieve over prime powers (no product formula).
# Part 2: A(t) = #{odd d : mu(d) <= t} by enumerating the divisors of n'_{t+1} and of n'_{t+3} with mu by factoring.
# Part 3: partial sums with exact fractions; the fractions quoted in the result file.
# Part 4: the tail estimate, step by step; my own upper bounds for W.
import sys, math
from fractions import Fraction
import numpy as np
from rlib import factor, divisors, mu, nprime

D = int(sys.argv[1]) if len(sys.argv) > 1 else 30_000_000

# ---------- Part 1: sieve ----------
print("Part 1. mu(d) for every odd d <= %d, from the definition (sieve over prime powers)" % D)
isp = np.ones(D + 1, dtype=bool)
isp[:2] = False
for q in range(2, int(D ** 0.5) + 1):
    if isp[q]:
        isp[q * q::q] = False
primes = np.nonzero(isp)[0]
CAP = 30000                      # mu values above CAP are stored as CAP (only small values are tallied)
muarr = np.zeros(D + 1, dtype=np.int16)
for p in primes:
    p = int(p)
    if p == 2:
        continue
    pk, k = p, 1
    while pk <= D:
        val = min(k * (p - 1), CAP)
        seg = muarr[pk::pk]
        np.maximum(seg, val, out=seg)
        pk *= p
        k += 1
odd = muarr[1::2]                # d = 1, 3, 5, ...
TMAX = 60
tally = np.bincount(odd[1:].astype(np.int64), minlength=CAP + 1)   # d > 1
print("  number of odd d in (1, D] with mu(d) = t:")
for t in range(2, 26, 2):
    print("    t = %2d : %d" % (t, tally[t]))
assert all(tally[t] == 0 for t in range(1, TMAX, 2)), "mu is even"
part = sum(Fraction(int(tally[t]), 2 ** t) for t in range(2, 2001, 2))
print("  sum of 2^(-mu(d)) over odd 1 < d <= D with mu <= 2000 = %.8f  (a lower bound for W)" % float(part))
# spot check of the sieve against factoring
import random
rng = random.Random(1)
for _ in range(20000):
    d = 2 * rng.randrange(1, D // 2) + 1
    assert min(mu(d), CAP) == int(muarr[d]), d
print("  sieve agrees with mu(d) by trial division on 20000 random odd d")
# compare with the divisors of n'_{t+1} that are <= D
for t in range(2, 26, 2):
    N = nprime(t + 1)
    ds = [d for d in divisors(N) if 1 < d <= D]
    c = sum(1 for d in ds if mu(d) == t)
    lows = sum(1 for d in ds if mu(d) > t)
    assert lows == 0
    assert c == tally[t], (t, c, tally[t])
    print("    t = %2d : n'_%d = %d %s; its divisors d <= D with mu(d) = t: %d  (equal to the sieve count)"
          % (t, t + 1, N, "<= D, complete" if N <= D else "> D, partial", c))

# ---------- Part 2: A(t) by enumeration ----------
print("Part 2. A(t) by enumeration of divisors (mu by factoring) against the product formula")


def A_formula(t):
    r = 1
    for p in range(3, t + 2, 2):
        if all(p % q for q in range(3, int(p ** 0.5) + 1, 2)):
            r *= 1 + t // (p - 1)
    return r


def divisors_big(N):
    return divisors(N)


enumA = {}
for t in range(0, 28, 2):
    N = nprime(t + 1)
    N3 = nprime(t + 3)
    ds = divisors_big(N3)
    mus = {d: mu(d) for d in ds}
    a = sum(1 for d in ds if mus[d] <= t)
    # the d with mu <= t among the divisors of n'_{t+3} are exactly the divisors of n'_{t+1}
    assert all((N % d == 0) == (mus[d] <= t) for d in ds)
    # and "the divisors of n'_m are exactly the odd d with mu(d) <= m-1", m = t+3
    assert all(mus[d] <= t + 2 for d in ds)
    assert a == A_formula(t), (t, a, A_formula(t))
    enumA[t] = a
    print("  t = %2d  A(t) = %d   (divisors of n'_%d: %d)" % (t, a, t + 3, len(ds)))
table = {2: 2, 4: 6, 6: 16, 8: 30, 10: 72, 12: 336, 14: 384, 16: 1080, 18: 3200, 20: 6336, 22: 13824, 24: 32760,
         26: 35280, 28: 86400, 30: 294912, 32: 528768, 34: 559872, 36: 3064320, 38: 3225600, 40: 9313920}
assert all(A_formula(t) == v for t, v in table.items())
print("  the table of A(t), t = 2..40, in the result file equals the product formula; t <= 26 also by enumeration")
# W_m by enumeration: sum over divisors d > 1 of n'_m of 2^(-mu(d))
for m in range(2, 28):
    N = nprime(m)
    s = sum(Fraction(1, 2 ** mu(d)) for d in divisors_big(N) if d > 1)
    tt = m - 1 if (m - 1) % 2 == 0 else m - 2
    s2 = sum(Fraction(A_formula(t) - A_formula(t - 2), 2 ** t) for t in range(2, tt + 1, 2))
    assert s == s2, m
print("  W_m (sum over the divisors d > 1 of n'_m, mu by factoring) equals the partial sum up to t = 2*floor((m-1)/2), m = 2..27")

# ---------- Part 3: partial sums ----------
print("Part 3. partial sums S(T) = sum over even t <= T of (A(t) - A(t-2)) / 2^t")


def S(T):
    return sum(Fraction(A_formula(t) - A_formula(t - 2), 2 ** t) for t in range(2, T + 1, 2))


quoted = {2: Fraction(1, 4), 4: Fraction(1, 2), 6: Fraction(21, 32), 8: Fraction(91, 128), 10: Fraction(385, 512),
          12: Fraction(209, 256), 40: Fraction(7253932573, 8589934592), 60: Fraction(7428069951793, 8796093022208)}
for T, q in quoted.items():
    print("  T = %2d  S = %s = %.12f   quoted %s : %s" % (T, S(T), float(S(T)), q, "equal" if S(T) == q else "DIFFERENT"))
for T in (80, 100, 200, 400, 1000):
    print("  T = %4d  S = %.30f" % (T, float(S(T))), " (first 40 digits: %s)" % str(S(T).numerator * 10 ** 40 // S(T).denominator))

# ---------- Part 4: tail ----------
print("Part 4. the tail")
# (i) count of j = +-1 mod 6, 5 <= j <= y, against floor((y+1)/6) + floor((y-1)/6) and against (y-1)/3, y = k/8
bad = 0
for k in range(24, 8 * 3000):
    y = Fraction(k, 8)
    cnt = sum(1 for j in range(5, int(y) + 1) if j % 6 in (1, 5))
    f = math.floor((y + 1) / 6) + math.floor((y - 1) / 6)
    if cnt != f or cnt > (y - 1) / 3:
        bad += 1
print("  count of j = +-1 (mod 6) in [5, y] equals floor((y+1)/6) + floor((y-1)/6) and is <= (y-1)/3 for y = 3, 3.125, .., 3000: %d failures" % bad)
# (ii) pi'(y) <= 1 + (y-1)/3 for integers 3 <= y <= D (enough: pi' is constant between integers, the bound increases)
pi_odd = np.cumsum(isp[: 2_000_001]) - 1          # number of odd primes <= y
y = np.arange(2_000_001)
ok = (3 * pi_odd[3:] <= 3 + (y[3:] - 1)).all()
print("  pi'(y) <= 1 + (y-1)/3 for every integer 3 <= y <= 2000000:", bool(ok))
# (iii) A(t) as a product over k
for t in range(2, 202, 2):
    num, den = 1, 1
    for k in range(1, t // 2 + 1):
        e = int(pi_odd[t // k + 1])          # pi'(t/k + 1) = pi'(floor(t/k) + 1)
        num *= (k + 1) ** e
        den *= k ** e
    assert Fraction(num, den) == A_formula(t), t
print("  A(t) = prod_{k=1}^{t/2} ((k+1)/k)^{pi'(t/k+1)} for even t <= 200: exact")
# (iv) K
import mpmath
mpmath.mp.dps = 40
N = 2000
part2000 = mpmath.fsum(mpmath.log1p(mpmath.mpf(1) / k) / k for k in range(1, N))
print("  sum_{k<2000} ln(1+1/k)/k =", mpmath.nstr(part2000, 15), "; 1/1999 =", mpmath.nstr(mpmath.mpf(1) / 1999, 8))
N = 1_000_000
partN = mpmath.fsum(mpmath.log1p(mpmath.mpf(1) / k) / k for k in range(1, N))
# for k >= N: 1/k^2 - 1/(2k^3) < ln(1+1/k)/k < 1/k^2;  sum_{k>=N} 1/k^2 < 1/(N-1), > 1/N
Klo = partN + mpmath.mpf(1) / N - mpmath.mpf(1) / (2 * (N - 1) ** 2)
Khi = partN + mpmath.mpf(1) / (N - 1)
print("  K = sum_{k>=1} ln(1+1/k)/k lies in (%s, %s)" % (mpmath.nstr(Klo, 12), mpmath.nstr(Khi, 12)))
assert Khi < mpmath.mpf("1.2578")
x = mpmath.exp(2 * mpmath.mpf("1.2578") / 3) / 4
print("  x = e^(2*1.2578/3)/4 =", mpmath.nstr(x, 10), "(< 0.5783:", bool(x < mpmath.mpf("0.5783")), ")")
print("  growth: A(t) <= (t/2+1)*2^(c t) with c = K/(3 ln 2) <", mpmath.nstr(mpmath.mpf("1.2578") / (3 * mpmath.log(2)), 6))
# (v) A(t) <= (t/2+1) e^{K t/3}, checked
worst = 0
for t in range(2, 2002, 2):
    lhs = mpmath.log(A_formula(t))
    rhs = mpmath.log(t // 2 + 1) + Khi * t / 3
    assert lhs <= rhs, t
    worst = max(worst, float(lhs / rhs))
print("  ln A(t) <= ln(t/2+1) + K t/3 for every even t <= 2000 (largest ratio %.4f)" % worst)
# (vi) the closed form of the tail
x0 = mpmath.mpf("0.5783")
for U in (21, 31):
    closed = x0 ** U * ((U + 1) - U * x0) / (1 - x0) ** 2
    direct = mpmath.fsum((u + 1) * x0 ** u for u in range(U, 2000))
    print("  sum_{u>=%d} (u+1) x^u at x = 0.5783: closed form %s, summed %s" % (U, mpmath.nstr(closed, 8), mpmath.nstr(direct, 8)))
# (vii) upper bounds for W
print("  upper bounds for W = S(T) + tail(T):")
for T in (40, 60, 100, 200, 400):
    U = T // 2 + 1
    tail = x0 ** U * ((U + 1) - U * x0) / (1 - x0) ** 2
    print("    T = %3d: S(T) = %.15f, tail < %s, W < %s" % (T, float(S(T)), mpmath.nstr(tail, 4), mpmath.nstr(mpmath.mpf(S(T).numerator) / S(T).denominator + tail, 18)))
# (viii) a cruder tail of my own that uses only "odd primes are odd numbers": pi'(y) <= (y-1)/2, so
#        ln A(t) <= (t/2) * sum_k ln(1+1/k)/k <= K t/2 and A(t) 2^(-t) <= r^t, r = e^(K/2)/2 < 1.
r = mpmath.exp(mpmath.mpf("1.2578") / 2) / 2
print("  cruder bound: r = e^(K/2)/2 <", mpmath.nstr(r, 8))
for t in range(2, 2002, 2):
    assert mpmath.log(A_formula(t)) <= Khi * t / 2
for T in (200, 400, 1000):
    tail = r ** (T + 2) / (1 - r ** 2)
    print("    T = %4d: W < S(T) + r^(T+2)/(1-r^2) = %s  (tail %s)" % (T, mpmath.nstr(mpmath.mpf(S(T).numerator) / S(T).denominator + tail, 18), mpmath.nstr(tail, 4)))
print("  1 - W > %.6f" % (1 - float(S(1000)) - 1e-12))
