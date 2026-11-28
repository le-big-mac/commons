# Reader's check of section 17: the six examples said to attain the least shares,
# the arithmetic 1 - 2*beta, and the sum of 2^(-phi(m)) over odd m >= 3.
# All signings, exact integer arithmetic; "bad at d" = Phi_d divides the signed mask.
from fractions import Fraction as F
from itertools import product
from math import gcd


def polydivmod(a, b):
    a = a[:]
    q = [0] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and any(a):
        if a[-1] == 0:
            a.pop()
            continue
        c = a[-1] // b[-1]
        assert c * b[-1] == a[-1]
        k = len(a) - len(b)
        q[k] = c
        for i, bi in enumerate(b):
            a[k + i] -= c * bi
        a.pop()
    while a and a[-1] == 0:
        a.pop()
    return q, a


_cyc = {}


def cyclo(d):
    if d in _cyc:
        return _cyc[d]
    p = [-1] + [0] * (d - 1) + [1]
    for e in range(1, d):
        if d % e == 0:
            p, r = polydivmod(p, cyclo(e))
            assert not r
            while p and p[-1] == 0:
                p.pop()
    _cyc[d] = p
    return p


def shares(n, B):
    divs = [d for d in range(1, n + 1) if n % d == 0]
    m = len(B)
    good = 0
    badat = {d: 0 for d in divs}
    for eps in product((1, -1), repeat=m):
        S = [0] * n
        for e, b in zip(eps, B):
            S[b % n] += e
        bad = False
        for d in divs:
            # reduce S modulo X^d - 1 first (Phi_d | X^d - 1), then modulo Phi_d
            T = [0] * d
            for i, c in enumerate(S):
                T[i % d] += c
            _, r = polydivmod(T, cyclo(d))
            if not r:
                badat[d] += 1
                bad = True
        if not bad:
            good += 1
    return F(good, 2 ** m), {d: c for d, c in badat.items() if c}


examples = [
    (12, [0, 1, 2], F(1, 2)),
    (2, [0, 0, 0, 1], F(1, 4)),
    (30, [0, 1, 2, 3, 9], F(1, 2)),
    (6, [0, 0, 1, 2, 2, 4], F(5, 16)),
    (210, [0, 3, 9, 12, 32, 141, 202], F(9, 16)),
    (6, [0, 0, 0, 0, 1, 2, 2, 4], F(25, 64)),
]
for n, B, want in examples:
    g, at = shares(n, B)
    print(f"Z_{n} {B}: good share {g} (section 17 says {want}) {'OK' if g == want else 'DIFFERENT'}; bad at d: {at}")

# the odd reductions of the even-modulus examples: bad share on the odd part
for n, B in [(15, [0, 1, 2, 3, 9]), (3, [0, 0, 1, 2, 2, 4]), (105, [0, 3, 9, 12, 32, 141, 202]),
             (3, [0, 0, 0, 0, 1, 2, 2, 4]), (3, [0, 1, 2]), (1, [0, 0, 0, 1])]:
    g, at = shares(n, [b % n for b in B])
    print(f"  reduction on Z_{n}: bad share {1 - g}")

# other examples named in the texts
for n, B in [(15, [6, 8, 9, 10, 12]), (105, [0, 3, 9, 12, 32, 36, 97]), (105, [0, 1, 2, 3, 39, 75, 90]),
             (3, [0, 0, 1, 1, 2, 2]), (15, [3, 6, 9, 12, 5, 10]), (3, [0, 0, 0, 0, 1, 1, 2, 2]),
             (9, [0, 0, 1, 1, 2, 2, 3, 3, 6, 6])]:
    g, at = shares(n, B)
    print(f"  Z_{n} {B}: bad share {1 - g}")

# the table: 1 - 2*beta
beta = {3: F(1, 4), 4: F(3, 8), 5: F(1, 4), 6: F(11, 32), 7: F(7, 32), 8: F(39, 128), 'odd>=9': F(1, 4), 'even>=10': F(47, 128)}
for k, b in beta.items():
    print(k, b, '->', 1 - 2 * b)


def phi(m):
    return sum(1 for k in range(1, m + 1) if gcd(k, m) == 1)


s = F(0)
for m in range(3, 3002, 2):
    s += F(1, 2 ** phi(m))
print("sum of 2^(-phi(m)), odd m from 3 to 3001:", float(s))
s2 = sum(F(1, 2 ** phi(m)) for m in range(3, 200, 2))
print("to 199:", float(s2))
# c_m = C(m, floor(m/2))/2^m at most 3/8 for m >= 3
from math import comb
print([str(F(comb(m, m // 2), 2 ** m)) for m in range(1, 13)])
