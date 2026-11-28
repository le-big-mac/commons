#!/usr/bin/env python3
"""Referee's own tables for result.md, sections 2, 3, 4 (Prop. 7), 5, written from the text's definitions with exact
fractions and memoised recursions (no code of the author's is imported).

  c, z, cnz, vnf_p, vf_p (H1, H2, Z), BF_p(G, m), COMP(m) by plain enumeration of the families (j_p),
  enf, ef_p, df_p, last_p, nonlast_p, PP_p(m), T2(m).

usage: r_tables.py MMAX [noexact]
The exact U_p(m) are read from a table typed here from the TEXT (section 4) -- and cross-checked separately against
r_tree.py outputs by r_compare.py.
"""
import sys
from fractions import Fraction as F
from math import comb
from functools import lru_cache

sys.setrecursionlimit(10000)


def primes_upto(n):
    return [q for q in range(3, n + 1) if all(q % r for r in range(2, int(q ** 0.5) + 1))]


@lru_cache(maxsize=None)
def c(r):
    return F(comb(r, r // 2), 2 ** r)


def cnz(r):
    if r == 1: return F(1, 2)
    if r == 2: return F(1, 4)
    return c(r)


def z(r, p):
    if r == 1: return F(0)
    if r == 2: return F(1, 2)
    if r == 3: return F(0) if p == 3 else F(1, 4)
    return c(r)


def cprime(r):
    """integer sums: largest share of a value other than 0"""
    if r % 2: return c(r)
    return F(comb(r, r // 2 + 1), 2 ** r)


WEIGHTS = {}


def w_of(name, p):
    key = (name, p)
    if key not in WEIGHTS:
        if name == 'cnz': f = cnz
        elif name == 'cnz_no2': f = (lambda r: F(0) if r == 2 else cnz(r))
        elif name == 'z': f = (lambda r, p=p: z(r, p))
        elif name == 'c': f = c
        elif name == 'cp': f = cprime
        WEIGHTS[key] = f
    return WEIGHTS[key]


@lru_cache(maxsize=None)
def best(name, p, k, n, lo, par):
    """largest product of w(r_1)...w(r_k), r_i >= lo, r_i = par mod 2 if par in (0, 1), sum n; 0 if impossible"""
    w = w_of(name, p)
    if k == 0:
        return F(1) if n == 0 else F(0)
    if n < k * lo:
        return F(0)
    b = F(0)
    for r in range(lo, n - (k - 1) * lo + 1):
        if par in (0, 1) and r % 2 != par:
            continue
        x = w(r)
        if x == 0:
            continue
        y = best(name, p, k - 1, n - r, lo, par)
        if x * y > b:
            b = x * y
    return b


@lru_cache(maxsize=None)
def vnf(p, R):
    return z(R, p) if R >= 2 else F(0)


@lru_cache(maxsize=None)
def vf(p, R):
    if R < p:
        return F(0)
    H1 = best('cnz_no2' if p == 3 else 'cnz', p, p - 1, R - 1, 1, -1)
    H2 = F(0)
    for s in range(2, R // p + 1):
        H2 = max(H2, best('cnz', p, p - 1, R - s, s, -1))
    Z = best('z', p, p, R, 2, -1)
    return max(H1, Z + H2)


@lru_cache(maxsize=None)
def cells(p, k, n, needfull):
    """largest product over exactly k cells with n elements (each cell >= 2), one valued vf if needfull"""
    if k == 0:
        return F(1) if (n == 0 and not needfull) else F(0)
    if n < 2 * k:
        return F(0)
    b = F(0)
    for R in range(2, n - 2 * (k - 1) + 1):
        a_any = max(vnf(p, R), vf(p, R))
        if needfull:
            x = vf(p, R)
            if x:
                b = max(b, x * cells(p, k - 1, n - R, False))
            if a_any:
                b = max(b, a_any * cells(p, k - 1, n - R, True))
        else:
            if a_any:
                b = max(b, a_any * cells(p, k - 1, n - R, False))
    return b


@lru_cache(maxsize=None)
def BF(p, G, m):
    b = F(0)
    for k in range(G, m // 2 + 1):
        b = max(b, cells(p, k, m, True))
    return b


def COMP(m):
    ps = primes_upto(m)
    # ranks with BF > 0 at their own G; a family containing a rank with BF_p(G_p) = 0 contributes 0
    ranks = {}
    for p in ps:
        g = []
        j = 1
        while BF(p, 1 + (j - 1) * (p - 1), m) > 0:
            g.append(1 + (j - 1) * (p - 1)); j += 1
        ranks[p] = g
    total = F(0)
    nfam = 0

    def rec(i, chosen, maxG):
        nonlocal total, nfam
        if i == len(ps):
            if len(chosen) >= 2:
                nfam += 1
                total += min(BF(p, maxG, m) for p in chosen)
            return
        rec(i + 1, chosen, maxG)
        p = ps[i]
        for G in ranks[p]:
            rec(i + 1, chosen + [p], max(maxG, G))

    rec(0, [], 1)
    return total, nfam


# ---------------- Proposition 7
@lru_cache(maxsize=None)
def enf(R):
    return c(R) if (R >= 2 and R % 2 == 0) else F(0)


@lru_cache(maxsize=None)
def ef_df(p, R, lo):
    """largest product of c (resp. c') over the p classes but a smallest, sizes of one parity, all >= lo"""
    e = d = F(0)
    for s in range(lo, R // p + 1):
        par = s % 2
        e = max(e, best('c', p, p - 1, R - s, s, par))
        d = max(d, best('cp', p, p - 1, R - s, s, par))
    return e, d


@lru_cache(maxsize=None)
def Emax(p, k, n, needfull, lo):
    """largest product of e over exactly k groups with n elements, one of them full (valued ef) if needfull"""
    if k == 0:
        return F(1) if (n == 0 and not needfull) else F(0)
    if n < 2 * k:
        return F(0)
    b = F(0)
    for R in range(2, n - 2 * (k - 1) + 1):
        ef = ef_df(p, R, lo)[0]
        ea = max(enf(R), ef)
        if needfull:
            if ef:
                b = max(b, ef * Emax(p, k - 1, n - R, False, lo))
            if ea:
                b = max(b, ea * Emax(p, k - 1, n - R, True, lo))
        else:
            if ea:
                b = max(b, ea * Emax(p, k - 1, n - R, False, lo))
    return b


@lru_cache(maxsize=None)
def Vmax(p, k, n, lo):
    """the text's upper bound for the largest sum_k delta(D_k) prod_{l != k} e(D_l): recursion over the groups"""
    if k == 0:
        return F(0)
    b = F(0)
    for R in range(0, n + 1):
        ef, df = ef_df(p, R, lo)
        ea = max(enf(R), ef)
        if df == 0 and ea == 0:
            continue
        v = df * Emax(p, k - 1, n - R, False, lo) + ea * Vmax(p, k - 1, n - R, lo)
        if v > b:
            b = v
    return b


def PP(p, m):
    kmax = m // 2
    out_last, out_non = [], []
    j = 1
    while 1 + (j - 1) * (p - 1) <= kmax:
        G = 1 + (j - 1) * (p - 1)
        lastE = max(Emax(p, k, m, True, 1) for k in range(G, kmax + 1))
        lastV = max(Vmax(p, k, m, 1) for k in range(G, kmax + 1))
        nonE = max(Emax(p, k, m, True, 2) for k in range(G, kmax + 1))
        nonV = max(Vmax(p, k, m, 2) for k in range(G, kmax + 1))
        out_last.append(min(lastE, lastV)); out_non.append(min(nonE, nonV))
        j += 1
    val = F(0); acc = F(0)
    for l in range(len(out_last)):
        val = max(val, acc + out_last[l])
        acc += out_non[l]
    return val


# exact U_p(m) as printed in the TEXT (section 4)
U_TEXT = {
    3: dict(zip(range(3, 17), "1/4 0 3/16 1/32 5/32 1/32 35/256 19/512 63/512 9/256 231/2048 143/4096 429/4096 69/2048".split())),
    5: dict(zip(range(5, 17), "1/16 0 3/64 0 5/128 1/512 35/1024 1/512 63/2048 1/512 231/8192 1/512".split())),
    7: dict(zip(range(7, 17), "1/64 0 3/256 0 5/512 0 35/4096 1/8192 63/8192 1/8192".split())),
    11: dict(zip(range(11, 17), "1/1024 0 3/4096 0 5/8192 0".split())),
    13: dict(zip(range(13, 17), "1/4096 0 3/16384 0".split())),
}
# U_5 for m = 17..20 is not printed in the text; values from the author's ptree_5.out (checked by r_tree.py)
U_TEXT[5].update({17: "429/16384", 18: "1/512", 19: "6435/262144", 20: "1025/524288"})


def main():
    MMAX = int(sys.argv[1])
    noexact = len(sys.argv) > 2 and sys.argv[2] == 'noexact'
    print("# m | level0 | sum_p U_p or PP_p | COMP (families) | T2 | T2 <= 3/8 | per prime 3,5,7")
    for m in range(3, MMAX + 1):
        lvl0 = c(m) if m % 2 == 0 else F(0)
        pp = F(0); det = []
        for p in primes_upto(m):
            if (not noexact) and p in U_TEXT and m in U_TEXT[p]:
                v = F(U_TEXT[p][m])
            else:
                v = PP(p, m)
            pp += v
            if p <= 7:
                det.append("%d:%s" % (p, v))
        comp, nfam = COMP(m)
        t = lvl0 + pp + comp
        print(m, "|", lvl0, "|", pp, "|", comp, "(%d)" % nfam, "|", t, "= %.6f" % float(t), "|", t <= F(3, 8), "|", " ".join(det), flush=True)


if __name__ == '__main__':
    main()
