"""Reader's checks of the page 'signs-where-it-stands' (exact integer arithmetic)."""
from fractions import Fraction as F
from itertools import product
from math import comb, sqrt, pi, gcd


def polydivmod_exact(num, den):
    """num, den integer coefficient lists (low degree first), den monic. Returns remainder."""
    num = num[:]
    dd = len(den) - 1
    for i in range(len(num) - 1, dd - 1, -1):
        c = num[i]
        if c:
            for j in range(dd + 1):
                num[i - dd + j] -= c * den[j]
    return num[:dd] if dd > 0 else []


def polydiv_quot(num, den):
    num = num[:]
    dd = len(den) - 1
    q = [0] * (len(num) - dd)
    for i in range(len(num) - 1, dd - 1, -1):
        c = num[i]
        q[i - dd] = c
        if c:
            for j in range(dd + 1):
                num[i - dd + j] -= c * den[j]
    assert not any(num[:dd]), "inexact"
    return q


_cyc = {}


def cyclo(d):
    if d in _cyc:
        return _cyc[d]
    p = [-1] + [0] * (d - 1) + [1]  # X^d - 1
    for e in range(1, d):
        if d % e == 0:
            p = polydiv_quot(p, cyclo(e))
    _cyc[d] = p
    return p


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def bad_count(B, n):
    """number of signings of the multiset B on Z_n that are bad at some d | n (exact)."""
    m = len(B)
    ds = divisors(n)
    bad = 0
    for signs in product((1, -1), repeat=m):
        isbad = False
        for d in ds:
            # fold modulo X^d - 1, then remainder modulo Phi_d
            f = [0] * d
            for s, b in zip(signs, B):
                f[b % d] += s
            r = polydivmod_exact(f, cyclo(d))
            if not any(r):
                isbad = True
                break
        if isbad:
            bad += 1
    return bad


def odd_part(n):
    while n % 2 == 0:
        n //= 2
    return n


print("== the six examples of section 17 (and the page's {0,0,0,1} on Z_2) ==")
examples = [
    (3, [0, 1, 2], 12),
    (4, [0, 0, 0, 1], 2),
    (5, [0, 1, 2, 3, 9], 30),
    (6, [0, 0, 1, 2, 2, 4], 6),
    (7, [0, 3, 9, 12, 32, 141, 202], 210),
    (8, [0, 0, 0, 0, 1, 2, 2, 4], 6),
]
beta = {3: F(1, 4), 4: F(3, 8), 5: F(1, 4), 6: F(11, 32), 7: F(7, 32), 8: F(39, 128)}
least = {3: F(1, 2), 4: F(1, 4), 5: F(1, 2), 6: F(5, 16), 7: F(9, 16), 8: F(25, 64)}
for m, B, n in examples:
    bad = bad_count(B, n)
    good_share = 1 - F(bad, 2 ** m)
    n1 = odd_part(n)
    B1 = [b % n1 for b in B]
    bad1 = bad_count(B1, n1)
    print(m, B, "on Z_%d" % n, "good share", good_share, "page", least[m], good_share == least[m],
          "| reduction mod", n1, "bad share", F(bad1, 2 ** m), "beta", beta[m], F(bad1, 2 ** m) == beta[m],
          "| 1-2beta", 1 - 2 * beta[m] == least[m], "| twice:", bad <= 2 * bad1)

print("== pairs: exceptional iff 2^k does not divide a-b; even order ==")
ok = True
for n in range(1, 41):
    k2 = n // odd_part(n)
    for a in range(n):
        for b in range(a, n):
            bad = bad_count([a, b], n)
            exc = ((a - b) % k2 != 0)
            order = n // gcd(n, (a - b) % n) if (a - b) % n else 1
            if (bad == 4) != exc or exc != (order % 2 == 0):
                ok = False
                print("MISMATCH", n, a, b, bad, exc, order)
print("pairs on Z_n, n <= 40: no good signing exactly for the exceptional pairs, = even order:", ok)

print("== beta(2) and m copies ==")
for n in (1, 3, 5, 9, 15):
    s = set()
    for a in range(n):
        s.add(F(bad_count([0, a], n), 4))
    print("pairs on Z_%d: bad shares" % n, sorted(s))
for m in (2, 4, 6, 8, 10):
    print("m copies of 0 on Z_3, m =", m, F(bad_count([0] * m, 3), 2 ** m), "C(m,m/2)/2^m =", F(comb(m, m // 2), 2 ** m))
for m in (3, 5, 7):
    print("m copies of 0 on Z_3, m =", m, F(bad_count([0] * m, 3), 2 ** m))

print("== arithmetic ==")
print("sqrt(2/pi) =", sqrt(2 / pi))
print("sqrt(2/pi)*(1+2.6251) =", sqrt(2 / pi) * 3.6251, "(page 2.893)")
print("2*1.56 =", 2 * 1.56)
K_even = F(78764625, 67108864)
K_odd = F(337, 512)
print("K even", float(K_even), "-> limit", sqrt(2 / pi) * float(K_even), "(page 1.1737, 0.9364)")
print("K odd", float(K_odd), "-> limit", sqrt(2 / pi) * float(K_odd), "(page 0.658, 0.5251)")
for m in (2, 4, 6, 8):
    b = {2: F(1, 2), 4: F(3, 8), 6: F(11, 32), 8: F(39, 128)}[m]
    print("m =", m, "beta*sqrt(m) =", float(b) * sqrt(m))
for m in (100, 1000, 10000, 10 ** 6):
    print("m =", m, "C(m,m/2)/2^m*sqrt(m) =", comb(m, m // 2) / 2 ** m * sqrt(m))
print("C(m,floor(m/2))/2^m for m=3..8:", [str(F(comb(m, m // 2), 2 ** m)) for m in range(3, 9)])
print("odd m with 1/sqrt(m) <= 1/4: m >= 16; 1/sqrt(9)=", 1 / 3, " 1/sqrt(15)=", 1 / sqrt(15))
print("1-3.12/sqrt(m) vs 17/64 (even m>=10):", [(m, round(1 - 3.12 / sqrt(m), 4)) for m in (16, 18, 20, 22)], 17 / 64)
print("1-2/sqrt(m) vs 1/2 (odd):", [(m, round(1 - 2 / sqrt(m), 4)) for m in (15, 17)])
print("47/128 =", 47 / 128, " 3/8 =", 3 / 8)
