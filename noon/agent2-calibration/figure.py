"""One figure: every expectation at its forecast, coloured by what happened.   usage: python -I figure.py scored.json out.png"""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
S = json.load(open(sys.argv[1]))
INK, MUTED, GRID, BLUE, ORANGE, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
NAMES = {'antipodes': 'opposite points', 'antipodes-second-year': 'opposite points: a second year', 'antipodes-finer-grid': 'opposite points: a finer grid',
         'antipodes-sharpest-gri': 'x', 'antipodes-sharpest-grid': 'opposite points: the sharpest grid', 'voices': 'three voices', 'voices-human-control': 'three voices: naturalists',
         'voices-reader-test': 'three voices: readers', 'trails': 'trails on a lawn', 'snowdrops': 'snowdrops', 'atlantic': 'closing the Atlantic', 'clinch': 'football: settled when?',
         'pacing': 'ice ages', 'plurality': 'ranked ballots', 'aroma': 'smells'}
files = []
for s in S:
    if s['file'] not in files:
        files.append(s['file'])
stat = {f: (np.mean([s['forecast'] for s in S if s['file'] == f]), np.mean([s['outcome'] for s in S if s['file'] == f])) for f in files}
files.sort(key=lambda f: stat[f][0] - stat[f][1])                        # most too low at the bottom, most too high at the top
fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.6, 7.4), gridspec_kw={"width_ratios": [2.15, 1], "wspace": 0.16})
COL = {1.0: BLUE, 0.0: ORANGE, 0.5: NEUTRAL}
for yy, f in enumerate(files):
    its = sorted([s for s in S if s['file'] == f], key=lambda s: s['forecast'])
    ax.plot([0, 1], [yy, yy], color=GRID, lw=1, zorder=1)
    used = {}
    for s in its:
        x = round(s['forecast'], 2)
        k = used.get(x, 0); used[x] = k + 1
        off = (0.0, 0.26, -0.26, 0.13, -0.13)[k % 5]                      # equal forecasts are stacked, not hidden
        ax.scatter([s['forecast']], [yy + off], s=64, color=COL[s['outcome']], edgecolor='white', lw=1.1, zorder=3 + (s['outcome'] == 0))
    ax.plot([stat[f][1]], [yy], marker='|', ms=22, mew=2, color=INK, zorder=2)
ax.set_yticks(range(len(files))), ax.set_yticklabels([NAMES.get(f, f) for f in files], fontsize=10, color=INK)
ax.set_xlim(-0.02, 1.02), ax.set_ylim(-0.7, len(files) - 0.3)
ax.set_xticks(np.arange(0, 1.01, 0.2)), ax.set_xticklabels([f"{int(100 * x)}%" for x in np.arange(0, 1.01, 0.2)])
ax.set_xlabel("the forecasters' probability that the expectation would hold (median of five)")
ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.legend(handles=[Line2D([], [], marker='o', ls='', ms=8.5, color=BLUE, mec='white', label="held"), Line2D([], [], marker='o', ls='', ms=8.5, color=ORANGE, mec='white', label="failed"),
                   Line2D([], [], marker='o', ls='', ms=8.5, color=NEUTRAL, mec='white', label="half"), Line2D([], [], marker='|', ls='', ms=14, mew=2, color=INK, label="how that study scored (a half counts half)")],
          loc='upper left', bbox_to_anchor=(-0.02, 1.075), frameon=False, fontsize=9.5, ncols=4, columnspacing=1.6, handletextpad=0.3)
# calibration in bands
fc = np.array([s['forecast'] for s in S]); y = np.array([s['outcome'] for s in S])
edges = [0, 0.3, 0.5, 0.65, 0.8, 1.0001]
bx.plot([0, 1], [0, 1], color=INK, lw=1, ls=(0, (4, 3)), zorder=1)
for a, b in zip(edges[:-1], edges[1:]):
    m = (fc >= a) & (fc < b)
    if m.sum():
        bx.scatter([fc[m].mean()], [y[m].mean()], s=30 + 14 * m.sum(), color=BLUE, edgecolor='white', lw=1.2, zorder=3)
        bx.annotate(f"{int(m.sum())}", (fc[m].mean(), y[m].mean()), xytext=(0, -1), textcoords='offset points', ha='center', va='center', fontsize=8.5, color='white', zorder=4)
bx.text(0.97, 0.05, "on the dashed line, what was\nsaid and what happened agree", fontsize=9, color=INK, ha='right', va='bottom')
bx.set_xlim(0, 1), bx.set_ylim(0, 1), bx.set_aspect('equal')
bx.set_xticks(np.arange(0.2, 1.01, 0.2)), bx.set_xticklabels([f"{int(100 * x)}%" for x in np.arange(0.2, 1.01, 0.2)])
bx.set_yticks(np.arange(0, 1.01, 0.2)), bx.set_yticklabels([f"{int(100 * x)}%" for x in np.arange(0, 1.01, 0.2)])
bx.set_xlabel("forecast (mean of the band)"), bx.set_ylabel("share that held (a half counts half)")
bx.grid(color=GRID, lw=0.8), bx.set_axisbelow(True), bx.tick_params(length=0)
for sp in bx.spines.values():
    sp.set_visible(False)
bx.set_title("Five bands of forecast; the number\nin each dot is how many expectations", loc='left', fontsize=10, color=INK)
fig.suptitle(sys.argv[3] if len(sys.argv) > 3 else "78 expectations, forecast blind by five fresh instances", x=0.02, y=0.985, ha='left', fontsize=14, color=INK)
fig.subplots_adjust(left=0.205, right=0.985, top=0.855, bottom=0.085)
fig.savefig(sys.argv[2], dpi=130, facecolor='white')
