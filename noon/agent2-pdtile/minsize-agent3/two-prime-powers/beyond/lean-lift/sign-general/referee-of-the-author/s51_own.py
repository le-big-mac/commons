"""Referee's check of section 5.1 of sign-general-result.md by exhaustion.

Box Z_3 x Z_3 x Z_5, B = {(0,0,0), (1,0,1), (2,0,2), (0,1,3), (0,2,4)}.  Every one of the 32 signings is tested at each of
the 8 levels over Q (good = some cube sum is not 0).  Then: all sets containing the cell 0 of size <= SIZE in the same
box: is 'all +' or some single turned sign good at every level?  (The text: five is the smallest size at which it fails.)
usage: s51_own.py SIZE
"""
import sys
import numpy as np
from itertools import product, combinations
from boxtools import all_levels, good_batch, good_at

sides = (3, 3, 5); levels = all_levels(3)
B = [(0, 0, 0), (1, 0, 1), (2, 0, 2), (0, 1, 3), (0, 2, 4)]
print('the five points, all 32 signings (signs in the order of the points); levels at which the signed function is degenerate:')
good_by_turns = {}
for signs in product((1, -1), repeat=5):
    g = np.zeros(sides, dtype=np.int64)
    for pt, s in zip(B, signs): g[pt] += s
    bad = [tuple(i + 1 for i in P) for P in levels if not good_at(g[None], P)[0]]
    turns = min(sum(1 for s in signs if s == -1), sum(1 for s in signs if s == 1))
    good_by_turns.setdefault(turns, []).append(not bad)
    if signs[0] == 1:
        print('  ', ''.join('+' if s == 1 else '-' for s in signs), 'good' if not bad else f'degenerate at levels {bad}')
for t in sorted(good_by_turns):
    v = good_by_turns[t]
    print(f'signings with {t} signs turned (up to changing all signs): {len(v)} signings, good: {sum(v)}')
# marginals named in the text
g = np.zeros(sides, dtype=np.int64)
for pt in B: g[pt] = 1
print('marginals of all +: third coordinate', g.sum(axis=(0, 1)).tolist(), '; first', g.sum(axis=(1, 2)).tolist(), '; second', g.sum(axis=(0, 2)).tolist())
print('every point has first or second coordinate 0:', all(pt[0] == 0 or pt[1] == 0 for pt in B))

SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 5
cells = list(product(*[range(n) for n in sides])); ncell = len(cells)
print(f'all sets containing the cell 0 in the box {sides}:')
for size in range(1, SIZE + 1):
    lst = list(combinations(range(1, ncell), size - 1))
    combos = np.array(lst, dtype=np.int64).reshape(len(lst), size - 1)
    M = combos.shape[0]
    fails_total = 0; allplus_good = 0
    for start in range(0, M, 200000):
        cb = combos[start:start + 200000]; m = cb.shape[0]
        members = np.concatenate([np.zeros((m, 1), dtype=np.int64), cb], axis=1)       # (m, size) cell indices
        G = np.zeros((m, ncell), dtype=np.int64)
        np.put_along_axis(G, members, 1, axis=1)
        ok_plus = good_batch(G.reshape((m,) + sides), levels)
        ok = ok_plus.copy()
        for j in range(size):                 # turn the sign of the j-th member
            H = G.copy()
            np.put_along_axis(H, members[:, j:j + 1], -1, axis=1)
            ok |= good_batch(H.reshape((m,) + sides), levels)
        fails_total += int((~ok).sum()); allplus_good += int(ok_plus.sum())
        if size == 5 and (~ok).any() and start == 0:
            ex = members[np.nonzero(~ok)[0][0]]
            print('      an example of size 5:', [cells[i] for i in ex])
    print(f'   size {size}: {M} sets; all + good for {allplus_good}; neither all + nor any single turn good: {fails_total}')
