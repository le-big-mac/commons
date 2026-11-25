"""Referee: a length estimate that uses no threshold and no skeleton.
Each of the six routes (ordered pairs) is reduced to its mean path (footstep centroid in 100 slices along the chord, plus the two gates).
L(delta) = sum over routes of the integral of ds / m, where m = 1 + number of OTHER routes passing within delta of that point.
delta -> 0 counts every route separately except where they truly coincide; large delta merges near-parallel trails."""
import sys, numpy as np
from direction import load
NS = 100
def meanpath(c, A, B):
    x, y, w = c
    ax = (B - A) / np.linalg.norm(B - A); Lab = np.linalg.norm(B - A)
    s = ((x - A[0]) * ax[0] + (y - A[1]) * ax[1]) / Lab
    b = np.floor(s * NS).astype(int); ok = (b >= 0) & (b < NS)
    sw = np.bincount(b[ok], w[ok], NS); good = sw > 0
    px = np.bincount(b[ok], w[ok] * x[ok], NS)[good] / sw[good]; py = np.bincount(b[ok], w[ok] * y[ok], NS)[good] / sw[good]
    return np.vstack([A, np.c_[px, py], B])
def dist_to_poly(P, Q):
    """distance from each point of P to polyline Q"""
    a = Q[:-1][None]; b = Q[1:][None]; p = P[:, None]
    ab = b - a; t = np.clip(((p - a) * ab).sum(-1) / np.maximum((ab * ab).sum(-1), 1e-18), 0, 1)
    return np.hypot(*np.moveaxis(p - (a + t[..., None] * ab), -1, 0)).min(1)
deltas = [0.5, 1, 2, 3, 4, 5, 6, 8, 12]
print("cap | sum of the six mean-path lengths | L(delta) for delta (cells) = " + " ".join(str(d) for d in deltas))
for fn in sys.argv[1:]:
    gates, h, cl, det, cap = load(fn)
    paths = {k: meanpath(cl[k], gates[k[0]], gates[k[1]]) for k in cl}
    tot = sum(np.hypot(*np.diff(p, axis=0).T).sum() for p in paths.values())
    out = []
    for dl in deltas:
        L = 0.0
        for k, p in paths.items():
            mid = 0.5 * (p[1:] + p[:-1]); seg = np.hypot(*np.diff(p, axis=0).T)
            m = np.ones(len(mid))
            for k2, q in paths.items():
                if k2 != k:
                    m += dist_to_poly(mid, q) <= dl * h
            L += (seg / m).sum()
        out.append(L)
    print(f"{cap:.1f} | {tot:.3f} | " + " ".join(f"{v:.2f}" for v in out) + f"   [{fn.split('/')[-1]}]")
