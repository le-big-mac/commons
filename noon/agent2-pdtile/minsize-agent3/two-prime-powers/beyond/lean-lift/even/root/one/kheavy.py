"""K(D) for one heavy element: h copies of 0 and a decoration D on Z_n (n odd), exact.

A signing is bad iff T + Q(zeta) = 0 for some n-th root of unity zeta (T the signed sum of the heavy copies, Q the
signed mask of D).  K_same(D) = the expected number of distinct integers v = -Q(zeta) with v = |D| (mod 2)
(the case m = h + |D| even), K_other(D) the same with v = |D| + 1 (mod 2) (m odd).  As h grows the bad share is
K sqrt(2/(pi m)) (1 + o(1)) (the brief's data section).  Written from the definitions, independent of kdec.py.

usage: kheavy.py N 'b:a,b:a,...' [more decorations]
"""
import sys, math
from fractions import Fraction
import numpy as np
sys.path.insert(0, '/home/agent3/lean/lift-check/even/root/one')
from test_lemmas import red_matrix, divisors

def K(n, items):
    acc = {}
    for b, a in items:
        if b % n and a > 0: acc[b % n] = acc.get(b % n, 0) + a
    items = sorted(acc.items()); r = sum(a for _, a in items)
    res = [b for b, _ in items]
    grids = [np.arange(-a, a + 1, 2, dtype=np.int64) for _, a in items]
    S = np.array(np.meshgrid(*grids, indexing='ij')).reshape(len(items), -1)
    W = None
    for (_, a), g in zip(items, grids):
        w = np.array([math.comb(a, (a + int(s)) // 2) for s in g], dtype=object)
        W = w if W is None else np.multiply.outer(W, w)
    W = W.reshape(-1)
    BIG = 10 ** 9
    out = []
    for par in (r % 2, (r + 1) % 2):
        rows = []
        for d in divisors(n):
            V = red_matrix(n, d)[:, res] @ S                    # Q modulo Phi_d
            const = ~np.any(V[1:] != 0, axis=0) if V.shape[0] > 1 else np.ones(S.shape[1], dtype=bool)
            v = -V[0]
            ok = const & ((v - par) % 2 == 0)
            rows.append(np.where(ok, v, BIG))
        A = np.sort(np.array(rows), axis=0)
        cnt = (A[0] != BIG).astype(np.int64)
        for i in range(1, A.shape[0]):
            cnt += ((A[i] != BIG) & (A[i] != A[i - 1])).astype(np.int64)
        tot = sum(int(w) * int(c) for w, c in zip(W, cnt))
        out.append(Fraction(tot, 2 ** r))
    return out, r

if __name__ == '__main__':
    n = int(sys.argv[1])
    for t in sys.argv[2:]:
        items = [(int(x.split(':')[0]), int(x.split(':')[1])) for x in t.split(',') if x]
        (ks, ko), r = K(n, items)
        s2 = math.sqrt(2 / math.pi)
        print(f"n = {n}  D = {t}  ({r} elements):  K_same = {ks} = {float(ks):.6f}  (times sqrt(2/pi): {float(ks) * s2:.5f})   "
              f"K_other = {ko} = {float(ko):.6f}  (times sqrt(2/pi): {float(ko) * s2:.5f})", flush=True)
