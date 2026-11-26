# meansq.py -- for odd m <= N with real cosets and rounds that do not close: is the mean square of the coset
# sums, (n/k) * sum over d | m of d mu(m/d) / ord_d(2), below n?  Counted for all such m, primes and others apart.
# Also: the least non-zero |S| among rounds of at most 10 steps (from all-6001.txt, every coset for m <= 6001).
import sys
from math import gcd
from fractions import Fraction

def order(m):
    if m == 1: return 1
    x = 2 % m; n = 1
    while x != 1: x = 2 * x % m; n += 1
    return n

def factor(m):
    f = {}; p = 3
    while p * p <= m:
        while m % p == 0: f[p] = f.get(p, 0) + 1; m //= p
        p += 2
    if m > 1: f[m] = f.get(m, 0) + 1
    return f

def divisors(f):
    ds = [1]
    for p, e in f.items(): ds = [d * p ** i for d in ds for i in range(e + 1)]
    return ds

def mu(k):
    f = factor(k)
    return 0 if any(e > 1 for e in f.values()) else (-1) ** len(f)

if __name__ == '__main__':
    N = int(sys.argv[1])
    tot = pr = comp = comp_less = pr_less = eq = 0
    for m in range(3, N + 1, 2):
        f = factor(m); rad = 1
        for p in f: rad *= p
        n = order(m)
        if order(rad) != n: continue                       # rounds close
        if pow(2, n // 2, m) != m - 1 or n % 2: continue   # -1 not a power of 2: no real cosets
        phi = m
        for p in f: phi = phi // p * (p - 1)
        k = phi // n
        ms = Fraction(n, k) * sum(Fraction(d * mu(m // d), order(d)) for d in divisors(f))
        tot += 1
        isp = (len(f) == 1 and list(f.values())[0] == 1)
        if isp: pr += 1; pr_less += ms < n
        else: comp += 1; comp_less += ms < n
        eq += ms == n
    print('odd m <= %d with real cosets whose rounds do not close: %d ; primes %d (mean square below n: %d) ; others %d (mean square below n: %d) ; equal to n: %d' % (N, tot, pr, pr_less, comp, comp_less, eq))
    rows = [l.split() for l in open('/home/agent2/gospel/small-referee/all-6001.txt') if not l.startswith('#')]
    short = [(float(r[0]), int(r[3]), int(r[4]), int(r[5])) for r in rows if int(r[5]) <= 10]
    short.sort()
    print('rounds of at most 10 steps (m <= 6001, so every m dividing 2^n - 1, n <= 10): %d cosets ; the three least non-zero |S|: %s' % (len(short), short[:3]))
