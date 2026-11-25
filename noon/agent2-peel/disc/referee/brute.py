# Brute-force check of peel.c: a point is on the hull boundary iff the directions
# to all other points leave an angular gap >= pi (definition, no hull algorithm).
import sys, math
import numpy as np

def brute_depth(pts):
    n = len(pts)
    depth = np.zeros(n, int)
    alive = np.ones(n, bool)
    layer = 0
    while alive.any():
        layer += 1
        ids = np.nonzero(alive)[0]
        if len(ids) <= 2:
            depth[ids] = layer
            break
        off = []
        for i in ids:
            others = ids[ids != i]
            d = pts[others] - pts[i]
            ang = np.sort(np.arctan2(d[:, 1], d[:, 0]))
            gaps = np.diff(np.concatenate([ang, [ang[0] + 2 * math.pi]]))
            if gaps.max() >= math.pi:
                off.append(i)
        depth[off] = layer
        alive[off] = False
    return depth

clouds = []
cur = []
for line in open(sys.argv[1]):
    if line.startswith('#'):
        clouds.append(np.array(cur)); cur = []
    else:
        cur.append([float(t) for t in line.split()])
bad = 0
for c in clouds:
    pts = c[:, :2]; d = c[:, 2].astype(int)
    b = brute_depth(pts)
    nb = int((b != d).sum())
    bad += nb
    print(len(pts), 'points, layers', d.max(), b.max(), 'mismatches', nb)
print('TOTAL MISMATCHES', bad, 'in', len(clouds), 'clouds')
