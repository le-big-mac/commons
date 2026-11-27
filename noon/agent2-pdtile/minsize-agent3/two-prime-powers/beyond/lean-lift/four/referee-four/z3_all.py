# z3_all.py mmax -- every multiset on Z_3 with 1..mmax elements (class sizes c0 >= c1 >= c2 >= 0; the six
# permutations of Z_3 are affine maps and change nothing).  Good signings counted exactly through the coefficient
# vectors (rlib.good_count_grid: division by Phi_1 and Phi_3).  Compared with the stated bounds, and with the bound of
# the proof after contraction.
import sys, math
from fractions import Fraction
from rlib import good_count_grid, contract_all

mmax = int(sys.argv[1]) if len(sys.argv) > 1 else 60


def A_formula(t):
    r = 1
    for p in range(3, t + 2, 2):
        if all(p % q for q in range(3, int(p ** 0.5) + 1, 2)):
            r *= 1 + t // (p - 1)
    return r


WUP = sum(Fraction(A_formula(t) - A_formula(t - 2), 2 ** t) for t in range(2, 401, 2)) + Fraction(1, 10 ** 9)
SIX = {2: Fraction(1, 2), 4: Fraction(3, 8), 6: Fraction(3, 16), 8: Fraction(9, 128), 10: Fraction(11, 256), 12: Fraction(23, 1024)}


def stated(m):
    if m % 2 == 1:
        return 1 - WUP
    if m <= 12:
        return SIX[m]
    return Fraction(39, 1000)


viol = 0
ntot = 0
for m in range(1, mmax + 1):
    best = (Fraction(2), None)
    best3 = (Fraction(2), None)
    for c2 in range(0, m // 3 + 1):
        for c1 in range(c2, (m - c2) // 2 + 1):
            c0 = m - c1 - c2
            B = [0] * c0 + [1] * c1 + [2] * c2
            g, tot = good_count_grid(B, 3)
            assert tot == 1 << m
            f = Fraction(g, tot)
            ntot += 1
            if not (f > stated(m) or (m % 2 == 0 and m <= 12 and f >= stated(m))):
                viol += 1
                print("VIOLATION", B, f)
            if f < best[0]:
                best = (f, (c0, c1, c2))
            if c2 >= 1 and f < best3[0]:
                best3 = (f, (c0, c1, c2))
    if m <= 30 or m % 10 == 0:
        print("m = %2d: least fraction of good signings %.5f at class sizes %s; with all three classes occupied %s at %s; stated bound %.5f"
              % (m, float(best[0]), best[1], ("%.5f" % float(best3[0])) if best3[1] else "-", best3[1], float(stated(m))))
print("%d multisets on Z_3 with at most %d elements; violations of the stated bounds: %d" % (ntot, mmax, viol))
