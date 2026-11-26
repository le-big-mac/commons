"""Is the whole north polar region at order n my strictly frozen region at order n + 1?   Added 26 November 2026.
usage: python -I region.py [growths] [order] [first seed] > region.out      (numpy, scipy; aztec.py beside it)
P (order n): blocks holding the dimer a, alone or with d, joined to block (0, 0) side by side through such blocks.
S (order n + 1, the same growth): blocks holding exactly a, joined to block (0, 0) side by side through such blocks."""
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from multiprocessing import Pool
import aztec

def region(x, tosses, strict):
    from scipy.ndimage import label
    a, b, c, d = aztec.parts(x)
    mask = (a & ~b & ~c & ~d) if strict else a
    if not mask[0, 0]: return frozenset()
    lab, _ = label(mask)
    return frozenset(map(tuple, np.argwhere(lab == lab[0, 0])))

def job(arg):
    seed, n = arg; rng = np.random.default_rng(seed); out = {}
    def rd(x, t):
        return region(x, t, strict=False), region(x, t, strict=True)
    _, _, out = aztec.grow(n + 1, rng, rd, at=(n, n + 1))
    P, S = out[n][0], out[n + 1][1]
    diag = lambda R: next((k for k in range(n + 2) if (k, k) not in R), n + 2)
    # the last two are controls, added after the sealed run: the two kinds of region at ONE order, and P at two orders
    return (P == S, len(P), len(S), len(P - S), len(S - P), diag(P), diag(S), out[n][0] == out[n][1], out[n][0] == out[n + 1][0])

if __name__ == '__main__':
    G = int(sys.argv[1]) if len(sys.argv) > 1 else 2000; n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    seed0 = int(sys.argv[3]) if len(sys.argv) > 3 else 660000
    with Pool(8) as p: res = np.array(p.map(job, [(seed0 + s, n) for s in range(G)], chunksize=50), dtype=int)
    same = int(res[:, 0].sum())
    print(f"{G} growths (seeds {seed0} on), each read at order {n} and at order {n + 1}")
    print(f"P and S are the same set in {same} of {G}; mean size of P {res[:, 1].mean():.1f} blocks, of S {res[:, 2].mean():.1f}")
    print(f"the depth on the diagonal is the same in {int((res[:, 5] == res[:, 6]).sum())} of {G}")
    diff = res[res[:, 0] == 0]
    if len(diff):
        print(f"where they differ ({len(diff)} growths): blocks in P and not in S, mean {diff[:, 3].mean():.2f}, most {diff[:, 3].max()}; in S and not in P, mean {diff[:, 4].mean():.2f}, most {diff[:, 4].max()};"
              f" P the larger in {int((diff[:, 1] > diff[:, 2]).sum())}, S the larger in {int((diff[:, 2] > diff[:, 1]).sum())}, equal in size in {int((diff[:, 1] == diff[:, 2]).sum())}")
    print(f"controls, added after the sealed run: at order {n} alone the polar region and the strictly frozen region are the same set in {int(res[:, 7].sum())} of {G};"
          f" the polar region at order {n} and at order {n + 1} are the same set in {int(res[:, 8].sum())} of {G}")
