"""Lemma P by exhaustion: every multiset of K parts r_i >= 1 with sum M <= MMAX: prod c_(r_i) <= 2^(1-K) c*_(M-2K+2);
h_M(K+1) <= h_M(K) for all K >= 1 (also K > M); g(a) g(b) <= g(1) g(a+b-1); c_(r-2) <= 2 c_r, <= (4/3) c_r for r >= 4.
usage: lemmaP.py MMAX"""
import sys, math
from fractions import Fraction as Fr
def c(r): return Fr(math.comb(r, r // 2), 2 ** r)
def cs(r): return Fr(1, 2) if r <= 0 else c(r)
def g(j): return Fr(math.comb(2 * j, j), 4 ** j)
def parts(M, K, lo=1):
    if K == 1:
        if M >= lo: yield (M,)
        return
    for r in range(lo, M // K + 1):
        for rest in parts(M - r, K - 1, r): yield (r,) + rest
MMAX = int(sys.argv[1]); n = 0; eq = 0; bad = 0
for M in range(1, MMAX + 1):
    for K in range(1, M + 1):
        h = Fr(1, 2 ** (K - 1)) * cs(M - 2 * K + 2)
        for p in parts(M, K):
            pr = Fr(1)
            for r in p: pr *= c(r)
            n += 1
            if pr > h: bad += 1; print("FAIL", p)
            if pr == h: eq += 1
    for K in range(1, M + 5):
        if Fr(1, 2 ** K) * cs(M - 2 * K) > Fr(1, 2 ** (K - 1)) * cs(M - 2 * K + 2): bad += 1; print("FAIL monotony", M, K)
print(f"Lemma P: {n} partitions of M <= {MMAX}, equalities {eq}, failures {bad}")
print("c_(2j-1) = c_(2j) = g(j), j <= 200:", all(c(2 * j - 1) == c(2 * j) == g(j) for j in range(1, 201)))
print("g(a) g(b) <= g(1) g(a+b-1), a, b <= 150:", all(g(a) * g(b) <= g(1) * g(a + b - 1) for a in range(1, 151) for b in range(a, 151)))
print("c*_(r-2) <= 2 c*_r for -10 <= r <= 400:", all(cs(r - 2) <= 2 * cs(r) for r in range(-10, 401)), ";  c_(r-2) <= (4/3) c_r for 4 <= r <= 400:", all(3 * c(r - 2) <= 4 * c(r) for r in range(4, 401)))
