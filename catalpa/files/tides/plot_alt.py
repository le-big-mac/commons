# Figure: where the excess of October 2026 sits.  Left: altimetry, October 2026 minus the mean of Octobers 2017-2025, off California.  Right: the same against distance from the coast,
# with the two tide gauges at zero.  Reads /tmp/alt_anom.pkl written by alt.py (run that first).
import numpy as np, pickle, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
SURF, INK, INK2, GRID, MID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df', '#f0efec'; BLUE, ORANGE = '#2a78d6', '#eb6834'
cells, anom, D = pickle.load(open('/tmp/alt_anom.pkl', 'rb'))
lats = sorted(set(k[0] for k in cells)); lons = sorted(set(k[1] for k in cells)); Z = np.full((len(lats), len(lons)), np.nan)
for k in cells: Z[lats.index(k[0]), lons.index(k[1])] = anom[k]
cmap = LinearSegmentedColormap.from_list('div', [(0, '#104281'), (0.25, '#2a78d6'), (0.42, '#b7d3f6'), (0.5, MID), (0.58, '#f4bcb8'), (0.75, '#e34948'), (1, '#7d1a1d')]); levels = np.arange(-22, 22.1, 4); norm = BoundaryNorm(levels, cmap.N)      # eleven bands, the middle one (-2..+2) the neutral grey
fig = plt.figure(figsize=(11, 5.9), facecolor=SURF); ax = fig.add_axes([0.05, 0.10, 0.40, 0.78]); bx = fig.add_axes([0.56, 0.17, 0.41, 0.70])
le = np.r_[np.array(lons) - 0.125, lons[-1] + 0.125]; la = np.r_[np.array(lats) - 0.125, lats[-1] + 0.125]
pm = ax.pcolormesh(le, la, np.ma.masked_invalid(Z), cmap=cmap, norm=norm, edgecolors=SURF, linewidth=0.25)
ax.set_facecolor(SURF); ax.set_aspect(1 / np.cos(np.radians(33))); ax.set_xlim(-128, -116); ax.set_ylim(28, 38)
for name, lat, lon in (('San Diego', 32.714, -117.174), ('San Francisco', 37.807, -122.465), ('Los Angeles', 33.72, -118.27)):
    ax.scatter([lon], [lat], s=42, color=INK, edgecolor=SURF, linewidth=1.5, zorder=5); ax.annotate(name, (lon, lat), xytext=(lon + 0.35, lat), ha='left', va='center', fontsize=9, color=INK, zorder=6)
ax.set_xticks([-128, -124, -120, -116]); ax.set_xticklabels(['128°W', '124°W', '120°W', '116°W']); ax.set_yticks([28, 30, 32, 34, 36, 38]); ax.set_yticklabels([f'{v}°N' for v in (28, 30, 32, 34, 36, 38)])
ax.tick_params(colors=INK2, length=0, labelsize=8.5)
for s in ax.spines.values(): s.set_visible(False)
ax.set_title('Sea level from satellites, October 2026\nminus the mean of Octobers 2017–2025', loc='left', fontsize=10.5, color=INK, pad=8)
ax.text(-116.3, 35.6, 'land\n(no cells)', ha='right', va='center', fontsize=8.5, color=INK2)
tk = [-18, -10, -2, 2, 10, 18]; cb = fig.colorbar(pm, ax=ax, orientation='horizontal', ticks=tk, pad=0.07, fraction=0.035, aspect=42); cb.outline.set_visible(False); cb.ax.tick_params(colors=INK2, length=0, labelsize=8.5)
cb.ax.set_xticklabels(['−18', '−10', '−2', '+2', '+10', '+18 cm'])
edges = np.arange(0, 525, 25); mid = (edges[:-1] + edges[1:]) / 2
for (la0, la1), col, name, g, gname in (((32, 34), BLUE, 'off southern California, 32–34°N', 33.7, 'San Diego gauge'), ((36, 38), ORANGE, 'off San Francisco, 36–38°N', 25.3, 'San Francisco gauge')):
    m = np.array([np.mean([anom[k] for k in cells if la0 <= k[0] <= la1 and a <= D[k] < b] or [np.nan]) for a, b in zip(edges[:-1], edges[1:])])
    bx.plot(mid, m, color=col, lw=2, zorder=3); bx.scatter(mid, m, s=22, color=col, edgecolor=SURF, linewidth=1, zorder=4)
    bx.scatter([0], [g], s=80, marker='D', color=col, edgecolor=SURF, linewidth=1.5, zorder=5, clip_on=False)
    bx.annotate(f'{gname}: +{g:.0f} cm', (0, g), xytext=(12, 0), textcoords='offset points', va='center', fontsize=9, color=INK)
    bx.annotate(name, (mid[-1], m[-1]), xytext=(4, 10 if la0 == 36 else -16), textcoords='offset points', fontsize=9, color=INK, ha='right')
bx.axhline(0, color=INK2, lw=1, zorder=2); bx.set_facecolor(SURF); bx.grid(True, axis='y', color=GRID, lw=1); bx.set_axisbelow(True)
for s in ('top', 'right', 'left'): bx.spines[s].set_visible(False)
bx.spines['bottom'].set_color(GRID); bx.tick_params(colors=INK2, length=0, labelsize=9); bx.set_xlim(-8, 500); bx.set_ylim(-6, 38)
bx.set_xlabel('distance from the coast, km', color=INK2, fontsize=9.5); bx.set_title('The same, by distance from the coast (cm);\ndiamonds: the tide gauges, same months', loc='left', fontsize=10.5, color=INK, pad=8)
fig.text(0.56, 0.035, 'NOAA CoastWatch blended altimetry (0.25°, daily means of October) and\nNOAA tide gauges 9410170 and 9414290, as served on 25 Nov 2026.', color=INK2, fontsize=8, va='bottom')
fig.savefig('offshore.png', dpi=150, facecolor=SURF)
