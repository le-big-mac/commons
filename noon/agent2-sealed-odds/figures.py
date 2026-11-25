"""Two figures for the report.   usage: python figures.py lines.csv calibration.png studies.png"""
import sys, csv, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = [r for r in csv.DictReader(open(sys.argv[1])) if r['outcome'] != '']
INK, MUTED, GRID, BLUE, ORANGE, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#b9b1a5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
fo = lambda r: r['forecasters'] or r.get('forecasters_late', '')
def style(ax, title):
    ax.grid(color=GRID, lw=0.8); ax.set_axisbelow(True); ax.tick_params(length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(title, loc='left', fontsize=10.5, color=INK, pad=8)
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d; return c - h, c + h
def bins(odds, y, edges):
    out = []
    for lo, hi in zip(edges, edges[1:]):
        k = (odds >= lo) & (odds < hi)
        if k.sum(): a, b = wilson(int(y[k].sum()), int(k.sum())); out.append((odds[k].mean(), y[k].mean(), a, b, int(k.sum())))
    return out
fig, axs = plt.subplots(1, 3, figsize=(13.6, 5.2), sharey=True); fig.subplots_adjust(left=0.06, right=0.985, top=0.74, bottom=0.12, wspace=0.08)
o = np.array([float(r['odds']) for r in R]); y = np.array([float(r['outcome']) for r in R])
M = [r for r in R if r['kind'] == 'sheet' and fo(r)]
om = np.array([float(r['odds']) for r in M]); ym = np.array([float(r['outcome']) for r in M]); fm = np.array([float(fo(r)) for r in M])
E = [0, 0.5, 0.6, 0.7, 0.8, 0.9, 1.01]
for ax, (oo, yy, col, title) in zip(axs, ((o, y, BLUE, f"My odds, all {len(R)} settled lines"), (om, ym, BLUE, f"My odds, the {len(M)} main-sheet lines"), (fm, ym, ORANGE, f"Three forecasters' median, the same {len(M)} lines"))):
    ax.plot([0, 1], [0, 1], color=NEUTRAL, lw=1.2, ls=(0, (4, 3)))
    for x, p, lo, hi, n in bins(oo, yy, E):
        ax.plot([x, x], [lo, hi], color=col, lw=1.2); ax.plot(x, p, marker='o', ms=7, color=col, markeredgecolor='white', markeredgewidth=1); ax.annotate(f"{n}", (x, p), xytext=(7, -4), textcoords='offset points', fontsize=8.5, color=MUTED)
    ax.set_xlim(0.0, 1.0); ax.set_ylim(0.0, 1.03); ax.set_xlabel("the odds given beforehand (mean of the group)"); style(ax, title)
axs[0].set_ylabel("share that held")
fig.suptitle("Were the odds right?", x=0.06, y=0.965, ha='left', fontsize=15, color=INK)
fig.text(0.06, 0.915, "Expectations sealed with odds on 21 and 22 November, grouped by the odds given, against how often the group held.\nDashed: odds that would be exactly right. Bars: 95% intervals as if the lines were independent, which they are not. Small figures: lines in the group.\nGroups: below 0.5, then by tenths. The forecasters\' panel pools six sheets priced at the time with four priced a day later.", fontsize=9.5, color=MUTED, va='top', linespacing=1.5)
fig.savefig(sys.argv[2], dpi=130, facecolor='white'); plt.close(fig)
# ---- by study
fig = plt.figure(figsize=(12.4, 5.0)); ax = fig.add_axes([0.20, 0.13, 0.77, 0.67])
studies = list(dict.fromkeys(r['study'] for r in sorted(R, key=lambda r: int(r['order'])))); ypos = np.arange(len(studies))[::-1]
for st, yp in zip(studies, ypos):
    rows = [r for r in R if r['study'] == st and r['kind'] == 'sheet']; oo = np.array([float(r['odds']) for r in rows]); yy = np.array([float(r['outcome']) for r in rows]); mine = ((oo - yy) ** 2).mean()
    fc = [r for r in rows if fo(r)]; late = bool(fc) and not fc[0]['forecasters']
    ax.barh(yp + (0.19 if fc else 0), mine, height=0.36, color=BLUE); ax.text(mine + 0.004, yp + (0.19 if fc else 0), f"{mine:.3f}  ({int(yy.sum())} of {len(rows)} held; my odds averaged {oo.mean():.2f})", va='center', fontsize=8.5, color=INK)
    if fc:
        f = np.array([float(fo(r)) for r in fc]); t = ((f - yy) ** 2).mean(); ax.barh(yp - 0.19, t, height=0.36, color=ORANGE, alpha=0.55 if late else 1.0); ax.text(t + 0.004, yp - 0.19, f"{t:.3f}  (their odds averaged {f.mean():.2f}{'; priced a day later' if late else ''})", va='center', fontsize=8.5, color=INK)
ax.set_yticks(ypos); ax.set_yticklabels(studies, fontsize=9.5, color=INK); ax.set_xlim(0, 0.70); ax.set_xlabel("Brier score on the main sheet (lower is better; saying one half to everything scores 0.25)")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=BLUE, label="my sealed odds"), Patch(color=ORANGE, label="three blind forecasters' median (paler: priced afterwards)")], loc='lower right', bbox_to_anchor=(1.0, 1.0), ncol=2, frameon=False, fontsize=9)
ax.axvline(0.25, color=NEUTRAL, lw=1.2, ls=(0, (4, 3))); style(ax, "The ten main sheets, in the order they were sealed"); ax.grid(axis='y', visible=False)
fig.suptitle("Sheet by sheet", x=0.07, y=0.965, ha='left', fontsize=15, color=INK)
fig.savefig(sys.argv[3], dpi=130, facecolor='white')
