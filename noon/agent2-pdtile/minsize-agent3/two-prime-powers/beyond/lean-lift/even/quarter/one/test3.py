"""Tests of Lemmas 1 and 2 of result.md and of the bounds xi(m), for the prime 3, by exact arithmetic and ALL signings.

Part 1 (shapes): every multiset of m elements on Z_(3^a), up to the automorphisms of the ternary tree (which permute
the three children of any class and do not change the events), is a "shape": depth 0: the number of elements; depth a:
a sorted triple of shapes of depth a - 1.  For every shape the joint distribution of (sum of signs, set of levels
i >= 1 at which the signing is bad) over all signings is computed from the children (all signings, by convolution).
Checked for every shape: Lemma 1 (root not branching), Lemma 2 (i), (a), (b), (c) with the true values of the
children, and X(B) <= xi(m) with xi from a second implementation of the recursion.  Printed: the largest X(B) and the
largest share of bad signings for each m, to be compared with xi(m).

Part 2 (definition): for random multisets on Z_27 and Z_81 the distribution of Part 1 is compared with the definition:
a signing is bad at 3^i iff the signed mask, an integer polynomial, leaves remainder 0 on division by
Phi_(3^i)(X) = 1 + X^(3^(i-1)) + X^(2*3^(i-1))  (Phi_1 = X - 1).

usage: test3.py shapes A MMAX   |   test3.py definition SEED COUNT
"""
import sys, itertools, random
from fractions import Fraction as F
from math import comb
from functools import lru_cache


def c(r):
    return F(comb(r, r // 2), 2 ** r)


def pr(v, r):
    if (r + v) % 2 or abs(v) > r:
        return F(0)
    return F(comb(r, (r + v) // 2), 2 ** r)


def recursion(M):
    xi = {0: F(0)}
    for m in range(1, M + 1):
        best = F(0)
        for r0 in range(m, 0, -1):
            for r1 in range(min(r0, m - r0), 0, -1):
                r2 = m - r0 - r1
                if r2 > r1:
                    continue
                rs = (r0, r1, r2)
                A = sum(pr(v, r0) * pr(v, r1) * pr(v, r2) for v in range(-r2, r2 + 1) if v != 0)
                gs = [(c(r) if r % 2 == 0 else 0) + xi[r] for r in rs]
                S = gs[0] * gs[1] * gs[2]
                if all(r % 2 == 0 for r in rs):
                    S = min(S, S - c(r0) * c(r1) * c(r2))
                if r2 == 0 and r0 % 2 and r1 % 2 and r0 <= 7:
                    S = min(S, xi[r0] * xi[r1] / 2)
                best = max(best, A + S)
        xi[m] = best
    return xi


# ---------- shapes
@lru_cache(maxsize=None)
def shapes(a, m):
    if a == 0:
        return (m,)
    out = []
    for r0 in range(m, -1, -1):
        for r1 in range(min(r0, m - r0), -1, -1):
            r2 = m - r0 - r1
            if r2 > r1 or r2 < 0:
                continue
            L0, L1, L2 = shapes(a - 1, r0), shapes(a - 1, r1), shapes(a - 1, r2)
            for i0, s0 in enumerate(L0):
                for i1, s1 in enumerate(L1):
                    if r1 == r0 and i1 < i0:
                        continue
                    for i2, s2 in enumerate(L2):
                        if r2 == r1 and i2 < i1:
                            continue
                        out.append((s0, s1, s2))
    return tuple(out)


def size(a, s):
    return s if a == 0 else sum(size(a - 1, t) for t in s)


@lru_cache(maxsize=None)
def dist(a, s):
    """dict (sigma, mask) -> number of signings; bit i-1 of mask: bad at 3^i (all groups at level i flat)"""
    if a == 0:
        return {(v, 0): comb(s, (s + v) // 2) for v in range(-s, s + 1, 2)}
    D0, D1, D2 = (dist(a - 1, t) for t in s)
    out = {}
    for (v0, k0), n0 in D0.items():
        for (v1, k1), n1 in D1.items():
            k01 = k0 & k1; n01 = n0 * n1; e = (v0 == v1)
            for (v2, k2), n2 in D2.items():
                key = (v0 + v1 + v2, ((k01 & k2) << 1) | (1 if e and v1 == v2 else 0))
                out[key] = out.get(key, 0) + n01 * n2
    return out


def stats(a, s):
    D = dist(a, s)
    X = sum(n for (v, k), n in D.items() if k and v)                 # bad at some 3^i, i >= 1, sum != 0
    PU = sum(n for (v, k), n in D.items() if k)                      # bad at some 3^i, i >= 1
    PU0 = sum(n for (v, k), n in D.items() if k and v == 0)
    BAD = sum(n for (v, k), n in D.items() if k or v == 0)
    E1X = sum(n for (v, k), n in D.items() if (k & 1) and v)
    H = sum(n for (v, k), n in D.items() if k >> 1)
    HX = sum(n for (v, k), n in D.items() if (k >> 1) and v)
    return X, PU, PU0, BAD, E1X, H, HX


def run_shapes(a, mmax):
    xi = recursion(mmax)
    print(f"shapes on the ternary tree of depth {a} (Z_{3 ** a}), m = 1..{mmax}; every check is exact and over all signings")
    for m in range(1, mmax + 1):
        L = shapes(a, m)
        nb = 0; n1 = 0; cnt = dict(i=0, a=0, b=0, c=0)
        bestX = F(0); bestBad = F(0); exX = exB = None
        for s in L:
            X, PU, PU0, BAD, E1X, H, HX = stats(a, s)
            tot = 2 ** m
            rs = [size(a - 1, t) for t in s]
            occupied = sum(1 for r in rs if r)
            assert F(X, tot) <= xi[m], ("xi fails", a, s)
            if F(X, tot) > bestX: bestX = F(X, tot); exX = s
            if F(BAD, tot) > bestBad: bestBad = F(BAD, tot); exB = s
            ch = [stats(a - 1, t) for t in s]
            if occupied == 1:                                        # Lemma 1
                t = [i for i in range(3) if rs[i]][0]
                assert X == ch[t][0] and BAD == ch[t][3] and PU == ch[t][3], ("Lemma 1 fails", a, s)
                n1 += 1
                continue
            nb += 1
            # Lemma 2 (i)
            A = sum(pr(v, rs[0]) * pr(v, rs[1]) * pr(v, rs[2]) for v in range(-m, m + 1) if v != 0)
            assert F(E1X, tot) == A, ("Lemma 2 (i) fails", a, s); cnt['i'] += 1
            # Lemma 2 (a)
            pu = [F(ch[i][1], 2 ** rs[i]) for i in range(3)]
            assert F(HX, tot) <= pu[0] * pu[1] * pu[2], ("Lemma 2 (a) fails", a, s); cnt['a'] += 1
            assert F(X, tot) <= A + F(HX, tot)
            if all(r % 2 == 0 for r in rs):                          # Lemma 2 (b)
                pu0 = [F(ch[i][2], 2 ** rs[i]) for i in range(3)]
                assert F(HX, tot) <= pu[0] * pu[1] * pu[2] - pu0[0] * pu0[1] * pu0[2], ("Lemma 2 (b) fails", a, s)
                assert all(pu0[i] <= c(rs[i]) for i in range(3))
                cnt['b'] += 1
            srt = sorted(rs, reverse=True)
            if srt[2] == 0 and srt[0] % 2 and srt[1] % 2 and srt[0] <= 7:   # Lemma 2 (c)
                assert 2 * HX == H, ("Lemma 2 (c) fails", a, s); cnt['c'] += 1
        target = (c(m - 2) / 2 if m >= 3 else F(0)) if m % 2 else None
        note = f"  = c_(m-2)/2: {bestX == target}" if m % 2 else f"  c_m + xi = {c(m) + xi[m]}"
        print(f"m = {m:2d}  shapes {len(L):7d} (root branching {nb}, not {n1})  largest X = {bestX} (xi = {xi[m]})  largest bad share = {bestBad}{note}"
              f"  checks: (i) {cnt['i']} (a) {cnt['a']} (b) {cnt['b']} (c) {cnt['c']}", flush=True)
        print(f"         X largest at {exX};  bad share largest at {exB}", flush=True)
    print("no failure")


# ---------- definition
def polyrem(coef, i):
    """remainder of the integer polynomial coef (list, low degree first) modulo Phi_(3^i); True if it is 0"""
    if i == 0:
        return sum(coef) == 0
    h = 3 ** (i - 1); f = [0] * (3 * h)
    for j, x in enumerate(coef):
        f[j % (3 * h)] += x                                          # modulo X^(3^i) - 1, a multiple of Phi_(3^i)
    for j in range(3 * h - 1, 2 * h - 1, -1):                        # divide by the monic 1 + X^h + X^(2h)
        x = f[j]
        if x:
            f[j] = 0; f[j - h] -= x; f[j - 2 * h] -= x
    return not any(f)


def shape_of(a, elems):
    if a == 0:
        return len(elems)
    kids = [tuple(sorted(b // 3 for b in elems if b % 3 == t)) for t in range(3)]
    return tuple(shape_of(a - 1, k) for k in kids)


def run_definition(seed, count):
    rnd = random.Random(seed); done = 0; sign_total = 0
    for trial in range(count):
        a = rnd.choice([2, 3, 3, 4]); n = 3 ** a; m = rnd.randint(2, 10)
        style = rnd.randint(0, 3)
        if style == 0:
            B = [rnd.randrange(n) for _ in range(m)]
        elif style == 1:                                             # few classes, repeated elements
            pool = [rnd.randrange(n) for _ in range(3)]
            B = [rnd.choice(pool) for _ in range(m)]
        elif style == 2:                                             # pairs: all class sizes even
            pool = [rnd.randrange(n) for _ in range(m // 2 + 1)]
            B = (pool * 2)[:m]
        else:                                                        # heavy class and a spread remainder
            x = rnd.randrange(n)
            B = [x] * (m - 2) + [(x + rnd.choice([1, 3, 9]) * rnd.choice([1, 2])) % n for _ in range(2)]
        D = {}
        for signs in itertools.product((1, -1), repeat=m):
            coef = [0] * n
            for b, e in zip(B, signs):
                coef[b] += e
            mask = 0
            for i in range(1, a + 1):
                if polyrem(coef, i):
                    mask |= 1 << (i - 1)
            assert polyrem(coef, 0) == (sum(signs) == 0)
            key = (sum(signs), mask)
            D[key] = D.get(key, 0) + 1
        sign_total += 2 ** m
        # the DP of part 1 on the same multiset (children in the order 0, 1, 2; no sorting needed for dist)
        s = shape_of(a, B)
        D2 = {k: v for k, v in dist(a, s).items() if v}
        assert D == D2, ("definition and recursion differ", n, B)
        done += 1
    print(f"seed {seed}: {done} random multisets on Z_9, Z_27, Z_81 (2 to 10 elements, four styles), {sign_total} signings: "
          f"the events 'Phi_(3^i) divides the signed mask' (polynomial division) agree with the tree recursion in every case")


def random_shape(rnd, a, m):
    if a == 0:
        return m
    if m == 0:
        return (random_shape(rnd, a - 1, 0),) * 3
    style = rnd.randint(0, 5)
    if style == 0 or m == 1:                               # no branching
        parts = [m, 0, 0]
    elif style == 1:                                       # heavy class and two small ones
        x = rnd.randint(1, 3); y = rnd.randint(0, 3)
        parts = [max(m - x - y, 0), min(x, m), min(y, max(m - x, 0))]
        parts[0] = m - parts[1] - parts[2]
    elif style == 2:                                       # all even where possible
        x = 2 * rnd.randint(0, m // 4); y = 2 * rnd.randint(0, (m - x) // 4)
        parts = [m - x - y, x, y]
    elif style == 3:                                       # nearly equal
        parts = [m // 3, (m + 1) // 3, m - m // 3 - (m + 1) // 3]
    else:
        x = rnd.randint(0, m); y = rnd.randint(0, m - x)
        parts = [x, y, m - x - y]
    return tuple(random_shape(rnd, a - 1, r) for r in parts)


def run_random(seed, count, mlo, mhi):
    """random shapes with more elements and deeper trees than the exhaustive runs: X(B) <= xi(m), all signings"""
    rnd = random.Random(seed); xi = recursion(mhi)
    best = {}
    for _ in range(count):
        a = rnd.randint(2, 6); m = rnd.randint(mlo, mhi)
        s = random_shape(rnd, a, m)
        X = F(stats(a, s)[0], 2 ** m)
        assert X <= xi[m], ("xi fails", a, s)
        if m % 2:
            assert X <= c(m - 2) / 2
        else:
            assert X <= min(F(309, 8192), c(m) / 2)
        if X > best.get(m, (F(-1), None))[0]:
            best[m] = (X, s)
        dist.cache_clear()
    print(f"seed {seed}: {count} random shapes of depth 2 to 6 with {mlo} to {mhi} elements, all signings: X(B) <= xi(m) in every case")
    for m in sorted(best):
        print(f"  m = {m:2d}: largest X = {best[m][0]} = {float(best[m][0]):.6f}   xi(m) = {float(xi[m]):.6f}")


if __name__ == '__main__':
    if sys.argv[1] == 'random':
        run_random(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
    elif sys.argv[1] == 'shapes':
        run_shapes(int(sys.argv[2]), int(sys.argv[3]))
    else:
        run_definition(int(sys.argv[2]), int(sys.argv[3]))
