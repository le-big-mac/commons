r"""Z_{p^n q}: the explicit certificates of the proof, built and checked by brute force (agent3 / Yonder).
 (S1) A' = T_E x Z_q has p^|E| q elements and zeros  {p^l : l in E} and {p^l q : all l >= 0}.
 (S2) A''= T_E x {0}  has p^|E| elements   and zeros  {p^l, p^l q : l in E}.
 (C)  for a pattern (E, F) with 0 in F, a = max(E \ F) and no level above a in F \ E: the set B of the proof has
      min(p, q) p^(n-|E|) elements and no two of them differ by an element whose order is p^l (l in E) or p^l q (l in F).
 Each bound is also compared with the exact D+ (agent2's lp.py) when the group is small enough.
 And for every pattern: the proof's prediction of which patterns can be the zero set of a pd-tiling set is compared
 with the necessary condition 'D+(Z) is a multiple of k(Z), and D+(Z) = k(Z)' computed exactly."""
import sys, itertools
from math import gcd
sys.path.insert(0, "/srv/commons/agent2-pdtile/flat"); sys.path.insert(0, "/home/agent3/review2")
from lp import Setup
from cyclo_exact import divides
def run(p, n, q, with_lp=True):
    M = p ** n * q; P = p ** n
    crt = {(x % P, x % q): x for x in range(M)}
    levels = list(range(1, n + 1)); subsets = [frozenset(c) for r in range(n + 1) for c in itertools.combinations(levels, r)]
    S = Setup(M) if with_lp else None
    zeros = lambda A: ({l for l in levels if divides(p ** l, sorted(A), M)}, {l for l in range(n + 1) if divides(p ** l * q, sorted(A), M)})
    order = lambda x: M // gcd(x, M)
    T = {}
    for E in subsets:
        T[E] = [sum(d * p ** (l - 1) for d, l in zip(ds, sorted(E))) for ds in itertools.product(range(p), repeat=len(E))]
        A1 = [crt[(u, w)] for u in T[E] for w in range(q)]; A2 = [crt[(u, 0)] for u in T[E]]
        E1, F1 = zeros(A1); E2, F2 = zeros(A2)
        assert len(set(A1)) == p ** len(E) * q and E1 >= E and F1 == set(range(n + 1)), ("S1", p, n, q, E)
        assert len(set(A2)) == p ** len(E) and E2 >= E and F2 >= E, ("S2", p, n, q, E)
    ncl = 0; nlp = 0; npat = 0; agree = 0
    for E in subsets:
        for Fp in subsets:
            for zero_in_F in (False, True):
                F = set(Fp) | ({0} if zero_in_F else set()); npat += 1
                bad_same = {p ** l for l in E}; bad_cross = {p ** l * q for l in F}
                Z = sorted(bad_same | bad_cross); k = p ** len(E) * (q if zero_in_F else 1)
                predicted_possible = (Fp <= E) if not zero_in_F else (E <= Fp)       # what the theorem allows
                d = S.Dplus(Z)[0] if with_lp else None
                if with_lp:
                    nlp += 1
                    assert d <= p ** len(E) * q                                       # (S1)
                    if not zero_in_F and Fp <= E: assert d <= p ** len(E)             # (S2)
                    if predicted_possible: assert d == k, ("standard pattern with D+ != k", E, F, d)
                if zero_in_F and not (E <= Fp):
                    a = max(E - Fp)
                    if not any(l > a for l in Fp - E):
                        t = min(p, q); B = []
                        free_hi = [l for l in levels if l > a and l not in E and l not in Fp]; free_lo = [l for l in levels if l < a and l not in E]
                        for c in range(t):
                            for ds in itertools.product(range(p), repeat=len(free_hi) + len(free_lo)):
                                u = c * p ** (n - a) + sum(dd * p ** (n - l) for dd, l in zip(ds, free_hi + free_lo))
                                B.append((u, c))
                        assert len(set(B)) == t * p ** (n - len(E)), ("C size", E, F)
                        for (u1, w1), (u2, w2) in itertools.combinations(B, 2):
                            o = order(crt[((u1 - u2) % P, (w1 - w2) % q)])
                            assert o not in bad_same and o not in bad_cross, ("C", p, n, q, E, F, (u1, w1), (u2, w2), o)
                        ncl += 1
                        if with_lp: assert d <= k // t if k % t == 0 else d <= k / t
    print(f"p={p} n={n} q={q} M={M}: {len(subsets)} sets T_E verified (S1, S2); {ncl} clique certificates verified; "
          f"{npat} patterns" + (f", exact D+ compared for {nlp}" if with_lp else ""), flush=True)
for p, n, q, lp_ in [(2, 1, 3, True), (3, 1, 2, True), (2, 2, 3, True), (3, 2, 2, True), (2, 2, 5, True), (3, 2, 5, True), (2, 3, 3, True), (3, 3, 2, True), (2, 3, 5, True), (2, 4, 3, True), (3, 3, 5, False), (2, 5, 3, False), (5, 2, 7, True), (5, 3, 2, False)]:
    run(p, n, q, lp_)
