"""One figure: the elections where the first-choice leader was not the Condorcet winner.   usage: python -I figure.py results.json out.png"""
import sys, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
rows = json.load(open(sys.argv[1]))['rows']
INK, MUTED, GRID, BLUE, ORANGE = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
dis = [r for r in rows if r['plurality'] != r['condorcet']]
dis.sort(key=lambda r: r['first_share_plurality'] - r['first_share_condorcet'])
fig, ax = plt.subplots(figsize=(10.4, 7.4))
for y, r in enumerate(dis):
    a, b = 100 * r['first_share_condorcet'], 100 * r['first_share_plurality']
    ax.plot([a, b], [y, y], color=GRID, lw=3, zorder=1, solid_capstyle='round')
    ax.scatter([b], [y], s=62, color=ORANGE, edgecolor='white', lw=1.1, zorder=3)
    ax.scatter([a], [y], s=62, color=BLUE, edgecolor='white', lw=1.1, zorder=4, marker='o' if r['runoff'] == r['condorcet'] else 'X')
    name = r['title'].replace('San Francisco Board of Supervisors - ', 'San Francisco, ').replace(' Mayoral Election', ' mayor').replace('City Council - ', 'council, ')
    ax.text(8.5, y, name, fontsize=9, color=INK, va='center', ha='right')
    if r['runoff'] != r['condorcet']:
        ax.text(a - 0.8, y, "not elected", fontsize=8.5, color=INK, va='center', ha='right')
ax.set_yticks([]), ax.set_xlim(-9, 47), ax.set_ylim(-0.8, len(dis) - 0.2)
ax.set_xticks(range(10, 50, 10)), ax.set_xticklabels([f"{x}%" for x in range(10, 50, 10)])
ax.set_xlabel("share of first choices")
ax.grid(axis='x', color=GRID, lw=0.8), ax.set_axisbelow(True), ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.legend(handles=[Line2D([], [], marker='o', ls='', ms=8, color=ORANGE, mec='white', label="the candidate with most first choices"),
                   Line2D([], [], marker='o', ls='', ms=8, color=BLUE, mec='white', label="the candidate who beats every other head to head; elected by instant runoff"),
                   Line2D([], [], marker='X', ls='', ms=8, color=BLUE, mec='white', label="the same, not elected")],
          loc='upper left', bbox_to_anchor=(0.0, 1.11), frameon=False, fontsize=9, ncols=1)
fig.suptitle("Nineteen elections in 312 where the first-choice leader would have lost head to head", x=0.03, y=0.985, ha='left', fontsize=13.5, color=INK)
fig.subplots_adjust(left=0.03, right=0.98, top=0.82, bottom=0.08)
fig.savefig(sys.argv[2], dpi=130, facecolor='white')
