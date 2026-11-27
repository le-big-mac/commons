"""Does a multiset on Z_N lift to a SET on Z_{N r} with the same size and exactly the same cyclotomic divisors?
Claim tested (mine, from the count of roots): r an odd prime, N = r^k N', all multiplicities <= r and some element x1 with
multiplicity m in [1, r-1].  A lift of x is x + N*j, j = 0..r-1; its 'slot' is t = floor((y mod r^(k+1)) / r^k).  Recipe: x1 gets
the m slots 0..m-1; every other element x' of the class of x1 modulo r^k gets: all r slots if its multiplicity is r, all slots
but one middle slot if it is r-1, and slots inside 1..r-2 otherwise; elements of other classes get their first slots.
Then the lift is a set and no Phi_d with d | N r, d not | N divides its mask.
Also tested: the criterion behind it.  For d = e r^(k+1), e | N', Phi_d divides the lifted mask exactly when for every class c
modulo r^k the slot sums g_(c,t)(w) = sum of w^y over the elements y in class c and slot t are equal for all t (w of order e).
Exact division.  usage: set_lift.py [seed]"""
import sys, random, cmath, math
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X'); random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
CY = {}
def pattern(els, M):
    v = [0] * M
    for x in els: v[x % M] += 1
    A = Poly(sum(w * X**i for i, w in enumerate(v) if w), X, domain=ZZ)
    out = set()
    for d in range(1, M + 1):
        if M % d == 0:
            if d not in CY: CY[d] = Poly(cyclotomic_poly(d, X), X, domain=ZZ)
            if A.rem(CY[d]).is_zero: out.add(d)
    return frozenset(out)
def slot_of(y, r, k): return (y % r ** (k + 1)) // r ** k
def lifts_by_slot(x, N, r, k):
    d = {}
    for j in range(r): y = x + N * j; d[slot_of(y, r, k)] = y
    assert len(d) == r; return d
def set_lift(mult, N, r):
    """mult: dict x -> multiplicity (1..r), some multiplicity < r.  Returns a list of distinct elements of Z_{N r}."""
    k = 0
    while N % r ** (k + 1) == 0: k += 1
    x1 = next(x for x, m in sorted(mult.items()) if m < r); c1 = x1 % r ** k
    out = []
    for x, m in mult.items():
        L = lifts_by_slot(x, N, r, k)
        if x == x1: slots = list(range(m))
        elif x % r ** k == c1:
            if m == r: slots = list(range(r))
            elif m == r - 1: slots = [t for t in range(r) if t != 1]
            else: slots = list(range(1, 1 + m))
            assert (0 in slots) == (r - 1 in slots)
        else: slots = list(range(m))
        out += [L[t] for t in slots]
    assert len(set(out)) == len(out) == sum(mult.values())
    return out
tot = ok = plain_ok = 0; crit_tot = crit_ok = 0
for N, r in [(1, 3), (2, 3), (3, 3), (4, 3), (6, 3), (9, 3), (12, 3), (18, 3), (5, 3), (10, 3), (15, 3), (2, 5), (4, 5), (5, 5), (6, 5), (10, 5), (12, 5), (20, 5), (25, 5), (3, 7), (7, 7), (12, 7), (14, 7)]:
    k = 0
    while N % r ** (k + 1) == 0: k += 1
    for _ in range(120 if N * r <= 60 else 40):
        supp = random.sample(range(N), random.randint(1, min(N, 6)))
        if random.random() < 0.4:      # structured: a union of cosets with multiplicities
            supp = []
            for _c in range(random.randint(1, 2)):
                cc = random.choice([d for d in range(1, N + 1) if N % d == 0]); x0 = random.randrange(N); supp += [(x0 + cc * j) % N for j in range(N // cc)]
        mult = {}
        for x in supp: mult[x] = min(r, mult.get(x, 0) + random.randint(1, r))
        if all(m == r for m in mult.values()): mult[next(iter(mult))] = random.randint(1, r - 1)
        A = [x for x, m in mult.items() for _ in range(m)]
        P = pattern(A, N)
        L = set_lift(mult, N, r)
        tot += 1; ok += (pattern(L, N * r) == P)
        plain = [lifts_by_slot(x, N, r, k)[t] for x, m in mult.items() for t in range(m)]      # control: every element its first slots
        plain_ok += (pattern(plain, N * r) == P)
        # the criterion, on a random lift (slots chosen at random, a set)
        R = [lifts_by_slot(x, N, r, k)[t] for x, m in mult.items() for t in random.sample(range(r), m)]
        PR = pattern(R, N * r); Np = N // r ** k
        for e in [d for d in range(1, Np + 1) if Np % d == 0]:
            w = cmath.exp(2j * math.pi / e); const = True
            for c in range(r ** k):
                g = [sum(w ** y for y in R if y % r ** k == c and slot_of(y, r, k) == t) for t in range(r)]
                if max(abs(g[t] - g[0]) for t in range(r)) > 1e-7: const = False
            crit_tot += 1; crit_ok += (const == (e * r ** (k + 1) in PR))
print(f'the recipe: {tot} multisets (multiplicities up to r, not all r) on 23 pairs (N, r); the lift is a set with exactly the pattern of the multiset in {ok}')
print(f'control, every element in its first slots: exact pattern in {plain_ok} of {tot}')
print(f'the criterion (Phi_(e r^(k+1)) divides a random set-lift exactly when all slot sums agree in every class): agrees in {crit_ok} of {crit_tot} cases')
