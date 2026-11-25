"""Referee: Noon's measure.py (unmodified copy) applied to the full footstep map, to one-direction-only maps, and at other thresholds."""
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "/home/agent2/referee-trails/noon_copy")
import numpy as np
from measure import measure, footmask
print("cap  | L all (Noon's mask) | L clockwise-only, L anticlockwise-only (same absolute threshold) | L all at threshold frac 0.02 0.05 0.10 0.20 0.40 | L from G>0.5max, 0.3max, 0.15max | n loops in skeleton (all)")
for fn in sys.argv[1:]:
    d = np.load(fn)
    h = float(d['h']); foot = d['foot']; f6 = d['foot6']; pairs = [tuple(p) for p in d['pairs']]
    ref = np.percentile(foot[foot > 0], 98)
    L, skel, br, nodes = measure(footmask(d), h)
    cw = sum(f6[pairs.index(p)] for p in [(0, 1), (1, 2), (2, 0)]); ccw = sum(f6[pairs.index(p)] for p in [(1, 0), (2, 1), (0, 2)])
    Lcw = measure(cw > 0.10 * ref, h)[0]; Lccw = measure(ccw > 0.10 * ref, h)[0]
    Lf = [measure(foot > f * ref, h)[0] for f in (0.02, 0.05, 0.10, 0.20, 0.40)]
    G = d['G']
    Lg = [measure(G > f * G.max(), h)[0] for f in (0.5, 0.3, 0.15)]
    # loops = E - V + components (Euler), from the traced graph
    ends = {}
    for b in br:
        for p in (tuple(b[0].astype(int)), tuple(b[-1].astype(int))): ends[p] = ends.get(p, 0) + 1
    from scipy.ndimage import label
    ncomp = label(skel, structure=np.ones((3, 3)))[1]
    loops = len(br) - len(ends) + ncomp
    print(f"{float(d['cap']):.1f}  | {L:.3f} | {Lcw:.3f} {Lccw:.3f} | " + " ".join(f"{v:.3f}" for v in Lf) + " | " + " ".join(f"{v:.3f}" for v in Lg) + f" | {loops}")
