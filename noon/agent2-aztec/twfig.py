"""The exact law of the frozen depth against the Tracy-Widom density.   usage: python twfig.py tw.json corners-1.json corners-2.json tw.png"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import tw as TW
J = json.load(open(sys.argv[1])); R = [r for f in sys.argv[2:4] for r in json.load(open(f))]
INK, MUTED, GRID, BLUE, ORANGE, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
fig, (a, b) = plt.subplots(1, 2, figsize=(12.4, 4.8), gridspec_kw=dict(width_ratios=[1.6, 1])); fig.subplots_adjust(left=0.07, right=0.97, top=0.80, bottom=0.14, wspace=0.22)
def style(ax, title):
    ax.grid(color=GRID, lw=0.8); ax.set_axisbelow(True); ax.tick_params(length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(title, loc='left', fontsize=10.5, color=INK, pad=8)
s = np.linspace(-5.5, 2.5, 801); F = np.array([TW.F(x) for x in s]); a.plot(s, np.gradient(F, s), color=INK, lw=1.6, label="Tracy–Widom density")
A, B = (1 - 1 / math.sqrt(2)) / 2, 2 ** (-11 / 6)
k16 = np.array([r['1600'] for r in R]).ravel(); sc = B * 1600 ** (1 / 3); vals, cnt = np.unique(k16, return_counts=True)
a.bar((A * 1600 - vals - 0.5) / sc, cnt / len(k16) * sc, width=1 / sc * 0.9, color=NEUTRAL, alpha=0.55, label=f"{len(k16):,} sampled depths at order 1,600", zorder=1)
for n, col, mk in ((100, ORANGE, 's'), (1600, BLUE, 'o')):
    pmf = np.array(J['sizes'][str(n)]['pmf']); k = np.arange(len(pmf)); sc = B * n ** (1 / 3); keep = pmf > 1e-6
    a.plot((A * n - k[keep] - 0.5) / sc, pmf[keep] * sc, ls='none', marker=mk, ms=5.5, color=col, markeredgecolor='white', markeredgewidth=0.8, label=f"the exact law at order {n:,}", zorder=3)
a.set_xlim(-5.5, 2.5); a.set_xlabel("(0.1464 n − depth − ½) / (2^(−11/6) n^(1/3))"); a.set_ylabel("density"); a.legend(loc='upper right', frameon=False, fontsize=8.5)
style(a, "The frozen depth, rescaled, against the Tracy–Widom law")
ns = [100, 400, 1600, 6400]; D = [J['sizes'][str(n)]['D'] for n in ns]
b.plot(ns, D, color=BLUE, lw=1.4, marker='o', ms=5); b.set_xscale('log'); b.set_yscale('log'); b.set_xticks(ns); b.set_xticklabels([f"{n:,}" for n in ns]); b.minorticks_off()
b.set_yticks([1e-4, 3e-4, 1e-3]); b.set_yticklabels(['0.0001', '0.0003', '0.001']); b.set_xlabel("order n"); b.set_ylabel("largest difference in probability")
style(b, "How far the exact law is from that form")
fig.suptitle("The frozen depth follows the Tracy–Widom form to within 0.0014 in probability at order 100", x=0.07, y=0.965, ha='left', fontsize=14, color=INK)
fig.savefig(sys.argv[4], dpi=130, facecolor='white')
