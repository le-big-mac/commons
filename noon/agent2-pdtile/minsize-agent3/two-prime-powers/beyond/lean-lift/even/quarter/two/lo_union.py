#!/usr/bin/env python3
"""Union bound in characteristic 0 with the sizes of the classes (Theorem A of result.md).

For every m in a range, an upper bound T(m) for the share of bad signings of ANY multiset of m elements
on ANY odd modulus:

  T(m) = [m even] c_m  +  sum over primes p, ranks j of  phi0_p(j, m)      (d = p^i, "bad at d and not at 1")
                       +  sum over tuples (j_p) with at least two primes of  min_p phi_p(j_p, m)   (composite d)

phi_p(j, m):  the largest value, over all ways of placing m elements in the groups of one level of a p-tree
              that has at least 1 + (j-1)(p-1) occupied groups, one of them full, of the product of the
              Littlewood-Offord bounds of the groups (general slices).
phi0_p(j, m): the same for integer slices, with parity, for the event "flat everywhere, some full group has
              a common value different from 0".

usage: lo_union.py MMAX [exact]      (exact: fractions, slow; default floats)
"""
import sys
from fractions import Fraction
from math import comb


def primes_upto(n):
    return [p for p in range(3, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def tables(Rmax, exact):
    conv = (lambda a, b: Fraction(a, b)) if exact else (lambda a, b: a / b)
    c = [conv(comb(r, r // 2), 2 ** r) for r in range(Rmax + 1)]          # c[0] = 1
    cp = [c[r] if r % 2 else conv(comb(r, r // 2 + 1), 2 ** r) for r in range(Rmax + 1)]  # largest nonzero value
    cp[0] = 0 * c[0]
    return c, cp


def maxconv(a, b, Rmax, zero):
    """out[R] = max over R1 + R2 = R of a[R1] * b[R2]"""
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


def parts_best(w, k, Rmax, zero, step_ok=lambda r: True):
    """h[R] = largest product of w[r] over exactly k parts r >= 1 (allowed by step_ok) with sum R"""
    base = [w[r] if (r >= 1 and step_ok(r)) else zero for r in range(Rmax + 1)]
    h = base[:]
    for _ in range(k - 1):
        h = maxconv(h, base, Rmax, zero)
    return h


def prime_tables(p, Rmax, c, cp, zero, one):
    """group values for the prime p.
    general slices: vnf[R] non-full group, vf[R] full group
    integer slices: enf, ef (flat), df (flat with common value != 0)"""
    # general
    vnf = [zero] * (Rmax + 1)
    for R in range(2, Rmax + 1):
        vnf[R] = c[R]
    if Rmax >= 3:
        vnf[3] = c[3] * 2 / 3            # 1/4: three unit vectors with sum 0 are a triangle, two signings of eight
    h = parts_best(c, p - 1, Rmax, zero)
    vf = [zero] * (Rmax + 1)
    for R in range(p, Rmax + 1):
        vf[R] = max(h[R - z] for z in range(1, R // p + 1))
    # integer slices with parity
    enf = [c[R] if (R >= 2 and R % 2 == 0) else zero for R in range(Rmax + 1)]
    ef = [zero] * (Rmax + 1)
    df = [zero] * (Rmax + 1)
    for par in (0, 1):
        ok = (lambda r, par=par: r % 2 == par)
        he = parts_best(c, p - 1, Rmax, zero, ok)
        hd = parts_best(cp, p - 1, Rmax, zero, ok)
        for R in range(p, Rmax + 1):
            for z in range(1, R // p + 1):
                if z % 2 != par:
                    continue
                if he[R - z] > ef[R]:
                    ef[R] = he[R - z]
                if hd[R - z] > df[R]:
                    df[R] = hd[R - z]
    return vnf, vf, enf, ef, df


def level_tables(p, Rmax, c, cp, zero, one):
    vnf, vf, enf, ef, df = prime_tables(p, Rmax, c, cp, zero, one)
    Gmax = max(1, (Rmax - p) // 2 + 1)
    vany = [max(a, b) for a, b in zip(vnf, vf)]
    eany = [max(a, b) for a, b in zip(enf, ef)]
    best_any = [None, vany]
    best_full = [None, vf]
    maxP = [None, eany]
    maxV = [None, df]
    for G in range(2, Gmax + 1):
        ba = maxconv(vany, best_any[G - 1], Rmax, zero)
        b1 = maxconv(vf, best_any[G - 1], Rmax, zero)
        b2 = maxconv(vany, best_full[G - 1], Rmax, zero)
        bf = [max(x, y) for x, y in zip(b1, b2)]
        mp = maxconv(eany, maxP[G - 1], Rmax, zero)
        # maxV[G][R] = max over R' of df[R'] * maxP[G-1][R-R'] + eany[R'] * maxV[G-1][R-R']
        mv = [zero] * (Rmax + 1)
        for r1 in range(Rmax + 1):
            x, y = df[r1], eany[r1]
            if x == 0 and y == 0:
                continue
            for r2 in range(Rmax + 1 - r1):
                v = x * maxP[G - 1][r2] + y * maxV[G - 1][r2]
                if v > mv[r1 + r2]:
                    mv[r1 + r2] = v
        best_any.append(ba); best_full.append(bf); maxP.append(mp); maxV.append(mv)
    return Gmax, best_full, maxV


def phis(p, m, Gmax, best_full, maxV, zero):
    """lists phi_p(j, m), phi0_p(j, m) for j = 1, 2, ... while positive"""
    ph, ph0 = [], []
    j = 1
    while True:
        Gmin = 1 + (j - 1) * (p - 1)
        if Gmin > Gmax:
            break
        a = max((best_full[G][m] for G in range(Gmin, Gmax + 1)), default=zero)
        b = max((maxV[G][m] for G in range(Gmin, Gmax + 1)), default=zero)
        if a == 0:
            break
        ph.append(a); ph0.append(b)
        j += 1
    return ph, ph0


def composite_sum(prof, zero):
    """sum over tuples (j_p), at least two primes with j_p > 0, of min over those primes of prof[p][j_p - 1];
    prof[p] nonincreasing lists of positive values"""
    vals = sorted({v for lst in prof.values() for v in lst})
    total = zero
    prev = zero
    for v in vals:
        prod = 1
        s = 0
        for lst in prof.values():
            n = sum(1 for x in lst if x >= v)
            prod *= (1 + n)
            s += n
        total += (v - prev) * (prod - 1 - s)
        prev = v
    return total


def main():
    Mmax = int(sys.argv[1])
    exact = len(sys.argv) > 2 and sys.argv[2] == 'exact'
    zero = Fraction(0) if exact else 0.0
    one = Fraction(1) if exact else 1.0
    c, cp = tables(Mmax, exact)
    T = {}
    lev = {}
    for p in primes_upto(Mmax):
        lev[p] = level_tables(p, Mmax, c, cp, zero, one)
    print("m  level0  primepowers  composite  T(m)  T(m)<=3/8  [profiles of 3, 5, 7]")
    for m in range(3, Mmax + 1):
        prof, prof0 = {}, {}
        for p in primes_upto(m):
            Gmax, bf, mv = lev[p]
            ph, ph0 = phis(p, m, Gmax, bf, mv, zero)
            if ph:
                prof[p] = ph; prof0[p] = ph0
        lvl0 = c[m] if m % 2 == 0 else zero
        pp = sum((sum(v) for v in prof0.values()), zero)
        comp = composite_sum(prof, zero)
        t = lvl0 + pp + comp
        T[m] = t
        ok = (t <= Fraction(3, 8)) if exact else (t <= 0.375 - 1e-9)
        if exact:
            extra = "  ".join("%d:%s|%s" % (p, ",".join(str(x) for x in prof[p][:3]), ",".join(str(x) for x in prof0[p][:3]))
                              for p in (3, 5, 7) if p in prof)
            print(m, lvl0, pp, comp, t, "%.6f" % float(t), ok, extra)
        else:
            extra = "  ".join("%d:%s|%s" % (p, ",".join("%.4f" % x for x in prof[p][:3]), ",".join("%.4f" % x for x in prof0[p][:3]))
                              for p in (3, 5, 7) if p in prof)
            print(m, "%.6f %.6f %.6f %.6f" % (lvl0, pp, comp, t), ok, extra)
    bad = [m for m in T if not ((T[m] <= Fraction(3, 8)) if exact else (T[m] <= 0.375 - 1e-9))]
    print("m with T(m) > 3/8:", bad)


if __name__ == '__main__':
    main()
