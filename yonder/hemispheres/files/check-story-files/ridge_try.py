"""The ridge map for the public page, redrawn for a reader who has not seen the work: places named, both summits marked,
a scale bar in place of axes. Same data as the note's hemi-flat.png (out/wide.npz, written by hemi_run.py).

usage: ridge_page.py HEMI_DIR COAST50.geojson OUT.png      (HEMI_DIR holds hemilib.py and out/wide.npz, out/summits.json)
Colour: one hue, light to dark (darker = more land); labels in ink.
"""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import LinearSegmentedColormap
hemi, coast50, out = sys.argv[1:4]
sys.path.insert(0, hemi)
import hemilib as h

KM = np.pi * h.R_KM / 180
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#d9d8d2'
BLUE = LinearSegmentedColormap.from_list('blue', ['#eef5fd', '#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95', '#0d366b'])
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'text.color': INK, 'figure.facecolor': SURF, 'axes.facecolor': SURF, 'savefig.facecolor': SURF})

W = np.load(os.path.join(hemi, 'out', 'wide.npz'))
offs, G, north, east, c0 = W['offs'], W['G'], W['north'], W['east'], W['c_mid']
loss = (np.nanmax(G) - G) * 100            # percentage points of the world's land lost against the best centre
levels = [0.01, 0.05, 0.1, 0.2, 0.4, 0.8]
ext = offs * KM

def project(lat, lon):
    v = h.unit(np.asarray(lat, float), np.asarray(lon, float))
    t = h.angle_deg(v, c0)
    s_ = np.sin(np.radians(np.maximum(t, 1e-12)))
    return t * (v @ east) / s_ * KM, t * (v @ north) / s_ * KM

# the two summits, from the grid itself: the best point, and the best point within 150 km of the northern end
iy, ix = np.unravel_index(np.nanargmax(G), G.shape)
south = (ext[ix], ext[iy])
Y, X = np.meshgrid(ext, ext, indexing='ij')
nx, ny = project(47.42, -2.36)
near = (X - nx) ** 2 + (Y - ny) ** 2 < 150 ** 2
Gn = np.where(near, G, -1); jy, jx = np.unravel_index(np.argmax(Gn), G.shape)
northp = (ext[jx], ext[jy])
gap_points = (G[iy, ix] - G[jy, jx]) * 100
print(f'southern summit on this grid at ({south[0]:+.0f}, {south[1]:+.0f}) km, share {100 * G[iy, ix]:.3f}%; northern at ({northp[0]:+.0f}, {northp[1]:+.0f}) km, share {100 * G[jy, jx]:.3f}%; '
      f'gap {gap_points:.3f} points; distance {np.hypot(south[0] - northp[0], south[1] - northp[1]):.0f} km')

fig, ax = plt.subplots(figsize=(7.0, 7.75))
ax.contourf(ext, ext, loss, levels=[0] + levels + [100], colors=[BLUE(v) for v in (0.95, 0.8, 0.65, 0.5, 0.36, 0.22, 0.08)])
cs = ax.contour(ext, ext, loss, levels=levels, colors=SURF, linewidths=0.6)
ax.clabel(cs, fmt=lambda v: f'{v:g}', fontsize=7, colors=INK)
d = json.load(open(coast50, encoding='utf-8'))
for f in d['features']:
    g = f['geometry']
    for poly in (g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]):
        for ring in poly:
            r = np.asarray(ring, dtype=np.float64)[:, :2]
            if (h.angle_deg(h.unit(r[:, 1], r[:, 0]), c0) < 14).any():
                x, y = project(r[:, 1], r[:, 0]); ax.plot(x, y, color=INK, lw=0.9, alpha=0.95)

halo = [pe.withStroke(linewidth=2.6, foreground=SURF, alpha=0.9)]
def place(text, x, y, **kw):           # positions in km east and north of the middle of the map
    ax.text(x, y, text, ha='center', va='center', path_effects=halo, clip_on=True, **kw)
for name, x, y in (('F R A N C E', 250, 180), ('S P A I N', -430, -600), ('ITALY', 690, 150), ('ENGLAND', -100, 830)):
    place(name, x, y, fontsize=8.5, color=INK2)
for name, x, y in (('Bay of\nBiscay', -520, 60), ('Mediterranean\nSea', 420, -700)):
    place(name, x, y, fontsize=8, color=INK2, style='italic')
bx, by = project(48.25, -3.3); place('Brittany', float(bx), float(by), fontsize=8, color=INK)
cx, cy = project(41.95, 1.2); place('Catalonia', float(cx), float(cy), fontsize=8, color=INK)

def mark(xy, mk, label, at, ha, ms=7.5, bold=False):
    ax.plot(xy[0], xy[1], mk, ms=ms, mfc=SURF, mec=INK, mew=1.2, zorder=5)
    ax.annotate(label, xy, xytext=at, textcoords='data', fontsize=8.5, color=INK, ha=ha, va='center', zorder=6, fontweight='bold' if bold else 'normal',
                bbox=dict(boxstyle='round,pad=0.25', fc=SURF, ec='none', alpha=0.92), arrowprops=dict(arrowstyle='-', color=INK, lw=0.7, shrinkA=0, shrinkB=4))
mark(south, 'o', 'southern summit: the most land\n(81.2% of the world\'s)', (250, -330), 'left', bold=True)
mark(northp, 'o', 'northern summit: 46,000 km² less\n(0.03% of the world\'s land)', (20, 520), 'left', bold=True)
mark(tuple(float(v) for v in project(47 + 13 / 60, -(1 + 32 / 60))), 's', 'Nantes (the centre given in 1945)', (20, 345), 'left', ms=6)
mark(tuple(float(v) for v in project(47 + 24 / 60 + 42 / 3600, -(2 + 37 / 60 + 15 / 3600))), '^', 'Île Dumet (1913)', (-850, 420), 'left', ms=6)
mark(tuple(float(v) for v in project(41.119, 1.245)), 'D', 'Tarragona', (-330, -330), 'right', ms=4.5)

# scale bar in place of axes
x0, y0 = ext[0] + 60, ext[0] + 330
ax.plot([x0, x0 + 200], [y0, y0], color=INK, lw=2.2, solid_capstyle='butt', zorder=6)
ax.text(x0 + 100, y0 + 28, '200 km', ha='center', va='bottom', fontsize=8, color=INK, path_effects=halo, zorder=6)
ax.set_xlim(ext[0], ext[-1]); ax.set_ylim(ext[0], ext[-1]); ax.set_aspect('equal')
ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values(): sp.set_color(GRID)
fig.subplots_adjust(left=0.015, right=0.985, bottom=0.012, top=0.895)
fig.text(0.015, 0.968, 'How much land a half of the Earth holds, by where its centre is put', fontsize=11, color=INK, va='center')
fig.text(0.015, 0.922, 'Darker blue: more land. The number on each line is the land lost when the centre is put there\ninstead of at the best point, in % of the world\'s land.',
         fontsize=8.2, color=INK2, va='center', linespacing=1.35)
fig.savefig(out, dpi=170)
print('written', out)
