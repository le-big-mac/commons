# Statements 1 and 2 (Erdos's bound for the problem of Littlewood and Offord), tested by exact counting.
# For a list a of nonzero integers (or pairs of integers = Gaussian integers), the number of signings with a given
# signed sum is found for every value at once by doubling a table; the largest count is compared with C(m, m//2).
# usage: python lo.py
import itertools, random, sys
from collections import Counter
from math import comb


def table(a):
    """Counter: value -> number of signings eps with sum eps_i a_i = value.  a: ints or pairs of ints."""
    pair = len(a) > 0 and isinstance(a[0], tuple)
    t = Counter({((0, 0) if pair else 0): 1})
    for x in a:
        u = Counter()
        if pair:
            for (p, q), c in t.items():
                u[(p + x[0], q + x[1])] += c
                u[(p - x[0], q - x[1])] += c
        else:
            for s, c in t.items():
                u[s + x] += c
                u[s - x] += c
        t = u
    return t


def brute(a):
    """the same by listing all signings (second instrument, small m only)"""
    pair = len(a) > 0 and isinstance(a[0], tuple)
    t = Counter()
    for eps in itertools.product((1, -1), repeat=len(a)):
        if pair:
            t[(sum(e * x[0] for e, x in zip(eps, a)), sum(e * x[1] for e, x in zip(eps, a)))] += 1
        else:
            t[sum(e * x for e, x in zip(eps, a))] += 1
    return t


def main():
    rng = random.Random(20261128)
    M = 12
    # second instrument agrees with the first
    nb = 0
    for _ in range(400):
        m = rng.randrange(0, 9)
        a = [rng.choice([-3, -2, -1, 1, 2, 3]) for _ in range(m)]
        assert table(a) == brute(a) or (m == 0 and table(a)[0] == 1 and brute(a)[0] == 1)
        b = [rng.choice([(1, 0), (0, 1), (1, 1), (-1, 2), (2, -1), (0, -3)]) for _ in range(m)]
        if m:
            assert table(b) == brute(b)
        nb += 2
    print("doubling table against plain listing of signings: %d lists agree" % nb)
    assert sum(table([1, 2, 3, 4, 5]).values()) == 32

    best = {("real", m): (0, None) for m in range(M + 1)}
    best.update({("gauss", m): (0, None) for m in range(M + 1)})
    ncase = Counter()
    eqcases = {}

    def see(kind, a):
        m = len(a)
        t = table(a)
        v, c = max(t.items(), key=lambda kv: kv[1])
        ncase[(kind, m)] += 1
        if c > comb(m, m // 2):
            print("VIOLATION", kind, a, v, c, comb(m, m // 2))
            sys.exit(1)
        if c > best[(kind, m)][0]:
            best[(kind, m)] = (c, (list(a), v))
        if c == comb(m, m // 2):
            eqcases.setdefault((kind, m), (list(a), v))

    for m in range(M + 1):
        # structured, real
        see("real", [1] * m)
        see("real", [-1] * m)
        see("real", [7] * m)
        see("real", [(-1) ** i for i in range(m)])
        see("real", [i + 1 for i in range(m)])
        see("real", [2 ** i for i in range(m)])
        see("real", [1] * (m // 2) + [2] * (m - m // 2))
        see("real", [1] * (m - 1) + [2] * (1 if m else 0))
        see("real", [1] * (m - 1) + [3] * (1 if m else 0))
        see("real", [1 + (i % 3) for i in range(m)])
        # random, real
        for R in (1, 2, 3, 5, 10, 100, 10 ** 6):
            for _ in range(300):
                see("real", [rng.choice([-1, 1]) * rng.randint(1, R) for _ in range(m)])
        # structured, Gaussian
        see("gauss", [(1, 1)] * m)
        see("gauss", [(0, 1)] * m)
        see("gauss", [(1, 0)] * (m // 2) + [(0, 1)] * (m - m // 2))
        see("gauss", [[(1, 0), (0, 1), (-1, 0), (0, -1)][i % 4] for i in range(m)])
        see("gauss", [[(1, 0), (0, 1), (1, 1)][i % 3] for i in range(m)])
        see("gauss", [(1, i) for i in range(m)])
        for R in (1, 2, 3, 10, 1000):
            for _ in range(300):
                a = []
                while len(a) < m:
                    z = (rng.randint(-R, R), rng.randint(-R, R))
                    if z != (0, 0):
                        a.append(z)
                see("gauss", a)
    # exhaustive: all multisets from small alphabets
    for m in range(0, 11):
        for a in itertools.combinations_with_replacement([1, 2, 3, 4, 5], m):
            see("real", list(a))
    for m in range(0, 8):
        for a in itertools.combinations_with_replacement([-2, -1, 1, 2, 3, 5], m):
            see("real", list(a))
    G = [(1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, 2)]
    for m in range(0, 9):
        for a in itertools.combinations_with_replacement(G, m):
            see("gauss", list(a))

    print()
    print("kind   m  lists  largest count of one value  C(m,m//2)  ratio  equality   a case with the largest count")
    for kind in ("real", "gauss"):
        for m in range(M + 1):
            c, ex = best[(kind, m)]
            b = comb(m, m // 2)
            print("%-5s %2d %6d %10d %18d %8.4f  %-8s  %s" % (
                kind, m, ncase[(kind, m)], c, b, c / b, "yes" if c == b else "no", ex if m <= 6 else str(ex)[:60]))
    print()
    print("largest ratio, real: %.4f; Gaussian: %.4f; no violation in %d lists" % (
        max(best[("real", m)][0] / comb(m, m // 2) for m in range(M + 1)),
        max(best[("gauss", m)][0] / comb(m, m // 2) for m in range(M + 1)), sum(ncase.values())))

    # the hypothesis a_i != 0 is needed: with one zero the count at v = 0 can exceed the bound
    print()
    print("with zeros allowed (outside the hypothesis):")
    for a in ([0], [0, 0], [0, 1, 1], [0, 0, 1, 1], [0, 1, 1, 1, 1]):
        t = table(a)
        v, c = max(t.items(), key=lambda kv: kv[1])
        m = len(a)
        print("  a = %s: value %s is taken %d times, C(%d,%d) = %d  %s" % (
            a, v, c, m, m // 2, comb(m, m // 2), "EXCEEDS" if c > comb(m, m // 2) else "within"))
    # m = 0 and m = 1
    print()
    print("m = 0: table", dict(table([])), " bound", comb(0, 0))
    print("m = 1, a = [5]: table", dict(table([5])), " bound", comb(1, 0))


main()
