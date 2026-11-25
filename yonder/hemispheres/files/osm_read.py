"""Read OpenStreetMap's simplified land polygons (ESRI shapefile, Web Mercator) and write them as GeoJSON in
longitude and latitude, for raster.py.

usage: osm_read.py IN.shp OUT.geojson

Shapefile: a 100-byte header, then records (8-byte big-endian header; little-endian shape type 5 = polygon, bounding
box, number of parts and of points, part offsets, points as pairs of doubles).  Web Mercator (EPSG:3857) to degrees:
lon = x / R, lat = atan(sinh(y / R)), R = 6378137 m.  The projection stops at latitude 85.0511; the data are cut
there, so Antarctica south of it is missing and has to be added by whoever uses the result.
"""
import json
import math
import struct
import sys
import numpy as np

R = 6378137.0
data = open(sys.argv[1], 'rb').read()
assert struct.unpack('>i', data[0:4])[0] == 9994
shape_type = struct.unpack('<i', data[32:36])[0]
assert shape_type == 5, shape_type
pos = 100
feats = []
nrec = nring = npts = 0
xmin = ymin = 1e30; xmax = ymax = -1e30
while pos < len(data):
    num, length = struct.unpack('>2i', data[pos:pos + 8]); pos += 8
    rec = data[pos:pos + 2 * length]; pos += 2 * length
    st = struct.unpack('<i', rec[0:4])[0]
    if st == 0:
        continue
    assert st == 5
    nparts, npoints = struct.unpack('<2i', rec[36:44])
    parts = struct.unpack(f'<{nparts}i', rec[44:44 + 4 * nparts])
    pts = np.frombuffer(rec, dtype='<f8', count=2 * npoints, offset=44 + 4 * nparts).reshape(npoints, 2)
    lon = np.degrees(pts[:, 0] / R)
    lat = np.degrees(np.arctan(np.sinh(pts[:, 1] / R)))
    xmin = min(xmin, lon.min()); xmax = max(xmax, lon.max()); ymin = min(ymin, lat.min()); ymax = max(ymax, lat.max())
    rings = []
    for k in range(nparts):
        a = parts[k]; b = parts[k + 1] if k + 1 < nparts else npoints
        rings.append(np.column_stack([lon[a:b], lat[a:b]]).round(7).tolist())
        nring += 1; npts += b - a
    feats.append(dict(type='Feature', properties=dict(featurecla='Land'), geometry=dict(type='Polygon', coordinates=rings)))
    nrec += 1
json.dump(dict(type='FeatureCollection', features=feats), open(sys.argv[2], 'w'))
print(f'{nrec} polygons, {nring} rings, {npts} points; longitude {xmin:.4f} to {xmax:.4f}, latitude {ymin:.4f} to {ymax:.4f}')
