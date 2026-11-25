"""Blind step, items 1 and 2: enumerate every coin sequence for small orders.
usage: ref_exact.py MAXORDER
"""
import sys, itertools
from fractions import Fraction
import numpy as np
from ref_core import *

MAXN = int(sys.argv[1]) if len(sys.argv) > 1 else 4


def all_tilings(n):
    """independent brute force: all perfect matchings of the vertex graph, as bytes of block values."""
    # vertices: V[i][j] i in 0..n, j in 0..n-1 ; H[i][j] i in 0..n-1, j in 0..n
    def Vv(i, j): return i * n + j
    nV = (n + 1) * n
    def Hv(i, j): return nV + i * (n + 1) + j
    nvert = 2 * nV
    inc = [[] for _ in range(nvert)]
    for i in range(n):
        for j in range(n):
            blk = i * n + j
            for bit, (u, w) in ((1, (Hv(i, j), Vv(i, j))), (2, (Vv(i, j), Hv(i, j + 1))),
                                (4, (Hv(i, j), Vv(i + 1, j))), (8, (Vv(i + 1, j), Hv(i, j + 1)))):
                inc[u].append((w, blk, bit)); inc[w].append((u, blk, bit))
    out = set()
    cov = [False] * nvert
    val = [0] * (n * n)

    def rec(start):
        u = start
        while u < nvert and cov[u]:
            u += 1
        if u == nvert:
            out.add(bytes(val)); return
        cov[u] = True
        for w, blk, bit in inc[u]:
            if not cov[w]:
                cov[w] = True; val[blk] |= bit
                rec(u + 1)
                cov[w] = False; val[blk] &= ~bit
        cov[u] = False
    rec(0)
    return out


def enumerate_alg(rule, maxn, cap=3_000_000):
    """rule: 'worded' (simultaneous), 'scan' (reading order, earlier fills count), 'pre' (fill blocks empty
    before step 2). Returns list per order of dict config-bytes -> [n sequences, probability]."""
    res = []
    cur = {bytes([0]) + b"": None}
    # order 1: step 4 on a single empty block
    cur = {bytes([9]): [1, Fraction(1, 2)], bytes([6]): [1, Fraction(1, 2)]}
    res.append(cur)
    ambiguous = 0
    for n in range(1, maxn):
        nxt = {}
        for key, (ns, p) in cur.items():
            old = np.frombuffer(key, np.uint8).reshape(n, n)
            new = shift(old)
            pre_empty = new == 0
            after_del = LUT_DEL[new]
            ambiguous += int((POP[after_del] > 1).sum())
            new = LUT_SWAP[after_del]
            if rule == "worded":
                fill = candidates(new)
            elif rule == "scan":
                fill = sequential_fill_set(new)
            else:
                fill = pre_empty
            idx = np.flatnonzero(fill.ravel())
            f = len(idx)
            pp = p / (1 << f)
            flat = new.ravel().copy()
            for choice in itertools.product((9, 6), repeat=f):
                flat[idx] = choice
                k = flat.tobytes()
                e = nxt.get(k)
                if e is None:
                    nxt[k] = [ns, pp]
                else:
                    e[0] += ns; e[1] += pp
            if len(nxt) > cap:
                print("   cap reached, stopping", flush=True); return res, ambiguous
        cur = nxt
        res.append(cur)
    return res, ambiguous


def report(rule, maxn):
    print(f"== rule: {rule}")
    res, amb = enumerate_alg(rule, maxn)
    for n, cur in enumerate(res, 1):
        T = TIL[n]
        nseq = sum(e[0] for e in cur.values())
        ncfg = len(cur)
        ntil = sum(1 for k in cur if is_tiling(np.frombuffer(k, np.uint8).reshape(n, n)))
        same = set(cur) == T
        ps = set(e[1] for e in cur.values())
        tot = sum(e[1] for e in cur.values())
        multi = sum(1 for e in cur.values() if e[0] > 1)
        maxseq = max(e[0] for e in cur.values())
        # toss counts
        print(f" order {n}: sequences {nseq}, distinct configurations {ncfg}, of which tilings {ntil}; "
              f"true tilings {len(T)} (2^{n*(n+1)//2}={2**(n*(n+1)//2)}); set equal to true tilings: {same}; "
              f"total prob {tot}; distinct probabilities {len(ps)} (min {min(ps)}, max {max(ps)}); "
              f"configs reached by >1 sequence: {multi}, max sequences for one config {maxseq}")
    print(f"   blocks holding 2+ dimers after step 2 (wording of step 3 ambiguous there): {amb}")
    return res


TIL = {n: all_tilings(n) for n in range(1, MAXN + 1)}
print("brute-force numbers of tilings:", {n: len(t) for n, t in TIL.items()})
for rule in ("worded", "scan", "pre"):
    res = report(rule, MAXN)
    if rule == "pre":
        # toss statistics for the corrected algorithm: distribution of deletions m when going n -> n+1
        for n, cur in enumerate(res, 1):
            ms = {}
            for k in cur:
                old = np.frombuffer(k, np.uint8).reshape(n, n)
                new = shift(old)
                m = int(((new == 9) | (new == 6)).sum())
                ms[m] = ms.get(m, 0) + 1
            em = Fraction(sum(m * c for m, c in ms.items()), len(cur))
            print(f"   order {n}: deletions when shuffled to order {n+1}: histogram {dict(sorted(ms.items()))}, mean {em} = {float(em):.5f}")
        # check rules 'scan' and 'pre' pick the same blocks on every true tiling
        bad = 0; tot = 0
        for n in range(1, MAXN + 1):
            for k in TIL[n]:
                old = np.frombuffer(k, np.uint8).reshape(n, n)
                new = shift(old); pre = new == 0; new = LUT_DELSWAP[new]
                tot += 1
                if not (sequential_fill_set(new) == pre).all():
                    bad += 1
        print(f"   scan rule vs empty-before-step-2 rule on all true tilings of orders 1..{MAXN}: {tot} cases, {bad} differ")
