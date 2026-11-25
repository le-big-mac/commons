"""The figure.   usage: python -I figures.py results.json snap hawk.png"""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
R = json.load(open(sys.argv[1]))['curves']; snapdir = sys.argv[2]
INK, MUTED, GRID, BLUE, ORANGE, AQUA, YELLOW, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
fig = plt.figure(figsize=(12.4, 9.4))
ax = fig.add_axes([0.07, 0.46, 0.88, 0.37]); r = np.array([p[0] for p in R['lattice4']])
ax.plot([0, 1], [1, 0], color=NEUTRAL, lw=1.6, ls=(0, (5, 3)))
ax.plot(r, [p[1] for p in R['lattice8']], color=AQUA, lw=2); ax.plot(r, [p[1] for p in R['sync4']], color=ORANGE, lw=1.4); ax.plot(r, [p[1] for p in R['lattice4']], color=BLUE, lw=2.4)
ax.text(0.84, 0.19, "well mixed: 1 − r", color=MUTED, fontsize=9.5, rotation=-33); ax.text(0.235, 0.80, "4 neighbours", color=BLUE, fontsize=9.5); ax.text(0.185, 0.66, "8 neighbours", color=AQUA, fontsize=9.5, ha='right')
ax.annotate("4 neighbours, all sites\nupdated at once", (0.34, 0.567), xytext=(0.40, 0.72), color=ORANGE, fontsize=9, arrowprops=dict(arrowstyle='-', color=ORANGE, lw=0.8))
ax.annotate("falls between\n0.210 and 0.215", (0.2125, 0.93), xytext=(0.30, 1.03), color=BLUE, fontsize=8.5, arrowprops=dict(arrowstyle='-', color=BLUE, lw=0.7)); ax.annotate("between 0.112\nand 0.115", (0.1135, 0.93), xytext=(0.02, 0.80), color=AQUA, fontsize=8.5, arrowprops=dict(arrowstyle='-', color=AQUA, lw=0.7))
ax.annotate("none left after 15,000\ngenerations from r = 0.68\n(a few at 0.74)", (0.68, 0.0), xytext=(0.50, 0.07), color=BLUE, fontsize=9, ha='right', arrowprops=dict(arrowstyle='-', color=BLUE, lw=0.8))
ax.annotate("from r = 0.78", (0.78, 0.0), xytext=(0.80, 0.09), color=AQUA, fontsize=9, arrowprops=dict(arrowstyle='-', color=AQUA, lw=0.8))
ax.set_xlim(0, 1); ax.set_ylim(-0.02, 1.14); ax.set_xlabel("r: what sharing costs, as a share of what it brings (cost / (2 × benefit − cost))"); ax.set_ylabel("share of doves, generations 10,001 to 15,000")
ax.grid(color=GRID, lw=0.8); ax.set_axisbelow(True); ax.tick_params(length=0)
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_title("Share of doves on a lattice of 200 × 200, against the well-mixed crowd", loc='left', fontsize=10.5, color=INK, pad=16)
cm = ListedColormap(["#2b2622", "#dfe9f5"])
for k, (rr, note) in enumerate((("0.15", "r = 0.15: a few hawks, alone or in pairs"), ("0.30", "r = 0.30: 59% doves (well mixed: 70%)"), ("0.50", "r = 0.50: 34% doves (well mixed: 50%)"), ("0.64", "r = 0.64: 10% doves (well mixed: 36%)"))):
    a = np.fromfile(f"{snapdir}/s-{rr}.bin", dtype=np.uint8)[-40000:].reshape(200, 200)[:100, :100]
    axs = fig.add_axes([0.07 + k * 0.225, 0.065, 0.205, 0.205 * 12.4 / 9.4]); axs.imshow(a, cmap=cm, vmin=0, vmax=1, interpolation='nearest'); axs.set_xticks([]); axs.set_yticks([])
    for sp in axs.spines.values(): sp.set_color(GRID)
    axs.set_title(note, loc='left', fontsize=9, color=INK, pad=5)
fig.text(0.07, 0.375, "A quarter of each lattice after 15,000 generations. Light: doves. Dark: hawks.", fontsize=9.5, color=MUTED)
fig.suptitle("Hawks and doves with neighbours: fewer doves than in a well-mixed crowd, except at small r", x=0.07, y=0.975, ha='left', fontsize=15, color=INK)
fig.text(0.07, 0.935, "Each site plays its nearest neighbours and now and then copies a neighbour who is doing better. For small r the lattice is not yet at rest in this window:\nthe hawks go on thinning out.", fontsize=9.5, color=MUTED, va='top', linespacing=1.5)
fig.savefig(sys.argv[3], dpi=130, facecolor='white')
