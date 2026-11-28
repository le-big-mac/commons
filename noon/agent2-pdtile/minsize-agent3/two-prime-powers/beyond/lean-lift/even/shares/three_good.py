"""On a modulus n prime to 6: the largest share of signings that are NOT 3-good, over all multisets of m elements
containing 0.  A signing is 3-bad at e | n if the remainder of its signed mask modulo Phi_e has every coefficient
divisible by 3 (for 3 not dividing e this is "Phi_e divides the mask modulo 3"); not 3-good: 3-bad at some e | n.
Every signing with the first sign + (a global sign changes nothing).  Exact integers.
usage: three_good.py M N [N ...]"""
import sys, itertools
from fractions import Fraction
import numpy as np
from minshare import red_matrix
def run(n, m, batch=20000):
    assert n % 2 and n % 3
    R, blocks = red_matrix(n)
    E = np.array([[1] + [1 if (s >> i) & 1 else -1 for i in range(m - 1)] for s in range(2 ** (m - 1))], dtype=np.int64).T
    worst = -1; ex = []; count = 0; nworst = 0
    it = itertools.combinations_with_replacement(range(n), m - 1)
    while True:
        chunk = list(itertools.islice(it, batch))
        if not chunk: break
        XS = np.zeros((len(chunk), m), dtype=np.int64); XS[:, 1:] = np.array(chunk, dtype=np.int64)
        V = (R[:, XS] @ E) % 3
        bad = np.zeros(V.shape[1:], dtype=bool)
        for (start, k, d) in blocks: bad |= ~np.any(V[start:start + k] != 0, axis=0)
        b = bad.sum(axis=1); count += len(chunk)
        g = int(b.max())
        if g > worst: worst = g; ex = []; nworst = 0
        if g == worst:
            idx = np.nonzero(b == g)[0]; nworst += len(idx)
            for i in idx[:2]:
                if len(ex) < 2: ex.append(tuple(int(v) for v in XS[i]))
    return count, Fraction(worst, 2 ** (m - 1)), nworst, ex
if __name__ == '__main__':
    m = int(sys.argv[1])
    for n in map(int, sys.argv[2:]):
        c, sh, nb, ex = run(n, m)
        print(f"m = {m}  n = {n:4d}  multisets {c:9d}  largest share not 3-good {str(sh):>7s} = {float(sh):.5f}  (3/8 = 0.375)  attained by {nb:6d}  e.g. {ex}", flush=True)
