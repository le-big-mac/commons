# t0_selfcheck.py -- checks rlib against two independent computations:
#  (1) "bad at d" against complex evaluation at a primitive d-th root of unity;
#  (2) "3-bad at d" against a long division of the whole mask by Phi_d with Python integers,
#      and against the norm-free definition through a second basis: S(zeta) in 3Z[zeta] iff
#      S = 3*Q + Phi_d * P, tested by reducing S modulo 3 and dividing by Phi_d over F_3.
import sys, random, cmath
from rlib import *

random.seed(12345)


def rem_python(coeffs, d):
    phi = cyclo(d)
    num = list(coeffs)
    dd = len(phi) - 1
    for i in range(len(num) - 1, dd - 1, -1):
        c = num[i]
        if c:
            for j in range(dd + 1):
                num[i - dd + j] -= c * phi[j]
    return num[:dd]


def rem_mod3(coeffs, d):
    phi = [c % 3 for c in cyclo(d)]
    num = [c % 3 for c in coeffs]
    dd = len(phi) - 1
    for i in range(len(num) - 1, dd - 1, -1):
        c = num[i] % 3
        if c:
            for j in range(dd + 1):
                num[i - dd + j] = (num[i - dd + j] - c * phi[j]) % 3
    return [c % 3 for c in num[:dd]]


cnt = bad = bad3 = 0
for trial in range(4000):
    n = random.choice([4, 6, 8, 10, 12, 15, 18, 20, 21, 24, 28, 30, 35, 36, 40, 45, 60, 70, 84, 90, 100, 105, 120, 140, 210])
    m = random.randint(1, 9)
    if random.random() < 0.5:
        # structured: few values, so that vanishing happens
        vals = random.sample(range(n), min(n, random.randint(1, 3)))
        step = n // random.choice([p for p in factor(n)])
        B = [(random.choice(vals) + step * random.randint(0, 6)) % n for _ in range(m)]
    else:
        B = [random.randrange(n) for _ in range(m)]
    Sg = signs(m, half=False)
    for d in divisors(n):
        b = bad_at(B, d, half=False)
        b3 = bad3_at(B, d, half=False)
        for s in random.sample(range(len(Sg)), min(len(Sg), 6)):
            coeffs = [0] * n
            for e, x in zip(Sg[s], B):
                coeffs[x] += int(e)
            r = rem_python(coeffs, d)
            z = cmath.exp(2j * cmath.pi / d)
            val = sum(int(e) * z ** x for e, x in zip(Sg[s], B))
            isbad = not any(r)
            assert isbad == bool(b[s]), (n, B, d, s)
            assert isbad == (abs(val) < 1e-9), (n, B, d, s, val)
            is3 = all(c % 3 == 0 for c in r)
            assert is3 == bool(b3[s])
            assert is3 == (not any(rem_mod3(coeffs, d)))
            cnt += 1
            bad += isbad
            bad3 += is3
print("pairs (signed multiset, level) compared:", cnt, " bad:", bad, " 3-bad:", bad3, " all agree")
# cyclotomic sanity
from math import gcd
for d in range(1, 200):
    assert len(cyclo(d)) - 1 == sum(1 for k in range(1, d + 1) if gcd(k, d) == 1)
print("degrees of Phi_d = phi(d) for d < 200: ok")
