"""open-picture.py -- two open reaches at t = 125 (seed 1, one paper's values): the first node fixed at the left, the last free.
Above: nothing comes in at the first node.  Below: the first node is given the curvature of the far end, the paper's rule.
usage: python open-picture.py"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK, MUTED, SURF, WATER = "#0b0b0b", "#52514e", "#fcfcfb", "#2a78d6"
def at(fn, t):
    for line in open(fn):
        f = line.split()
        if abs(float(f[0]) - t) < 1e-6: return np.array(f[2:], float).reshape(-1, 2)
fig, axs = plt.subplots(2, 1, figsize=(13, 6.6), facecolor=SURF)
for ax, (fn, label) in zip(axs, (("out/open/quiet-s1.snap", "nothing comes in at the fixed first node"), ("out/open/fed-s1.snap", "the first node is given the curvature of the far end (the paper's rule, as I read it)"))):
    xy = at(fn, 125.0); L = np.hypot(*np.diff(xy, axis=0).T).sum(); d = np.hypot(*(xy[-1] - xy[0]))
    ax.plot(xy[:, 0], xy[:, 1], color=WATER, lw=1.1, solid_joinstyle="round"); ax.plot([xy[0, 0]], [xy[0, 1]], "o", color=INK, ms=5); ax.plot([xy[-1, 0]], [xy[-1, 1]], "o", mfc=SURF, mec=INK, ms=5)
    ax.set_aspect("equal"); ax.set_xlim(-25, 345); ax.set_ylim(-52, 52); ax.set_facecolor(SURF)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(MUTED); ax.set_yticks([]); ax.tick_params(colors=MUTED, labelsize=8)
    ax.set_title("%s — at t = 125: length ÷ distance between the ends = %.2f" % (label, L / d), loc="left", fontsize=10, color=INK)
axs[-1].set_xlabel("distance along the valley, in units of D0 (filled dot: the fixed first node; open dot: the free end)", color=INK, fontsize=9)
fig.tight_layout(); fig.savefig("open.png", dpi=100); print("open.png written")
