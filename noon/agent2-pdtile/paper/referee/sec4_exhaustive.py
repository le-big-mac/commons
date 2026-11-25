"""Referee check of Section 4 of weak-pqr.tex as WRITTEN (Lemma dich, Prop. bounds), independent of Lean,
by exhaustion over all subsets of small boxes (coprimality is not needed for Section 4), plus a look at
what happens to Theorem 'structure' in boxes with non-coprime sizes (Remark 1 of the last section).

For every nonempty A in the box: LP for a step complement gamma (8 unknowns, gamma>=0, gamma_xyz=1,
sum_{a in A} gamma_{ag(v,a)} = 1 for all v). If one exists:
  - Lambda_0 |A| = M, and Lambda_S = 0 or (F_S)       [Lemma dich]
  - (b0)..(b3) with all coordinate permutations        [Prop. bounds]
  - is the projection to E = {i : F_i} a bijection?   [Thm structure; expected to fail for non-coprime sizes]
  - is the projection to SOME set of coordinates a bijection?
"""
import itertools, sys
import numpy as np
from scipy.optimize import linprog

coords = (0, 1, 2)
subsets = [frozenset(c) for r in range(4) for c in itertools.combinations(coords, r)]
idx = {T: n for n, T in enumerate(subsets)}
FULL = frozenset(coords)

def run(P):
    pts = list(itertools.product(*[range(n) for n in P]))
    npts = len(pts)
    M = npts
    ag = [[idx[frozenset(i for i in coords if v[i] == a[i])] for a in pts] for v in pts]
    stats = dict(sets=0, step=0, dich_bad=0, bound_bad=0, E_fail=0, no_transversal=0)
    examples = []
    for mask in range(1, 1 << npts):
        stats['sets'] += 1
        members = [n for n in range(npts) if mask >> n & 1]
        Aeq = np.zeros((npts + 1, 8)); beq = np.ones(npts + 1)
        for vi in range(npts):
            for ai in members:
                Aeq[vi, ag[vi][ai]] += 1
        Aeq[npts, idx[FULL]] = 1
        r = linprog(np.zeros(8), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * 8, method='highs')
        if r.status != 0:
            continue
        stats['step'] += 1
        gam = r.x
        A = [pts[n] for n in members]
        nA = len(A)
        a = np.zeros(P, dtype=int)
        for v in A:
            a[v] = 1
        # seven conditions
        F = {}
        for i in coords:
            other = tuple(j for j in coords if j != i)
            F[frozenset({i})] = len(set(a.sum(axis=other).tolist())) == 1
        for i, j in [(0, 1), (0, 2), (1, 2)]:
            k = 3 - i - j
            Nij = a.sum(axis=k)
            d = Nij[:, None, :, None] + Nij[None, :, None, :] - Nij[:, None, None, :] - Nij[None, :, :, None]
            F[frozenset({i, j})] = not d.any()
        d3 = (a[:, None, :, None, :, None] - a[None, :, :, None, :, None] - a[:, None, None, :, :, None] + a[None, :, None, :, :, None]
              - a[:, None, :, None, None, :] + a[None, :, :, None, None, :] + a[:, None, None, :, None, :] - a[None, :, None, :, None, :])
        F[FULL] = not d3.any()
        # mu, Lambda
        mu = {S: sum((-1) ** (len(S) - len(R)) * gam[idx[R]] for R in subsets if R <= S) for S in subsets}
        Lam = {S: sum(mu[T] * np.prod([P[i] for i in coords if i not in T]) for T in subsets if S <= T) for S in subsets}
        if abs(Lam[frozenset()] * nA - M) > 1e-6:
            stats['dich_bad'] += 1
        for S in subsets:
            if S and abs(Lam[S]) > 1e-6 and not F[S]:
                stats['dich_bad'] += 1
        # bounds, all permutations (x,y,z) -> (i,j,k)
        for (i, j, k) in itertools.permutations(coords):
            fi, fj, fk = (frozenset({t}) for t in (i, j, k))
            if not any(F.values()) and nA != 1:
                stats['bound_bad'] += 1                                   # (b0)
            if not F[fj] and not F[fk] and not F[frozenset({j, k})] and nA > P[i]:
                stats['bound_bad'] += 1                                   # (b1)
            if not F[fk] and nA > P[i] * P[j]:
                stats['bound_bad'] += 1                                   # (b2)
            if not F[frozenset({i, j})] and not F[fk] and not F[FULL] and nA > max(P[i], P[j]):
                stats['bound_bad'] += 1                                   # (b3)
        # structure
        def bij(E):
            proj = {tuple(v[i] for i in sorted(E)) for v in A}
            return len(proj) == nA == int(np.prod([P[i] for i in E]))
        E = frozenset(i for i in coords if F[frozenset({i})])
        if not bij(E):
            stats['E_fail'] += 1
            if len(examples) < 3:
                examples.append((A, sorted(E), [sorted(T) for T in subsets if bij(T)]))
        if not any(bij(T) for T in subsets):
            stats['no_transversal'] += 1
    print('box', P, stats)
    for ex in examples:
        print('   step complement, but projection to E not bijective: A =', ex[0], 'E =', ex[1], 'bijective for', ex[2])

if __name__ == '__main__':
    boxes = [tuple(int(c) for c in s.split('x')) for s in sys.argv[1:]] or [(2, 2, 3), (2, 2, 2), (2, 3, 3)]
    for P in boxes:
        run(P)
