"""Check, by a program of my own, of the referee's table S(Pi) (report of 27 November 2026, item 1).
S(Pi) = sum_{p in Pi} delta_p + sum over e* with at least two primes, all in Pi, of 2^(1 - mu(e*)),
delta_p = sum_{l>=1} 2^(1 - (p-1) p^(l-1)),  mu(e*) = max_p v_p(e*) (p - 1).
The second sum is computed in two independent ways:
 (A) by the product formula: #{e* : mu <= t} = prod_{p in Pi, p <= t+1} (1 + floor(t/(p-1))), minus the pure prime powers,
     exactly up to t = T (T = 60), plus the tail bound of Lemma W of sign-four-result.md applied term by term:
     sum over t >= 62 of (number of odd d with mu(d) = t) 2^(-t) <= sum_{u >= 31} (u+1) x^u, x = 0.5783;
 (B) for finite Pi, by listing the exponent vectors (l_p) with (p-1) l_p <= T directly.
Pi may be a finite set, or a finite set together with all primes >= q."""
from fractions import Fraction as F
import itertools

def is_prime(p): return p > 1 and all(p % q for q in range(2, int(p ** .5) + 1))
def primes_upto(N): return [p for p in range(3, N + 1, 2) if is_prime(p)]

T = 60
x = 0.5783
TAIL = x ** 31 * (32 - 31 * x) / (1 - x) ** 2          # bound for sum_{u>=31} (u+1) x^u

def members(fin, q):
    """the primes of Pi that are <= T + 1 (the others play no part up to t = T)"""
    ps = set(fin)
    if q is not None: ps |= {p for p in primes_upto(T + 1) if p >= q}
    return sorted(ps)

def delta(p):
    s = F(0); l = 1
    while (p - 1) * p ** (l - 1) < 400:
        s += F(2, 2 ** ((p - 1) * p ** (l - 1))); l += 1
    return s

def S_formula(fin, q=None):
    ps = members(fin, q)
    def A(t):
        r = 1
        for p in ps:
            if p <= t + 1: r *= 1 + t // (p - 1)
        return r
    mixed = F(0)
    for t in range(2, T + 1, 2):
        pure_t = sum(1 for p in ps if t % (p - 1) == 0)        # the prime powers p^l with l (p-1) = t
        mixed += F(2 * (A(t) - A(t - 2) - pure_t), 2 ** t)
    pure = sum(delta(p) for p in ps)
    if q is not None:                                          # the primes of Pi above T + 1: delta_p < 2^(3-p)
        pure_tail = sum(F(8, 2 ** p) for p in primes_upto(400) if p > T + 1) + F(1, 2 ** 390)
    else: pure_tail = F(0)
    lo = pure + mixed
    hi = float(lo) + float(pure_tail) + 2 * TAIL
    return float(lo), hi

def S_listing(fin):
    ps = sorted(fin); rng = [range(0, T // (p - 1) + 1) for p in ps]; mixed = F(0)
    for ls in itertools.product(*rng):
        if sum(1 for l in ls if l) >= 2:
            mixed += F(2, 2 ** max(l * (p - 1) for l, p in zip(ls, ps)))
    return float(sum(delta(p) for p in ps) + mixed)

print(f'tail bound used after t = {T}: 2 * {TAIL:.3e}')
rows = [((3, 5), None, '0.98515'), ((3, 5, 7), None, '1.3161'), ((3, 5, 11), None, '1.0263'), ((3, 5, 13), None, '0.99980'),
        ((3, 5, 17), None, '0.98660'), ((3, 5), 17, '0.98760'), ((3, 5, 13), 23, '0.99989'), ((3, 5, 13, 17), None, '1.0027'),
        ((3, 5, 13, 19), None, '1.0006')]
for fin, q, ref in rows:
    lo, hi = S_formula(fin, q)
    name = '{' + ', '.join(map(str, fin)) + '}' + (f' and all primes >= {q}' if q else '')
    extra = f'  listing (B): {S_listing(fin):.6f}' if q is None else ''
    print(f'{name}: {lo:.6f} <= S <= {hi:.6f}   (referee: {ref}){extra}')
# what the two infinite families leave out, and the smallest sets outside them
for fin in ((3, 5, 19), (3, 5, 23), (3, 5, 13, 23), (3, 5, 17, 19)):
    lo, hi = S_formula(fin); print('{' + ', '.join(map(str, fin)) + '}', f': {lo:.6f} <= S <= {hi:.6f}  listing (B): {S_listing(fin):.6f}')
