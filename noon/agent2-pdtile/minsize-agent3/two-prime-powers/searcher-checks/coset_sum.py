"""SEALED helper.  Sum of cosets x_c + c Z_M, one for each maximal non-member c of an up-set, with the shifts of
the sealed file (p-coordinate p^j for the j-th corner, q-coordinate 0), for M = p^n q^m.  Prints whether it is
a set and whether its exact pattern is the up-set D = {d | M : d divides no corner}.
usage: python -I coset_sum.py p n q m  c0 c1 ...   (corners in increasing order of their exponent of p)"""
import sys
from math import gcd
p, n, q, m = (int(x) for x in sys.argv[1:5]); C = [int(x) for x in sys.argv[5:]]
M = p ** n * q ** m
def cyclotomic(k, cache={}):
    if k in cache: return cache[k]
    num = [-1] + [0] * (k - 1) + [1]
    for d in range(1, k):
        if k % d == 0:
            den = cyclotomic(d); qq = [0] * (len(num) - len(den) + 1); num = num[:]
            for i in range(len(qq) - 1, -1, -1):
                qq[i] = num[i + len(den) - 1]
                for j, c in enumerate(den): num[i + j] -= qq[i] * c
            assert not any(num); num = qq
    cache[k] = num; return num
def divides(phi, a):
    a = a[:]; deg = len(phi) - 1
    for i in range(len(a) - 1, deg - 1, -1):
        c = a[i]
        if c:
            for j in range(deg + 1): a[i - deg + j] -= c * phi[j]
    return not any(a)
for mode in ('all shifts 0', 'shifts p^j'):
    A = [0] * M
    for j, c in enumerate(C):
        assert M % c == 0
        x = 0
        if mode != 'all shifts 0':
            x = next(t for t in range(M) if t % p ** n == (p ** j) % p ** n and t % q ** m == 0)
        for k in range(M // c): A[(x + c * k) % M] += 1
    divs = [d for d in range(2, M + 1) if M % d == 0]
    D = [d for d in divs if all(c % d for c in C)]
    pat = [d for d in divs if divides(cyclotomic(d), A)]
    print(f'M = {M}, corners {C}, gcd {gcd(*C)}, {mode}: size {sum(A)} = sum of M/c {sum(M // c for c in C)}; '
          f'is a set: {max(A) <= 1}; pattern equals D: {pat == D}')
