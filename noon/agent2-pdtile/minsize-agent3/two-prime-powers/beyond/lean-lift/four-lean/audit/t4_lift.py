"""exists_lift_two_all: for N and every multiset w of m elements of Z_N that contains 0 (every multiset has such a
translate, and a lift of the translate is a translate of a lift), search for a multiset w' on Z_{2N} with
reduce w' = w whose mask is divisible by no Phi_d with d | 2N, d not dividing N.

A w' with reduce w' = w is exactly a choice, for each element x of w (copies counted separately), of one of the two
residues y in [0, 2N) with y mod N = x, namely x ("low") or x + N ("high").  The mask of w' is sum X^y; "Phi_d divides
it" is decided from the remainders of X^y modulo Phi_d (integer vectors), for every d | 2N with d not dividing N.
Adding N to every element of w' (a translation of Z_{2N}) exchanges low and high and keeps the divisors, so the first
element is kept low; the choices are tried by increasing number of high lifts, all 2^(m-1) before a multiset is
declared to have no lift.
usage: t4_lift.py N mmin mmax"""
import os
import sys
import time
from itertools import combinations_with_replacement, islice, chain
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import core
from t3_a1 import big_table, signings


def run(N, m, batch_cells=24_000_000):
    new = [d for d in core.divisors(2 * N) if N % d != 0]
    Tall, sl = big_table(2 * N, new)
    assert Tall.shape == (2 * N, N)
    B = max(1000, batch_cells // max(N, 1))
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
        for idx, s in enumerate(signings(m)):            # s[k] = +1: low, -1: high
            R = np.zeros((rest.shape[0], N), dtype=np.int16)
            for k in range(m):
                R += Tall[rest[:, k] + (N if s[k] == -1 else 0)]
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
    return total, low_fail, maxtried, none, examples, len(new)


if __name__ == '__main__':
    N, mmin, mmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    for m in range(mmin, mmax + 1):
        t0 = time.time()
        total, lf, mt, none, ex, nd = run(N, m)
        print('N = %d m = %d multisets %d all-low-fails %d most-lifts-tried %d WITHOUT-lift %d %s new-divisors %d (%.0f s)'
              % (N, m, total, lf, mt, none, ex if none else '', nd, time.time() - t0), flush=True)
