"""Tests of raster.py and hemilib.py on cases whose answer is known, run before any real number was computed.

usage: test_hemi.py SCRATCH_DIR
"""
import json
import os
import subprocess
import sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)   # the helpers live beside this script; run with python -I
import hemilib as h

scratch = sys.argv[1]
rng = np.random.default_rng(20261121)
ok = True


def check(name, cond, detail=''):
    global ok
    ok = ok and bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name + (': ' + detail if detail else ''))


def write_geojson(path, ringsets):
    feats = [dict(type='Feature', properties=dict(featurecla='Land'), geometry=dict(type='Polygon', coordinates=rs)) for rs in ringsets]
    json.dump(dict(type='FeatureCollection', features=feats), open(path, 'w'))


def raster(path, out, fine=0.01, block=5):
    r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'raster.py'), path, out, str(fine), str(block)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return np.load(out)


# 1. a longitude-latitude rectangle with a rectangular hole: area known in closed form
rect = [[-20.003, 10.002], [35.007, 10.002], [35.007, 61.004], [-20.003, 61.004], [-20.003, 10.002]]
hole = [[0.001, 20.003], [0.001, 30.006], [12.004, 30.006], [12.004, 20.003], [0.001, 20.003]]
write_geojson(f'{scratch}/rect.geojson', [[rect, hole]])
cov = raster(f'{scratch}/rect.geojson', f'{scratch}/rect.npy')
A = h.area_weights(cov).sum()
exact = h.R_KM ** 2 * (np.radians(55.010) * (np.sin(np.radians(61.004)) - np.sin(np.radians(10.002)))
                       - np.radians(12.003) * (np.sin(np.radians(30.006)) - np.sin(np.radians(20.003))))
check('rectangle with hole, area', abs(A / exact - 1) < 2e-4, f'raster {A:,.0f} km2, exact {exact:,.0f} km2, ratio {A / exact:.6f}')

# 2. a triangle with slanted edges, compared with the planar (lon-lat) integral of cos(lat)
tri = [[-100.0, -40.0], [-30.0, -55.0], [-60.0, 20.0], [-100.0, -40.0]]
write_geojson(f'{scratch}/tri.geojson', [[tri]])
cov = raster(f'{scratch}/tri.geojson', f'{scratch}/tri.npy')
A = h.area_weights(cov).sum()
pts = np.column_stack([rng.uniform(-100, -30, 4_000_000), rng.uniform(-55, 20, 4_000_000)])


def in_tri(p, t):
    def side(a, b):
        return (b[0] - a[0]) * (p[:, 1] - a[1]) - (b[1] - a[1]) * (p[:, 0] - a[0])
    s1, s2, s3 = side(t[0], t[1]), side(t[1], t[2]), side(t[2], t[0])
    return ((s1 >= 0) & (s2 >= 0) & (s3 >= 0)) | ((s1 <= 0) & (s2 <= 0) & (s3 <= 0))


inside = in_tri(pts, tri)
mc = h.R_KM ** 2 * np.radians(70) * np.radians(75) * np.mean(inside * np.cos(np.radians(pts[:, 1])))
check('triangle, area against Monte Carlo', abs(A / mc - 1) < 3e-3, f'raster {A:,.0f}, Monte Carlo {mc:,.0f}, ratio {A / mc:.5f}')

# 3. share() against the closed form for a cap-shaped "continent" drawn on the weight grid directly
H, W = 1800, 3600
lat = -90 + (np.arange(H) + 0.5) * 0.1
lon = -180 + (np.arange(W) + 0.5) * 0.1
LA, LO = np.meshgrid(lat, lon, indexing='ij')
V = h.unit(LA, LO)
p = h.unit(33.0, 71.0)
cap = (V @ p > np.cos(np.radians(40.0))).astype(np.float64)   # continent: cap of radius 40 deg
wg = h.area_weights(cap)
X, w, eps = h.cells(wg)
check('cap continent, area', abs(w.sum() / (2 * np.pi * h.R_KM ** 2 * (1 - np.cos(np.radians(40)))) - 1) < 1e-3,
      f'ratio {w.sum() / (2 * np.pi * h.R_KM ** 2 * (1 - np.cos(np.radians(40)))):.6f}')
# share within 90 deg of a centre at distance t from p: Monte Carlo with exact tests
U = rng.normal(size=(3_000_000, 3)); U /= np.linalg.norm(U, axis=1)[:, None]
incap = U @ p > np.cos(np.radians(40.0))
worst = 0
for t in (0, 30, 50, 60, 75, 90, 110, 130, 150):
    c = h.unit(33.0 - t, 71.0) if 33.0 - t >= -90 else h.unit(-180 - (33.0 - t), 71.0 - 180)
    s = h.share(X, w, c, eps)
    mc = np.mean(incap & (U @ c > 0)) / np.mean(incap)
    worst = max(worst, abs(s - mc))
check('cap continent, hemisphere shares at 9 distances against Monte Carlo', worst < 2e-3, f'largest difference {worst:.5f}')
for r in (20.0, 55.0, 120.0):
    c = h.unit(10.0, 40.0)
    s = h.share(X, w, c, eps, r)
    mc = np.mean(incap & (U @ c > np.cos(np.radians(r)))) / np.mean(incap)
    check(f'cap continent, share within {r} deg', abs(s - mc) < 2e-3, f'{s:.5f} against {mc:.5f}')

# 4. best_cap(): two unequal blobs 100 deg apart plus a third; the answer by brute force on random centres
wg2 = h.area_weights(((V @ h.unit(10, 20) > np.cos(np.radians(25))) | (V @ h.unit(-30, 120) > np.cos(np.radians(35)))
                      | (V @ h.unit(60, -120) > np.cos(np.radians(15)))).astype(np.float64))
res = h.best_cap(wg2, verbose=False)
X2, w2, e2 = h.cells(wg2)
cands = rng.normal(size=(4000, 3)); cands /= np.linalg.norm(cands, axis=1)[:, None]
brute = max(h.share(X2, w2, c, e2) for c in cands)
check('best hemisphere of three blobs is at least as good as 4,000 random centres', res['share'] >= brute - 1e-6, f"best_cap {res['share']:.5f} at {res['lat']:.2f}, {res['lon']:.2f}; random best {brute:.5f}")
check('share + share of the antipode = 1', abs(h.share(X2, w2, res['c'], e2) + h.share(X2, w2, -res['c'], e2) - 1) < 1e-6)

# 5. best_cap with a radius: point masses; the smallest cap holding two equal masses 40 deg apart is centred between them
pg = np.zeros((1800, 3600)); pg[900 + 100, 1800 + 300] = 1.0; pg[900 + 100, 1800 + 700] = 1.0; pg[300, 500] = 1.5
res = h.best_cap(pg, r_deg=22.0, verbose=False)
la1, lo1 = lat[1000], lon[2100]; la2, lo2 = lat[1000], lon[2500]
mid = h.unit(la1, lo1) + h.unit(la2, lo2); mid /= np.linalg.norm(mid)
sep = h.angle_deg(h.unit(la1, lo1), h.unit(la2, lo2))
d1 = h.angle_deg(res['c'], h.unit(la1, lo1)); d2 = h.angle_deg(res['c'], h.unit(la2, lo2))
# (first version of this test asked for the centre within 22 - sep/2 of the midpoint, which is the extent of the set of
#  valid centres ALONG the line joining the masses only; the right criterion is that both masses are inside the cap)
check('cap of radius 22 deg finds the pair of point masses', abs(res['share'] - 2 / 3.5) < 1e-6 and max(d1, d2) < 22 + 0.06,
      f"share {res['share']:.4f}, centre {d1:.2f} and {d2:.2f} deg from the two masses, which are {sep:.2f} deg apart")
res = h.best_cap(pg, r_deg=15.0, verbose=False)
check('cap of radius 15 deg takes the single larger mass', abs(res['share'] - 1.5 / 3.5) < 1e-6, f"share {res['share']:.4f} at {res['lat']:.2f}, {res['lon']:.2f}")

# 6. Local agrees with share
loc = h.Local(X2, w2, e2, h.unit(12, 34), 3.0)
c = h.unit(13.1, 35.9)
check('Local.share equals share', abs(loc.share(c) - h.share(X2, w2, c, e2)) < 1e-7, f'{loc.share(c):.8f} against {h.share(X2, w2, c, e2):.8f}')
print('ALL PASS' if ok else 'SOME FAILED')
