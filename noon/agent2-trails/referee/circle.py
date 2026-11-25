import sys, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
GATES = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]]); O = GATES.mean(0)
d = np.load("out2/run_c0.90_s0.npz")
tot = []; near = []; wind = []
fig, axs = plt.subplots(1, 3, figsize=(21, 7))
n = 0
for k in range(6):
    for q in range(int(d[f"ntrk{k}"])):
        tr = d[f"trk{k}_{q}"]
        c = tr[::8]; v = np.diff(c, axis=0); th = np.unwrap(np.arctan2(v[:, 1], v[:, 0]))
        tot.append(np.degrees(np.abs(np.diff(th)).sum())); 
        r = np.hypot(*(tr - O).T); near.append((r < 0.08).sum() * (1 / 320))            # time within 0.08 of the centre
        ang = np.unwrap(np.arctan2(*(tr - O).T[::-1])); wind.append(np.degrees(abs(ang[-1] - ang[0])))
        if n < 12:
            axs[0].plot(tr[:, 0], tr[:, 1], lw=0.6)
            axs[1].plot(tr[:, 0], tr[:, 1], lw=0.6, marker='.', ms=1.5)
            if n < 3: axs[2].plot(tr[:, 0], tr[:, 1], lw=0.6, marker='.', ms=3)
        n += 1
axs[0].set_aspect('equal'); axs[0].set_title("cap 0.9: 12 complete tracks")
axs[1].set_xlim(0.38, 0.62); axs[1].set_ylim(0.17, 0.41); axs[1].set_aspect('equal'); axs[1].set_title("zoom on the junction (0.24 x 0.24)")
axs[2].set_xlim(0.20, 0.26); axs[2].set_ylim(0.09, 0.15); axs[2].set_aspect('equal'); axs[2].set_title("zoom on an arm (0.06 x 0.06 = 9.6 cells); dots = steps")
plt.tight_layout(); plt.savefig("cap09_tracks.png", dpi=70)
print(f"cap 0.9, {n} complete tracks: total turning of the route (heading over 4 cells) mean {np.mean(tot):.0f} deg, max {np.max(tot):.0f} deg; "
      f"angle swept round the centre mean {np.mean(wind):.0f} deg, max {np.max(wind):.0f} deg (a straight Y route sweeps 120); "
      f"time within 0.08 of the centre mean {np.mean(near):.3f} (straight through: about 0.16)")
