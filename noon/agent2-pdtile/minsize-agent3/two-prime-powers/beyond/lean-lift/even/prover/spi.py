"""Check, by a program of my own, of the referee's table S(Pi) (its report of 27 November 2026, item 1; corrected after
its second look: the first version, kept as spi.first-version.py, printed bounds rounded to NEAREST and stopped at t = 60;
this one rounds lower bounds DOWN and upper bounds UP and goes to t = 120).
S(Pi) = sum_{p in Pi} delta_p + sum over e* with at least two primes, all in Pi, of 2^(1 - mu(e*)),
delta_p = sum_{l>=1} 2^(1 - (p-1) p^(l-1)),  mu(e*) = max_p v_p(e*) (p - 1).
The second sum is computed in two independent ways:
 (A) by the product formula: #{e* : mu <= t} = prod_{p in Pi, p <= t+1} (1 + floor(t/(p-1))), minus the pure prime powers,
     exactly (fractions) up to t = T, plus the tail bound of Lemma W of sign-four-result.md applied term by term:
     sum over even t > T of (number of odd d with mu(d) = t) 2^(-t) <= sum_{u >= T/2+1} (u+1) x^u, x = 0.5783;
 (B) for finite Pi, by listing the exponent vectors (l_p) with (p-1) l_p <= T directly (exact).
Every term is >= 0, so the exact partial sum is a lower bound; partial sum + tails is an upper bound.
Pi may be a finite set, or a finite set together with all primes >= q."""
from fractions import Fraction as F
import itertools, math

def is_prime(p): return p > 1 and all(p % q for q in range(2, int(p ** .5) + 1))
def primes_upto(N): return [p for p in range(3, N + 1, 2) if is_prime(p)]

T = 120
X = F(5783, 10000)
U0 = T // 2 + 1
TAIL = X ** U0 * ((U0 + 1) - U0 * X) / (1 - X) ** 2      # exact value of sum_{u >= U0} (u+1) x^u

def down(v, k=6): return F(math.floor(v * 10 ** k), 10 ** k)
def up(v, k=6):   return F(math.ceil(v * 10 ** k), 10 ** k)
def dec(v, k):    # exact decimal string of a fraction with k places, truncated
    n = math.floor(v * 10 ** k); return f'{n // 10 ** k}.{n % 10 ** k:0{k}d}'

def members(fin, q):
    ps = set(fin)
    if q is not None: ps |= {p for p in primes_upto(T + 1) if p >= q}
    return sorted(ps)

def delta(p):
    s = F(0); l = 1
    while (p - 1) * p ** (l - 1) < 600:
        s += F(2, 2 ** ((p - 1) * p ** (l - 1))); l += 1
    return s, F(4, 2 ** 600)        # the value up to exponent 600, and a bound for the rest of the series

def S_formula(fin, q=None):
    ps = members(fin, q)
    def A(t):
        r = 1
        for p in ps:
            if p <= t + 1: r *= 1 + t // (p - 1)
        return r
    mixed = F(0)
    for t in range(2, T + 1, 2):
        pure_t = sum(1 for p in ps if t % (p - 1) == 0)         # the prime powers p^l with l (p-1) = t
        mixed += F(2 * (A(t) - A(t - 2) - pure_t), 2 ** t)
    pure = F(0); rest = F(0)
    for p in ps:
        d, r = delta(p); pure += d; rest += r
    if q is not None: rest += F(16, 2 ** (T + 1))               # primes of Pi above T + 1: sum of delta_p < 2^(4 - (T+2))
    lo = pure + mixed
    hi = lo + rest + 2 * TAIL
    return lo, hi

def S_listing(fin):
    ps = sorted(fin); rng = [range(0, T // (p - 1) + 1) for p in ps]; mixed = F(0)
    for ls in itertools.product(*rng):
        if sum(1 for l in ls if l) >= 2:
            mixed += F(2, 2 ** max(l * (p - 1) for l, p in zip(ls, ps)))
    return sum(delta(p)[0] for p in ps) + mixed

print(f'T = {T}; tail bound after t = T: 2 * {float(TAIL):.3e}')
rows = [((3, 5), None), ((3, 5, 7), None), ((3, 5, 11), None), ((3, 5, 13), None), ((3, 5, 17), None), ((3, 5), 17),
        ((3, 5, 13), 23), ((3, 5, 13, 17), None), ((3, 5, 13, 19), None), ((3, 5, 19), None), ((3, 5, 23), None),
        ((3, 5, 13, 23), None), ((3, 5, 17, 19), None)]
res = {}
for fin, q in rows:
    lo, hi = S_formula(fin, q); res[(fin, q)] = (lo, hi)
    name = '{' + ', '.join(map(str, fin)) + '}' + (f' and all primes >= {q}' if q else '')
    line = f'{name}: S = {dec(lo, 10)}... ; {dec(down(lo), 6)} <= S <= {dec(up(hi), 6)}'
    if q is None:
        b = S_listing(fin); assert b == lo, (fin, float(b), float(lo)); line += '   listing (B): equal exactly'
    print(line)
# the bounds written in even-result.md after the referee's second look
checks = [('0.98516 > S({3,5})', res[((3, 5), None)][1] < F(98516, 100000)),
          ('S({3,5,13}) < 0.99980', res[((3, 5, 13), None)][1] < F(99980, 100000)),
          ('0.999790 <= S({3,5,13})', res[((3, 5, 13), None)][0] >= F(999790, 10 ** 6)),
          ('S({3,5,13}) <= 0.999797', res[((3, 5, 13), None)][1] <= F(999797, 10 ** 6)),
          ('NOT 0.999791 <= S({3,5,13})  (the bound of the first version, false)', res[((3, 5, 13), None)][1] < F(999791, 10 ** 6)),
          ('S({3,5} and all p >= 17) < 0.98760', res[((3, 5), 17)][1] < F(98760, 100000)),
          ('S({3,5} and all p >= 17) <= 0.987599', res[((3, 5), 17)][1] <= F(987599, 10 ** 6)),
          ('S({3,5,13} and all p >= 23) < 0.99989', res[((3, 5, 13), 23)][1] < F(99989, 100000)),
          ('S({3,5,13} and all p >= 23) <= 0.999891', res[((3, 5, 13), 23)][1] <= F(999891, 10 ** 6)),
          ('S({3,5,13,17}) >= 1.002697', res[((3, 5, 13, 17), None)][0] >= F(1002697, 10 ** 6)),
          ('S({3,5,13,19}) >= 1.000636', res[((3, 5, 13, 19), None)][0] >= F(1000636, 10 ** 6)),
          ('NOT S({3,5,13,19}) >= 1.000637  (the bound of the first version, false)', res[((3, 5, 13, 19), None)][1] < F(1000637, 10 ** 6)),
          ('S({3,5,7}) > 1.3161 and S({3,5,11}) > 1.0262', res[((3, 5, 7), None)][0] > F(13161, 10000) and res[((3, 5, 11), None)][0] > F(10262, 10000))]
for name, ok in checks: print(('TRUE   ' if ok else 'FALSE  ') + name)
assert all(ok for _, ok in checks)
