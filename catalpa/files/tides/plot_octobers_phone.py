# The chart of Octobers redrawn for a phone (27 Nov 2026): 700 px wide, large lettering, one yardstick.
# Each October's mean sea level at San Diego and San Francisco, measured from the straight line through all the
# Octobers of that gauge (the slow rise of the sea). Run from ~/tides: ~/ipd/.venv/bin/python -I plot_octobers_phone.py > octobers_phone.out
import csv, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'
fig, axes = plt.subplots(2, 1, figsize=(5.0, 5.6), sharex=True, facecolor=SURF); fig.subplots_adjust(left=0.115, right=0.975, top=0.925, bottom=0.075, hspace=0.16)
for ax, (st, name, col) in zip(axes, (('9410170', 'San Diego', '#2a78d6'), ('9414290', 'San Francisco', '#eb6834'))):
    rows = [r for r in csv.reader(open(f'/home/agent1/tides/data/{st}_monthly_mean.csv')) if r and r[0].strip().isdigit() and int(r[1]) == 10 and r[5].strip() not in ('', 'NaN')]
    y = np.array([int(r[0]) for r in rows]); v = 100 * np.array([float(r[5]) for r in rows]); c = np.polyfit(y, v, 1); res = v - np.polyval(c, y)
    ax.set_facecolor(SURF); ax.axhline(0, color=INK2, lw=1, zorder=1)
    ax.plot(y, res, color=col, lw=1.0, alpha=0.5, zorder=2); ax.scatter(y, res, s=13, color=col, edgecolor=SURF, linewidth=0.5, zorder=3)
    for yr in (1982, 1997, 2015, 2026):
        if yr in y:
            i = list(y).index(yr); big = yr == 2026
            ax.scatter([yr], [res[i]], s=95 if big else 40, color=col, edgecolor=SURF, linewidth=1.5, zorder=4)
            below = (name == 'San Francisco' and yr == 1997)      # at San Francisco the label would otherwise sit on the point for 1983
            ax.annotate(str(yr), (yr, res[i]), xytext=(-9 if big else (4 if below else (-6 if yr != 2015 else 0)), 0 if big else (-9 if below else 8)), textcoords='offset points', ha='right' if (big or (yr != 2015 and not below)) else ('left' if below else 'center'), va='center' if big else ('top' if below else 'bottom'), fontsize=12.5 if big else 10.5, color=INK if big else INK2, fontweight='bold' if big else 'normal')
    ax.text(0.015, 0.93, name, transform=ax.transAxes, fontsize=12.5, color=INK, va='top', fontweight='bold')
    ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.set_ylim(-22, 42); ax.set_yticks([-20, 0, 20, 40]); ax.set_xlim(1850, 2031)
    for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(GRID); ax.tick_params(colors=INK2, length=0, labelsize=11.5)
    i26 = list(y).index(2026); prev = np.argmax(np.where(y == 2026, -99, res))
    e = res[y != 2026]; print(f"{name}: earlier Octobers lie between {e.min():+.1f} and {e.max():+.1f} cm of the line; within 12 cm of it: {np.sum(np.abs(e) <= 12)} of {len(e)}")
    print(f"{name}: {len(y)} Octobers, {y[0]} to {y[-1]}; the line rises {c[0] * 10:.2f} mm a year; October 2026 stands {res[i26]:+.1f} cm above it; the highest earlier October, {y[prev]}, {res[prev]:+.1f}; ratio {res[i26] / res[prev]:.2f}; 1997 {res[list(y).index(1997)]:+.1f}, 2015 {res[list(y).index(2015)]:+.1f}, 1982 {res[list(y).index(1982)]:+.1f}; above the gauge's 1983-2001 level: 2026 {v[i26]:+.1f}")
axes[1].set_xticks([1860, 1900, 1940, 1980, 2020])
fig.text(0.015, 0.985, 'cm above the slow rise of the sea', fontsize=11.5, color=INK2, va='top')
fig.savefig('/home/agent1/site/img/coast-octobers.png', dpi=140, facecolor=SURF)
