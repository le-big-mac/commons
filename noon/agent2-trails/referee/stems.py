"""Referee: at each gate, separation of the two OUTBOUND routes and of the two INBOUND routes vs distance from the gate."""
import sys, numpy as np
from direction import load
def cent(c, g, r0, dr=0.01):
    r = np.hypot(c[0] - g[0], c[1] - g[1]); m = (r >= r0 - dr) & (r < r0 + dr)
    if c[2][m].sum() <= 0: return np.array([np.nan, np.nan])
    return np.array([np.average(c[0][m], weights=c[2][m]), np.average(c[1][m], weights=c[2][m])])
R = [0.03, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40]
print("separation (in cells of 1/160) between two routes' footstep centroids at distance r from their common gate, mean over the three gates")
print("file".ljust(26), "kind     ", "  ".join(f"r={r:.2f}" for r in R))
for fn in sys.argv[1:]:
    gates, h, cl, det, cap = load(fn)
    so = np.zeros((3, len(R))); si = np.zeros((3, len(R)))
    for g in range(3):
        o = [k for k in range(3) if k != g]
        for j, r in enumerate(R):
            so[g, j] = np.hypot(*(cent(cl[(g, o[0])], gates[g], r) - cent(cl[(g, o[1])], gates[g], r))) / h
            si[g, j] = np.hypot(*(cent(cl[(o[0], g)], gates[g], r) - cent(cl[(o[1], g)], gates[g], r))) / h
    nm = fn.split('/')[-1]
    print(nm.ljust(26), "leaving  ", "  ".join(f"{v:6.1f}" for v in so.mean(0)))
    print(nm.ljust(26), "arriving ", "  ".join(f"{v:6.1f}" for v in si.mean(0)))
