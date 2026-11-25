"""Referee: where along its journey is a walker turned away from the line of sight?  Complete tracks from the blind code.
'route heading' = direction over 4 cells (8 steps); 'step heading' = direction of each single step."""
import sys, numpy as np
GATES = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]]); PAIRS = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]
for fn in sys.argv[1:]:
    d = np.load(fn); cap = float(d['cap'])
    acc = np.zeros((2, 8)); cnt = np.zeros(8); zz = np.zeros(8)
    for k, (a, b) in enumerate(PAIRS):
        A, B, C = GATES[a], GATES[b], GATES[3 - a - b]
        for q in range(int(d[f"ntrk{k}"])):
            tr = d[f"trk{k}_{q}"]
            for kind, lag in ((0, 8), (1, 1)):
                v = tr[lag:] - tr[:-lag]; p = tr[:-lag]
                los = B - p; los /= np.hypot(*los.T)[:, None]; v = v / np.maximum(np.hypot(*v.T), 1e-12)[:, None]
                ang = np.degrees(np.arctan2(los[:, 0] * v[:, 1] - los[:, 1] * v[:, 0], (los * v).sum(1)))
                frac = 1 - np.hypot(*(B - p).T) / np.hypot(*(B - A))          # share of the straight distance already made good
                bins = np.clip((frac * 8).astype(int), 0, 7)
                acc[kind] += np.bincount(bins, np.abs(ang), 8)
                if kind == 1:
                    cnt += np.bincount(bins, minlength=8)
                else:
                    zz += np.bincount(bins, minlength=8)
    print(f"{fn.split('/')[-1]} cap {cap} (max turn {np.degrees(np.arcsin(cap)):.0f} deg). Mean angle between heading and line of sight, by eighth of the distance made good:")
    print("    route (over 4 cells): " + " ".join(f"{v:5.1f}" for v in acc[0] / np.maximum(zz, 1)))
    print("    single steps:         " + " ".join(f"{v:5.1f}" for v in acc[1] / np.maximum(cnt, 1)))
    print("    steps spent per eighth, relative to straight walking (40 steps): " + " ".join(f"{v:5.2f}" for v in cnt / (sum(int(d[f'ntrk{k}']) for k in range(6)) * 40.0)))
