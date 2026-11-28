"""Tests for limits.md, by exact counts over all signings.
(1) Lemma 1 (two factors): for every multiset containing 0 of m elements on Z_n, every divisor d > 1 of n and every
    residue x modulo d with fewer than m elements in its class:  #bad at d  <=  c_a * c_(m-a) * 2^m.
(2) "From below": for a decoration D on Z_L and h copies of 0, the share of bad signings against c_h * K_pi(D).
usage: test_two_factors.py"""
import sys, itertools, math
from fractions import Fraction
import numpy as np
sys.path.insert(0, '/home/agent3/lean/lift-check/even/shares'); sys.path.insert(0, '/home/agent3/lean/lift-check/even/asym')
from minshare import red_matrix
from kdec import K
from heavy import share
def c(r): return Fraction(1) if r == 0 else Fraction(math.comb(r, r // 2), 2 ** r)
def lemma1(n, m):
    R, blocks = red_matrix(n)
    E = np.array(list(itertools.product((1, -1), repeat=m)), dtype=np.int64).T
    cases = 0; worst = Fraction(0); eq = 0
    for rest in itertools.combinations_with_replacement(range(n), m - 1):
        xs = (0,) + rest
        V = R[:, list(xs)] @ E
        for (start, k, d) in blocks:
            if d == 1: continue
            bad = int((~np.any(V[start:start + k] != 0, axis=0)).sum())
            for x in range(d):
                a = sum(1 for b in xs if b % d == x)
                if a == m: continue
                bound = c(a) * c(m - a) * 2 ** m
                cases += 1
                assert bad <= bound, (n, xs, d, x, a, bad, bound)
                if bound > 0:
                    q = Fraction(bad) / bound
                    if q > worst: worst = q
                    if q == 1: eq += 1
    return cases, worst, eq
if __name__ == '__main__':
    tot = 0
    for n, mmax in ((3, 10), (5, 8), (7, 7), (9, 8), (15, 6), (21, 5), (25, 5), (27, 5), (45, 4), (105, 3)):
        for m in range(2, mmax + 1):
            cases, worst, eq = lemma1(n, m); tot += cases
            print(f"Lemma 1: n = {n:3d}  m = {m:2d}: {cases:8d} cases (multiset, d, x); largest count/bound {float(worst):.4f}; equal to the bound in {eq}", flush=True)
    print(f"Lemma 1: {tot} cases in all, no failure", flush=True)
    for (L, D, name) in ((3, [1, 1, 2, 2], "pairs at 1 and 2 on Z_3"), (9, [1, 1, 2, 2, 3, 3, 6, 6], "pairs at 1, 2, 3, 6 on Z_9"), (15, [10, 5, 3, 6, 9, 12], "one element in each nonzero class modulo 3 and 5, on Z_15")):
        R, blocks = red_matrix(L); r = len(D)
        ks, ko = K(R, blocks, D)
        items = sorted(set(D)); mult = [(b, D.count(b)) for b in items]
        for h in (r % 2 + 2, r % 2 + 20, r % 2 + 200, r % 2 + 2000, (r + 1) % 2 + 1, (r + 1) % 2 + 21, (r + 1) % 2 + 201, (r + 1) % 2 + 2001):
            s, m = share(R, blocks, [(0, h)] + mult)
            kk = ks if (h - r) % 2 == 0 else ko
            print(f"from below: {name}: h = {h:5d} (m = {m}, {'even' if m % 2 == 0 else 'odd'}): share / c_h = {float(s / c(h)):.5f}; K = {kk} = {float(kk):.5f}; share <= c_h K: {s <= c(h) * kk}", flush=True)
