"""Self-test of core.py: Phi_d against sympy and against the defining product; "bad at d" for all signings against literal
long division; live/rank against a second implementation written differently (children of occupied classes)."""
import os
import random
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import core

rng = random.Random(20261127)

# 1. Phi_d against sympy, d <= 300, and prod_{d | n} Phi_d = X^n - 1 for n <= 120
import sympy
X = sympy.Symbol('X')
bad_c = 0
for d in range(1, 301):
    mine = list(core.cyclo(d))
    theirs = [int(c) for c in reversed(sympy.Poly(sympy.cyclotomic_poly(d, X), X).all_coeffs())]
    if mine != theirs:
        bad_c += 1
print('Phi_d against sympy, d = 1..300: mismatches', bad_c)
bad_p = 0
for n in range(1, 121):
    prod = [1]
    for d in core.divisors(n):
        prod = core.pmul(prod, list(core.cyclo(d)))
    if prod != [-1] + [0] * (n - 1) + [1]:
        bad_p += 1
print('prod_{d|n} Phi_d = X^n - 1, n = 1..120: mismatches', bad_p)

# 2. bad(e, d) for all signings against literal division, random families with exponents beyond d
mism = 0
cases = 0
truecases = 0
for trial in range(1500):
    d = rng.choice([1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 15, 18, 21, 25, 27, 30, 35, 45, 63, 75, 105])
    m = rng.randint(1, 7)
    R = rng.choice([d, 2 * d, 3 * d + 5])
    kind = rng.random()
    if kind < 0.5:
        e = [rng.randrange(R) for _ in range(m)]
    else:                                   # unions of cosets, so that divisibility happens
        q = rng.choice(list(core.factor(d))) if d > 1 else 1
        e = []
        while len(e) < m:
            a = rng.randrange(R)
            e += [a + t * (d // q) for t in range(q)]
        e = e[:max(m, 1)]
    m = len(e)
    v = core.bad(e, d)
    S = core.signs(m)
    for j in range(2 ** m):
        lit = core.bad_literal(e, [int(s) for s in S[j]], d)
        cases += 1
        truecases += lit
        if lit != bool(v[j]):
            mism += 1
print('bad at d, table against literal long division:', cases, 'signed families,', truecases, 'of them bad; mismatches', mism)

# 3. live and rank against a second implementation
def live2(e, p, i):
    if i == 0:
        # Lean: p^(0-1) = p^0 = 1, classes modulo 1: needs 0 = t for every t < p
        return p <= 1 and (p == 0 or len(e) > 0)
    parents = {}
    for x in e:
        r = x % p ** i
        parents.setdefault(r % p ** (i - 1), set()).add(r // p ** (i - 1))
    return any(len(ch) == p for ch in parents.values())
mism = 0
n = 0
for trial in range(20000):
    p = rng.choice([2, 3, 5, 7])
    m = rng.randint(1, 14)
    R = rng.choice([p, p * p, p ** 3, 2 * p ** 3 + 1, 500])
    e = [rng.randrange(R) for _ in range(m)]
    for i in range(0, 5):
        n += 1
        if core.live(e, p, i) != live2(e, p, i):
            mism += 1
        if core.rank(e, p, i) != sum(live2(e, p, j) for j in range(1, i + 1)):
            mism += 1
print('live, rank against a second implementation:', n, 'cases; mismatches', mism)
