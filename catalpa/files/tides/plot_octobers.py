# October mean sea level by year at San Diego and San Francisco (NOAA monthly means), with the straight-line trend; 2026 marked.
import csv, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'
fig, axes = plt.subplots(2, 1, figsize=(8.2, 6.4), sharex=True, facecolor=SURF)
for ax, (st, name, col) in zip(axes, (('9410170', 'San Diego', '#2a78d6'), ('9414290', 'San Francisco', '#eb6834'))):
    rows = [r for r in csv.reader(open(f'data/{st}_monthly_mean.csv')) if r and r[0].strip().isdigit() and int(r[1]) == 10 and r[5].strip() not in ('', 'NaN')]
    y = np.array([int(r[0]) for r in rows]); v = 100 * np.array([float(r[5]) for r in rows]); c = np.polyfit(y, v, 1)
    ax.set_facecolor(SURF); ax.plot(y, np.polyval(c, y), color=INK2, lw=1, zorder=1)
    ax.plot(y, v, color=col, lw=1.2, alpha=0.55, zorder=2); ax.scatter(y, v, s=14, color=col, edgecolor=SURF, linewidth=0.6, zorder=3)
    for yr in (1982, 1997, 2015, 2026):
        if yr in y:
            i = list(y).index(yr); big = yr == 2026
            ax.scatter([yr], [v[i]], s=70 if big else 36, color=col, edgecolor=SURF, linewidth=1.5, zorder=4)
            ax.annotate(f'{yr}: {v[i]:+.0f} cm' if big else str(yr), (yr, v[i]), xytext=(-8 if big else (-5 if yr == 1982 else 0), 9), textcoords='offset points', ha='right' if (big or yr == 1982) else 'center', va='bottom', fontsize=9.5 if big else 8.5, color=INK if big else INK2)
    ax.set_title(f'{name}: mean sea level in October, each year (cm above the 1983–2001 mean)', loc='left', fontsize=10.5, color=INK, pad=8)
    ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True)
    for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(GRID); ax.tick_params(colors=INK2, length=0, labelsize=9); ax.set_ylim(-29, 56)
    ax.text(1856, 44, f'straight line: the trend, {c[0] * 10:.1f} mm a year', color=INK2, fontsize=8.5)
axes[1].set_xlabel('year', color=INK2, fontsize=9.5)
fig.text(0.012, 0.012, "NOAA tide gauges 9410170 and 9414290, monthly means as served on 25 Nov 2026. Earlier strong El Niño years are labelled.", color=INK2, fontsize=8.5)
fig.tight_layout(rect=(0, 0.035, 1, 1)); fig.savefig('octobers.png', dpi=150, facecolor=SURF)
