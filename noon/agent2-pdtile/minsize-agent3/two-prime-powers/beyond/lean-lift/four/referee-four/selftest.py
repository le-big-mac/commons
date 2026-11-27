# selftest.py -- checks of rlib.py against independent computations.
import random, itertools, sys
import numpy as np
import sympy
from rlib import *

rng = random.Random(4)

# 1. cyclotomic polynomials against sympy
X = sympy.Symbol("X")
for d in range(1, 400):
    ref = sympy.Poly(sympy.cyclotomic_poly(d, X), X).all_coeffs()[::-1]
    assert [int(c) for c in ref] == cyclo(d), d
print("cyclo(d) equals sympy.cyclotomic_poly for d < 400")

# 2. the table X^x mod Phi_d against long division of X^x
for n in (9, 15, 27, 45, 63, 105, 225, 315):
    for d in divisors(n):
        T = xtable(n, d)
        for x in range(n):
            q, r = pdivmod([0] * x + [1], cyclo(d))
            r = r + [0] * (len(cyclo(d)) - 1 - len(r))
            assert list(T[x]) == r, (n, d, x)
print("table X^x mod Phi_d equals long division, 8 groups")

# 3. bad_at (table, all signings) against division of the signed mask polynomial itself
cnt = bad = 0
for trial in range(400):
    n = rng.choice([9, 15, 21, 25, 27, 35, 45, 63, 75, 105, 135, 225])
    m = rng.randint(1, 7)
    kind = rng.random()
    if kind < 0.4:
        B = [rng.randrange(n) for _ in range(m)]
    elif kind < 0.7:
        pool = [rng.randrange(n) for _ in range(2)]
        B = [rng.choice(pool) for _ in range(m)]
    else:
        g = rng.choice([d for d in divisors(n) if d > 1])
        B = [(rng.randrange(g) * (n // g) + rng.choice([0, 0, 1])) % n for _ in range(m)]
    E = signs(m)
    for d in divisors(n):
        v = bad_at(B, n, d, E)
        for r in range(1 << m):
            w = divides_direct(B, E[r], d)
            assert w == bool(v[r]), (n, B, d, r)
            cnt += 1
            bad += w
print("bad_at equals direct division: %d triples (multiset, signing, d), %d of them with Phi_d | S" % (cnt, bad))

# 4. evaluation at a complex root of unity (floating point) as a third look
import cmath
cnt = dis = 0
for trial in range(200):
    n = rng.choice([9, 15, 27, 45, 105])
    m = rng.randint(2, 6)
    B = [rng.randrange(n) for _ in range(m)]
    E = signs(m)
    for d in divisors(n):
        z = cmath.exp(2j * cmath.pi / d)
        v = bad_at(B, n, d, E)
        for r in range(1 << m):
            val = sum(int(E[r, k]) * z ** B[k] for k in range(m))
            cnt += 1
            if (abs(val) < 1e-9) != bool(v[r]):
                dis += 1
print("floating evaluation at exp(2 pi i/d): %d cases, %d disagreements" % (cnt, dis))

# 5. grid count against sign count
cnt = 0
for trial in range(300):
    n = rng.choice([3, 9, 15, 27, 45])
    m = rng.randint(1, 10)
    pool = [rng.randrange(n) for _ in range(rng.randint(1, 5))]
    B = [rng.choice(pool) for _ in range(m)]
    g1 = int(good_vector(B, n).sum())
    g2, tot = good_count_grid(B, n)
    assert g1 == g2 and tot == 1 << m, (n, B, g1, g2)
    cnt += 1
print("grid count equals sign count: %d multisets" % cnt)

# 6. known small cases
assert int(bad_at([0, 1, 2], 3, 3).sum()) == 2
assert int(bad_at([0, 1, 2, 3, 4], 5, 5).sum()) == 2
B, n = [0, 3, 7], 9
assert contractible(B, 3, 1) and contractible(B, 3, 2)
print("Z_9, {0,3,7}: level 1 first ->", contract_all(B, n, "shallow")[:2], "; level 2 first ->", contract_all(B, n, "deep")[:2])
assert nprime(37) == 3**18 * 5**9 * 7**6 * 11**3 * 13**3 * 17**2 * 19**2 * 23 * 29 * 31 * 37
assert [mu(d) for d in (1, 3, 5, 9, 15, 45, 27, 7, 21, 25, 75, 81, 11, 49)] == [0, 2, 4, 4, 4, 4, 6, 6, 6, 8, 8, 8, 10, 12]
print("known cases ok")
