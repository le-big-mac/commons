# Referee, second look: what the recursion for E3 gives with the exception for sizes {3,5} (the text's definition)
# and with {3,5,7} (Remark 3.3, not adopted by the text).  My own code, exact fractions.  usage: seven_rec.py M
import sys
from fractions import Fraction as Fr
from math import comb
M = int(sys.argv[1]) if len(sys.argv) > 1 else 200
def c(r): return Fr(comb(r, r // 2), 2 ** r) if r % 2 == 0 else Fr(0)
def cnt(r, v): return 0 if (abs(v) > r or (r + v) % 2) else comb(r, (r + v) // 2)
_g = {}
def g(r0, r1, r2):
    key = (r0, r1, r2)
    if key not in _g:
        _g[key] = Fr(2 * sum(cnt(r0, v) * cnt(r1, v) * cnt(r2, v) for v in range(1, min(key) + 1)), 2 ** (r0 + r1 + r2))
    return _g[key]
def rec(exc):
    E = {1: Fr(0), 2: Fr(0)}; terms10 = []
    for m in range(3, M + 1):
        best = None
        for r1 in range(1, m // 2 + 1):
            r0 = m - r1
            val = E[r0] * E[r1] / 2 if (r0 in exc and r1 in exc) else c(r0) * E[r1] + c(r1) * E[r0] + E[r0] * E[r1]
            if m == 10: terms10.append(((r0, r1), val))
            if best is None or val > best: best = val
        for r2 in range(1, m // 3 + 1):
            for r1 in range(r2, (m - r2) // 2 + 1):
                r0 = m - r1 - r2
                val = g(r0, r1, r2) + (c(r0) + E[r0]) * (c(r1) + E[r1]) * (c(r2) + E[r2]) - c(r0) * c(r1) * c(r2)
                if m == 10: terms10.append(((r0, r1, r2), val))
                if val > best: best = val
        E[m] = best
    return E, terms10
E5, t5 = rec((3, 5)); E7, t7 = rec((3, 5, 7))
print('terms for m = 10 with the exception {3,5,7}: %d terms: %s' % (len(t7), ', '.join('%s: %s' % (k, v) for k, v in t7)))
print('largest: %s ; with {3,5} the term (7,3) is %s and the largest %s' % (max(v for k, v in t7), dict(t5)[(7, 3)], max(v for k, v in t5)))
diff = [m for m in range(3, M + 1) if E5[m] != E7[m]]
print('sizes m <= %d where the two recursions differ (%d of them): %s' % (M, len(diff), diff))
print('all odd among them: %s ; E7 <= E5 everywhere: %s ; largest difference: %s at m=%d' % ([m for m in diff if m % 2], all(E7[m] <= E5[m] for m in E5), max((E5[m] - E7[m], m) for m in diff)[0], max((E5[m] - E7[m], m) for m in diff)[1]))
print('first differences:', [(m, str(E5[m]), str(E7[m])) for m in diff[:6]])
print('even m in [22,%d] where they do NOT differ: %s' % (M, [m for m in range(22, M + 1, 2) if m not in diff]))
print('m = 12..21 unchanged: %s ; E7(10) = %s ; c(10)+E7(10) = %s' % (all(E5[m] == E7[m] for m in range(11, 22)), E7[10], c(10) + E7[10]))
print('largest E for even m: with {3,5}: %s ; with {3,5,7}: %s' % (max((E5[m], m) for m in range(6, M + 1, 2)), max((E7[m], m) for m in range(6, M + 1, 2))))
# W_m(no 3) by direct enumeration
def primes_upto(N): return [p for p in range(2, N + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]
def Wm(m):
    from collections import Counter
    cm = Counter({0: 1})
    for p in [p for p in primes_upto(m) if p >= 5]:
        new = Counter()
        for mu, k in cm.items():
            for e in range(0, (m - 1) // (p - 1) + 1): new[max(mu, e * (p - 1))] += k
        cm = new
    return sum(Fr(k, 2 ** mu) for mu, k in cm.items() if mu > 0)
T5 = {m: c(m) + E5[m] + Wm(m) for m in range(3, M + 1)}
print('Theorem 7 bound (the text\'s E3) for m = 3..12: %s' % [(m, str(T5[m])) for m in range(3, 13)])
print('  at most 377/1024 for all 12 <= m <= %d: %s ; below 3/8 for all odd 5 <= m <= %d: %s ; m <= %d with value >= 3/8: %s' % (M, all(T5[m] <= Fr(377, 1024) for m in range(12, M + 1)), M, all(T5[m] < Fr(3, 8) for m in range(5, M + 1, 2)), M, [(m, str(T5[m])) for m in range(3, M + 1) if T5[m] >= Fr(3, 8)]))
T7 = {m: c(m) + E7[m] + Wm(m) for m in range(3, M + 1)}
print('  with {3,5,7}: largest for m >= 12: %s (the text\'s: %s) ; m in [12,21] unchanged: %s' % (max((T7[m], m) for m in range(12, M + 1)), max((T5[m], m) for m in range(12, M + 1)), all(T5[m] == T7[m] for m in range(11, 22))))
print('ten elements: the text\'s BB(10) = 91/256 and Remark 6.1 bound 83/256 contain E3(10) once; with 19/512 they would be %s and %s' % (Fr(91, 256) - E5[10] + E7[10], Fr(83, 256) - E5[10] + E7[10]))
