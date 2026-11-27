"""My own end-to-end test of the new theorem's claim for squarefree n (written from the statement, not from the instance's
programs): for a set B in Z_n, n squarefree and odd, some signing of product form sign(x) = prod over primes p | n of
sigma_p(x mod p), with sigma_p : Z_p -> {+1, -1}, has a signed mask divisible by no Phi_d, d | n.  Exact division.
Sets: unions and sums of cosets of several subgroups (so that 'all +' has many divisors), with a few random points.
Patterns are drawn at random until one is good; the statement says at least a fraction 2^(-number of primes) are.
usage: squarefree_own.py n COUNT [seed]"""
import sys, random
from sympy import Poly, cyclotomic_poly, symbols, ZZ, factorint
n = int(sys.argv[1]); cnt = int(sys.argv[2]); random.seed(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
X = symbols('X'); ps = sorted(factorint(n)); assert all(e == 1 for e in factorint(n).values()) and n % 2
divs = [d for d in range(1, n + 1) if n % d == 0]; CY = {d: Poly(cyclotomic_poly(d, X), X, domain=ZZ) for d in divs}
def zeros(sg):                      # sg: dict x -> coefficient
    A = Poly(sum(c * X**x for x, c in sg.items() if c), X, domain=ZZ)
    return [d for d in divs if A.rem(CY[d]).is_zero]
tried_tot = 0; worst = 0; allplus_bad = 0; found = 0
for _ in range(cnt):
    B = set()
    for _c in range(random.randint(1, 3)):
        d = random.choice([d for d in divs if 1 < d < n]); x0 = random.randrange(n); B |= {(x0 + d * j) % n for j in range(n // d)}
    for _c in range(random.randint(0, 3)): B ^= {random.randrange(n)}
    if not B: continue
    if zeros({x: 1 for x in B}): allplus_bad += 1
    for t in range(1, 400):
        sig = {p: [random.choice((1, -1)) for _ in range(p)] for p in ps}
        sg = {}
        for x in B:
            s = 1
            for p in ps: s *= sig[p][x % p]
            sg[x] = s
        if not zeros(sg): found += 1; tried_tot += t; worst = max(worst, t); break
print(f'n = {n} ({" * ".join(map(str, ps))}): {cnt} sets (unions of cosets with a few points changed); all + has a cyclotomic divisor for {allplus_bad}; a good signing of product form found for {found}; random patterns tried: {tried_tot / max(found, 1):.2f} on average, at most {worst} (the bound of the theorem: a fraction of at least 1/{2 ** len(ps)} of the patterns)')
