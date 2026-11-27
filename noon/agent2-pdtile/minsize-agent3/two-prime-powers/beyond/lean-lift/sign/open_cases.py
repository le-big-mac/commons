"""Sampling in the first cases NOT covered by the theorems of the result file: n = 1155 = 3*5*7*11 and n = 1575 = 3^2*5^2*7.
Structured sets (unions of cosets with a few points changed), random sets and small multisets; for each: is all signs + good?
if not, does turning ONE sign give a good signing?  if not, two?  (exact integer arithmetic; remainders modulo Phi_d, d | n).
usage: open_cases.py n count seed"""
import sys, random, itertools
import numpy as np
from constructions import remainder_maps, structured_sets
n, count, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
RM = {d: R.astype(np.int64) for d, R in remainder_maps(n).items()}          # entries are tiny; int64 is exact here
assert all(np.abs(R).max() < 10 ** 6 for R in RM.values())
rng = random.Random(seed)
hist = {'all + good': 0, 'one turn needed': 0, 'two turns needed': 0, 'not found with <= 2 turns': 0}; tot = 0; worst = None
for Bm in structured_sets(n, rng, count):
    tot += 1
    S = np.zeros(n, dtype=np.int64)
    for x in Bm: S[x % n] += 1
    V = {d: R @ S for d, R in RM.items()}
    if all(v.any() for v in V.values()): hist['all + good'] += 1; continue
    pts = sorted(set(x % n for x in Bm))
    ok1 = np.ones(len(pts), dtype=bool)
    for d, R in RM.items(): ok1 &= (V[d][:, None] - 2 * R[:, pts]).any(axis=0)
    if ok1.any(): hist['one turn needed'] += 1; continue
    found = False
    for i, j in itertools.combinations(range(len(pts)), 2):
        if all((V[d] - 2 * R[:, pts[i]] - 2 * R[:, pts[j]]).any() for d, R in RM.items()): found = True; break
    if found: hist['two turns needed'] += 1
    else: hist['not found with <= 2 turns'] += 1; worst = Bm
print(f'n = {n}: tried {tot}: {hist}' + (f'; example without a good signing among <= 2 turns: {worst}' if worst else ''), flush=True)
