"""Numerical check of Lemma A and Lemma B of the result file on random examples (exact arithmetic).
Lemma A: n = m q^b, q prime not dividing m; if Phi_{d' q^j} | S in Z[X] then Phi_{d'} | (S folded modulo X^m - 1) in F_q[X].
Lemma B: f primitive on Z_d; (a) Phi_d | T  =>  <f, T> = 0;  (b) Phi_d | T in F_q[X]  =>  <f, T> = 0 mod q.
   f ranges over: sibling differences (d = p^i), mixed differences (d = p r), and the function h of Proposition 4.
usage: lemmas_AB.py"""
import random
from sympy import Poly, cyclotomic_poly, symbols, ZZ, GF, factorint
X = symbols('X'); rng = random.Random(5)
def fold(coeffs, m):
    out = [0] * m
    for i, c in enumerate(coeffs): out[i % m] += c
    return out
def low(poly): return [int(c) for c in poly.all_coeffs()[::-1]]
# Lemma A
tests = 0
for (m, q, b) in [(15, 7, 1), (9, 5, 2), (15, 7, 2), (21, 5, 1), (45, 7, 1), (5, 3, 3), (35, 3, 2), (1, 3, 3), (105, 11, 1)]:
    n = m * q ** b
    for dprime in [d for d in range(1, m + 1) if m % d == 0]:
        for j in range(b + 1):
            d = dprime * q ** j
            phi = Poly(cyclotomic_poly(d, X), X, domain=ZZ)
            for _ in range(3):
                A = Poly([rng.randrange(-3, 4) for _ in range(rng.randrange(1, 8))] or [1], X, domain=ZZ)
                S = low(phi * A)                                   # divisible by Phi_d (degree need not be < n: the lemma does not ask it)
                Sbar = Poly(fold(S, m)[::-1], X, modulus=q)
                r = Sbar.rem(Poly(cyclotomic_poly(dprime, X), X, modulus=q))
                assert r.is_zero, (m, q, b, dprime, j)
                tests += 1
print(f'Lemma A: {tests} random cases, all as stated')
# Lemma B
def primitive_ok(f, d):
    for p in factorint(d):
        step = d // p
        for y in range(step):
            if sum(f[(y + k * step) % d] for k in range(p)) != 0: return False
    return True
def sibling_diff(d, p):
    i = factorint(d)[p]; u = rng.randrange(d); t = rng.randrange(1, p)
    f = [0] * d; f[u] += 1; f[(u + t * (d // p)) % d] -= 1; return f
def cube(d):
    f = [0] * d; P = list(factorint(d)); u = rng.randrange(d); t = {p: rng.randrange(1, p) for p in P}
    for mask in range(1 << len(P)):
        y = u; sg = 1
        for k, p in enumerate(P):
            if mask >> k & 1: y += t[p] * (d // p); sg = -sg
        f[y % d] += sg
    return f
def hfun(d):
    f = [1] * d
    for p, e in factorint(d).items():
        v = rng.randrange(p)
        for y in range(d): f[y] *= (p * (((y % p ** e) // p ** (e - 1)) == v) - 1)
    return f
ta = tb = 0
for d in [3, 9, 27, 5, 25, 15, 21, 45, 105, 225, 63]:
    phi = Poly(cyclotomic_poly(d, X), X, domain=ZZ)
    for _ in range(12):
        f = rng.choice([cube, hfun])(d)
        assert primitive_ok(f, d)
        A = Poly([rng.randrange(-3, 4) for _ in range(rng.randrange(1, 9))] or [1], X, domain=ZZ)
        T = low(phi * A); Tf = fold(T, d)
        assert sum(a * c for a, c in zip(f, Tf)) == 0; ta += 1
        for q in (3, 5, 7, 11):
            Bq = Poly([rng.randrange(-3, 4) for _ in range(rng.randrange(1, 9))] or [1], X, domain=ZZ)
            T2 = low(phi * A + q * Bq); Tf2 = fold(T2, d)
            assert sum(a * c for a, c in zip(f, Tf2)) % q == 0; tb += 1
print(f'Lemma B: (a) {ta} random cases, (b) {tb} random cases, all as stated')
