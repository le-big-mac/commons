# The numbers used in even-result-2.md, with exact fractions.
from fractions import Fraction as Fr
import math, itertools

def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]

def A(t, excl=(2, 3)):
    # number of e* >= 1 whose primes are not in excl with mu(e*) = max v_p (p-1) <= t
    r = 1
    for p in primes_upto(t + 1):
        if p not in excl: r *= 1 + t // (p - 1)
    return r

# check the product formula by enumeration for t <= 12
def mu_enum(tmax):
    ps = [p for p in primes_upto(tmax + 1) if p >= 5]
    cnt = {}
    rng = [range(0, tmax // (p - 1) + 1) for p in ps]
    for ex in itertools.product(*rng):
        m = max([v * (p - 1) for v, p in zip(ex, ps)] + [0])
        cnt[m] = cnt.get(m, 0) + 1
    return cnt
cnt = mu_enum(12)
for t in range(0, 13, 2):
    assert sum(v for m, v in cnt.items() if m <= t) == A(t), t
print('product formula for A(t), primes >= 5, checked by enumeration for t <= 12')

T = 60
W3 = Fr(0); terms = {}
for t in range(2, T + 1, 2):
    c = A(t) - A(t - 2); terms[t] = c
    W3 += Fr(c, 2 ** t)
print('W(no 3): partial sum up to t = 40: %.9f' % float(sum(Fr(terms[t], 2 ** t) for t in range(2, 41, 2))), ' up to t = 60: %.9f' % float(W3))
print('   with the tail bound 5.7e-4 of Lemma W after t = 40: W(no 3) < %.6f ; 2 W(no 3) < %.6f ; 1/4 - 2 W(no 3) > %.6f' % (
    float(sum(Fr(terms[t], 2 ** t) for t in range(2, 41, 2))) + 5.7e-4, 2 * (float(sum(Fr(terms[t], 2 ** t) for t in range(2, 41, 2))) + 5.7e-4),
    0.25 - 2 * (float(sum(Fr(terms[t], 2 ** t) for t in range(2, 41, 2))) + 5.7e-4)))

# p_r = P(sum of r signs = 0 mod 3)
p = [Fr(1)]
for r in range(1, 41): p.append((1 - p[-1]) / 2)
print('p_r, r = 0..12:', ' '.join(str(x) for x in p[:13]))
assert all(Fr(1, 4) <= p[r] <= Fr(1, 2) for r in range(2, 41))
assert all(p[r] <= Fr(3, 8) for r in range(3, 41)) and all(p[r] <= Fr(11, 32) for r in range(5, 41))
print('1/4 <= p_r <= 1/2 for 2 <= r <= 40; p_r <= 3/8 for r >= 3; p_r <= 11/32 for r >= 5 (checked to 40; in general p_{r+1} = (1 - p_r)/2)')
# least value of p_E + p_D - 2 p_E p_D over the sizes (not both 1, not both 0)
best = min((p[a] + p[b] - 2 * p[a] * p[b], a, b) for a in range(0, 41) for b in range(0, 41) if (a, b) not in ((1, 1), (0, 0)))
print('least p_E + p_D - 2 p_E p_D over sizes up to 40, (|E|,|D|) not (1,1), (0,0):', best)
print('Proposition H: 1 - p_m - W(no 3):  m = 3: 3/4;  m = 4: 5/8;  m >= 5: > %.4f' % (1 - 11 / 32 - 0.119134))

# section 5: the budget for odd m
d3 = sum(Fr(2, 2 ** (2 * 3 ** (l - 1))) for l in range(1, 6))
print('delta_3 = sum_l 2^(1 - 2*3^(l-1)) = %.6f' % float(d3))
def TA(mu):
    return sum(Fr(2, 2 ** max(2 * 3 ** (l - 1), mu + 1)) for l in range(1, 12))
sA = sum(terms[t] * TA(t) for t in terms)
print('case A:  sum over e2* of T_A(mu) (t <= 60) = %.6f' % float(sA))
for rho in (Fr(2, 3), Fr(9, 10), Fr(1), Fr(2)):
    s = sum(terms[t] * max(TA(t), (1 + rho) * Fr(2, 2 ** t)) for t in terms)
    print('   if every dangerous e2 had mixed cost <= rho * 2^(1-mu), rho = %s:  delta_3 + sum_e2* max(T_A, (1+rho) 2^(1-mu)) = %.6f' % (rho, float(d3 + s)))
