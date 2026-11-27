"""Referee's test of Theorem P' (other families of levels) on small boxes: least share of patterns good at every level of
the family, against c(L) computed from the definition in the text (coverage_own.c_family, exact fractions).
Families: the tree levels of digit boxes, and a few other subset-closed families.
usage: thmPprime_own.py SEED
"""
import sys, time
import numpy as np
from fractions import Fraction as Fr
from itertools import product, combinations
from boxtools import all_levels, pattern_array, good_batch, fraction_good
from coverage_own import c_family
from thmP_own import structured, KINDS

def cval(sides, fam):
    sd = tuple((j, n) for j, n in enumerate(sides))
    return c_family(sd, frozenset(frozenset(P) for P in fam))

def tree(labels):
    return [P for P in all_levels(len(labels)) if len({labels[i] for i in P}) == len(P)]

def closure(tops, k):
    fam = set()
    for T in tops:
        for r in range(len(T) + 1):
            for P in combinations(T, r): fam.add(tuple(P))
    return sorted(fam)

if __name__ == '__main__':
    rng = np.random.default_rng(int(sys.argv[1]))
    # exhaustive: tree levels of the digits (3, 3) of 9, every nonzero function over F_5 and F_7
    sides = (3, 3); fam = tree([3, 3]); PA, _ = pattern_array(sides); PA = PA.astype(np.int64)
    for q in (5, 7):
        t0 = time.time(); least = PA.shape[0]; nf = 0
        tail = np.array(list(product(range(q), repeat=6)), dtype=np.int64)
        for head in product(range(q), repeat=3):
            G = np.concatenate([np.tile(np.array(head, dtype=np.int64), (tail.shape[0], 1)), tail], axis=1)
            G = G[G.any(axis=1)].reshape(-1, 3, 3)
            cnt = np.zeros(G.shape[0], dtype=np.int64)
            for i in range(PA.shape[0]):
                cnt += good_batch(G * PA[i][None], fam, q)
            least = min(least, int(cnt.min())); nf += G.shape[0]
        print(f'digits (3, 3), tree levels {fam}, every nonzero function over F_{q} ({nf}): least share {Fr(least, PA.shape[0])}; '
              f'c = {cval(sides, fam)}  [{time.time() - t0:.0f} s]', flush=True)
    cases = [((3, 3, 5), tree([3, 3, 5]), [None, 7, 11]), ((3, 3, 7), tree([3, 3, 7]), [None, 5]), ((5, 5), tree([5, 5]), [None, 3, 7]),
             ((5, 5, 3), tree([5, 5, 3]), [7]), ((3, 5, 5), closure([(0, 1), (2,)], 3), [None, 7]), ((5, 3, 7), closure([(0, 1), (1, 2)], 3), [11]),
             ((3, 3, 5, 5), tree([3, 3, 5, 5]), [7])]
    for sides, fam, fields in cases:
        k = len(sides); PA, _ = pattern_array(sides); c = cval(sides, fam); t0 = time.time()
        for q in fields:
            least = None
            for kind in KINDS:
                for _ in range(40 if np.prod(sides) < 100 else 12):
                    g = structured(rng, sides, q, kind)
                    if not (g % q if q else g).any(): continue
                    a, b = fraction_good(g, fam, [q], PA)[q]
                    fr = Fr(a, b); least = fr if least is None else min(least, fr)
            ok = 'no bound from the recursion' if c <= 0 else ('OK' if least >= c else 'VIOLATION')
            print(f'box {sides}, family of {len(fam)} levels {"(tree)" if fam == tree(list(sides)) else ""}, field {"Q" if q is None else "F_%d" % q}: '
                  f'least share {least}; c = {c}: {ok}')
            assert c <= 0 or least >= c
        print(f'   [{time.time() - t0:.0f} s]', flush=True)
