"""The two summits of the land share (off Catalonia, and in southern Brittany) under changes of data and definition.

usage: summits.py GRID_DIR OUT_DIR

For each variant: climb to the nearest local maximum from each of the two summits found with the 1:10m Natural
Earth land on a sphere, and report both shares and their difference. Not scored; run after the sealed expectations
had been scored.

Changed after the third review (21 November): the four GSHHG rows now use the grids of gshhg_fix.py (the islands off
Antarctica that GSHHG files under level 5 are included; lake water is levels 2 - 3 + 4). The output of the run before
that change is kept as out/summits-before-review.out.
"""
import json
import os
import sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hemilib as h

gdir, odir = sys.argv[1], sys.argv[2]
KM = np.pi * h.R_KM / 180
MED = (40.82, 1.72)
BRIT = (47.41, -2.33)
E2 = 0.00669437999014


def geocentric(lat_deg):
    return np.degrees(np.arctan((1 - E2) * np.tan(np.radians(np.asarray(lat_deg, dtype=np.float64)))))


def inverse(latmap, v):
    g = np.linspace(-90, 90, 360001)
    return float(np.interp(v, latmap(g), g))


def climb(X, w, e, start):
    c = h.unit(*start)
    for half, step in ((0.6, 0.05), (0.12, 0.01)):
        for it in range(400):
            lc = h.Local(X, w, e, c, half * 1.5)
            o, g, n_, e_ = lc.grid(half, step)
            i, j = np.unravel_index(np.nanargmax(g), g.shape)
            if o[i] == 0 and o[j] == 0:
                break
            c = lc.point(o[i], o[j], n_, e_)
    return c, h.share(X, w, c, e)


def load(name):
    return np.load(f'{gdir}/{name}.npy')


land = load('land10')
variants = [
    ('Natural Earth 1:10m, sphere (the scored run)', lambda: h.area_weights(land), None),
    ('Natural Earth 1:50m', lambda: h.area_weights(load('land50')), None),
    ('Natural Earth 1:110m', lambda: h.area_weights(load('land110')), None),
    ('Natural Earth 1:10m, lakes counted as water', lambda: h.area_weights(np.clip(land - load('lakes10'), 0, 1)), None),
    ('Natural Earth 1:10m, equal-area (authalic) sphere', lambda: h.area_weights(land, h.authalic), h.authalic),
    ('Natural Earth 1:10m, plane through the centre of the ellipsoid, true areas', lambda: h.area_weights(land, h.authalic), geocentric),
    ('GSHHG 2.3.7 intermediate, grounding line, lakes as land', lambda: h.area_weights(load('gshhg_i2')), None),
    ('GSHHG 2.3.7 high, grounding line, lakes as land', lambda: h.area_weights(load('gshhg_h2')), None),
    ('GSHHG 2.3.7 intermediate, lakes counted as water', lambda: h.area_weights(np.clip(load('gshhg_i2') - load('gshhg_i_water'), 0, 1)), None),
    ('GSHHG 2.3.7 high, plane through the centre of the ellipsoid, true areas', lambda: h.area_weights(load('gshhg_h2'), h.authalic), geocentric),
]
rows = []
for name, make, latmap in variants:
    wg = make()
    X, w, e = h.cells(wg, latmap)
    out = {}
    for tag, start in (('med', MED), ('brit', BRIT)):
        s0 = (float(latmap(start[0])), start[1]) if latmap else start
        c, s = climb(X, w, e, s0)
        la, lo = h.latlon(c)
        la_g = inverse(latmap, la) if latmap else float(la)
        out[tag] = dict(lat=la_g, lon=float(lo), share=s, km_from_start=float(h.angle_deg(h.unit(la_g, lo), h.unit(*start)) * KM))
    d = 100 * (out['med']['share'] - out['brit']['share'])
    rows.append(dict(name=name, area=float(wg.sum()), **out, diff_points=d))
    print(f'{name}\n   land {wg.sum():,.0f} km2 | Catalan summit {100 * out["med"]["share"]:.4f}% at {out["med"]["lat"]:.2f}, {out["med"]["lon"]:.2f} '
          f'({out["med"]["km_from_start"]:.0f} km from its starting point) | Breton summit {100 * out["brit"]["share"]:.4f}% at {out["brit"]["lat"]:.2f}, {out["brit"]["lon"]:.2f} '
          f'({out["brit"]["km_from_start"]:.0f} km) | Catalan - Breton = {d:+.4f} points = {d / 100 * wg.sum():+,.0f} km2', flush=True)
json.dump(rows, open(f'{odir}/summits.json', 'w'), indent=1)
print('written')
