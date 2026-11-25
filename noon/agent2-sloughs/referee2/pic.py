"""pic.py -- my open reaches, drawn.  usage: python -I pic.py out.png file.xy [...]"""
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fs = sys.argv[2:]
fig, axs = plt.subplots(len(fs), 1, figsize=(12, 3.2 * len(fs)))
for ax, f in zip(np.atleast_1d(axs), fs):
    a = np.loadtxt(f)
    ax.plot(a[:, 0], a[:, 1], lw=0.8, color="#2a78d6"); ax.plot(a[0, 0], a[0, 1], "ko", ms=4); ax.plot(a[-1, 0], a[-1, 1], "o", mfc="w", mec="k", ms=4)
    ax.set_aspect("equal"); ax.set_title(f, loc="left", fontsize=9); ax.set_xlim(-30, 360)
fig.tight_layout(); fig.savefig(sys.argv[1], dpi=70)
