"""Rasterise polygons given in longitude/latitude (GeoJSON) to fractional coverage on a regular grid.

usage: raster.py GEOJSON OUT.npy [FINE_DEG=0.01] [BLOCK=5] [--skip CLASS]...

Method. Every ring of every polygon is taken together and filled by the even-odd rule, sampled at the centres of
a fine grid (FINE_DEG), with polygon edges taken as straight lines in the longitude-latitude plane. The 0/1 result
is then averaged over BLOCK x BLOCK fine cells, giving the covered fraction of each coarse cell (float32).
Row 0 of the output is the southernmost band; column 0 starts at longitude -180.

Even-odd over all rings at once is right when rings are either disjoint or properly nested (holes, islands in
holes). It would be wrong for two overlapping polygons, so the script reports the total area for a sanity check.
Features whose property `featurecla` is given with --skip are left out.
"""
import json
import sys
import numpy as np


def rings(path, skip):
    d = json.load(open(path, encoding='utf-8'))
    n = 0
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
                n += 1
                yield a


def rasterise(path, d, block, skip):
    H = round(180 / d)
    W = round(360 / d)
    assert H % block == 0 and W % block == 0
    x1, y1, x2, y2 = [], [], [], []
    for a in rings(path, skip):
        x1.append(a[:-1, 0]); y1.append(a[:-1, 1]); x2.append(a[1:, 0]); y2.append(a[1:, 1])
    x1, y1, x2, y2 = (np.concatenate(v) for v in (x1, y1, x2, y2))
    ymin = np.minimum(y1, y2)
    ymax = np.maximum(y1, y2)
    # rows r whose centre latitude yc = -90 + (r + 0.5) d satisfies ymin <= yc < ymax
    r_lo = np.clip(np.ceil((ymin + 90) / d - 0.5).astype(np.int64), 0, H)
    r_hi = np.clip(np.ceil((ymax + 90) / d - 0.5).astype(np.int64), 0, H)
    n = np.maximum(r_hi - r_lo, 0)
    total = int(n.sum())
    idx = np.repeat(np.arange(len(n)), n)
    offs = np.arange(total) - np.repeat(np.cumsum(n) - n, n)
    rows = r_lo[idx] + offs
    yc = -90 + (rows + 0.5) * d
    x = x1[idx] + (yc - y1[idx]) * (x2[idx] - x1[idx]) / (y2[idx] - y1[idx])
    # the crossing toggles every cell whose centre longitude is >= x
    cols = np.clip(np.ceil((x + 180) / d - 0.5).astype(np.int64), 0, W)
    order = np.argsort(rows, kind='stable')
    rows = rows[order]; cols = cols[order]
    out = np.zeros((H // block, W // block), dtype=np.float32)
    chunk = block * 200
    for r0 in range(0, H, chunk):
        a = np.searchsorted(rows, r0, side='left')
        b = np.searchsorted(rows, r0 + chunk, side='left')
        flat = (rows[a:b] - r0) * (W + 1) + cols[a:b]
        cnt = np.bincount(flat, minlength=chunk * (W + 1)).reshape(chunk, W + 1)
        par = (cnt & 1).astype(np.uint8)
        inside = np.bitwise_xor.accumulate(par, axis=1)[:, :W]
        assert not par.sum(axis=1).astype(np.int64).__and__(1).any(), 'odd number of crossings in a row'
        out[r0 // block:(r0 + chunk) // block] = inside.reshape(chunk // block, block, W // block, block).mean(axis=(1, 3))
    return out, len(n), total


def main():
    args = sys.argv[1:]
    skip = set()
    while '--skip' in args:
        i = args.index('--skip')
        skip.add(args[i + 1])
        del args[i:i + 2]
    path, outp = args[0], args[1]
    d = float(args[2]) if len(args) > 2 else 0.01
    block = int(args[3]) if len(args) > 3 else 5
    cov, nedges, ncross = rasterise(path, d, block, skip)
    np.save(outp, cov)
    H, W = cov.shape
    lat = -90 + (np.arange(H) + 0.5) * (180 / H)
    R = 6371.0088
    cell = (np.pi / H) * (2 * np.pi / W) * R * R * np.cos(np.radians(lat))
    area = float((cov.sum(axis=1, dtype=np.float64) * cell).sum())
    print(f'{path.split("/")[-1]}: edges {nedges}, crossings {ncross}, grid {H}x{W}, skipped {sorted(skip)}')
    print(f'  area on a sphere of radius {R} km: {area:,.0f} km2 = {100 * area / (4 * np.pi * R * R):.3f}% of the sphere')


if __name__ == '__main__':
    main()
