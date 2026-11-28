# Referee's own recomputation of the numbers of result.md (three/), written from the text's definitions.
# Exact rationals / integers.  usage: mybounds.py M
import sys
from fractions import Fraction as Fr
from math import comb
from itertools import combinations

M = int(sys.argv[1]) if len(sys.argv) > 1 else 200

def c(r):
    return Fr(comb(r, r // 2), 2 ** r) if r % 2 == 0 else Fr(0)

# binomial rows as integers: N[r][v] = number of sign vectors of length r with sum v
def cnt(r, v):
    if abs(v) > r or (r + v) % 2:
        return 0
    return comb(r, (r + v) // 2)

def g(r0, r1, r2):
    lo = min(r0, r1, r2)
    tot = 0
    for v in range(1, lo + 1):
        tot += cnt(r0, v) * cnt(r1, v) * cnt(r2, v)
    return Fr(2 * tot, 2 ** (r0 + r1 + r2))

E3 = {1: Fr(0), 2: Fr(0)}
ARG = {}
for m in range(3, M + 1):
    best = None; arg = None
    for r1 in range(1, m // 2 + 1):
        r0 = m - r1
        if r0 in (3, 5) and r1 in (3, 5):
            val = E3[r0] * E3[r1] / 2
        else:
            val = c(r0) * E3[r1] + c(r1) * E3[r0] + E3[r0] * E3[r1]
        if best is None or val > best:
            best, arg = val, (r0, r1)
    for r2 in range(1, m // 3 + 1):
        for r1 in range(r2, (m - r2) // 2 + 1):
            r0 = m - r1 - r2
            val = g(r0, r1, r2) + (c(r0) + E3[r0]) * (c(r1) + E3[r1]) * (c(r2) + E3[r2]) - c(r0) * c(r1) * c(r2)
            if val > best:
                best, arg = val, (r0, r1, r2)
    E3[m] = best; ARG[m] = arg

print('E3(3..16):', [str(E3[m]) for m in range(3, 17)])
print('argmax  :', [ARG[m] for m in range(3, 17)])
print('c+E3 (3..16):', [str(c(m) + E3[m]) for m in range(3, 17)])
okodd = all(E3[m] == Fr(cnt(m - 2, 1), 2 ** (m - 1)) for m in range(5, M + 1, 2))
print('odd m in [5,%d]: E3(m) == P(S_(m-2)=1)/2 :' % M, okodd)
ev = [(E3[m], m) for m in range(6, M + 1, 2)]
print('even m in [6,%d]: largest E3 =' % M, max(ev))
print('all even m <= M: E3 <= 1/16:', all(E3[m] <= Fr(1, 16) for m in range(2, M + 1, 2)))
print('all odd m in [7,M]: E3 <= 5/32:', all(E3[m] <= Fr(5, 32) for m in range(7, M + 1, 2)))
print('all odd m: E3 <= 1/4:', all(E3[m] <= Fr(1, 4) for m in range(1, M + 1, 2)))
print('all r: c+E3 <= 1/2:', all(c(m) + E3[m] <= Fr(1, 2) for m in range(1, M + 1)), ' max c+E3 over r>=1:', max((c(m) + E3[m], m) for m in range(1, M + 1)))
print('even r>=6: c(r) <= 5/16:', all(c(r) <= Fr(5, 16) for r in range(6, M + 1, 2)))
print('even r>=6: E3(r) <= 1/16 and (c,E3) list small r:', [(r, str(c(r)), str(E3[r])) for r in (2, 4, 6, 8, 10)])

# --- W_m(no 3) by direct enumeration of e* (not the product formula)
def primes_upto(N):
    return [p for p in range(2, N + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]

def Wm(m):
    # e* > 1, all prime factors >= 5, mu(e*) = max_q v_q(e*)(q-1) <= m-1.  Enumerate exponent vectors.
    ps = [p for p in primes_upto(m) if p >= 5]
    from collections import Counter
    cntmu = Counter({0: 1})  # mu -> number of e*
    for p in ps:
        new = Counter()
        kmax = (m - 1) // (p - 1)
        for mu, k in cntmu.items():
            for e in range(0, kmax + 1):
                new[max(mu, e * (p - 1))] += k
        cntmu = new
    return sum(Fr(k, 2 ** mu) for mu, k in cntmu.items() if mu > 0)

print('W_m(no 3) for m=5..16:', [str(Wm(m)) for m in range(5, 17)])
WM = Wm(M)
print('W_%d(no 3) = %.12f' % (M, float(WM)))
T7 = {m: c(m) + E3[m] + Wm(m) for m in range(3, M + 1)}
print('Theorem 7 values m=5..20:', [(m, str(T7[m]), round(float(T7[m]), 6)) for m in range(5, 21)])
print('largest over 12<=m<=M:', max((T7[m], m) for m in range(12, M + 1)))
print('largest over odd 13<=m<=M:', max((T7[m], m) for m in range(13, M + 1, 2)))
print('largest over even 14<=m<=M:', max((T7[m], m) for m in range(14, M + 1, 2)))
print('all m in [12,M] below 3/8:', all(T7[m] < Fr(3, 8) for m in range(12, M + 1)))
print('m where Theorem-7 value >= 3/8 (3<=m<=M):', [m for m in range(3, M + 1) if T7[m] >= Fr(3, 8)])

# --- Proposition 5 / Theorem 6
def parts(total, k, mx=None):
    if mx is None: mx = total
    if k == 0:
        if total == 0: yield ()
        return
    for f in range(min(mx, total - k + 1), 0, -1):
        if f * k < total: break
        for rest in parts(total - f, k - 1, f):
            yield (f,) + rest

BB = {1: Fr(0), 2: Fr(1, 2)}

def pairings(idx, npairs):
    # all ways to choose npairs disjoint pairs from idx
    if npairs == 0:
        yield []
        return
    if len(idx) < 2 * npairs:
        return
    a = idx[0]
    # a unpaired
    for p in pairings(idx[1:], npairs):
        yield p
    for j in range(1, len(idx)):
        b = idx[j]
        rest = idx[1:j] + idx[j + 1:]
        for p in pairings(rest, npairs - 1):
            yield [(a, b)] + p

def phi(sizes, R, q):
    k = sum(1 for r in sizes if r == 1)
    if k >= 1:
        v = Fr(1, 2 ** (k - 1))
        for r in sizes:
            if r >= 2: v *= BB[r + 1]
        return v
    best = None
    for p in pairings(list(range(q)), q // 2):
        v = Fr(1)
        for (a, b) in p: v *= BB[sizes[a] + sizes[b]]
        if best is None or v < best: best = v
    sz = tuple(sorted(sizes, reverse=True))
    if q == 5:
        if sz == (2, 2, 2, 2, 2):
            if R == 0: return Fr(2, 1024)
            if R >= 2: return Fr(34, 1024)
        if sz == (4, 2, 2, 2, 2) and R == 0:
            return Fr(2, 1024) + (BB[6] - c(6)) / 8
        if sz == (3, 3, 2, 2, 2):
            return min(best, BB[5] ** 2 / 2)
    return best

def omega(R):
    return Fr(1) if R == 0 else (Fr(0) if R == 1 else Fr(1, 2))

PSI = {}
PSIARG = {}
def psi(q, m):
    best = Fr(0); arg = None
    for R in range(0, m - q + 1):
        for sizes in parts(m - R, q):
            v = phi(sizes, R, q) * omega(R)
            if v > best: best, arg = v, (sizes, R)
    PSI[(q, m)] = best; PSIARG[(q, m)] = arg
    return best

BB61 = {}
for m in range(3, 13):
    tot = c(m) + E3[m]; tot1 = c(m) + E3[m]
    desc = []
    for q in [p for p in primes_upto(m) if p >= 5]:
        ps = psi(q, m)
        tot += ((m - 1) // (q - 1)) * ps
        tot1 += ps
        desc.append('q=%d: %d x %s at %s' % (q, (m - 1) // (q - 1), ps, PSIARG[(q, m)]))
    BB[m] = tot; BB61[m] = tot1
    print('BB(%d) = %s + %s + [%s] = %s  %s   one-level-per-prime: %s' % (m, c(m), E3[m], '; '.join(desc), tot, '<=3/8' if tot <= Fr(3, 8) else 'ABOVE 3/8', tot1))
print('hypothesis BB(r) <= 1/2 for r < 12:', all(BB[r] <= Fr(1, 2) for r in range(1, 13)))
# full table of level bounds for m = 8 (used in the proof of beta(8))
for m in (6, 8):
    for q in (5, 7):
        for R in range(0, m - q + 1):
            for sizes in parts(m - R, q):
                print('   m=%d q=%d sizes=%s R=%d  lambda=%s' % (m, q, sizes, R, phi(sizes, R, q) * omega(R)))
