"""(1) inequalities (c) and the one of Lemma 3 (ii), exact or with a safe margin; (2) arithmetic of section 4;
(3) the tools against brute force; (4) the two quoted lower bounds for K_even, K_odd recomputed."""
import sys, math, random
from fractions import Fraction
sys.path.insert(0, '/home/agent3/lean/lift-check/even/limit/referee')
from lib import *

# (1) (c): sqrt(2/(pi(r+2))) <= c_r <= sqrt(2/(pi r)), compared as squares against rational bounds of pi
PI_LO = Fraction(314159265358979, 10 ** 14); PI_HI = PI_LO + Fraction(1, 10 ** 14)
bad = 0; worst_lo = None; worst_hi = None
for r in range(1, 4001):
    cr = c(r)
    lo_ok = cr * cr * PI_LO * (r + 2) >= 2      # c_r^2 >= 2/(pi (r+2))  holds if true with the smaller pi
    hi_ok = cr * cr * PI_HI * r <= 2            # c_r^2 <= 2/(pi r)      holds if true with the larger pi
    if not (lo_ok and hi_ok): bad += 1; print("(c) FAILS or too close at r =", r, lo_ok, hi_ok)
    if r >= 2 and c(r) > c(r - 1): bad += 1; print("monotony fails", r)
print(f"(c): sqrt(2/(pi(r+2))) <= c_r <= sqrt(2/(pi r)) and c non-increasing, r = 1..4000: failures {bad}")
bad = 0; worst = 0
for m in range(2, 4001):
    q = c((m + 1) // 2) / c(m)
    worst = max(worst, q)
    if q > 2: bad += 1
print(f"Lemma 3 (ii): c_ceil(m/2) <= 2 c_m for m = 2..4000: failures {bad}; largest quotient {float(worst):.6f}")
bad = 0
for m in range(1, 400):
    for s in range(1, m + 1):
        if (c(s) / c(m)) ** 2 > Fraction(m + 2, s): bad += 1
print(f"(c): c_s/c_m <= sqrt((m+2)/s), 1 <= s <= m < 400: failures {bad}")

# (2) arithmetic
k = math.sqrt(2 / math.pi)
print(f"sqrt(2/pi) = {k:.10f};  1.2699/sqrt(2/pi) = {1.2699 / k:.6f};  0.8084/sqrt(2/pi) = {0.8084 / k:.6f}")
print(f"78764625/67108864 = {78764625 / 67108864:.8f} (67108864 = 2^26: {67108864 == 2 ** 26});  337/512 = {337 / 512:.8f}")
print(f"sqrt(2/pi)*78764625/67108864 = {k * 78764625 / 67108864:.6f};  sqrt(2/pi)*337/512 = {k * 337 / 512:.6f}")
print("3-chain values:", [float(Fraction(*t)) for t in ((9, 8), (37, 32), (149, 128), (597, 512))], " 7/6 =", 7 / 6)

# (3) tools against brute force (float evaluation at roots of unity)
random.seed(12345); cases = 0
for n in (1, 3, 5, 9, 15, 21, 27, 45, 63, 105):
    for _ in range(12):
        m = random.randint(1, 13)
        if random.random() < 0.6 and n > 1:
            pool = random.sample(range(n), min(n, random.randint(1, 4))) ; p = random.choice([q for q in (3, 5, 7) if n % q == 0])
            pool += [(pool[0] + j * (n // p)) % n for j in range(p)]
            xs = [random.choice(pool) for _ in range(m)]
        else: xs = [random.randrange(n) for _ in range(m)]
        s1, _ = share(n, [(b, 1) for b in xs]); s2 = brute_share(n, xs)
        assert s1 == s2, (n, xs, s1, s2)
        for d in divisors(n):
            if d > 1:
                a1, _ = share(n, [(b, 1) for b in xs], divs=[d]); a2 = brute_share(n, xs, divs=[d])
                assert a1 == a2, (n, xs, d, a1, a2)
                cases += 1
        cases += 1
print(f"share (reduction, multiplicities) = share (all signings, float roots): {cases} comparisons, all equal")

# (4) the quoted lower bounds
D105 = [15, 21, 30, 35, 42, 45, 60, 63, 70, 75, 84, 90]
k0, k1 = K(105, D105); print(f"Z_105, one element in each nonzero class modulo 3, 5, 7 (r = 12): K_0 = {k0}, K_1 = {k1}  (K_odd uses K_(r+1) = K_1)")
D135 = [5] * 2 + [10] * 2 + [15] * 2 + [30] * 2 + [45] * 4 + [90] * 4 + [27] * 4 + [54] * 4 + [81] * 4 + [108] * 4
k0, k1 = K(135, D135); print(f"Z_135, pairs at 5, 10, 15, 30, fours at 45, 90, 27, 54, 81, 108 (r = {len(D135)}): K_0 = {k0} = {float(k0):.8f}, K_1 = {k1}")
for L, D in ((3, [1, 1, 2, 2]), (9, [1, 1, 2, 2, 3, 3, 6, 6]), (27, [1, 1, 2, 2, 3, 3, 6, 6, 9, 9, 18, 18]), (81, [1, 1, 2, 2, 3, 3, 6, 6, 9, 9, 18, 18, 27, 27, 54, 54])):
    k0, k1 = K(L, D); print(f"Z_{L}, pairs {sorted(set(D))}: K_0 = {k0}, K_1 = {k1}")
