"""One tiling, and how the frozen corner's depth behaves with size.   usage: python figures.py runs.json order300.png aztec.png"""
import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'referee'))
from ref_Kkraw import K_law            # the exact law of K, supplied by the referee
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = json.load(open(sys.argv[1])); sizes = np.array([100, 200, 400, 800, 1600]); get = lambda n, key: np.array([r[str(n)][key] for r in R])
INK, MUTED, GRID, BLUE, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
fig = plt.figure(figsize=(12.4, 7.4)); a = fig.add_axes([0.03, 0.04, 0.50, 0.84]); b = fig.add_axes([0.62, 0.55, 0.35, 0.30]); c = fig.add_axes([0.62, 0.10, 0.35, 0.30])
a.imshow(plt.imread(sys.argv[2])); a.axis('off'); a.set_title("One tiling of order 300, chosen evenly from all 2^45,150 of them", loc='left', fontsize=10.5, color=INK, pad=6)
from matplotlib.patches import Patch
a.legend(handles=[Patch(color="#2a78d6", label="lying, frozen at the top"), Patch(color="#eb6834", label="standing, frozen at the right"), Patch(color="#1baf7a", label="standing, frozen at the left"), Patch(color="#eda100", label="lying, frozen at the bottom")],
         loc='upper left', bbox_to_anchor=(0.0, 0.0), frameon=False, fontsize=8.5, ncol=4, columnspacing=1.2, handlelength=1.2)
def style(ax, title):
    ax.grid(color=GRID, lw=0.8); ax.set_axisbelow(True); ax.tick_params(length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(title, loc='left', fontsize=10.5, color=INK, pad=8)
m = np.array([get(n, 'K').mean() / n for n in sizes]); se = np.array([get(n, 'K').std(ddof=1) / math.sqrt(len(R)) / n for n in sizes]); lim = (1 - 1 / math.sqrt(2)) / 2
b.errorbar(sizes, m, yerr=2 * se, ls='none', marker='o', ms=5, color=BLUE, elinewidth=1); b.axhline(lim, color=NEUTRAL, lw=1.2, ls=(0, (4, 3))); b.text(1650, lim + 0.0015, "the circle: 0.1464", color=MUTED, fontsize=8.5, ha='right')
xs = np.geomspace(100, 1600, 50); grid = [100, 141, 200, 283, 400, 566, 800, 1131, 1600]; law = {n: K_law(n) for n in grid}
b.plot(grid, [law[n]['mean'] / n for n in grid], color=INK, lw=1.2, label="the exact law"); b.plot([], [], ls='none', marker='o', ms=5, color=BLUE, label="100 growths"); b.legend(loc='upper right', frameon=False, fontsize=9)
b.set_xscale('log'); b.set_xticks(sizes); b.set_xticklabels([f"{n:,}" for n in sizes]); b.minorticks_off(); b.set_xlabel("order n"); b.set_ylabel("depth / n")
style(b, "Depth of a frozen corner along the diagonal, over n")
s = np.array([get(n, 'K').std(ddof=1) for n in sizes]); sl, ic = np.polyfit(np.log(sizes), np.log(s), 1)
c.errorbar(sizes, s, yerr=2 * s / math.sqrt(2 * (len(R) - 1)), ls='none', marker='o', ms=5, color=BLUE, elinewidth=1, label=f"100 growths (fitted power {sl:.2f})")
c.plot(grid, [law[n]['sd'] for n in grid], color=INK, lw=1.2, label="the exact law")
c.plot(xs, law[1600]['sd'] * (xs / 1600) ** (1 / 3), color=NEUTRAL, lw=1.2, ls=(0, (4, 3)), label="n to the power 1/3")
c.set_xscale('log'); c.set_yscale('log'); c.set_xticks(sizes); c.set_xticklabels([f"{n:,}" for n in sizes]); c.minorticks_off(); c.set_ylim(0.9, 4.2); c.set_yticks([1, 2, 3, 4]); c.set_yticklabels(['1', '2', '3', '4'])
c.set_xlabel("order n"); c.set_ylabel("blocks"); c.legend(loc='upper left', frameon=False, fontsize=9); style(c, "How much that depth varies from tiling to tiling")
fig.suptitle("Random domino tilings of the Aztec diamond: the arctic circle", x=0.03, y=0.965, ha='left', fontsize=15, color=INK)
fig.text(0.62, 0.975, f"{len(R)} growths to order 1,600 by domino shuffling. Bars: two standard errors.\nBlack: the exact law of the depth, which the referee supplied.", fontsize=9, color=MUTED, va='top')
fig.savefig(sys.argv[3], dpi=130, facecolor='white')
