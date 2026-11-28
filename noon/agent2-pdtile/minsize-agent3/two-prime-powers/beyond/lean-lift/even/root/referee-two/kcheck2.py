# As kcheck.py, for decorations with any multiplicities (an element of multiplicity mu has signed sum s with weight
# C(mu, (mu+s)/2)).  K_same: the expected number of distinct EVEN integers v with Phi_d | v + Q(X) for some d | n.
# Used (a) to see whether pairs are the best decorations on powers of 3 (the text's "points to 7/6"), and
# (b) for the comparison with the two other texts (their larger K on Z_135).
import sys, itertools
import numpy as np
from fractions import Fraction as F
from math import comb
from kcheck import divisors, redmat

def K(n, items):
    res = sorted(items); mus = [items[b] for b in res]
    axes = [np.arange(-mu, mu + 1, 2, dtype=np.int64) for mu in mus]
    wax = [np.array([comb(mu, i) for i in range(mu + 1)], dtype=np.int64) for mu in mus]
    grids = np.meshgrid(*axes, indexing="ij"); wg = np.meshgrid(*wax, indexing="ij")
    V = np.stack([g.ravel() for g in grids], axis=1)
    W = np.ones(len(V), dtype=np.int64)
    for w in wg: W *= w.ravel()
    mats = [(d, redmat(d)[:, [b % d for b in res]].T.copy()) for d in divisors(n)]
    total = 0
    for lo in range(0, len(V), 100000):
        Vc = V[lo:lo + 100000]; vals = []
        for d, C in mats:
            Q = Vc @ C
            ok = ~(Q[:, 1:] != 0).any(axis=1) if Q.shape[1] > 1 else np.ones(len(Vc), dtype=bool)
            vals.append(np.where(ok & (Q[:, 0] % 2 == 0), -Q[:, 0], 10**6 + len(vals)))
        A = np.sort(np.stack(vals, axis=1), axis=1)
        distinct = (A < 10**6).sum(axis=1) - ((np.diff(A, axis=1) == 0) & (A[:, 1:] < 10**6)).sum(axis=1)
        total += int((distinct * W[lo:lo + 100000]).sum())
    return F(total, 2 ** sum(mus))

cases = [
    ("Z_3: fours at 1, 2", 3, {1: 4, 2: 4}),
    ("Z_3: sixes at 1, 2", 3, {1: 6, 2: 6}),
    ("Z_9: fours at 1, 2; pairs at 3, 6", 9, {1: 4, 2: 4, 3: 2, 6: 2}),
    ("Z_9: pairs at 1, 2; fours at 3, 6", 9, {1: 2, 2: 2, 3: 4, 6: 4}),
    ("Z_9: fours at 1, 2, 3, 6", 9, {1: 4, 2: 4, 3: 4, 6: 4}),
    ("Z_27: pairs at 1, 2, 3, 6; fours at 9, 18", 27, {1: 2, 2: 2, 3: 2, 6: 2, 9: 4, 18: 4}),
    ("Z_27: fours at 1, 2, 3, 6, 9, 18", 27, {1: 4, 2: 4, 3: 4, 6: 4, 9: 4, 18: 4}),
    ("Z_81: pairs at 1, 2, 3, 6, 9, 18; fours at 27, 54", 81, {1: 2, 2: 2, 3: 2, 6: 2, 9: 2, 18: 2, 27: 4, 54: 4}),
    ("Z_81: fours at 1, 2, 3, 6, 9, 18, 27, 54", 81, {1: 4, 2: 4, 3: 4, 6: 4, 9: 4, 18: 4, 27: 4, 54: 4}),
    ("Z_135 (text one): pairs at 5, 10, 15, 30; fours at 45, 90; pairs at 27, 54, 81, 108", 135,
     {5: 2, 10: 2, 15: 2, 30: 2, 45: 4, 90: 4, 27: 2, 54: 2, 81: 2, 108: 2}),
    ("Z_135 (text one): the same with fours at 27, 54, 81, 108", 135,
     {5: 2, 10: 2, 15: 2, 30: 2, 45: 4, 90: 4, 27: 4, 54: 4, 81: 4, 108: 4}),
]
for name, n, items in cases:
    k = K(n, items)
    print(f"{name}: K = {k} = {float(k):.6f} (times sqrt(2/pi): {float(k)*0.7978845608:.6f}); 7/6 = {7/6:.6f}", flush=True)
