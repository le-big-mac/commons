"""Test the three statements of Pnq/Upset.lean, read literally, against exhaustive computation in Z_M.

usage: statement_test.py M [--plain-rows N] [--lattice-cands N] [--only "d1,d2,..."] [--smax S] [--no-plain]

For every D accepted by IsUpSet M (literal translation, upset_lib.is_upset_lean) and a size bound S:

  L(D, S) = { w : Z_M -> N, sum w <= S, Phi_d | maskW w for every d in D }
  R(D, S) = { w : Z_M -> N, sum w <= S, w = sum over c in corners M D of g_c, g_c >= 0 periodic under adding c }

(a) structure_iff for every multiset of size <= S   <=>   L(D, S) = R(D, S) as sets;
(b) lower_bound for every multiset of size <= S     <=>   every w in L(D, S) with Phi_c not dividing maskW w
    for every corner c has   sum w >= B,  B = sum over the corners of M / c.   (Complete when S >= B - 1.)
(c) least_size: no w with 0 < sum w < B has "for all d | M, d != 1: Phi_d | maskW w <-> d in D"  (complete
    when S >= B - 1), and some w with sum w = B has it (found by the search when S >= B; in every case the
    multiset "sum over the corners c of the indicator of the multiples of c" is tested by long division).

Two ways to get L(D, S):
  plain   : every multiset of size <= S, divisibility by the linear remainder map (exact integers);
  lattice : the first r = M - sum_{d in D} phi(d) coordinates determine w (see upset_lib.lattice_T); every
            head of sum <= S is tried.  Where both are run, they are compared.
R(D, S) is generated from the indicators of the classes of x ~ x + c.
"""
import argparse
import sys
import time
from math import comb

import numpy as np

from upset_lib import *

ap = argparse.ArgumentParser()
ap.add_argument('M', type=int)
ap.add_argument('--plain-rows', type=float, default=3.0e6)
ap.add_argument('--lattice-cands', type=float, default=2.0e7)
ap.add_argument('--only', type=str, default=None, help='comma-separated D (use "empty" for the empty set)')
ap.add_argument('--smax', type=int, default=None)
ap.add_argument('--no-plain', action='store_true')
ap.add_argument('--chunk', type=float, default=2.0e6)
args = ap.parse_args()

M = args.M
dv = nat_divisors(M)
ups = all_upsets(M)
if args.only is not None:
    want = tuple(sorted(int(x) for x in args.only.split(',') if x not in ('', 'empty')))
    assert want in ups, 'not an up-set by the Lean definition'
    ups = [want]
smax_default = M + 2 if args.smax is None else args.smax

t0 = time.time()
print('# M = %d, divisors %s, %d up-sets by the Lean definition' % (M, dv, len(all_upsets(M))), flush=True)

# plain enumeration, shared by all D
S_A = -1
if not args.no_plain:
    S_A = 0
    while S_A + 1 <= smax_default and comb(M + S_A + 1, M) <= args.plain_rows:
        S_A += 1
    W = enum_le(M, S_A)
    flagsW = div_flags(W, M, dv)
    sizeW = W.sum(axis=1, dtype=np.int64)
    print('# plain: every multiset of size <= %d: %d multisets  (%.0f s)' % (S_A, len(W), time.time() - t0), flush=True)


def witness(M, cs):
    """sum over the corners c of the indicator of the multiples of c (a candidate for the least size)"""
    return [sum(1 for c in cs if a % c == 0) for a in range(M)]


def analyse(D, cs, B, L, fl, S, label):
    """checks (a), (b), (c) on L = L(D, S) with fl the divisibility flags of its rows for every divisor"""
    size = L.sum(axis=1, dtype=np.int64)
    for d in D:
        assert fl[d].all()
    # (a)
    R = sums_of_periodic(M, cs, S)
    a_ok = same_rows(L, R)
    # (b)
    hc = np.ones(len(L), dtype=bool)
    for c in cs:
        hc &= ~fl[c]
    nb = int(hc.sum())
    minb = int(size[hc].min()) if nb else None
    b_ok = (minb is None) or (minb >= B)
    # (c)
    ex = size > 0
    for d in dv:
        if d != 1:
            ex &= (fl[d] == (d in D))
    nc = int(ex.sum())
    minc = int(size[ex].min()) if nc else None
    c_low_ok = (minc is None) or (minc >= B)
    c_found = (minc == B)
    wit = witness(M, cs)
    wit_ok = (sum(wit) == B) and B > 0 and exact_pattern(wit, M, D)       # slow layer, long division
    # cross-check a few rows with the slow literal layer
    rng = np.random.default_rng(1)
    for i in rng.choice(len(L), size=min(len(L), 25), replace=False):
        w = [int(x) for x in L[i]]
        assert lhs_structure(w, D)
        g = exists_g(w, M, cs) if sum(w) <= 14 else 'skipped'
        assert (g is not None) or not a_ok
        assert hyp_corners(w, cs) == bool(hc[i])
        assert (sum(w) > 0 and exact_pattern(w, M, D)) == bool(ex[i])
    if not a_ok:
        # show a smallest multiset on which the two sides of structure_iff differ (confirmed by the slow layer)
        Rset = set(map(bytes, R))
        order = np.argsort(size, kind='stable')
        for i in order:
            if bytes(L[i]) not in Rset:
                w = [int(x) for x in L[i]]
                print('#   (a) fails: w = %s (size %d): every Phi_d, d in D, divides its mask (slow layer: %s); a family g'
                      ' exists (slow layer): %s' % (w, sum(w), lhs_structure(w, D), exists_g(w, M, cs) is not None), flush=True)
                break
        Lset = set(map(bytes, L))
        for x in R:
            if bytes(x) not in Lset:
                print('#   (a) fails the other way: w = %s is a sum of periodic functions but not in L' % [int(v) for v in x], flush=True)
                break
    for (name, flag, okflag) in (('(b)', hc, b_ok), ('(c)', ex, c_low_ok)):
        if not okflag:
            i = int(np.argmin(np.where(flag, size, 10 ** 9)))
            w = [int(x) for x in L[i]]
            print('#   %s fails: w = %s (size %d < B = %d); slow layer: hdiv %s, hcor %s, exact pattern %s' % (
                name, w, sum(w), B, lhs_structure(w, D), hyp_corners(w, cs), exact_pattern(w, M, D)), flush=True)
    complete = S >= B - 1
    print('%d\t%s\t%s\t%d\t%s\t%d\t%d\t%d\t%s\t%d\t%s\t%s\t%d\t%s\t%s\t%s\t%s\t%s' % (
        M, list(D), cs, B, label, S, len(L), len(R), 'OK' if a_ok else 'FAIL',
        nb, minb, 'OK' if b_ok else 'FAIL',
        nc, minc, 'OK' if c_low_ok else 'FAIL',
        'found' if c_found else ('not-reached' if S < B else 'MISSING'),
        'OK' if wit_ok else 'FAIL', 'complete' if complete else 'partial'), flush=True)
    return a_ok and b_ok and c_low_ok and wit_ok and (c_found or S < B)


print('M\tD\tcorners\tB\tmethod\tS\t|L|\t|R|\t(a)L=R\t#hdiv&hcor\tmin\t(b)\t#exact\tmin\t(c)lower\t(c)attained-by-search\t(c)witness\tcoverage')
all_ok = True
for D in ups:
    assert is_upset_lean(M, D)
    cs = corners_lean(M, D)
    B = corner_sum(M, cs)
    r = M - sum(len(cyclotomic(d)) - 1 for d in D)
    if S_A >= 0:
        Lmask = np.ones(len(W), dtype=bool)
        for d in D:
            Lmask &= flagsW[d]
        LA = W[Lmask]
        flA = {d: flagsW[d][Lmask] for d in dv}
        all_ok &= analyse(D, cs, B, LA, flA, S_A, 'plain')
    # lattice: as far as the candidate budget allows
    S_B = 0
    while S_B + 1 <= smax_default and comb(r + S_B + 1, r) <= args.lattice_cands:
        S_B += 1
    if D and S_B > S_A:           # for D = ∅ the lattice is everything: nothing beyond the plain run
        t1 = time.time()
        LB = solutions_lattice(M, D, S_B, chunk=int(args.chunk))
        flB = div_flags(LB, M, dv)
        if S_A >= 0:                      # the two methods agree on the sizes both cover
            sub = LB[LB.sum(axis=1, dtype=np.int64) <= S_A]
            assert same_rows(sub, LA), 'lattice and plain enumeration disagree'
        all_ok &= analyse(D, cs, B, LB, flB, S_B, 'lattice(r=%d,%d heads,%.0fs)' % (r, comb(r + S_B, r), time.time() - t1))
print('# M = %d: %s   (%.0f s)' % (M, 'ALL CHECKS PASSED' if all_ok else 'SOME CHECK FAILED', time.time() - t0), flush=True)
sys.exit(0 if all_ok else 1)
