# self-test of core.py: cyclotomic polynomials against sympy and against known ones; fast tables against long division;
# translation invariance of the divisor set (used only where "fix_zero" is used)
import random, sys
sys.path.insert(0, '/home/agent3/lean/lift-audit')
from core import *
import sympy
X = sympy.Symbol('X')
for d in range(1, 201):
    c = sympy.Poly(sympy.cyclotomic_poly(d, X), X).all_coeffs()[::-1]
    assert [int(t) for t in c] == cyclotomic(d), d
assert cyclotomic(1) == [-1, 1] and cyclotomic(2) == [1, 1] and cyclotomic(3) == [1, 1, 1] and cyclotomic(4) == [1, 0, 1]
assert cyclotomic(6) == [1, -1, 1] and cyclotomic(12) == [1, 0, -1, 0, 1] and cyclotomic(9) == [1, 0, 0, 1, 0, 0, 1]
print("Phi_d, d = 1..200: equal to sympy's; small ones equal to the textbook ones")
random.seed(1)
nchk = 0
for M in [1, 2, 3, 4, 6, 8, 9, 12, 15, 18, 30, 36, 54]:
    G = Group(M)
    for trial in range(300):
        s = random.randint(0, 9)
        t = tuple(sorted(random.randrange(M) for _ in range(s)))
        # bias towards structured multisets (cosets), where divisibility actually happens
        if trial % 3 == 0 and M > 1:
            d = random.choice(G.divs); a = random.randrange(M)
            t = tuple(sorted(list(t[:2]) + [(a + j * (M // d)) % M for j in range(d)]))
        w = counts_of(t, M)
        slow = G.divset(w)
        fast = G.decode(int(G.divset_block(np.array([t], dtype=np.int16).reshape(1, len(t)))[0]))
        assert slow == fast, (M, t, slow, fast)
        sh = random.randrange(M)
        w2 = counts_of([(y + sh) % M for y in t], M)
        assert G.divset(w2) == slow
        nchk += 1
print("fast table = long division, and translation keeps the divisor set:", nchk, "random multisets, no mismatch")
# the empty multiset: mask 0, divisible by everything
for M in [1, 6, 18]:
    assert Group(M).divset([0] * M) == frozenset(divisors(M))
print("empty multiset: every Phi_d divides (mask 0)")
