"""A4. The construction of section 2, built from the note's words alone (not from construct.py), for every pattern with
0 not in F; pattern checked by exact integer polynomial division and by the tree; size compared with the theorem.
"Level a is the digit of p^(a-1)": u = sum_{a=1..n} d_a p^(a-1)."""
import sys, itertools
sys.path.insert(0, '/home/agent3/minsize/check')
from pat import *


def build(p, q, n, E, F):
    M = p ** n * q
    w = [0] * M
    def x_of(u, layer):
        for x in range(u, M, p ** n):
            if x % q == layer: return x
    EF = [a for a in E if a not in F]                      # levels of E \ F
    def all_u(free):
        for digs in itertools.product(*[range(p) if a in free else (0,) for a in range(1, n + 1)]):
            yield sum(d * p ** (a - 1) for a, d in zip(range(1, n + 1), digs)), dict(zip(range(1, n + 1), digs))
    # A1: digits free at the levels of E u F, 0 elsewhere; layer tau(u)
    for u, d in all_u(set(E) | set(F)):
        tau = 1 if (EF and all(d[a] != 0 for a in EF)) else 0
        w[x_of(u, tau)] += 1
    # A2: digits free at the levels of E, 0 elsewhere, in every layer; only if F is not inside E
    if not set(F) <= set(E):
        for u, d in all_u(set(E)):
            for layer in range(q): w[x_of(u, layer)] += 1
    return w


tot = 0
for (p, q, nmax) in [(2, 3, 5), (3, 2, 4), (2, 5, 4), (5, 2, 4), (3, 5, 4), (5, 3, 4), (2, 7, 3), (7, 2, 3), (3, 7, 3), (7, 3, 2), (5, 7, 2), (7, 5, 2), (2, 11, 3), (11, 2, 2)]:
    for n in range(1, nmax + 1):
        ok = bad = sets = 0
        lv = range(1, n + 1)
        for ke in range(n + 1):
            for E in itertools.combinations(lv, ke):
                for kf in range(n + 1):
                    for F in itertools.combinations(lv, kf):
                        w = build(p, q, n, E, F)
                        good = (exact_pattern_division(p, q, n, w) == (E, F)) and (tree_pattern(p, q, n, w) == (E, F)) and sum(w) == thm_value(p, q, E, F)
                        ok += good; bad += (not good); sets += (max(w) <= 1)
                        if not good and bad <= 3: print('  NOT AS WANTED', p, q, n, E, F, exact_pattern_division(p, q, n, w), sum(w), thm_value(p, q, E, F))
        tot += ok + bad
        print(f'p={p} q={q} n={n} order {p ** n * q}: {ok} of {ok + bad} patterns with 0 not in F: the construction has exactly the pattern (exact division and tree) and the size of the theorem; it is a set in {sets}', flush=True)
print('patterns built and checked:', tot)
