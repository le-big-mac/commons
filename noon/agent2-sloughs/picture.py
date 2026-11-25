"""picture.py -- what four of the rivers look like: the centre line at one moment, 120 D of valley each.   usage: python picture.py"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK, MUTED, SURF, WATER = "#0b0b0b", "#52514e", "#fcfcfb", "#2a78d6"
cases = [("out/look/P2-dc0.4.snap", "P = 2, cutoff distance 0.4 D"), ("out/look/P3-dc0.4.snap", "P = 3, cutoff distance 0.4 D (the setting of the page)"),
         ("out/look/P6-dc0.4.snap", "P = 6, cutoff distance 0.4 D"), ("out/look/P3-dc1.6.snap", "P = 3, cutoff distance 1.6 D")]
LX = 120.0
fig, axs = plt.subplots(2, 2, figsize=(13, 7.4), facecolor=SURF)
for ax, (fn, label) in zip(axs.ravel(), cases):
    f = open(fn).read().strip().split("\n")[-1].split(); t = float(f[0]); xy = np.array(f[2:], float).reshape(-1, 2)
    x, y = xy[:, 0], xy[:, 1]; y = y - y.mean()
    xx = np.concatenate([x, x[:1] + LX]); yy = np.concatenate([y, y[:1]])
    S = np.hypot(np.diff(xx), np.diff(yy)).sum() / LX
    base = -LX * np.floor(x[0] / LX)
    for k in (-1, 0, 1): ax.plot(xx + base + k * LX, yy, color=WATER, lw=1.3, solid_joinstyle="round")
    ax.set_xlim(0, LX); ax.set_ylim(-32, 32); ax.set_aspect("equal"); ax.set_facecolor(SURF)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(MUTED); ax.set_yticks([]); ax.tick_params(colors=MUTED, labelsize=8)
    ax.set_title("%s\nat this moment (t = %g): length ÷ valley length = %.2f" % (label, t, S), loc="left", fontsize=9.5, color=INK)
for ax in axs[-1]: ax.set_xlabel("distance along the valley, in units of D", color=INK, fontsize=9)
fig.tight_layout(); fig.savefig("rivers.png", dpi=100); print("rivers.png written")
