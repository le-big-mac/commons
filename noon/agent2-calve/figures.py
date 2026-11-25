"""The figure.   usage: python figures.py berg.png"""
import sys, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import berg
D = berg.D
INK, MUTED, GRID, BLUE, ORANGE, AQUA, YELLOW, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
def style(ax, title):
    ax.grid(color=GRID, lw=0.8); ax.set_axisbelow(True); ax.tick_params(length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(title, loc='left', fontsize=10.5, color=INK, pad=8)
fig = plt.figure(figsize=(12.4, 8.6))
# (a) which way up
ax = fig.add_axes([0.06, 0.53, 0.52, 0.30]); es = np.round(np.concatenate([np.arange(0.30, 0.73, 0.02), np.arange(0.7300, 0.7560, 0.0005), np.arange(0.76, 1.32, 0.02), np.arange(1.3200, 1.3640, 0.0005), np.arange(1.37, 1.61, 0.02)]), 4)
pts = [(e, t) for e in es for t, _ in berg.minima(float(e), n=720)]
up = [(e, t) for e, t in pts if t < 0.5]; side = [(e, t) for e, t in pts if t > 89.5]; lean = [(e, t) for e, t in pts if 0.5 <= t <= 89.5]
ax.plot([e for e, _ in up], [t for _, t in up], color=BLUE, lw=2.6); ax.plot([e for e, _ in side], [t for _, t in side], color=ORANGE, lw=2.6)
for seg in ([p for p in lean if p[0] < 1], [p for p in lean if p[0] > 1]): ax.plot([e for e, _ in seg], [t for _, t in seg], color=AQUA, lw=2.6)
ax.text(1.15, 5, "upright", color=BLUE, fontsize=9.5); ax.text(0.45, 82, "on its side", color=ORANGE, fontsize=9.5); ax.annotate("leaning", (0.742, 13), xytext=(0.52, 30), color=AQUA, fontsize=9.5, arrowprops=dict(arrowstyle='-', color=AQUA, lw=0.8))
ax.annotate("leaning", (1.345, 78), xytext=(1.42, 55), color=AQUA, fontsize=9.5, arrowprops=dict(arrowstyle='-', color=AQUA, lw=0.8))
ax.axvspan(0.7521, 1.3297, color=NEUTRAL, alpha=0.13, lw=0); ax.text(1.04, 45, "either way up", color=MUTED, fontsize=9, ha='center')
ax.set_xlim(0.3, 1.6); ax.set_ylim(-4, 94); ax.set_yticks([0, 30, 60, 90]); ax.set_xlabel("width of the block as a share of its height"); ax.set_ylabel("tilt at rest, degrees"); style(ax, "Which way up a block of ice can rest")
# inset: the leaning range
ax2 = fig.add_axes([0.66, 0.53, 0.30, 0.30]); seg = [p for p in lean if p[0] < 1]
ax2.plot([e for e, _ in seg], [t for _, t in seg], color=AQUA, lw=2.6); ax2.plot([0.7521, 0.775], [0, 0], color=BLUE, lw=2.6)
tw = np.linspace(0.7364, 0.7520, 60); ax2.plot(tw, [math.degrees(math.atan(math.sqrt(max(0.0, -2 * (e * e / (12 * D) - (1 - D) / 2) / (e * e / (12 * D)))))) for e in tw], color=INK, lw=1, ls=(0, (4, 3)))
ax2.plot([0.7363], [16.9], marker='o', ms=6, color=AQUA, markeredgecolor='white'); ax2.annotate("no lean\nbelow 0.736", (0.7363, 16.9), xytext=(0.7336, 19.0), fontsize=8.5, color=MUTED)
ax2.text(0.756, 9.0, "dashed: the formula\nfor small leans", fontsize=8.5, color=MUTED, ha='left')
ax2.axvline(0.7424, color=MUTED, lw=1, ls=(0, (1, 2))); ax2.text(0.7428, 20.6, "let go upright without friction,\nit is caught only to the right\nof the dotted line", fontsize=8.5, color=MUTED, va='top')
ax2.set_xlim(0.733, 0.775); ax2.set_ylim(-1, 22); ax2.set_xlabel("width as a share of height"); style(ax2, "The narrow range in which it leans")
# (b) energy
ax3 = fig.add_axes([0.06, 0.09, 0.26, 0.31]); e = np.linspace(0.02, 0.7363, 200); ax3.plot(e, (1 - D) * e * (1 - e) / 2, color=ORANGE, lw=2.2); ax3.plot([0.5], [(1 - D) / 8], marker='o', ms=6, color=ORANGE, markeredgecolor='white')
ax3.annotate("a block 800 m tall and 400 m wide:\n6 × 10¹⁰ joules for each metre\nof its length", (0.5, (1 - D) / 8), xytext=(0.27, 0.0012), fontsize=8.5, color=MUTED, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax3.set_xlim(0, 0.8); ax3.set_ylim(0, 0.0145); ax3.set_xlabel("width as a share of height"); ax3.set_ylabel("ice density × g × height³"); style(ax3, "The most a roll can give up")
# (c), (d) dynamics
tr = berg.run(0.5, 1.0, 40.0, dt=0.004)
ax4 = fig.add_axes([0.40, 0.09, 0.26, 0.31]); ax4.plot(tr[:, 0], np.degrees(tr[:, 2]), color=BLUE, lw=2); ax4.axhline(90, color=NEUTRAL, lw=1, ls=(0, (4, 3))); ax4.axhline(180, color=NEUTRAL, lw=1, ls=(0, (4, 3)))
ax4.text(0.6, 93, "on its side", fontsize=8.5, color=MUTED, ha='left'); ax4.text(0.6, 183, "upside down", fontsize=8.5, color=MUTED, ha='left'); ax4.text(21.3, 153, "148.7°", fontsize=8.5, color=BLUE, ha='center'); ax4.text(39.5, 6, "much later it passes 170°", fontsize=8.5, color=MUTED, ha='right')
ax4.set_xlim(0, 40); ax4.set_ylim(0, 195); ax4.set_yticks([0, 45, 90, 135, 180]); ax4.set_xlabel("time, in units of √(height / g): 9 s for 800 m"); ax4.set_ylabel("tilt, degrees"); style(ax4, "Half as wide as tall, let go at 1°, no friction")
ax5 = fig.add_axes([0.72, 0.09, 0.24, 0.31]); ax5.plot(tr[:, 0], tr[:, 1], color=AQUA, lw=2); ax5.axhline(0, color=NEUTRAL, lw=1, ls=(0, (4, 3))); ax5.text(39.5, 0.012, "water line", fontsize=8.5, color=MUTED, ha='right')
ax5.set_xlim(0, 40); ax5.set_ylim(-0.45, 0.06); ax5.set_xlabel("time"); ax5.set_ylabel("height of its centre, in block heights"); style(ax5, "and how it bobs meanwhile")
fig.suptitle("Calved: which blocks of ice stay up, which lean, which roll over", x=0.06, y=0.975, ha='left', fontsize=15, color=INK)
fig.text(0.06, 0.935, "A long block of ice (917 kg/m³) in sea water (1,025 kg/m³), seen end on. Statics exact for a rectangle; the two panels at lower right use the water's\nstatic pressure only: no inertia of the water, no drag, no waves. What those do to a roll is not computed here.", fontsize=9.5, color=MUTED, va='top', linespacing=1.5)
fig.savefig(sys.argv[1], dpi=130, facecolor='white')
