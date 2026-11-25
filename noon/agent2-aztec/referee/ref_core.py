"""Referee's own implementation (blind). Block value = a*1 + b*2 + c*4 + d*8.
a = NW edge (touches left, top corner), b = NE (top, right), c = SW (left, bottom), d = SE (bottom, right).
"""
import numpy as np

A_, B_, C_, D_ = 1, 2, 4, 8
PAIR_AD, PAIR_BC = 9, 6


def _swap(v):
    r = 0
    if v & 1: r |= 8
    if v & 8: r |= 1
    if v & 2: r |= 4
    if v & 4: r |= 2
    return r


def _del(v):
    if (v & 9) == 9: v &= ~9
    if (v & 6) == 6: v &= ~6
    return v


LUT_DEL = np.array([_del(v) for v in range(16)], np.uint8)
LUT_SWAP = np.array([_swap(v) for v in range(16)], np.uint8)
LUT_DELSWAP = np.array([_swap(_del(v)) for v in range(16)], np.uint8)
POP = np.array([bin(v).count("1") for v in range(16)], np.uint8)


def shift(old):
    """step 1: old n x n -> new (n+1) x (n+1), every old dimer lies in some new block."""
    n = old.shape[0]
    new = np.zeros((n + 1, n + 1), np.uint8)
    new[:n, :n] |= (old & 1) << 3      # old a(i,j) is the SE edge (d) of new (i,j)
    new[:n, 1:] |= (old & 2) << 1      # old b(i,j) is the SW edge (c) of new (i,j+1)
    new[1:, :n] |= (old & 4) >> 1      # old c(i,j) is the NE edge (b) of new (i+1,j)
    new[1:, 1:] |= (old & 8) >> 3      # old d(i,j) is the NW edge (a) of new (i+1,j+1)
    return new


def candidates(v):
    """as worded, step 4 condition: empty and no corner touched by a neighbouring block's dimer."""
    empty = v == 0
    t = np.zeros_like(empty); t[1:, :] = (v[:-1, :] & 12) != 0   # block above holds c or d
    b = np.zeros_like(empty); b[:-1, :] = (v[1:, :] & 3) != 0    # block below holds a or b
    l = np.zeros_like(empty); l[:, 1:] = (v[:, :-1] & 10) != 0   # left block holds b or d
    r = np.zeros_like(empty); r[:, :-1] = (v[:, 1:] & 5) != 0    # right block holds a or c
    return empty & ~t & ~b & ~l & ~r


def sequential_fill_set(v):
    """reading-order scan: a block is filled if empty and no corner touched, counting fills made earlier
    in the same scan. Returns boolean mask of blocks to fill."""
    n = v.shape[0]
    w = v.copy()
    out = np.zeros(v.shape, bool)
    for i in range(n):
        for j in range(n):
            if w[i, j]:
                continue
            if i > 0 and (w[i - 1, j] & 12): continue
            if i < n - 1 and (w[i + 1, j] & 3): continue
            if j > 0 and (w[i, j - 1] & 10): continue
            if j < n - 1 and (w[i, j + 1] & 5): continue
            out[i, j] = True
            w[i, j] = 9   # either pair touches all four corners
    return out


def vertex_counts(v):
    n = v.shape[0]
    a = (v & 1) != 0; b = (v & 2) != 0; c = (v & 4) != 0; d = (v & 8) != 0
    V = np.zeros((n + 1, n), np.int8)
    V[:n, :] += a.astype(np.int8) + b
    V[1:, :] += c.astype(np.int8) + d
    H = np.zeros((n, n + 1), np.int8)
    H[:, :n] += a.astype(np.int8) + c
    H[:, 1:] += b.astype(np.int8) + d
    return V, H


def is_tiling(v):
    V, H = vertex_counts(v)
    return bool((V == 1).all() and (H == 1).all())


def grow_step(old, rng):
    """corrected step (referee's rule): fill exactly the new blocks that were empty after step 1
    (before the deletion). Returns new array and number of tosses."""
    new = shift(old)
    fill = new == 0
    new = LUT_DELSWAP[new]
    k = int(fill.sum())
    new[fill] = np.where(rng.integers(0, 2, k, dtype=np.uint8) == 1, np.uint8(9), np.uint8(6))
    return new, k


def K_of(v):
    dg = np.diagonal(v) == 1
    bad = np.flatnonzero(~dg)
    return int(bad[0]) if len(bad) else v.shape[0]


def frozen_parts(v):
    from scipy import ndimage
    n = v.shape[0]
    res = []
    for val, (ci, cj) in ((1, (0, 0)), (2, (0, n - 1)), (4, (n - 1, 0)), (8, (n - 1, n - 1))):
        m = v == val
        if not m[ci, cj]:
            res.append(0); continue
        lab, _ = ndimage.label(m)          # default structure = 4-connectivity (sharing a side)
        res.append(int((lab == lab[ci, cj]).sum()))
    return res


def frozen_fraction(v):
    return sum(frozen_parts(v)) / v.size


def central_shares(v, lo=0.4, hi=0.6, inclusive=False):
    n = v.shape[0]
    idx = np.arange(n)
    sel = (idx >= lo * n) & ((idx <= hi * n) if inclusive else (idx < hi * n))
    s = v[np.ix_(sel, sel)]
    cnt = np.array([((s & bit) != 0).sum() for bit in (1, 2, 4, 8)], float)
    return cnt, cnt / cnt.sum()
