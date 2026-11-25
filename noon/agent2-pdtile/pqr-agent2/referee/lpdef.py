"""Decide pd-tiling FROM ITS DEFINITION, on concrete sets, with a linear program (HiGHS, floating point):
   maximise f(0) over real f on Z_M with f >= 0, hat f >= 0 (real part >= 0, imaginary part = 0),
   (1_A * f)(x) = 1 for all x.      A pd-tiles  iff  the maximum is 1  (it is always <= 1, see below).
Compare with the exact value D+(Z_A)/|A| (dplus.py) for three representatives of every realised
(pattern, size) class of M = 30 (representatives written by enum.c: smallest bitmask, largest, a hashed one).

Why max f(0) <= 1 and why it should equal D+(Z_A)/|A|:  1_A * f = 1 forces hat f = 0 wherever hat 1_A != 0
(off 0) and hat f(0) = M/|A|; then h = (|A|/M) hat f is admissible for D+(Z_A) and sum h = |A| f(0).
The script does not use this: it solves the LP on the set itself and only compares at the end.
usage: lpdef.py p0 p1 p2 histfile
"""
import sys
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, '/tmp/agent2_referee3')
from dplus import dplus, describe

p = tuple(int(a) for a in sys.argv[1:4]); M = p[0]*p[1]*p[2]
x = np.arange(M)
COS = np.cos(2*np.pi*np.outer(x, x)/M); SIN = np.sin(2*np.pi*np.outer(x, x)/M)

def maxf0(A):
    """A: list of elements."""
    conv = np.zeros((M, M))
    for a in A:
        for y in range(M):
            conv[y, (y - a) % M] += 1          # (1_A * f)(y) = sum_a f(y - a)
    c = np.zeros(M); c[0] = -1
    res = linprog(c, A_ub=-COS, b_ub=np.zeros(M), A_eq=np.vstack([conv, SIN]), b_eq=np.concatenate([np.ones(M), np.zeros(M)]),
                  bounds=[(0, None)]*M, method='highs')
    if res.status == 2:
        return None      # infeasible: no f at all
    assert res.status == 0, res.message
    return -res.fun

rows = []
for line in open(sys.argv[4]):
    if line[0] == '#': continue
    f = line.split()
    rows.append((int(f[0]), int(f[1]), int(f[2]), [int(f[4]), int(f[5]), int(f[6])]))
D = {m: dplus(p, m) for m in range(128)}
worst = 0; nlp = 0; npd = 0; disagree = 0; pdsets = 0
for mask, n, cnt, reps in rows:
    for r in sorted(set(reps)):
        A = [e for e in range(M) if r >> e & 1]
        assert len(A) == n
        v = maxf0(A); nlp += 1
        target = float(D[mask]) / n
        if v is None:
            print("LP infeasible for", A); disagree += 1; continue
        worst = max(worst, abs(v - target))
        lp_pd = v > 1 - 1e-7
        ex_pd = (D[mask] == n)
        if lp_pd != ex_pd:
            disagree += 1; print("DISAGREE", describe(p, mask), n, A, v, target)
        if lp_pd: pdsets += 1
    if D[mask] == n: npd += 1
print(f"M={M}: {len(rows)} classes, {nlp} LPs solved on concrete sets; max |max f(0) - D+(Z_A)/|A|| = {worst:.2e}")
print(f"classes with |A| = D+(Z_A): {npd}; representative sets the LP calls pd-tiling: {pdsets}; disagreements LP vs exact: {disagree}")
# smallest gap 1 - D+/n over non-pd classes, to show the 1e-7 threshold is safe
gap = min(1 - float(D[m])/n for m, n, c, r in rows if D[m] != n)
print("smallest value of 1 - D+(Z_A)/|A| over the non-pd classes:", gap)
