#!/usr/bin/env python3
"""Theorem B of result.md: one computation at m = M that bounds the share of bad signings for EVERY m >= M.

  Univ(M, t) = c_M + sum over d* > 1 with mu(d*) <= t of  min over p | d* of max(phi_p(j_p, M), 2^(-(M+p-1)/2))
                   + (W_upper - W_t)

phi_p(j, M): largest product of the plain Littlewood-Offord bounds (c_r for every class but the smallest of a full
group, c_r for every class of a group that is not full, which then has at least two elements) over all ways of putting
M elements into at least 1 + (j-1)(p-1) groups, one of them full.   W_t: partial sum of Lemma W of sign-four-result.md
(sum of 2^(-mu(d)) over odd d > 1 with mu(d) <= t); W_upper = W_60 + 3.4e-6 (its tail bound).

usage: tail.py MLO MHI t
"""
import sys
from math import comb
from fractions import Fraction
import numpy as np


def primes_upto(n):
    return [p for p in range(3, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def maxconv(a, b):
    R = len(a) - 1
    out = np.zeros(R + 1)
    for r1 in range(R + 1):
        if a[r1] == 0:
            continue
        np.maximum(out[r1:], a[r1] * b[:R + 1 - r1], out=out[r1:])
    return out


def A(t):
    r = 1
    for p in primes_upto(t + 1):
        r *= 1 + t // (p - 1)
    return r


def Wpartial(t):
    return sum(Fraction(A(s) - A(s - 2), 2 ** s) for s in range(2, t + 1, 2))


def main():
    Mlo, Mhi, t = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    R = Mhi
    c = np.array([comb(r, r // 2) / 2 ** r for r in range(R + 1)])
    W60 = Wpartial(60)
    Wup = float(W60) + 3.4e-6
    Wt = float(Wpartial(t))
    print("W_60 = %.9f  W_upper = %.9f  W_%d = %.9f  tail = %.9f  number of d* with mu <= %d: %d" % (float(W60), Wup, t, Wt, Wup - Wt, t, A(t) - 1))
    lev = {}
    for p in primes_upto(t + 1):
        vnf = c.copy(); vnf[:2] = 0
        vf = np.zeros(R + 1)
        for zmin in range(1, R // p + 1):
            base = c.copy(); base[:zmin] = 0
            h = base.copy()
            for _ in range(p - 2):
                h = maxconv(h, base)
            for RR in range(p * zmin, R + 1):
                vf[RR] = max(vf[RR], h[RR - zmin])
        vany = np.maximum(vnf, vf)
        Gmax = max(1, 1 + (t // (p - 1) - 1) * (p - 1))
        Gcap = max(1, (R - p) // 2 + 1)
        best_any = [None, vany]; best_full = [None, vf]
        for G in range(2, Gcap + 1):
            ba = maxconv(vany, best_any[G - 1])
            bf = np.maximum(maxconv(vf, best_any[G - 1]), maxconv(vany, best_full[G - 1]))
            best_any.append(ba); best_full.append(bf)
        lev[p] = (Gcap, best_full)
    first = None
    for M in range(Mlo, Mhi + 1):
        prof = {}
        for p in primes_upto(t + 1):
            Gcap, bf = lev[p]
            lst = []
            for j in range(1, t // (p - 1) + 1):
                G0 = 1 + (j - 1) * (p - 1)
                phi = max((bf[G][M] for G in range(G0, Gcap + 1)), default=0.0)
                lst.append(max(phi, 2.0 ** (-(M + p - 1) / 2)))
            prof[p] = lst
        vals = sorted({v for l in prof.values() for v in l})
        total = 0.0; prev = 0.0
        for v in vals:
            prod = 1
            for l in prof.values():
                prod *= 1 + sum(1 for x in l if x >= v)
            total += (v - prev) * (prod - 1)
            prev = v
        univ = c[M] + total + (Wup - Wt)
        ok = univ <= 0.375 - 1e-9
        if ok and first is None:
            first = M
        print("M=%d  c_M=%.6f  sum(mu<=%d)=%.6f  tail=%.6f  Univ=%.6f  %s" % (M, c[M], t, total, Wup - Wt, univ, ok), flush=True)
    print("# smallest M in range with Univ(M, %d) <= 3/8: %s" % (t, first))


if __name__ == '__main__':
    main()
