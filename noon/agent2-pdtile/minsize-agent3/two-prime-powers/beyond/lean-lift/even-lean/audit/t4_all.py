"""A' (exists_not_bad3) and B (exists_not_badAt_of_three_le) by brute force: every multiset of m elements of Z_n
(exponents 0..n-1) has a signing that is 3-bad at no d | n (A', n prime to 3), resp. bad at no d | n (B).

A signing and its negative are bad at the same d, so the first sign is fixed to + (2^(m-1) signings).  Signings are
tried in a fixed order until one works; a multiset for which none works is a counterexample and is printed.
By default only multisets that contain 0 are listed (adding c to every exponent multiplies the signed mask by X^c
modulo X^n - 1, which changes neither "Phi_d divides", d | n, nor "3-bad at d"); with ALL every multiset is listed,
to test that reduction as well.

usage: t4_all.py MODE N MMIN MMAX [ALL]      MODE = A (3-bad, needs 3 not dividing N) or B (bad over Z)
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import time
from itertools import combinations_with_replacement, islice
from math import comb
import numpy as np
from ecore import divisors, rem_table, phi


def big_table(n):
    """(n, n) table: row x is the concatenation over d | n of the remainder of X^x modulo Phi_d; and the blocks"""
    cols = []
    blocks = []
    off = 0
    for d in divisors(n):
        t = rem_table(d)
        cols.append(t[[x % d for x in range(n)]])
        blocks.append((d, off, off + t.shape[1]))
        off += t.shape[1]
    T = np.concatenate(cols, axis=1)
    assert T.shape == (n, n)
    assert np.abs(T).max() < 100
    return T.astype(np.int16), blocks


def sign_order(m):
    """signings with the first sign +, as lists of +1/-1: fewest minus signs first"""
    out = []
    for s in sorted(range(1 << (m - 1)), key=lambda s: (bin(s).count('1'), s)):
        out.append([1] + [-1 if (s >> k) & 1 else 1 for k in range(m - 1)])
    return out


def good_mask(R, blocks, mode):
    """R: (B, n) remainders; True where the signing is bad (resp. 3-bad) at no d"""
    if mode == 'A':
        R = R % 3
    ok = np.ones(R.shape[0], dtype=bool)
    for (d, a, b) in blocks:
        ok &= np.any(R[:, a:b] != 0, axis=1)
    return ok


def run(mode, n, m, all_multisets, T, blocks, t0):
    if m == 0:
        # one signing, the mask is 0
        R = np.zeros((1, n), dtype=np.int16)
        ok = good_mask(R, blocks, mode)
        return 1, int((~ok).sum()), 0, 0, [()] if not ok[0] else []
    order = sign_order(m)
    if all_multisets:
        it = combinations_with_replacement(range(n), m)
        total = comb(n + m - 1, m)
    else:
        it = ((0,) + c for c in combinations_with_replacement(range(n), m - 1))
        total = comb(n + m - 2, m - 1)
    chunk = 200000
    n_all = 0
    n_plus_fail = 0
    max_tried = 0
    failures = []
    while True:
        batch = list(islice(it, chunk))
        if not batch:
            break
        E = np.array(batch, dtype=np.int64)
        n_all += len(batch)
        rem = np.arange(len(batch))
        for si, sg in enumerate(order):
            if rem.size == 0:
                break
            R = np.zeros((rem.size, n), dtype=np.int16)
            for k in range(m):
                if sg[k] == 1:
                    R += T[E[rem, k]]
                else:
                    R -= T[E[rem, k]]
            ok = good_mask(R, blocks, mode)
            if si == 0:
                n_plus_fail += int((~ok).sum())
            rem = rem[~ok]
            if rem.size:
                max_tried = max(max_tried, si + 2)
        if rem.size:
            max_tried = min(max_tried, len(order))
            for r in rem:
                failures.append(tuple(int(x) for x in E[r]))
        if time.time() - t0 > 270:
            return n_all, len(failures), n_plus_fail, max_tried, failures, total
    assert n_all == total
    return n_all, len(failures), n_plus_fail, max_tried, failures, total


def main():
    mode, n, mmin, mmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    all_multisets = len(sys.argv) > 5 and sys.argv[5] == 'ALL'
    if mode == 'A':
        assert n % 3 != 0
    T, blocks = big_table(n)
    t0 = time.time()
    for m in range(mmin, mmax + 1):
        res = run(mode, n, m, all_multisets, T, blocks, t0)
        n_all, n_fail, n_plus_fail, max_tried, failures = res[:5]
        total = res[5] if len(res) > 5 else n_all
        note = "" if n_all == total else f" INCOMPLETE ({n_all} of {total}, stopped by the clock)"
        print(f"{mode} n={n} m={m} {'all multisets' if all_multisets else 'multisets containing 0'}: {n_all} multisets, "
              f"without a {'3-good' if mode == 'A' else 'good'} signing: {n_fail}; 'all +' fails for {n_plus_fail}; "
              f"most signings tried {max_tried}{note} ({time.time() - t0:.0f} s)")
        if failures:
            print("   WITHOUT:", failures[:40], "..." if len(failures) > 40 else "")
        sys.stdout.flush()
        if n_all != total:
            break


main()
