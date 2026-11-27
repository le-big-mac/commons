"""Exact tests of the two reductions for the statement on signs (27 Nov 2026, agent3).
R1 (strip a large prime): n = n' q^b, q prime not dividing n', q > m = number of elements of the multiset B on Z_n.
    Claim: for EVERY signing, the signed mask of B is free of cyclotomic divisors Phi_d (d | n) if and only if the signed mask
    of B mod n' is free of the Phi_d' (d' | n').
R2 (contract a level without branching): n = p^a n'', 1 <= t <= a, and any two elements of B that agree mod p^(t-1) agree mod p^t.
    Delete the p-adic digit of index t-1 of every element (CRT with n''): a multiset on Z_(n/p).  Claim: for EVERY signing the
    two signed masks are both free of cyclotomic divisors, or neither is.
Signed masks are divided by cyclotomic polynomials with integer arithmetic (star.exact_ok).
usage: test_reductions.py SEED COUNT"""
import sys, random, itertools
sys.path.insert(0, '/home/agent3/lean/lift-check/mod4')
from star import exact_ok
from math import gcd

def crt(r1, m1, r2, m2):
    for k in range(m2):
        x = r1 + m1 * k
        if x % m2 == r2: return x % (m1 * m2)
def signings(m):
    for k in range(m):
        for M in itertools.combinations(range(1, m), k): yield M          # the first element keeps +
def good(n, B, M):
    return exact_ok(n, tuple(B), tuple(B[i] for i in M))

def test_R1(rng, count):
    cases = 0; signs = 0; goodn = 0
    shapes = [(9, 7, 1), (15, 7, 1), (9, 5, 1), (3, 7, 2), (45, 7, 1), (5, 7, 1), (25, 7, 1), (15, 11, 1), (9, 11, 1), (27, 5, 1), (3, 5, 2), (21, 5, 1)]
    while cases < count:
        n1, q, b = rng.choice(shapes); n = n1 * q ** b
        m = rng.randint(2, q - 1)                       # q > m
        if m > 7: m = 7
        kind = rng.randrange(3)
        if kind == 0: B = [rng.randrange(n) for _ in range(m)]
        elif kind == 1:                                 # few residues mod n', spread mod q^b: many vanishing sums mod n'
            base = [rng.randrange(n1) for _ in range(max(1, m // 2))]
            B = [crt(rng.choice(base), n1, rng.randrange(q ** b), q ** b) for _ in range(m)]
        else:                                           # cosets of a subgroup of n' with points spread mod q
            d = rng.choice([x for x in range(2, n1 + 1) if n1 % x == 0]); r = rng.randrange(n1)
            pts = [(r + (n1 // d) * j) % n1 for j in range(d)]
            B = [crt(pts[i % len(pts)], n1, rng.randrange(q ** b), q ** b) for i in range(m)]
        B1 = [x % n1 for x in B]
        for M in signings(m):
            a = good(n, B, M); c = good(n1, B1, M); signs += 1; goodn += a
            assert a == c, ('R1 FAILS', n1, q, b, B, M, a, c)
        cases += 1
    print(f'R1: {cases} multisets, {signs} signings (of which {goodn} good on the large group): the two sides agree in every case', flush=True)

def digits(x, p, a): return [(x // p ** i) % p for i in range(a)]
def undig(d, p): return sum(v * p ** i for i, v in enumerate(d))

def test_R2(rng, count):
    cases = 0; signs = 0; goodn = 0
    shapes = [(3, 2, 1), (3, 2, 5), (3, 3, 1), (3, 3, 5), (5, 2, 1), (5, 2, 3), (3, 2, 7), (3, 4, 1), (5, 2, 9), (3, 3, 7), (7, 2, 3)]
    while cases < count:
        p, a, n2 = rng.choice(shapes); n = p ** a * n2; t = rng.randint(1, a)
        m = rng.randint(2, 6)
        # elements as (digits of the p-part, residue mod n''); the digit of index t-1 is made a function of the lower digits
        f = {}
        B = []; Bt = []
        for _ in range(m):
            d = [rng.randrange(p) for _ in range(a)]
            if rng.random() < 0.6 and B:                # share a prefix with an earlier element, so that there is some structure
                e = digits(B[rng.randrange(len(B))] % p ** a, p, a); k = rng.randint(0, a); d[:k] = e[:k]
            key = tuple(d[:t - 1]); d[t - 1] = f.setdefault(key, d[t - 1])
            r = rng.randrange(n2)
            B.append(crt(undig(d, p), p ** a, r, n2) if n2 > 1 else undig(d, p))
            dt = d[:t - 1] + d[t:]
            Bt.append((crt(undig(dt, p), p ** (a - 1), r, n2) if n2 > 1 else undig(dt, p)) if a > 1 else r)
        for i in range(m):                              # the hypothesis, checked
            for j in range(i):
                if (B[i] - B[j]) % p ** (t - 1) == 0: assert (B[i] - B[j]) % p ** t == 0
        nt = n // p
        for M in signings(m):
            x = good(n, B, M); y = good(nt, Bt, M); signs += 1; goodn += x
            assert x == y, ('R2 FAILS', p, a, n2, t, B, Bt, M, x, y)
        cases += 1
    print(f'R2: {cases} multisets, {signs} signings (of which {goodn} good): the two sides agree in every case', flush=True)

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); count = int(sys.argv[2])
    test_R1(rng, count); test_R2(rng, count)
