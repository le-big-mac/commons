"""Referee: EVERY multiset of M elements on Z_(3^A * Q), Q a prime >= 5, up to the symmetries that leave all the
events "bad at d" unchanged (automorphisms of the ternary tree; permutations of the classes modulo Q), all signings,
by the definition (remainders modulo the cyclotomic polynomials).

A multiset is a table: rows = occupied leaves of a shape of the 3-tree (ref_tree3.all_shapes), columns = classes
modulo Q, entries = multiplicities.  Columns are generated in lexicographically non-increasing order (one table per
orbit of the column permutations); symmetric shapes give some tables more than once, which only repeats work.

usage: ref_two.py A Q M
"""
import sys
from fractions import Fraction as Fr
import numpy as np
from cyc import rem_matrix, divisors
from ref_tree3 import all_shapes
from ref_odd import BB, BETA_EXACT

A, Q, M = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
P3 = 3 ** A
n = P3 * Q
divs = divisors(n)
big = np.hstack([rem_matrix(n, d) for d in divs]).astype(np.int32)
cuts = np.cumsum([0] + [rem_matrix(n, d).shape[1] for d in divs])
blocks = [(int(cuts[i]), int(cuts[i + 1])) for i in range(len(divs))]
idx = np.arange(2 ** (M - 1), dtype=np.int64)[:, None]
E = (1 - 2 * ((idx >> np.arange(M, dtype=np.int64)[None, :]) & 1)).astype(np.int32)     # last sign always +
assert (E[:, M - 1] == 1).all()
crt = {(x % P3, x % Q): x for x in range(n)}


def leaves(s, a, base=0, step=1):
    """(residue modulo 3^a, size) of the occupied leaves of the shape s"""
    if a == 0:
        return [(base, s)] if s else []
    out = []
    for t in range(3):
        out += leaves(s[t], a - 1, base + t * step, step * 3)
    return out


def rows_gen(k, tied, q):
    """compositions (x_0..x_(q-1)) of k with x_c >= x_(c+1) wherever columns c, c+1 are still tied"""
    def rec(c, left, prev, acc):
        if c == q:
            if left == 0:
                yield tuple(acc)
            return
        hi = left if (c == 0 or not tied[c - 1]) else min(left, prev)
        for x in range(hi, -1, -1):
            acc.append(x)
            yield from rec(c + 1, left - x, x, acc)
            acc.pop()
    yield from rec(0, k, 0, [])


def tables(sizes, q):
    def rec(i, tied, acc):
        if i == len(sizes):
            yield acc[:]
            return
        for row in rows_gen(sizes[i], tied, q):
            nt = tuple(tied[c] and row[c] == row[c + 1] for c in range(q - 1))
            acc.append(row)
            yield from rec(i + 1, nt, acc)
            acc.pop()
    yield from rec(0, tuple([True] * (q - 1)), [])


best = 0; ex = None; count = 0; hist = {}; nshapes = 0; live_count = 0
for s in all_shapes(A, M):
    lv = leaves(s, A)
    nshapes += 1
    for tab in tables([k for _, k in lv], Q):
        B = []
        for (r3, _), row in zip(lv, tab):
            for c, x in enumerate(row):
                B += [crt[(r3, c)]] * x
        R = E @ big[B]
        bad = np.zeros(R.shape[0], dtype=bool)
        for u, v in blocks:
            bad |= ~R[:, u:v].any(axis=1)
        c = int(bad.sum()); count += 1
        hist[c] = hist.get(c, 0) + 1
        if len(set(b % Q for b in B)) == Q:
            live_count += 1
        if c > best:
            best = c; ex = sorted(B)
sh = Fr(best, 2 ** (M - 1))
cap = BB.get(M); claim = BETA_EXACT.get(M)
ok = (cap is None or sh <= cap) and (claim is None or sh <= claim) and (M < 3 or sh <= Fr(3, 8))
top = sorted(hist.items(), reverse=True)[:3]
print(f"Z_{n} = Z_(3^{A} * {Q}), m = {M}: {nshapes} shapes of the 3-tree, {count} tables ({live_count} with all {Q} classes modulo {Q} occupied), all signings: "
      f"largest bad share {sh} at {ex}; b(m) = {cap}; claimed exact beta = {claim}; within every claim: {ok}; largest counts of {2 ** (M - 1)}: {top}", flush=True)
assert ok
