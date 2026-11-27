# Self-check: the fast count against the literal one-signing-at-a-time count; p_r against a direct count;
# the numbers quoted in the statement.
import sys, random, itertools
from fractions import Fraction
sys.path.insert(0, sys.path[0])
from ref_lib import p, rho, rho_slow, bad_levels

random.seed(20261127)
# p_r is the probability that r signs sum to 0 mod 3
for r in range(0, 15):
    c = sum(1 for e in itertools.product((1, -1), repeat=r) if sum(e) % 3 == 0)
    assert Fraction(c, 2 ** r) == p(r), r
print("p_r = share of sign vectors of length r with sum = 0 mod 3: r = 0..14 ok;",
      [str(p(r)) for r in range(8)])
# (F1)
for a in range(1, 30):
    for b in range(1, 30):
        assert p(a + b - 1) == (1 - p(a)) * p(b) + p(a) * p(b - 1)
print("(F1) for 1 <= a, b <= 29 ok")
# end inequality of (B2), every n
for n in range(1, 60):
    from math import comb
    lhs = Fraction(1, 2 ** n) * sum(comb(n, u) * p(u - 1) for u in range(1, n))
    closed = Fraction(1, 3) + Fraction(2, 3) / 2 ** n - Fraction(4, 3) / 4 ** n + Fraction(4, 3) * (-1) ** n / 4 ** n
    assert lhs == closed, n
    assert lhs >= p(2 * n - 1)
    assert (lhs == p(2 * n - 1)) == (n == 1)
print("(B2) closed form of the sum and the last inequality, n = 1..59 ok; equality only n = 1")
n_cmp = 0
for trial in range(3000):
    k = random.randint(0, 5)
    m = random.randint(1, 9)
    kind = random.random()
    if kind < 0.3:
        B = [random.randrange(1 << k) for _ in range(m)]
    elif kind < 0.6:
        pool = [random.randrange(1 << k) for _ in range(random.randint(1, 3))]
        B = [random.choice(pool) for _ in range(m)]
    else:
        B = random.sample(range(1 << k), min(m, 1 << k))
    B = sorted(B)
    a = rho(B, k)
    b = rho_slow(B, k)
    assert a == b, (B, k, a, b)
    n_cmp += 1
print("fast count == literal count on", n_cmp, "random multisets (k <= 5, m <= 9)")
# statement's side remarks
assert rho([0, 1], 1) == 0 and rho([3, 3], 2) == Fraction(1, 2) and rho([5], 3) == 1
assert rho_slow([], 3) == 0
print("pair of different elements 0, two equal elements 1/2, one element 1, empty 0: ok")
