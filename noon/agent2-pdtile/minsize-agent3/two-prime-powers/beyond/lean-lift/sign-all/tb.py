# tb.py -- tools for "tree boxes": X = T_1 x ... x T_k with T_j = Z_{p_j^{a_j}} (one coordinate per prime).
# A level is a tuple (i_1..i_k), 0 <= i_j <= a_j.  A cube at that level: for each j with i_j >= 1 two sibling classes
# modulo p_j^{i_j} (two classes modulo p^i inside one class modulo p^(i-1)); for i_j = 0 the whole coordinate is summed.
# g is good at the level if some cube sum is nonzero (modulo q if q is given, else over the integers).
# All arithmetic is in exact integers (numpy int64 on small numbers), reduced modulo q where q is given.
import itertools
import numpy as np

def fold_axis(A, axis, p, a, i):
    """class sums modulo p^i along `axis` (length p^a): v = h*p^i + c -> c."""
    sh = list(A.shape)
    n = sh[axis]
    assert n == p ** a
    new = sh[:axis] + [p ** (a - i), p ** i] + sh[axis + 1:]
    return A.reshape(new).sum(axis=axis)

def diff_axis(A, axis, p, i):
    """A[c] - A[c mod p^(i-1)] along axis (length p^i), i >= 1: zero iff the classes of every sibling group agree."""
    idx = np.arange(p ** i) % (p ** (i - 1))
    return A - np.take(A, idx, axis=axis)

def level_image(A, spec, level, q=None, first_axis=0):
    """the array of sibling mixed differences of A at `level`; axes first_axis.. are the coordinates."""
    B = A
    for j, ((p, a), i) in enumerate(zip(spec, level)):
        ax = first_axis + j
        B = fold_axis(B, ax, p, a, i)
        if i >= 1:
            B = diff_axis(B, ax, p, i)
        if q is not None:
            B = B % q
    return B

def all_levels(spec):
    return list(itertools.product(*[range(a + 1) for (p, a) in spec]))

def good_batch(A, spec, q=None, levels=None):
    """A: batch array (N, n_1, .., n_k).  Returns boolean vector: good at every level."""
    ok = np.ones(A.shape[0], dtype=bool)
    for lev in (levels if levels is not None else all_levels(spec)):
        B = level_image(A, spec, lev, q, first_axis=1)
        ok &= B.reshape(B.shape[0], -1).any(axis=1)
    return ok

def good_one(g, spec, q=None, levels=None):
    return bool(good_batch(g[None, ...], spec, q, levels)[0])

def all_signs(n):
    """all 2^n sign vectors as an int8 array (2^n, n)."""
    idx = np.arange(2 ** n, dtype=np.int64)[:, None]
    bits = (idx >> np.arange(n)) & 1
    return (1 - 2 * bits).astype(np.int64)

def count_good_patterns(g, spec, q=None, chunk=4096):
    """number of product patterns (one arbitrary sign vector per coordinate) that make g good at every level,
    and the number of patterns.  Enumerates everything; only for small boxes."""
    sizes = [p ** a for (p, a) in spec]
    k = len(spec)
    signs = [all_signs(n) for n in sizes]
    total = 0
    good = 0
    # iterate over patterns of coordinates 1..k-1, batch over coordinate 0
    for combo in itertools.product(*[range(s.shape[0]) for s in signs[1:]]):
        h = g
        for j, c in enumerate(combo):
            shp = [1] * k
            shp[j + 1] = sizes[j + 1]
            h = h * signs[j + 1][c].reshape(shp)
        S0 = signs[0]
        for st in range(0, S0.shape[0], chunk):
            blk = S0[st:st + chunk]
            A = blk.reshape((blk.shape[0], sizes[0]) + (1,) * (k - 1)) * h[None, ...]
            good += int(good_batch(A, spec, q).sum())
            total += blk.shape[0]
    return good, total

# brute definition of "good" by explicit cubes, for cross-checking the vectorised version (slow)
def good_one_slow(g, spec, q=None):
    sizes = [p ** a for (p, a) in spec]
    k = len(spec)
    for lev in all_levels(spec):
        found = False
        # choices of sibling pairs per coordinate
        pair_lists = []
        for (p, a), i in zip(spec, lev):
            if i == 0:
                pair_lists.append([None])
            else:
                prs = []
                for c in range(p ** i):
                    for c2 in range(p ** i):
                        if c != c2 and c % p ** (i - 1) == c2 % p ** (i - 1):
                            prs.append((c, c2))
                pair_lists.append(prs)
        for cube in itertools.product(*pair_lists):
            tot = 0
            for x in itertools.product(*[range(n) for n in sizes]):
                w = 1
                for j, ((p, a), i) in enumerate(zip(spec, lev)):
                    if i == 0:
                        continue
                    c, c2 = cube[j]
                    r = x[j] % p ** i
                    if r == c: w *= 1
                    elif r == c2: w *= -1
                    else:
                        w = 0; break
                if w:
                    tot += w * int(g[x])
            if (tot % q if q else tot) != 0:
                found = True; break
        if not found:
            return False
    return True
