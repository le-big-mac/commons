"""Largest share of BAD signings, by exhaustion (the mirror of minshare.py: it reports the least share of good ones;
this one prints the bad share, how many multisets attain it, and examples, and also the largest share of signings bad
at some divisor > 1 and not at 1).
usage: maxbad.py M N [N ...]"""
import sys, itertools
from fractions import Fraction
import numpy as np
from minshare import red_matrix
def run(n, m, batch=20000):
    R, blocks = red_matrix(n)
    E = np.array([[1] + [1 if (s >> i) & 1 else -1 for i in range(m - 1)] for s in range(2 ** (m - 1))], dtype=np.int64).T
    best = -1; ex = []; count = 0; best2 = -1; ex2 = None
    it = itertools.combinations_with_replacement(range(n), m - 1)
    while True:
        chunk = list(itertools.islice(it, batch))
        if not chunk: break
        XS = np.zeros((len(chunk), m), dtype=np.int64); XS[:, 1:] = np.array(chunk, dtype=np.int64)
        V = R[:, XS] @ E
        bad = np.zeros(V.shape[1:], dtype=bool); bad1 = None
        for (start, k, d) in blocks:
            z = ~np.any(V[start:start + k] != 0, axis=0)
            if d == 1: bad1 = z
            bad |= z
        b = bad.sum(axis=1); b2 = (bad & ~bad1).sum(axis=1); count += len(chunk)
        g = int(b.max())
        if g > best: best = g; ex = []
        if g == best and len(ex) < 2: ex.append(tuple(int(v) for v in XS[int(np.argmax(b))]))
        g2 = int(b2.max())
        if g2 > best2: best2 = g2; ex2 = tuple(int(v) for v in XS[int(np.argmax(b2))])
    d = 2 ** (m - 1)
    return count, Fraction(best, d), ex, Fraction(best2, d), ex2
if __name__ == '__main__':
    m = int(sys.argv[1])
    for n in map(int, sys.argv[2:]):
        c, sh, ex, sh2, ex2 = run(n, m)
        print(f"m = {m:2d}  n = {n:4d}  multisets {c:9d}  largest bad share {str(sh):>9s} = {float(sh):.4f}  e.g. {ex[0]}   |  largest share bad somewhere but not at 1: {str(sh2):>8s} = {float(sh2):.4f}  e.g. {ex2}", flush=True)
