"""Theorem 'structure' of weak-pqr.tex, as written (with the specific set E), on the box 2 x 3 x 5:
every subset A containing the origin with |A| <= 6 (wlog: the symmetric groups act transitively on points).
For each A with a step complement (LP), check that the projection to E = {i : (F_i)} is a bijection.
Also record that the sets WITHOUT the property never have a step complement is not tested (not claimed)."""
import itertools, sys
import numpy as np
from scipy.optimize import linprog
P = (2, 3, 5)
coords = (0, 1, 2)
subsets = [frozenset(c) for r in range(4) for c in itertools.combinations(coords, r)]
idx = {T: n for n, T in enumerate(subsets)}
pts = list(itertools.product(*[range(n) for n in P]))
npts = len(pts)
ag = np.array([[idx[frozenset(i for i in coords if v[i] == a[i])] for a in pts] for v in pts])
onehot = np.zeros((npts, npts, 8))
for vi in range(npts):
    for ai in range(npts):
        onehot[vi, ai, ag[vi, ai]] = 1
maxsize = int(sys.argv[1]) if len(sys.argv) > 1 else 6
tested = step = bad = 0
by_size = {}
for r in range(0, maxsize):
    for rest in itertools.combinations(range(1, npts), r):
        mem = (0,) + rest
        tested += 1
        Aeq = np.vstack([onehot[:, mem, :].sum(axis=1), np.eye(8)[idx[frozenset(coords)]][None, :]])
        res = linprog(np.zeros(8), A_eq=Aeq, b_eq=np.ones(npts + 1), bounds=[(0, None)] * 8, method='highs')
        if res.status != 0:
            continue
        step += 1
        A = [pts[n] for n in mem]
        E = []
        for i in coords:
            cnt = [sum(1 for v in A if v[i] == t) for t in range(P[i])]
            if len(set(cnt)) == 1:
                E.append(i)
        proj = {tuple(v[i] for i in E) for v in A}
        ok = len(proj) == len(A) == int(np.prod([P[i] for i in E]))
        by_size.setdefault((len(A), tuple(E)), 0)
        by_size[(len(A), tuple(E))] += 1
        if not ok:
            bad += 1
            print('VIOLATION', A, E)
print('box', P, ': sets tested', tested, '; with a step complement', step, '; violations of Theorem structure', bad)
print('(size, E) -> count:', dict(sorted(by_size.items())))
