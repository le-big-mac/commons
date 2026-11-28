# Every number used in result.md, by exact rationals.
import sys
from fractions import Fraction as F
from math import comb
import bounds
from bounds import c, E3, BB
from badlib import bad_share

M = int(sys.argv[1]) if len(sys.argv) > 1 else 200
bounds.build3(M)

def p1(r):            # P(S_r = 1), r odd
    return F(comb(r, (r + 1) // 2), 2 ** r)

print('--- Proposition 3: the recursion for powers of 3, m <= %d' % M)
assert E3[1] == E3[2] == E3[4] == 0 and E3[3] == F(1, 4) and E3[5] == F(3, 16) and E3[6] == F(1, 32)
assert all(E3[m] == p1(m - 2) / 2 for m in range(5, M + 1, 2))
print('odd m in [5,%d]: E3(m) = P(S_(m-2) = 1)/2 exactly (attained by the classes (m-2,1,1) modulo 3): True' % M)
assert all(E3[m] <= F(5, 32) for m in range(7, M + 1, 2))
ev = max((E3[m], m) for m in range(6, M + 1, 2))
print('even m in [6,%d]: largest E3(m) = %s = %.6f at m = %d;  <= 1/16: %s' % (M, ev[0], float(ev[0]), ev[1], ev[0] <= F(1, 16)))
assert ev[0] <= F(1, 16)
print('first values E3(3..16):', [str(E3[m]) for m in range(3, 17)])
print('c(m)+E3(m), m = 3..16:', [str(c(m) + E3[m]) for m in range(3, 17)])

print('--- tail constants')
print('c(68) = %.6f (< 0.097);  P(S_67 = 1) = %.6f (< 0.1);  (3/8)^3 - (5/16)^3 = %.6f;  (1/2)((3/8)^2-(5/16)^2) = %.6f'
      % (float(c(68)), float(p1(67)), float(F(3, 8) ** 3 - F(5, 16) ** 3), float((F(3, 8) ** 2 - F(5, 16) ** 2) / 2)))
assert c(68) < F(97, 1000) and p1(67) < F(1, 10)
assert all(F(comb(r, r // 2 + 1), 2 ** r) <= F(1, 4) for r in range(2, 400, 2))      # P(S_r = 2) <= 1/4, r even
assert all(c(r) <= F(5, 16) for r in range(6, 400, 2))

print('--- W_m(no 3) = sum of 2^(-mu(e)) over e > 1 with prime factors >= 5 and mu(e) <= m - 1')
def primes_upto(n):
    return [q for q in range(5, n + 1) if all(q % p for p in range(2, int(q ** 0.5) + 1))]
def A(t):
    r = 1
    for p in primes_upto(t + 1):
        r *= 1 + t // (p - 1)
    return r
def W(m):
    s = F(0)
    for t in range(4, m, 2):
        s += F(A(t) - A(t - 2), 2 ** t)
    return s
assert W(7) == W(8) == F(3, 32) and W(9) == W(10) == F(13, 128) and W(11) == W(12) == F(55, 512)
print('W_8, W_10, W_12, W_14, W_16 =', W(8), W(10), W(12), W(14), W(16), ' W_%d = %.9f (< 0.118569)' % (M, float(W(M))))
assert W(M) < F(118569, 1000000)

print('--- Theorem 7: m >= 12, bound c(m) + E3(m) + W_m(no 3)')
worst = None
for m in range(12, M + 1):
    tot = c(m) + E3[m] + W(m)
    assert tot <= F(3, 8), m
    if worst is None or tot > worst[0]:
        worst = (tot, m)
    if m <= 20:
        print('  m=%d: %s + %s + %s = %s = %.6f' % (m, c(m), E3[m], W(m), tot, float(tot)))
print('largest value for 12 <= m <= %d: %s = %.6f at m = %d (3/8 = 0.375)' % (M, worst[0], float(worst[0]), worst[1]))
wo = max((c(m) + E3[m] + W(m), m) for m in range(13, M + 1, 2))
we = max((c(m) + E3[m] + W(m), m) for m in range(14, M + 1, 2))
print('largest for odd 13 <= m <= %d: %s = %.6f at m = %d;  for even 14 <= m <= %d: %s = %.6f at m = %d'
      % (M, wo[0], float(wo[0]), wo[1], M, we[0], float(we[0]), we[1]))
print('m > %d: odd: 5/32 + 0.118569 = %.6f;  even: c(m) + 1/16 + 0.118569 <= %.6f' %
      (M, 5 / 32 + 0.118569, float(c(M + 2)) + 1 / 16 + 0.118569))
# added after the referee's report (its required change 4): the same bound for m <= 11, where Theorem 7 holds too
print('the bound c(m) + E3(m) + W_m(no 3) for m = 3..11: ' +
      ', '.join('%d: %s%s' % (m, c(m) + E3[m] + W(m), '' if c(m) + E3[m] + W(m) < F(3, 8) else ' (not below 3/8)')
                for m in range(3, 12)))
assert all(c(m) + E3[m] + W(m) < F(3, 8) for m in range(5, 12, 2))

print('--- Theorem 6: m <= 12, bound BB(m)')
bounds.build(12)
for m in range(3, 13):
    parts = ['q=%d: %d x %s at %s' % (q, (m - 1) // (q - 1), bounds.psi(q, m), bounds.PSIARG[(q, m)])
             for q in bounds.primes_from5(m)]
    print('  BB(%d) = %s + %s + [%s] = %s = %.6f  %s' % (m, c(m), E3[m], '; '.join(parts), BB[m], float(BB[m]),
                                                  '<= 3/8' if BB[m] <= F(3, 8) else 'ABOVE'))
    assert BB[m] <= F(3, 8)

print('--- Remark 6.1: for m <= 12 only one level of each prime can have a nonempty event: one PSI per prime')
for m in range(9, 13):
    b1 = c(m) + E3[m] + sum(bounds.psi(q, m) for q in bounds.primes_from5(m))
    print('  m=%d: %s = %.6f   (good share on every Z_n at least %s)' % (m, b1, float(b1), 1 - 2 * b1))

print('--- examples (lower bounds), all divisors, exact')
def crt(res_mod):          # dict modulus -> residue, pairwise coprime moduli
    n = 1
    for q in res_mod:
        n *= q
    x = 0
    for q, r in res_mod.items():
        cc = n // q
        x += r * cc * pow(cc, -1, q)
    return x % n, n
def pattern(m, primes):
    B = []
    for j in range(m):
        b, n = crt({q: (j if 1 <= j <= q - 1 else 0) for q in primes})
        B.append(b)
    return n, B
for m, primes in ((5, (3, 5)), (7, (3, 5, 7)), (9, (3, 5, 7)), (11, (3, 5, 7, 11)), (13, (3, 5, 7, 11, 13))):
    n, B = pattern(m, primes)
    print('  m=%d: heavy class and single elements at every prime of n=%d: bad share %s   B=%s' % (m, n, bad_share(n, B), B))
for n, B in ((75, [0, 0, 25, 25, 38, 50]), (105, [32, 35, 38, 59, 82, 85, 93, 93]),
             (315, [2, 34, 51, 90, 164, 165, 183, 258, 261, 277])):
    print('  m=%d on Z_%d: bad share %s   B=%s' % (len(B), n, bad_share(n, B), B))
