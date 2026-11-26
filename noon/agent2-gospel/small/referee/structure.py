# structure.py -- for the small sums in small-2e6.txt: does S(m,a) factor as S(m1,a1)*S(m2,a2)
# with m = m1*m2, gcd(m1,m2) = 1 and gcd(ord_m1(2), ord_m2(2)) = 1 ?  (Then <2> mod m is the direct
# product of <2> mod m1 and <2> mod m2, and by the Chinese remainder theorem
# e(a/m) = e(a1/m1) e(a2/m2) with a1 = a * m2^-1 mod m1, a2 = a * m1^-1 mod m2.)
import sys, cmath, math
from itertools import combinations

def ppfactor(m):
    f = []; p = 3
    while p * p <= m:
        if m % p == 0:
            q = 1
            while m % p == 0: m //= p; q *= p
            f.append(q)
        p += 2
    if m > 1: f.append(m)
    return f

def order(m):
    x = 2 % m; n = 1
    while x != 1: x = 2 * x % m; n += 1
    return n

def S(m, a):
    a %= m; x = a; s = 0j; n = 0; selfneg = False
    while True:
        s += cmath.exp(2j * math.pi * x / m)
        if x == (m - a) % m: selfneg = True
        x = 2 * x % m; n += 1
        if x == a: break
    return s, n, selfneg

def canon(m, a):
    """least representative of the pair of cosets {a<2>, -a<2>}"""
    a %= m; x = a; best = min(a, m - a)
    while True:
        x = 2 * x % m
        if x == a: break
        best = min(best, x, m - x)
    return best

def splits(m):
    pp = ppfactor(m); out = []
    for r in range(1, len(pp)):
        for c in combinations(pp, r):
            m1 = 1
            for q in c: m1 *= q
            m2 = m // m1
            if m1 < m2 or len(pp) == 2 and m1 > m2:
                pass
            n1, n2 = order(m1), order(m2)
            if math.gcd(n1, n2) == 1 and m1 < m2: out.append((m1, m2, n1, n2))
    return out

if __name__ == '__main__':
    fn = sys.argv[1]; lim = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-3
    rows = [l.split() for l in open(fn) if not l.startswith('#')]
    nfac = {0: 0, 1: 0}; nprim = {0: 0, 1: 0}; first_prim = {}
    for r in rows:
        ab = float(r[0]); m, a, n, self_ = int(r[3]), int(r[4]), int(r[5]), int(r[6])
        if ab >= lim: break
        sp = splits(m)
        if not sp:
            nprim[self_] += 1
            if self_ not in first_prim: first_prim[self_] = (ab, m, a, n)
            if self_ == 0: print('%.6e m=%d a=%d n=%d self=%d : NO coprime-order splitting; m = %s' % (ab, m, a, n, self_, '*'.join(map(str, ppfactor(m)))))
            continue
        nfac[self_] += 1
        for (m1, m2, n1, n2) in sp:
            a1 = a * pow(m2, -1, m1) % m1; a2 = a * pow(m1, -1, m2) % m2
            s1, k1, sn1 = S(m1, a1); s2, k2, sn2 = S(m2, a2)
            print('%.6e m=%d a=%d n=%d self=%d : m=%d*%d, n=%d*%d ; |S(%d,%d)|=%.6e (self=%d) ; |S(%d,%d)|=%.6e (self=%d) ; product %.6e ; ratio to |S| %.12f'
                  % (ab, m, a, n, self_, m1, m2, n1, n2, m1, canon(m1, a1), abs(s1), sn1, m2, canon(m2, a2), abs(s2), sn2, abs(s1) * abs(s2), abs(s1) * abs(s2) / ab))
    print('below %g: not self-negative: %d factor, %d do not ; self-negative: %d factor, %d do not' % (lim, nfac[0], nprim[0], nfac[1], nprim[1]))
    print('smallest that does not factor: not self-negative %s ; self-negative %s' % (first_prim.get(0), first_prim.get(1)))
