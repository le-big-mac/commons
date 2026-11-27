"""Lifting a multiset to a SET on a larger group, step by step along an odd prime r, spreading the copies of each element over
its r lifts.  Claim (mine): if all multiplicities are <= r^j and not all equal to r^j, the multiset on Z_N lifts to a set on
Z_{N r^j} with the same size, reducing to it, with exactly the same cyclotomic divisors.
One step (N = r^k N', i steps still to go, invariant: all multiplicities <= r^i, not all equal to r^i):
  pick x1: one whose multiplicity is not divisible by r if there is one, otherwise one with multiplicity < r^i;
  x1 = r a + rho copies:  if rho > 0: slot 0 gets a + 1, slot r-1 gets a, the other rho - 1 extra copies go to middle slots;
                          if rho = 0: slot 0 gets a + 1, slot r-1 gets a - 1, the middle slots a;
  every other element of the class of x1 modulo r^k: as evenly as possible, with slot 0 and slot r-1 getting the same number;
  elements of other classes: as evenly as possible.
Then slot 0 and slot r-1 of that class differ by exactly one (or two) copies of x1, so no new Phi_d divides (count of roots).
Tests: random multisets, and the least multisets of the theorem for Z_{p^n q} found by the solver (out/*-multi-cpsat.jsonl):
each is lifted to a set on Z_{p^n q r^j} and its pattern there is compared, by exact division, with the pattern on Z_{p^n q}.
usage: spread_lift.py r [WITNESS-FILES...]"""
import sys, random, json, collections
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X'); random.seed(5); CY = {}
def pattern(mult, M):
    A = Poly(sum(w * X**i for i, w in mult.items() if w), X, domain=ZZ); out = set()
    for d in range(1, M + 1):
        if M % d == 0:
            if d not in CY: CY[d] = Poly(cyclotomic_poly(d, X), X, domain=ZZ)
            if A.rem(CY[d]).is_zero: out.add(d)
    return frozenset(out)
def even_split(m, r, same_ends=True):
    a, rho = divmod(m, r); s = [a] * r
    if rho == r - 1:
        for t in range(r): s[t] += 1
        s[1] -= 1
    else:
        for t in range(1, 1 + rho): s[t] += 1          # rho <= r-2 middle slots
    assert sum(s) == m and s[0] == s[r - 1]; return s
def step(mult, N, r, i):
    """one lift along r; mult: dict x -> multiplicity on Z_N, all <= r^i and not all = r^i; returns dict on Z_{N r}"""
    assert max(mult.values()) <= r ** i and not all(m == r ** i for m in mult.values())
    k = 0
    while N % r ** (k + 1) == 0: k += 1
    cand = [x for x in sorted(mult) if mult[x] % r] or [x for x in sorted(mult) if mult[x] < r ** i]
    x1 = cand[0]; c1 = x1 % r ** k; out = {}
    for x, m in mult.items():
        if x == x1:
            a, rho = divmod(m, r)
            if rho > 0:
                s = [a] * r; s[0] += 1
                for t in range(1, rho): s[t] += 1          # rho - 1 <= r - 2 middle slots
            else:
                s = [a] * r; s[0] += 1; s[r - 1] -= 1
            assert sum(s) == m and s[0] != s[r - 1] and min(s) >= 0
        else: s = even_split(m, r)
        for j in range(r):
            y = x + N * j; t = (y % r ** (k + 1)) // r ** k
            if s[t]: out[y] = s[t]
    return out
def lift_to_set(mult, N, r):
    j = 0
    while not (max(mult.values()) <= r ** j and not all(m == r ** j for m in mult.values())): j += 1
    M = N
    for i in range(j, 0, -1): mult = step(mult, M, r, i); M *= r
    assert max(mult.values()) == 1
    return mult, M, j
r = int(sys.argv[1]); files = sys.argv[2:]
tot = ok = 0; js = collections.Counter()
for N in [1, 2, 3, 4, 5, 6, 9, 10, 12, 15, 18, 20]:
    for _ in range(40):
        supp = random.sample(range(N), random.randint(1, min(N, 5)))
        mult = {x: random.choice([1, 1, 2, 3, r, r + 1, 2 * r, r * r - 1, r * r]) for x in supp}
        if N * r * r * r > 2500: mult = {x: min(m, r) for x, m in mult.items()}
        P = pattern(mult, N); S, M, j = lift_to_set(mult, N, r); js[j] += 1
        tot += 1; ok += (pattern(S, M) == P and sum(S.values()) == sum(mult.values()) and all((y % N) in mult for y in S))
print(f'r = {r}: random multisets: {tot}; lifted to a set on Z_(N r^j) with exactly the same pattern and size: {ok}; steps j used: {dict(sorted(js.items()))}')
tot = ok = 0; js = collections.Counter(); noset = 0
for f in files:
    for line in open(f):
        if not line.startswith('{'): continue
        o = json.loads(line)
        if o.get('min') is None or not o.get('witness'): continue
        N = o['p'] ** o['n'] * o['q']; mult = {}
        for t in o['witness'].split():
            x, _, m = t.partition('^'); mult[int(x)] = int(m) if m else 1
        assert sum(mult.values()) == o['min']
        if N * r ** 3 > 6000 and max(mult.values()) > r * r: continue
        P = pattern(mult, N); S, M, j = lift_to_set(mult, N, r); js[j] += 1
        tot += 1; ok += (pattern(S, M) == P and sum(S.values()) == o['min'])
print(f'r = {r}: least multisets of the theorem (solver witnesses): {tot}; each lifted to a SET of the same size on Z_(p^n q r^j) with exactly the same pattern: {ok}; steps j used: {dict(sorted(js.items()))}')
