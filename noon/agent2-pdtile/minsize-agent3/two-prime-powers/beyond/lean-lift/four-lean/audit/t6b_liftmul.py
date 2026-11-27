"""The fact behind sizes_eq_mul_all, for a general factor s: every nonempty multiset w on Z_N is the reduction modulo N
of a multiset w' on Z_{Ns}, of the same size, whose mask is divisible by no Phi_d with d | Ns, d not dividing N.
(Then w' has, among the d != 1 dividing Ns, exactly the cyclotomic divisors that w has among those dividing N, which
gives the inclusion "sizes on Z_N are sizes on Z_{Ns}" at EVERY size; the other inclusion is reduction.)

For N, s and every multiset of m elements of Z_N that contains 0: each element x goes to one of x + jN, 0 <= j < s
(these are the residues modulo Ns that reduce to x).  Adding N to every element keeps the divisors, so the first element
keeps j = 0; the choices are tried by increasing number of elements with j != 0, all s^(m-1) of them before a multiset
is declared to have no such lift.  Exact: remainders of X^y modulo Phi_d as integer vectors.
The largest m for each pair is the largest for which multisets x (Ns - N) x m stays within BUDGET, at most MMAX.
usage: t6b_liftmul.py BUDGET MMAX N1,N2,... s1,s2,..."""
import os
import sys
import time
from itertools import combinations, combinations_with_replacement, islice, chain, product
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import core
from t3_a1 import big_table
from t6_mul import is_pnq


def choices(m, s):
    """j-vectors with j[0] = 0, by increasing number of nonzero entries"""
    for k in range(0, m):
        for pos in combinations(range(1, m), k):
            for vals in product(range(1, s), repeat=k):
                j = [0] * m
                for p_, v in zip(pos, vals):
                    j[p_] = v
                yield j


def run(N, s, m, Tall, sl, batch_cells=24_000_000):
    M = N * s
    cols = Tall.shape[1]
    B = max(1000, batch_cells // max(cols, 1))
    it = combinations_with_replacement(range(N), m - 1)
    total = low_fail = none = 0
    maxtried = 1
    examples = []
    while True:
        flat = np.fromiter(chain.from_iterable(islice(it, B)), dtype=np.int32)
        if flat.size == 0 and m > 1:
            break
        E = np.zeros((flat.size // (m - 1) if m > 1 else 1, m), dtype=np.int32)
        if m > 1:
            E[:, 1:] = flat.reshape(-1, m - 1)
        total += E.shape[0]
        rest = E
        for idx, j in enumerate(choices(m, s)):
            R = np.zeros((rest.shape[0], cols), dtype=np.int16)
            for k in range(m):
                R += Tall[rest[:, k] + N * j[k]]
            b = np.zeros(rest.shape[0], dtype=bool)
            for d, (a, c) in sl.items():
                b |= ~R[:, a:c].any(axis=1)
            if idx == 0:
                low_fail += int(b.sum())
            if (~b).any():
                maxtried = max(maxtried, idx + 1)
            rest = rest[b]
            if rest.shape[0] == 0:
                break
        else:
            none += rest.shape[0]
            examples += rest[:3].tolist()
        if m == 1:
            break
    assert total == comb(N + m - 2, m - 1)
    return total, low_fail, maxtried, none, examples


if __name__ == '__main__':
    budget = int(float(sys.argv[1]))
    mmax = int(sys.argv[2])
    Ns = [int(x) for x in sys.argv[3].split(',')]
    ss = [int(x) for x in sys.argv[4].split(',')]
    for N in Ns:
        for s in ss:
            t0 = time.time()
            M = N * s
            new = [d for d in core.divisors(M) if N % d != 0]
            if not new:                                   # s = 1
                continue
            Tall, sl = big_table(M, new)
            assert Tall.shape == (M, M - N)
            tot = lf = none = 0
            mt = 1
            ex = []
            top = 0
            for m in range(1, mmax + 1):
                if m > 1 and comb(N + m - 2, m - 1) * (M - N) * m > budget:
                    break
                a, b, c, d, e = run(N, s, m, Tall, sl)
                tot += a; lf += b; mt = max(mt, c); none += d; ex += e
                top = m
            kind = ('s-even-not-2 ' if (s % 2 == 0 and s != 2) else 's-odd-or-2 ') + ('N-pnq' if is_pnq(N) else 'N-not-pnq')
            print('N = %d s = %d sizes-up-to %d multisets %d all-low-fails %d most-lifts-tried %d WITHOUT-lift %d %s '
                  'new-divisors %d kind %s (%.0f s)'
                  % (N, s, top, tot, lf, mt, none, ex if none else '', len(new), kind, time.time() - t0), flush=True)
