# The upper bounds of result.md, exact rationals.
#   c(m)      P(the signs add up to 0)
#   E3[m]     bound for "bad at some 3^i, i >= 1, and not at 1" on powers of 3 (Proposition 3; with the remark for (3,3))
#   PSI(q,m)  bound for one live level of a prime q >= 5 (Proposition 5)
#   BB[m]     = c(m) + E3[m] + sum over primes 5 <= q <= m of floor((m-1)/(q-1)) * PSI(q,m)   (Theorem 6)
# usage: bounds.py M
import sys
from fractions import Fraction as F
from math import comb
from functools import lru_cache
from itertools import combinations

def c(r):
    return F(comb(r, r // 2), 2 ** r) if r % 2 == 0 else F(0)

def pv(r, v):
    if (r + v) % 2 or abs(v) > r:
        return F(0)
    return F(comb(r, (r + v) // 2), 2 ** r)

@lru_cache(None)
def g3(r0, r1, r2):
    r = min(r0, r1, r2)
    return 2 * sum(pv(r0, v) * pv(r1, v) * pv(r2, v) for v in range(1, r + 1))

E3 = {0: F(0), 1: F(0), 2: F(0)}
ARG3 = {}
REFINE33 = True

def two_class(r0, r1):
    if REFINE33 and r0 in (3, 5) and r1 in (3, 5):
        # Remark 3.2: on the event X of a multiset of 3 or 5 elements the signs add up to +3 or -3; half of X x X is bad at 1
        return E3[r0] * E3[r1] / 2
    return c(r0) * E3[r1] + c(r1) * E3[r0] + E3[r0] * E3[r1]

def three_class(r0, r1, r2):
    return g3(*sorted((r0, r1, r2), reverse=True)) + (c(r0) + E3[r0]) * (c(r1) + E3[r1]) * (c(r2) + E3[r2]) \
        - c(r0) * c(r1) * c(r2)

def build3(M):
    for m in range(3, M + 1):
        if m in E3:
            continue
        best = F(-1); arg = None
        for r1 in range(1, m // 2 + 1):
            val = two_class(m - r1, r1)
            if val > best:
                best, arg = val, (m - r1, r1)
        for r2 in range(1, m // 3 + 1):
            for r1 in range(r2, (m - r2) // 2 + 1):
                r0 = m - r1 - r2
                val = three_class(r0, r1, r2)
                if val > best:
                    best, arg = val, (r0, r1, r2)
        E3[m] = best; ARG3[m] = arg

def primes_from5(m):
    return [q for q in range(5, m + 1) if all(q % p for p in range(2, int(q ** 0.5) + 1))]

def partitions(total, parts, maxpart=None):
    """partitions of total into exactly `parts` parts >= 1, nonincreasing"""
    if maxpart is None:
        maxpart = total
    if parts == 0:
        if total == 0:
            yield ()
        return
    for first in range(min(maxpart, total - (parts - 1)), 0, -1):
        if first * parts < total:
            break
        for rest in partitions(total - first, parts - 1, first):
            yield (first,) + rest

BB = {1: F(0), 2: F(1, 2)}
PSIARG = {}

def best_pairing(sizes):
    # minimum over perfect-but-one pairings of prod BB[ru + rt]  (sizes all >= 2, an odd number of them)
    sizes = list(sizes)
    @lru_cache(None)
    def rec(rem):
        rem = list(rem)
        if len(rem) <= 1:
            return F(1)
        best = None
        # either leave rem[0] out (only if odd count) or pair it
        if len(rem) % 2 == 1:
            best = rec(tuple(rem[1:]))
        for j in range(1, len(rem)):
            v = BB[rem[0] + rem[j]] * rec(tuple(rem[1:j] + rem[j + 1:]))
            if best is None or v < best:
                best = v
        return best
    return rec(tuple(sizes))

def phi_group(sizes, R):
    """bound for: exists x such that the full group with these subclass sizes is flat at x (Lemma G), R elements outside"""
    k = sum(1 for r in sizes if r == 1)
    q = len(sizes)
    if k >= 1:
        val = F(1, 2 ** (k - 1))
        for r in sizes:
            if r >= 2:
                val *= BB[r + 1]
        return val
    if q == 5 and all(r == 2 for r in sizes):
        return F(2, 1024) if R == 0 else F(34, 1024)      # beyond "bad at 1" when R = 0
    sz = tuple(sorted(sizes, reverse=True))
    if sz == (4, 2, 2, 2, 2) and R == 0:
        # Proposition 5, case S1 (beyond "bad at 1"): five equal nonzero sums, or an "extra" bad signing of six elements
        return F(2, 1024) + (BB[6] - c(6)) / 8
    if sz == (3, 3, 2, 2, 2):
        # Proposition 5, case S2: two bad signings of five elements and one equality of sums of two pairs
        return min(best_pairing(tuple(sizes)), BB[5] * BB[5] / 2)
    return best_pairing(tuple(sizes))

def beyond1(sizes, R):
    """structures for which the level bound is a bound for the part of the event outside "bad at 1" only"""
    sz = tuple(sorted(sizes, reverse=True))
    return R == 0 and sz in ((2, 2, 2, 2, 2), (4, 2, 2, 2, 2))

def omega(R):
    return F(1) if R == 0 else (F(0) if R == 1 else F(1, 2))

def level_bound(sizes, R):
    return phi_group(sizes, R) * omega(R)

def psi(q, m):
    best = F(0); arg = None
    for gsz in range(q, m + 1):
        R = m - gsz
        if R == 1:
            continue
        for sizes in partitions(gsz, q):
            v = level_bound(sizes, R)
            if v > best:
                best, arg = v, (sizes, R)
    PSIARG[(q, m)] = arg
    return best

def build(M):
    build3(M)
    for m in range(3, M + 1):
        tot = c(m) + E3[m]
        for q in primes_from5(m):
            tot += ((m - 1) // (q - 1)) * psi(q, m)
        BB[m] = tot

if __name__ == '__main__':
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    build(M)
    print('m | c(m) | E3(m) [argmax] | per prime q>=5: levels x PSI [argmax] | BB(m) | BB(m) <= 3/8 ?')
    for m in range(3, M + 1):
        parts = []
        for q in primes_from5(m):
            parts.append(f'q={q}: {(m - 1) // (q - 1)} x {psi(q, m)} {PSIARG[(q, m)]}')
        print(m, '|', c(m), '|', E3[m], ARG3[m], '|', '; '.join(parts), '|', BB[m], f'= {float(BB[m]):.6f}', '|',
              'yes' if BB[m] <= F(3, 8) else 'NO')
