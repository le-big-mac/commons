"""Checks on the zero-finder that do not rest on the parity it is supposed to demonstrate.

1. Every zero is a zero: the two fields are interpolated afresh at the reported points; the largest value is printed.
2. The zeros come in antipodal pairs: each has a partner at (-lat, lon + 180); the largest miss is printed.
3. Completeness, by a different route: the other variable eliminated first gives the same set of zeros.
   (Not in the two rows of cells that touch the poles: there the fields do not depend on longitude along the
   polar edge, and only the order used in pairs.py can be solved.  Those cells are covered by check 4.)
4. Completeness, by brute force and without the solver, at a sample of times: every candidate cell is cut into
   64 x 64 sub-cells and the fields evaluated at the sub-nodes.  Every reported zero must lie in a sub-cell where
   both fields change sign; and a sub-cell where both change sign that is not next to a reported zero is cut
   again (16 x 16, twice) to see whether both fields still change sign in one tiny piece of it, which is what a
   missed zero would look like.

usage: python -I check.py DATADIR pairs.npz [slp|pres]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))          # my own directory (python -I leaves it out)
import numpy as np
import pairs

datadir, saved = sys.argv[1], np.load(sys.argv[2])
time, lat, lon, g1, g2 = pairs.load(datadir, sys.argv[3] if len(sys.argv) > 3 else 'slp')
recs, counts = saved['recs'], saved['counts']


def interp(G, la, lo):
    y, x = (90 - la) / 2.5, (lo % 360) / 2.5
    i, j = np.minimum(np.floor(y).astype(int), 71), np.floor(x).astype(int) % 144
    v, u = y - i, x - np.floor(x)
    j1 = (j + 1) % 144
    return (1 - v) * ((1 - u) * G[i, j] + u * G[i, j1]) + v * ((1 - u) * G[i + 1, j] + u * G[i + 1, j1])


def bil(c, vs, us):
    """the bilinear function with corner values c (2 x 2: rows v = 0, 1; columns u = 0, 1) on the grid vs x us"""
    return np.outer(1 - vs, 1 - us) * c[0, 0] + np.outer(1 - vs, us) * c[0, 1] + np.outer(vs, 1 - us) * c[1, 0] + np.outer(vs, us) * c[1, 1]


def changes(F):
    lo_ = np.minimum(np.minimum(F[:-1, :-1], F[:-1, 1:]), np.minimum(F[1:, :-1], F[1:, 1:]))
    hi_ = np.maximum(np.maximum(F[:-1, :-1], F[:-1, 1:]), np.maximum(F[1:, :-1], F[1:, 1:]))
    return (lo_ < 0) & (hi_ > 0)


def deeper(c1, c2, v0, u0, size, depth):
    """Do both fields still change sign in one piece of the square [v0, v0 + size] x [u0, u0 + size] after `depth`
    further cuts into 16 x 16?"""
    m = 16
    vs, us = v0 + size * np.arange(m + 1) / m, u0 + size * np.arange(m + 1) / m
    both = changes(bil(c1, vs, us)) & changes(bil(c2, vs, us))
    if depth == 1:
        return bool(both.any())
    return any(deeper(c1, c2, vs[a], us[b], size / m, depth - 1) for a, b in zip(*np.nonzero(both)))


worst_res = worst_partner = 0.0
differ_swap = polar_zeros = 0
worst_swap = 0.0
for t in range(len(time)):
    r = recs[recs[:, 0] == t]
    la, lo = r[:, 1], r[:, 2]
    assert len(la) == 2 * counts[t]
    worst_res = max(worst_res, np.abs(interp(g1[t], la, lo)).max(), np.abs(interp(g2[t], la, lo)).max())
    # partner at the antipode
    d = np.abs(la[:, None] + la[None, :]) + np.abs((lo[:, None] - lo[None, :] - 180 + 180) % 360 - 180)
    assert (np.argmin(d, axis=1) != np.arange(len(la))).all()
    worst_partner = max(worst_partner, d.min(axis=1).max())
    assert len(set(np.argmin(d, axis=1).tolist())) == len(la)           # a bijection
    la2, lo2 = pairs.zeros(g1[t], g2[t], swap=True)
    k1, k2 = np.abs(la) < 87.5, np.abs(la2) < 87.5                      # leave out the cells that touch the poles
    polar_zeros += int((~k1).sum())
    if k1.sum() != k2.sum():
        differ_swap += 1
    else:
        a, b = np.lexsort((lo[k1], la[k1])), np.lexsort((lo2[k2], la2[k2]))
        worst_swap = max(worst_swap, np.abs(la[k1][a] - la2[k2][b]).max(), np.abs((lo[k1][a] - lo2[k2][b] + 180) % 360 - 180).max())
print(f"1. largest |field| at a reported zero: {worst_res:.2e}")
print(f"2. largest distance from a zero's antipode to the nearest reported zero: {worst_partner:.2e} degrees")
print(f"3. away from the polar cells: times at which eliminating the other variable gives a different number of zeros: {differ_swap} of {len(time)};"
      f" largest difference in position: {worst_swap:.1e} degrees  (zeros in polar cells, left out here: {polar_zeros} of {len(recs)})")

# 4. brute force on a sample of times
n = 64
s = np.arange(n + 1) / n
found = unconfirmed = near2 = near4 = 0
sample = list(range(0, len(time), 37))
for t in sample:
    G1 = np.concatenate([g1[t], g1[t][:, :1]], axis=1)
    G2 = np.concatenate([g2[t], g2[t][:, :1]], axis=1)
    r = recs[recs[:, 0] == t]
    Y, X = (90 - r[:, 1]) / 2.5, r[:, 2] / 2.5                          # reported zeros in units of cells
    zi, zj = np.minimum(np.floor(Y).astype(int), 71), np.floor(X).astype(int) % 144
    seen = np.zeros(len(Y), bool)
    for i in range(72):
        for j in range(144):
            c1, c2 = G1[i:i + 2, j:j + 2], G2[i:i + 2, j:j + 2]
            here = np.nonzero((zi == i) & (zj == j))[0]
            if not (c1.min() < 0 < c1.max() and c2.min() < 0 < c2.max()):
                assert len(here) == 0
                continue
            both = changes(bil(c1, s, s)) & changes(bil(c2, s, s))      # sub-cells that could hold a zero
            for k in here:                                              # every reported zero sits in such a sub-cell
                seen[k] = True
                if both[min(int((Y[k] - i) * n), n - 1), min(int((X[k] - j) * n), n - 1)]:
                    found += 1
                else:
                    unconfirmed += 1
            for a, b in zip(*np.nonzero(both)):                         # and the other such sub-cells?
                d = np.maximum(np.abs(Y - (i + (a + .5) / n)), np.abs((X - (j + (b + .5) / n) + 72) % 144 - 72))
                if d.min() > 1.5 / n + 1e-9:                            # not next to a reported zero (also across cell edges)
                    near2 += deeper(c1, c2, a / n, b / n, 1 / n, 2)
                    near4 += deeper(c1, c2, a / n, b / n, 1 / n, 4)
    assert seen.all()
print(f"4. brute force at {len(sample)} times: reported zeros confirmed by a sign change of both fields in their sub-cell: {found};"
      f" not confirmed: {unconfirmed}")
print(f"   sub-cells away from every reported zero in which both fields still change sign in one piece after two more cuts"
      f" (1/16384 of a cell): {near2}; after four more cuts (1/4194304 of a cell): {near4}")
