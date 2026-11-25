"""Referee: is the walked distance the length of the ROUTE, or does it include cell-scale zig-zag?
For the last walkers of each blind run: length of the track at full time resolution (= time walked), and of the same track
sampled every k steps (k steps = k/2 cells), all divided by the straight distance (1)."""
import sys, numpy as np
for fn in sys.argv[1:]:
    d = np.load(fn)
    rows = []
    for k in range(6):
        for q in range(int(d[f"ntrk{k}"])):
            tr = d[f"trk{k}_{q}"]
            def plen(step):
                idx = np.r_[np.arange(0, len(tr) - 1, step), len(tr) - 1]
                return np.hypot(*np.diff(tr[idx], axis=0).T).sum()
            rows.append([plen(s) for s in (1, 4, 8, 16, 32, 64)])
    r = np.array(rows)
    print(f"{fn.split('/')[-1]}: cap {float(d['cap'])}, {len(r)} tracks; length sampled every 1,4,8,16,32,64 steps: " + " ".join(f"{v:.4f}" for v in r.mean(0))
          + f" | detour of run {float(d['mean_detour']):.4f}")
