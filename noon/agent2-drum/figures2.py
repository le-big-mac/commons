"""The second figure: a load of any radial shape, from the searches made after the referee (rings2.py, 80 rings, exact matching).
usage: python figures2.py onedisc.json drum2.png     (reads rings2-free-*.json and rings2-piled-*.json)"""
import sys, json, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ONE = sorted(json.load(open(sys.argv[1])), key=lambda r: r['weight']); R = {}
for f in glob.glob("rings2-*-*.json"):
    d = json.load(open(f)); R[(d['kind'], d['weight'])] = d['rings']
W = [r['weight'] for r in ONE]; N = 80; EDGE = np.arange(N + 1) / N
INK, MUTED, GRID, BLUE, ORANGE, AQUA, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#1baf7a", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
fig = plt.figure(figsize=(12.4, 7.4))
def steps(ax, a, col, label, lw=2.0, z=3): ax.step(EDGE, np.concatenate([a, [a[-1]]]), where='post', color=col, lw=lw, label=label, zorder=z)
def tidy(ax):
    ax.tick_params(length=0); ax.grid(axis='y', color=GRID, lw=0.8); ax.set_axisbelow(True)
    for sp in ax.spines.values(): sp.set_visible(False)
# (a) loads at the one disc's weight
ax = fig.add_axes([0.065, 0.525, 0.40, 0.275]); o = next(r for r in ONE if abs(r['weight'] - 1.43) < 1e-9); disc = np.where(EDGE[:-1] < o['k'] - 1e-9, o['s'] - 1, 0.0); f = R[("free", 1.43)][str(N)]
steps(ax, disc, ORANGE, f"one even disc: largest miss {100 * o['miss']:.1f}%"); steps(ax, np.array(f['a']), AQUA, f"any radial load: {100 * f['exact']:.2f}%")
ax.set_xlim(0, 0.6); ax.set_ylim(0, None); ax.set_ylabel("added weight per area, in skins"); ax.set_xlabel("distance from the centre, as a share of the skin's radius"); tidy(ax); ax.legend(loc='upper right', frameon=False, fontsize=8.5)
ax.set_title("With 1.43 skins of added mass, the one disc's own", loc='left', fontsize=10.5, color=INK, pad=8)
# (b) loads at 12 skins
ax = fig.add_axes([0.065, 0.085, 0.40, 0.275]); p = R[("piled", 12.0)][str(N)]; f = R[("free", 12.0)][str(N)]
steps(ax, np.array(p['a']), BLUE, f"discs piled on discs: {100 * p['exact']:.2f}%"); steps(ax, np.array(f['a']), AQUA, f"any radial load: {100 * f['exact']:.2f}%")
ax.set_xlim(0, 0.6); ax.set_ylim(0, None); ax.set_ylabel("added weight per area, in skins"); ax.set_xlabel("distance from the centre, as a share of the skin's radius"); tidy(ax); ax.legend(loc='upper right', frameon=False, fontsize=8.5)
ax.set_title("With 12 skins of added mass, the most I allowed", loc='left', fontsize=10.5, color=INK, pad=8)
# (c) least largest miss against weight
ax = fig.add_axes([0.555, 0.085, 0.30, 0.715])
for y, col, name in (([100 * r['miss'] for r in ONE], ORANGE, "one even disc"), ([100 * R[("piled", m)][str(N)]['exact'] for m in W], BLUE, "discs piled on discs"), ([100 * R[("free", m)][str(N)]['exact'] for m in W], AQUA, "any radial load")):
    ax.plot(W, y, color=col, lw=2, marker='o', ms=4.5, markeredgecolor='white', markeredgewidth=0.8, label=name, zorder=3)
    ax.text(12.9, y[-1], name + f"\n{y[-1]:.2f}% ({1200 * np.log2(1 + y[-1] / 100):.0f} cents)", va='center', ha='left', fontsize=8.5, color=INK, linespacing=1.35)
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlim(0.95, 12.6); ax.set_ylim(0.4, 12); ax.set_xticks([1, 1.43, 2, 2.79, 4, 6, 9.6, 12]); ax.set_xticklabels(["1", "1.43", "2", "2.79", "4", "6", "9.6", "12"]); ax.set_yticks([0.5, 1, 2, 3, 5, 10]); ax.set_yticklabels(["0.5%", "1%", "2%", "3%", "5%", "10%"]); ax.minorticks_off()
ax.set_xlabel("added mass allowed, in skins (the bare skin's whole weight = 1)"); ax.set_ylabel("least largest miss found"); tidy(ax); ax.legend(loc='lower left', frameon=False, fontsize=8.5)
ax.set_title("The least largest miss found, by the weight allowed", loc='left', fontsize=10.5, color=INK, pad=8)
fig.suptitle("A drumskin loaded in rings: how close nine modes were brought to five harmonics", x=0.065, y=0.975, ha='left', fontsize=15, color=INK)
fig.text(0.065, 0.925, "The load is free in each of 80 rings, and searches look for the load whose worst mode is nearest its harmonic (1, 2, 3, 3, 4, 4, 5, 5, 5 times the lowest).\nPiled loads never grow heavier outward. These are the least found, not the least there is: narrower rings come a little closer, and the heavy ring narrows with them.", fontsize=9.5, color=MUTED, va='top', linespacing=1.5)
fig.savefig(sys.argv[2], dpi=130, facecolor='white')
