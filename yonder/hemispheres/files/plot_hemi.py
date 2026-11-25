"""Figures for the hemisphere note.

usage: plot_hemi.py GRID_DIR OUT_DIR COAST110.geojson COAST50.geojson

Reads OUT_DIR/results.json and maps.npz (from hemi_run.py) and the grids; writes
  OUT_DIR/hemi-maps.png    share of land, and of people, within 90 degrees of every point
  OUT_DIR/hemi-globes.png  the two hemispheres of each, seen from above their centres
  OUT_DIR/hemi-flat.png    how flat the land maximum is, around its centre
Colour: one hue per quantity, light to dark (blue for land shares, orange for people); text in ink.
"""
import json
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hemilib as h

gdir, odir, coast110, coast50 = sys.argv[1:5]
res = json.load(open(f'{odir}/results.json'))
M = np.load(f'{odir}/maps.npz')
KM = np.pi * h.R_KM / 180
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#d9d8d2'
BLUE = LinearSegmentedColormap.from_list('blue', ['#eef5fd', '#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95', '#0d366b'])
ORANGE = LinearSegmentedColormap.from_list('orange', ['#fdf1ea', '#fbd9c8', '#f6b596', '#f08e62', '#eb6834', '#c44f1f', '#963a14', '#6b280c'])
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'text.color': INK, 'axes.edgecolor': GRID,
                     'axes.labelcolor': INK2, 'xtick.color': INK2, 'ytick.color': INK2, 'figure.facecolor': SURF,
                     'axes.facecolor': SURF, 'savefig.facecolor': SURF})


def coast_rings(path):
    d = json.load(open(path, encoding='utf-8'))
    out = []
    for f in d['features']:
        g = f['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in polys:
            for ring in poly:
                out.append(np.asarray(ring, dtype=np.float64)[:, :2])
    return out


C110 = coast_rings(coast110)

# ------------------------------------------------------------------ world maps of the two shares
fig = plt.figure(figsize=(7.6, 8.4))
for k, (key, cmap, word, r) in enumerate((('land', BLUE, 'land', res['land10']), ('pop', ORANGE, 'people', res['people']))):
    ax = fig.add_subplot(2, 1, k + 1, projection='mollweide')
    lats, lons, S = M[f'{key}_lats'], M[f'{key}_lons'], M[f'{key}_S'] * 100
    step = lats[1] - lats[0]
    le = np.radians(np.append(lons - step / 2, 180)); be = np.radians(np.append(lats - step / 2, 90))
    pc = ax.pcolormesh(le, be, S, cmap=cmap, vmin=0, vmax=100, shading='flat', rasterized=True)
    LO, LA = np.meshgrid(np.radians(lons), np.radians(lats))
    cs = ax.contour(LO, LA, S, levels=[10, 20, 30, 40, 50, 60, 70, 80, 90], colors=SURF, linewidths=0.5)
    ax.clabel(cs, levels=[30, 50, 70] if key == 'land' else [20, 50, 80], fmt='%d%%', fontsize=7, colors=INK)
    for ring in C110:
        x = np.radians(ring[:, 0]); y = np.radians(ring[:, 1])
        ax.plot(x, y, color=INK, lw=0.35, alpha=0.75)
    la, lo = r['lat'], r['lon']
    ax.plot(np.radians(lo), np.radians(la), 'o', ms=5, mfc=SURF, mec=INK, mew=1.0)
    ax.annotate(f'most {word}: {100 * r["share"]:.1f}%', (np.radians(lo), np.radians(la)), xytext=(8, 8), textcoords='offset points',
                fontsize=8, color=INK, bbox=dict(boxstyle='round,pad=0.2', fc=SURF, ec='none', alpha=0.85))
    alo = lo + 180 if lo < 0 else lo - 180
    ax.plot(np.radians(alo), np.radians(-la), 'o', ms=5, mfc=INK, mec=SURF, mew=0.8)
    ax.annotate(f'least {word}: {100 * (1 - r["share"]):.1f}%', (np.radians(alo), np.radians(-la)), xytext=(9, -3), textcoords='offset points',
                ha='left', fontsize=8, color=INK, bbox=dict(boxstyle='round,pad=0.2', fc=SURF, ec='none', alpha=0.85))
    ax.set_xticklabels([]); ax.set_yticklabels([])
    ax.grid(False)
    ax.set_title(f'Share of the world\'s {word} within 90° of each point', fontsize=10, loc='left', color=INK, pad=8)
    cb = fig.colorbar(pc, ax=ax, orientation='vertical', fraction=0.025, pad=0.02, ticks=[0, 25, 50, 75, 100])
    cb.ax.set_yticklabels(['0', '25', '50', '75', '100%']); cb.outline.set_visible(False); cb.ax.tick_params(length=0, labelsize=7)
fig.tight_layout()
fig.savefig(f'{odir}/hemi-maps.png', dpi=200)
plt.close(fig)

# ------------------------------------------------------------------ globes
land = np.load(f'{gdir}/land10.npy')
pop = np.load(f'{gdir}/pop005.npy')
f = 4
land_c = land.reshape(land.shape[0] // f, f, land.shape[1] // f, f).mean(axis=(1, 3))        # 0.2 degree
pop_c = pop.reshape(pop.shape[0] // f, f, pop.shape[1] // f, f).sum(axis=(1, 3))


def ortho(centre, n=700):
    """For an n x n picture of the hemisphere centred on `centre`: grid indices of each pixel, and a mask of the disc."""
    c = h.unit(*centre)
    la0, lo0 = centre
    north = h.unit(la0 + 90, lo0) if la0 <= 0 else -h.unit(la0 - 90, lo0)
    east = np.cross(north, c)
    u = np.linspace(-1, 1, n)
    Xp, Yp = np.meshgrid(u, -u)
    rr = Xp ** 2 + Yp ** 2
    disc = rr <= 1
    z = np.sqrt(np.clip(1 - rr, 0, 1))
    V = Xp[..., None] * east + Yp[..., None] * north + z[..., None] * c
    lat, lon = h.latlon(V)
    H, W = land_c.shape
    i = np.clip(((lat + 90) / 180 * H).astype(int), 0, H - 1)
    j = np.clip(((lon + 180) / 360 * W).astype(int), 0, W - 1)
    return i, j, disc


def antipode(p):
    return (-p[0], p[1] + 180 if p[1] < 0 else p[1] - 180)


fig, axes = plt.subplots(2, 2, figsize=(7.6, 8.0))
cl = (res['land10']['lat'], res['land10']['lon'])
cp = (res['people']['lat'], res['people']['lon'])
rows = [(cl, res['land10']['share'], 'land'), (cp, res['people']['share'], 'people')]
for a, (centre, share, word) in enumerate(rows):
    for b, (cen, sh) in enumerate(((centre, share), (antipode(centre), 1 - share))):
        ax = axes[a, b]
        i, j, disc = ortho(cen)
        img = np.ones(i.shape + (3,))
        water = np.array(matplotlib.colors.to_rgb('#e3eefb')); ground = np.array(matplotlib.colors.to_rgb('#b9b8b1'))
        lc = land_c[i, j][..., None]
        base = water * (1 - lc) + ground * lc
        if word == 'people':
            dens = pop_c[i, j]
            t = np.clip((np.log10(np.maximum(dens, 1)) - 2) / (6.5 - 2), 0, 1)     # 100 .. 3 million people per 0.2-degree cell
            col = ORANGE(0.25 + 0.75 * t)[..., :3]
            m = (dens > 100)[..., None]
            base = np.where(m, col, base)
        else:
            base = water * (1 - lc) + np.array(matplotlib.colors.to_rgb('#256abf')) * lc
        img[disc] = base[disc]
        img[~disc] = matplotlib.colors.to_rgb(SURF)
        ax.imshow(img, extent=(-1, 1, -1, 1), interpolation='bilinear')
        ax.add_patch(plt.Circle((0, 0), 1, fill=False, ec=INK2, lw=0.6))
        ax.plot(0, 0, '+', ms=7, mec=INK, mew=0.9)
        ax.set_xlim(-1.03, 1.03); ax.set_ylim(-1.03, 1.03); ax.set_aspect('equal'); ax.axis('off')
        la, lo = cen
        where = f'{abs(la):.1f}°{"N" if la >= 0 else "S"}, {abs(lo):.1f}°{"E" if lo >= 0 else "W"}'
        head = (f'The half with most {word}' if b == 0 else 'The other half')
        ax.set_title(f'{head}\n{100 * sh:.1f}% of the world\'s {word}; centre {where}', fontsize=9, color=INK, loc='center')
fig.tight_layout()
fig.savefig(f'{odir}/hemi-globes.png', dpi=200)
plt.close(fig)

# ------------------------------------------------------------------ flatness of the two maxima (wide maps)
C50 = coast_rings(coast50)


def flat_figure(npz, cmap, levels, marks, title, out):
    Wd = np.load(npz)
    offs, G, north, east, c0 = Wd['offs'], Wd['G'], Wd['north'], Wd['east'], Wd['c_mid']
    loss = (np.nanmax(G) - G) * 100
    fig, ax = plt.subplots(figsize=(7.2, 7.0))
    ext = offs * KM
    ax.contourf(ext, ext, loss, levels=[0] + levels + [100], colors=[cmap(v) for v in (0.95, 0.8, 0.65, 0.5, 0.36, 0.22, 0.08)])
    cs = ax.contour(ext, ext, loss, levels=levels, colors=SURF, linewidths=0.6)
    ax.clabel(cs, fmt=lambda v: f'{v:g}', fontsize=7, colors=INK)

    def project(lat, lon):
        v = h.unit(lat, lon)
        t = h.angle_deg(v, c0)
        s_ = np.sin(np.radians(np.maximum(t, 1e-12)))
        return t * (v @ east) / s_ * KM, t * (v @ north) / s_ * KM

    for ring in C50:
        v = h.unit(ring[:, 1], ring[:, 0])
        if (h.angle_deg(v, c0) < 14).any():
            x, y = project(ring[:, 1], ring[:, 0])
            ax.plot(x, y, color=INK, lw=0.55, alpha=0.8)
    for name, p_, mk, off, ha in marks:
        x, y = project(*p_)
        ax.plot(x, y, mk, ms=6.5, mfc=SURF, mec=INK, mew=1.1, zorder=5)
        if name:
            ax.annotate(name, (x, y), xytext=off, textcoords='offset points', fontsize=8, color=INK, ha=ha, zorder=6,
                        bbox=dict(boxstyle='round,pad=0.15', fc=SURF, ec='none', alpha=0.85))
    ax.set_xlim(ext[0], ext[-1]); ax.set_ylim(ext[0], ext[-1]); ax.set_aspect('equal')
    ax.set_xlabel('km east'); ax.set_ylabel('km north')
    ax.set_title(title, fontsize=10, loc='left', color=INK)
    for sp in ax.spines.values():
        sp.set_color(GRID)
    ax.tick_params(length=0)
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    plt.close(fig)


flat_figure(f'{odir}/wide.npz', BLUE, [0.01, 0.05, 0.1, 0.2, 0.4, 0.8],
            [('largest share\n(this computation)', cl, 'o', (9, -14), 'left'), ('Nantes (1945)', (47 + 13 / 60, -(1 + 32 / 60)), 's', (9, 3), 'left'),
             ('Île Dumet (1913)', (47 + 24 / 60 + 42 / 3600, -(2 + 37 / 60 + 15 / 3600)), '^', (-9, 5), 'right')],
            'How much land a hemisphere loses when its centre is moved away from the best\n(percentage points of the world\'s land; 1:10m coastline)',
            f'{odir}/hemi-flat.png')
if os.path.exists(f'{odir}/wide-people.npz'):
    flat_figure(f'{odir}/wide-people.npz', ORANGE, [0.02, 0.06, 0.1, 0.2, 0.4, 0.8],
                [('largest share, 2020', cp, 'o', (9, 4), 'left'), ('western Alps: highest\nin the grids up to 2010', (45.05, 6.69), 's', (9, -12), 'left'),
                 ('', (46.0, 7.17), 's', (0, 0), 'left'), ('', (44.35, 7.28), 's', (0, 0), 'left'),
                 ('Upper Palatinate:\nlevel with the top in 2015', (49.37, 12.38), '^', (9, -8), 'left')],
                'How many people a hemisphere loses when its centre is moved away from the best\n(percentage points of the world\'s people, 2020)',
                f'{odir}/hemi-flat-people.png')
print('figures written')
