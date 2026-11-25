"""The land hemisphere, the population hemisphere and the smallest cap holding half of humanity.

usage: hemi_run.py GRID_DIR OUT_DIR

GRID_DIR holds land10.npy, land50.npy, land110.npy, shelf10.npy (coverage fractions from raster.py) and pop005.npy
(people per cell from popgrid.py). Everything printed here is also written to OUT_DIR/results.json; the coarse maps
go to OUT_DIR/maps.npz for the figure. Scored against predictions-hemi.md by score_hemi.py, not here.
"""
import json
import os
import sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)   # helpers live beside this script; run with python -I
import hemilib as h

gdir, odir = sys.argv[1], sys.argv[2]
KM = np.pi * h.R_KM / 180     # km per degree of arc
NANTES = (47 + 13 / 60, -(1 + 32 / 60))
DUMET = (47 + 24 / 60 + 42 / 3600, -(2 + 37 / 60 + 15 / 3600))
TOKYO = (35.6895, 139.6917)
QUAH = (21.7, 99.4)
res = {}


def km_between(a, b):
    return float(h.angle_deg(h.unit(*a), h.unit(*b)) * KM)


def report(tag, r):
    print(f'{tag}: best share {100 * r["share"]:.4f}% at {r["lat"]:.3f}, {r["lon"]:.3f}')


# ---------- land, 1:10m, no ice shelves
print('== land, 1:10m, ice shelves not counted')
land = np.load(f'{gdir}/land10.npy')
wl = h.area_weights(land)
print(f'land area {wl.sum():,.0f} km2')
r10 = h.best_cap(wl)
report('land 10m', r10)
cstar = (r10['lat'], r10['lon'])
X, w, e = r10['X'], r10['w'], r10['eps']
L_star = h.share(X, w, r10['c'], e)
L_nantes = h.share(X, w, h.unit(*NANTES), e)
L_dumet = h.share(X, w, h.unit(*DUMET), e)
print(f'L(c*) {100 * L_star:.4f}%  L(Nantes) {100 * L_nantes:.4f}%  L(Ile Dumet) {100 * L_dumet:.4f}%')
print(f'c* is {km_between(cstar, NANTES):.1f} km from Nantes and {km_between(cstar, DUMET):.1f} km from Ile Dumet')
print(f'L(c*) - L(Nantes) = {100 * (L_star - L_nantes):.4f} percentage points; L(c*) - L(Dumet) = {100 * (L_star - L_dumet):.4f}')
# how flat: a grid of centres +-3 degrees around c*, every 0.05 degree
loc = h.Local(X, w, e, r10['c'], 4.5)
offs, G, north, east = loc.grid(3.0, 0.05)
DN, DE = np.meshgrid(offs, offs, indexing='ij')
dist = np.hypot(DN, DE) * KM
flat = {}
for tol in (0.001, 0.01, 0.05, 0.1):
    m = (G.max() - G) * 100 < tol
    touches = bool(m[0].any() or m[-1].any() or m[:, 0].any() or m[:, -1].any())
    flat[tol] = dict(max_km=float(dist[m].max()), area_km2=float(m.sum() * (0.05 * KM) ** 2), touches_edge=touches)
    print(f'  centres within {tol} percentage points of the best: up to {dist[m].max():.0f} km away, region of {m.sum() * (0.05 * KM) ** 2:,.0f} km2' + ('  (reaches the edge of the +-3 degree box)' if touches else ''))
res['land10'] = dict(lat=r10['lat'], lon=r10['lon'], share=L_star, area_km2=float(wl.sum()), L_nantes=L_nantes, L_dumet=L_dumet,
                     km_from_nantes=km_between(cstar, NANTES), km_from_dumet=km_between(cstar, DUMET), flat=flat)
maps = dict(land_lats=r10['coarse'][0], land_lons=r10['coarse'][1], land_S=r10['coarse'][2], flat_offs=offs, flat_G=G,
            flat_north=north, flat_east=east)

# ---------- variants
print('== land with the Antarctic ice shelves counted as land')
shelf = np.load(f'{gdir}/shelf10.npy')
overlap = h.area_weights(np.minimum(land, shelf)).sum()
print(f'ice shelves {h.area_weights(shelf).sum():,.0f} km2; overlap with the land polygons {overlap:,.0f} km2')
ws = h.area_weights(np.clip(land + shelf, 0, 1))
rs = h.best_cap(ws)
report('land + shelves', rs)
print(f'  moved {km_between(cstar, (rs["lat"], rs["lon"])):.3f} km from c*')
res['shelves'] = dict(lat=rs['lat'], lon=rs['lon'], share=rs['share'], km_from_cstar=km_between(cstar, (rs['lat'], rs['lon'])),
                      same_point=bool(rs['lat'] == r10['lat'] and rs['lon'] == r10['lon']), overlap_km2=float(overlap))
for name in ('land50', 'land110'):
    print(f'== {name}')
    g = h.area_weights(np.load(f'{gdir}/{name}.npy'))
    r = h.best_cap(g)
    report(name, r)
    print(f'  {km_between(cstar, (r["lat"], r["lon"])):.1f} km from c* (10m); the 10m land has {100 * h.share(X, w, r["c"], e):.4f}% in this hemisphere')
    res[name] = dict(lat=r['lat'], lon=r['lon'], share=r['share'], km_from_cstar=km_between(cstar, (r['lat'], r['lon'])), area_km2=float(g.sum()))
print('== land 10m on the equal-area (authalic) sphere of WGS84: a sensitivity check, not one of the expectations')
wa = h.area_weights(land, h.authalic)
ra = h.best_cap(wa, latmap=h.authalic)
# the centre is a point of the authalic sphere; turn its latitude back into a geodetic one
grid_lat = np.linspace(-90, 90, 180001)
geod = float(np.interp(ra['lat'], h.authalic(grid_lat), grid_lat))
report('land 10m, authalic', ra)
print(f'  land area on the ellipsoid {wa.sum():,.0f} km2; centre in geodetic latitude {geod:.3f}, {ra["lon"]:.3f}: {km_between(cstar, (geod, ra["lon"])):.1f} km from c*')
res['authalic'] = dict(lat_geodetic=geod, lon=ra['lon'], share=ra['share'], area_km2=float(wa.sum()), km_from_cstar=km_between(cstar, (geod, ra['lon'])))

# ---------- people
print('== people (GHS-POP, 2020, summed to 0.05 degree)')
pop = np.load(f'{gdir}/pop005.npy')
print(f'total {pop.sum():,.0f}')
rp = h.best_cap(pop)
report('people', rp)
Xp, wp, ep = rp['X'], rp['w'], rp['eps']
P_star = h.share(Xp, wp, r10['c'], ep)
P_nantes = h.share(Xp, wp, h.unit(*NANTES), ep)
print(f'people in the land hemisphere (centre c*): {100 * P_star:.3f}%; centred on Nantes: {100 * P_nantes:.3f}%')
print(f'land (10m) in the people hemisphere: {100 * h.share(X, w, rp["c"], e):.3f}%')
locp = h.Local(Xp, wp, ep, rp['c'], 4.5)
offp, Gp, northp, eastp = locp.grid(3.0, 0.1)
DNp, DEp = np.meshgrid(offp, offp, indexing='ij')
for tol in (0.01, 0.1):
    m = (Gp.max() - Gp) * 100 < tol
    print(f'  centres within {tol} percentage points of the best: up to {(np.hypot(DNp, DEp) * KM)[m].max():.0f} km away')
res['people'] = dict(lat=rp['lat'], lon=rp['lon'], share=rp['share'], total=float(pop.sum()), P_cstar=P_star, P_nantes=P_nantes,
                     land_share_in_it=h.share(X, w, rp['c'], e))
maps.update(pop_lats=rp['coarse'][0], pop_lons=rp['coarse'][1], pop_S=rp['coarse'][2])
# Tokyo and the boundary of the land hemisphere
t = float(h.angle_deg(r10['c'], h.unit(*TOKYO)))
print(f'Tokyo is {t:.3f} degrees from c*: {abs(t - 90) * KM:.0f} km {"inside" if t < 90 else "outside"} the land hemisphere')
res['tokyo'] = dict(angle_deg=t, km_from_boundary=abs(t - 90) * KM, inside=bool(t < 90))

# ---------- the smallest cap with half of the people
print('== smallest cap holding half of the people')
lo, hi = 20.0, 40.0
flo = h.best_cap(pop, r_deg=lo, verbose=False)['share']; fhi = h.best_cap(pop, r_deg=hi, verbose=False)['share']
print(f'  radius {lo} deg: best share {flo:.4f}; radius {hi} deg: best share {fhi:.4f}')
assert flo < 0.5 < fhi
trail = []
for _ in range(14):
    mid = (lo + hi) / 2
    r = h.best_cap(pop, r_deg=mid, verbose=False)
    trail.append((mid, r['share'], r['lat'], r['lon']))
    print(f'  radius {mid:.4f} deg = {mid * KM:.0f} km: best share {r["share"]:.5f} at {r["lat"]:.2f}, {r["lon"]:.2f}')
    if r['share'] >= 0.5:
        hi, rhalf = mid, r
    else:
        lo = mid
print(f'half of humanity fits in a cap of radius {hi:.3f} deg = {hi * KM:.0f} km centred at {rhalf["lat"]:.2f}, {rhalf["lon"]:.2f}, '
      f'{km_between((rhalf["lat"], rhalf["lon"]), QUAH):.0f} km from 21.7 N, 99.4 E')
res['half'] = dict(radius_deg=hi, radius_km=hi * KM, lat=rhalf['lat'], lon=rhalf['lon'], share=rhalf['share'],
                   km_from_quah=km_between((rhalf['lat'], rhalf['lon']), QUAH), trail=trail)
json.dump(res, open(f'{odir}/results.json', 'w'), indent=1)
np.savez_compressed(f'{odir}/maps.npz', **maps)
print('written', f'{odir}/results.json')
