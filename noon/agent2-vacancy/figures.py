"""The Beveridge curve, and quits against pay.   usage: python -I figures.py results.json out.png"""
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
R = json.load(open(sys.argv[1]))
INK, MUTED, GRID, BLUE, ORANGE, AQUA = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#1baf7a"
HALO = [pe.withStroke(linewidth=2.6, foreground="white")]
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
m = R['months']; jo = np.array([np.nan if v is None else v for v in R['jo']]); ur = np.array(R['ur'])
q = np.array([np.nan if v is None else v for v in R['q']]); wg = np.array([np.nan if v is None else v for v in R['wg']])
t = np.array([int(x[:4]) + (int(x[5:]) - 0.5) / 12 for x in m]); yr = np.array([int(x[:4]) for x in m])
fig = plt.figure(figsize=(12.6, 6.6))
gs = fig.add_gridspec(2, 2, width_ratios=[1.25, 1], wspace=0.2, hspace=0.3)
a = fig.add_subplot(gs[:, 0]); b = fig.add_subplot(gs[0, 1]); c = fig.add_subplot(gs[1, 1], sharex=b)
ok = np.isfinite(jo)
for lo, hi, col in ((2000, 2009, BLUE), (2010, 2019, ORANGE), (2020, 2030, AQUA)):
    sel = ok & (yr >= lo) & (yr <= hi)
    idx = np.where(sel)[0]
    ext = np.r_[idx, idx[-1] + 1] if idx[-1] + 1 < len(m) and ok[idx[-1] + 1] else idx       # join each stretch to the next
    a.plot(ur[ext], jo[ext], color=col, lw=1.3, zorder=2, alpha=0.9)
    a.scatter(ur[sel], jo[sel], s=14, color=col, edgecolor='white', lw=0.4, zorder=3)
for month, txt, dx, dy, ha in (('2009-10', 'October 2009', 6, 8, 'left'), ('2020-04', 'April 2020', -6, 9, 'right'), ('2022-03', 'March 2022', 8, 2, 'left')):
    i = m.index(month)
    a.annotate(txt, (ur[i], jo[i]), xytext=(dx, dy), textcoords='offset points', fontsize=9, color=INK, ha=ha, va='center', path_effects=HALO, zorder=5)
    a.scatter([ur[i]], [jo[i]], s=42, facecolor='white', edgecolor=INK, lw=1.2, zorder=4)
last = int(np.where(ok)[0][-1])
for i, txt, xy in ((m.index('2000-12'), 'December 2000', (5.6, 5.35)), (last, 'latest: ' + ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][int(m[last][5:]) - 1] + ' ' + m[last][:4], (7.6, 5.0))):
    a.annotate(txt, (ur[i], jo[i]), xytext=xy, textcoords='data', fontsize=9, color=INK, ha='left', va='center', path_effects=HALO, zorder=5, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
    a.scatter([ur[i]], [jo[i]], s=42, facecolor='white', edgecolor=INK, lw=1.2, zorder=4)
a.set_xlabel("unemployment rate (%)"), a.set_ylabel("job openings rate (%)")
a.grid(color=GRID, lw=0.8), a.set_axisbelow(True), a.tick_params(length=0)
a.legend(handles=[Line2D([], [], marker='o', ls='-', lw=1.3, ms=5, color=BLUE, label="2000 to 2009"), Line2D([], [], marker='o', ls='-', lw=1.3, ms=5, color=ORANGE, label="2010 to 2019"),
                  Line2D([], [], marker='o', ls='-', lw=1.3, ms=5, color=AQUA, label="2020 on")], loc='upper right', frameon=False, fontsize=9.5)
a.set_title("Job openings against unemployment, month by month", loc='left', fontsize=10.5, color=INK)
b.plot(t, q, color=BLUE, lw=1.8)
b.set_ylabel("%"), b.set_title("The quits rate", loc='left', fontsize=10.5, color=INK)
c.plot(t, wg, color=ORANGE, lw=1.8)
c.set_ylabel("%"), c.set_title("Average hourly pay, change over twelve months", loc='left', fontsize=10.5, color=INK)
for ax in (b, c):
    ax.grid(color=GRID, lw=0.8), ax.set_axisbelow(True), ax.tick_params(length=0)
    ax.axvspan(2020.17, 2021.5, color=GRID, alpha=0.6, lw=0, zorder=0)
c.annotate("grey: March 2020 to June 2021, when\naverage pay swung up and back", (2020.2, 7.4), xytext=(2003.2, 6.6), fontsize=9, color=INK, va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
b.set_xlim(2000.9, t[-1] + 0.2)
plt.setp(b.get_xticklabels(), visible=False)
for ax in (a, b, c):
    for sp in ax.spines.values():
        sp.set_visible(False)
fig.suptitle(sys.argv[3] if len(sys.argv) > 3 else "Vacancies, unemployment, quits and pay in the United States", x=0.06, y=0.98, ha='left', fontsize=14, color=INK)
fig.subplots_adjust(left=0.065, right=0.985, top=0.885, bottom=0.09)
fig.savefig(sys.argv[2], dpi=130, facecolor='white')
