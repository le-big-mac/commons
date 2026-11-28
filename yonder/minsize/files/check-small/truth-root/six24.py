"""The marking of 24 marks on the clock of 6 hours: hour 0 once, hour 1 eight times, hour 3 seven times,
hour 5 eight times.  Count the bad ways of choosing the signs, in two ways that share no code with
evenclocks.py: (A) every one of the 2^24 choices of signs, integers only; (B) signed counts with
binomial weights and exact division of integer polynomials by the cyclotomic polynomials."""
import numpy as np
from math import comb, sqrt
from itertools import product

mult = {0: 1, 1: 8, 3: 7, 5: 8}
m = sum(mult.values())
assert m == 24

# (A) all 2^24 sign choices
N = 1 << m
idx = np.arange(N, dtype=np.uint32)
def popcount(x):
    x = x - ((x >> 1) & 0x55555555)
    x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
    x = (x + (x >> 4)) & 0x0F0F0F0F
    return ((x * 0x01010101) & 0xFFFFFFFF) >> 24
c = np.zeros((6, N), dtype=np.int32)
shift = 0
for h, k in mult.items():
    field = (idx >> shift) & ((1 << k) - 1)
    minus = popcount(field.astype(np.uint32)).astype(np.int32)
    c[h] = k - 2 * minus           # pluses minus minuses at hour h
    shift += k
bad1 = (c.sum(axis=0) == 0)                                     # X - 1
bad2 = ((c[0] - c[1] + c[2] - c[3] + c[4] - c[5]) == 0)         # X + 1
r0, r1, r2 = c[0] + c[3], c[1] + c[4], c[2] + c[5]              # modulo X^3 - 1
bad3 = (r0 == r1) & (r1 == r2)                                  # X^2 + X + 1
e0, e1, e2 = c[0] - c[3], c[1] - c[4], c[2] - c[5]              # modulo X^3 + 1
bad6 = (e0 == e2) & (e1 == -e2)                                 # X^2 - X + 1
bad = bad1 | bad2 | bad3 | bad6
A = int(bad.sum())
print("(A) all", N, "choices: bad", A, " at 1:", int(bad1.sum()), " at 2:", int(bad2.sum()),
      " at 3:", int(bad3.sum()), " at 6:", int(bad6.sum()))

# (B) signed counts, exact polynomial remainders
PHI = {1: [-1, 1], 2: [1, 1], 3: [1, 1, 1], 6: [1, -1, 1]}     # low degree first, monic
def divisible(coef, phi):
    r = list(coef)
    d = len(phi) - 1
    for i in range(len(r) - 1, d - 1, -1):
        q = r[i]
        if q:
            for j in range(d + 1):
                r[i - d + j] -= q * phi[j]
    return all(x == 0 for x in r[:d])
B = 0
hours = sorted(mult)
for ks in product(*[range(mult[h] + 1) for h in hours]):       # ks = number of minuses at each hour
    w = 1
    coef = [0] * 6
    for h, k in zip(hours, ks):
        w *= comb(mult[h], k)
        coef[h] = mult[h] - 2 * k
    if any(divisible(coef, PHI[d]) for d in (1, 2, 3, 6)):
        B += w
print("(B) signed counts: bad", B)
print("share", A / N, " times sqrt(24):", A / N * sqrt(m), " 3.12/sqrt(24) =", 3.12 / sqrt(m))
from fractions import Fraction
print("as a fraction:", Fraction(A, N))
