"""List sets in the 2x2x3 box that have a step complement but are not a transversal of any coordinate projection."""
import itertools
import numpy as np
from scipy.optimize import linprog
P = (2, 2, 3)
coords = (0, 1, 2)
subsets = [frozenset(c) for r in range(4) for c in itertools.combinations(coords, r)]
idx = {T: n for n, T in enumerate(subsets)}
pts = list(itertools.product(*[range(n) for n in P]))
out = {}
for mask in range(1, 1 << len(pts)):
    A = [pts[n] for n in range(len(pts)) if mask >> n & 1]
    Aeq = np.zeros((len(pts) + 1, 8)); beq = np.ones(len(pts) + 1)
    for vi, v in enumerate(pts):
        for a in A:
            Aeq[vi, idx[frozenset(i for i in coords if v[i] == a[i])]] += 1
    Aeq[len(pts), idx[frozenset(coords)]] = 1
    r = linprog(np.zeros(8), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * 8, method='highs')
    if r.status != 0:
        continue
    def bij(E):
        proj = {tuple(v[i] for i in sorted(E)) for v in A}
        return len(proj) == len(A) == int(np.prod([P[i] for i in E]))
    if not any(bij(T) for T in subsets):
        out.setdefault(len(A), []).append((A, {''.join('xyz'[i] for i in sorted(T)) or '0': round(float(r.x[idx[T]]), 4) for T in subsets if r.x[idx[T]] > 1e-9}))
for n, L in sorted(out.items()):
    print('size', n, ':', len(L), 'sets; e.g.', L[0])
