"""Step 2: (a) holes() against a plain reading-order scan and against 'empty before deletion' on EVERY tiling of orders 1..5
and on random tilings; (b) other reasonable definitions of the frozen region, on the referee's saved tilings."""
import sys
sys.dont_write_bytecode = True
import numpy as np
from scipy import ndimage
sys.path.insert(0, "/home/agent2/aztec")
import aztec as A
from ref_core import *

def to_cells(v):
    n = v.shape[0]; x = np.zeros((2 * n, 2 * n), bool)
    x[0::2, 0::2] = (v & 1) != 0; x[0::2, 1::2] = (v & 2) != 0; x[1::2, 0::2] = (v & 4) != 0; x[1::2, 1::2] = (v & 8) != 0
    return x
def to_vals(x):
    a, b, c, d = A.parts(x); return (a * 1 + b * 2 + c * 4 + d * 8).astype(np.uint8)

# (a) exhaustive: all tilings of orders 1..5 from the referee's enumeration (rule 'pre', which was checked against brute force)
cur = {bytes([9]), bytes([6])}; tot = 0; bad_scan = 0; bad_pre = 0; bad_order = {"reverse": 0, "columns": 0}
import itertools
for n in range(1, 6):
    nxt = set()
    for key in cur:
        old = np.frombuffer(key, np.uint8).reshape(n, n)
        y = A.shuffle(to_cells(old)); h = A.holes(y)
        new = shift(old); pre = new == 0; new = LUT_DELSWAP[new]
        assert (to_vals(y) == new).all()
        tot += 1
        scan = sequential_fill_set(new)
        bad_scan += int((h != scan).any()); bad_pre += int((h != pre).any())
        # other scan orders: reversed reading order, column-major
        bad_order["reverse"] += int((sequential_fill_set(new[::-1, ::-1].copy() if False else LUT_SWAP[new][::-1, ::-1])[::-1, ::-1] != scan).any())
        bad_order["columns"] += int((sequential_fill_set(np.array([[v & 9 | ((v & 2) << 1) | ((v & 4) >> 1) for v in row] for row in new.T], np.uint8)).T != scan).any())
        if n < 5:
            idx = np.flatnonzero(pre.ravel()); flat = new.ravel().copy()
            for ch in itertools.product((9, 6), repeat=len(idx)):
                flat[idx] = ch; nxt.add(flat.tobytes())
    cur = nxt if n < 5 else cur
    print(f"order {n} -> {n+1}: tilings so far {tot}; holes() != plain scan: {bad_scan}; holes() != empty-before-deletion: {bad_pre}; scan order changes the set (reverse, column-major): {bad_order}", flush=True)
# random larger tilings: holes() vs a plain Python scan, orders 2..120, 3 growths
rng = np.random.default_rng(5); nb = 0; steps = 0
for g in range(3):
    v = np.zeros((0, 0), np.uint8)
    for n in range(1, 121):
        if n > 1:
            y = A.shuffle(to_cells(v)); h = A.holes(y); steps += 1
            nb += int((h != sequential_fill_set(to_vals(y))).any())
        v, _ = grow_step(v, rng)
print(f"random tilings, orders 1..119 shuffled once, 3 growths: {steps} steps; holes() != plain scan in {nb}")

# (b) definitions of the frozen region on saved tilings (40 growths at 100, 200, 400)
Z = np.load("/home/agent2/aztec/referee/s_a.npz")
def corner_views(v):
    """the four corners brought to the top-left with their dimer relabelled as a."""
    fl = np.zeros(16, np.uint8); ud = np.zeros(16, np.uint8)
    for x in range(16):
        a, b, c, d = x & 1, (x >> 1) & 1, (x >> 2) & 1, (x >> 3) & 1
        fl[x] = b | (a << 1) | (d << 2) | (c << 3)      # mirror left-right: a<->b, c<->d
        ud[x] = c | (d << 1) | (a << 2) | (b << 3)      # mirror up-down: a<->c, b<->d
    return [v, fl[v][:, ::-1], ud[v][::-1, :], ud[fl[v]][::-1, ::-1]]
for n in (100, 200, 400):
    rows = []
    for g in range(40):
        v = Z[f"g{g}_n{n}"]; r = []
        for w in corner_views(v):
            ea = w == 1
            lab, _ = ndimage.label(ea); flood4 = int((lab == lab[0, 0]).sum()) if ea[0, 0] else 0
            lab8, _ = ndimage.label(ea, structure=np.ones((3, 3))); flood8 = int((lab8 == lab8[0, 0]).sum()) if ea[0, 0] else 0
            L = np.argmin(np.hstack([ea, np.zeros((n, 1), bool)]), axis=1)      # leading run of exactly-a blocks in each row
            stair = int(L.sum())
            mono = bool((np.diff(L) <= 0).all())
            # 'a present' (a alone or a with d) flood, the polar region counted by north-going dominoes
            ha = (w & 1) != 0; labp, _ = ndimage.label(ha); floodp = int((labp == labp[0, 0]).sum()) if ha[0, 0] else 0
            Kd = K_of(w); Kfl = int(np.argmin(np.append(np.diagonal(lab == lab[0, 0]) if ea[0, 0] else np.zeros(n, bool), False)))
            Krow = int(np.argmin(np.append(L[np.arange(n)] > np.arange(n), False)))
            r.append([flood4, flood8, stair, floodp, mono, Kd, Kfl, Krow])
        rows.append(r)
    R = np.array(rows, float)      # growth x corner x stat
    f4, f8, st, fp = (R[:, :, i].sum(1).mean() / n ** 2 for i in range(4))
    lim = 1 - np.pi / 4
    print(f"n={n}: frozen fraction, author's definition (4-neighbour flood, exactly one dimer) {f4:.5f}; 8-neighbour flood {f8:.5f}; staircase (leading runs of rows) {st:.5f}; "
          f"flood through blocks holding the corner's dimer at all {fp:.5f}")
    print(f"      (fraction - 0.2146) n^(2/3): {(f4-lim)*n**(2/3):.3f}, {(f8-lim)*n**(2/3):.3f}, {(st-lim)*n**(2/3):.3f}, {(fp-lim)*n**(2/3):.3f}; "
          f"leading runs non-increasing in every corner: {bool(R[:,:,4].all())}; K by diagonal == K by flood == K by leading runs in all 160 corners: {bool((R[:,:,5]==R[:,:,6]).all() and (R[:,:,5]==R[:,:,7]).all())}; "
          f"mean K over the four corners {R[:,:,5].mean():.3f} (sd between corners of one tiling {R[:,:,5].std(axis=1,ddof=1).mean():.3f}, correlation between corners {np.corrcoef(R[:,:,5].T)[np.triu_indices(4,1)].mean():+.2f})")
