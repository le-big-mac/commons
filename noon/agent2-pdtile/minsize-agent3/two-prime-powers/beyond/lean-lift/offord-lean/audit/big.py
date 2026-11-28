# Larger m (up to 26) for statements 3, 5, 7, where listing 2^m signings is too slow: count by class sums.
# Modulo X^N - 1 the mask of a signing is sum_r s_r X^r, s_r the signed sum over the elements with exponent = r mod N;
# s_r runs over -m_r, -m_r+2, .., m_r and is taken by C(m_r, (m_r+s_r)/2) signings of that class.  Badness at d | N
# depends on (s_r) only.  So the count is a weighted sum over the vectors (s_r), exact (Python integers for the
# weights via object arrays would be slow; the weights are < 2^63 for m <= 26, checked).
# First the method is compared with the listing of all signings (bad.py) for m <= 11.
# usage: python big.py SECONDS
import os, sys, random, time, itertools
from math import comb
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # the interpreter runs isolated (-I)
import bad


def class_count(sizes, N, want):
    """sizes: dict residue -> number of elements.  want: list of lists of divisors; returns for each list the number
    of signings bad at some divisor in it."""
    res = sorted(sizes)
    grids = [np.arange(-sizes[r], sizes[r] + 1, 2, dtype=np.int64) for r in res]
    wts = [np.array([comb(sizes[r], (sizes[r] + int(s)) // 2) for s in g], dtype=np.int64) for r, g in zip(res, grids)]
    mesh = np.meshgrid(*grids, indexing="ij") if res else []
    wmesh = np.meshgrid(*wts, indexing="ij") if res else []
    if not res:
        return [1 for _ in want]
    S = np.stack([x.ravel() for x in mesh], axis=1)        # vectors (s_r)
    W = np.ones(S.shape[0], dtype=np.int64)
    for x in wmesh:
        W = W * x.ravel()
    assert int(W.sum()) == 2 ** sum(sizes.values())
    alld = sorted(set(d for lst in want for d in lst))
    badat = {}
    for d in alld:
        T = bad.redtable(d)
        V = T[np.array(res, dtype=np.int64) % d]
        badat[d] = ~(S @ V).any(axis=1)
    out = []
    for lst in want:
        acc = np.zeros(S.shape[0], dtype=bool)
        for d in lst:
            acc |= badat[d]
        out.append(int(W[acc].sum()))
    return out


def sizes_of(e, N):
    s = {}
    for x in e:
        s[x % N] = s.get(x % N, 0) + 1
    return s


def random_sizes(N, m, rng, maxclasses):
    """class sizes: a few occupied classes, structured with respect to N"""
    divs = [c for c in bad.divisors(N) if c > 1]
    ncl = rng.randint(1, maxclasses)
    mode = rng.randrange(4)
    if mode == 0 or not divs:
        res = [rng.randrange(N) for _ in range(ncl)]
    elif mode == 1:
        c = rng.choice(divs)
        res = [(j * (N // c)) % N for j in range(min(c, ncl))]
    elif mode == 2:
        c1, c2 = rng.choice(divs), rng.choice(divs)
        res = [(rng.randrange(c1) * (N // c1) + rng.randrange(c2) * (N // c2)) % N for _ in range(ncl)]
    else:
        p = rng.choice(bad.prime_factors(N))
        s0 = rng.randrange(N)
        res = [(s0 + j * (N // p)) % N for j in range(p)][:ncl]
        if N % 2 == 0 and rng.random() < 0.5:
            res = res + [(r + N // 2) % N for r in res][:max(0, ncl - len(res))]
    res = list(dict.fromkeys(res))
    sizes = {r: 1 for r in res}
    left = m - len(res)
    if left < 0:
        res = res[:m]
        sizes = {r: 1 for r in res}
        left = 0
    # put the rest mostly on one class, or spread
    if rng.random() < 0.5 and res:
        sizes[res[0]] += left
    else:
        for _ in range(left):
            sizes[rng.choice(res)] += 1
    return sizes


def main():
    budget = float(sys.argv[1])
    rng = random.Random(11)
    # 1. the method against the listing of signings
    n = 0
    t0 = time.time()
    while time.time() - t0 < 20:
        n1 = rng.choice([1, 3, 5, 7, 9, 15])
        k = rng.randint(0, 3)
        N = 2 ** k * n1
        m = rng.randint(0, 11)
        e = bad.gen_exps(N, m, rng)
        divN = bad.divisors(N)
        c, per = bad.union_count(e, N)
        got = class_count(sizes_of(e, N), N, [divN] + [[d] for d in divN])
        assert got[0] == c, (e, N, got[0], c)
        for d, g in zip(divN, got[1:]):
            assert g == int(per[d].sum()), (e, N, d)
        n += 1
    print("class sums against listing of signings: %d (e, N) agree, union and each divisor" % n)

    # 2. larger m
    M0, M1 = 2, 26
    best7 = {}     # (n', m) -> (ratio, count, bound, sizes, k)
    best5 = {}     # m -> (count, sizes, k)
    best3 = {}     # m -> (count, sizes, d)
    twice = {0: (0,), 1: (0,)}
    ncases = 0

    def see(sizes, k, n1):
        nonlocal ncases
        if any(v < 0 for v in sizes.values()):
            return
        sizes = {r: v for r, v in sizes.items() if v > 0}
        N = 2 ** k * n1
        m = sum(sizes.values())
        divN = bad.divisors(N)
        div1 = bad.divisors(n1)
        got = class_count(sizes, N, [divN, div1] + [[d] for d in divN])
        ncases += 1
        c, c1 = got[0], got[1]
        C = comb(m, m // 2)
        rhs = 2 * len(div1) * C
        if c > rhs:
            print("VIOLATION of statement 7", sizes, k, n1, c, rhs)
            sys.exit(1)
        if c > 2 * c1:
            print("VIOLATION of card_exists_badAt_le", sizes, k, n1, c, c1)
            sys.exit(1)
        for d, g in zip(divN, got[2:]):
            if g > C:
                print("VIOLATION of statement 3", sizes, d, g, C)
                sys.exit(1)
            if d == 1 and m % 2 and g:
                print("VIOLATION of statement 4", sizes)
                sys.exit(1)
            if g > best3.get(m, (-1,))[0]:
                best3[m] = (g, dict(sizes), d)
        if n1 == 1:
            if m % 2 and c:
                print("VIOLATION of statement 6", sizes, k)
                sys.exit(1)
            if c > best5.get(m, (-1,))[0]:
                best5[m] = (c, dict(sizes), k)
        r = c / rhs
        if r > best7.get((n1, m), (-1,))[0]:
            best7[(n1, m)] = (r, c, rhs, dict(sizes), k)
        if c1 and c / c1 > twice[m % 2][0]:
            twice[m % 2] = (c / c1, c, c1, dict(sizes), k, n1)

    odd = [1, 3, 5, 7, 9, 15, 25, 27, 45]
    # structured cases
    for m in range(M0, M1 + 1):
        for k in range(0, 4):
            see({0: m - 1, 1: 1}, k, 1)
            see({0: m - 3, 1: 3}, k, 1)
            for n1 in odd:
                N = 2 ** k * n1
                see({0: m}, k, n1)
                if k:
                    see({0: m - 1, N // 2: 1}, k, n1)
                if n1 % 3 == 0:
                    see({0: m - 2, N // 3: 1, 2 * N // 3: 1}, k, n1)
                    if k:
                        see({0: m - 2, N // 6: 1, 2 * N // 6: 1}, k, n1)
                        see({0: m - 3, N // 6: 1, 2 * N // 6: 1, N // 2: 1}, k, n1)
                        see({0: m - 5, N // 6: 1, 2 * N // 6: 1, 3 * N // 6: 1, 4 * N // 6: 1, 5 * N // 6: 1}, k, n1)
    t0 = time.time()
    while time.time() - t0 < budget:
        n1 = rng.choice(odd)
        k = rng.randint(0, 3)
        m = rng.randint(M0, M1)
        sizes = random_sizes(2 ** k * n1, m, rng, 7)
        nvec = 1
        for v in sizes.values():
            nvec *= v + 1
        if nvec > 400000:
            continue
        see(sizes, k, n1)
    print("m from %d to %d: %d cases (class sizes; k <= 3; n' in %s)" % (M0, M1, ncases, odd))
    print()
    print("statement 3, largest count bad at one d, by m:")
    for m in range(M0, M1 + 1):
        g, sizes, d = best3[m]
        C = comb(m, m // 2)
        print("  m = %2d: %9d of C = %9d  ratio %.4f %s  sizes %s, d = %d%s" % (
            m, g, C, g / C, "equality" if g == C else "", sizes, d,
            ("  [= C(m-1,(m-1)/2)]" if m % 2 and g == comb(m - 1, (m - 1) // 2) else "")))
    print()
    print("statement 5 (n' = 1), largest count bad at some divisor of 2^k, by m:")
    for m in range(M0, M1 + 1):
        c, sizes, k = best5[m]
        rhs = 2 * comb(m, m // 2)
        print("  m = %2d: %9d of 2C = %9d  ratio %.4f %s  sizes %s, k = %d" % (
            m, c, rhs, c / rhs, "equality" if c == rhs else "", sizes, k))
    print()
    print("statement 7, largest ratio count / (2 d(n') C(m,m//2)) by n' (over m = %d..%d), and whether the bound is below 2^m there:" % (M0, M1))
    for n1 in odd:
        rows = [(best7[(n1, m)], m) for m in range(M0, M1 + 1) if (n1, m) in best7]
        (r, c, rhs, sizes, k), m = max(rows, key=lambda x: x[0][0])
        print("  n' = %2d: %.4f (%d / %d), m = %d, k = %d, sizes %s; bound %s 2^m" % (
            n1, r, c, rhs, m, k, sizes, "<" if rhs < 2 ** m else ">="))
    print("  the same restricted to m where the bound is below 2^m:")
    for n1 in odd:
        rows = [(best7[(n1, m)], m) for m in range(M0, M1 + 1) if (n1, m) in best7 and best7[(n1, m)][2] < 2 ** m]
        if not rows:
            print("  n' = %2d: bound >= 2^m for every m <= %d" % (n1, M1))
            continue
        (r, c, rhs, sizes, k), m = max(rows, key=lambda x: x[0][0])
        print("  n' = %2d: %.4f (%d / %d), m = %d, k = %d, sizes %s" % (n1, r, c, rhs, m, k, sizes))
    print()
    print("the proved 'twice', largest count(2^k n') / count(n'):")
    for key in (0, 1):
        if len(twice[key]) > 1:
            r, c, c1, sizes, k, n1 = twice[key]
            print("  m %s: %.4f (%d / %d), sizes %s, k = %d, n' = %d" % ("even" if key == 0 else "odd", r, c, c1, sizes, k, n1))
    print()
    print("least m with 2 d C(m,m//2) < 2^m, by d = d(n'):")
    for dn in (1, 2, 3, 4, 6, 8):
        m = 0
        while 2 * dn * comb(m, m // 2) >= 2 ** m:
            m += 1
        # is it monotone from there on?  check the next 400
        ok = all(2 * dn * comb(x, x // 2) < 2 ** x for x in range(m, m + 400))
        print("  d = %d: m = %d%s" % (dn, m, "" if ok else " (not for every larger m)"))


main()
