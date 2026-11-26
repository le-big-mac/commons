"""A first look (nothing sealed yet rests on this file's output beyond what the sheet says it saw).
The doubling turtle of HAKMEM 45 / the book's GOSPEL: steps at headings a, 2a, 4a, ... (in turns).  For a = 1/q, q odd, the
headings repeat with the order of 2 mod q, and the path is bounded exactly when one round of the cycle sums to nought.
usage: python -I first-look.py QMAX"""
import math, sys, cmath

def order2(q):
    k, x = 1, 2 % q
    while x != 1: x = x * 2 % q; k += 1
    return k

def loop_sum(q, p=1):
    n = order2(q); x = p % q; s = 0j
    for _ in range(n): s += cmath.exp(2j * math.pi * x / q); x = x * 2 % q
    return abs(s), n

def rule(q):
    """the rule to be sealed: some prime l with l^2 | q for which the order of 2 mod q differs from its order mod q/l"""
    m, l = q, 3
    primes = []
    while l * l <= m:
        if m % l == 0:
            e = 0
            while m % l == 0: m //= l; e += 1
            primes.append((l, e))
        l += 2
    if m > 1: primes.append((m, 1))
    return any(e >= 2 and order2(q) != order2(q // l) for l, e in primes), primes

if __name__ == '__main__':
    QMAX = int(sys.argv[1]); bounded = []; disagree = []; hakmem_exc = []
    for q in range(3, QMAX + 1, 2):
        s, n = loop_sum(q); b = s < 1e-9; r, primes = rule(q)
        if b: bounded.append(q)
        if b != r: disagree.append(q)
        sq = any(e >= 2 for l, e in primes)
        if sq and not b: hakmem_exc.append(q)
    print(f"odd q from 3 to {QMAX}: the cycle of 1/q sums to nought for {len(bounded)}; the rule disagrees with the sum for {len(disagree)}: {disagree[:10]}")
    print("bounded:", bounded[:40])
    print(f"q with the square of an odd prime that are NOT bounded ({len(hakmem_exc)}):", hakmem_exc[:40])
