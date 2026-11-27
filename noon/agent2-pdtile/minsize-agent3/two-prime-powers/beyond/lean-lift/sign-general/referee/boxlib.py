# Referee's own tools: cube sums on boxes, pattern tables.  Exact integer arithmetic (int64, small values).
import itertools
import numpy as np
from fractions import Fraction


def signs(n):
    return np.array(list(itertools.product([1, -1], repeat=n)), dtype=np.int64)


def axis_mats(n):
    S = signs(n)
    D = np.zeros((n - 1, n), dtype=np.int64)
    for a in range(1, n):
        D[a - 1, a] = 1
        D[a - 1, 0] = -1
    return S[:, None, :].copy(), S[:, None, :] * D[None, :, :]


def all_levels(k):
    return [frozenset(c) for r in range(k + 1) for c in itertools.combinations(range(k), r)]


def good_table(g, sides, q, levels):
    """per_level[P][s1,...,sk] = True iff (sigma g) has a nonzero cube sum at P (mod q, or over Z if q == 0).
    Cubes with a'_i = 0 only: they span all cubes (delta_a - delta_a' = (delta_a - delta_0) - (delta_a' - delta_0))."""
    k = len(sides)
    mats = [axis_mats(n) for n in sides]
    per = {}
    for P in levels:
        T = np.asarray(g, dtype=np.int64)
        for i in range(k):
            A = mats[i][1 if i in P else 0]
            T = np.tensordot(T, A, axes=([0], [2]))
        if q:
            T = T % q
        per[P] = (T != 0).any(axis=tuple(range(1, 2 * k, 2)))
    res = np.ones([2 ** n for n in sides], dtype=bool)
    for P in levels:
        res &= per[P]
    return res, per


def cube_sums_plain(f, sides, P, q):
    """all cube sums (a' = 0) of f at level P, no signs"""
    T = np.asarray(f, dtype=np.int64)
    for i, n in enumerate(sides):
        if i in P:
            D = np.zeros((n - 1, n), dtype=np.int64)
            for a in range(1, n):
                D[a - 1, a] = 1
                D[a - 1, 0] = -1
        else:
            D = np.ones((1, n), dtype=np.int64)
        T = np.tensordot(T, D, axes=([0], [1]))
    return T % q if q else T


def brute_cube_good(f, sides, P, q):
    """independent slow check with all pairs a != a'"""
    k = len(sides)
    P = sorted(P)
    f = np.asarray(f)
    for cube in itertools.product(*[[(a, b) for a in range(sides[i]) for b in range(sides[i]) if a != b] for i in P]):
        tot = 0
        for x in itertools.product(*[range(n) for n in sides]):
            w = 1
            for (i, (a, b)) in zip(P, cube):
                w *= (x[i] == a) - (x[i] == b)
                if w == 0:
                    break
            if w:
                tot += w * int(f[x])
        if (tot % q if q else tot) != 0:
            return True
    return False


def rank(M, q):
    M = [list(r) for r in M]
    if not M:
        return 0
    if q:
        M = [[x % q for x in r] for r in M]
    else:
        M = [[Fraction(int(x)) for x in r] for r in M]
    rk = 0
    rows, cols = len(M), len(M[0])
    for c in range(cols):
        piv = None
        for r in range(rk, rows):
            if M[r][c] != 0:
                piv = r
                break
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        inv = pow(M[rk][c], -1, q) if q else 1 / M[rk][c]
        M[rk] = [(x * inv) % q if q else x * inv for x in M[rk]]
        for r in range(rows):
            if r != rk and M[r][c] != 0:
                f = M[r][c]
                M[r] = [((x - f * y) % q) if q else (x - f * y) for x, y in zip(M[r], M[rk])]
        rk += 1
        if rk == rows:
            break
    return rk
