"""N1 (lhsN1_lt_one): for m >= 1 and a finite set T of odd t > 1 with mu t + 1 <= m, lhsN1 m T < 1.  Exact rationals.

lhsN1 m T grows when an element is added to T (an element other than 3 adds (1/2)^mu > 0; the element 3 adds
1/4 - 1/16 or 1/4), so its largest value over the allowed T is at T = Tmax(m) = all odd t > 1 with mu t <= m - 1,
which is a finite set.  This program
 1. enumerates Tmax(m) explicitly for m <= M1 (products of powers of the odd primes p <= m), recomputes mu of every
    element by factorising it, checks the enumeration against a sieve of all odd t < 10^6, and evaluates lhsN1 literally;
 2. evaluates the same from the counting formula A(s) = prod_{odd p <= s+1} (1 + s // (p-1)) for m <= M2, and compares
    the two on m <= M1;
 3. bounds the infinite series W rigorously (halving bound a(u)^2 <= 8^u, checked here for u <= 3000 together with the
    three steps of its proof by induction), so that every m beyond M2 is covered;
 4. prints the margins, the m for which the statement would fail without the "- 1/16", and the numbers of the plan's route.
usage: t2_n1.py M1 M2"""
import os
import sys
from fractions import Fraction
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core

M1, M2 = int(sys.argv[1]), int(sys.argv[2])


def is_prime(p):
    return p >= 2 and all(p % q for q in range(2, int(p ** 0.5) + 1))


def tmax(m):
    res = [1]
    for p in range(3, m + 1):
        if is_prime(p):
            res = [t * p ** v for t in res for v in range((m - 1) // (p - 1) + 1)]
    return [t for t in res if t > 1]


def A(s):
    """number of odd t >= 1 with mu t <= s"""
    r = 1
    for p in range(3, s + 2):
        if is_prime(p):
            r *= 1 + s // (p - 1)
    return r


def c(m):
    return Fraction(comb(m, m // 2), 2 ** m) if m % 2 == 0 else Fraction(0)


# ---- 0. the sieve: for odd t < 10^6, mu t by factorising; Tmax(m) below 10^6 must be exactly {t : mu t <= m-1} ----
LIM = 10 ** 6
mus = {t: core.mu(t) for t in range(3, LIM, 2)}
assert all(v % 2 == 0 and v >= 2 for v in mus.values())
print('mu t is even and >= 2 for every odd t, 3 <= t < 10^6: yes (%d values)' % len(mus))
bad_enum = 0
for m in range(1, 41):
    a = sorted(t for t in tmax(m) if t < LIM) if m <= 34 else None
    b = sorted(t for t, v in mus.items() if v <= m - 1)
    if a is not None and a != b:
        bad_enum += 1
print('Tmax(m) below 10^6 against the sieve, m = 1..34: mismatches', bad_enum)

# ---- 1. explicit enumeration ----
print('explicit enumeration of Tmax(m): m, |Tmax|, lhsN1 m Tmax (exact), decimal, margin 1 - lhs')
explicit = {}
for m in range(1, M1 + 1):
    T = tmax(m)
    assert len(set(T)) == len(T) and all(t % 2 == 1 and t > 1 for t in T)
    ms = [core.mu(t) for t in T]
    assert all(x + 1 <= m for x in ms)
    if m <= 20:
        val = core.lhsN1(m, T)                        # the definition, literally
    else:
        val = c(m) + sum(Fraction(1, 2 ** x) for x in ms) - (Fraction(1, 16) if (m % 2 == 0 and m >= 14 and 3 in T) else 0)
    explicit[m] = val
    assert len(T) == A(m - 1) - 1, (m, len(T), A(m - 1))
    print('  m = %2d  |Tmax| = %8d  lhs = %s = %.6f  margin %.6f' % (m, len(T), val, float(val), float(1 - val)))
    assert val < 1

# ---- 2. by the counting formula ----
def Wm(m):
    """sum of (1/2)^mu t over the odd t > 1 with mu t <= m - 1"""
    s = Fraction(0)
    for u in range(1, (m - 1) // 2 + 1):
        s += Fraction(A(2 * u) - A(2 * u - 2), 4 ** u)
    return s

formula = {}
W_partial = Fraction(0)          # running sum over u
prevA = 1
u_done = 0
for m in range(1, M2 + 1):
    U = (m - 1) // 2
    while u_done < U:
        u_done += 1
        a_u = A(2 * u_done)
        W_partial += Fraction(a_u - prevA, 4 ** u_done)
        prevA = a_u
    val = c(m) + W_partial - (Fraction(1, 16) if (m % 2 == 0 and m >= 14) else 0)
    formula[m] = (val, W_partial)
mm = [m for m in explicit if explicit[m] != formula[m][0]]
print('formula against explicit enumeration, m = 1..%d: mismatches %d' % (M1, len(mm)))
assert all(Wm(m) == formula[m][1] for m in (1, 2, 3, 7, 12, 13, 14, 25, 40))
worst = max(formula, key=lambda m: formula[m][0])
print('largest lhsN1 m Tmax over m = 1..%d: at m = %d, %s = %.6f' % (M2, worst, formula[worst][0], float(formula[worst][0])))
for name, sel in (('odd m', lambda m: m % 2 == 1), ('even m <= 12', lambda m: m % 2 == 0 and m <= 12),
                  ('even m >= 14', lambda m: m % 2 == 0 and m >= 14)):
    ms_ = [m for m in formula if sel(m)]
    w = max(ms_, key=lambda m: formula[m][0])
    print('   %-13s largest at m = %4d: %.9f (margin %.9f)' % (name, w, float(formula[w][0]), float(1 - formula[w][0])))
print('   every m <= %d has lhsN1 m Tmax < 1: %s' % (M2, all(formula[m][0] < 1 for m in formula)))
print('   even m, the six fractions of the plan (m = 2..12):', [str(formula[m][0]) for m in (2, 4, 6, 8, 10, 12)])
print('   even m >= 14, first values:', ['%d: %.5f' % (m, float(formula[m][0])) for m in range(14, 42, 2)])
nosub = [m for m in formula if m % 2 == 0 and m >= 14 and formula[m][0] + Fraction(1, 16) >= 1]
print('   without the "- 1/16" the left side at Tmax would be >= 1 for m in', nosub)
nosub3 = [m for m in formula if m % 2 == 0 and m >= 14 and formula[m][0] + Fraction(1, 16) - Fraction(1, 4) >= 1]
print('   Tmax without 3 (no 1/16 taken, no 1/4 for t = 3): >= 1 for m in', nosub3)
wrong = [m for m in formula if m % 2 == 0 and m < 14 and formula[m][0] - Fraction(1, 16) >= 1]
print('   (a check of the direction: taking 1/16 away only for 3 in T and m >= 14 even; for odd m and even m <= 12 nothing is taken)')

# ---- 3. the infinite series, rigorously ----
def a(u):
    return A(2 * u)
def npi(u):
    return sum(1 for p in range(3, 2 * u + 2) if is_prime(p))
ok1 = all(1 + u // k <= 2 * (1 + (u // 2) // k) for u in range(0, 3001) for k in range(1, min(u, 200) + 2))
ok1b = all(1 + u // k <= 2 * (1 + (u // 2) // k) for u in range(0, 400) for k in range(1, u + 2))
print('halving step (1): 1 + u//k <= 2 (1 + (u//2)//k): holds for u <= 3000, k <= 201: %s; for u < 400, all k <= u + 1: %s' % (ok1, ok1b))
aa = [a(u) for u in range(0, 3001)]
pis = [npi(u) for u in range(0, 3001)]
print('step a(u) <= 2^pi(u) a(u//2) for u <= 3000:', all(aa[u] <= 2 ** pis[u] * aa[u // 2] for u in range(0, 3001)))
print('step (2): 3 pi(u) <= 2u + 5 for u <= 3000:', all(3 * pis[u] <= 2 * u + 5 for u in range(0, 3001)),
      '; 2 pi(u) <= 3 (u - u//2) for 20 <= u <= 3000:', all(2 * pis[u] <= 3 * (u - u // 2) for u in range(20, 3001)),
      '; it fails for u in', [u for u in range(0, 20) if 2 * pis[u] > 3 * (u - u // 2)])
print('step (3): a(u)^2 <= 8^u for u <= 3000:', all(aa[u] ** 2 <= 8 ** u for u in range(0, 3001)),
      '; a(u) <= 3 * 8^(u//2):', all(aa[u] <= 3 * 8 ** (u // 2) for u in range(0, 3001)))
print('   largest a(u)^2 / 8^u: %.6f at u = %d' % max((aa[u] ** 2 / 8 ** u, u) for u in range(0, 200)))
# W <= sum_{u <= U} (a(u) - a(u-1)) / 4^u + sum_{u > U} a(u)/4^u,  a(u)/4^u <= 8^(u/2)/4^u = 2^(-u/2)
for U in (19, 60, 200, 1000):
    part = sum(Fraction(aa[u] - aa[u - 1], 4 ** u) for u in range(1, U + 1))
    # sum_{u > U} 2^(-u/2) = 2^(-(U+1)/2) / (1 - 2^(-1/2)) < 3.42 * 2^(-(U+1)/2)
    tail = 3.42 * 2 ** (-(U + 1) / 2)
    print('   U = %4d: partial sum of W = %.12f, tail below %.3e, so W < %.12f' % (U, float(part), tail, float(part) + tail))
partial200 = sum(Fraction(aa[u] - aa[u - 1], 4 ** u) for u in range(1, 201))
Wup = partial200 + Fraction(1, 10 ** 20)
print('   W is between %.12f and %.12f' % (float(partial200), float(Wup)))
print('   odd m: lhsN1 <= W < 1 for every m: margin %.6f' % float(1 - Wup))
cM = c(M2 if M2 % 2 == 0 else M2 - 1)
print('   even m > %d: lhsN1 <= c_m + W - 1/16 <= %.6f + %.6f - 0.0625 < 1: %s (c_m decreases: checked for even m <= %d: %s)'
      % (M2, float(cM), float(Wup), cM + Wup - Fraction(1, 16) < 1, M2, all(c(m + 2) < c(m) for m in range(2, M2, 2))))
print('   the plan\'s crude bound for even m >= 14: c_14 + W - 1/16 = %.6f (margin %.6f); exact largest value is above' %
      (float(c(14) + Wup - Fraction(1, 16)), float(1 - (c(14) + Wup - Fraction(1, 16)))))

# ---- 4. the plan's route for Lean ----
S19 = sum(Fraction(aa[u] - aa[u - 1], 4 ** u) for u in range(1, 20))
print('plan\'s route: sum_{u<=19} (a(u)-a(u-1))/4^u = %.6f; + 15/2^11 = %.6f; plan says "below 0.8518": %s; '
      '1 + 1/16 - c_14 = %.6f; bound below it: %s' %
      (float(S19), float(S19 + Fraction(15, 2 ** 11)), S19 + Fraction(15, 2 ** 11) < Fraction(8518, 10000),
       float(1 + Fraction(1, 16) - c(14)), S19 + Fraction(15, 2 ** 11) < 1 + Fraction(1, 16) - c(14)))
print('   partial sums for u = 1..6:', [str(sum(Fraction(aa[u] - aa[u - 1], 4 ** u) for u in range(1, U + 1))) for U in range(1, 7)])
print('   A(s) for s = 2, 4, .., 40:', [A(s) for s in range(2, 42, 2)])
