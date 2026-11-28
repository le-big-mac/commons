#!/usr/bin/env python3
"""Referee's own exact computation of U_p(m) and T_p(m) (result.md, section 4), written from the text's definitions.

A multiset on Z_(p^a) is a tree of nested classes.  For a subtree with r elements and `a` remaining levels the
distribution is: for each (s, L), s = sum of the signs, L = bitmask of the relative levels 1..a inside the subtree at
which every group is flat (bit i-1 for relative level i), the number of signings.  A group (class with its p
subclasses) is flat iff the p subclass sums are equal, an empty subclass having sum 0.

usage: r_tree.py p mmin mmax [depthcap]
"""
import sys, time
from math import comb
from fractions import Fraction


def build(p):
    memo = {}

    def D(r, a):
        key = (r, a)
        if key in memo:
            return memo[key]
        if a == 0:
            d = tuple(sorted(((s, 0), comb(r, (r + s) // 2)) for s in range(-r, r + 1, 2)))
            memo[key] = (d,)
            return memo[key]
        allones = (1 << (a - 1)) - 1
        found = set()

        def rec(left, kleft, maxsize, minidx, state, k):
            if left == 0:
                res = {}
                for (s, mk, cv), cnt in state.items():
                    flat = (cv != 'N') and (k == p or cv == 0)
                    k2 = (s, (mk << 1) | (1 if flat else 0))
                    res[k2] = res.get(k2, 0) + cnt
                found.add(tuple(sorted(res.items())))
                return
            if kleft == 0:
                return
            for sz in range(min(left, maxsize), 0, -1):
                if left - sz > (kleft - 1) * sz:
                    break
                ds = D(sz, a - 1)
                start = minidx if sz == maxsize else 0
                for idx in range(start, len(ds)):
                    d = ds[idx]
                    new = {}
                    for (s, mk, cv), cnt in state.items():
                        for (s2, L2), c2 in d:
                            if cv is None:
                                ncv = s2
                            elif cv == 'N' or cv != s2:
                                ncv = 'N'
                            else:
                                ncv = cv
                            kk = (s + s2, mk & L2, ncv)
                            new[kk] = new.get(kk, 0) + cnt * c2
                    rec(left - sz, kleft - 1, sz, idx, new, k + 1)

        rec(r, p, r, 0, {(0, allones, None): 1}, 0)
        memo[key] = tuple(found)
        return memo[key]

    return D


def main():
    p = int(sys.argv[1]); mmin = int(sys.argv[2]); mmax = int(sys.argv[3])
    cap = int(sys.argv[4]) if len(sys.argv) > 4 else None
    D = build(p)
    t0 = time.time()
    for m in range(mmin, mmax + 1):
        a = (m - 1) // (p - 1)
        if cap is not None:
            a = min(a, cap)
        bT = bU = 0
        ds = D(m, a)
        for d in ds:
            assert sum(c for _, c in d) == 2 ** m
            T = sum(c for (s, L), c in d if s == 0 or L)
            U = sum(c for (s, L), c in d if s != 0 and L)
            bT = max(bT, T); bU = max(bU, U)
        print("p=%d m=%d depth=%d ndist=%d T=%s U=%s  (%.0fs)" % (p, m, a, len(ds), Fraction(bT, 2 ** m), Fraction(bU, 2 ** m), time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
