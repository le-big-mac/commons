"""Four small panels.   usage: python -I figures.py results.json out.png"""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = json.load(open(sys.argv[1]))
INK, MUTED, GRID, BLUE, ORANGE, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
fig, axes = plt.subplots(2, 2, figsize=(12.4, 9.4), gridspec_kw={"hspace": 0.42, "wspace": 0.2})
(a, b), (c, d) = axes
# a: period against size
P = np.array([p for p, r in R['pr']]); S = np.array([r for p, r in R['pr']])
a.scatter(P, S, s=5, color=BLUE, alpha=0.35, lw=0, zorder=2)
a.set_xscale('log'), a.set_yscale('log'), a.set_xlim(0.3, 1000), a.set_ylim(0.4, 30)
a.set_xticks([1, 10, 100, 1000]), a.set_xticklabels(['1', '10', '100', '1,000']), a.set_yticks([1, 2, 4, 8, 16]), a.set_yticklabels(['1', '2', '4', '8', '16'])
a.set_xlabel("orbital period (days)"), a.set_ylabel("size (Earth radii)")
a.set_title("Transit planets by period and size", loc='left', fontsize=10.5, color=INK)
a.annotate("hot Jupiters", (2.2, 16), xytext=(14, 24), fontsize=9.5, color=INK, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
a.annotate("few hot\nNeptunes", (1.3, 5), xytext=(0.36, 6.3), fontsize=9.5, color=INK)
# b: sizes
e = np.array(R['hist']['edges']); n = np.array(R['hist']['counts'])
mid = np.sqrt(e[:-1] * e[1:])
valley = (mid > 1.78) & (mid < 2.0)
b.bar(range(len(n)), n, color=[ORANGE if v else BLUE for v in valley], width=0.86, edgecolor='white', lw=1, zorder=2)
b.set_xticks(np.arange(len(e)) - 0.5), b.set_xticklabels([f"{v:.1f}" if i % 2 == 0 else "" for i, v in enumerate(e)])
b.set_xlabel("size (Earth radii), periods under 100 days"), b.set_ylabel("planets")
b.set_title("Sizes: at most a shallow dip just below 2 Earth radii (orange)", loc='left', fontsize=10.5, color=INK)
# c: period ratios
r = np.array(R['ratio'])
bins = np.arange(1.2, 2.6001, 0.02)
h, _ = np.histogram(r, bins)
c.bar(bins[:-1] + 0.01, h, width=0.018, color=BLUE, zorder=2)
for xx, lab in ((1.5, "3 : 2"), (2.0, "2 : 1"), (4 / 3, "4 : 3"), (5 / 3, "5 : 3")):
    c.axvline(xx, color=INK, lw=0.9, ls=(0, (4, 3)), zorder=3)
    c.text(xx, h.max() * 1.06, lab, ha='center', va='bottom', fontsize=9, color=INK, bbox=dict(facecolor='white', edgecolor='none', pad=1.5), zorder=5)
c.set_ylim(0, h.max() * 1.18), c.set_xlim(1.2, 2.6)
c.set_xlabel("period of the outer neighbour over that of the inner"), c.set_ylabel("pairs")
c.set_title("Neighbours' period ratios: a spike just outside 3 : 2, a hole just inside 2 : 1", loc='left', fontsize=10.5, color=INK)
# d: neighbours' sizes
X = np.array([p[0] for p in R['pairs']]); Y = np.array([p[1] for p in R['pairs']])
d.plot([0.4, 20], [0.4, 20], color=INK, lw=0.9, ls=(0, (4, 3)), zorder=1)
d.scatter(X, Y, s=9, color=BLUE, alpha=0.4, lw=0, zorder=2)
d.set_xscale('log'), d.set_yscale('log'), d.set_xlim(0.4, 20), d.set_ylim(0.4, 20)
d.set_xticks([0.5, 1, 2, 4, 8, 16]), d.set_xticklabels(['0.5', '1', '2', '4', '8', '16']), d.set_yticks([0.5, 1, 2, 4, 8, 16]), d.set_yticklabels(['0.5', '1', '2', '4', '8', '16'])
d.set_xlabel("size of the inner neighbour (Earth radii)"), d.set_ylabel("size of the outer neighbour")
d.set_title("Neighbours' sizes (above the dashed line the outer one is larger)", loc='left', fontsize=10.5, color=INK)
for ax in (a, b, c, d):
    ax.grid(color=GRID, lw=0.8), ax.set_axisbelow(True), ax.tick_params(length=0, which='both')
    for sp in ax.spines.values():
        sp.set_visible(False)
fig.suptitle(sys.argv[3] if len(sys.argv) > 3 else f"{R['n']:,} planets found by transit, as the public catalogue lists them", x=0.06, y=0.985, ha='left', fontsize=14, color=INK)
fig.subplots_adjust(left=0.065, right=0.985, top=0.915, bottom=0.07)
fig.savefig(sys.argv[2], dpi=130, facecolor='white')
