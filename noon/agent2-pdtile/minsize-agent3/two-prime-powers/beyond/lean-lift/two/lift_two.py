"""Lifting along the prime 2, built from the sign lemma for n = p^a q^b as proved by the instance I asked (its Lemma C and Theorem 2),
in an implementation of my own written from the description, and tested end to end.
N = 2^k N', N' = p^a q^b odd (at most two prime factors).  A nonempty multiset A on Z_N.  Recipe: take one nonempty class c modulo
2^k; sign its elements by the path rule on the p-tree of Z_{p^a} (the signed class sums along a path from a point u* to the root stay
nonzero modulo q, and at each level two sibling classes get different sums modulo q); lift the elements with sign + 'low'
(y mod 2^(k+1) = x mod 2^k) and those with sign - 'high' (y mod 2^(k+1) = x mod 2^k + 2^k); lift every other element low.
Claim: the lift has exactly the cyclotomic divisors of A (those d | N with Phi_d | A), and none of the new ones (d | 2N, d not | N).
Exact division.  Control: all elements low.   usage: lift_two.py [seed]"""
import sys, random
from sympy import Poly, cyclotomic_poly, symbols, ZZ, factorint
X = symbols('X'); random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
def pattern(els, M):
    v = [0] * M
    for x in els: v[x % M] += 1
    A = Poly(sum(w * X**i for i, w in enumerate(v) if w), X, domain=ZZ)
    return frozenset(d for d in range(2, M + 1) if M % d == 0 and A.rem(Poly(cyclotomic_poly(d, X), X, domain=ZZ)).is_zero)
def signs_by_path(B, p, a, q):
    """B: list of residues modulo N' (the elements of one class); returns a list of signs, one for each element"""
    pa = p ** a
    idx = {}
    for j, x in enumerate(B): idx.setdefault(x % pa, []).append(j)
    sg = [None] * len(B)
    def give(js, total):                     # signs for the elements js with sum = total (same parity as len(js), |total| <= len(js))
        assert (len(js) - abs(total)) % 2 == 0 and abs(total) <= len(js)
        s = 1 if total >= 0 else -1
        for i, j in enumerate(js): sg[j] = s if i < abs(total) else (1 if (i - abs(total)) % 2 == 0 else -1)
    ustar = next(iter(idx))
    t = 1 if len(idx[ustar]) % 2 else 2
    give(idx[ustar], t)
    for i in range(a, 0, -1):                # siblings of C_i: the classes modulo p^i inside the class of u* modulo p^(i-1), other than that of u*
        sib = {}
        for u, js in idx.items():
            if u % p ** (i - 1) == ustar % p ** (i - 1) and u % p ** i != ustar % p ** i: sib.setdefault(u % p ** i, []).extend(js)
        odd = [c for c, js in sib.items() if len(js) % 2]; even = [c for c, js in sib.items() if len(js) % 2 == 0]
        for c in even: give(sib[c], 0)
        eta = {}
        for h, c in enumerate(odd[:len(odd) - len(odd) % 2]): eta[c] = 1 if h % 2 == 0 else -1
        if len(odd) % 2:
            e0 = 1 if (t + 1) % q else -1; assert (t + e0) % q; eta[odd[-1]] = e0; t += e0
        for c in odd: give(sib[c], eta[c])
        assert t % q
    assert all(s in (1, -1) for s in sg)
    return sg
def lift_two(A, N):
    k = 0
    while N % 2 ** (k + 1) == 0: k += 1
    Np = N // 2 ** k; f = factorint(Np); assert len(f) <= 2
    if len(f) == 0: p, a, q = 3, 0, 5
    elif len(f) == 1: p = next(iter(f)); a = f[p]; q = 3 if p != 3 else 5
    else: (p, a), (q, _) = sorted(f.items())
    c = A[0] % 2 ** k; cls = [j for j, x in enumerate(A) if x % 2 ** k == c]
    sg = signs_by_path([A[j] % Np for j in cls], p, a, q)
    top = [0] * len(A)
    for j, s in zip(cls, sg): top[j] = 0 if s == 1 else 1
    out = []
    for x, tp in zip(A, top):
        target = x % 2 ** k + tp * 2 ** k
        y = x if x % 2 ** (k + 1) == target else x + N
        assert y % N == x and y % 2 ** (k + 1) == target; out.append(y)
    return out
res = {'the recipe': [0, 0], 'control, all low': [0, 0]}
for N in [1, 3, 9, 15, 45, 25, 75, 2, 6, 12, 18, 30, 36, 60, 90, 20, 50, 100, 150, 24, 72, 4, 8, 10, 21, 42, 63, 126]:
    for _ in range(60 if N <= 60 else 20):
        if random.random() < 0.5: A = [random.randrange(N) for _ in range(random.randint(1, 2 * N if N < 20 else 30))]
        else:
            A = []
            for _ in range(random.randint(1, 3)):
                cc = random.choice([d for d in range(1, N + 1) if N % d == 0]); x0 = random.randrange(N); A += [(x0 + cc * j) % N for j in range(N // cc)]
        P = pattern(A, N)
        res['the recipe'][0] += 1; res['the recipe'][1] += (pattern(lift_two(A, N), 2 * N) == P)
        low = []
        k = 0
        while N % 2 ** (k + 1) == 0: k += 1
        for x in A: low.append(x if x % 2 ** (k + 1) == x % 2 ** k else x + N)
        res['control, all low'][0] += 1; res['control, all low'][1] += (pattern(low, 2 * N) == P)
for name, (n, ok) in res.items(): print(f'{name}: {n} multisets on 28 groups Z_N; the lift to Z_2N has exactly the pattern of the multiset in {ok}')
