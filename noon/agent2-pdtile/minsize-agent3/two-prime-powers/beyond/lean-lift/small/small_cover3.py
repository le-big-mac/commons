"""How far Theorem 7 of the third result (tree boxes: n = m' q^b or n = m' with Gamma(m') > 0) reaches on the reduced shapes
        n'_m = product over odd primes p <= m of p^floor((m-1)/(p-1)).
Only Gamma is used (coverage2.py's own function, from Lemmas S, T, 3T and Lemma 3 of the second result); the digit recursion
of Theorem 6 is not needed and is left out because it runs out of memory on these shapes.
usage: small_cover3.py MAXM"""
import sys
sys.setrecursionlimit(100000)
sys.path.insert(0, '/home/agent3/lean/lift-check/general2')
from coverage2 import Gamma
from sympy import primerange
M = int(sys.argv[1]); last_ok = 0; first_bad = None
for m in range(1, M + 1):
    f = {p: (m - 1) // (p - 1) for p in primerange(3, m + 1)}
    f = {p: a for p, a in f.items() if a > 0}
    if len(f) <= 2:
        print(f'm={m}: at most two primes: Theorem 2 of the first result'); last_ok = m if first_bad is None else last_ok; continue
    best = None
    for q in [None] + sorted(f):
        rest = tuple(sorted((p, a) for p, a in f.items() if p != q))
        G = Gamma(rest)
        if G > 0 and (best is None or G > best[1]): best = (q, G)
    shape = ' * '.join(f'{p}^{a}' if a > 1 else f'{p}' for p, a in sorted(f.items()))
    if best:
        print(f'm={m}: {shape}: Gamma > 0 with the prime {best[0]} taken out: Gamma = {float(best[1]):.3g}', flush=True)
        if first_bad is None: last_ok = m
    else:
        print(f'm={m}: {shape}: Gamma <= 0 for every choice', flush=True)
        if first_bad is None: first_bad = m
print(f'covered for every m up to {last_ok}; first m not covered: {first_bad}')
