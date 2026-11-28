from math import comb, sqrt
from fractions import Fraction as F
from itertools import product
def C(m): return comb(m, m // 2)
# thresholds: first m with 2*d*C(m) < 2^m, and whether it holds for all larger m up to 400
for d in (1, 2, 3, 4, 6, 8):
    ok = [m for m in range(0, 401) if 2 * d * C(m) < 2 ** m]
    first = ok[0]
    print("d(n') =", d, "first m with bound < 2^m:", first, "; holds for every m from there to 400:", ok == list(range(first, 401)))
# same without the factor 2 (the bound d(n) * C for odd n)
for d in (2, 4):
    ok = [m for m in range(0, 401) if d * C(m) < 2 ** m]
    print("without the factor 2, d =", d, "first m:", ok[0])
# c_m
c = lambda m: F(C(m), 2 ** m)
print("c_m, m=0..8:", [str(c(m)) for m in range(9)])
print("max c_m for 3 <= m <= 2000:", max(c(m) for m in range(3, 2001)), "attained at", [m for m in range(3, 60) if c(m) == F(3, 8)])
print("c_m nonincreasing to 2000:", all(c(m + 1) <= c(m) for m in range(0, 2000)))
worst = max((2 * float(c(m)) * sqrt(m), m) for m in range(1, 200001, 1) if m < 3000 or m % 997 == 0)
print("max of 2 c_m sqrt(m) over tested m:", worst, " 2*sqrt(2/pi) =", 2 * sqrt(2 / 3.141592653589793))
print("1 - 2 c_m for m = 2..8:", [str(1 - 2 * c(m)) for m in range(2, 9)])
# {0,0,0,1} on Z_2: signings bad at 1 or at 2
e = [0, 0, 0, 1]
bad1 = bad2 = bad = 0
for s in product((1, -1), repeat=4):
    b1 = sum(s) == 0
    b2 = sum(si * (-1) ** ei for si, ei in zip(s, e)) == 0
    bad1 += b1; bad2 += b2; bad += (b1 or b2)
print("{0,0,0,1} on Z_2: bad at 1:", bad1, "bad at 2:", bad2, "bad:", bad, "of 16; good share", F(16 - bad, 16))
# 3.12/sqrt(m) vs 2 c_m (statement 4's conclusion on every Z_n) and 1/4 for m>=3
print("2 c_m <= 3.12/sqrt(m) for 1<=m<=3000:", all(2 * float(c(m)) <= 3.12 / sqrt(m) for m in range(1, 3001)))
print("1 - 2 c_m >= 1/4 for 3<=m<=3000:", all(1 - 2 * c(m) >= F(1, 4) for m in range(3, 3001)), "; equality at", [m for m in range(3, 200) if 1 - 2 * c(m) == F(1, 4)])
print("odd m, 1/2: trivial (no bad signing). even m=4: beta(4)=3/8 in the page vs n'=1 share c_4 =", c(4))
