# Expected values for CheckEven.lean, worked out outside Lean from the plan's definitions.
from itertools import product
from fractions import Fraction


def sg(b):
    return 1 if b else -1


def csum(pos, val, eps, M, r, mod):
    s = sum(sg(eps[k]) * val[k] for k in range(len(pos)) if pos[k] % M == r)
    return s % mod if mod else s


def level_bad(pos, val, eps, j, mod):
    if j == 0:
        s = sum(sg(eps[k]) * val[k] for k in range(len(pos)))
        return (s % mod if mod else s) == 0
    i = j - 1
    return all(csum(pos, val, eps, 2 ** j, r, mod) == csum(pos, val, eps, 2 ** j, r + 2 ** i, mod)
               for r in range(2 ** i))


def counts(pos, val, K, mod):
    m = len(pos)
    anyb = 0
    zero = 0
    per = [0] * (K + 1)
    for eps in product([True, False], repeat=m):
        lv = [level_bad(pos, val, eps, j, mod) for j in range(K + 1)]
        anyb += any(lv)
        zero += lv[0]
        for j in range(K + 1):
            per[j] += lv[j]
    return anyb, zero, per


fams = [
    ("pair", [0, 1], [1, 1], 1, 0),
    ("f3a", [0, 1, 2], [1, 1, 1], 2, 0),
    ("f3b", [0, 0, 1], [1, 2, 1], 2, 3),
    ("f4a", [0, 1, 2, 3], [1, 1, 1, 1], 3, 0),
    ("f4b", [0, 0, 2, 5], [1, -1, 0, 2], 3, 0),
    ("f4c", [3, 3, 1, 5], [1, 1, 2, 2], 3, 3),
    ("f5a", [0, 1, 1, 2, 7], [1, 2, 3, 4, 1], 3, 5),
    ("f5b", [0, 4, 2, 6, 1], [1, 1, 1, 1, 0], 3, 0),
    ("f4d", [0, 0, 0, 1], [1, 1, 1, 1], 2, 3),
]
for name, pos, val, K, mod in fams:
    a, z, per = counts(pos, val, K, mod)
    print(name, "pos", pos, "val", val, "mod", mod, "K", K, "-> some level:", a, " level 0:", z, " per level:", per,
          " T holds:", a <= 2 * z)

# levelBad by hand: pos 0,1,2,3, values 1 in Z
for eps in ([True, True, False, False], [True, False, True, False]):
    print("eps", eps, [level_bad([0, 1, 2, 3], [1, 1, 1, 1], eps, j, 0) for j in range(4)])

# E1: the number of signings of m elements whose sum is divisible by 3
for m in range(0, 8):
    c = sum(1 for eps in product([1, -1], repeat=m) if sum(eps) % 3 == 0)
    lhs = 3 * c + (0 if m % 2 == 0 else 2)
    rhs = 2 ** m + (2 if m % 2 == 0 else 0)
    print("m", m, "count", c, "3*count", 3 * c, "equation holds:", lhs == rhs)


def factor(t):
    f = {}
    p = 2
    while p * p <= t:
        while t % p == 0:
            f[p] = f.get(p, 0) + 1
            t //= p
        p += 1
    if t > 1:
        f[t] = f.get(t, 0) + 1
    return f


def mu(t):
    if t <= 1:
        return 0
    return max((p - 1) * v for p, v in factor(t).items())


for T in ([5], [5, 7, 35], [5, 7, 25, 35, 175], [5, 7, 11, 25, 35, 55, 77, 175, 275, 385, 1925]):
    print(T, [mu(t) for t in T], sum(Fraction(1, 2) ** mu(t) for t in T))

# exceptional pairs: the additive order of a - b in Z_n
from math import gcd
for n, a, b in [(2, 0, 1), (4, 0, 1), (4, 0, 2), (4, 1, 1), (6, 0, 1), (6, 0, 2), (6, 0, 3), (6, 1, 3),
                (12, 0, 4), (12, 0, 3), (12, 0, 6), (12, 0, 8), (12, 0, 2), (12, 5, 1)]:
    o = n // gcd(n, (a - b) % n)
    print("n", n, "a", a, "b", b, "order of a-b:", o, "exceptional:", o % 2 == 0)
