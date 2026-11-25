"""GSHHG land and lake-water rasters again, after the third review.

usage: gshhg_fix.py GSHHG_DIR GRID_DIR

The reviewer found two faults in which levels I had selected (the reader itself was right):
 1. Levels 1 and 6 alone leave out the islands off Antarctica that GSHHG files under level 5 only (Adelaide, James
    Ross, Anvers, ...). Land = level 1 + level 6 + every level-5 polygon except the ice-front mainland (the one
    running from -180 to +180).
 2. "Lakes as water" must subtract lakes (level 2) but keep islands in lakes (level 3) and subtract ponds on them
    (level 4): an even-odd fill of levels 2, 3 and 4 together is exactly the water.
Writes gshhg_<r>2.npy (land) and gshhg_<r>_water.npy for r = i, h, and prints areas and an overlap check.
"""
import json
import os
import subprocess
import sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gshhg_read as g
import hemilib as h

gdir, odir = sys.argv[1], sys.argv[2]


def write(polys, path):
    feats = []
    for p in polys:
        lon, lat = p['lon'], p['lat']
        closed = lon[0] == lon[-1] and lat[0] == lat[-1]
        if not closed and lon.min() <= -179.99 and lon.max() >= 179.99:
            a, b = (lon[-1], lat[-1]), (lon[0], lat[0])
            lon = np.concatenate([lon, [a[0], b[0], b[0]]]); lat = np.concatenate([lat, [-90.0, -90.0, b[1]]])
        rings = [np.column_stack([lon, lat])]
        if lon.max() > 180:
            rings.append(np.column_stack([lon - 360, lat]))
        if lon.min() < -180:
            rings.append(np.column_stack([lon + 360, lat]))
        for r in rings:
            feats.append(dict(type='Feature', properties=dict(featurecla='x', level=int(p['level']), id=int(p['id'])), geometry=dict(type='Polygon', coordinates=[r.tolist()])))
    json.dump(dict(type='FeatureCollection', features=feats), open(path, 'w'))
    return len(feats)


def raster(src, dst):
    r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'raster.py'), src, dst, '0.01', '5'], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return np.load(dst)


for res in ('i', 'h'):
    P = list(g.polygons(f'{gdir}/gshhs_{res}.b'))
    main5 = [p for p in P if p['level'] == 5 and p['lon'].min() <= -179.99 and p['lon'].max() >= 179.99]
    assert len(main5) == 1
    isl5 = [p for p in P if p['level'] == 5 and p is not main5[0]]
    base = [p for p in P if p['level'] in (1, 6)]
    n1 = write(base, f'{odir}/_tmp_base.geojson'); n2 = write(isl5, f'{odir}/_tmp_isl5.geojson')
    a = raster(f'{odir}/_tmp_base.geojson', f'{odir}/_tmp_base.npy')
    b = raster(f'{odir}/_tmp_isl5.geojson', f'{odir}/_tmp_isl5.npy')
    both = h.area_weights(np.maximum(a + b - 1, 0)).sum()
    land = np.clip(a + b, 0, 1)
    np.save(f'{odir}/gshhg_{res}2.npy', land.astype(np.float32))
    nw = write([p for p in P if p['level'] in (2, 3, 4)], f'{odir}/_tmp_water.geojson')
    w = raster(f'{odir}/_tmp_water.geojson', f'{odir}/gshhg_{res}_water.npy')
    print(f'{res}: levels 1 and 6: {h.area_weights(a).sum():,.0f} km2; level-5 islands ({len(isl5)} polygons): {h.area_weights(b).sum():,.0f} km2; '
          f'overlap of the two at most {both:,.0f} km2; land {h.area_weights(land).sum():,.0f} km2; lake water (levels 2-3+4) {h.area_weights(w).sum():,.0f} km2; '
          f'land less lake water {h.area_weights(np.clip(land - w, 0, 1)).sum():,.0f} km2')
    for f in ('_tmp_base.geojson', '_tmp_isl5.geojson', '_tmp_water.geojson', '_tmp_base.npy', '_tmp_isl5.npy'):
        os.remove(f'{odir}/{f}')
