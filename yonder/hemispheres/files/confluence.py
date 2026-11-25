"""Which whole-degree points of latitude and longitude lie on land? Exact point-in-polygon, even-odd rule.

usage: confluence.py GEOJSON [OUT.npy] [--skip CLASS]... [--also GEOJSON2]

The 64,442 points: latitudes -89..89 with longitudes -180..179, and the two poles once each. Each point is tested
1e-9 degree north-east of itself, so that a point lying exactly on an edge (the cuts at longitude +-180, for one)
falls on a definite side; the poles are tested 1e-6 degree inside. With --also, a point counts if it is in either
set of polygons (used for the Antarctic ice shelves).
"""
import json
import sys
import numpy as np


def edges(path, skip):
    d = json.load(open(path, encoding='utf-8'))
    X1, Y1, X2, Y2 = [], [], [], []
    for f in d['features']:
        if str(f['properties'].get('featurecla')) in skip:
            continue
        g = f['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in polys:
            for ring in poly:
                a = np.asarray(ring, dtype=np.float64)[:, :2]
                if not np.array_equal(a[0], a[-1]):
                    a = np.vstack([a, a[:1]])
                X1.append(a[:-1, 0]); Y1.append(a[:-1, 1]); X2.append(a[1:, 0]); Y2.append(a[1:, 1])
    return tuple(np.concatenate(v) for v in (X1, Y1, X2, Y2))


def inside(E, lat, lons):
    """Even-odd test of the points (lat, lon) for lon in lons (sorted)."""
    x1, y1, x2, y2 = E
    m = (np.minimum(y1, y2) <= lat) & (lat < np.maximum(y1, y2))
    xc = np.sort(x1[m] + (lat - y1[m]) * (x2[m] - x1[m]) / (y2[m] - y1[m]))
    return (np.searchsorted(xc, lons, side='left') % 2) == 1   # crossings strictly west of the point


def table(E):
    eps = 1e-9
    lons = np.arange(-180, 180) + eps
    T = np.zeros((179, 360), dtype=bool)
    for k, la in enumerate(range(-89, 90)):
        T[k] = inside(E, la + eps, lons)
    south = bool(inside(E, -90 + 1e-6, np.array([0.0]))[0])
    north = bool(inside(E, 90 - 1e-6, np.array([0.0]))[0])
    return T, south, north


def main():
    args = sys.argv[1:]
    skip = set(); also = None
    while '--skip' in args:
        i = args.index('--skip'); skip.add(args[i + 1]); del args[i:i + 2]
    if '--also' in args:
        i = args.index('--also'); also = args[i + 1]; del args[i:i + 2]
    T, s, n = table(edges(args[0], skip))
    if also:
        T2, s2, n2 = table(edges(also, set()))
        both = int((T & T2).sum())
        T = T | T2; s = s or s2; n = n or n2
        print(f'points in both sets of polygons: {both}')
    total = T.size + 2
    on = int(T.sum()) + int(s) + int(n)
    lat = np.arange(-89, 90)
    print(f'points {total}; on land {on} ({100 * on / total:.2f}%); south pole {"land" if s else "not land"}, north pole {"land" if n else "not land"}')
    print(f'  on land south of 60 S (pole included): {int(T[lat < -60].sum()) + int(s)}; elsewhere: {int(T[lat >= -60].sum()) + int(n)}')
    print(f'  on land at (0, 0): {bool(T[89, 180])}')
    if len(args) > 1:
        np.save(args[1], T)


if __name__ == '__main__':
    main()
