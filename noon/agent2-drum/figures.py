"""The figure.   usage: python figures.py results.json after.json layers-2.json drum.png"""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = json.load(open(sys.argv[1])); A = json.load(open(sys.argv[2])); L2 = json.load(open(sys.argv[3]))
INK, MUTED, GRID, BLUE, ORANGE, AQUA, YELLOW, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
fig = plt.figure(figsize=(12.4, 8.4))
# (a) ladders
ax = fig.add_axes([0.065, 0.50, 0.90, 0.33]); rows = [("plain skin", np.array(A['unloaded_w']) / A['unloaded_w'][0], NEUTRAL), ("one even disc at the centre", np.array(R['ratios']), ORANGE), ("two discs, about twice the weight", np.array(L2['ratios'][:9]), BLUE)]
for h in range(1, 6): ax.axvline(h, color=GRID, lw=6, zorder=0); ax.text(h, 3.62, f"{h}", ha='center', fontsize=10, color=MUTED)
for j, (name, r, col) in enumerate(rows):
    y = 2.6 - j * 1.1
    for x in r: ax.plot([x, x], [y - 0.36, y + 0.36], color=col if col != NEUTRAL else INK, lw=2.2)
    ax.text(-0.75, y, name, ha='left', va='center', fontsize=9.5, color=INK)
    if j: ax.text(5.62, y, f"largest miss\n{100 * max(abs(r[i] / t - 1) for i, t in enumerate([1, 2, 3, 3, 4, 4, 5, 5, 5])):.2f}% ({1200 * np.log2(1 + max(abs(r[i] / t - 1) for i, t in enumerate([1, 2, 3, 3, 4, 4, 5, 5, 5]))):.0f} cents)", ha='left', va='center', fontsize=8.5, color=MUTED)
ax.set_xlim(-0.8, 6.25); ax.set_ylim(-0.35, 3.9); ax.set_yticks([]); ax.set_xticks([]); ax.text(-0.75, 3.62, "harmonic:", fontsize=9.5, color=MUTED, va='bottom')
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_title("The first nine modes, as multiples of the lowest", loc='left', fontsize=10.5, color=INK, pad=8)
# (b) map
ax = fig.add_axes([0.065, 0.085, 0.40, 0.31]); k = np.array(A['map']['k']); s = np.array(A['map']['s']); Z = 100 * np.array(A['map']['miss'])
cs = ax.contourf(k, s, Z, levels=[0, 4, 6, 8, 12, 16, 24, 40], colors=["#1c5cab", "#3987e6", "#7fb2ef", "#b9d3f6", "#dde9fa", "#f0eeea", "#f7f5f1"]); ax.contour(k, s, Z, levels=[4, 6, 8, 12, 16, 24], colors='white', linewidths=0.6)
ax.plot([R['best_k']], [R['best_s']], marker='o', ms=6, color=ORANGE, markeredgecolor='white'); ax.annotate(f"best: {R['best_s']:.1f} times the skin's weight\nover {R['best_k']:.2f} of the radius: 3.2%", (R['best_k'], R['best_s']), xytext=(0.47, 22.5), fontsize=8.5, color=INK, arrowprops=dict(arrowstyle='-', color=INK, lw=0.7))
ax.set_xlabel("radius of the disc, as a share of the skin's"); ax.set_ylabel("the disc's weight per area, in skins"); ax.tick_params(length=0)
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_title("One even disc: the largest miss, by its size and weight", loc='left', fontsize=10.5, color=INK, pad=8)
cb = fig.colorbar(cs, cax=fig.add_axes([0.475, 0.085, 0.012, 0.31])); cb.set_label("largest miss, %", color=MUTED, fontsize=8.5); cb.outline.set_visible(False); cb.ax.tick_params(length=0, labelsize=8)
# (c) cents
ax = fig.add_axes([0.60, 0.085, 0.365, 0.31]); labels = ["(1,1)", "(2,1)", "(0,2)", "(3,1)", "(1,2)", "(4,1)", "(2,2)", "(0,3)"]; T = [2, 3, 3, 4, 4, 5, 5, 5]; x = np.arange(8)
for off, (name, r, col) in zip((-0.19, 0.19), rows[1:]): ax.bar(x + off, [1200 * np.log2(r[i + 1] / t) for i, t in enumerate(T)], width=0.34, color=col, label=name)
ax.axhline(0, color=INK, lw=0.8); ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8.5); ax.set_ylabel("cents from its harmonic (100 = a semitone)"); ax.set_ylim(-65, 65); ax.tick_params(length=0); ax.grid(axis='y', color=GRID, lw=0.8); ax.set_axisbelow(True)
for sp in ax.spines.values(): sp.set_visible(False)
ax.legend(loc='upper left', frameon=False, fontsize=8.5, ncol=1); ax.set_title("How far each mode sits from its harmonic", loc='left', fontsize=10.5, color=INK, pad=8)
fig.suptitle("A drumskin with a loaded centre: nine modes drawn towards five harmonics", x=0.065, y=0.975, ha='left', fontsize=15, color=INK)
fig.text(0.065, 0.93, "A round skin held at its rim, with heavier skin at the centre. Each tick is one mode of vibration; a mode (m, n) has m nodal diameters. The one disc is the one that brings the\nnine modes closest to 1, 2, 3, 3, 4, 4, 5, 5, 5 times the lowest (by the largest miss). The two discs are a pair of about twice its weight; heavier pairs come closer still.", fontsize=9.5, color=MUTED, va='top', linespacing=1.5)
fig.savefig(sys.argv[4], dpi=130, facecolor='white')
