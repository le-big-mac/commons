"""Referee's tools for functions on boxes, written from section 2 of sign-general-result.md.

A box has sides (n_1, ..., n_k); a function is an integer array of that shape; a batch is an array (M, n_1, ..., n_k).
A level is a tuple of axes (0-based).  A cube at level P: two values a_i != a'_i for i in P; cube sum
    sum_x g(x) prod_{i in P} ([x_i = a_i] - [x_i = a'_i]).
g is good at P if some cube sum is not 0 (in Q, or modulo q).

Used here: every factor [x_i = a] - [x_i = a'] is ([x_i = a] - [x_i = 0]) - ([x_i = a'] - [x_i = 0]), so all cube sums at
level P vanish iff all cube sums with a'_i = 0 (i in P) vanish.  Those are computed: sum over the axes outside P,
then subtract the slice at index 0 along each axis of P.  (cube_sums_direct below is the definition itself and is
compared with it in selftest.)
"""
import numpy as np
from itertools import combinations, product

def all_levels(k):
    return [P for r in range(k + 1) for P in combinations(range(k), r)]

def level_table(H, P):
    """H: batch (M, *sides), integer.  Returns the array of the cube sums at level P with base corners 0
    (shape (M, ...); entries with some coordinate of P equal to 0 are 0 and carry no information)."""
    k = H.ndim - 1
    out = tuple(i + 1 for i in range(k) if i not in P)
    D = H.sum(axis=out, keepdims=True) if out else H
    for i in P:
        D = D - np.take(D, [0], axis=i + 1)
    return D.reshape(D.shape[0], -1)

def good_batch(H, levels, q=None):
    """boolean (M,): good at every level of `levels`, over Q (q None) or modulo q."""
    ok = np.ones(H.shape[0], dtype=bool)
    for P in levels:
        D = level_table(H, P)
        if q is not None:
            D = D % q
        ok &= (D != 0).any(axis=1)
    return ok

def good_batch_fields(H, levels, fields):
    """dict q -> boolean (M,), for several fields at once (None = Q)."""
    ok = {q: np.ones(H.shape[0], dtype=bool) for q in fields}
    for P in levels:
        D = level_table(H, P)
        for q in fields:
            ok[q] &= ((D != 0) if q is None else (D % q != 0)).any(axis=1)
    return ok

def good_at(H, P, q=None):
    D = level_table(H, P)
    if q is not None: D = D % q
    return (D != 0).any(axis=1)

def sign_vectors(n, normalized):
    """all sign vectors of length n as an int8 array (2^n or 2^(n-1), n); normalized: first entry +1."""
    m = n - 1 if normalized else n
    rows = np.array(list(product((1, -1), repeat=m)), dtype=np.int8).reshape(-1, m)
    if normalized:
        rows = np.concatenate([np.ones((rows.shape[0], 1), dtype=np.int8), rows], axis=1)
    return rows

def pattern_array(sides, normalized=True, dtype=np.int8):
    """array (npat, *sides) of all product patterns sigma(x) = prod sigma_j(x_j).
    normalized: each sigma_j has sigma_j(first) = +1.  Changing the sign of one sigma_j changes sigma*g into -sigma*g,
    which is good exactly when sigma*g is; so the fraction of good patterns among the normalized ones equals the
    fraction among all 2^(n_1+...+n_k)."""
    k = len(sides)
    vecs = [sign_vectors(n, normalized) for n in sides]
    out = np.ones((1,) * (2 * k), dtype=dtype)
    for j, V in enumerate(vecs):
        shape = [1] * (2 * k)
        shape[j] = V.shape[0]; shape[k + j] = sides[j]
        out = out * V.reshape(shape).astype(dtype)
    return out.reshape((-1,) + tuple(sides)), vecs

def fraction_good(g, levels, fields, PA=None):
    """g: integer array of the box shape.  Returns dict q -> (number of good normalized patterns, number of patterns)."""
    sides = g.shape
    if PA is None:
        PA, _ = pattern_array(sides)
    H = PA.astype(np.int64) * g[None].astype(np.int64)
    ok = good_batch_fields(H, levels, fields)
    return {q: (int(ok[q].sum()), PA.shape[0]) for q in fields}

def cube_sums_direct(g, P):
    """the definition, for one function: list of all cube sums at level P (python ints)."""
    sides = g.shape; k = len(sides); res = []
    choices = [[(a, b) for a in range(sides[i]) for b in range(sides[i]) if a != b] for i in P]
    for cube in product(*choices):
        tot = 0
        for x in product(*[range(n) for n in sides]):
            f = 1
            for (i, (a, b)) in zip(P, cube):
                f *= (1 if x[i] == a else 0) - (1 if x[i] == b else 0)
                if f == 0: break
            if f: tot += f * int(g[x])
        res.append(tot)
    return res

def selftest():
    rng = np.random.default_rng(5)
    n_checked = 0
    for sides in [(3, 5), (3, 3), (4, 3), (3, 3, 5), (2, 3, 4)]:
        k = len(sides)
        for _ in range(60):
            kind = rng.integers(0, 3)
            if kind == 0:
                g = rng.integers(-2, 3, size=sides)
            elif kind == 1:
                g = (rng.random(sides) < 0.3).astype(np.int64)
            else:   # degenerate at many levels on purpose: sum of functions each missing one coordinate
                g = np.zeros(sides, dtype=np.int64)
                for i in range(k):
                    sh = list(sides); sh[i] = 1
                    g = g + rng.integers(-2, 3, size=sh)
            for P in all_levels(k):
                for q in (None, 3, 5, 7):
                    cs = cube_sums_direct(g, P)
                    direct = any((c != 0) if q is None else (c % q != 0) for c in cs)
                    fast = bool(good_at(g[None].astype(np.int64), P, q)[0])
                    assert direct == fast, (sides, P, q)
                    n_checked += 1
    # normalisation of patterns: full enumeration against normalised, one box
    sides = (3, 5); PAf, _ = pattern_array(sides, normalized=False); PAn, _ = pattern_array(sides, normalized=True)
    for _ in range(40):
        g = rng.integers(-1, 2, size=sides)
        if not g.any(): continue
        for q in (None, 7):
            a = good_batch(PAf.astype(np.int64) * g[None], all_levels(2), q).mean()
            b = good_batch(PAn.astype(np.int64) * g[None], all_levels(2), q).mean()
            assert a == b
    return n_checked

if __name__ == '__main__':
    print('boxtools selftest: fast test of "good at a level" against the definition (all cubes):', selftest(), 'comparisons, no difference;')
    print('fraction over normalised patterns equals fraction over all patterns on 3x5: checked')
