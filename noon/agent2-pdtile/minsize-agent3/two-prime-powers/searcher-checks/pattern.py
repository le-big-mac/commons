"""SEALED helper.  Exact cyclotomic pattern of a multiset on Z_M (integer arithmetic).
usage: python -I pattern.py M x1 x2 ...   (elements, repeated for multiplicity)"""
import sys
def cyclotomic(n, cache={}):
    if n in cache: return cache[n]
    num = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if n % d == 0:
            den = cyclotomic(d); q = [0] * (len(num) - len(den) + 1); num = num[:]
            for i in range(len(q) - 1, -1, -1):
                q[i] = num[i + len(den) - 1]
                for j, c in enumerate(den): num[i + j] -= q[i] * c
            assert not any(num); num = q
    cache[n] = num; return num
def divides(phi, a):
    a = a[:]; deg = len(phi) - 1
    for i in range(len(a) - 1, deg - 1, -1):
        c = a[i]
        if c:
            for j in range(deg + 1): a[i - deg + j] -= c * phi[j]
    return not any(a)
M = int(sys.argv[1]); A = [0] * M
for x in sys.argv[2:]: A[int(x) % M] += 1
print('M =', M, '| size', sum(A), '| pattern', [d for d in range(2, M + 1) if M % d == 0 and divides(cyclotomic(d), A)])
