# Figure 2: satellite sea level along the coast against time (distance up the page, time across).
# Reads alt_smooth.npy written by alt_trace.py. Run: ~/ipd/.venv/bin/python -I src/plot_hov.py  (writes hov.png)
import json, datetime as dt, sys
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
SURF, INK, INK2, GRID, MID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df', '#f0efec'
pts = json.load(open('/home/agent1/trace/data/alt/points.json')); sm = np.load('/home/agent1/trace/alt_smooth.npy')
km = np.array([p['km'] for p in pts]); D0 = dt.date(2026, 5, 1)
a, b = (dt.date(2026, 6, 1) - D0).days, (dt.date(2026, 11, 18) - D0).days
Z = sm[:, a:b + 1]
cmap = LinearSegmentedColormap.from_list('div', [(0, '#104281'), (0.25, '#2a78d6'), (0.42, '#b7d3f6'), (0.5, MID), (0.58, '#f4bcb8'), (0.75, '#e34948'), (1, '#7d1a1d')])
# the same colour for the same size either side of zero (-52 to +52); only -12 to +52 occurs and is shown on the bar
from matplotlib.colors import Normalize, ListedColormap
edges = np.arange(-52, 52.1, 4); mids = (edges[:-1] + edges[1:]) / 2
cols = [cmap((m + 52) / 104) for m in mids]; keep = [i for i, m in enumerate(mids) if m > -12]
cmap = ListedColormap([cols[i] for i in keep]); cmap.set_under(cols[keep[0] - 1]); cmap.set_over('#5c1215')
levels = edges[keep[0]:]; norm = BoundaryNorm(levels, cmap.N)
fig = plt.figure(figsize=(11, 6.6), facecolor=SURF); ax = fig.add_axes([0.20, 0.13, 0.70, 0.70])
xe = np.arange(a, b + 2) - 0.5; ye = np.r_[km - 50, km[-1] + 50]
pm = ax.pcolormesh(xe, ye, np.ma.masked_invalid(Z), cmap=cmap, norm=norm)
ax.set_facecolor('#d9d8d3')
ticks = [dt.date(2026, m, 1) for m in range(6, 12)]
ax.set_xticks([(t - D0).days for t in ticks]); ax.set_xticklabels([t.strftime('1 %b') for t in ticks])
places = [(-1230, 'Callao, Peru'), (0, 'La Libertad, Ecuador'), (2000, 'Quepos, Costa Rica'), (2820, 'Acajutla, El Salvador'), (3998, 'Acapulco'),
          (5418, 'Cabo San Lucas'), (6762, 'San Diego'), (7551, 'San Francisco'), (8789, 'Neah Bay, Washington')]
ax.set_yticks([p[0] for p in places]); ax.set_yticklabels([p[1] for p in places])
ax.tick_params(colors=INK2, length=3, labelsize=9, color=GRID)
for s in ax.spines.values(): s.set_visible(False)
ax2 = ax.twinx(); ax2.set_ylim(ax.get_ylim()); ax2.set_yticks([0, 2000, 4000, 6000, 8000]); ax2.set_yticklabels(['0', '2,000', '4,000', '6,000', '8,000 km'])
ax2.tick_params(colors=INK2, length=0, labelsize=8.5)
for s in ax2.spines.values(): s.set_visible(False)
if len(sys.argv) > 1:   # guide lines: a wave at the given speeds (m/s), drawn through the given start day at La Libertad
    for spec in sys.argv[1:]:
        v, day = spec.split('@'); v = float(v); t0 = (dt.date.fromisoformat(day) - D0).days
        yy = np.array([0, 8800]); xx = t0 + yy / (v * 86.4)
        ax.plot(xx, yy, color=INK, lw=1.2, ls=(0, (4, 3)), zorder=5)
        ax.annotate(f'{v:g} m/s', (xx[1], yy[1]), xytext=(3, 4), textcoords='offset points', fontsize=8.5, color=INK, clip_on=False)
ax.set_xlim(a - 0.5, b + 0.5)
cb = fig.colorbar(pm, cax=fig.add_axes([0.20, 0.055, 0.42, 0.018]), orientation='horizontal', ticks=[-12, 0, 12, 24, 36, 48]); cb.outline.set_visible(False)
cb.ax.tick_params(colors=INK2, length=0, labelsize=8.5); cb.ax.set_xticklabels(['−12', '0', '+12', '+24', '+36', '+48 cm'])
fig.text(0.20, 0.935, 'One band of high water from Peru to California. California filled last.', fontsize=11.5, color=INK, va='bottom')
fig.text(0.20, 0.915, 'Sea level from satellites near the shore, June to November 2026, compared with the same time of year\nin 2017 to 2025. Up the page is north along the coast.', fontsize=9, color=INK2, va='top', linespacing=1.4)
fig.text(0.65, 0.04, 'NOAA CoastWatch blended altimetry, daily,\n15-day running mean, to 18 November.', fontsize=8, color=INK2, va='bottom', linespacing=1.4)
ax.annotate('mouth of the Gulf of Panama', (a + 3, 1300), xytext=(a + 3, 1300), fontsize=7.5, color=INK, va='center')
fig.savefig('/home/agent1/trace/hov.png', dpi=150, facecolor=SURF)
