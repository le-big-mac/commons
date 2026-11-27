from math import comb
spec = {12: 11, 24: 8, 36: 7, 60: 6, 84: 4, 120: 4, 180: 4, 360: 3}
tot = 0
for n, mm in spec.items():
    s = sum(comb(n + m - 2, m - 1) for m in range(3, mm + 1))
    print(n, mm, s)
    tot += s
print("total", tot, "clocks", len(spec), "all divisible by 12:", all(n % 12 == 0 for n in spec))
# p_m: chance that m coin signs add up to a multiple of 3
from fractions import Fraction
from itertools import product
for m in range(1, 13):
    c = sum(1 for s in product((1, -1), repeat=m) if sum(s) % 3 == 0)
    print(m, Fraction(c, 2 ** m), float(Fraction(c, 2 ** m)))
print(2 * Fraction(11, 32) + 2 * Fraction(118569, 1000000), float(2 * Fraction(11, 32) + 2 * 0.118569))
