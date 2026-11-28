from fractions import Fraction as F
from math import comb, sqrt, pi

def c(r):
    return F(comb(r, r // 2), 2 ** r)

print("--- the four figures")
for m in (100, 10000):
    print(m, "good at least", 1 - 3.12 / sqrt(m))
for m in (101, 10001):
    print(m, "good more than", 1 - 2 / sqrt(m))

print("--- thresholds: odd m, new (1-2/sqrt m) against 1/2")
for m in range(9, 26, 2):
    print(m, round(1 - 2 / sqrt(m), 5), "more than half" if 1 - 2 / sqrt(m) > 0.5 else "not more")
print("--- thresholds: even m, new (1-3.12/sqrt m) against 1/4 and against 17/64 =", 17 / 64)
for m in range(10, 27, 2):
    v = 1 - 3.12 / sqrt(m)
    print(m, round(v, 6), "> 1/4" if v > 0.25 else "<= 1/4", "> 17/64" if v > 17 / 64 else "<= 17/64")
print("exact: 3.12^2 = %.4f; (3/4)^2*m at 16,18: %.4f %.4f; (47/64)^2*m at 18,20: %.4f %.4f" % (
    3.12 ** 2, 0.5625 * 16, 0.5625 * 18, (47 / 64) ** 2 * 18, (47 / 64) ** 2 * 20))

print("--- where the bounds say anything at all (bound < 1)")
print("3.12/sqrt(m) < 1 from m =", min(m for m in range(1, 100) if 3.12 / sqrt(m) < 1))
print("2/sqrt(m) < 1 from odd m =", min(m for m in range(1, 100, 2) if 2 / sqrt(m) < 1))

print("--- all marks on one hour: c_m * sqrt(m), even m")
for m in (2, 4, 10, 20, 100, 1000, 10000):
    print(m, float(c(m)) * sqrt(m))
print("sqrt(2/pi) =", sqrt(2 / pi))

print("--- odd m, (m-2,1,1) mod 3: c_(m-2)/2 * sqrt(m)")
for m in (3, 5, 11, 101, 1001):
    print(m, float(c(m - 2) / 2) * sqrt(m))

print("--- 760 in 1,000 (odd marks, clocks without a factor 3) against 1 - 2/sqrt(m)")
for m in range(61, 76, 2):
    print(m, round(1 - 2 / sqrt(m), 5), "more than 0.76" if 1 - 2 / sqrt(m) > 0.76 else "less")

print("--- section 17 exact values times sqrt(m), even m <= 8, against 1")
for m, b in ((2, F(1, 2)), (4, F(3, 8)), (6, F(11, 32)), (8, F(39, 128))):
    print(m, float(b) * sqrt(m))
print("--- constants")
print("2*2.893 =", 2 * 2.893, " 2*1.56 =", 2 * 1.56, " 2*1.5529 =", 2 * 1.5529)
print("K*sqrt(2/pi) =", 78764625 / 67108864 * sqrt(2 / pi))
print("Miller's limit 2*sqrt(2)/sqrt(pi) =", 2 * sqrt(2) / sqrt(pi))
print("--- with the sharper 1.5529: good at 18 marks at least", 1 - 2 * 1.5529 / sqrt(18))
