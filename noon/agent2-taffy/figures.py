"""How fast each device lengthens a loop.   usage: python figures.py sheet.json film.json taffy.png"""
import sys, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = json.load(open(sys.argv[1])); FL = json.load(open(sys.argv[2])); OUT = sys.argv[3]
INK, MUTED, GRID, BLUE, ORANGE = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
NAMES = {'T1': "s₁ S₂", 'T2': "s₁ s₁ S₂ S₂", 'T3': "s₁ s₂", 'T4': "s₁ s₂ S₃", 'T5': "s₁ s₃ S₂", 'T6': "s₁ s₃ S₂ S₂"}
fig, (a, b) = plt.subplots(1, 2, figsize=(12.4, 5.4), gridspec_kw=dict(width_ratios=[1.25, 1])); fig.subplots_adjust(left=0.085, right=0.97, top=0.80, bottom=0.12, wspace=0.22)
def style(ax, title):
    ax.grid(color=GRID, lw=0.8); ax.set_axisbelow(True); ax.tick_params(length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(title, loc='left', fontsize=10.5, color=INK, pad=8)
order = sorted(('T1', 'T2', 'T3', 'T4', 'T5', 'T6'), key=lambda k: math.log(R[k]['growth']) / len(R[k]['moves']))
for y, k in enumerate(order):
    rate = math.log(R[k]['growth']) / len(R[k]['moves']); col = BLUE if R[k]['n'] == 3 else ORANGE
    a.barh(y, rate, height=0.62, color=col)
    a.text(rate + 0.008, y, f"×{R[k]['growth']:.3f} a period, ×{math.exp(rate):.3f} an exchange" if R[k]['growth'] > 1.0001 else "no growth", fontsize=9, color=INK, va='center')
a.set_yticks(range(len(order))); a.set_yticklabels([NAMES[k] for k in order], fontsize=9.5, color=INK); a.set_xlim(0, 0.78); a.set_xlabel("stretching per exchange of two rods (logarithm of the growth factor)")
from matplotlib.patches import Patch
a.legend(handles=[Patch(color=BLUE, label="three rods"), Patch(color=ORANGE, label="four rods")], loc='lower right', frameon=False, fontsize=9)
style(a, "What the braid forces, counted per exchange (other units change the order)")
a.grid(axis='y', visible=False)
for j, (name, col) in enumerate((("s₁ s₁ S₂ S₂", BLUE), ("s₁ s₂", MUTED))):
    y = np.array(FL['lengths'][j]); b.plot(np.arange(len(y)), y, color=col, lw=1.8, marker='o', ms=3.5)
    b.text(len(y) - 1 + 0.3, y[-1], f"{name}:\n×{y[-1]:,.0f} after {len(y) - 1} moves", fontsize=8.5, color=INK, va='center')
xs = np.arange(8, 17); b.plot(xs, 30 * R['T2']['growth'] ** ((xs - 12) / 4), color="#b9b1a5", lw=1.3, ls=(0, (4, 3)), zorder=1); b.text(1.0, 230, "dashed: the rate the braid forces,\n×5.83 every 4 moves", fontsize=8.5, color=MUTED, va='top')
b.set_yscale('log'); b.set_xlim(0, 23); b.set_xticks(range(0, 17, 4)); b.set_xlabel("moves made"); b.set_ylabel("length of the material loop (start = 1)")
style(b, "A loop in my model fluid: its length after each move")
fig.suptitle("How fast a taffy puller lengthens the candy", x=0.07, y=0.96, ha='left', fontsize=15, color=INK)
fig.text(0.07, 0.885, "s = two neighbouring rods change places clockwise, S = anticlockwise; the subscript says which pair. A device repeats its list of moves.", fontsize=9.5, color=MUTED)
fig.savefig(OUT, dpi=130, facecolor='white')
