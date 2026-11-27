"""Self-test of reflib: cyclotomic polynomials, the two tests of 'good', the contraction map.
usage: ref_selftest.py SEED"""
import sys, random
import numpy as np
from reflib import *

rng = random.Random(int(sys.argv[1]))

# 1. cyclotomic polynomials: degrees = Euler phi, product over d | n equals X^n - 1, some known ones
def phi_euler(n):
    return sum(1 for k in range(1, n + 1) if np.gcd(k, n) == 1)
def polymul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return out
for n in list(range(1, 80)) + [105, 135, 225, 315, 945]:
    assert len(cyclo(n)) - 1 == phi_euler(n)
    if n < 80:
        prod = [1]
        for d in divisors(n):
            prod = polymul(prod, list(cyclo(d)))
        assert prod == [-1] + [0] * (n - 1) + [1]
assert cyclo(1) == (-1, 1) and cyclo(3) == (1, 1, 1) and cyclo(9) == (1, 0, 0, 1, 0, 0, 1)
assert cyclo(15) == (1, -1, 0, 1, -1, 1, 0, -1, 1)
assert min(cyclo(105)) == -2
print('cyclotomic polynomials: degrees, products X^n - 1 (n < 80), Phi_15, the coefficient -2 of Phi_105: right')

# 2. rem_matrix against long division
for d in [1, 3, 5, 9, 15, 21, 27, 45, 63, 105]:
    R = rem_matrix(d)
    for j in range(d):
        q, r = poly_divmod([0] * j + [1], list(cyclo(d)))
        r = r + [0] * (R.shape[0] - len(r))
        assert list(R[:, j]) == r[:R.shape[0]]
print('X^j modulo Phi_d: equal to long division for d in 1, 3, 5, 9, 15, 21, 27, 45, 63, 105')

# 3. the two tests of 'good' on random signed multisets
cnt = 0; ngood = 0
for _ in range(1500):
    n = rng.choice([3, 5, 9, 15, 21, 27, 45, 63, 75, 105, 135, 225])
    m = rng.randint(1, 7)
    kind = rng.randrange(3)
    if kind == 0:
        el = [rng.randrange(n) for _ in range(m)]
    elif kind == 1:
        d = rng.choice([x for x in divisors(n) if x > 1]); c = rng.randrange(n)
        el = [(c + (n // d) * rng.randrange(d)) % n for _ in range(m)]
    else:
        ps = list(factor(n)); p = rng.choice(ps); c = rng.randrange(n)
        el = [(c + (n // p) * j) % n for j in range(p)][:m]
        while len(el) < m: el.append(rng.randrange(n))
    g = good_all(n, el)
    sg = sign_matrix(len(el))
    for row, gv in zip(sg, g):
        gp = good_plain(n, el, list(row))
        assert gp == bool(gv), (n, el, list(row))
        bl = bad_levels(n, el, list(row))
        assert (len(bl) == 0) == gp
        cnt += 1; ngood += gp
print(f'good_all = good_plain (dense long division by every Phi_d) on {cnt} signings of 1500 multisets ({ngood} good, {cnt - ngood} bad)')

# 4. the contraction map: digits
for _ in range(2000):
    p = rng.choice([3, 5, 7]); a = rng.randint(1, 4); n2 = rng.choice([1, 2, 4, 11, 13, 16, 77])
    if n2 % p == 0: continue
    n = p ** a * n2; t = rng.randint(1, a); x = rng.randrange(n)
    (y,) = contract([x], n, p, a, t)
    assert 0 <= y < n // p and y % n2 == x % n2
    dx = [(x % p ** a // p ** i) % p for i in range(a)]
    dy = [(y % p ** (a - 1) // p ** i) % p for i in range(a - 1)]
    assert dy == dx[:t - 1] + dx[t:]
print('contraction map: second coordinate kept, digit of index t-1 deleted (2000 random cases)')
