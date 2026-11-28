#!/usr/bin/env python3
"""Referee's own computation for section 6 of result.md (Lemma 8, Theorem B), from the text's definitions.

phi_p(j, m): largest product over the configurations: m elements in at least 1 + (j-1)(p-1) cells, each "not full"
with R >= 2 elements and value c_R, or "full" with p classes r_t >= 1 and value prod_{t != t0} c_(r_t) (t0 a smallest
class), at least one full.
Univ(M, t) = c_M + sum over d* > 1 with mu(d*) <= t of min_{p | d*} max(phi_p(v_p(d*), M), 2^(-(M+p-1)/2)) + (W - W_t).

usage: r_tail.py M t MCHECK      (MCHECK: Lemma 8 is checked on computed values for M <= m' <= MCHECK)
"""
import sys, math
from fractions import Fraction as F
from functools import lru_cache
import r_tables as RT

c = RT.c


@lru_cache(maxsize=None)
def fullval(p, R):
    b = F(0)
    for s in range(1, R // p + 1):
        b = max(b, RT.best('c', p, p - 1, R - s, s, -1))
    return b


@lru_cache(maxsize=None)
def conf(p, k, n, needfull):
    if k == 0:
        return F(1) if (n == 0 and not needfull) else F(0)
    if n < 2 * k:
        return F(0)
    b = F(0)
    for R in range(2, n - 2 * (k - 1) + 1):
        nf = c(R)
        fv = fullval(p, R)
        if needfull:
            if fv:
                b = max(b, fv * conf(p, k - 1, n - R, False))
            b = max(b, max(nf, fv) * conf(p, k - 1, n - R, True))
        else:
            b = max(b, max(nf, fv) * conf(p, k - 1, n - R, False))
    return b


@lru_cache(maxsize=None)
def phi(p, j, m):
    G0 = 1 + (j - 1) * (p - 1)
    b = F(0)
    for k in range(G0, m // 2 + 1):
        b = max(b, conf(p, k, m, True))
    return b


def A(t):
    r = 1
    for p in RT.primes_upto(t + 1):
        r *= 1 + t // (p - 1)
    return r


def Wpart(t):
    return sum((F(A(s) - A(s - 2), 2 ** s) for s in range(2, t + 1, 2)), F(0))


def main():
    M, t, MCHECK = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    ps = RT.primes_upto(t + 1)
    # ---- W
    W60 = Wpart(60); Wt = Wpart(t)
    print("A(30) =", A(30), " W_30 =", Wpart(30), "= %.9f" % float(Wpart(30)), " W_60 =", W60, "= %.9f" % float(W60))
    # the tail of sign-four-result.md, Lemma W, redone: K < 1.2578, x = e^(2K/3)/4, sum_{u >= 31} (u+1) x^u
    K = sum(math.log(1 + 1 / k) / k for k in range(1, 2000)) + 1 / 1999
    x = math.exp(2 * K / 3) / 4
    tail60 = x ** 31 * (32 - 31 * x) / (1 - x) ** 2
    print("K < %.7f  x < %.6f  tail beyond t = 60 < %.3e (text: 3.4e-6)" % (K, x, tail60))
    # exact terms up to 400 as a further check of the size of the tail
    print("W_400 - W_60 = %.3e" % float(Wpart(400) - W60))
    Wup = W60 + F(34, 10 ** 7)
    # ---- Lemma 8 on computed values: phi_p(j, m') <= max(phi_p(j, M0), 2^(-(M0+p-1)/2)) for M0 <= m' <= MCHECK
    ncase = nfail = ngrow = 0
    for p in ps:
        for j in range(1, t // (p - 1) + 1):
            for M0 in range(p, MCHECK + 1):
                for m2 in (M0 + 1,) if M0 < MCHECK else ():
                    a = phi(p, j, m2); b = phi(p, j, M0)
                    ncase += 1
                    if a > b:
                        ngrow += 1
                        # need a <= 2^(-(M0+p-1)/2):  a^2 <= 2^-(M0+p-1)
                        if a * a > F(1, 2 ** (M0 + p - 1)):
                            nfail += 1
                            print("  LEMMA 8 FAILS at p=%d j=%d m=%d -> %d: %s > max(%s, 2^-%s/2)" % (p, j, M0, m2, a, b, M0 + p - 1))
    print("Lemma 8, one step m -> m+1, primes <= %d, m < %d: %d cases, phi grows in %d, failures %d" % (t + 1, MCHECK, ncase, ngrow, nfail))
    # ---- Univ(M, t)
    valf = {}; valx = {}
    for p in ps:
        for j in range(1, t // (p - 1) + 1):
            ph = phi(p, j, M)
            e = M + p - 1
            valf[(p, j)] = max(float(ph), 2.0 ** (-e / 2))
            valx[(p, j)] = max(ph, F(1, 2 ** (e // 2)))          # rounded up
    tot_f = 0.0; tot_x = F(0); n = 0

    def rec(i, mf, mx, nonempty):
        nonlocal tot_f, tot_x, n
        if i == len(ps):
            if nonempty:
                n += 1; tot_f += mf; tot_x += mx
            return
        rec(i + 1, mf, mx, nonempty)
        p = ps[i]
        for j in range(1, t // (p - 1) + 1):
            rec(i + 1, min(mf, valf[(p, j)]), min(mx, valx[(p, j)]), True)

    rec(0, float('inf'), F(10), False)
    cM = c(M)
    print("M=%d t=%d: number of d* = %d;  c_M = %.9f;  sum (float, the text's definition) = %.9f;  sum (fractions, 2^-floor) = %.9f" % (M, t, n, float(cM), tot_f, float(tot_x)))
    print("  tail W_up - W_t = %.9f" % float(Wup - Wt))
    print("  Univ (float) = %.9f   Univ (exact upper bound) = %.9f  <= 3/8: %s" % (float(cM) + tot_f + float(Wup - Wt), float(cM + tot_x + Wup - Wt), cM + tot_x + Wup - Wt <= F(3, 8)))
    for (p, j) in [(3, 1), (3, 2), (3, 3), (5, 1), (5, 2), (7, 1), (11, 1), (13, 1), (31, 1)]:
        print("  phi_%d(%d, %d) = %s = %.3e" % (p, j, M, phi(p, j, M), float(phi(p, j, M))))


if __name__ == '__main__':
    main()
