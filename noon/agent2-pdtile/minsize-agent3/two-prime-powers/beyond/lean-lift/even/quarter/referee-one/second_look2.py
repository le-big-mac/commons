"""Referee, second look: the text now cites my run "73/256 is exactly the largest on Z_45" (ref_two.py, tables up to
symmetry).  Here the table enumeration is compared with the plain one (every multiset containing 0) on cases where
both are possible: the SET of all numbers of bad signings that occur must be the same in both.

usage: second_look2.py A Q M   (modulus 3^A * Q)
"""
import sys
import numpy as np
from cyc import rem_matrix, divisors
from ref_tree3 import all_shapes

A, Q, M = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
P3 = 3 ** A; n = P3 * Q
divs = divisors(n)
big = np.hstack([rem_matrix(n, d) for d in divs]).astype(np.int32)
cuts = np.cumsum([0] + [rem_matrix(n, d).shape[1] for d in divs])
blocks = [(int(cuts[i]), int(cuts[i + 1])) for i in range(len(divs))]
idx = np.arange(2 ** (M - 1), dtype=np.int64)[:, None]
E = (1 - 2 * ((idx >> np.arange(M, dtype=np.int64)[None, :]) & 1)).astype(np.int32)
crt = {(x % P3, x % Q): x for x in range(n)}


def nbad(B):
    R = E @ big[B]
    bad = np.zeros(R.shape[0], dtype=bool)
    for u, v in blocks:
        bad |= ~R[:, u:v].any(axis=1)
    return int(bad.sum())


# ---- tables (same generation as ref_two.py, written again)
def leaves(s, a, base=0, step=1):
    if a == 0:
        return [(base, s)] if s else []
    out = []
    for t in range(3):
        out += leaves(s[t], a - 1, base + t * step, step * 3)
    return out


def rows(k, tied):
    def rec(c, left, prev, acc):
        if c == Q:
            if left == 0:
                yield tuple(acc)
            return
        hi = left if (c == 0 or not tied[c - 1]) else min(left, prev)
        for x in range(hi, -1, -1):
            yield from rec(c + 1, left - x, x, acc + [x])
    yield from rec(0, k, 0, [])


def tables(sizes):
    def rec(i, tied, acc):
        if i == len(sizes):
            yield acc
            return
        for row in rows(sizes[i], tied):
            yield from rec(i + 1, tuple(tied[c] and row[c] == row[c + 1] for c in range(Q - 1)), acc + [row])
    yield from rec(0, tuple([True] * (Q - 1)), [])


set_tab = {}; ntab = 0
for s in all_shapes(A, M):
    lv = leaves(s, A)
    for tab in tables([k for _, k in lv]):
        B = [crt[(r3, c)] for (r3, _), row in zip(lv, tab) for c, x in enumerate(row) for _ in range(x)]
        c = nbad(B); ntab += 1
        set_tab[c] = set_tab.get(c, 0) + 1

# ---- plain: every nondecreasing (0, b_2, ..., b_M)
set_plain = {}; nplain = 0


def rec(k, lo, B):
    global nplain
    if k == M:
        c = nbad(B); nplain += 1
        set_plain[c] = set_plain.get(c, 0) + 1
        return
    for b in range(lo, n):
        rec(k + 1, b, B + [b])


rec(1, 0, [0])
same = set(set_tab) == set(set_plain)
print(f"Z_{n}, m = {M}: {ntab} tables, {nplain} multisets with 0; numbers of bad signings (of {2 ** (M - 1)}) that occur: "
      f"tables {sorted(set_tab)}; plain {sorted(set_plain)}; the same set: {same}; largest {max(set_tab)} and {max(set_plain)}", flush=True)
assert same
