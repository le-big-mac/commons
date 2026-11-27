# Referee's recomputation for item 5 of section 3: W_m, p_m, the shares 1 - 2 p_m - 2 W_m, the bound for
# every m >= 5, and p_m + W_m (item 3).  Exact fractions.  Imports nothing of the author's.
#
# mu(e) = max over the primes q | e of v_q(e) * (q - 1);  W_m = sum of 2^(-mu(e)) over the e > 1 with all
# prime factors >= 5 and mu(e) <= m - 1.
from fractions import Fraction as Fr
import itertools

def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % r for r in range(2, int(p ** 0.5) + 1))]

def mu_by_factoring(e):
    """mu(e) from the factorisation of e by trial division; None if 2 or 3 divides e."""
    if e % 2 == 0 or e % 3 == 0:
        return None
    best, q = 0, 5
    while q * q <= e:
        if e % q == 0:
            v = 0
            while e % q == 0:
                e //= q
                v += 1
            best = max(best, v * (q - 1))
        q += 2
    if e > 1:
        best = max(best, e - 1)
    return best

def A_formula(t):
    """the product formula of Lemma L3 (c): number of e >= 1, prime factors >= 5, mu(e) <= t."""
    r = 1
    for p in primes_upto(t + 1):
        if p >= 5:
            r *= 1 + t // (p - 1)
    return r

def list_by_exponents(t):
    """all e >= 1 with prime factors >= 5 and mu(e) <= t, listed through their exponent vectors,
    with mu recomputed from the vector; returns {mu: count}."""
    ps = [p for p in primes_upto(t + 1) if p >= 5]
    counts = {}
    def rec(i, cur):
        if i == len(ps):
            counts[cur] = counts.get(cur, 0) + 1
            return
        p = ps[i]
        v = 0
        while v * (p - 1) <= t:
            rec(i + 1, max(cur, v * (p - 1)))
            v += 1
    rec(0, 0)
    return counts

print("1. The e* listed directly.")
# (i) every integer up to the largest e with mu <= 12 (5^3 * 7^2 * 11 * 13 = 875875), mu by trial division
BOUND = 5 ** 3 * 7 ** 2 * 11 * 13
by_mu = {}
for e in range(1, BOUND + 1):
    mu = mu_by_factoring(e)
    if mu is not None and mu <= 12:
        by_mu[mu] = by_mu.get(mu, 0) + 1
cum = 0
for t in range(0, 13, 2):
    cum += by_mu.get(t, 0)
    assert cum == A_formula(t), (t, cum, A_formula(t))
    print(f"   t={t:2d}: e with mu = t (integers <= {BOUND} factored): {by_mu.get(t,0):4d}; with mu <= t: {cum:4d}; product formula A(t) = {A_formula(t)}")
assert not any(t % 2 for t in by_mu), "an odd mu"
small = sorted(e for e in range(2, 2000) if (mu_by_factoring(e) or 99) <= 8)
print("   the e* > 1 with mu <= 8:", small, " (their mu:", [mu_by_factoring(e) for e in small], ")")
# (ii) by exponent vectors up to t = 40
tot40 = 0
for t in range(0, 41, 2):
    c = list_by_exponents(t)
    assert sum(c.values()) == A_formula(t), t
    tot40 = sum(c.values())
print(f"   exponent-vector listing agrees with the product formula for every even t <= 40; number with mu <= 40: {tot40}")

def W_cut(m):
    """sum of 2^(-mu) over e > 1 with mu <= m - 1 (mu is even)."""
    s = Fr(0)
    t = 2
    while t <= m - 1:
        s += Fr(A_formula(t) - A_formula(t - 2), 2 ** t)
        t += 2
    return s

def p(r):
    x = Fr(1)
    for _ in range(r):
        x = (1 - x) / 2
    return x

# p_r checked against a direct count of the sign vectors
for r in range(0, 15):
    cnt = sum(1 for s in itertools.product((1, -1), repeat=r) if sum(s) % 3 == 0)
    assert Fr(cnt, 2 ** r) == p(r), r
print("2. p_r = (1 - p_(r-1))/2 agrees with a count of all sign vectors for r <= 14.")

print("3. m, p_m, W_m, share = 1 - 2 p_m - 2 W_m, and p_m + W_m (the bound for the bad share on odd n):")
for m in range(5, 17):
    sh = 1 - 2 * p(m) - 2 * W_cut(m)
    print(f"   m={m:2d}  p_m={p(m)}  W_m={W_cut(m)}  share={sh} = {float(sh):.6f}   p_m+W_m={p(m)+W_cut(m)} = {float(p(m)+W_cut(m)):.6f}")
claimed = {5: Fr(1, 4), 6: Fr(3, 16), 7: Fr(5, 32), 8: Fr(9, 64), 9: Fr(17, 128), 10: Fr(33, 256),
           11: Fr(61, 512), 12: Fr(121, 1024)}
ok = all(1 - 2 * p(m) - 2 * W_cut(m) == v for m, v in claimed.items())
print("   the note's 1/4, 3/16, 5/32, 9/64, 17/128, 33/256, 61/512, 121/1024 for m = 5..12:", "all equal" if ok else "DIFFER")
print("   W_5 = W_6 =", W_cut(5), W_cut(6))

# 4. every m >= 5.  Exact for m <= M; beyond M a tail bound proved here:
#    #{e : mu(e) <= t} = prod_{k=1}^{t/4} ((k+1)/k)^(pi5(t/k + 1)),  pi5(y) = number of primes in [5, y] <= (y - 1)/3
#    (they are = +-1 mod 6), so ln A(t) <= (t/3) * K with K = sum_{k>=1} ln(1 + 1/k)/k, and
#    A(t) 2^(-t) <= x^(t/2), x = exp(2K/3)/4.  The terms with mu = t add up to at most A(t) 2^(-t).
import math
N = 200000
K_upper = sum(math.log1p(1.0 / k) / k for k in range(1, N)) + 1.0 / (N - 1) + 1e-9   # tail < sum 1/k^2 < 1/(N-1)
x = math.exp(2 * K_upper / 3) / 4
assert all(sum(1 for q in range(5, y + 1) if all(q % r for r in range(2, q))) <= (y - 1) / 3 for y in range(3, 400))
assert all(Fr(A_formula(t), 2 ** t) <= Fr(x).limit_denominator(10 ** 12) ** (t // 2) + Fr(1, 10 ** 30) for t in range(2, 301, 2))
M = 200
WM = W_cut(M + 1)                      # all terms with mu <= M
tail = x ** (M // 2 + 1) / (1 - x)     # terms with mu >= M + 2
print(f"4. K < {K_upper:.6f}, x = exp(2K/3)/4 < {x:.6f}; W up to mu = {M}: {float(WM):.12f}; the rest < {tail:.3e}")
Winf_upper = float(WM) + tail + 1e-15
print(f"   so W(no 3) < {math.ceil(Winf_upper * 1e11) / 1e11:.11f}   (the texts: 0.1185646982..., < 0.118569); up to mu = 60: {float(W_cut(61)):.12f}")
least = min((1 - 2 * p(m) - 2 * W_cut(m), m) for m in range(5, M + 1))
print(f"   least share 1 - 2 p_m - 2 W_m over 5 <= m <= {M}: {float(least[0]):.10f} at m = {least[1]}")
beyond = Fr(1, 3) - Fr(4, 3) / 2 ** (M + 1) - 2 * Fr(Winf_upper).limit_denominator(10 ** 15)
print(f"   for m > {M}: share > 1/3 - (4/3)/2^{M+1} - 2 W(no 3) > {float(beyond):.10f}")
print("   'more than 0.0961 for every m >= 5':", least[0] > Fr(961, 10000) and beyond > Fr(961, 10000))
print(f"   would 'more than 0.0962' hold?  limit 1/3 - 2 W(no 3) = {1/3 - 2*float(WM):.10f}; least over m <= {M} = {float(least[0]):.10f}")
most = max((p(m) + W_cut(m), m) for m in range(5, M + 1))
print(f"   largest p_m + W_m over 5 <= m <= {M}: {float(most[0]):.10f} at m = {most[1]}; beyond: < {1/3 + (2/3)/2**(M+1) + Winf_upper:.10f}")
print("   'beta(m) < 0.452 for every m >= 5':", most[0] < Fr(452, 1000) and 1 / 3 + (2 / 3) / 2 ** (M + 1) + Winf_upper < 0.452)
print("   the note's step for m > 60: 1 - 2 (1/3 + (2/3)/2^61) - 2 * 0.118569 =", float(1 - 2 * (Fr(1, 3) + Fr(2, 3) / 2 ** 61) - 2 * Fr(118569, 10 ** 6)))
least60 = min((1 - 2 * p(m) - 2 * W_cut(m), m) for m in range(5, 61))
print(f"   least share over 5 <= m <= 60: {float(least60[0]):.10f} at m = {least60[1]}")
