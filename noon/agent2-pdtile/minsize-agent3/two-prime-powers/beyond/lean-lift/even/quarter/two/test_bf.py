#!/usr/bin/env python3
"""Test of the tables BF_p(G, m) of lo_union2.py against a plain enumeration of ALL configurations.

A configuration: a multiset of cells, each cell a partition of its number of elements (>= 2) into at most p classes
(a cell with p classes is p-full).  Its value is the product of the cell values of Lemma 4 (function cell_value of
test_cells.py, written independently of the tables).  For every p, m and G:

    max over the configurations with m elements, at least G cells, at least one p-full cell   <=   BF_p(G, m),

and the program reports in how many cases the two are equal.

usage: test_bf.py MMAX
"""
import sys
from fractions import Fraction
import lo_union2 as L
import test_cells as TC


def partitions(r, k, mx=None, mn=1):
    """partitions of r into at most k parts, each >= mn, nonincreasing"""
    if mx is None:
        mx = r
    if r == 0:
        yield ()
        return
    if k == 0:
        return
    for first in range(min(r, mx), mn - 1, -1):
        for rest in partitions(r - first, k - 1, first, mn):
            yield (first,) + rest


def main():
    Mmax = int(sys.argv[1])
    ctx = TC.Ctx(Mmax)
    ncfg = 0
    cases = equal = 0
    for p in L.primes_upto(Mmax):
        # best value of one cell with R elements: full / not full
        full = {}
        notfull = {}
        for R in range(2, Mmax + 1):
            bf_ = Fraction(0); bn = Fraction(0)
            for part in partitions(R, p):
                sizes = list(part) + [0] * (p - len(part))
                v = TC.cell_value(ctx, p, sizes)
                ncfg += 1
                if len(part) == p:
                    bf_ = max(bf_, v)
                else:
                    bn = max(bn, v)
            full[R] = bf_; notfull[R] = bn
        for m in range(p, Mmax + 1):
            # all multisets of cell sizes: partitions of m into parts >= 2
            best = {}
            for cells in partitions(m, m // 2, None, 2):
                G = len(cells)
                # at least one full cell: choose which cells are counted as full; the best choice
                val_any = Fraction(1)
                for R in cells:
                    val_any *= max(full[R], notfull[R])
                # force one full cell
                b = Fraction(0)
                for i, R in enumerate(cells):
                    if full[R] == 0:
                        continue
                    v = full[R]
                    for k, R2 in enumerate(cells):
                        if k != i:
                            v *= max(full[R2], notfull[R2])
                    b = max(b, v)
                best[G] = max(best.get(G, Fraction(0)), b)
            run = Fraction(0)
            for G in range(m // 2, 0, -1):
                run = max(run, best.get(G, Fraction(0)))
                dp = ctx.BF(p, G, m)
                assert run <= dp, ("BF", p, m, G, run, dp)
                cases += 1
                if run == dp:
                    equal += 1
    print("test_bf: m <= %d, %d cell shapes; %d cases (p, m, G): enumeration <= BF_p(G, m) in all, equal in %d. NO FAILURE"
          % (Mmax, ncfg, cases, equal))


if __name__ == '__main__':
    main()
