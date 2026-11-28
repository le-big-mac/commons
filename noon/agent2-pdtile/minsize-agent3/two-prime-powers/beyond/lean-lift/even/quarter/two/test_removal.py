#!/usr/bin/env python3
"""Test of Lemma 8 (removal) on computed values, exact fractions:

    phi_p(j, m + 1) <= max(phi_p(j, m), 2^(-(m+p-1)/2))     for all primes p <= PMAX, ranks j, m < MMAX,

phi_p(j, m) the plain value of section 6 (the largest product over all configurations), computed here by a dynamic
programme of its own, with fractions.  2^(-(m+p-1)/2) is compared exactly, through squares.

Then, with the same exact values, an upper bound for Univ(M, t) of Theorem B in fractions: the second term
2^(-(M+p-1)/2) is replaced by the larger 2^(-floor((M+p-1)/2)), W_t is exact, and only the cited bound
W < W_60 + 3.4e-6 is taken as a decimal.

With a fifth argument "cert" (added after the referee's report, its item (ii)): 2^(-1/2) is replaced by the larger
rational 70710678119/10^11 (checked: 2 * 70710678119^2 >= 10^22), so that for odd M + p - 1 the second term is
bounded by 2^(-floor((M+p-1)/2)) * 70710678119/10^11 instead of 2^(-floor((M+p-1)/2)).

usage: test_removal.py PMAX MMAX [M t [cert]]      (PMAX >= t + 1, MMAX > M)
"""
import sys
from fractions import Fraction
from math import comb


def primes_upto(n):
    return [p for p in range(3, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def maxconv(a, b, R):
    out = [Fraction(0)] * (R + 1)
    for r1 in range(R + 1):
        x = a[r1]
        if x == 0:
            continue
        for r2 in range(R + 1 - r1):
            y = b[r2]
            if y and x * y > out[r1 + r2]:
                out[r1 + r2] = x * y
    return out


def main():
    PMAX, R = int(sys.argv[1]), int(sys.argv[2])
    c = [Fraction(comb(r, r // 2), 2 ** r) for r in range(R + 1)]
    checked = strict_second = 0
    PHI = {}
    for p in primes_upto(PMAX):
        vnf = [c[r] if r >= 2 else Fraction(0) for r in range(R + 1)]
        vf = [Fraction(0)] * (R + 1)
        for zmin in range(1, R // p + 1):
            base = [c[r] if r >= zmin else Fraction(0) for r in range(R + 1)]
            h = base[:]
            for _ in range(p - 2):
                h = maxconv(h, base, R)
            for RR in range(p * zmin, R + 1):
                vf[RR] = max(vf[RR], h[RR - zmin])
        vany = [max(a, b) for a, b in zip(vnf, vf)]
        Gcap = max(1, (R - p) // 2 + 1)
        best_any = [None, vany]; best_full = [None, vf]
        for G in range(2, Gcap + 1):
            best_any.append(maxconv(vany, best_any[G - 1], R))
            b1 = maxconv(vf, best_any[G - 1], R); b2 = maxconv(vany, best_full[G - 1], R)
            best_full.append([max(x, y) for x, y in zip(b1, b2)])
        j = 1
        while 1 + (j - 1) * (p - 1) <= Gcap:
            G0 = 1 + (j - 1) * (p - 1)
            phi = [max(best_full[G][m] for G in range(G0, Gcap + 1)) for m in range(R + 1)]
            PHI[(p, j)] = phi
            for m in range(1, R):
                lhs = phi[m + 1]
                if lhs <= phi[m]:
                    checked += 1
                    continue
                # lhs <= 2^(-(m+p-1)/2)  iff  lhs^2 <= 2^(-(m+p-1))
                assert lhs * lhs <= Fraction(1, 2 ** (m + p - 1)), ("Lemma 8 fails", p, j, m, lhs, phi[m])
                checked += 1; strict_second += 1
            j += 1
    print("test_removal: primes <= %d, m < %d: %d cases (p, j, m) checked, in %d of them phi grows and is covered by the second term. NO FAILURE"
          % (PMAX, R, checked, strict_second))
    if len(sys.argv) > 4:
        M, t = int(sys.argv[3]), int(sys.argv[4])
        cert = len(sys.argv) > 5 and sys.argv[5] == 'cert'
        RS = Fraction(70710678119, 10 ** 11)          # an upper bound for 2^(-1/2)
        assert 2 * 70710678119 ** 2 >= 10 ** 22
        prof = {}
        for p in primes_upto(t + 1):
            lst = []
            for j in range(1, t // (p - 1) + 1):
                phi = PHI[(p, j)][M] if (p, j) in PHI else Fraction(0)
                second = Fraction(1, 2 ** ((M + p - 1) // 2))
                if cert and (M + p - 1) % 2 == 1:
                    second *= RS
                lst.append(max(phi, second))
            prof[p] = lst
        vals = sorted({v for l in prof.values() for v in l})
        total = Fraction(0); prev = Fraction(0); ntup = 0
        for v in vals:
            prod = 1
            for l in prof.values():
                prod *= 1 + sum(1 for x in l if x >= v)
            total += (v - prev) * (prod - 1)
            prev = v
        ntup = 1
        for l in prof.values():
            ntup *= 1 + len(l)

        def A(u):
            r = 1
            for q in primes_upto(u + 1):
                r *= 1 + u // (q - 1)
            return r
        W = lambda u: sum(Fraction(A(x) - A(x - 2), 2 ** x) for x in range(2, u + 1, 2))
        tailw = W(60) + Fraction(34, 10 ** 7) - W(t)
        univ = c[M] + total + tailw
        print("Univ(%d, %d) <= c_M + sum + tail = %.9f + %.9f + %.9f = %.9f  (%d values of d*);  <= 3/8: %s"
              % (M, t, float(c[M]), float(total), float(tailw), float(univ), ntup - 1, univ <= Fraction(3, 8)))
        if cert:
            print("cert: 2^(-1/2) replaced by 70710678119/10^11; exact comparisons: Univ < 36242/100000: %s; Univ < 3625/10000: %s; Univ <= 362413084/10^9: %s"
                  % (univ < Fraction(36242, 100000), univ < Fraction(3625, 10000), univ <= Fraction(362413084, 10 ** 9)))
            # added after the referee's second look: the bound written in the proof of Theorem B
            print("cert: exact comparison: Univ < 3624131/10^7: %s" % (univ < Fraction(3624131, 10 ** 7)))


if __name__ == '__main__':
    main()
