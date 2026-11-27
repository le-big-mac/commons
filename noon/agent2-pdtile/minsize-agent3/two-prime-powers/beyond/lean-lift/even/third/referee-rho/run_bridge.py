# The bridge of lemma-rho.md: for a multiset B on Z_n, n = 2^k n', a signing is "3-bad at 2^j" (S(w) in 3 Z[w] for w of
# order 2^j, i.e. the remainder of S(X) = sum eps_b X^b modulo Phi_(2^j)(X) has all coefficients divisible by 3)
# iff "level j is bad" for the residues of B modulo 2^k.  Exact integer arithmetic; Phi_d computed from
# X^d - 1 = product of Phi_e over e | d by exact division, not typed in.
# Also the consequence for n = 2^k 3^a: a signing with no bad level is good on Z_n (S(z) != 0 for every z of order d | n).
import sys, random, itertools
from fractions import Fraction
from collections import Counter
from ref_lib import bad_levels, p

random.seed(1127)


def polydivmod(a, b):
    """a, b integer coefficient lists (low degree first), b monic. Returns (q, r)."""
    a = a[:]
    db = len(b) - 1
    q = [0] * max(1, len(a) - db)
    for i in range(len(a) - 1, db - 1, -1):
        c = a[i]
        if c:
            q[i - db] = c
            for t in range(db + 1):
                a[i - db + t] -= c * b[t]
    return q, a[:db]


_phi = {}


def phi(d):
    if d not in _phi:
        a = [-1] + [0] * (d - 1) + [1]
        for e in range(1, d):
            if d % e == 0:
                a, r = polydivmod(a, phi(e))
                assert not any(r)
                while len(a) > 1 and a[-1] == 0:
                    a.pop()
        _phi[d] = a
    return _phi[d]


def rem(B, eps, n, d):
    S = [0] * n
    for b, e in zip(B, eps):
        S[b % n] += e
    return polydivmod(S, phi(d))[1]


for j in range(0, 6):
    ph = phi(1 << j)
    expect = [-1, 1] if j == 0 else [1] + [0] * ((1 << (j - 1)) - 1) + [1]
    assert ph == expect
assert phi(12) == [1, 0, -1, 0, 1] and phi(9) == [1, 0, 0, 1, 0, 0, 1]
print("Phi_(2^j) = X^(2^(j-1)) + 1 for j = 1..5, Phi_1 = X - 1; Phi_9, Phi_12 as known: ok")

cnt = Counter(); fail = Counter()


def multisets(n, m, cap):
    total = 1
    for i in range(m):
        total = total * (n + i) // (i + 1)
    if total <= cap:
        yield from itertools.combinations_with_replacement(range(n), m)
    else:
        for _ in range(cap):
            yield tuple(sorted(random.randrange(n) for _ in range(m)))


# ---- the bridge, for n = 2^k n' with n' = 1, 3, 5, 7, 9, 15
for n in (1, 2, 4, 8, 16, 32, 6, 12, 24, 48, 10, 20, 40, 14, 28, 18, 36, 30, 60):
    k = 0
    while n % (1 << (k + 1)) == 0:
        k += 1
    N = 1 << k
    for m in range(1, 7):
        for B in multisets(n, m, 250 if n > 16 else 400):
            Br = [b % N for b in B]
            for eps in itertools.product((1, -1), repeat=m):
                bad = bad_levels(Br, k, eps)
                for j in range(0, k + 1):
                    three_bad = all(c % 3 == 0 for c in rem(B, eps, n, 1 << j))
                    cnt["bridge: (signing, j) pairs"] += 1
                    if three_bad != (j in bad):
                        fail["bridge"] += 1
                        if fail["bridge"] <= 5:
                            print("  bridge mismatch", n, B, eps, j)
    print(f"  bridge on Z_{n} (k = {k}) done; pairs so far {cnt['bridge: (signing, j) pairs']}, failures {fail['bridge']}", flush=True)

# ---- consequence: n = 2^k 3^a; signings with no bad level are good on Z_n; share of good >= rho_2 >= p_(m-1)
for n in (1, 2, 4, 8, 16, 3, 9, 6, 12, 24, 18, 36, 72, 54):
    k = 0
    while n % (1 << (k + 1)) == 0:
        k += 1
    N = 1 << k
    divs = [d for d in range(1, n + 1) if n % d == 0]
    worst = None
    for m in range(1, 7):
        for B in multisets(n, m, 150 if n > 12 else 300):
            Br = [b % N for b in B]
            g = 0; g3 = 0
            for eps in itertools.product((1, -1), repeat=m):
                good = all(any(rem(B, eps, n, d)) for d in divs)
                nobad = not bad_levels(Br, k, eps)
                g += good; g3 += nobad
                if nobad and not good:
                    fail["no bad level but not good on Z_n"] += 1
            cnt["consequence: multisets"] += 1
            if Fraction(g, 2 ** m) < p(m - 1):
                fail["share of good below p_(m-1)"] += 1
            if g == (2 ** m) * p(m - 1):
                cnt["consequence: share of good exactly p_(m-1)"] += 1
            # the pair remarks
            if m == 2:
                exceptional = (B[0] - B[1]) % N != 0
                if exceptional and g != 0:
                    fail["exceptional pair has a good signing"] += 1
                if not exceptional and g3 * 2 != 4:
                    fail["non-exceptional pair: rho_2 = 1/2"] += 1
    print(f"  consequence on Z_{n} done; multisets so far {cnt['consequence: multisets']}", flush=True)
print("counts:", dict(cnt))
print("failures:", dict(fail) if fail else "none")
