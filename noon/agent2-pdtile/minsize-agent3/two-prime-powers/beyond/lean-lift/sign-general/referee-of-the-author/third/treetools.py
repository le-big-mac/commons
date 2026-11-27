"""Referee, third pass: trees and tree boxes, from section 1 of sign-all-result.md.

Tree T = Z_{p^a}.  Class at depth i: a residue class modulo p^i.  Group at level i (1 <= i <= a): a class modulo
p^(i-1) with its p subclasses modulo p^i; sibling classes: two distinct subclasses of one group.
f : T -> V is flat at level i >= 1 if in every group at level i the p subclass sums are equal; flat at level 0 if f(T) = 0.
Tree box T_1 x ... x T_k; level (i_1, ..., i_k); a cube picks a sibling pair C_j != C'_j at level i_j for each j with
i_j >= 1; cube sum = sum_x g(x) prod_j ([x_j in C_j] - [x_j in C'_j]); good at the level if some cube sum is not 0.

Fast test: for i >= 1 the matrix M_i with rows c = residues modulo p^i,
    M_i[c, v] = [v = c mod p^i] - [v = (c mod p^(i-1)) mod p^i],
i.e. (sum over the subclass c) - (sum over the subclass of the same group with digit 0); all sibling differences in all
groups vanish iff M_i f = 0.  For i = 0 the row of ones.  A function on a box is degenerate at (i_1..i_k) iff applying
M_{i_j} along every axis gives 0.  (direct_good below is the definition itself, with every cube, for cross-checking.)
"""
import numpy as np
from itertools import product

def level_matrix(p, a, i):
    n = p ** a
    if i == 0:
        return np.ones((1, n), dtype=np.int64)
    M = np.zeros((p ** i, n), dtype=np.int64)
    v = np.arange(n)
    for c in range(p ** i):
        M[c] = (v % p ** i == c).astype(np.int64) - (v % p ** i == c % p ** (i - 1)).astype(np.int64)
    return M

def box_levels(trees):
    return list(product(*[range(a + 1) for (_, a) in trees]))

class TreeBox:
    def __init__(self, trees):
        self.trees = list(trees); self.k = len(trees)
        self.sides = tuple(p ** a for p, a in trees)
        self.levels = box_levels(trees)
        self.M = [[level_matrix(p, a, i) for i in range(a + 1)] for (p, a) in trees]

    def transform(self, H, level):
        """H: batch (B, *sides).  The array of base cube sums at the level (shape (B, ...))."""
        T = H
        for j, i in enumerate(level):
            T = np.moveaxis(np.tensordot(T, self.M[j][i], axes=([j + 1], [1])), -1, j + 1)
        return T.reshape(T.shape[0], -1)

    def good_at(self, H, level, q=None):
        T = self.transform(H, level)
        if q is not None: T = T % q
        return (T != 0).any(axis=1)

    def good(self, H, q=None, levels=None):
        ok = np.ones(H.shape[0], dtype=bool)
        for lv in (self.levels if levels is None else levels):
            ok &= self.good_at(H, lv, q)
        return ok

    def direct_good_at(self, g, level, q=None):
        """the definition, one function: every cube (every ordered sibling pair in every group)."""
        choices = []
        for j, i in enumerate(level):
            if i == 0: choices.append([None]); continue
            p, a = self.trees[j]
            prs = [(c, c2) for c in range(p ** i) for c2 in range(p ** i) if c != c2 and c % p ** (i - 1) == c2 % p ** (i - 1)]
            choices.append(prs)
        idx = [np.arange(n) for n in self.sides]
        for cube in product(*choices):
            w = np.ones(self.sides, dtype=np.int64)
            for j, pr in enumerate(cube):
                if pr is None: continue
                p, a = self.trees[j]; i = level[j]
                f = (idx[j] % p ** i == pr[0]).astype(np.int64) - (idx[j] % p ** i == pr[1]).astype(np.int64)
                sh = [1] * self.k; sh[j] = self.sides[j]
                w = w * f.reshape(sh)
            s = int((w * g).sum())
            if (s != 0) if q is None else (s % q != 0): return True
        return False

# ---- one tree, scalar or vector valued, batches of signed functions ----
def flat_at(H, p, a, i, q=None):
    """H: array (B, p^a) or (B, p^a, dim).  Boolean (B,): flat at level i (i = 0: total 0)."""
    M = level_matrix(p, a, i)
    T = np.tensordot(H, M, axes=([1], [1]))            # (B, [dim,] rows)
    if q is not None: T = T % q
    return ~(T != 0).reshape(T.shape[0], -1).any(axis=1)

def all_signs(w):
    return np.array(list(product((1, -1), repeat=w)), dtype=np.int64).reshape(-1, w)

def selftest():
    rng = np.random.default_rng(11); n = 0
    for trees in [[(3, 2)], [(3, 2), (3, 1)], [(3, 2), (5, 1)], [(3, 1), (3, 2)], [(5, 1), (3, 2)], [(3, 2), (3, 2)], [(3, 3)], [(5, 2)]]:
        tb = TreeBox(trees)
        for _ in range(25 if tb.k == 1 else 12):
            kind = rng.integers(0, 3)
            if kind == 0: g = rng.integers(-2, 3, size=tb.sides)
            elif kind == 1: g = (rng.random(tb.sides) < 0.25).astype(np.int64)
            else:
                # made degenerate at many levels: constant on classes of a random depth in each coordinate, plus a few cells
                g = np.ones(tb.sides, dtype=np.int64)
                for j, (p, a) in enumerate(trees):
                    d = rng.integers(0, a + 1); vals = rng.integers(-2, 3, size=p ** d)
                    sh = [1] * tb.k; sh[j] = tb.sides[j]
                    g = g * vals[np.arange(tb.sides[j]) % p ** d].reshape(sh)
                for _c in range(rng.integers(0, 2)):
                    g[tuple(rng.integers(0, s) for s in tb.sides)] += 1
            for lv in tb.levels:
                for q in (None, 5, 7):
                    assert bool(tb.good_at(g[None], lv, q)[0]) == tb.direct_good_at(g, lv, q), (trees, lv, q)
                    n += 1
    return n

if __name__ == '__main__':
    print('treetools selftest: fast test of "good at a level" on trees and tree boxes against the definition (every sibling cube):',
          selftest(), 'comparisons, no difference')
