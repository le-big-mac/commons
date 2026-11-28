"""Recomputations for the reading of the four paragraphs of 28 November (exact integers, every choice of signs).

A marking is a list of hours on the clock of n hours.  Signed marks balance at a divisor d of n (1 included) when
the cyclotomic polynomial Phi_d divides sum(sign * X^hour); a choice of signs is good when there is no balance at
any divisor of n, bad otherwise.

Severe test at d (the page's words: "they can be brought to balance there by adding weights three at a time"):
the weights at the d points of the walk, taken modulo 3, agree with some integer weights that balance at d.
Two independent ways are used for it:
  (a) remainder of the signed polynomial modulo Phi_d has all coefficients divisible by 3;
  (b) for d = 1: number of pluses minus number of minuses divisible by 3; for d a prime p: the p weights are all
      equal modulo 3; for d = p*q: the p-by-q table of weights (point j at row j mod p, column j mod q) is, modulo 3,
      a sum of a function of the row and a function of the column.  (No cyclotomic polynomial is used in (b).)
"""
import itertools, sys
from fractions import Fraction
from math import gcd


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def polymul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


def polydivmod(a, b):
    """a, b integer coefficient lists, lowest degree first; b monic."""
    a = a[:]
    q = [0] * max(1, len(a) - len(b) + 1)
    for k in range(len(a) - len(b), -1, -1):
        c = a[k + len(b) - 1]
        q[k] = c
        if c:
            for i, y in enumerate(b):
                a[k + i] -= c * y
    return q, a[:len(b) - 1]


_phi = {}


def cyclotomic(d):
    if d not in _phi:
        p = [-1] + [0] * (d - 1) + [1]          # X^d - 1
        for e in divisors(d):
            if e < d:
                p, rem = polydivmod(p, cyclotomic(e))
                assert not any(rem)
        _phi[d] = p
    return _phi[d]


_red = {}


def red_rows(n, d):
    """for each hour h < n: remainder of X^h modulo Phi_d, as a tuple of phi(d) integers."""
    if (n, d) not in _red:
        ph = cyclotomic(d)
        rows = []
        for h in range(n):
            _, r = polydivmod([0] * h + [1], ph) if h >= len(ph) - 1 else (None, ([0] * h + [1] + [0] * (len(ph) - 2 - h)))
            r = list(r) + [0] * (len(ph) - 1 - len(r))
            rows.append(tuple(r))
        _red[(n, d)] = rows
    return _red[(n, d)]


def signings(m):
    """all sign vectors with the first sign +; a global change of sign changes nothing, so shares are the same."""
    for bits in range(2 ** (m - 1)):
        yield [1] + [1 if (bits >> i) & 1 else -1 for i in range(m - 1)]


def balances(n, d, hours, signs):
    rows = red_rows(n, d)
    k = len(rows[0])
    for c in range(k):
        if sum(s * rows[h][c] for h, s in zip(hours, signs)):
            return False
    return True


def bad_count(n, hours, divs=None):
    """number of sign choices (first sign +) with a balance at some divisor in divs (default: all divisors of n)."""
    divs = divs or divisors(n)
    m = len(hours)
    return sum(1 for s in signings(m) if any(balances(n, d, hours, s) for d in divs))


def good_share(n, hours):
    m = len(hours)
    return Fraction(2 ** (m - 1) - bad_count(n, hours), 2 ** (m - 1))


def severe_a(n, d, hours, signs):
    rows = red_rows(n, d)
    k = len(rows[0])
    return all(sum(s * rows[h][c] for h, s in zip(hours, signs)) % 3 == 0 for c in range(k))


def severe_b(n, d, hours, signs):
    w = [0] * d
    for h, s in zip(hours, signs):
        w[h % d] += s
    if d == 1:
        return w[0] % 3 == 0
    fac = [p for p in range(2, d + 1) if d % p == 0 and all(p % q for q in range(2, p))]
    if fac == [d]:
        return len({x % 3 for x in w}) == 1
    if len(fac) == 2 and fac[0] * fac[1] == d:
        p, q = fac
        t = {}
        for j in range(d):
            t[(j % p, j % q)] = w[j]
        return all((t[(x, y)] - t[(x, 0)] - t[(0, y)] + t[(0, 0)]) % 3 == 0 for x in range(p) for y in range(q))
    raise ValueError(d)


def part1():
    print("PART 1. The examples.")
    ex = [(12, [0, 1, 2]), (2, [0, 0, 0, 1]), (30, [0, 1, 2, 3, 9]), (6, [0, 0, 1, 2, 2, 4]),
          (210, [0, 3, 9, 12, 32, 141, 202]), (6, [0, 0, 0, 0, 1, 2, 2, 4])]
    for n, hs in ex:
        m = len(hs)
        g = good_share(n, hs)
        odd = n
        while odd % 2 == 0:
            odd //= 2
        back = [h % odd for h in hs]
        b_odd = Fraction(bad_count(odd, back), 2 ** (m - 1))
        print(f"  clock {n:3d}, marks {hs}: good ways {g * 2 ** m} of {2 ** m} = {g};"
              f" wound back onto {odd}: bad share {b_odd}; 1 - 2*that = {1 - 2 * b_odd}")
    # the clock of 2 hours with all 16 signings written out, no symmetry used
    hs = [0, 0, 0, 1]
    good = 0
    for s in itertools.product((1, -1), repeat=4):
        at1 = sum(s) == 0
        at2 = sum(x * (-1) ** h for x, h in zip(s, hs)) == 0
        good += not (at1 or at2)
    print("  clock 2, marks 0,0,0,1, all 16 choices by hand rule (sum of signs; sum with the odd hour turned):", good, "good of 16")


def part2():
    print("PART 2. The clock of 35 hours, marks 0,1,2,3,4,5,20: falls that fail the severe test at some divisor.")
    n, hs = 35, [0, 1, 2, 3, 4, 5, 20]
    m = len(hs)
    fa = fb = 0
    per = {d: 0 for d in divisors(n)}
    plain = 0
    for s in itertools.product((1, -1), repeat=m):
        a = [severe_a(n, d, hs, s) for d in divisors(n)]
        b = [severe_b(n, d, hs, s) for d in divisors(n)]
        assert a == b, (s, a, b)
        fa += any(a)
        fb += any(b)
        for d, x in zip(divisors(n), a):
            per[d] += x
        plain += any(balances(n, d, hs, list(s)) for d in divisors(n))
    print(f"  fail somewhere: {fa} of {2 ** m} = {Fraction(fa, 2 ** m)} (both ways agree: {fa == fb}); at each divisor: {per}")
    print(f"  for comparison, plain balance somewhere: {plain} of {2 ** m} = {Fraction(plain, 2 ** m)}")
    print(f"  3 in 8 would be {Fraction(3, 8) * 2 ** m} of {2 ** m}")


def multisets_with_zero(n, m):
    for rest in itertools.combinations_with_replacement(range(n), m - 1):
        yield [0] + list(rest)


def part3():
    print("PART 3. Small clocks, every marking that contains hour 0 (turning the clock changes nothing).")
    print("  odd clocks: largest share of bad falls")
    for m, ns in ((3, (3, 5, 7, 9, 15, 21)), (4, (3, 5, 7, 9, 15)), (5, (3, 5, 9, 15)), (6, (3, 5, 9)), (7, (3, 9))):
        for n in ns:
            worst = max(bad_count(n, hs) for hs in multisets_with_zero(n, m))
            print(f"    marks {m}, clock {n:2d}: {Fraction(worst, 2 ** (m - 1))}")
    print("  even clocks: least share of good ways, and the statement about all the ladders (bad <= 2 * bad of the marks wound back onto the odd part)")
    for m, ns in ((3, (2, 4, 6, 8, 10, 12, 18)), (4, (2, 4, 6, 10, 12)), (5, (2, 4, 6, 10, 12)), (6, (2, 6, 12)), (7, (2, 6)), (8, (2, 6))):
        for n in ns:
            odd = n
            while odd % 2 == 0:
                odd //= 2
            least = None
            ok = True
            cnt = 0
            for hs in multisets_with_zero(n, m):
                cnt += 1
                b = bad_count(n, hs)
                b_odd = bad_count(odd, [h % odd for h in hs])
                b_odd_div = bad_count(n, hs, [d for d in divisors(n) if d % 2])
                if b_odd != b_odd_div or b > 2 * b_odd:
                    ok = False
                g = Fraction(2 ** (m - 1) - b, 2 ** (m - 1))
                if least is None or g < least[0]:
                    least = (g, hs)
            print(f"    marks {m}, clock {n:2d}: {cnt} markings; least good share {least[0]} at {least[1]}; ladders statement and winding back hold: {ok}")


if __name__ == "__main__":
    which = sys.argv[1:] or ["1", "2", "3"]
    if "1" in which:
        part1()
    if "2" in which:
        part2()
    if "3" in which:
        part3()
