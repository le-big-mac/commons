# Theorem B, brute force from the definition (remainder modulo Phi_d for every d | n), every multiset with 0 of
# 2, 3, 4 elements on Z_n (the statement is invariant under translation), every signing with the first sign +.
#   m = 2: a good signing exists iff 2^k | a - b.
#   m = 3: at most two of the four signings are bad (sets AND multisets); recorded: the distribution.
#   m = 4: a signing is good on Z_n  iff  the same signs are good for the residues modulo 2^k on Z_{2^k}
#          (computed separately, with the tables of Z_{2^k}); and a good signing exists.
# usage: tB.py n1 n2 ...   or   tB.py lo-hi
import sys, itertools
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rlib import table, divisors, split2

def run(n):
    k, npr = split2(n)
    K = 1 << k
    ds = divisors(n)
    res = {}
    # ---- m = 2
    for b in range(n):
        goods = 0
        for s in (1, -1):
            badsomewhere = False
            for d in ds:
                T = table(n, d)
                if not (T[0] + s * T[b]).any():
                    badsomewhere = True
            goods += not badsomewhere
        assert (goods > 0) == (b % K == 0), (n, b)
    # ---- m = 3
    xs, ys = np.triu_indices(n)                 # 0 <= x <= y < n
    bad = np.zeros((4, len(xs)), dtype=bool)
    for d in ds:
        T = table(n, d).astype(np.int16)
        if T.shape[1] == 0:
            continue
        Tx, Ty = T[xs], T[ys]
        i = 0
        for s1 in (1, -1):
            A = T[0][None, :] + s1 * Tx
            for s2 in (1, -1):
                bad[i] |= (A == -s2 * Ty).all(axis=1)
                i += 1
    nbad = bad.sum(axis=0)
    assert nbad.max() <= 2, (n, "m=3")
    isset = (xs != 0) & (ys != xs)
    hist3 = [int(((nbad == t) & isset).sum()) for t in range(3)]
    notset_bad = int(nbad[~isset].max()) if (~isset).any() else 0
    # ---- m = 4
    trip = np.array(list(itertools.combinations_with_replacement(range(n), 3)), dtype=np.int32)
    M = len(trip)
    nb4 = 0
    hist4 = np.zeros(9, dtype=np.int64)
    CH = 150000
    for lo in range(0, M, CH):
        X, Y, Z = trip[lo:lo + CH, 0], trip[lo:lo + CH, 1], trip[lo:lo + CH, 2]
        badn = np.zeros((8, len(X)), dtype=bool)
        bad2 = np.zeros((8, len(X)), dtype=bool)
        for d in ds:
            T = table(n, d).astype(np.int16)
            assert np.abs(table(n, d)).max() < 2000
            _acc(badn, T, X, Y, Z)
        for j in range(k + 1):
            T = table(K, 1 << j).astype(np.int16)
            _acc(bad2, T, X % K, Y % K, Z % K)
        assert (badn == bad2).all(), (n, "m=4: good on Z_n differs from good modulo 2^k")
        g = (~badn).sum(axis=0)
        assert g.min() >= 1, (n, "m=4: no good signing")
        hist4 += np.bincount(g, minlength=9)
        nb4 += len(X)
    print("n=%d (2^%d*%d): m=2 ok (%d pairs); m=3: %d multisets, bad signings of 4 among the sets: none/1/2 = %d/%d/%d, among the non-sets at most %d;"
          " m=4: %d multisets, good on Z_n = good mod 2^k for all 8 signings of each; least number of good of 8: %d"
          % (n, k, npr, n, len(xs), hist3[0], hist3[1], hist3[2], notset_bad, nb4, int(np.nonzero(hist4)[0][0])), flush=True)
    return len(xs), nb4

def _acc(bad, T, X, Y, Z):
    if T.shape[1] == 0:
        return
    Tx, Ty, Tz = T[X], T[Y], T[Z]
    A = {1: T[0][None, :] + Tx, -1: T[0][None, :] - Tx}
    Bp = {1: Ty + Tz, -1: Ty - Tz}
    i = 0
    for s1 in (1, -1):
        for s2 in (1, -1):
            for s3 in (1, -1):
                # 1 + s1 x + s2 y + s3 z = A[s1] + s2 (y + s2 s3 z)
                Bm = Bp[s2 * s3]
                if s2 == 1:
                    bad[i] |= (A[s1] == -Bm).all(axis=1)
                else:
                    bad[i] |= (A[s1] == Bm).all(axis=1)
                i += 1

ns = []
for a in sys.argv[1:]:
    if '-' in a:
        lo, hi = a.split('-')
        ns += list(range(int(lo), int(hi) + 1))
    else:
        ns.append(int(a))
t3 = t4 = 0
for n in ns:
    a, b = run(n)
    t3 += a; t4 += b
print("TOTAL: %d moduli; %d multisets of three elements, %d of four; no failure" % (len(ns), t3, t4))
