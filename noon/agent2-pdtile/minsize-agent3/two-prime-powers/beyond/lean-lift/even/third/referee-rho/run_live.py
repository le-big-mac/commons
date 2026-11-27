# Two small claims of the referee's report.
# (1) A level at which no class is divided (both halves nonempty) can be dropped: if it is bad, level 0 is bad;
#     deleting that binary digit from every element gives a multiset with the same rho_2.  So a multiset of m elements
#     has the rho_2 of a multiset on Z_(2^(m-1)).
# (2) 2^m p_(m-1) = 4 J_(m-2), J the Jacobsthal numbers 0, 1, 1, 3, 5, 11, 21, ...
import random, itertools
from fractions import Fraction
from ref_lib import p, rho, bad_levels

random.seed(5)
J = [0, 1]
for i in range(2, 40):
    J.append(J[-1] + 2 * J[-2])
for m in range(2, 40):
    assert (1 << m) * p(m - 1) == 4 * J[m - 2]
for r in range(1, 40):
    assert p(r) == Fraction(J[r - 1], 2 ** (r - 1))
    assert p(r + 1) == (p(r) + p(r - 1)) / 2
assert Fraction(1, 3) + Fraction(2, 3) * Fraction(-1, 2) ** (-1) == -1
print("2^m p_(m-1) = 4 J_(m-2) for m = 2..39; p_r = J_(r-1)/2^(r-1); p_(r+1) = (p_r + p_(r-1))/2: ok")


def drop_dead_levels(B, k):
    B = list(B)
    j = 1
    while j <= k:
        cl = {}
        for b in B:
            cl.setdefault(b % (1 << (j - 1)), set()).add((b >> (j - 1)) & 1)
        if all(len(v) == 1 for v in cl.values()):
            B = [(b % (1 << (j - 1))) + ((b >> j) << (j - 1)) for b in B]
            k -= 1
        else:
            j += 1
    return sorted(B), k


n = 0; fail = 0; deepest = 0; implied = 0
for trial in range(20000):
    k = random.randint(1, 9); m = random.randint(1, 8)
    if random.random() < 0.5:
        pool = [random.randrange(1 << k) for _ in range(random.randint(1, 4))]
        B = sorted(random.choice(pool) for _ in range(m))
    else:
        B = sorted(random.randrange(1 << k) for _ in range(m))
    B2, k2 = drop_dead_levels(B, k)
    n += 1
    deepest = max(deepest, k2 - (len(B) - 1))
    if rho(B, k) != rho(B2, k2):
        fail += 1
    if trial < 1500:
        # a bad level at which no class is divided forces level 0 bad
        for eps in itertools.product((1, -1), repeat=m):
            bad = bad_levels(B, k, eps)
            for j in bad:
                if j >= 1:
                    cl = {}
                    for b in B:
                        cl.setdefault(b % (1 << (j - 1)), set()).add((b >> (j - 1)) & 1)
                    if all(len(v) == 1 for v in cl.values()):
                        implied += 1
                        if 0 not in bad:
                            fail += 1
print(f"{n} random multisets (k <= 9, m <= 8): rho_2 unchanged by dropping the undivided levels; "
      f"levels left minus (m - 1), largest: {deepest}; (signing, bad undivided level) pairs with level 0 bad: {implied}; failures: {fail}")
