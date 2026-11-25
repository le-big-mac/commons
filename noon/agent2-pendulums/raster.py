"""The piece written out: one row per voice, one dot per strike.   usage: python raster.py pendula.json raster.png"""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
J = json.load(open(sys.argv[1])); S = J['strikes']; T = J['T']; N = J['N']
INK, MUTED, GRID = "#2b2622", "#6f675e", "#e4dfd6"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
fig = plt.figure(figsize=(12.4, 5.6)); ax = fig.add_axes([0.07, 0.13, 0.9, 0.68])
lo, hi = np.array([18, 62, 125]) / 255, np.array([150, 196, 245]) / 255
for f, lab in ((0, "all sixteen"), (1 / 4, "every 4th"), (1 / 3, "every 3rd"), (1 / 2, "every 2nd"), (2 / 3, "every 3rd"), (3 / 4, "every 4th"), (1, "all sixteen")):
    ax.axvline(f * T, color=GRID, lw=1.2, zorder=0); ax.text(f * T, N - 0.25, lab, ha='center', va='bottom', fontsize=8.5, color=MUTED)
t = np.array([s[0] for s in S]); k = np.array([s[1] for s in S])
ax.scatter(t, k, s=13, c=[lo + (hi - lo) * x / (N - 1) for x in k], linewidths=0, zorder=2)
ax.set_xlim(-2, T + 2); ax.set_ylim(-0.8, N + 0.6); ax.set_xticks(np.arange(0, T + 1, 12)); ax.set_yticks([0, N - 1]); ax.set_yticklabels(["lowest,\nslowest", "highest,\nfastest"])
ax.set_xlabel("seconds"); ax.tick_params(length=0)
for sp in ax.spines.values(): sp.set_visible(False)
fig.suptitle("Sixteen pendulums", x=0.07, y=0.96, ha='left', fontsize=15, color=INK)
fig.text(0.07, 0.885, "Every dot is one note. Each voice keeps a steady beat of its own; the patterns are only the beats drifting past one another.", fontsize=10, color=MUTED)
fig.savefig(sys.argv[2], dpi=130, facecolor='white')
