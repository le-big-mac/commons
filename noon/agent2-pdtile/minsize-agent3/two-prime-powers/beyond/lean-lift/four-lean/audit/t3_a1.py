"""A1 (exists_not_badAt) and exists_signs_odd: for n and every multiset of m elements of Z_n that contains 0 (every
multiset has such a translate, with the same divisors for every signing), search the signings for one whose signed mask
is divisible by no Phi_d, d | n.  Exact: remainders modulo Phi_d as integer vectors (core.xtab).  A signing and its
negative are bad at the same d, so the first sign is fixed to +; signings are tried by increasing number of minus signs,
all 2^(m-1) of them before a multiset is declared to have none.
For even n (not allowed by the statements) the same search is a control: there the statement is false.
"most-signings-tried" is the largest number of signings tried before a good one was found.
usage: t3_a1.py n mmin mmax"""
import os
import sys
import time
from itertools import combinations, combinations_with_replacement, islice, chain
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import core


def big_table(n, ds):
    cols = []
    sl = {}
    a = 0
    for d in ds:
        T = core.xtab(d)[np.arange(n) % d]
        cols.append(T)
        sl[d] = (a, a + T.shape[1])
        a += T.shape[1]
    Tall = np.concatenate(cols, axis=1)
    assert np.abs(Tall).max() * 64 < 2 ** 15
    return Tall.astype(np.int16), sl


def bad_any(E, s, Tall, sl):
    """E: rows of residues; s: one signing (+1/-1 per position); True where some Phi_d divides the signed mask"""
    R = np.zeros((E.shape[0], Tall.shape[1]), dtype=np.int16)
    for k in range(E.shape[1]):
        if s[k] == 1:
            R += Tall[E[:, k]]
        else:
            R -= Tall[E[:, k]]
    out = np.zeros(E.shape[0], dtype=bool)
    for d, (a, b) in sl.items():
        out |= ~R[:, a:b].any(axis=1)
    return out


def signings(m):
    """first sign +, by increasing number of minus signs"""
    for k in range(0, m):
        for minus in combinations(range(1, m), k):
            s = [1] * m
            for j in minus:
                s[j] = -1
            yield s


def run(n, m, batch_cells=24_000_000):
    ds = core.divisors(n)
    Tall, sl = big_table(n, ds)
    B = max(1000, batch_cells // max(n, 1))
    it = combinations_with_replacement(range(n), m - 1)
    total = allplus_fail = none = 0
    maxtried = 1
    examples = []
    first_fail = None
    while True:
        flat = np.fromiter(chain.from_iterable(islice(it, B)), dtype=np.int32)
        if flat.size == 0 and m > 1:
            break
        E = np.zeros((flat.size // (m - 1) if m > 1 else 1, m), dtype=np.int32)
        if m > 1:
            E[:, 1:] = flat.reshape(-1, m - 1)
        total += E.shape[0]
        rest = E
        for idx, s in enumerate(signings(m)):
            b = bad_any(rest, s, Tall, sl)
            if idx == 0:
                allplus_fail += int(b.sum())
                if first_fail is None and b.any():
                    first_fail = rest[np.argmax(b)].tolist()
            if (~b).any():
                maxtried = max(maxtried, idx + 1)      # the signing number idx + 1 was needed by some multiset
            rest = rest[b]
            if rest.shape[0] == 0:
                break
        else:
            none += rest.shape[0]
            examples += rest[:3].tolist()
        if m == 1:
            break
    assert total == comb(n + m - 2, m - 1), (total, n, m)
    return total, allplus_fail, maxtried, none, examples, first_fail


if __name__ == '__main__':
    n, mmin, mmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    for m in range(mmin, mmax + 1):
        t0 = time.time()
        total, apf, mt, none, ex, ff = run(n, m)
        print('n = %d m = %d multisets %d all-plus-fails %d most-signings-tried %d WITHOUT-good-signing %d %s first-all-plus-failure %s (%.0f s)'
              % (n, m, total, apf, mt, none, ex if none else '', ff, time.time() - t0), flush=True)
