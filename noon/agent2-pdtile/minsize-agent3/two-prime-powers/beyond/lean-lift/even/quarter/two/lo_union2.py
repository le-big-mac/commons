#!/usr/bin/env python3
"""Theorem A of result.md: for each m an upper bound T2(m) for the share of bad signings of ANY multiset of m
elements on ANY odd modulus,

  T2(m) = [m even] c_m + sum over primes p of PP_p(m) + COMP(m).

COMP(m): composite d.  A fully live d corresponds to a tuple (j_p), j_p >= 1 the rank of the live level v_p(d) of p,
  for the primes p of d.  The cells of d (classes modulo d/rad(d)) number at least
  G(d) = max_p (1 + (j_p - 1)(p - 1)), each has at least two elements, and for each prime p of d one of them is
  p-full.  For each prime p of d:  P(bad at d) <= BF_p(G(d), m) := the largest product of cell bounds over all ways of
  putting m elements into at least G(d) cells, one of them p-full, the cells seen through p.
  COMP(m) = sum over tuples with at least two primes of min_p BF_p(G(d), m).
PP_p(m): prime powers of p, the event "bad at some p^i, i >= 1, and not at 1".  Exact (from ptree.py outputs) when
  available, otherwise the bound of section 5 (integer slices, parity, singletons kill deeper levels).

usage: lo_union2.py MMIN MMAX [exact]
"""
import sys, os, re
import numpy as np
from fractions import Fraction
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))


def primes_upto(n):
    return [p for p in range(3, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def maxconv(a, b, Rmax, zero):
    if isinstance(zero, float):
        A = np.asarray(a, dtype=float); B = np.asarray(b, dtype=float); out = np.zeros(Rmax + 1)
        for r1 in range(Rmax + 1):
            x = A[r1]
            if x == 0:
                continue
            np.maximum(out[r1:], x * B[:Rmax + 1 - r1], out=out[r1:])
        return out.tolist()
    out = [zero] * (Rmax + 1)
    for r1 in range(Rmax + 1):
        x = a[r1]
        if x == 0:
            continue
        for r2 in range(Rmax + 1 - r1):
            y = b[r2]
            if y == 0:
                continue
            v = x * y
            if v > out[r1 + r2]:
                out[r1 + r2] = v
    return out


def parts_best(w, k, Rmax, zero, ok=lambda r: True):
    """largest product of w[r] over exactly k parts r >= 1 allowed by ok, with sum R"""
    base = [w[r] if (r >= 1 and ok(r)) else zero for r in range(Rmax + 1)]
    h = base[:]
    for _ in range(k - 1):
        h = maxconv(h, base, Rmax, zero)
    return h


class Tab:
    def __init__(self, Rmax, exact):
        self.Rmax = Rmax
        self.exact = exact
        conv = (lambda a, b: Fraction(a, b)) if exact else (lambda a, b: a / b)
        self.zero = conv(0, 1)
        self.c = [conv(comb(r, r // 2), 2 ** r) for r in range(Rmax + 1)]
        # integer slices: largest probability of a value different from 0
        self.cp = [self.c[r] if r % 2 else conv(comb(r, r // 2 + 1), 2 ** r) for r in range(Rmax + 1)]
        self.cp[0] = self.zero
        # general slices: probability of the value 0 (z), of a given value different from 0 (cnz)
        self.z = self.c[:]
        if Rmax >= 1: self.z[1] = self.zero
        if Rmax >= 3: self.z[3] = conv(1, 4)
        self.cnz = self.c[:]
        if Rmax >= 2: self.cnz[2] = conv(1, 4)


def general_tables(p, T):
    """cell values through the prime p, general slices: vnf (not p-full), vf (p-full)"""
    Rmax, zero = T.Rmax, T.zero
    z = T.z[:]
    if p == 3 and Rmax >= 3:
        z[3] = zero                    # no triangle: the order of the values is prime to 3
    vnf = [z[R] if R >= 2 else zero for R in range(Rmax + 1)]
    Zp = parts_best(z, p, Rmax, zero, lambda r: r >= 2)
    # H1: some class of the cell is a single element (then no class has slice 0, the term with z is absent);
    # H2: every class has at least two elements
    H1 = [zero] * (Rmax + 1)
    H2 = [zero] * (Rmax + 1)
    for zmin in range(1, Rmax // p + 1):
        w = T.cnz[:]
        if p == 3 and zmin == 1 and Rmax >= 2:
            w[2] = zero                # with a single element in the cell, two elements cannot match it (no triangle)
        h = parts_best(w, p - 1, Rmax, zero, lambda r, zmin=zmin: r >= zmin)
        Hx = H1 if zmin == 1 else H2
        for R in range(p, Rmax + 1):
            if R - zmin >= 0 and zmin <= R // p and h[R - zmin] > Hx[R]:
                Hx[R] = h[R - zmin]
    vf = [max(H1[R], Zp[R] + H2[R]) for R in range(Rmax + 1)]
    return vnf, vf


def level_dp(vnf, vf, Gmax, Rmax, zero):
    """best_full[G][R]: largest product over exactly G cells with R elements, at least one of them full"""
    vany = [max(a, b) for a, b in zip(vnf, vf)]
    best_any = [None, vany]
    best_full = [None, vf[:]]
    for G in range(2, Gmax + 1):
        ba = maxconv(vany, best_any[G - 1], Rmax, zero)
        b1 = maxconv(vf, best_any[G - 1], Rmax, zero)
        b2 = maxconv(vany, best_full[G - 1], Rmax, zero)
        best_any.append(ba)
        best_full.append([max(x, y) for x, y in zip(b1, b2)])
    return best_any, best_full


def suffix_max(tab, Gmax, m, zero):
    """BF[G] = max over G' >= G of tab[G'][m], G = 1..Gmax (index 0 unused, BF[Gmax+1] = 0)"""
    BF = [zero] * (Gmax + 2)
    for G in range(Gmax, 0, -1):
        BF[G] = max(BF[G + 1], tab[G][m])
    return BF


def integer_tables(p, T, big):
    """integer slices.  enf: not full (even classes with sum 0); ef: full, flat; df: full, flat, common value != 0.
    big: every class has at least two elements"""
    Rmax, zero = T.Rmax, T.zero
    lo = 2 if big else 1
    enf = [T.c[R] if (R >= 2 and R % 2 == 0) else zero for R in range(Rmax + 1)]
    ef = [zero] * (Rmax + 1)
    df = [zero] * (Rmax + 1)
    for par in (0, 1):
        for zmin in range(lo, Rmax // p + 1):
            if zmin % 2 != par:
                continue
            ok = (lambda r, par=par, zmin=zmin: r % 2 == par and r >= zmin)
            he = parts_best(T.c, p - 1, Rmax, zero, ok)
            hd = parts_best(T.cp, p - 1, Rmax, zero, ok)
            for R in range(p, Rmax + 1):
                if zmin <= R // p:
                    if he[R - zmin] > ef[R]: ef[R] = he[R - zmin]
                    if hd[R - zmin] > df[R]: df[R] = hd[R - zmin]
    return enf, ef, df


def integer_level(p, T, big, Gmax):
    Rmax, zero = T.Rmax, T.zero
    enf, ef, df = integer_tables(p, T, big)
    eany = [max(a, b) for a, b in zip(enf, ef)]
    _, Efull = level_dp(enf, ef, Gmax, Rmax, zero)
    maxP = [None, eany]
    maxV = [None, df[:]]
    for G in range(2, Gmax + 1):
        mp = maxconv(eany, maxP[G - 1], Rmax, zero)
        if isinstance(zero, float):
            mvv = np.zeros(Rmax + 1)
            P1 = np.asarray(maxP[G - 1], dtype=float); V1 = np.asarray(maxV[G - 1], dtype=float)
            for r1 in range(Rmax + 1):
                x, y = df[r1], eany[r1]
                if x == 0 and y == 0:
                    continue
                np.maximum(mvv[r1:], x * P1[:Rmax + 1 - r1] + y * V1[:Rmax + 1 - r1], out=mvv[r1:])
            mv = mvv.tolist()
        else:
            mv = [zero] * (Rmax + 1)
            for r1 in range(Rmax + 1):
                x, y = df[r1], eany[r1]
                if x == 0 and y == 0:
                    continue
                for r2 in range(Rmax + 1 - r1):
                    v = x * maxP[G - 1][r2] + y * maxV[G - 1][r2]
                    if v > mv[r1 + r2]:
                        mv[r1 + r2] = v
        maxP.append(mp); maxV.append(mv)
    return Efull, maxV


def read_exact_U():
    """U_p(m) from the outputs of ptree.py"""
    U = {}
    for fn in sorted(os.listdir(HERE)):
        if fn.startswith('ptree_') and fn.endswith('.out'):
            for line in open(os.path.join(HERE, fn)):
                mm = re.match(r'p=(\d+) m=(\d+) depth=(\d+) .*U_p\(m\)=(\S+)', line)
                if mm:
                    p, m, a = int(mm.group(1)), int(mm.group(2)), int(mm.group(3))
                    if a == (m - 1) // (p - 1):
                        U[(p, m)] = Fraction(mm.group(4))
    return U


def f_sum(n, v, zero):
    """sum over nonempty sets P of primes of prod_{p in P} n[p] * min_{p in P} v[p]"""
    vals = sorted({v[p] for p in v if v[p] > 0 and n[p] > 0})
    total = zero
    prev = zero
    for x in vals:
        prod = 1
        for p in v:
            if n[p] > 0 and v[p] >= x:
                prod *= (1 + n[p])
        total += (x - prev) * (prod - 1)
        prev = x
    return total


def main():
    Mmin, Mmax = int(sys.argv[1]), int(sys.argv[2])
    exact = len(sys.argv) > 3 and sys.argv[3] == 'exact'
    T = Tab(Mmax, exact)
    zero = T.zero
    U = {} if os.environ.get('NOEXACT') else read_exact_U()
    primes = primes_upto(Mmax)
    gen, intl, intb = {}, {}, {}
    for p in primes:
        Gmax = max(1, (Mmax - p) // 2 + 1)
        vnf, vf = general_tables(p, T)
        _, bf = level_dp(vnf, vf, Gmax, Mmax, zero)
        gen[p] = (Gmax, bf)
        intl[p] = integer_level(p, T, False, Gmax)
        intb[p] = integer_level(p, T, True, Gmax)
    three8 = Fraction(3, 8) if exact else 0.375 - 1e-9
    fails = []
    print("# m | level 0 | prime powers (sum of PP_p; * = all exact from ptree.py) | composite | T2(m) | T2(m) <= 3/8")
    for m in range(Mmin, Mmax + 1):
        # ---------- composite d
        BF, ranks = {}, {}
        for p in primes_upto(m):
            Gmax, bf = gen[p]
            B = suffix_max(bf, Gmax, m, zero)
            BF[p] = B
            g = []
            j = 1
            while 1 + (j - 1) * (p - 1) <= Gmax and B[1 + (j - 1) * (p - 1)] > 0:
                g.append(1 + (j - 1) * (p - 1)); j += 1
            ranks[p] = g
        Gs = sorted({G for p in ranks for G in ranks[p]})
        comp = zero
        gen_single = {}
        for G in Gs:
            v = {p: (BF[p][G] if G < len(BF[p]) else zero) for p in ranks}
            n1 = {p: sum(1 for x in ranks[p] if x <= G) for p in ranks}
            n0 = {p: sum(1 for x in ranks[p] if x < G) for p in ranks}
            singles = sum(((n1[p] - n0[p]) * v[p] for p in ranks), zero)
            comp += f_sum(n1, v, zero) - f_sum(n0, v, zero) - singles
        # ---------- prime powers
        pp = zero
        allexact = True
        detail = []
        for p in primes_upto(m):
            if (p, m) in U:
                val = U[(p, m)] if exact else float(U[(p, m)])
            else:
                allexact = False
                Gmax = gen[p][0]
                Ef, Vf = intl[p]
                Eb, Vb = intb[p]
                sE, sV = suffix_max(Ef, Gmax, m, zero), suffix_max(Vf, Gmax, m, zero)
                bE, bV = suffix_max(Eb, Gmax, m, zero), suffix_max(Vb, Gmax, m, zero)
                last, nonlast = [], []
                j = 1
                while 1 + (j - 1) * (p - 1) <= Gmax:
                    G = 1 + (j - 1) * (p - 1)
                    last.append(min(sE[G], sV[G])); nonlast.append(min(bE[G], bV[G]))
                    j += 1
                val = zero
                acc = zero
                for l in range(len(last)):
                    val = max(val, acc + last[l])
                    acc += nonlast[l]
            pp += val
            if p <= 7:
                detail.append("%d:%s" % (p, val if exact else "%.5f" % val))
        lvl0 = T.c[m] if m % 2 == 0 else zero
        t = lvl0 + pp + comp
        ok = t <= three8
        if not ok:
            fails.append(m)
        if exact:
            print(m, "|", lvl0, "|", pp, "*" if allexact else "", "|", comp, "|", t, "= %.6f" % float(t), "|", ok, "|", " ".join(detail))
        else:
            print(m, "| %.6f | %.6f%s | %.6f | %.6f | %s | %s" % (lvl0, pp, "*" if allexact else "", comp, t, ok, " ".join(detail)))
        sys.stdout.flush()
    print("# m in [%d, %d] with T2(m) > 3/8:" % (Mmin, Mmax), fails)


if __name__ == '__main__':
    main()
