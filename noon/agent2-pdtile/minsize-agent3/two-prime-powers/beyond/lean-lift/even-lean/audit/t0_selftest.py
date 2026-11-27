"""Self-test of ecore.py.
1. Phi_d against sympy for d <= 200, and prod_{d | n} Phi_d = X^n - 1 for n <= 80.
2. bad(e, d) against a long division of the signed mask by Phi_d, written out separately.
3. bad3(e, d) (remainder modulo Phi_d divisible by 3) against bad3_literal(e, d) (the definition as Lean has it:
   vanishing at every primitive d-th root of unity in GF(3^r)), all signings of random families, many d prime to 3;
   and how often "vanishes at ONE primitive root" differs from "at every one".
4. the largest pivot set by all subsets against the formula.
"""
import os
import random
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy
from ecore import *

random.seed(20261127)
X = sympy.symbols('X')

# 1
for d in range(1, 201):
    c = sympy.Poly(sympy.cyclotomic_poly(d, X), X).all_coeffs()[::-1]
    assert tuple(int(x) for x in c) == cyclo(d), d


def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


for n in range(1, 81):
    a = [1]
    for d in divisors(n):
        a = pmul(a, list(cyclo(d)))
    assert a == [-1] + [0] * (n - 1) + [1], n
print("1. Phi_d equals sympy's for d <= 200; the product over d | n is X^n - 1 for n <= 80")

# 2
cnt = 0
nbad = 0
for trial in range(3000):
    d = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 24, 28, 30, 35, 36, 40, 60])
    m = random.randint(0, 7)
    if random.random() < 0.5:
        e = [random.randrange(0, 3 * d) for _ in range(m)]
    else:
        q = random.choice([q for q in divisors(d)])
        e = [random.randrange(0, 3) * (d // q) + random.choice([0, 0, d]) for _ in range(m)]
    b = bad(e, d)
    for s in range(1 << m):
        mask = [0] * (max(e, default=0) + 1)
        for k, x in enumerate(e):
            mask[x] += 1 if (s >> k) & 1 else -1
        _, r = pdivmod(mask, list(cyclo(d)))
        assert (not any(r)) == bool(b[s]), (e, d, s)
        cnt += 1
        nbad += int(b[s])
print(f"2. bad(e, d) equals long division on {cnt} signings ({nbad} of them bad)")

# 3
ds = [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 20, 22, 25, 26, 28, 35, 40, 44, 49, 50, 55, 56, 70, 77, 80]
tot = 0
tot_bad = 0
one_not_all = 0
per_d = {}
for d in ds:
    g, r = irreducible_factor3(d)
    nb = 0
    nfam = 0
    diff = 0
    for trial in range(400):
        m = random.randint(0, 8)
        kind = random.random()
        if kind < 0.35:
            e = [random.randrange(0, 2 * d) for _ in range(m)]
        elif kind < 0.7:
            q = random.choice([q for q in divisors(d) if q > 1] or [1])
            e = [random.randrange(0, q) * (d // q) + random.choice([0, 0, 0, d]) for _ in range(m)]
        else:
            q = random.choice([q for q in divisors(d)])
            base = [random.randrange(0, d) for _ in range(2)]
            e = [random.choice(base) + random.randrange(0, q) * (d // q) for _ in range(m)]
        a = bad3(e, d)
        b = bad3_literal(e, d)
        assert np.array_equal(a, b), (e, d)
        if m:
            one = bad3_literal_one(e, d, 1)
            diff += int(np.sum(one & ~b))
        nb += int(a.sum())
        nfam += 1
        tot += 1 << m
    per_d[d] = (r, phi(d) // r, nfam, nb, diff)
    tot_bad += nb
    one_not_all += diff
print(f"3. bad3 (remainder modulo Phi_d divisible by 3) equals the literal definition (every primitive d-th root in "
      f"GF(3^r)) on {tot} signings, {tot_bad} of them 3-bad; d in {ds}")
print("   d: (r = order of 3 mod d, number of irreducible factors of Phi_d mod 3, families, 3-bad signings, "
      "signings where the mask vanishes at one primitive root but not at every one)")
for d in ds:
    print(f"   {d}: {per_d[d]}")
print(f"   vanishing at one primitive root without being 3-bad: {one_not_all} signings (so 'every' matters)")

# 4
cnt = 0
for trial in range(4000):
    p = random.choice([2, 3, 5, 7])
    i = random.randint(0, 3)
    m = random.randint(0, 8)
    N = p ** i
    if random.random() < 0.5:
        e = [random.randrange(0, 2 * N + 3) for _ in range(m)]
    else:
        L = p ** max(i - 1, 0)
        cs = [random.randrange(0, L) for _ in range(2)]
        e = [random.choice(cs) + random.randrange(0, p) * L for _ in range(m)]
    if i >= 1:
        assert max_pivot(e, p, i) == max_pivot_formula(e, p, i), (e, p, i)
        cnt += 1
print(f"4. largest pivot set by all subsets equals (occupied classes) - (full groups) on {cnt} cases (i >= 1)")
print("self-test passed")
