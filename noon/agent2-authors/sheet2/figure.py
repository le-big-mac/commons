"""One figure: Brier score against the time each pricer took.   usage: python -I figure.py SHEET1DIR SHEET2DIR out.png
Minutes are from first seeing the task to filing the odds (file times and the harness's durations), typed in below."""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
D1, D2, OUT = sys.argv[1:4]
INK, MUTED, GRID, BLUE, ORANGE, AQUA = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
brier = lambda p, y: float(((np.array(p) - np.array(y)) ** 2).mean())
MIN = {  # minutes: sheet 1, sheet 2
    'quick': ([29.4 / 60, 36.1 / 60, 22.1 / 60], [41.2 / 60, 34.7 / 60, 47.9 / 60]),
    'careful': ([389.1 / 60, 640.6 / 60, 617.8 / 60], [714.1 / 60, 656.7 / 60, 653.9 / 60]),
    'author_quick': (8.77, 6.95), 'author_careful': (16.92, None), 'outsider': (2.70, 2.68)}
pts = []
for si, D in enumerate((D1, D2)):
    s = json.load(open(f"{D}/scored.json")); q = json.load(open(f"{D}/quick/scored.json")); y = s['outcome']
    for k in range(3):
        pts.append(('quick reader', si, MIN['quick'][si][k], brier(q['quick_readers'][k], y)))
        pts.append(('careful reader', si, MIN['careful'][si][k], brier(s['readers'][k], y)))
    pts.append(('author, quick odds', si, MIN['author_quick'][si], brier(s['quick'], y)))
    if s.get('careful'):
        pts.append(('author, careful odds', si, MIN['author_careful'][si], brier(s['careful'], y)))
    pts.append(('outsider (Noon)', si, MIN['outsider'][si], brier(s['outsider'], y)))
COL = {'quick reader': BLUE, 'careful reader': BLUE, 'author, quick odds': ORANGE, 'author, careful odds': ORANGE, 'outsider (Noon)': AQUA}
fig, ax = plt.subplots(figsize=(10.2, 6.4))
for name, si, t, b in pts:
    ax.scatter([t], [b], s=95, marker='o' if si == 0 else 's', color=COL[name], edgecolor='white', lw=1.2, zorder=3, alpha=0.9)
ax.set_xscale('log'), ax.set_xlim(0.25, 30), ax.set_ylim(-0.005, 0.155)
ax.set_xticks([0.5, 1, 2, 5, 10, 20]), ax.set_xticklabels(['½', '1', '2', '5', '10', '20'])
ax.set_xlabel("minutes from first seeing the task to filing the odds (only the two kinds of reader were assigned theirs)"), ax.set_ylabel("Brier score on that sheet's twelve statements (lower is better)")
ax.grid(color=GRID, lw=0.8), ax.set_axisbelow(True), ax.tick_params(length=0, which='both')
for sp in ax.spines.values():
    sp.set_visible(False)
ax.text(0.72, 0.137, "readers told to answer at once,\nwithout recalling figures", fontsize=9.5, color=INK, ha='left', va='center')
ax.text(2.7, 0.070, "me, an outsider\nto each sheet", fontsize=9.5, color=INK, ha='center', va='bottom')
ax.text(7.2, 0.082, "authors' first numbers\n(filed with the sheet they\nhad just written)", fontsize=9.5, color=INK, ha='center', va='bottom')
ax.text(14.5, 0.058, "readers who\ntook their time", fontsize=9.5, color=INK, ha='left', va='bottom')
ax.text(16.9, 0.026, "author's careful\nsecond pass", fontsize=9.5, color=INK, ha='center', va='top')
ax.legend(handles=[Line2D([], [], marker='o', ls='', ms=9, color=BLUE, mec='white', label="readers"), Line2D([], [], marker='o', ls='', ms=9, color=ORANGE, mec='white', label="the sheet's author"),
                   Line2D([], [], marker='o', ls='', ms=9, color=AQUA, mec='white', label="outsider (Noon)"),
                   Line2D([], [], marker='o', ls='', ms=8, color=MUTED, mec='white', label="first sheet (earthquakes)"), Line2D([], [], marker='s', ls='', ms=8, color=MUTED, mec='white', label="second sheet (sunspots)")],
          loc='upper left', bbox_to_anchor=(0.0, 1.105), frameon=False, fontsize=9.5, ncols=5, columnspacing=1.4, handletextpad=0.2)
fig.suptitle("Readers left to take their time scored far better than readers told to answer at once", x=0.075, y=0.975, ha='left', fontsize=13.5, color=INK)
fig.subplots_adjust(left=0.085, right=0.98, top=0.86, bottom=0.105)
fig.savefig(OUT, dpi=130, facecolor='white')
for p in sorted(pts, key=lambda p: p[2]):
    print(f"{p[0]:22s} sheet {p[1] + 1}  {p[2]:6.2f} min  Brier {p[3]:.4f}")
