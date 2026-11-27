# Self-test of rlib: Phi_d against known values, exact test against complex evaluation, factorisation mod 2.
import random, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rlib import *

random.seed(11)
assert cyclo(1) == (-1, 1) and cyclo(2) == (1, 1) and cyclo(3) == (1, 1, 1) and cyclo(4) == (1, 0, 1)
assert cyclo(6) == (1, -1, 1) and cyclo(12) == (1, 0, -1, 0, 1) and cyclo(9) == (1, 0, 0, 1, 0, 0, 1)
assert min(cyclo(105)) == -2            # the first cyclotomic polynomial with a coefficient -2
for n in range(1, 200):
    assert sum(phi(d) for d in divisors(n)) == n
# X^n - 1 = product of Phi_d
for n in [12, 30, 36, 105, 120]:
    prod = [1]
    for d in divisors(n):
        P = cyclo(d)
        new = [0] * (len(prod) + len(P) - 1)
        for i, a in enumerate(prod):
            for j, b in enumerate(P):
                new[i + j] += a * b
        prod = new
    assert prod == [-1] + [0] * (n - 1) + [1]
cnt = bad = 0
for trial in range(4000):
    n = random.choice([6, 8, 10, 12, 14, 18, 20, 24, 30, 36, 40, 42, 60, 72, 90, 105, 120])
    m = random.randint(1, 8)
    if random.random() < 0.5:
        B = [random.randrange(n) for _ in range(m)]
    else:   # concentrated near a subgroup, so that vanishing happens
        g = random.choice([d for d in divisors(n) if d > 1])
        B = [(random.randrange(n // g) * g + random.choice([0, 0, 0, 1])) % n for _ in range(m)]
    s = [random.choice([1, -1]) for _ in range(m)]
    for d in divisors(n):
        e = bad_one(B, s, n, d)
        c = bad_one_complex(B, s, n, d)
        assert e == c, (n, B, s, d)
        cnt += 1
        bad += e
    # matrix version against single version
    bl = bad_levels(B, n)
    idx = sum((1 << i) for i in range(m) if s[i] == -1)
    for d in divisors(n):
        assert bool(bl[d][idx]) == bad_one(B, s, n, d)
print("exact test = complex evaluation on", cnt, "triples (signed multiset, d);", bad, "of them bad")
for e in [1, 3, 5, 7, 9, 15, 17, 21, 23, 31, 35, 45, 51, 63, 73, 85, 105]:
    fs = factors_mod2(e)
    print("e =", e, ": primes above 2:", len(fs), "of degree", ord2(e))
print("OK")
