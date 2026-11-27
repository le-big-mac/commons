"""Referee, third pass: on the remark of section 6 of sign-all-result.md that the union over the levels P' of Y of the
lost sets is small while their sum is not.  Box Z_9 x Z_3 over Q (T = Z_9 new, Y = Z_3 with its two levels).
For a given g and each of the 8 patterns sigma of Y: the shares (among the sign vectors on the active rows) of
Lost(sigma, 0), Lost(sigma, 1), of their union, and then the share of lost pairs over all sigma.
A search over functions with slices of rank two for the largest union for a single sigma."""
import sys
import numpy as np
from fractions import Fraction as Fr
from itertools import product
from treetools import level_matrix, all_signs

T = (3, 2); Y = (3, 1)
MT = [level_matrix(3, 2, i) for i in range(3)]; MY = [level_matrix(3, 1, j) for j in range(2)]

def shares(g):
    act = np.nonzero(g.any(axis=1))[0]
    ST = np.ones((2 ** len(act), 9), dtype=np.int64); ST[:, act] = all_signs(len(act))
    SY = all_signs(3); BT = ST.shape[0]
    nz = [[None, None] for _ in range(3)]
    for i in range(3):
        P = (MT[i][None] * ST[:, None, :]) @ g
        for j in range(2):
            R = np.tensordot(P, SY[:, None, :] * MY[j][None], axes=([2], [2]))
            nz[i][j] = (R != 0).any(axis=(1, 3))
    A = nz[0][0] & nz[0][1]
    out = []; lost_all = 0
    for b in range(8):
        l0 = A[:, b] & (~nz[1][0][:, b] | ~nz[2][0][:, b]); l1 = A[:, b] & (~nz[1][1][:, b] | ~nz[2][1][:, b])
        out.append((SY[b].tolist(), Fr(int(l0.sum()), BT), Fr(int(l1.sum()), BT), Fr(int((l0 | l1).sum()), BT)))
        lost_all += int((l0 | l1).sum())
    good = np.ones_like(A)
    for i in range(3):
        for j in range(2): good &= nz[i][j]
    return out, Fr(lost_all, BT * 8), Fr(int(good.sum()), BT * 8)

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
best = None
vecs = [np.array(v) for v in product((-1, 0, 1), repeat=3) if any(v)]
for trial in range(4000):
    # g = 1_{D1} (x) h1 + 1_{D2} (x) h2, D1, D2 small sets of rows
    g = np.zeros((9, 3), dtype=np.int64)
    for _ in range(2):
        rows = rng.permutation(9)[:rng.integers(1, 5)]
        g[rows] += vecs[rng.integers(0, len(vecs))][None, :] * rng.choice([1, -1], size=(len(rows), 1))
    if np.linalg.matrix_rank(g) < 2: continue
    out, lost_all, good = shares(g)
    m = max(o[3] for o in out)
    if best is None or m > best[0] or (m == best[0] and lost_all < best[2]):
        best = (m, g.copy(), lost_all, good, out)
m, g, lost_all, good, out = best
print('box Z_9 x Z_3 over Q, functions whose slices span a plane: the largest union found for a single sigma_Y is', m, '(2^(1-p) = 1/4, L_Y 2^(1-p) = 1/2)')
print('at g (rows v = 0..8, columns y = 0..2):', g.tolist())
for o in out:
    print(f'   sigma_Y = {o[0]}: share lost at the level 0 of Y: {o[1]}, at the level 1: {o[2]}, union: {o[3]}, sum: {o[1] + o[2]}')
print(f'   over all sigma_Y: share of pairs lost at some level: {lost_all}; share of good pairs: {good}')
