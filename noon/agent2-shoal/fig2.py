"""How forty schools ended at each width of the orientation zone, under the paper's rule and under mine.
usage: python -I fig2.py rule.json trend.json rule.png        (numpy, matplotlib)   Added 26 November 2026."""
import sys, json
sys.dont_write_bytecode = True
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

INK, MUTED, GRID = "#2b2622", "#6f675e", "#e4dfd6"
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#b9b2a7"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
printed = json.load(open(sys.argv[1]))['printed']; mine = json.load(open(sys.argv[2]))
W = (2, 3, 4, 5, 6, 7, 8)
fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.9), sharey=True)
fig.subplots_adjust(left=0.07, right=0.985, top=0.77, bottom=0.2, wspace=0.07)
for ax, rows, title in ((axes[0], printed, "The rule as the paper prints it"), (axes[1], mine, "My variant (each pull scaled to the same strength first)")):
    for i, d in enumerate(W):
        r = [x for x in rows if x[0] == d]
        counts = [sum(x[2] == 'M' for x in r), sum(x[2] == '.' for x in r), sum(x[2] == 'A' for x in r)]
        bottom = 0
        for c, col in zip(counts, (BLUE, GREY, ORANGE)):
            if c:
                ax.bar(i, c, bottom=bottom, width=0.62, color=col, edgecolor="white", linewidth=2)
                if c >= 3: ax.text(i, bottom + c / 2, str(c), ha="center", va="center", fontsize=9.5, color="white" if col != GREY else INK)
                else: ax.text(i + 0.36, bottom + c / 2, str(c), ha="left", va="center", fontsize=8.5, color=INK)
            bottom += c
    ax.set_xticks(range(len(W))); ax.set_xticklabels([str(d) for d in W]); ax.set_ylim(0, 40); ax.set_yticks([0, 10, 20, 30, 40])
    ax.set_title(title, loc="left", fontsize=11, color=INK)
    ax.tick_params(length=0); ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.set_xlabel("width of the zone in which a fish lines up with its neighbours")
axes[0].set_ylabel("schools, of forty")
fig.legend(handles=[Patch(color=BLUE, label="largest group circling (a mill)"), Patch(color=GREY, label="neither"), Patch(color=ORANGE, label="largest group swimming one way")],
           loc="lower left", bbox_to_anchor=(0.065, 0.0), ncol=3, frameon=False, fontsize=9.5)
fig.suptitle("The same forty starts under two ways of combining the pulls", x=0.07, y=0.975, ha="left", fontsize=14, color=INK)
fig.text(0.07, 0.868, "A hundred fish in two dimensions, 450 time units a run. The three labels are my own thresholds on the largest group.\nUnder the paper's rule 12 of 280 schools split; under mine, 211.", fontsize=9.5, color=MUTED, linespacing=1.4)
fig.savefig(sys.argv[3], dpi=130, facecolor="white")
