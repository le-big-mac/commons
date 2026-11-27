# W(no 3) = sum over the integers e* > 1 with all prime factors >= 5 of 2^(-mu(e*)), mu(e*) = max_q v_q(e*) (q - 1).
# Exact fractions; decimals are printed rounded DOWN for lower bounds and UP for upper bounds.
# (wsum2.py printed "0.118564492 + 5.7e-4" rounded to nearest as 0.119134; the sum is 0.119134492, so that line did
#  not prove "< 0.119134".  This program replaces that line.)
from fractions import Fraction as Fr
import itertools, math

def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]

def A(t):
    # number of e* >= 1 with all prime factors >= 5 and mu(e*) <= t
    r = 1
    for p in primes_upto(t + 1):
        if p >= 5: r *= 1 + t // (p - 1)
    return r

def down(x, k=9):
    return math.floor(x * 10 ** k) / 10 ** k if False else '%d.%0*d' % (0, k, (x.numerator * 10 ** k) // x.denominator)
def up(x, k=9):
    return '%d.%0*d' % (0, k, -((-x.numerator * 10 ** k) // x.denominator))

# 1. the product formula against a list of all e* with mu <= 40
T0 = 40
ps = [p for p in primes_upto(T0 + 1) if p >= 5]
rng = [range(0, T0 // (p - 1) + 1) for p in ps]
cnt = {}
n_listed = 0
for ex in itertools.product(*rng):
    m = max([v * (p - 1) for v, p in zip(ex, ps)] + [0])
    cnt[m] = cnt.get(m, 0) + 1; n_listed += 1
for t in range(0, T0 + 1, 2):
    assert sum(v for m, v in cnt.items() if m <= t) == A(t), t
print('listed all', n_listed, 'numbers e* (1 included) with mu <= 40; the product formula A(t) agrees for every even t <= 40')
S40_list = sum(Fr(v, 2 ** m) for m, v in cnt.items() if m > 0)

def partial(T):
    return sum(Fr(A(t) - A(t - 2), 2 ** t) for t in range(2, T + 1, 2))
assert partial(40) == S40_list
for T in (40, 60, 120, 400):
    s = partial(T)
    print('partial sum up to t = %3d:  %s <= sum <= %s' % (T, down(s, 12), up(s, 12)))

# 2. the tail after t = 60, as in the last sentence of the proof of Lemma W of sign-four-result.md:
#    A_all(t) 2^(-t) <= (u + 1) x^u, u = t/2, x = e^(2K/3)/4 < 0.5783 (K < 1.2578), and A(t) <= A_all(t) (fewer primes).
K = Fr(12578, 10000)
x_num = math.exp(2 * float(K) / 3) / 4
assert x_num < 0.5783, x_num
x = Fr(5783, 10000)
tail60 = x ** 31 * (32 - 31 * x) / (1 - x) ** 2          # sum over u >= 31 of (u + 1) x^u
tail40 = x ** 21 * (22 - 21 * x) / (1 - x) ** 2
print('e^(2K/3)/4 with K = 1.2578: %.6f < 0.5783' % x_num)
print('tail after t = 40 <= %s ;  tail after t = 60 <= %s' % (up(tail40, 9), up(tail60, 9)))
assert tail60 < Fr(34, 10 ** 7)
# the tail directly, for comparison (not a proof beyond t = 400): the terms from t = 62 to t = 400
print('terms t = 62 .. 400 sum to at most', up(partial(400) - partial(60), 12))
ub = partial(60) + tail60
print('W(no 3) <= partial(60) + tail(60) <= %s' % up(ub, 9))
assert ub < Fr(118569, 10 ** 6)
print('hence W(no 3) < 0.118569;  2 W(no 3) < %s;  3 W(no 3) < %s' % (up(2 * ub, 6), up(3 * ub, 6)))
print('the bound printed before, 0.118564492 + 0.00057 =', up(partial(40) + Fr(57, 10 ** 5), 9), '(not below 0.119134)')
# 3. the later numbers that use W(no 3) < 0.119134 or 2 W(no 3) < 0.238269 stand, since 0.118569 < 0.119134
W = Fr(119134, 10 ** 6)
print('1 - 11/32 - 0.119134 =', float(1 - Fr(11, 32) - W), ' 2 * 0.119134 =', float(2 * W), ' 1/4 - 0.238269 =', float(Fr(1, 4) - Fr(238269, 10 ** 6)))
print('0.531258 + 1.13282 * 0.238269 =', float(Fr(531258, 10 ** 6) + Fr(113282, 10 ** 5) * Fr(238269, 10 ** 6)), '< 0.80118')
# 4. road 1 of section 6: the mixed levels 3^i e'' (i >= 1, e'' > 1) by Lemma V alone cost 2 (W - W(no 3) - 1/3),
#    W the sum over all odd e* > 1 (partial sums up to t = 120, exact)
def A_all(t):
    r = 1
    for p in primes_upto(t + 1):
        if p >= 3: r *= 1 + t // (p - 1)
    return r
W_all = sum(Fr(A_all(t) - A_all(t - 2), 2 ** t) for t in range(2, 121, 2))
mixed = 2 * (W_all - partial(120) - Fr(1, 3))
print('W (all odd primes), partial sum up to t = 120: %s ;  2 (W - W(no 3) - 1/3) = %s (rounded down)' % (down(W_all, 9), down(mixed, 6)))
