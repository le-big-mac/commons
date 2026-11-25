"""Figure for the woodpecker coda: share of woodpecker species within 90 degrees of each point, and where they live.

usage: plot_wp.py OUT_DIR COAST110.geojson
"""
import json
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

odir, coast110 = sys.argv[1], sys.argv[2]
res = json.load(open(f'{odir}/woodpeckers.json'))
M = np.load(f'{odir}/woodpecker-maps.npz')
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#d9d8d2'
AQUA = LinearSegmentedColormap.from_list('aqua', ['#eefaf5', '#cdeede', '#9adcc0', '#5cc79f', '#1baf7a', '#168f64', '#106b4b', '#0a4a34'])
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'text.color': INK, 'figure.facecolor': SURF, 'axes.facecolor': SURF, 'savefig.facecolor': SURF,
                     'axes.edgecolor': GRID, 'axes.labelcolor': INK2, 'xtick.color': INK2, 'ytick.color': INK2})
d = json.load(open(coast110, encoding='utf-8'))
rings = []
for f in d['features']:
    g = f['geometry']
    for poly in (g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]):
        for ring in poly:
            rings.append(np.asarray(ring, dtype=np.float64)[:, :2])
fig = plt.figure(figsize=(7.6, 8.4))
# (a) share map
ax = fig.add_subplot(2, 1, 1, projection='mollweide')
lats, lons, S = M['wp_lats'], M['wp_lons'], M['wp_S'] * 100
step = lats[1] - lats[0]
le = np.radians(np.append(lons - step / 2, 180)); be = np.radians(np.append(lats - step / 2, 90))
pc = ax.pcolormesh(le, be, S, cmap=AQUA, vmin=0, vmax=100, shading='flat', rasterized=True)
LO, LA = np.meshgrid(np.radians(lons), np.radians(lats))
cs = ax.contour(LO, LA, S, levels=[10, 20, 30, 40, 50, 60, 70, 80], colors=SURF, linewidths=0.5)
ax.clabel(cs, levels=[20, 50, 80], fmt='%d%%', fontsize=7, colors=INK)
for r in rings:
    ax.plot(np.radians(r[:, 0]), np.radians(r[:, 1]), color=INK, lw=0.35, alpha=0.75)
k = res['K5']
ax.plot(np.radians(k['lon']), np.radians(k['lat']), 'o', ms=5, mfc=SURF, mec=INK, mew=1.0)
ax.annotate(f'most woodpeckers: {100 * k["share"]:.1f}%', (np.radians(k['lon']), np.radians(k['lat'])), xytext=(8, 8), textcoords='offset points',
            fontsize=8, color=INK, bbox=dict(boxstyle='round,pad=0.2', fc=SURF, ec='none', alpha=0.85))
ax.set_xticklabels([]); ax.set_yticklabels([]); ax.grid(False)
ax.set_title('Share of the world\'s woodpecker species within 90° of each point', fontsize=10, loc='left', color=INK, pad=8)
cb = fig.colorbar(pc, ax=ax, orientation='vertical', fraction=0.025, pad=0.02, ticks=[0, 25, 50, 75, 100])
cb.ax.set_yticklabels(['0', '25', '50', '75', '100%']); cb.outline.set_visible(False); cb.ax.tick_params(length=0, labelsize=7)
# (b) richness per 5-degree box
ax = fig.add_subplot(2, 1, 2, projection='mollweide')
rich = M['wp_rich'].astype(float)
rich[rich == 0] = np.nan
le = np.radians(np.arange(-180, 181, 5)); be = np.radians(np.arange(-90, 91, 5))
pc = ax.pcolormesh(le, be, rich, cmap=AQUA, vmin=0, vmax=np.nanmax(rich), shading='flat', rasterized=True)
for r in rings:
    ax.plot(np.radians(r[:, 0]), np.radians(r[:, 1]), color=INK, lw=0.35, alpha=0.75)
ax.set_xticklabels([]); ax.set_yticklabels([]); ax.grid(False)
ax.set_title('Woodpecker species with at least five records, per 5° box (GBIF)', fontsize=10, loc='left', color=INK, pad=8)
cb = fig.colorbar(pc, ax=ax, orientation='vertical', fraction=0.025, pad=0.02)
cb.outline.set_visible(False); cb.ax.tick_params(length=0, labelsize=7)
fig.tight_layout()
fig.savefig(f'{odir}/hemi-woodpeckers.png', dpi=200)
print('written')
