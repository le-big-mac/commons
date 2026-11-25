"""Checker's own reader of the Horizons tables (data only). Caches arrays in check-scripts/cache.npz.
usage: python -I load.py DATADIR"""
import sys, os, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BODIES = ('sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn')
EPS = math.radians(84381.448 / 3600.0)      # IAU 1976 obliquity at J2000


def parse(path):
    jd, ra, de, lon, lat = [], [], [], [], []
    on = False
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.startswith('$$SOE'):
                on = True; continue
            if line.startswith('$$EOE'):
                break
            if not on: continue
            p = line.split(',')
            jd.append(float(p[0])); ra.append(float(p[3])); de.append(float(p[4])); lon.append(float(p[5])); lat.append(float(p[6]))
    return [np.array(x) for x in (jd, ra, de, lon, lat)]


def ecl_j2000(ra, de):
    """rotate the equatorial unit vector about x by the J2000 obliquity; return longitude, latitude in degrees"""
    ra, de = np.radians(ra), np.radians(de)
    x = np.cos(de) * np.cos(ra); y = np.cos(de) * np.sin(ra); z = np.sin(de)
    ye = y * math.cos(EPS) + z * math.sin(EPS)
    ze = -y * math.sin(EPS) + z * math.cos(EPS)
    return np.degrees(np.arctan2(ye, x)) % 360.0, np.degrees(np.arcsin(ze))


def load():
    z = np.load(os.path.join(HERE, 'cache.npz'))
    sky = {}
    for w in ('then', 'now'):
        sky[w] = {}
        for b in BODIES:
            sky[w][b] = {k: z[f'{w}_{b}_{k}'] for k in ('jd', 'S', 'latS', 'T', 'lat')}
    return sky


if __name__ == '__main__':
    D = sys.argv[1]
    out = {}
    for w in ('then', 'now'):
        for b in BODIES:
            jd, ra, de, lon, lat = parse(os.path.join(D, f'{b}_{w}.txt'))
            S, latS = ecl_j2000(ra, de)
            for k, v in (('jd', jd), ('S', S), ('latS', latS), ('T', lon % 360.0), ('lat', lat)):
                out[f'{w}_{b}_{k}'] = v
            step = np.diff(jd)
            print(f'{w:5s} {b:8s} rows {len(jd):6d} JD {jd[0]:.4f}..{jd[-1]:.4f} step min {step.min():.6f} max {step.max():.6f}  S-T first {((S[0]-lon[0]+180)%360-180):+.4f} last {((S[-1]-lon[-1]+180)%360-180):+.4f}')
    np.savez_compressed(os.path.join(HERE, 'cache.npz'), **out)
