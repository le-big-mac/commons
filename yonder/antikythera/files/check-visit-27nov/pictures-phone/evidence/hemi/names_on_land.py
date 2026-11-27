"""Does the middle of each place-name on the two maps stand on land or on sea, and how far from the coast?
The names' middles are taken from the programs (km east and north of the middle of the map), turned back into latitude and
longitude with my own inverse of the map's projection, and tested against the coastline file (parsed as JSON only).
usage: names_on_land.py WIDE.npz COAST.geojson"""
import sys, json, math
import numpy as np
from matplotlib.path import Path
R_KM = 6371.0088; KM = math.pi * R_KM / 180
Wz = np.load(sys.argv[1]); north, east, c0 = Wz['north'], Wz['east'], Wz['c_mid']
def fwd(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    v = np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], axis=-1)
    t = np.degrees(np.arccos(np.clip(v @ c0, -1, 1))); s = np.sin(np.radians(np.maximum(t, 1e-12)))
    return t * (v @ east) / s * KM, t * (v @ north) / s * KM, t
def inv(x, y):
    rho = math.hypot(x, y); t = math.radians(rho / KM)
    v = math.cos(t) * c0 + math.sin(t) * (east * x / rho + north * y / rho)
    return math.degrees(math.asin(v[2])), math.degrees(math.atan2(v[1], v[0]))
rings = []
for f in json.load(open(sys.argv[2], encoding='utf-8'))['features']:
    g = f['geometry']
    for poly in (g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]):
        outer = np.asarray(poly[0], dtype=float)[:, :2]
        x, y, t = fwd(outer[:, 1], outer[:, 0])
        if (t < 14).any(): rings.append((outer, np.column_stack([x, y]), t))
bx, by, _ = fwd(np.array([48.25]), np.array([-3.3])); cx, cy, _ = fwd(np.array([41.95]), np.array([1.2]))
bx, by, cx, cy = float(bx[0]), float(by[0]), float(cx[0]), float(cy[0])
NAMES = {'phone map': {'F R A N C E': (300, 130), 'S P A I N': (-430, -640), 'Bay of Biscay': (-560, 40), 'Mediterranean Sea': (520, -760), 'Brittany': (bx - 60, by + 75), 'Catalonia': (cx + 40, cy + 10)},
         'wide map': {'F R A N C E': (250, 180), 'S P A I N': (-430, -600), 'ITALY': (690, 150), 'ENGLAND': (-100, 830), 'Bay of Biscay': (-520, 60), 'Mediterranean Sea': (420, -700), 'Brittany': (bx, by), 'Catalonia': (cx, cy)}}
for m, names in NAMES.items():
    print(m)
    for name, (x, y) in names.items():
        lat, lon = inv(x, y)
        # land or sea: inside any outer ring (in latitude and longitude; the rings near the map do not cross the date line)
        on_land = any(Path(o).contains_point((lon, lat)) for o, p, t in rings)
        d = min(float(np.hypot(p[t < 14][:, 0] - x, p[t < 14][:, 1] - y).min()) for o, p, t in rings)
        print(f'  {name:18s} middle at ({x:+7.1f}, {y:+7.1f}) km = {lat:6.2f} N {lon:+7.2f} E: on {"land" if on_land else "SEA "}; nearest point of the coast file {d:5.1f} km away')
