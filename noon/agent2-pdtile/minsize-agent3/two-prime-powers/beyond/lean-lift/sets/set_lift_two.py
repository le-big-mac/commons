"""The prime 2: does a multiset on Z_N with multiplicities <= 2^j, not all equal to 2^j, lift to a SET on Z_{N 2^j} with the same
size and exactly the same cyclotomic divisors, when the odd part of N is p^a q^b?
One step (N = 2^k N', i steps to go): each element x has two lifts, low and high (residue modulo 2^(k+1) below 2^k, or not);
m(x) copies are split as a_x(low) + a_x(high).  Phi_(e 2^(k+1)) divides the lift exactly when, in every class modulo 2^k, the sum
over x of (a_x(low) - a_x(high)) w^x is 0 (w of order e).  Recipe:
  if some multiplicity is odd: take a class c that holds such an element; the elements of odd multiplicity in c get a sign by the
     lemma on signs (signs_by_path of ../two/lift_two.py, on their residues modulo N'): sign + means the extra copy goes low,
     sign - high; elements of even multiplicity, and all elements of other classes, are split evenly (odd ones elsewhere: extra low);
  if all multiplicities are even: one element x1 with m(x1) < 2^i gets m/2 + 1 low and m/2 - 1 high, the others are split evenly.
Exact division.  usage: set_lift_two.py [seed]"""
import sys, random, importlib.util
from sympy import Poly, cyclotomic_poly, symbols, ZZ, factorint
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
src = open('/home/agent3/lean/lift-check/two/lift_two.py').read()
ns = {}; exec(src[src.index('def signs_by_path'):src.index('def lift_two')], {'__builtins__': __builtins__}, ns); signs_by_path = ns['signs_by_path']
X = symbols('X'); CY = {}
def pattern(mult, M):
    A = Poly(sum(w * X**i for i, w in mult.items() if w), X, domain=ZZ); out = set()
    for d in range(1, M + 1):
        if M % d == 0:
            if d not in CY: CY[d] = Poly(cyclotomic_poly(d, X), X, domain=ZZ)
            if A.rem(CY[d]).is_zero: out.add(d)
    return frozenset(out)
def step2(mult, N, i):
    assert max(mult.values()) <= 2 ** i and not all(m == 2 ** i for m in mult.values())
    k = 0
    while N % 2 ** (k + 1) == 0: k += 1
    Np = N // 2 ** k; f = factorint(Np); assert len(f) <= 2
    if len(f) == 0: p, a, q = 3, 0, 5
    elif len(f) == 1: p = next(iter(f)); a = f[p]; q = 3 if p != 3 else 5
    else: (p, a), (q, _) = sorted(f.items())
    split = {}
    odd = [x for x in sorted(mult) if mult[x] % 2]
    if odd:
        c = odd[0] % 2 ** k; cls = [x for x in odd if x % 2 ** k == c]
        sg = signs_by_path([x % Np for x in cls], p, a, q)
        for x, s in zip(cls, sg): h = mult[x] // 2; split[x] = (h + 1, h) if s == 1 else (h, h + 1)
        for x, m in mult.items():
            if x not in split: split[x] = (m - m // 2, m // 2)
    else:
        x1 = next(x for x in sorted(mult) if mult[x] < 2 ** i)
        for x, m in mult.items(): split[x] = (m // 2 + 1, m // 2 - 1) if x == x1 else (m // 2, m // 2)
    out = {}
    for x, (lo, hi) in split.items():
        for y in (x, x + N):
            low = (y % 2 ** (k + 1)) < 2 ** k
            w = lo if low else hi
            if w: out[y] = w
    assert sum(out.values()) == sum(mult.values())
    return out
tot = ok = plain_ok = 0
for N in [1, 3, 9, 15, 45, 5, 25, 2, 6, 18, 10, 30, 4, 12, 36, 20, 8, 24, 21, 63, 42, 75]:
    for _ in range(60 if N <= 30 else 25):
        supp = random.sample(range(N), random.randint(1, min(N, 7)))
        if random.random() < 0.4:
            supp = []
            for _c in range(random.randint(1, 2)):
                cc = random.choice([d for d in range(1, N + 1) if N % d == 0]); x0 = random.randrange(N); supp += [(x0 + cc * t) % N for t in range(N // cc)]
        j = 1
        mult = {}
        for x in supp: mult[x] = min(2 ** j, mult.get(x, 0) + random.randint(1, 2 ** j))
        if all(m == 2 ** j for m in mult.values()): mult[next(iter(mult))] = random.randint(1, 2 ** j - 1)
        P = pattern(mult, N); cur = dict(mult); M = N
        for i in range(j, 0, -1): cur = step2(cur, M, i); M *= 2
        tot += 1; ok += (max(cur.values()) == 1 and pattern(cur, M) == P)
        # control: every element's copies in turn low, high, low, ... (a set when j = 1)
        if j == 1:
            pl = {}
            for x, m in mult.items():
                for t in range(m): pl[x + N * t] = 1
            plain_ok += (pattern(pl, 2 * N) == P)
print(f'the recipe for the prime 2: {tot} multisets (multiplicities 1 and 2, not all 2; one step) on 22 groups whose odd part is p^a q^b; lifted to a set on Z_(2N) with exactly the same pattern: {ok}')
print(f'control (j = 1, first copy to x, second to x + N): exact pattern in {plain_ok} of the cases with j = 1')
