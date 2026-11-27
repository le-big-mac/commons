# Census of a cyclic group: every multiset of size 1..S on Z_M containing 0, with the exact set of d | M such that Phi_d divides
# its mask.  For each such set: the sizes at which it occurs, how often, and a first example of least size.  Kept as a small
# JSON file census/M{M}.json (a running tally; no multiset is stored except the examples).
# S is chosen from a work budget unless given:  C(M + S - 1, S - 1) * M <= budget.
# usage: t3_census.py budget M [M ...]      or   t3_census.py S=<S> M
import sys, os, json, time, math
import numpy as np
from core import census, census_nodes, pattern_slow

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'census')


def pick_S(M, budget, smax=26):
    S = 1
    while S < smax and census_nodes(M, S + 1) * M <= budget:
        S += 1
    return S


def do(M, S):
    path = os.path.join(OUT, f"M{M}.json")
    if os.path.exists(path):
        old = json.load(open(path))
        if old['S'] >= S:
            print(f"M={M}: census to S={old['S']} already there", flush=True)
            return
    t0 = time.time()
    G, tally, exsize, ex, nodes = census(M, S)
    pats = []
    for c in range(tally.shape[0]):
        if exsize[c]:
            sizes = [t for t in range(1, S + 1) if tally[c, t]]
            e = [int(v) for v in ex[c, :exsize[c]]]
            assert exsize[c] == sizes[0]
            # the example, re-checked by long division
            assert G.mask_of(pattern_slow(e, M)) == c
            pats.append({'code': c, 'divs': sorted(G.decode(c)), 'sizes': sizes,
                         'counts': {str(t): int(tally[c, t]) for t in sizes}, 'example': e})
    os.makedirs(OUT, exist_ok=True)
    json.dump({'M': M, 'S': S, 'divisors': G.divs, 'nodes': int(nodes), 'patterns': pats}, open(path, 'w'))
    print(f"M={M:4d} S={S:2d} multisets={nodes:11d} divisor sets seen={len(pats):5d} of {1 << (G.nd - 1)} [{time.time() - t0:.1f}s]",
          flush=True)


if __name__ == '__main__':
    if sys.argv[1].startswith('S='):
        do(int(sys.argv[2]), int(sys.argv[1][2:]))
    else:
        budget = int(float(sys.argv[1]))
        for a in sys.argv[2:]:
            M = int(a)
            do(M, pick_S(M, budget))
