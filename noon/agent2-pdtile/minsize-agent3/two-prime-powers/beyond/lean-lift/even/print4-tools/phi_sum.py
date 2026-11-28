# usage: python3 -I phi_sum.py LIMIT
# My own arithmetic (reads no download): the sum of 2^(-phi(d)) over odd d from 3 to LIMIT, an upper bound
# (up to a tail) for the union bound "sum over divisors m > 1 of n of 2^(-phi(m))" for every odd n.
import sys
from fractions import Fraction
L = int(sys.argv[1])
phi = list(range(L + 1))
for p in range(2, L + 1):
    if phi[p] == p:
        for k in range(p, L + 1, p):
            phi[k] -= phi[k] // p
s = Fraction(0)
for d in range(3, L + 1, 2):
    s += Fraction(1, 2 ** phi[d])
    if d in (3, 5, 7, 9, 15, 45, 105, 1001):
        print("  up to d =", d, ":", float(s))
print("sum over odd d in [3, %d]: %.12f" % (L, float(s)), "| below 3/8:", s < Fraction(3, 8))
print("smallest phi(d) for odd d in (%d, %d]:" % (L // 2, L), min(phi[d] for d in range(L // 2 + 1, L + 1) if d % 2))
