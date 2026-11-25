"""Two figures for the smell ratings.   usage: python -I figures.py results-molecules.csv results.json OUTDIR"""
import sys, json, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
M = pd.read_csv(sys.argv[1]); R = json.load(open(sys.argv[2])); OUT = sys.argv[3]
os.makedirs(OUT, exist_ok=True)
INK, MUTED, GRID, BLUE, ORANGE, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#b9b1a5"
HALO = [pe.withStroke(linewidth=2.6, foreground="white")]
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})

# ---- 1: every molecule, strength against pleasantness
fig, ax = plt.subplots(figsize=(10.2, 7.6))
rest = M[~M['S'] & ~M['is_acid']]; ac = M[M['is_acid'] & ~M['S']]; su = M[M['S']]
ax.scatter(rest['strength'], rest['pleasantness'], s=26, color=NEUTRAL, edgecolor='white', lw=0.6, zorder=2)
ax.scatter(ac['strength'], ac['pleasantness'], s=46, color=BLUE, edgecolor='white', lw=0.9, zorder=3)
ax.scatter(su['strength'], su['pleasantness'], s=46, color=ORANGE, edgecolor='white', lw=0.9, zorder=4)
LAB = {'vanillin': ('vanillin', 8, 4, 'left'), 'Ethyl Vanillin': ('ethyl vanillin', -8, 2, 'right'), 'Methyl thiobutyrate': ('methyl thiobutyrate', -8, -3, 'right'),
       'isovaleric acid': ('isovaleric acid\n(sweat, cheese)', 8, -12, 'left'), 'Piperidine': ('piperidine', -6, -12, 'right'), 'D-Camphor': ('camphor', 8, 3, 'left'),
       'Benzene': ('benzene', 0, 9, 'center'), 'L-Cysteine': ('cysteine', -8, 4, 'right'), 'Linalool': ('linalool', 8, -3, 'left')}
for nm, (txt, dx, dy, ha) in LAB.items():
    r = M[M['name'] == nm]
    if len(r):
        r = r.iloc[0]
        ax.annotate(txt, (r['strength'], r['pleasantness']), xytext=(dx, dy), textcoords='offset points', fontsize=9, color=INK, ha=ha, va='center', path_effects=HALO, zorder=6)
ax.set_xlim(5, 97), ax.set_ylim(0, 92)
ax.set_xlabel("how strong (mean rating, 0 to 100)"), ax.set_ylabel("how pleasant (mean rating, 0 to 100)")
ax.grid(color=GRID, lw=0.8), ax.set_axisbelow(True), ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.legend(handles=[Line2D([], [], marker='o', ls='', ms=8, color=ORANGE, mec='white', label=f"contains sulfur ({len(su)})"),
                   Line2D([], [], marker='o', ls='', ms=8, color=BLUE, mec='white', label=f"an acid, no sulfur ({len(ac)})"),
                   Line2D([], [], marker='o', ls='', ms=6.5, color=NEUTRAL, mec='white', label=f"the other {len(rest)} molecules")],
          loc='upper left', bbox_to_anchor=(0.0, 1.075), frameon=False, fontsize=9.5, ncols=3, columnspacing=1.8, handletextpad=0.3)
fig.suptitle("480 molecules as 55 people smelled them: sulfur and acids sit at the foul end", x=0.065, y=0.98, ha='left', fontsize=13.5, color=INK)
fig.subplots_adjust(left=0.065, right=0.985, top=0.875, bottom=0.085)
fig.savefig(f"{OUT}/molecules.png", dpi=130, facecolor='white')
plt.close(fig)

# ---- 2: what can be predicted from the structure
attrs = sorted(R['model'], key=lambda a: R['model'][a])
sul = {a: abs(float(np.corrcoef(M['S'].astype(float), M[a])[0, 1])) for a in attrs}
NAMES = {'strength': 'how strong', 'pleasantness': 'how pleasant', 'familiarity': 'how familiar', 'ammonia': 'ammonia / urinous'}
fig, ax = plt.subplots(figsize=(9.6, 8.6))
ceiling = {}
for y, a in enumerate(attrs):
    ceil = float(np.sqrt(2 * R['half'][a] / (1 + R['half'][a])))        # what a perfect predictor would reach against the panel's noisy mean
    ceiling[a] = ceil
    xs = [sul[a], R['model'][a], ceil]
    ax.plot([min(xs), max(xs)], [y, y], color=GRID, lw=2.5, zorder=1, solid_capstyle='round')
    ax.plot([ceil], [y], marker='|', ms=13, mew=2, color=INK, zorder=3)
    ax.scatter([sul[a]], [y], s=58, color=ORANGE, edgecolor='white', lw=1.1, zorder=4)
    ax.scatter([R['model'][a]], [y], s=58, color=BLUE, edgecolor='white', lw=1.1, zorder=5)
ax.set_yticks(range(len(attrs))), ax.set_yticklabels([NAMES.get(a, a) for a in attrs], fontsize=10, color=INK)
ax.set_xlim(-0.02, 1.02), ax.set_ylim(-0.7, len(attrs) - 0.3)
ax.set_xlabel("correlation with the panel's mean rating, across molecules")
ax.grid(axis='x', color=GRID, lw=0.8), ax.set_axisbelow(True), ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.legend(handles=[Line2D([], [], marker='o', ls='', ms=8, color=BLUE, mec='white', label="a forest on 181 structural descriptors, molecules it has not seen"),
                   Line2D([], [], marker='o', ls='', ms=8, color=ORANGE, mec='white', label="one fact: does the molecule contain sulfur?"),
                   Line2D([], [], marker='|', ls='', ms=12, mew=2, color=INK, label="the limit for a predictor that knew the vial and its dilution, set by the noise in the panel's mean")],
          loc='upper left', bbox_to_anchor=(-0.02, 1.115), frameon=False, fontsize=9.5, ncols=1)
fig.suptitle("What the structure of a molecule says about its smell", x=0.03, y=0.985, ha='left', fontsize=13.5, color=INK)
fig.subplots_adjust(left=0.2, right=0.975, top=0.845, bottom=0.075)
fig.savefig(f"{OUT}/predict.png", dpi=130, facecolor='white')
json.dump(sul, open(f"{OUT}/sulfur-alone.json", 'w'), indent=1)
print({a: (round(sul[a], 2), round(R['model'][a], 2), round(ceiling[a], 2)) for a in attrs[::-1]})
json.dump(ceiling, open(f"{OUT}/ceiling.json", 'w'), indent=1)
