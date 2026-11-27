"""The fixed statement sizes_eq, tried by exhaustion on small cases: for N and an odd prime r, and every set P of divisors > 1 of N,
the sizes (up to a bound) of the nonempty multisets on Z_{N r} whose pattern among ALL divisors > 1 of N r is exactly P, against the
sizes of the nonempty multisets on Z_N with pattern exactly P.  Exact division.  Also r = 2 as a control (the statement excludes it).
usage: sizes_brute.py"""
import itertools
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X')
def sizes_by_pattern(M, bound):
    divs = [d for d in range(2, M + 1) if M % d == 0]; PHI = {d: Poly(cyclotomic_poly(d, X), X, domain=ZZ) for d in divs}
    out = {}
    for s in range(1, bound + 1):
        for comb in itertools.combinations_with_replacement(range(M), s):
            if comb[0] != 0: continue                      # up to translation (patterns are translation invariant)
            A = Poly(sum(X**i for i in comb), X, domain=ZZ)
            P = frozenset(d for d in divs if A.rem(PHI[d]).is_zero)
            out.setdefault(P, set()).add(s)
    return out
for N, r, bound in [(2, 3, 6), (3, 3, 6), (4, 3, 5), (6, 3, 4), (2, 5, 5), (3, 5, 4), (5, 3, 4), (4, 2, 5), (3, 2, 6), (6, 2, 5)]:
    big, small = sizes_by_pattern(N * r, bound), sizes_by_pattern(N, bound)
    dN = [d for d in range(2, N + 1) if N % d == 0]
    bad = []
    for k in range(len(dN) + 1):
        for P in itertools.combinations(dN, k):
            P = frozenset(P)
            if big.get(P, set()) != small.get(P, set()): bad.append((sorted(P), sorted(small.get(P, set())), sorted(big.get(P, set()))))
    print(f'N = {N}, r = {r}, sizes up to {bound}: {2 ** len(dN)} patterns of divisors of N; size sets equal for {2 ** len(dN) - len(bad)}' + (f'; differ (pattern, on Z_N, on Z_Nr): {bad}' if bad else ''), flush=True)
