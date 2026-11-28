"""Constants of result.md that are not in bound.py (exact fractions where it matters).

 (1) Lemma E': the largest value of sum over v != 0 of P_a(v) P_b(v), a, b even, 2 <= a, b <= 30
     (P_r(v) = the share of the signings of r elements with sum v), and c*_32 = C(32, 17)/2^32.
 (2) Theorem 5: Sigma_even = Sigma_1 - sum over prime powers p^j of 2^-(N-2) (1 - 2^-(p-2)) - (1/4 - 17/128),
     N(p^j) = j(p-1) + 1, and the constants sqrt(2/pi) (1 + Sigma_even).
 (3) the table T2(m), m = 3..46, of the second text (quarter/two/result.md, section 5), typed from that file:
     the largest T2(m) sqrt(m), over even and over odd m.
 (4) the facts on c_r used in section 2, checked on a range (c_(x-2) <= 2 c_x; c_r <= sqrt(2/(pi r)); the product lemma).
"""
import sys, math
from fractions import Fraction
from itertools import combinations_with_replacement
sys.path.insert(0, '/home/agent3/lean/lift-check/even/root/one')
from bound import c_frac, cnt_table, tail_beyond, odd_primes, NTOP

def P(r, v):
    return Fraction(math.comb(r, (r + v) // 2), 2 ** r) if abs(v) <= r and (r + v) % 2 == 0 else Fraction(0)

# (1)
best = (Fraction(0), None)
for a in range(2, 31, 2):
    for b in range(a, 31, 2):
        s = sum(P(a, v) * P(b, v) for v in range(-a, a + 1) if v != 0)
        if s > best[0]: best = (s, (a, b))
cs32 = Fraction(math.comb(32, 17), 2 ** 32)
print(f"(1) largest sum over v != 0 of P_a(v) P_b(v), a, b even <= 30: {best[0]} = {float(best[0]):.6f} at (a, b) = {best[1]};"
      f"  c*_32 = {float(cs32):.6f} < 17/128 = {17 / 128:.6f}: {cs32 < Fraction(17, 128)}")
cstar = [Fraction(math.comb(r, r // 2 + 1), 2 ** r) for r in range(2, 200, 2)]
print("    c*_r <= 1/4 for even r in [2, 198] and non-increasing from r = 4:", all(x <= Fraction(1, 4) for x in cstar) and all(cstar[i + 1] <= cstar[i] for i in range(1, len(cstar) - 1)))

# (2)
cnt = cnt_table(NTOP); tail = tail_beyond(NTOP)
S1 = sum(Fraction(cnt[N], 2 ** (N - 2)) for N in cnt)
pp = Fraction(0); ppg = Fraction(0); npp = {}
for p in odd_primes(NTOP):
    j = 1
    while j * (p - 1) + 1 <= NTOP:
        N = j * (p - 1) + 1
        pp += Fraction(1, 2 ** (N - 2)); ppg += Fraction(1, 2 ** (N - 2 + p - 2)); npp[N] = npp.get(N, 0) + 1
        j += 1
assert all(npp[N] <= cnt[N] for N in npp)
Seven = S1 - pp + ppg - (Fraction(1, 4) - Fraction(17, 128))
s2pi = math.sqrt(2 / math.pi)
print(f"(2) Sigma_1 (N <= {NTOP}) = {float(S1):.9f}, tail beyond at most {tail:.3e}")
print(f"    prime powers: sum of 2^-(N-2) = {float(pp):.9f}; with the factor 2^-(p-2): {float(ppg):.9f}")
print(f"    Sigma_even <= {float(Seven) + tail:.9f};  sqrt(2/pi) (1 + Sigma_even) <= {s2pi * (1 + float(Seven) + tail):.6f}")
print(f"    without Lemma E' (3 at rank 1 with 1/4): Sigma <= {float(S1 - pp + ppg) + tail:.9f}; constant <= {s2pi * (1 + float(S1 - pp + ppg) + tail):.6f}")
print(f"    for comparison: sqrt(2/pi) Sigma_1 <= {s2pi * (float(S1) + tail):.6f} (odd m), sqrt(2/pi) (1 + Sigma_1) <= {s2pi * (1 + float(S1) + tail):.6f} (even m, Theorem 4)")

# (3)
T2 = {3: Fraction(1, 4), 4: Fraction(3, 8), 5: Fraction(5, 16), 6: Fraction(3, 8), 7: Fraction(5, 16), 8: Fraction(3, 8),
      9: Fraction(71, 256), 10: Fraction(47, 128), 11: Fraction(265, 1024), 12: Fraction(707, 2048), 13: Fraction(1033, 4096),
      14: Fraction(175, 512), 15: Fraction(1971, 8192), 16: Fraction(10737, 32768),
      17: 0.249557, 18: 0.366203, 19: 0.236824, 20: 0.349281, 21: 0.221837, 22: 0.334183, 23: 0.208458, 24: 0.320811,
      25: 0.196207, 26: 0.304530, 27: 0.185741, 28: 0.290239, 29: 0.175215, 30: 0.278365, 31: 0.166942, 32: 0.266245,
      33: 0.159746, 34: 0.255903, 35: 0.153502, 36: 0.248232, 37: 0.147865, 38: 0.239581, 39: 0.142856, 40: 0.231802,
      41: 0.138279, 42: 0.226072, 43: 0.134185, 44: 0.219407, 45: 0.130451, 46: 0.213360}
for par in (0, 1):
    v, m = max(((float(T2[m]) + 1e-6) * math.sqrt(m), m) for m in T2 if m % 2 == par)
    print(f"(3) largest (T2(m) + 10^-6) sqrt(m) over {'even' if par == 0 else 'odd'} m in [3, 46]: {v:.5f} at m = {m}")
print("    odd m in [3, 46] with (T2(m) + 10^-6) sqrt(m) >= 1:", [m for m in T2 if m % 2 == 1 and (float(T2[m]) + 1e-6) * math.sqrt(m) >= 1])

# (4)
c = c_frac(4000)
def cc(x): return c[x] if x >= 1 else Fraction(1)
ok1 = all(cc(x - 2) <= 2 * cc(x) for x in range(-5, 4001))
ok2 = all(float(c[r]) <= math.sqrt(2 / (math.pi * r)) for r in range(1, 4001))
ok3 = all(c[r + 1] <= c[r] for r in range(1, 4000))
n_tuples = 0; ok4 = True
for n in range(1, 6):
    for tup in combinations_with_replacement(range(1, 15 if n >= 4 else 41), n):
        prod = Fraction(1)
        for a in tup: prod *= c[a]
        n_tuples += 1
        if prod > Fraction(1, 2 ** (n - 1)) * cc(sum(tup) - 2 * (n - 1)): ok4 = False
print(f"(4) c_(x-2) <= 2 c_x for -5 <= x <= 4000: {ok1};  c_r <= sqrt(2/(pi r)) for r <= 4000: {ok2};  c non-increasing: {ok3};"
      f"  product lemma on {n_tuples} tuples (n <= 5): {ok4}")

# (5) the table b(m), m = 3..26, of the first text (quarter/one/table.out), typed from that file, with T2 of (3):
b1 = {3: Fraction(1, 4), 4: Fraction(3, 8), 5: Fraction(1, 4), 6: Fraction(3, 8), 7: Fraction(15, 64), 8: Fraction(47, 128),
      9: Fraction(55, 256), 10: Fraction(183, 512), 11: Fraction(105, 512), 12: Fraction(699, 2048), 13: Fraction(831, 4096),
      14: Fraction(2759, 8192), 15: Fraction(905, 4096), 16: Fraction(11431, 32768), 17: Fraction(14123, 65536),
      18: Fraction(22301, 65536), 19: Fraction(27631, 131072), 20: Fraction(86387, 262144), 21: Fraction(108221, 524288),
      22: Fraction(672239, 2097152), 23: Fraction(212387, 1048576), 24: Fraction(1307819, 4194304),
      25: Fraction(1670387, 8388608), 26: Fraction(2555035, 8388608)}
def both(m):
    v = float(T2[m]) + 1e-6
    if m in b1: v = min(v, float(b1[m]))
    return v
for par in (0, 1):
    v, m = max((both(m) * math.sqrt(m), m) for m in T2 if m % 2 == par)
    print(f"(5) largest min(b(m), T2(m) + 10^-6) sqrt(m) over {'even' if par == 0 else 'odd'} m in [3, 46]: {v:.5f} at m = {m}")
v, m = max((float(b1[m]) * math.sqrt(m), m) for m in b1 if m % 2 == 1)
print(f"    largest b(m) sqrt(m) over odd m in [3, 25]: {v:.5f} at m = {m};  largest (T2(m) + 10^-6) sqrt(m) over odd m in [27, 45]: "
      f"{max((float(T2[m]) + 1e-6) * math.sqrt(m) for m in T2 if m % 2 == 1 and m >= 27):.5f}")
print("    even m in [3, 46]:", ' '.join(f"{m}:{both(m) * math.sqrt(m):.4f}" for m in T2 if m % 2 == 0))
