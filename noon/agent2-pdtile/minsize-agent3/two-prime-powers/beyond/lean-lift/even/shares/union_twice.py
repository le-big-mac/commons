"""Test of the union form of "twice": for a multiset B on Z_n, n = 2^k n', the number of signings bad at SOME divisor of n
is at most twice the number of signings bad at some divisor of n' for the reduction of B modulo n'.
Exhaustive over every multiset of m elements containing 0 (first sign +; both counts are then halves of the full counts).
Exact integer arithmetic (remainders modulo the cyclotomic polynomials).
usage: union_twice.py M N [N ...]      prints for each n: multisets, failures, largest ratio, how many attain ratio 2
(among those with a bad signing on the odd part), and the number of multisets whose odd part has no bad signing but
which have one on Z_n (must be 0)."""
import sys, itertools
from fractions import Fraction
import numpy as np
from minshare import red_matrix
def badcount(R, blocks, XS, E):
    V = R[:, XS] @ E
    bad = np.zeros(V.shape[1:], dtype=bool)
    for (start, k, d) in blocks: bad |= ~np.any(V[start:start + k] != 0, axis=0)
    return bad.sum(axis=1)
def run(n, m, batch=20000):
    n1 = n
    while n1 % 2 == 0: n1 //= 2
    R, blocks = red_matrix(n); R1, blocks1 = red_matrix(n1)
    E = np.array([[1] + [1 if (s >> i) & 1 else -1 for i in range(m - 1)] for s in range(2 ** (m - 1))], dtype=np.int64).T
    count = fails = eq = zero_viol = 0; best = Fraction(0); ex = None
    it = itertools.combinations_with_replacement(range(n), m - 1)
    while True:
        chunk = list(itertools.islice(it, batch))
        if not chunk: break
        XS = np.zeros((len(chunk), m), dtype=np.int64); XS[:, 1:] = np.array(chunk, dtype=np.int64)
        b = badcount(R, blocks, XS, E); b1 = badcount(R1, blocks1, XS % n1, E)
        count += len(chunk)
        fails += int((b > 2 * b1).sum()); zero_viol += int(((b1 == 0) & (b > 0)).sum())
        nz = b1 > 0
        eq += int((b[nz] == 2 * b1[nz]).sum())
        if nz.any():
            i = np.argmax(b[nz] / b1[nz]); r = Fraction(int(b[nz][i]), int(b1[nz][i]))
            if r > best: best = r; ex = tuple(int(v) for v in XS[nz][i])
    return count, fails, best, eq, zero_viol, ex
if __name__ == '__main__':
    m = int(sys.argv[1])
    for n in map(int, sys.argv[2:]):
        c, f, best, eq, z, ex = run(n, m)
        print(f"m = {m}  n = {n:4d}  multisets {c:9d}  FAILURES {f}  largest ratio {best}  ratio 2 attained by {eq}  bad on Z_n but none on the odd part: {z}  e.g. {ex}", flush=True)
