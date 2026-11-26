"""Recompute the smallest sums of small.sealed-run.out with 40-digit arithmetic, and look at the least sum of a pair.
usage: python -I verify.py small.sealed-run.out HOW_MANY > verify.out"""
import sys, re
from math import gcd
from mpmath import mp, mpf, cos, sin, pi, sqrt

def order2(m):
    n, x = 1, 2 % m
    while x != 1: x = x * 2 % m; n += 1
    return n

def coset_sum(m, a):
    """the sum of e(x/m) over x = a 2^k modulo m, as (real part, imaginary part, number of terms, real coset?)"""
    w = 2 * pi / m; x = a; sr = mpf(0); si = mpf(0); n = 0; real = False
    while True:
        sr += cos(x * w); si += sin(x * w); n += 1
        if x == m - a: real = True
        x = x * 2 % m
        if x == a: break
    return sr, si, n, real

def factor(m):
    f, l = [], 3
    while l * l <= m:
        if m % l == 0:
            e = 0
            while m % l == 0: m //= l; e += 1
            f.append((l, e))
        l += 2
    if m > 1: f.append((m, 1))
    return f

def closes(m):
    """Fuchs's rule in his own form: some prime power l^e of m whose order of 2 is divisible by l, and more times than
    the order of 2 modulo any other prime of m"""
    f = factor(m)
    def v(o, l):
        k = 0
        while o % l == 0: o //= l; k += 1
        return k
    for l, e in f:
        k = v(order2(l ** e), l)
        if k >= 1 and all(k > v(order2(r), l) for r, _ in f if r != l): return True
    return False

if __name__ == '__main__':
    mp.dps = 40
    rec = open(sys.argv[1], encoding='utf-8').read(); K = int(sys.argv[2])
    rows = [(float(v), int(m), int(a), int(n), kind) for v, m, a, n, kind in re.findall(r'^\s+([0-9.e+-]+)\s+m = (\d+)\s+a = (\d+)\s+round of (\d+) steps\s+(real|complex)', rec, re.M)]
    print('the %d smallest sums of %s, recomputed with %d-digit arithmetic' % (K, sys.argv[1], mp.dps))
    worst = 0.0; bad = 0
    for v, m, a, n, kind in rows[:K]:
        sr, si, n2, real = coset_sum(m, a); size = sqrt(sr * sr + si * si); d = abs(float(size) - v); worst = max(worst, d)
        ok = n2 == n and real == (kind == 'real') and d < 1e-9 and not closes(m)
        bad += not ok
        print('  m = %-8d a = %-7d n = %-7d %-7s  program %.9e  recomputed %s  differ by %.1e  imaginary part %s  %s%s' % (
            m, a, n, kind, v, mp.nstr(size, 12), d, mp.nstr(abs(si), 3), 'm = ' + ' x '.join('%d^%d' % (l, e) if e > 1 else str(l) for l, e in factor(m)),
            '' if ok else '   <-- DOES NOT AGREE'))
    print('largest difference %.1e; %d of %d do not agree; every one of these m has rounds that do not close by the rule in Fuchs\'s form: %s' % (
        worst, bad, min(K, len(rows)), all(not closes(r[1]) for r in rows[:K])))
    # the least sum of a pair: is it a product?
    pairs = [r for r in rows if r[4] == 'complex']
    print()
    for v, m, a, n, kind in pairs[:5]:
        f = factor(m); found = []
        for mask in range(1, 2 ** len(f) - 1):
            m1 = 1
            for i, (l, e) in enumerate(f):
                if mask >> i & 1: m1 *= l ** e
            m2 = m // m1
            n1, n2 = order2(m1), order2(m2)
            if gcd(n1, n2) != 1: continue
            a1 = a * pow(m2, -1, m1) % m1; a2 = a * pow(m1, -1, m2) % m2
            r1 = coset_sum(m1, a1); r2 = coset_sum(m2, a2)
            s1 = sqrt(r1[0] ** 2 + r1[1] ** 2); s2 = sqrt(r2[0] ** 2 + r2[1] ** 2)
            found.append((m1, m2, n1, n2, r1[3], r2[3], s1, s2))
        print('pair m = %d, a = %d, |S| = %.9e, n = %d: %d ways of writing m = m1 m2 with coprime orders of 2' % (m, a, v, n, len(found)))
        for m1, m2, n1, n2, re1, re2, s1, s2 in found:
            print('    m1 = %d (order %d, %s, |S1| = %s), m2 = %d (order %d, %s, |S2| = %s): product %s, the sum itself %.9e; S1 is real and smaller than the sum: %s' % (
                m1, n1, 'real' if re1 else 'pair', mp.nstr(s1, 10), m2, n2, 'real' if re2 else 'pair', mp.nstr(s2, 10), mp.nstr(s1 * s2, 10), v, bool(re1 and s1 < v)))
