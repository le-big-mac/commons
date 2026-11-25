"""The two summits of the land share on a third coastline: OpenStreetMap's simplified land polygons.

usage: osm_summits.py GRID_DIR OUT_DIR

grids/osm_raw.npy is the raster of the polygons (osm_read.py, raster.py).  The data stop at 85.0511 S, where Web
Mercator ends; everything south of that is land and is added here.  Not scored; done on 21 November after the note
was published, to close the gap it named ("I have not tried the OpenStreetMap coastline").
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
MED, BRIT = (40.82, 1.72), (47.41, -2.33)
E2 = 0.00669437999014
geocentric = lambda lat: np.degrees(np.arctan((1 - E2) * np.tan(np.radians(np.asarray(lat, dtype=np.float64)))))
inverse = lambda latmap, v: float(np.interp(v, latmap(np.linspace(-90, 90, 360001)), np.linspace(-90, 90, 360001)))


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
        else:
            raise SystemExit('climb did not stop')
    return c, h.share(X, w, c, e)


osm = np.load(f'{gdir}/osm_raw.npy').astype(np.float64)
H = osm.shape[0]
lat_top = -90 + (np.arange(H) + 1) * (180 / H)                 # upper edge of each row
cap = lat_top <= -85.0511
part = (lat_top > -85.0511) & (lat_top - 180 / H < -85.0511)   # the row the cut passes through
print(f'rows wholly south of 85.0511 S: {cap.sum()}; coverage there before: {osm[cap].mean():.4f}; set to 1')
osm[cap] = 1.0
if part.any():
    r = np.flatnonzero(part)[0]
    frac = (-85.0511 - (lat_top[r] - 180 / H)) / (180 / H)
    osm[r] = np.maximum(osm[r], frac)                           # the strip of that row south of the cut is land
ne = np.load(f'{gdir}/land10.npy'); shelf = np.load(f'{gdir}/shelf10.npy')
print(f'OSM land (with the cap): {h.area_weights(osm).sum():,.0f} km2; Natural Earth 1:10m land {h.area_weights(ne).sum():,.0f}, with ice shelves {h.area_weights(np.clip(ne + shelf, 0, 1)).sum():,.0f}')
print(f'area where OSM and Natural Earth with shelves differ: {h.area_weights(np.abs(osm - np.clip(ne + shelf, 0, 1))).sum():,.0f} km2; north of 60 S only: {h.area_weights(np.abs(osm - ne))[1800 // 3:].sum():,.0f} km2')
rows = []
for name, wg, latmap in (('OpenStreetMap simplified land polygons (18 Nov 2026), sphere', h.area_weights(osm), None),
                         ('OpenStreetMap, plane through the centre of the ellipsoid, true areas', h.area_weights(osm, h.authalic), geocentric)):
    X, w, e = h.cells(wg, latmap)
    out = {}
    for tag, start in (('med', MED), ('brit', BRIT)):
        s0 = (float(latmap(start[0])), start[1]) if latmap else start
        c, s = climb(X, w, e, s0)
        la, lo = h.latlon(c)
        la_g = inverse(latmap, la) if latmap else float(la)
        out[tag] = dict(lat=la_g, lon=float(lo), share=s)
    d = 100 * (out['med']['share'] - out['brit']['share'])
    rows.append(dict(name=name, area=float(wg.sum()), **out, diff_points=d))
    print(f'{name}\n   land {wg.sum():,.0f} km2 | Catalan summit {100 * out["med"]["share"]:.4f}% at {out["med"]["lat"]:.2f}, {out["med"]["lon"]:.2f} | '
          f'Breton summit {100 * out["brit"]["share"]:.4f}% at {out["brit"]["lat"]:.2f}, {out["brit"]["lon"]:.2f} | Catalan - Breton = {d:+.4f} points = {d / 100 * wg.sum():+,.0f} km2', flush=True)
# every summit within 0.3 points, by the multi-start search
S = h.summits(h.area_weights(osm), tol=0.003)
print('summits within 0.3 points of the best (multi-start): ' + '; '.join(f'{100 * s["share"]:.4f}% at {s["lat"]:.2f}, {s["lon"]:.2f}' for s in S))
json.dump(rows, open(f'{odir}/osm_summits.json', 'w'), indent=1)
