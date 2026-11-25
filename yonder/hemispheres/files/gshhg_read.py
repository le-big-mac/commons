"""Read a GSHHG binary shoreline file (version 2.x) and write chosen levels as GeoJSON polygons in [-180, 180].

usage: gshhg_read.py IN.b OUT.geojson LEVEL [LEVEL ...]      (or: gshhg_read.py IN.b --list)

Format (gshhs.h of GSHHG 2.3.7): for each polygon a header of eleven big-endian 32-bit integers
(id, n, flag, west, east, south, north, area, area_full, container, ancestor), then n points (x, y) as 32-bit
integers in micro-degrees. level = flag & 255 (1 land, 2 lake, 3 island in lake, 4 pond, 5 Antarctic ice front,
6 Antarctic grounding line); greenwich = (flag >> 16) & 3.
Longitudes are stored in 0..360. As in gshhs.c, 360 is subtracted from a point's longitude when the polygon lies
wholly west of Greenwich (west > 180), or when it crosses Greenwich and the point is east of 270 (first polygon,
Eurasia and Africa) or of 180 (the others). A polygon then reaching past +180 is written a second time moved by
-360, so that a rasteriser that clips at +-180 sees both parts. A polygon that runs from -180 to +180 without
closing (Antarctica) is closed through the South Pole.
"""
import json
import struct
import sys
import numpy as np


def polygons(path):
    with open(path, 'rb') as f:
        data = f.read()
    pos = 0
    first = True
    while pos < len(data):
        pid, n, flag, west, east, south, north, area, area_full, container, ancestor = struct.unpack('>11i', data[pos:pos + 44])
        pos += 44
        pts = np.frombuffer(data, dtype='>i4', count=2 * n, offset=pos).reshape(n, 2).astype(np.float64) * 1e-6
        pos += 8 * n
        level = flag & 255
        greenwich = (flag >> 16) & 3
        lon = pts[:, 0].copy(); lat = pts[:, 1]
        max_east = 270.0 if first else 180.0
        first = False
        if west * 1e-6 > 180:
            lon -= 360
        elif greenwich & 1:
            lon[lon > max_east] -= 360
        yield dict(id=pid, n=n, level=level, greenwich=greenwich, west=west * 1e-6, east=east * 1e-6, south=south * 1e-6, north=north * 1e-6,
                   lon=lon, lat=lat)


def main():
    path = sys.argv[1]
    if sys.argv[2] == '--list':
        counts = {}
        for k, p in enumerate(polygons(path)):
            counts[p['level']] = counts.get(p['level'], 0) + 1
            if k < 6 or p['level'] >= 5 and counts[p['level']] <= 2:
                closed = p['lon'][0] == p['lon'][-1] and p['lat'][0] == p['lat'][-1]
                print(f"id {p['id']} level {p['level']} n {p['n']} greenwich {p['greenwich']} header W/E/S/N {p['west']:.3f} {p['east']:.3f} {p['south']:.3f} {p['north']:.3f} | "
                      f"lon {p['lon'].min():.3f}..{p['lon'].max():.3f} lat {p['lat'].min():.3f}..{p['lat'].max():.3f} closed {closed} "
                      f"first ({p['lon'][0]:.4f}, {p['lat'][0]:.4f}) last ({p['lon'][-1]:.4f}, {p['lat'][-1]:.4f}) largest jump in lon {np.abs(np.diff(p['lon'])).max():.3f}")
        print('polygons per level', dict(sorted(counts.items())))
        return
    outp = sys.argv[2]
    levels = {int(v) for v in sys.argv[3:]}
    feats = []
    notes = []
    for p in polygons(path):
        if p['level'] not in levels:
            continue
        lon, lat = p['lon'], p['lat']
        closed = lon[0] == lon[-1] and lat[0] == lat[-1]
        assert np.abs(np.diff(lon)).max() < 180, f"polygon {p['id']}: a jump of {np.abs(np.diff(lon)).max():.1f} degrees in longitude"
        if not closed and lon.min() <= -179.99 and lon.max() >= 179.99:
            # an open line right round the pole: close it through the South Pole
            a, b = (lon[-1], lat[-1]), (lon[0], lat[0])
            lon = np.concatenate([lon, [a[0], b[0], b[0]]]); lat = np.concatenate([lat, [-90.0, -90.0, b[1]]])
            notes.append(f"polygon {p['id']} (level {p['level']}) closed through the South Pole")
        else:
            assert closed, f"polygon {p['id']} is not closed"
        rings = [np.column_stack([lon, lat])]
        if lon.max() > 180:
            rings.append(np.column_stack([lon - 360, lat]))
            notes.append(f"polygon {p['id']} reaches {lon.max():.2f} E: also written moved by -360")
        if lon.min() < -180:
            rings.append(np.column_stack([lon + 360, lat]))
            notes.append(f"polygon {p['id']} reaches {lon.min():.2f}: also written moved by +360")
        for r in rings:
            feats.append(dict(type='Feature', properties=dict(featurecla='Land', level=int(p['level']), id=int(p['id'])),
                              geometry=dict(type='Polygon', coordinates=[r.tolist()])))
    json.dump(dict(type='FeatureCollection', features=feats), open(outp, 'w'))
    print(f'{len(feats)} rings written for levels {sorted(levels)}')
    for n in notes:
        print(' ', n)


if __name__ == '__main__':
    main()
