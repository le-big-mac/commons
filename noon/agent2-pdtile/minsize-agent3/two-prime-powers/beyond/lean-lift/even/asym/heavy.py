"""Exact share of bad signings of a multiset on Z_n (n odd) given with multiplicities, without listing the 2^m signings:
for each distinct element the signed sum s of its copies takes the values -a, -a+2, ..., a with weights C(a, (a+s)/2);
a vector of signed sums is bad iff sum s_i X^(b_i) is divisible by Phi_d for some d | n (tested in integers).
Prints the share and share * sqrt(pi m / 2) (which is 1 + o(1) for m copies of one element, m even).
usage: heavy.py N  'b:a,b:a,...'  [more multisets]      or   heavy.py N family 'b:a,...' H_FROM H_TO   (h copies of 0 added)"""
import sys, itertools, math
from fractions import Fraction
import numpy as np
sys.path.insert(0, '/home/agent3/lean/lift-check/even/shares')
from minshare import red_matrix
def share(R, blocks, items):
    items = [(b, a) for (b, a) in items if a > 0]
    m = sum(a for _, a in items)
    grids = [np.arange(-a, a + 1, 2, dtype=np.int64) for _, a in items]
    wts = [np.array([math.comb(a, (a + int(s)) // 2) for s in g], dtype=object) for (_, a), g in zip(items, grids)]
    S = np.array(np.meshgrid(*grids, indexing='ij')).reshape(len(items), -1)                 # k x G
    W = wts[0]
    for w in wts[1:]: W = np.multiply.outer(W, w)
    W = W.reshape(-1)
    V = R[:, [b for b, _ in items]] @ S
    bad = np.zeros(S.shape[1], dtype=bool)
    for (start, k, d) in blocks: bad |= ~np.any(V[start:start + k] != 0, axis=0)
    return Fraction(int(W[bad].sum()), 2 ** m), m
def parse(t): return [(int(x.split(':')[0]), int(x.split(':')[1])) for x in t.split(',') if x]
if __name__ == '__main__':
    n = int(sys.argv[1]); R, blocks = red_matrix(n)
    if sys.argv[2] == 'family':
        D = parse(sys.argv[3])
        for h in range(int(sys.argv[4]), int(sys.argv[5]) + 1):
            s, m = share(R, blocks, [(0, h)] + D)
            print(f"n = {n}  {h} copies of 0 with {sys.argv[3]}:  m = {m:3d}  bad share {float(s):.6f}  times sqrt(pi m/2) = {float(s) * math.sqrt(math.pi * m / 2):.4f}", flush=True)
    else:
        for t in sys.argv[2:]:
            s, m = share(R, blocks, parse(t))
            print(f"n = {n}  {t}:  m = {m}  bad share {s} = {float(s):.6f}  times sqrt(pi m/2) = {float(s) * math.sqrt(math.pi * m / 2):.4f}", flush=True)
