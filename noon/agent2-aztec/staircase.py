"""Is the polar region always a staircase, and is it the frozen corner one step later at all four corners?
Added 26 November 2026, to test region-proof.md; extended the same morning after a reader's check.
usage: python -I staircase.py [largest order to enumerate] [growths] [order of the growths] > staircase.out
        (numpy, scipy; aztec.py beside it)

P: the blocks that hold the dimer a (alone or with d) and are joined to block (0, 0) through side-by-side such
blocks.  "A staircase": if a block is in P, so are the block above it and the block to its left.
"Behind": the block one up and one to the left.

Part 1, on EVERY tiling of the small orders: is P a staircase; has any block of P a dimer d behind it.
   Controls, so that both can be seen to fail: the same two questions of all the blocks that hold a, and of
   the other joined-up groups of blocks holding a (each asked whether it is a staircase from its own corner).
Part 2, on EVERY step from every tiling of the small orders with every filling: at each of the four corners,
   is the polar region of the old tiling the strictly frozen region of the new one (the same set of blocks,
   counted from that corner)?  The page's "frozen fraction" is the four strictly frozen regions together.
   And is the page's K at each corner of the new tiling (aztec.four_corners: the run of blocks along the
   diagonal that hold exactly the corner's dimer) the depth of the old polar region on that diagonal?
Part 3: part 1 again on random growths (successive orders of one growth are not independent tilings)."""
import os, sys, itertools
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.ndimage import label
import aztec


def stair(M):
    return not (M[1:, :] & ~M[:-1, :]).any() and not (M[:, 1:] & ~M[:, :-1]).any()


def look(x, tosses=None):
    """(P is a staircase, blocks of P with d behind, blocks holding a with d behind, size of P,
        all the blocks holding a are a staircase, other groups, other groups that are staircases from their own corner)"""
    a, b, c, d = aztec.parts(x)
    behind_any = int((a[1:, 1:] & d[:-1, :-1]).sum())
    lab, k = label(a)
    own = lab[0, 0] if a[0, 0] else 0
    P = (lab == own) if own else np.zeros_like(a)
    others = ok = 0
    for g in range(1, k + 1):
        if g == own: continue
        C = lab == g; rows, cols = np.nonzero(C); others += 1
        ok += stair(C[rows.min():, cols.min():])
    return (stair(P), int((P[1:, 1:] & d[:-1, :-1]).sum()), behind_any, int(P.sum()), stair(a), others, ok)


def corner(x, which, alone):
    """the blocks holding that corner's dimer (alone, if asked) and joined to the corner block, counted from the corner"""
    a, b, c, d = aztec.parts(x)
    m, rest = {'a': (a, (b, c, d)), 'b': (b[:, ::-1], (a[:, ::-1], c[:, ::-1], d[:, ::-1])),
               'c': (c[::-1, :], (a[::-1, :], b[::-1, :], d[::-1, :])), 'd': (d[::-1, ::-1], (a[::-1, ::-1], b[::-1, ::-1], c[::-1, ::-1]))}[which]
    if alone: m = m & ~rest[0] & ~rest[1] & ~rest[2]
    if not m[0, 0]: return frozenset()
    lab, _ = label(m)
    return frozenset(map(tuple, np.argwhere(lab == lab[0, 0])))


def children(x):
    y = aztec.shuffle(x) if x is not None else np.zeros((2, 2), bool); w = aztec.holes(y)
    for toss in itertools.product((False, True), repeat=int(w.sum())):
        z = y.copy(); aztec.fill(z, w, np.array(toss, bool)); yield z


if __name__ == '__main__':
    top = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    G = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    level = {z.tobytes(): z for z in children(None)}
    for order in range(1, top + 1):
        t = np.array([look(x) for x in level.values()])
        print(f"order {order}: {len(level)} tilings (2^(n(n+1)/2) = {2 ** (order * (order + 1) // 2)}); P not empty in {int((t[:, 3] > 0).sum())}; P a staircase in {int(t[:, 0].sum())}; "
              f"a block of P with d behind it in {int((t[:, 1] > 0).sum())}", flush=True)
        print(f"   controls: any block holding a with d behind it in {int((t[:, 2] > 0).sum())}; all the blocks holding a a staircase in {int(t[:, 4].sum())}; "
              f"other joined-up groups of blocks holding a: {int(t[:, 5].sum())}, staircases from their own corner: {int(t[:, 6].sum())}", flush=True)
        if order == top: break
        nxt = {}; steps = 0; same = dict(a=0, b=0, c=0, d=0); depth_same = 0; depth_other = 0
        for x in level.values():
            old = {w: corner(x, w, False) for w in 'abcd'}
            depth = [next(k for k in range(order + 2) if (k, k) not in old[w]) for w in 'abcd']
            for z in children(x):
                steps += 1; nxt.setdefault(z.tobytes(), z)
                for w in 'abcd': same[w] += old[w] == corner(z, w, True)
                K = aztec.four_corners(z, None)
                depth_same += K == depth; depth_other += K == aztec.four_corners(x, None)      # the second is a control: K of the old tiling itself
        print(f"   every step from order {order} to {order + 1}: {steps} steps; the old polar region is the new strictly frozen region at corner a in {same['a']}, b in {same['b']}, c in {same['c']}, d in {same['d']}", flush=True)
        print(f"   the new tiling's K at all four corners is the old polar region's depth on the four diagonals in {depth_same}; control, it is the old tiling's own K at all four in {depth_other}", flush=True)
        level = nxt
    cnt = 0; tot = np.zeros(7)
    for s in range(G):
        rng = np.random.default_rng(770000 + s)
        _, _, out = aztec.grow(n, rng, look, at=tuple(range(2, n + 1)))
        for v in out.values():
            cnt += 1; tot += np.array([v[0], v[1] > 0, v[2] > 0, v[3], v[4], v[5], v[6]])
    print(f"{G} random growths to order {n} (seeds 770000 on), read at every order from 2: {cnt} tilings, not independent; P a staircase in {int(tot[0])}; "
          f"a block of P with d behind it in {int(tot[1])}; mean size of P {tot[3] / cnt:.1f} blocks")
    print(f"   controls: any block holding a with d behind it in {int(tot[2])}; all the blocks holding a a staircase in {int(tot[4])}; "
          f"other joined-up groups: {int(tot[5])}, staircases from their own corner: {int(tot[6])}")
