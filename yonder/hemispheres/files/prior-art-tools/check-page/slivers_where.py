"""Where are the people of the two slivers (inside exactly one of the half centred 52.37 N, 12.68 E and the half centred 46.0 N, 7.18 E)?
Prints the people of each sliver by box of 5 degrees, 2020 grid, hard edge, to see which countries they fall in.
usage: python -I slivers_where.py GRID_DIR"""
import sys, math
import numpy as np
G = sys.argv[1]
H, W = 3600, 7200
lat = np.radians(-90 + (np.arange(H) + 0.5) * 0.05); lon = np.radians(-180 + (np.arange(W) + 0.5) * 0.05)
def inside(la, lo):
    la, lo = math.radians(la), math.radians(lo)
    return (np.sin(lat)[:, None] * math.sin(la) + (np.cos(lat)[:, None] * math.cos(la)) * (np.cos(lon)[None, :] * math.cos(lo) + np.sin(lon)[None, :] * math.sin(lo))) > 0
p = np.load(G + "/pop005.npy").astype(np.float64)
B = inside(52.37, 12.68); A = inside(46.0, 7.18)
for name, m in (("only in the Berlin half", B & ~A), ("only in the Alpine half", A & ~B)):
    q = np.where(m, p, 0.0)
    print("== %s: %.1f million" % (name, q.sum() / 1e6))
    box = q.reshape(36, 100, 72, 100).sum(axis=(1, 3))   # 5-degree boxes
    out = []
    for i in range(36):
        for j in range(72):
            if box[i, j] > 5e4:
                out.append((box[i, j], -90 + 5 * i, -180 + 5 * j))
    for v, la, lo in sorted(out, reverse=True):
        print("   lat %4d to %4d, lon %5d to %5d: %7.2f million" % (la, la + 5, lo, lo + 5, v / 1e6))
