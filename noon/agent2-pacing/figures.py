"""Figures for the pacing of the ice ages.   usage: python -I figures.py results.npz toy.npz OUTDIR"""
import sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
r, toy, OUT = np.load(sys.argv[1]), np.load(sys.argv[2]), sys.argv[3]
os.makedirs(OUT, exist_ok=True)
INK, MUTED, GRID = "#2b2622", "#6f675e", "#e4dfd6"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
HALO = [pe.withStroke(linewidth=2.5, foreground="white")]
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False})
T = r['T']
fig = plt.figure(figsize=(13.4, 8.4))
gs = fig.add_gridspec(3, 2, width_ratios=[3.6, 1], height_ratios=[1.5, 1, 1], hspace=0.3, wspace=0.08, left=0.065, right=0.985, top=0.86, bottom=0.075)
a = fig.add_subplot(gs[0, 0]); b = fig.add_subplot(gs[1, 0], sharex=a); c = fig.add_subplot(gs[2, 0], sharex=a)
a.plot(r['grid'], r['raw'], color=BLUE, lw=0.6, alpha=0.45, zorder=2)
a.plot(r['grid'], r['sm'], color=BLUE, lw=2, zorder=3)
for lvl, name in ((float(r['L']), "L"), (float(r['U']), "U")):
    a.axhline(lvl, color=MUTED, lw=0.8, ls=(0, (4, 3)), zorder=1)
    a.text(802, lvl + 0.2, name, fontsize=9, color=MUTED, ha="right", va="bottom")
a.set_ylabel("temperature at Dome C,\nrelative to the last 1,000 years (°C)")
b.plot(r['oage'], r['obl'], color=INK, lw=1.4)
b.set_ylabel("tilt of the axis (°)")
c.plot(r['oage'], -r['prec'], color=INK, lw=1.2)
c.set_ylabel("precession:\nnorthern summer\nnearer the Sun  →")
c.set_yticks([])
for ax in (a, b, c):
    for t in T:
        ax.axvline(t, color=ORANGE, lw=1.3, zorder=1)
    ax.grid(axis="y", color=GRID, lw=0.7), ax.set_axisbelow(True), ax.tick_params(length=0)
for t in T:
    a.text(t - 4, 4.6, f"{t:.0f}", fontsize=8.5, color=INK, ha="left", va="bottom", rotation=0, path_effects=HALO)
a.set_xlim(810, 0), a.set_ylim(-11, 6.4)
plt.setp(a.get_xticklabels(), visible=False), plt.setp(b.get_xticklabels(), visible=False)
c.set_xlabel("thousands of years ago  (time runs left to right)")
for k, (ph, name, zero) in enumerate(((r['pt'], "Tilt", "tilt at\nits maximum"), (r['pp'], "Precession", "northern midsummer\nnearest the Sun"))):
    w = fig.add_subplot(gs[k + 1, 1], projection="polar")
    th = np.radians(ph)
    w.set_theta_zero_location("N"), w.set_theta_direction(-1)
    w.scatter(th, np.ones(len(th)), s=46, color=ORANGE, edgecolor="white", lw=1, zorder=3, clip_on=False)
    m = np.exp(1j * th).mean()
    w.annotate("", xy=(np.angle(m), abs(m)), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
    w.set_ylim(0, 1.0), w.set_yticks([]), w.set_xticks(np.radians([0, 90, 180, 270]))
    w.set_xticklabels([zero, "", "", ""], fontsize=8)
    w.spines["polar"].set_color(GRID), w.grid(color=GRID, lw=0.7)
    w.set_title(f"{name}: R = {abs(m):.2f}", fontsize=10.5, color=INK, pad=22)
t0 = fig.add_subplot(gs[0, 1]); t0.axis("off")
t0.text(0.0, 0.95, "Each orange line is a\ntermination: the temperature\nrising from below L to above U.\n\nThe wheels show where in\neach cycle the ten fall.\nTime runs clockwise; the arrow\nis their mean. R = 1 would be\nall at one point, R = 0 evenly\nspread.", fontsize=9.5, color=INK, va="top", linespacing=1.45, transform=t0.transAxes)
fig.suptitle("The ice ages end when the tilt is rising", x=0.065, y=0.975, ha="left", fontsize=15, color=INK)
fig.text(0.065, 0.915, "Dome C ice core (Antarctica) on its own time scale, against the orbit computed by Laskar and others. Ten terminations in 800,000 years.", fontsize=9.5, color=MUTED)
fig.savefig(f"{OUT}/pacing.png", dpi=125, facecolor="white")
plt.close(fig)

fig, ax = plt.subplots(figsize=(8.6, 5.0))
for key, col, name in (("mean0", MUTED, "threshold fixed: no pull from the tilt"), ("mean10", BLUE, "threshold lower when the tilt is high")):
    ax.plot(toy['T0s'], toy[key], color=col, lw=2, label=name)
for k in (1, 2, 3):
    ax.axhline(41 * k, color=GRID, lw=1, zorder=0)
    ax.text(171, 41 * k, f"{k} tilt cycle{'s' if k > 1 else ''}", fontsize=9, color=MUTED, va="center")
ax.set_xlim(20, 170), ax.set_ylim(15, 175)
ax.set_xlabel("how much ice it takes to collapse (in thousands of years of growth)"), ax.set_ylabel("mean time between collapses (thousand years)")
ax.tick_params(length=0)
ax.legend(loc="upper left", frameon=False, fontsize=9.5)
fig.suptitle("A toy ice sheet locks to the tilt in whole numbers of cycles", x=0.09, y=0.975, ha="left", fontsize=13.5, color=INK)
fig.text(0.09, 0.905, "Ice grows steadily and collapses past a threshold. The tilt is the real one of the last two million years.", fontsize=9, color=MUTED)
fig.subplots_adjust(left=0.09, right=0.88, top=0.86, bottom=0.11)
fig.savefig(f"{OUT}/toy.png", dpi=125, facecolor="white")
