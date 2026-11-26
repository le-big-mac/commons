"""The reader's lemma on lifts, tried by me.  r a prime, N = r^k N' (r not dividing N'), M = N r, A a nonempty multiset on Z_N.
Every element x of A is lifted to the y in Z_M with y = x mod N and (y mod r^(k+1)) < r^k, except one element, which is lifted to
the y with (y mod r^(k+1)) = (x mod r^k) + r^k.  Claim for r odd: the lifted multiset has exactly the pattern of A.
Exact division throughout.  Also the plain lift (no exception) and the case r = 2, as controls.   usage: lift_lemma_own.py [seed]"""
import sys, random
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X'); random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
def pattern(els, M):
    v = [0] * M
    for x in els: v[x] += 1
    A = Poly(sum(w * X**i for i, w in enumerate(v) if w), X, domain=ZZ)
    return frozenset(d for d in range(2, M + 1) if M % d == 0 and A.rem(Poly(cyclotomic_poly(d, X), X, domain=ZZ)).is_zero)
def lift(x, N, r, k, top):
    """the y mod N r with y = x mod N and y mod r^(k+1) = (x mod r^k) + top * r^k"""
    M = N * r; target = x % r ** k + top * r ** k
    for t in range(r):
        y = x + N * t
        if y % r ** (k + 1) == target: return y
    raise ValueError
res = {'odd, the lemma': [0, 0], 'odd, plain lift': [0, 0], 'r = 2, the lemma': [0, 0]}
for N, r in [(3, 3), (5, 3), (9, 3), (15, 3), (15, 5), (45, 3), (45, 5), (25, 5), (75, 3), (75, 5), (12, 3), (20, 5), (36, 3), (7, 7), (21, 3), (21, 7), (6, 2), (12, 2), (18, 2), (10, 2), (20, 2)]:
    k = 0
    while N % r ** (k + 1) == 0: k += 1
    for _ in range(40 if N * r <= 150 else 12):
        size = random.randint(1, 2 * N); A = [random.randrange(N) for _ in range(size)]
        if random.random() < 0.5:                       # half the trials: multisets with some structure (sums of cosets), so that the pattern is not empty
            A = []
            for _ in range(random.randint(1, 3)):
                c = random.choice([d for d in range(1, N + 1) if N % d == 0]); x0 = random.randrange(N); A += [(x0 + c * j) % N for j in range(N // c)]
        P = pattern(A, N)
        L = [lift(x, N, r, k, 0) for x in A[1:]] + [lift(A[0], N, r, k, 1)]
        key = 'odd, the lemma' if r > 2 else 'r = 2, the lemma'
        res[key][0] += 1; res[key][1] += (pattern(L, N * r) == P)
        if r > 2:
            L0 = [lift(x, N, r, k, 0) for x in A]
            res['odd, plain lift'][0] += 1; res['odd, plain lift'][1] += (pattern(L0, N * r) == P)
for k_, (n, ok) in res.items(): print(f'{k_}: {n} multisets, pattern kept in {ok}')
