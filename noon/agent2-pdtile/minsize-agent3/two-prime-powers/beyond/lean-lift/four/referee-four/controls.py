# controls.py -- do the checks bite?  Random multisets of 2..9 elements on small groups, all signings, exact division.
#  (i)  contract a level that is NOT contractible and test "good for the image => good for B": it must fail sometimes.
#  (ii) the level bound 2^(-mu(d)) of Corollary L applied to B itself when B is not fully contracted: it must fail
#       sometimes.
#  (iii) the union bound [m even] c_m + sum_{d | n, d > 1} 2^(-mu(d)) applied to B itself (not contracted).
import random, math
from fractions import Fraction
import numpy as np
from rlib import *

rng = random.Random(5)
t1 = f1 = t2 = f2 = t3 = f3 = 0
for trial in range(6000):
    n = rng.choice([9, 15, 27, 45, 63, 75, 81, 105, 135, 225])
    m = rng.randint(2, 9)
    r = rng.random()
    if r < 0.5:
        B = [rng.randrange(n) for _ in range(m)]
    else:
        pool = [rng.randrange(n) for _ in range(rng.randint(1, 4))]
        B = [(rng.choice(pool) + rng.choice([0, 0, n // 3, 2 * n // 3])) % n for _ in range(m)]
    good = good_vector(B, n)
    # (i)
    levels = [(p, t) for p, a in factor(n).items() for t in range(1, a + 1) if not contractible(B, p, t)]
    if levels:
        p, t = rng.choice(levels)
        Bc, nc = contract(B, n, p, t)
        gc = good_vector(Bc, nc)
        t1 += 1
        f1 += bool((gc & ~good).any())
    # (ii), (iii)
    Bf, nf, steps = contract_all(B, n, "deep")
    if steps:
        full = 1 << m
        bad = bad_all(B, n)
        t2 += 1
        f2 += any(int(v.sum()) << mu(d) > full for d, v in bad.items() if d > 1)
        bound = (Fraction(math.comb(m, m // 2), full) if m % 2 == 0 else 0) + sum(Fraction(1, 2 ** mu(d)) for d in bad if d > 1)
        t3 += 1
        f3 += Fraction(full - int(good.sum()), full) > bound
print("(i)   a level that is not contractible, contracted all the same: 'good for the image => good for B' fails for %d of %d multisets" % (f1, t1))
print("(ii)  level bound 2^(-mu(d)) on B itself, B not fully contracted: fails at some d for %d of %d multisets" % (f2, t2))
print("(iii) union bound on B itself, B not fully contracted: fails for %d of %d multisets" % (f3, t3))
