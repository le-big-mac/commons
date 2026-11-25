"""One figure: births per day by month for athletes (bars) and politicians of the same country (line).   usage: python -I figures.py results.json out.png"""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
R = json.load(open(sys.argv[1]))
INK, MUTED, GRID, BLUE, ORANGE, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
L = "JFMAMJJASOND"
P = [  # title, athletes' profile, first month of the year group (1-12), politicians' profile, note on the dividing date
    ("Spain, footballers", R['profile']['football-spain'], 1, R['control'].get('politicians-spain'), "dividing date now: 1 January"),
    ("Brazil, footballers", R['profile']['football-brazil'], 1, R['control'].get('politicians-brazil'), "dividing date now: 1 January"),
    ("Canada, ice hockey players", R['profile']['hockey-canada'], 1, R['control'].get('politicians-canada'), "dividing date now: 1 January"),
    ("United Kingdom, footballers", R['profile']['football-uk'], 9, R['control'].get('politicians-uk'), "dividing date in England and Wales: 1 September"),
    ("Japan, footballers", R['profile']['football-japan'], 4, R['control'].get('politicians-japan'), "dividing date: 2 April"),
    ("United States, baseball players", R['profile']['baseball-usa'], 8, R['control'].get('house-usa'), "dividing date assumed: 1 August"),
    ("Germany, men footballers born 1940 to 1979", R['germany_men']['1940-1979'], 8, R['control'].get('politicians-germany'), "dividing date then: 1 August"),
    ("Germany, men footballers born 1985 or later", R['germany_men']['1985-2005'], 1, R['control'].get('politicians-germany'), "dividing date now: 1 January"),
]
CUT = {1: "1 January", 4: "1 April", 8: "1 August", 9: "1 September"}
fig, axes = plt.subplots(3, 3, figsize=(12.6, 9.6), sharey=True)
axes = axes.ravel()
for ax, (title, prof, cut, pol, note) in zip(axes, P):
    hot = [(cut - 1 + k) % 12 for k in range(3)]
    cols = [ORANGE if i in hot else NEUTRAL for i in range(12)]
    ax.bar(range(12), [100 * x - 100 for x in prof], bottom=100, color=cols, width=0.78, zorder=2, edgecolor='white', linewidth=0.8)      # bars measure the distance from the average
    if pol:
        ax.plot(range(12), [100 * x for x in pol], color=INK, lw=1.6, marker='o', ms=3.2, zorder=4)
    ax.axhline(100, color=INK, lw=0.9, zorder=3)
    ax.set_title(title, loc='left', fontsize=10.5, color=INK, pad=19)
    ax.text(0, 1.035, note, transform=ax.transAxes, fontsize=9, color=MUTED, va='bottom')
    ax.set_xticks(range(12)), ax.set_xticklabels(list(L), fontsize=9)
    ax.set_ylim(52, 158), ax.set_yticks([60, 80, 100, 120, 140])
    ax.grid(axis='y', color=GRID, lw=0.8), ax.set_axisbelow(True), ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
axes[0].set_ylabel("births per day (average = 100)"), axes[3].set_ylabel("births per day (average = 100)"), axes[6].set_ylabel("births per day (average = 100)")
axes[8].axis('off')
axes[8].legend(handles=[Patch(color=ORANGE, label="athletes born in the first three\nmonths of the year group"), Patch(color=NEUTRAL, label="athletes born in the other months"),
                        Line2D([], [], color=INK, lw=1.6, marker='o', ms=3.2, label="politicians of the same country\n(not picked through youth sport)"),
                        Line2D([], [], color=INK, lw=0.9, label="100: births spread evenly over the year")],
               loc='center left', bbox_to_anchor=(0.0, 0.55), frameon=False, fontsize=10, labelspacing=1.0)
fig.suptitle("Athletes' birthdays pile up just after the date that divides their youth year groups, wherever that date falls", x=0.045, y=0.985, ha='left', fontsize=13.5, color=INK)
fig.subplots_adjust(left=0.065, right=0.985, top=0.895, bottom=0.045, hspace=0.42, wspace=0.08)
fig.savefig(sys.argv[2], dpi=130, facecolor='white')
