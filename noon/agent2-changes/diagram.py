"""The 120 changes written out, with the paths of two bells drawn through them.   usage: python diagram.py changes.json out.png"""
import sys, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
D = json.load(open(sys.argv[1])); rows = D['rows']; calls = D['calls']
INK, MUTED, GRID, BLUE, ORANGE = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK})
fig, axes = plt.subplots(1, 3, figsize=(9.6, 12.2))
for c, ax in enumerate(axes):
    part = rows[c * 40:(c + 1) * 40] + [rows[(c + 1) * 40] if (c + 1) * 40 < 120 else [1, 2, 3, 4, 5]]      # the row the column hands on to
    for bell, col, lw in ((1, ORANGE, 2.2), (2, BLUE, 2.2)):
        ax.plot([r.index(bell) + 1 for r in part], [-k for k in range(len(part))], color=col, lw=lw, zorder=1, solid_capstyle='round', solid_joinstyle='round')
    for k, r in enumerate(part):
        ghost = k == 40
        for x, b in enumerate(r, 1):
            ax.text(x, -k, str(b), ha='center', va='center', fontsize=10.5, family='DejaVu Sans Mono', color=MUTED if ghost else INK, fontweight='bold' if b in (1, 2) and not ghost else 'normal',
                    bbox=dict(facecolor='white', edgecolor='none', pad=1.2), zorder=3)
    for lead in range(4):
        y = -(lead * 10 + 9.5)
        ax.plot([0.6, 5.4], [y, y], color=GRID, lw=1, zorder=0)
        if calls[c * 4 + lead] == 'B':
            ax.text(5.75, y, "bob", fontsize=9.5, color=INK, va='center', ha='left')
    ax.set_xlim(0.2, 6.6), ax.set_ylim(-41, 1.2), ax.axis('off')
    ax.set_title(f"rows {c * 40 + 1} to {(c + 1) * 40}", fontsize=10, color=MUTED, loc='left', x=0.08, pad=2)
fig.legend(handles=[Line2D([], [], color=ORANGE, lw=2.2, label="the treble (bell 1, the highest): it hunts from the front to the back and home again, the same every time"),
                    Line2D([], [], color=BLUE, lw=2.2, label="bell 2: one of the four that do the work, dodging and making places at each lead end")],
           loc='upper left', bbox_to_anchor=(0.06, 0.962), frameon=False, fontsize=9.5)
fig.suptitle("All 120 orders of five bells, each rung once: Plain Bob Doubles", x=0.06, y=0.985, ha='left', fontsize=14, color=INK)
fig.text(0.06, 0.03, "Read down each column. Each row is one order of the bells 1 to 5; from one row to the next a bell stays or swaps with a neighbour.\n"
         "A lead is ten rows (grey rules). Three plain leads and a bob, three times over, and the bells come back to 1 2 3 4 5.\n"
         "A sixth bell, the tenor, strikes last in every row.", fontsize=9, color=MUTED, va='bottom')
fig.subplots_adjust(left=0.04, right=0.98, top=0.89, bottom=0.085, wspace=0.05)
fig.savefig(sys.argv[2], dpi=130, facecolor='white')
