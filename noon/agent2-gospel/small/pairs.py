"""Every sum of a pair in the list of the smallest sums: is it a product of a real sum for a smaller modulus and another sum,
the orders of 2 modulo the two factors being coprime?   usage: python -I pairs.py small.sealed-run.out > pairs.out"""
import sys, re, math
from math import gcd

def order2(m):
    n, x = 1, 2 % m
    while x != 1: x = x * 2 % m; n += 1
    return n

def coset(m, a):
    xs = []; x = a % m
    while True:
        xs.append(x); x = x * 2 % m
        if x == a % m: break
    sr = math.fsum(math.cos(2 * math.pi * x / m) for x in xs); si = math.fsum(math.sin(2 * math.pi * x / m) for x in xs)
    return math.hypot(sr, si), (m - a % m) % m in xs

def factor(m):
    f, l = [], 3
    while l * l <= m:
        if m % l == 0:
            e = 0
            while m % l == 0: m //= l; e += 1
            f.append(l ** e)
        l += 2
    if m > 1: f.append(m)
    return f

if __name__ == '__main__':
    rec = open(sys.argv[1], encoding='utf-8').read()
    rows = [(float(v), int(m), int(a), int(n), k) for v, m, a, n, k in re.findall(r'^\s+([0-9.e+-]+)\s+m = (\d+)\s+a = (\d+)\s+round of (\d+) steps\s+(real|complex)', rec, re.M)]
    pairs = [r for r in rows if r[4] == 'complex']; yes = 0; no = []; worst = 0.0; reals = {}; reals3 = set()
    for v, m, a, n, _ in pairs:
        f = factor(m); found = None
        for mask in range(1, 2 ** len(f) - 1):
            m1 = math.prod(f[i] for i in range(len(f)) if mask >> i & 1); m2 = m // m1
            if gcd(order2(m1), order2(m2)) != 1: continue
            a1 = a * pow(m2, -1, m1) % m1; a2 = a * pow(m1, -1, m2) % m2
            s1, real1 = coset(m1, a1); s2, real2 = coset(m2, a2)
            if real1 and abs(s1 * s2 / v - 1) < 1e-6: found = (m1, a1, s1, m2, s2); break
        if found:
            yes += 1; worst = max(worst, abs(found[2] * found[4] / v - 1)); reals.setdefault((found[0], round(found[2], 12)), 0); reals[(found[0], round(found[2], 12))] += 1
            if v < 1e-3: reals3.add((found[0], round(found[2], 12)))
        else: no.append((v, m, a))
        print('  %.6e  m = %-8d %s' % (v, m, ('= %d x %d: the real sum %.6e for %d, times %.6f' % (found[0], found[3], found[2], found[0], found[4])) if found else 'NOT such a product'))
    print('%d sums of pairs among the %d smallest sums (the largest of which is %.4e): %d are a real sum for a smaller modulus times another sum, with coprime orders; %d are not%s; largest relative difference of product and sum %.1e'
          % (len(pairs), len(rows), rows[-1][0], yes, len(no), (': ' + ', '.join('%.4e at m = %d' % (v, m) for v, m, a in no)) if no else '', worst))
    print('the real sums that the %d come from: %d different ones; of the %d that fall below 1e-3, the real sums they come from: %d different ones' % (len(pairs), len(reals), sum(1 for r in pairs if r[0] < 1e-3), len(reals3)))
