"""The figure.   usage: python -I figures.py all84.json peas.png"""
import sys, json, math
import numpy as np
from scipy.stats import norm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
D = json.load(open(sys.argv[1])); z = np.array(D['z']); F = D['fit']; n = len(z)
INK, MUTED, GRID, BLUE, ORANGE, AQUA, YELLOW, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
fig = plt.figure(figsize=(12.4, 8.2))
# ---- top: every test as a dot
ax = fig.add_axes([0.06, 0.56, 0.90, 0.27]); w = 0.1; order = np.argsort(z); stacks = {}
for v, i in zip(z[order], order):
    b = round(v / w); stacks[b] = stacks.get(b, 0) + 1
    ax.plot(b * w, stacks[b], marker='o', ms=6.5, color=BLUE if i < 35 else AQUA, markeredgecolor='white', markeredgewidth=0.8, ls='none')
xs = np.linspace(-3.2, 3.2, 400); ax.plot(xs, n * w * norm.pdf(xs), color=INK, lw=1.4); ax.fill_between(xs, 0, n * w * norm.pdf(xs), color=NEUTRAL, alpha=0.18, lw=0)
c = F['c']
for s in (-1, 1): ax.axvline(s * c, color=MUTED, lw=1, ls=(0, (4, 3)))
ax.text(c + 0.06, 6.6, f"nothing beyond\n{c:.2f} standard deviations", fontsize=8.5, color=MUTED, va='top')
ax.text(-3.15, 6.6, f"curve: where honest counts would fall\n(about {n * 2 * norm.sf(c):.0f} of 84 beyond the dashed lines)", fontsize=8.5, color=MUTED, va='top')
ax.set_xlim(-3.2, 3.2); ax.set_ylim(0, 7.2); ax.set_yticks([0, 2, 4, 6]); ax.set_xlabel("how far the count is from Mendel's expectation, in standard deviations"); ax.set_ylabel("tests")
for sp in ax.spines.values(): sp.set_visible(False)
ax.tick_params(length=0); ax.grid(axis='y', color=GRID, lw=0.8); ax.set_axisbelow(True)
ax.plot([], [], marker='o', ms=6.5, color=BLUE, ls='none', label="the 35 simple tests (seven crosses, eight tests of breeding true, twenty single plants)")
ax.plot([], [], marker='o', ms=6.5, color=AQUA, ls='none', label="49 tests made by splitting the seven experiments with several classes")
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False, fontsize=8.8)
# ---- bottom: four models
edges = [0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 3.5]; obs = [int(((abs(z) >= a) & (abs(z) < b)).sum()) for a, b in zip(edges, edges[1:])]
pv = lambda x: 2 * norm.sf(x)
def exp_honest(a, b): return pv(a) - pv(b)
def exp_shrunk(a, b): return pv(a / F['s']) - pv(b / F['s'])
def exp_cut(a, b): return (pv(min(a, c)) - pv(min(b, c))) / (1 - pv(c))
def cdfA(x): return x * x if x <= F['a'] else (1 + F['a']) * x - F['a']
def exp_best(a, b): return cdfA(pv(a)) - cdfA(pv(b))
models = (("Honest samples", "every count left as it fell", exp_honest, INK, None), ("Shrunk", f"every deviation reduced to {F['s']:.2f} of itself", exp_shrunk, ORANGE, F['ll_s']),
          ("Cut off", f"nothing reported beyond {c:.2f}", exp_cut, YELLOW, F['ll_c']), ("Better of two", "done again when it looked wrong", exp_best, BLUE, F['ll_a']))
labels = ["0 to\n0.3", "0.3 to\n0.6", "0.6 to\n0.9", "0.9 to\n1.2", "1.2 to\n1.5", "1.5 to\n1.8", "beyond\n1.8"]
for k, (title, sub, f, col, ll) in enumerate(models):
    ax = fig.add_axes([0.06 + k * 0.232, 0.09, 0.205, 0.30]); x = np.arange(len(obs))
    ax.bar(x, obs, width=0.72, color=NEUTRAL); e = [n * f(a, b if b < 3.5 else 99) for a, b in zip(edges, edges[1:])]
    ax.plot(x, e, marker='o', ms=5.5, color=col, lw=1.6, markeredgecolor='white', markeredgewidth=0.8)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=7.4); ax.set_ylim(0, 31); ax.set_yticks([0, 10, 20, 30]); ax.tick_params(length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.grid(axis='y', color=GRID, lw=0.8); ax.set_axisbelow(True); ax.set_title(title, loc='left', fontsize=10.5, color=INK, pad=18); ax.text(0, 1.035, sub, transform=ax.transAxes, fontsize=7.9, color=MUTED)
    if k == 0: ax.set_ylabel("tests of 84")
    if k: ax.set_yticklabels([])
    ax.text(0.98, 0.95, "likelihood: the yardstick" if ll is None else f"{math.exp(ll):,.0f} times as likely\nas honest counts", transform=ax.transAxes, ha='right', va='top', fontsize=8.3, color=MUTED)
fig.text(0.06, 0.455, "Bars: how many of the 84 tests fall in each band of distance from expectation. Line: what each account of the table predicts.", fontsize=9.5, color=MUTED)
fig.suptitle("In Mendel's table no count is far from what he expected", x=0.06, y=0.975, ha='left', fontsize=15, color=INK)
fig.text(0.06, 0.935, "All 84 degrees of freedom of Fisher's 1936 table, each taken as one test, from the counts printed in Mendel's paper. The larger experiments can be split\ninto single tests in many lawful ways; this is one. The furthest count is 1.4 to 1.9 standard deviations out in every one of 72 that were tried.", fontsize=9.5, color=MUTED, va='top', linespacing=1.5)
fig.savefig(sys.argv[2], dpi=130, facecolor='white')
