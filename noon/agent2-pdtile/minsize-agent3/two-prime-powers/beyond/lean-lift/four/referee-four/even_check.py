# even_check.py -- section 4 of sign-four-result.md, the even case, with exact fractions.
#   c_k = C(k, floor(k/2)) / 2^k
#   W_m = sum over odd d > 1 with mu(d) <= m-1 of 2^(-mu(d))
# Checks: the six fractions for m <= 12; c_m + W_m for every even m <= MMAX; the level d = 3 for m >= 14
# (every triple of class sizes); c_m + W_m - 1/4 + 5/32 < 1; c_k non-increasing.
import sys, math
from fractions import Fraction
from rlib import mu, divisors, nprime

MMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 400


def c(k):
    return Fraction(math.comb(k, k // 2), 2 ** k)


def A(t):
    r = 1
    for p in range(3, t + 2, 2):
        if all(p % q for q in range(3, int(p ** 0.5) + 1, 2)):
            r *= 1 + t // (p - 1)
    return r


def Wm_formula(m):
    return sum(Fraction(A(t) - A(t - 2), 2 ** t) for t in range(2, m, 2))      # even t <= m-1


def Wm_enum(m):
    return sum(Fraction(1, 2 ** mu(d)) for d in divisors(nprime(m)) if d > 1)


# c_k: largest probability of one value of a sum of k signs; non-increasing
for k in range(1, 400):
    dist = [Fraction(math.comb(k, j), 2 ** k) for j in range(k + 1)]
    assert max(dist) == c(k)
    assert c(k + 1) <= c(k)
    if k % 2 == 1:
        assert c(k) == c(k + 1) and c(k + 1) > c(k + 2)
print("c_k = max_j C(k,j)/2^k; c_(2j-1) = c_(2j) > c_(2j+1) for k < 400")
print("c_1..c_6 =", [str(c(k)) for k in range(1, 7)])

print("\neven m <= 12: c_m + W_m (W_m by enumeration of the divisors of n'_m, mu by factoring)")
stated = {2: Fraction(1, 2), 4: Fraction(3, 8), 6: Fraction(3, 16), 8: Fraction(9, 128), 10: Fraction(11, 256), 12: Fraction(23, 1024)}
for m in range(2, 13, 2):
    w = Wm_enum(m)
    assert w == Wm_formula(m)
    tot = c(m) + w
    print("  m = %2d: c_m = %s, W_m = %s, sum = %s, 1 - sum = %s (stated %s: %s)" % (m, c(m), w, tot, 1 - tot, stated[m], "equal" if 1 - tot == stated[m] else "DIFFERENT"))

print("\nW_m by enumeration equals the formula for m <= 27:", all(Wm_enum(m) == Wm_formula(m) for m in range(2, 28)))

# an upper bound for W: partial sum to t = 1000 plus 1e-27 (w_check.py, cruder tail)
WUP = sum(Fraction(A(t) - A(t - 2), 2 ** t) for t in range(2, 1001, 2)) + Fraction(1, 10 ** 27)
print("W < %.15f" % float(WUP))

print("\nevery even m <= %d: plain sum c_m + W_m, and with 5/32 in place of 1/4 for the level d = 3" % MMAX)
plain_ge1 = []
sharp_max = (0, None)
for m in range(2, MMAX + 1, 2):
    w = Wm_formula(m)
    plain = c(m) + w
    if plain >= 1:
        plain_ge1.append(m)
    if m >= 14:
        sharp = plain - Fraction(1, 4) + Fraction(5, 32)
        assert sharp < 1, m
        assert c(m) + WUP - Fraction(3, 32) < 1
        if sharp > sharp_max[0]:
            sharp_max = (sharp, m)
    else:
        assert plain < 1, m
    if m <= 40 or m % 40 == 0:
        print("  m = %3d: c_m + W_m = %.6f%s" % (m, float(plain), "" if m < 14 else ";  - 3/32: %.6f" % float(plain - Fraction(3, 32))))
print("plain sum >= 1 exactly for m in", plain_ge1)
print("largest value of c_m + W_m - 3/32 over even 14 <= m <= %d: %.6f at m = %d" % (MMAX, float(sharp_max[0]), sharp_max[1]))
print("c_14 + W - 3/32 < %.6f  (W replaced by its upper bound; c_m <= c_14 for m >= 14)" % float(c(14) + WUP - Fraction(3, 32)))
print("so the fraction of good signings for even m >= 14 is more than %.6f" % float(1 - (c(14) + WUP - Fraction(3, 32))))
print("c_24 + W = %.6f, c_26 + W = %.6f" % (float(c(24) + WUP), float(c(26) + WUP)))
# odd m: W_m < W < 1
print("odd m: 1 - W > %.6f" % float(1 - WUP))

# the level d = 3: all triples k0 >= k1 >= k2 >= 1, k0 + k1 + k2 = m
print("\nlevel d = 3: P(s0 = s1 = s2) for the three classes modulo 3, all triples of class sizes")


def dist(k):
    return {2 * j - k: math.comb(k, j) for j in range(k + 1)}          # value -> number of sign vectors


TM = 120
viol = 0
ntr = 0
best = {}
for m in range(3, TM + 1):
    for k2 in range(1, m // 3 + 1):
        d2 = dist(k2)
        for k1 in range(k2, (m - k2) // 2 + 1):
            k0 = m - k1 - k2
            d0, d1 = dist(k0), dist(k1)
            num = sum(d0.get(b, 0) * d1.get(b, 0) * v for b, v in d2.items())
            P = Fraction(num, 2 ** m)
            ntr += 1
            assert k0 >= -(-m // 3)
            if P > c(k0) * c(k1):
                viol += 1
            if m >= 14 and P > Fraction(5, 32):
                viol += 1
            if m not in best or P > best[m][0]:
                best[m] = (P, (k0, k1, k2))
print("  %d triples with 3 <= m <= %d: P <= c_k0 * c_k1 always, and P <= 5/32 for m >= 14: %d violations" % (ntr, TM, viol))
for m in list(range(3, 27)) + [30, 40, 60, 120]:
    P, tr = best[m]
    print("  m = %3d: largest P = %s = %.5f at class sizes %s   (c_ceil(m/3)/2 = %.5f)" % (m, P, float(P), tr, float(c(-(-m // 3)) / 2)))
# with the true maximum at level 3 in place of 5/32
print("\neven m, 14..60: c_m + W_m - 1/4 + (largest P at level 3 for that m):")
for m in range(14, 61, 2):
    v = c(m) + Wm_formula(m) - Fraction(1, 4) + best[m][0]
    assert v < 1
    print("  m = %2d: %.6f" % (m, float(v)))
