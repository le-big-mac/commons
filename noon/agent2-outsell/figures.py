"""The figure.   usage: python figures.py after-c.json after-3.json after-45678.json outsell.png"""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
C = json.load(open(sys.argv[1]))['curves']; B = json.load(open(sys.argv[2]))['big']; A = json.load(open(sys.argv[3]))
INK, MUTED, GRID, BLUE, ORANGE, AQUA, YELLOW = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
COL = {"0.0": BLUE, "0.5": AQUA, "1.0": ORANGE, "1.5": YELLOW}; NAME = {"0.0": "no imitation", "0.5": "weak imitation (g = 0.5)", "1.0": "in proportion to sales (g = 1)", "1.5": "more than in proportion (g = 1.5)"}
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
def tidy(ax, axis='y'):
    ax.tick_params(length=0); ax.grid(axis=axis, color=GRID, lw=0.8); ax.set_axisbelow(True)
    for sp in ax.spines.values(): sp.set_visible(False)
fig = plt.figure(figsize=(12.4, 8.2))
# (a) P against sales
ax = fig.add_axes([0.065, 0.47, 0.62, 0.37])
for g in ("0.0", "0.5", "1.0", "1.5"):
    x = [int(n) for n in C[g]]; y = [C[g][str(n)] for n in x]
    if g == "1.0": x = x + [int(n) for n in B if int(n) > 100000]; y = y + [B[str(n)] for n in x[len(C[g]):]]
    ax.plot(x, y, color=COL[g], lw=2, marker='o', ms=4, markeredgecolor='white', markeredgewidth=0.7, label=NAME[g], zorder=3)
ax.text(2.2e5, 0.985, "no imitation, and weak:\nahead every time by here", fontsize=8.5, va='top', color=INK); ax.text(1.4e12, B[str(10 ** 12)], f"in proportion:\n{B[str(10 ** 12)]:.2f} after a\nmillion million", fontsize=8.5, va='center', color=INK); ax.text(2.2e5, C["1.5"]["100000"] - 0.008, f"more than in proportion: stuck at {C['1.5']['100000']:.2f}", fontsize=8.5, va='top', color=INK)
ax.set_xscale('log'); ax.set_xlim(8, 1.3e12); ax.set_ylim(0.5, 1.01); ax.set_xticks([10, 1e3, 1e6, 1e9, 1e12]); ax.set_xticklabels(["10", "a thousand", "a million", "a thousand million", "a million million"]); ax.set_yticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0]); ax.minorticks_off(); tidy(ax)
ax.set_xlabel("sales so far, of both products together"); ax.set_ylabel("chance that the better product is ahead"); ax.legend(loc='lower right', bbox_to_anchor=(0.995, 0.17), frameon=False, fontsize=8.5)
ax.set_title("A product buyers prefer by 11 to 10: how often it is the one ahead", loc='left', fontsize=10.5, color=INK, pad=8)
# (b) the edge needed
ax = fig.add_axes([0.065, 0.075, 0.36, 0.29]); G = ["0", "0.25", "0.5", "0.75", "1", "1.25", "1.5", "2"]
for N, col in (("100", "#b9b1a5"), ("1000", "#6f675e"), ("10000", "#2b2622")):
    y = [A['edge'][N][g] for g in G]; ax.plot([float(g) for g in G], y, color=col, lw=2, marker='o', ms=4, markeredgecolor='white', markeredgewidth=0.7, label=f"after {int(N):,} sales", zorder=3)
ax.set_yscale('log'); ax.set_yticks([1.0, 1.1, 1.25, 1.5, 2, 3]); ax.set_yticklabels(["even", "11 to 10", "5 to 4", "3 to 2", "2 to 1", "3 to 1"]); ax.minorticks_off(); ax.set_ylim(0.97, 3.3); ax.set_xticks([0, 0.5, 1, 1.5, 2]); tidy(ax)
ax.set_xlabel("strength of imitation, g (0: none; 1: in proportion to sales)"); ax.set_ylabel("buyers' preference needed"); ax.legend(loc='upper left', frameon=False, fontsize=8.5)
ax.set_title("The edge it takes to be ahead nine times in ten", loc='left', fontsize=10.5, color=INK, pad=8)
# (c) shares
x = (np.arange(50) + 0.5) / 50
for i, g in enumerate(("0.0", "0.5", "1.0", "1.5")):
    ax = fig.add_axes([0.52, 0.075 + (3 - i) * 0.076, 0.42, 0.042]); p = np.array(A['shares'][g]['p']); h = np.array([p[20 * j + (1 if j else 0):20 * j + 21].sum() for j in range(50)])
    ax.bar(x, h / h.max(), width=0.017, color=COL[g]); ax.set_xlim(0, 1); ax.set_ylim(0, 1.08); ax.set_yticks([]); ax.tick_params(length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.axhline(0, color=GRID, lw=1); ax.text(0.0, 1.12, NAME[g], fontsize=8.5, color=INK, transform=ax.transAxes, va='bottom')
    if i < 3: ax.set_xticks([])
    else: ax.set_xticks([0, 0.25, 0.5, 0.75, 1]); ax.set_xticklabels(["none", "a quarter", "half", "three quarters", "all"]); ax.set_xlabel("the better product's share of the first thousand sales")
    if i == 0: ax.set_title("How a thousand sales are shared (each row drawn to its own height)", loc='left', fontsize=10.5, color=INK, pad=22)
fig.suptitle("How chancy is outselling? Two rival products, one better, and buyers who copy", x=0.065, y=0.975, ha='left', fontsize=15, color=INK)
fig.text(0.065, 0.93, "Each buyer weighs the two products by what earlier buyers bought, raised to a power g, and then prefers the better one by fixed odds. Every number is exact: all the ways\nthe sales can go are added up, with no sampling. Drawn for a = 1 (a product's first sale doubles its weight); a heavier start favours the better product. A model, not a market.", fontsize=9.5, color=MUTED, va='top', linespacing=1.5)
fig.savefig(sys.argv[4], dpi=130, facecolor='white')
