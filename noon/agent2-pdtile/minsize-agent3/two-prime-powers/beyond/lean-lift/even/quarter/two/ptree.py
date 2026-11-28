#!/usr/bin/env python3
"""Exact maxima for ONE prime p (moduli p^a), by all trees of class sizes.

A multiset of m elements on Z_(p^a) is, for the events "bad at p^i", a tree: the root is the whole multiset, the
children of a class at depth j are its occupied subclasses at depth j+1 (1 to p of them), the leaves at depth a carry
their numbers of elements.  A signing is bad at p^i (i >= 1) iff in every group at level i the p subclass sums are
equal (missing subclasses have sum 0), and bad at 1 iff the total is 0.

For every tree of depth a (unary steps allowed, so every smaller depth is included) the program computes, with
integers, the number of signings that are
    bad somewhere (level 0 included)                      -> T_p(m)  = largest share
    bad at some level i >= 1 and not at level 0           -> U_p(m)  = largest share
and prints the maxima over all trees.  Depth a = floor((m-1)/(p-1)) suffices (contraction; result.md, section 1).

usage: ptree.py p mmin mmax [amax]
"""
import sys
from math import comb
from fractions import Fraction
from itertools import combinations_with_replacement, product
from functools import lru_cache


def partitions(r, k, mx=None):
    """partitions of r into at most k parts, nonincreasing"""
    if mx is None:
        mx = r
    if r == 0:
        yield ()
        return
    if k == 0:
        return
    for first in range(min(r, mx), 0, -1):
        for rest in partitions(r - first, k - 1, first):
            yield (first,) + rest


def make(p):
    @lru_cache(maxsize=None)
    def dists(r, a):
        """set of distributions of subtrees with r >= 1 elements and depth a.
        a distribution is a frozenset of ((s, mask), count); bit k-1 of mask: all groups at relative level k flat"""
        if a == 0:
            return (frozenset(((s, 0), comb(r, (r + s) // 2)) for s in range(-r, r + 1, 2)),)
        out = set()
        for part in partitions(r, p):
            k = len(part)
            # group equal sizes to avoid repeating the same multiset of subtrees
            sizes = sorted(set(part), reverse=True)
            choices = []
            for sz in sizes:
                mult = part.count(sz)
                choices.append(list(combinations_with_replacement(dists(sz, a - 1), mult)))
            for combo in product(*choices):
                kids = [d for grp in combo for d in grp]
                # combine
                cur = {(0, (1 << (a - 1)) - 1, None, True): 1}   # (sum, and-mask, common value, all equal so far)
                for d in kids:
                    nxt = {}
                    for (s, mk, cv, eq), cnt in cur.items():
                        for (s2, mk2), cnt2 in d:
                            if cv is None:
                                ncv, neq = s2, True
                            else:
                                ncv, neq = cv, (eq and s2 == cv)
                            key = (s + s2, mk & mk2, ncv, neq)
                            nxt[key] = nxt.get(key, 0) + cnt * cnt2
                    cur = nxt
                res = {}
                for (s, mk, cv, eq), cnt in cur.items():
                    flat = eq and (k == p or cv == 0)
                    key = (s, (mk << 1) | (1 if flat else 0))
                    res[key] = res.get(key, 0) + cnt
                out.add(frozenset(res.items()))
        return tuple(out)
    return dists


def main():
    p = int(sys.argv[1]); mmin = int(sys.argv[2]); mmax = int(sys.argv[3])
    dists = make(p)
    for m in range(mmin, mmax + 1):
        a = (m - 1) // (p - 1)
        if len(sys.argv) > 4:
            a = min(a, int(sys.argv[4]))
        best_T = best_U = 0
        per_level = {}
        ds = dists(m, a)
        for d in ds:
            bad = sum(cnt for (s, mk), cnt in d if s == 0 or mk)
            new = sum(cnt for (s, mk), cnt in d if s != 0 and mk)
            best_T = max(best_T, bad); best_U = max(best_U, new)
        print("p=%d m=%d depth=%d distributions=%d  T_p(m)=%s  U_p(m)=%s  level0=%s" % (
            p, m, a, len(ds), Fraction(best_T, 2 ** m), Fraction(best_U, 2 ** m),
            Fraction(comb(m, m // 2), 2 ** m) if m % 2 == 0 else 0), flush=True)


if __name__ == '__main__':
    main()
