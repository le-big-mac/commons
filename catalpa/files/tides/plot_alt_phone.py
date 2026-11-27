# The satellite figure redrawn for a phone (27 Nov 2026) as two pictures 700 px wide with large lettering:
# the map (coast-map.png) and the same against distance from the coast (coast-profile.png).
# Reads alt_anom.pkl, written by alt.py. Run from anywhere: ~/ipd/.venv/bin/python -I ~/tides/plot_alt_phone.py > ~/tides/alt_phone.out
import numpy as np, pickle, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
SURF, INK, INK2, GRID, MID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df', '#f0efec'; BLUE, ORANGE = '#2a78d6', '#eb6834'
cells, anom, D = pickle.load(open('/home/agent1/tides/alt_anom.pkl', 'rb'))
lats = sorted(set(k[0] for k in cells)); lons = sorted(set(k[1] for k in cells)); Z = np.full((len(lats), len(lons)), np.nan)
for k in cells: Z[lats.index(k[0]), lons.index(k[1])] = anom[k]
cmap = LinearSegmentedColormap.from_list('div', [(0, '#104281'), (0.25, '#2a78d6'), (0.42, '#b7d3f6'), (0.5, MID), (0.58, '#f4bcb8'), (0.75, '#e34948'), (1, '#7d1a1d')]); levels = np.arange(-22, 22.1, 4); norm = BoundaryNorm(levels, cmap.N)
fig = plt.figure(figsize=(5.0, 4.15), facecolor=SURF); ax = fig.add_axes([0.13, 0.21, 0.86, 0.77])
le = np.r_[np.array(lons) - 0.125, lons[-1] + 0.125]; la = np.r_[np.array(lats) - 0.125, lats[-1] + 0.125]
pm = ax.pcolormesh(le, la, np.ma.masked_invalid(Z), cmap=cmap, norm=norm, edgecolors=SURF, linewidth=0.25)
ax.set_facecolor(SURF); ax.set_aspect(1 / np.cos(np.radians(33))); ax.set_xlim(-128, -113.6); ax.set_ylim(28, 38)
for name, lat, lon in (('San Diego', 32.714, -117.174), ('San Francisco', 37.807, -122.465), ('Los Angeles', 33.72, -118.27)):
    ax.scatter([lon], [lat], s=55, color=INK, edgecolor=SURF, linewidth=1.5, zorder=5)
    ax.annotate(name, (lon, lat), xytext=(lon + 0.45, lat + (0.0 if name != 'San Diego' else 0.05)), ha='left', va='center', fontsize=11, color=INK, zorder=6)
ax.set_xticks([-128, -124, -120, -116]); ax.set_xticklabels(['128°W', '124°W', '120°W', '116°W']); ax.set_yticks([30, 32, 34, 36, 38]); ax.set_yticklabels([f'{v}°N' for v in (30, 32, 34, 36, 38)])
ax.tick_params(colors=INK2, length=0, labelsize=10.5)
for s in ax.spines.values(): s.set_visible(False)
ax.text(-115.2, 36.6, 'land', ha='right', va='center', fontsize=11, color=INK2, style='italic')
cax = fig.add_axes([0.13, 0.095, 0.84, 0.03]); tk = [-18, -10, -2, 2, 10, 18]; cb = fig.colorbar(pm, cax=cax, orientation='horizontal', ticks=tk); cb.outline.set_visible(False); cb.ax.tick_params(colors=INK2, length=0, labelsize=10.5)
cb.ax.set_xticklabels(['−18', '−10', '−2', '+2', '+10', '+18 cm'])
fig.savefig('/home/agent1/site/img/coast-map.png', dpi=140, facecolor=SURF)
# the profile
fig = plt.figure(figsize=(5.0, 3.9), facecolor=SURF); bx = fig.add_axes([0.105, 0.15, 0.855, 0.72])
edges = np.arange(0, 525, 25); mid = (edges[:-1] + edges[1:]) / 2
for (la0, la1), col, name, g, gname, dy in (((32, 34), BLUE, 'off southern California', 33.7, 'San Diego gauge', -2.6), ((36, 38), ORANGE, 'off San Francisco', 25.3, 'San Francisco gauge', 2.2)):
    m = np.array([np.mean([anom[k] for k in cells if la0 <= k[0] <= la1 and a <= D[k] < b] or [np.nan]) for a, b in zip(edges[:-1], edges[1:])])
    bx.plot(mid, m, color=col, lw=2.2, zorder=3); bx.scatter(mid, m, s=24, color=col, edgecolor=SURF, linewidth=1, zorder=4)
    bx.scatter([0], [g], s=95, marker='D', color=col, edgecolor=SURF, linewidth=1.5, zorder=5, clip_on=False)
    bx.text(-12, g, gname.replace(' gauge', '\ngauge'), ha='right', va='center', fontsize=10.5, color=INK, linespacing=1.1)
    bx.text(498, m[-1] + dy, name, fontsize=11, color=INK, ha='right', va='center')
    print(f"{name}: gauge {g:+.1f}; first bins {np.round(m[:6], 1)}; at 187 km {m[7]:.1f}; last {m[-1]:.1f}")
bx.axhline(0, color=INK2, lw=1, zorder=2); bx.set_facecolor(SURF); bx.grid(True, axis='y', color=GRID, lw=1); bx.set_axisbelow(True)
for s in ('top', 'right', 'left'): bx.spines[s].set_visible(False)
bx.spines['bottom'].set_color(GRID); bx.tick_params(colors=INK2, length=0, labelsize=11.5); bx.set_xlim(-118, 500); bx.set_ylim(-6, 38); bx.set_yticks([0, 10, 20, 30]); bx.set_xticks([0, 100, 200, 300, 400, 500])
bx.set_xlabel('distance from the coast, km', color=INK2, fontsize=11.5)
fig.text(0.015, 0.975, 'cm above the Octobers of 2017 to 2025', fontsize=11.5, color=INK2, va='top')
fig.savefig('/home/agent1/site/img/coast-profile.png', dpi=140, facecolor=SURF)
