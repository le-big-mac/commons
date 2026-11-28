#!/usr/bin/env python3
"""After the referee's report, item (i): PP_p(m) recomputed from the definitions as now worded in Proposition 7 of
result.md (one group: enf, ef_p, df_p by plain enumeration of the class sizes; G groups: the recursions P_G, E_G,
V_G; ranks: last_p, nonlast_p; PP_p), written without using lo_union2.py, and compared with the values printed in
lo2_exact_46.out (its last column, primes 3, 5, 7) for 17 <= m <= MMAX (for p = 5 from m = 21: up to 20 the exact
U_5 was used there).

usage: check_prop7.py MMAX
"""
import sys, re
from fractions import Fraction
from math import comb


def parts(R, k, lo, mx=None):
    """nonincreasing k-tuples of integers >= lo with sum R"""
    if mx is None:
        mx = R
    if k == 0:
        if R == 0:
            yield ()
        return
    for first in range(min(R - lo * (k - 1), mx), lo - 1, -1):
        if first < lo:
            break
        for rest in parts(R - first, k - 1, lo, first):
            yield (first,) + rest


def group_values(p, M, lo):
    c = [Fraction(comb(r, r // 2), 2 ** r) for r in range(M + 1)]
    cp = [c[r] if r % 2 else Fraction(comb(r, r // 2 + 1), 2 ** r) for r in range(M + 1)]
    enf = [c[R] if (R >= 2 and R % 2 == 0) else Fraction(0) for R in range(M + 1)]
    ef = [Fraction(0)] * (M + 1)
    df = [Fraction(0)] * (M + 1)
    for R in range(p, M + 1):
        for sz in parts(R, p, lo):
            if len({r % 2 for r in sz}) != 1:
                continue
            others = sz[:-1]            # all but a smallest
            a = Fraction(1); b = Fraction(1)
            for r in others:
                a *= c[r]; b *= cp[r]
            ef[R] = max(ef[R], a); df[R] = max(df[R], b)
    return enf, ef, df


def levels(p, M, lo):
    enf, ef, df = group_values(p, M, lo)
    P1 = [max(x, y) for x, y in zip(enf, ef)]
    Gcap = max(1, (M - p) // 2 + 1)
    P = {1: P1}; E = {1: ef}; V = {1: df}
    for G in range(2, Gcap + 1):
        Pg = [Fraction(0)] * (M + 1); Eg = [Fraction(0)] * (M + 1); Vg = [Fraction(0)] * (M + 1)
        for R in range(M + 1):
            for r in range(R + 1):
                Pg[R] = max(Pg[R], P1[r] * P[G - 1][R - r])
                Eg[R] = max(Eg[R], ef[r] * P[G - 1][R - r], P1[r] * E[G - 1][R - r])
                Vg[R] = max(Vg[R], df[r] * P[G - 1][R - r] + P1[r] * V[G - 1][R - r])
        P[G] = Pg; E[G] = Eg; V[G] = Vg
    return Gcap, E, V


def main():
    M = int(sys.argv[1])
    want = {}
    for line in open('lo2_exact_46.out'):
        f = [x.strip() for x in line.split('|')]
        if len(f) >= 7 and f[0].isdigit():
            for tok in f[6].split():
                q, val = tok.split(':')
                want[(int(q), int(f[0]))] = Fraction(val)
    n = 0
    for p in (3, 5, 7):
        Gcap, E, V = levels(p, M, 1)
        _, Eb, Vb = levels(p, M, 2)
        for m in range(17, M + 1):
            if p == 5 and m <= 20:
                continue
            last, nonlast = [], []
            j = 1
            while 1 + (j - 1) * (p - 1) <= Gcap:
                G0 = 1 + (j - 1) * (p - 1)
                last.append(min(max(E[G][m] for G in range(G0, Gcap + 1)), max(V[G][m] for G in range(G0, Gcap + 1))))
                nonlast.append(min(max(Eb[G][m] for G in range(G0, Gcap + 1)), max(Vb[G][m] for G in range(G0, Gcap + 1))))
                j += 1
            pp = Fraction(0); acc = Fraction(0)
            for l in range(len(last)):
                pp = max(pp, acc + last[l]); acc += nonlast[l]
            assert pp == want[(p, m)], ("PP differs", p, m, pp, want[(p, m)])
            n += 1
    print("check_prop7: PP_p(m) from the definitions of Proposition 7 equals the value of lo2_exact_46.out in all %d cases (p = 3, 7: m = 17..%d; p = 5: m = 21..%d)" % (n, M, M))


if __name__ == '__main__':
    main()
