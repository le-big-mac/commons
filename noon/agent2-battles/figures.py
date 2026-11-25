"""One figure: the attacker's share of wins by force ratio, world-war rows against the rest.   usage: python -I figures.py results.json out.png"""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
R = json.load(open(sys.argv[1]))
INK, MUTED, GRID, BLUE, ORANGE = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
names = ["under ½", "½ to ¾", "¾ to 1", "1 to 1½", "1½ to 2", "2 to 3", "3 or more"]
S = R['split']
fig, ax = plt.subplots(figsize=(10.6, 6.4))
ax.axhline(50, color=INK, lw=0.9, zorder=1)
for key, col, off in (("all other rows", BLUE, -0.13), ("world-war rows", ORANGE, +0.13)):
    bs = S[key]['bands']
    xs = np.arange(len(bs)) + off
    ax.plot(xs, [100 * b['p'] for b in bs], color=col, lw=1.6, zorder=2, alpha=0.55)
    for x, b in zip(xs, bs):
        ax.plot([x, x], [100 * b['ci'][0], 100 * b['ci'][1]], color=col, lw=2, zorder=3, solid_capstyle='round')
        ax.scatter([x], [100 * b['p']], s=70, color=col, edgecolor='white', lw=1.2, zorder=4)
for i in range(len(names)):
    ax.text(i - 0.13, -2.5, f"{S['all other rows']['bands'][i]['n']}", ha='center', va='top', fontsize=9, color=MUTED)
    ax.text(i + 0.13, -8.5, f"{S['world-war rows']['bands'][i]['n']}", ha='center', va='top', fontsize=9, color=MUTED)
ax.text(-0.62, -2.5, "battles, other:", ha='right', va='top', fontsize=9, color=MUTED)
ax.text(-0.62, -8.5, "world wars:", ha='right', va='top', fontsize=9, color=MUTED)
ax.text(6.45, 51.5, "even chances", ha='right', va='bottom', fontsize=9, color=INK)
ax.set_xticks(range(len(names))), ax.set_xticklabels(names, fontsize=10, color=INK)
ax.tick_params(axis='x', pad=34)
ax.set_xlim(-1.6, 6.5), ax.set_ylim(-1, 101), ax.set_yticks(range(0, 101, 20)), ax.set_yticklabels([f"{v}%" for v in range(0, 101, 20)])
ax.set_xlabel("attacker's men for each of the defender's"), ax.set_ylabel("battles the attacker won (bars: 95% intervals)")
ax.grid(axis='y', color=GRID, lw=0.8), ax.set_axisbelow(True), ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.legend(handles=[Line2D([], [], marker='o', ls='-', lw=1.6, ms=8, color=ORANGE, mec='white', label=f"battles of the two world wars ({S['world-war rows']['n']})"),
                   Line2D([], [], marker='o', ls='-', lw=1.6, ms=8, color=BLUE, mec='white', label=f"all other battles, 1600 to 1982 ({S['all other rows']['n']})")],
          loc='upper left', bbox_to_anchor=(0.0, 1.10), frameon=False, fontsize=10, ncols=2, columnspacing=2.0)
fig.suptitle("More men went with winning in the two world wars, and nowhere else in the table", x=0.075, y=0.975, ha='left', fontsize=13.5, color=INK)
fig.subplots_adjust(left=0.075, right=0.985, top=0.84, bottom=0.185)
fig.savefig(sys.argv[2], dpi=130, facecolor='white')
