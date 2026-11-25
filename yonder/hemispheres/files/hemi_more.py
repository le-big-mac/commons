"""Follow-up questions raised by the first run; none of this is scored against the sealed expectations.

usage: hemi_more.py GRID_DIR OUT_DIR

 1. a wide map of the land share around western Europe (does a second, lower summit exist near Brittany?)
 2. hill-climbs from Nantes and from Ile Dumet
 3. the land hemisphere when lakes are counted as water
 4. Tokyo and people, for a hemisphere centred on Nantes
 5. the half-of-humanity cap: a fine map of centres at the radius found and just below it; the smallest radius for a
    cap centred on 21.7 N, 99.4 E
 6. who is left out of the hemisphere with most people
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
res = json.load(open(f'{odir}/results.json'))
NANTES = (47 + 13 / 60, -(1 + 32 / 60))
DUMET = (47 + 24 / 60 + 42 / 3600, -(2 + 37 / 60 + 15 / 3600))
TOKYO = (35.6895, 139.6917)
QUAH = (21.7, 99.4)
more = {}
land = np.load(f'{gdir}/land10.npy')
X, w, e = h.cells(h.area_weights(land))
cstar = (res['land10']['lat'], res['land10']['lon'])

print('== 1. wide map: +-8 degrees around 44.5 N, 0.5 E, every 0.1 degree')
c_mid = h.unit(44.5, 0.5)
loc = h.Local(X, w, e, c_mid, 12.0)
offs, G, north, east = loc.grid(8.0, 0.1)
a, b = np.unravel_index(np.nanargmax(G), G.shape)
la, lo = h.latlon(loc.point(offs[a], offs[b], north, east))
print(f'  best on this grid {100 * G[a, b]:.4f}% at {la:.2f}, {lo:.2f}')
# local maxima of the grid (strictly greater than the 8 neighbours)
core = G[1:-1, 1:-1]
ismax = np.ones_like(core, dtype=bool)
for da in (-1, 0, 1):
    for db in (-1, 0, 1):
        if da or db:
            ismax &= core > G[1 + da:G.shape[0] - 1 + da, 1 + db:G.shape[1] - 1 + db]
peaks = []
for i, j in np.argwhere(ismax):
    pla, plo = h.latlon(loc.point(offs[i + 1], offs[j + 1], north, east))
    peaks.append((float(core[i, j]), float(pla), float(plo)))
peaks.sort(reverse=True)
for s, pla, plo in peaks[:8]:
    print(f'  local summit {100 * s:.4f}% at {pla:.2f}, {plo:.2f} ({100 * (G[a, b] - s):.4f} points below the best)')
more['wide'] = dict(peaks=peaks[:20])
np.savez_compressed(f'{odir}/wide.npz', offs=offs, G=G, north=north, east=east, c_mid=c_mid)

print('== 2. hill-climbs')
for name, start in (('Nantes', NANTES), ('Ile Dumet', DUMET)):
    c = h.unit(*start)
    for it in range(200):
        lc = h.Local(X, w, e, c, 0.5)
        o, g, n_, e_ = lc.grid(0.3, 0.05)
        i, j = np.unravel_index(np.nanargmax(g), g.shape)
        if o[i] == 0 and o[j] == 0:
            break
        c = lc.point(o[i], o[j], n_, e_)
    la, lo = h.latlon(c)
    s = h.share(X, w, c, e)
    print(f'  from {name}: {it} steps of at most 0.3 degree, stops at {la:.2f}, {lo:.2f} with {100 * s:.4f}%, '
          f'{h.angle_deg(c, h.unit(*start)) * KM:.0f} km from the start and {h.angle_deg(c, h.unit(*cstar)) * KM:.0f} km from c*')
    more[f'climb_{name}'] = dict(lat=float(la), lon=float(lo), share=s, steps=it)

print('== 3. lakes counted as water')
lakes = np.load(f'{gdir}/lakes10.npy')
wl = h.area_weights(np.clip(land - lakes, 0, 1))
print(f'  land less lakes: {wl.sum():,.0f} km2')
r = h.best_cap(wl)
print(f'  best {100 * r["share"]:.4f}% at {r["lat"]:.3f}, {r["lon"]:.3f}: {h.angle_deg(r["c"], h.unit(*cstar)) * KM:.1f} km from c*')
more['lakes'] = dict(lat=r['lat'], lon=r['lon'], share=r['share'], area=float(wl.sum()))

print('== 4. a hemisphere centred on Nantes')
t = float(h.angle_deg(h.unit(*NANTES), h.unit(*TOKYO)))
print(f'  Tokyo is {t:.3f} degrees from Nantes: {abs(t - 90) * KM:.0f} km {"inside" if t < 90 else "outside"} that hemisphere')
more['tokyo_nantes'] = dict(angle=t, km=abs(t - 90) * KM)

print('== 5. the half-of-humanity cap')
pop = np.load(f'{gdir}/pop005.npy')
Xp, wp, ep = h.cells(pop)
rad = res['half']['radius_deg']
lats = np.arange(12, 36.01, 0.25); lons = np.arange(90, 112.01, 0.25)
for rr in (rad, rad - 0.1):
    S = np.array([[h.share(Xp, wp, h.unit(la, lo), ep, rr) for lo in lons] for la in lats])
    i, j = np.unravel_index(np.argmax(S), S.shape)
    print(f'  radius {rr:.3f} deg ({rr * KM:.0f} km): best of {S.size} centres every 0.25 degree in 12-36 N, 90-112 E: {S[i, j]:.5f} at {lats[i]:.2f}, {lons[j]:.2f}')
    core = S[1:-1, 1:-1]
    ismax = np.ones_like(core, dtype=bool)
    for da in (-1, 0, 1):
        for db in (-1, 0, 1):
            if da or db:
                ismax &= core >= S[1 + da:S.shape[0] - 1 + da, 1 + db:S.shape[1] - 1 + db]
    pk = sorted(((float(core[i, j]), float(lats[i + 1]), float(lons[j + 1])) for i, j in np.argwhere(ismax)), reverse=True)[:5]
    for s, pla, plo in pk:
        print(f'    summit {s:.5f} at {pla:.2f}, {plo:.2f}')
    if rr == rad:
        np.savez_compressed(f'{odir}/halfmap.npz', lats=lats, lons=lons, S=S, radius=rad)
        more['half_summits'] = pk
lo_r, hi_r = 20.0, 45.0
cq = h.unit(*QUAH)
for _ in range(40):
    mid = (lo_r + hi_r) / 2
    if h.share(Xp, wp, cq, ep, mid) >= 0.5:
        hi_r = mid
    else:
        lo_r = mid
print(f'  a cap centred on 21.7 N, 99.4 E needs a radius of {hi_r:.3f} deg = {hi_r * KM:.0f} km to hold half; with 3,300 km it holds {100 * h.share(Xp, wp, cq, ep, 3300 / KM):.2f}%')
more['quah'] = dict(radius_deg=hi_r, radius_km=hi_r * KM, share_3300=h.share(Xp, wp, cq, ep, 3300 / KM))

print('== 6. who is outside the hemisphere with most people')
cp = h.unit(res['people']['lat'], res['people']['lon'])
H, W = pop.shape
lat = -90 + (np.arange(H) + 0.5) * 180 / H; lon = -180 + (np.arange(W) + 0.5) * 360 / W
LA, LO = np.meshgrid(lat, lon, indexing='ij')
inside = (h.unit(LA, LO) @ cp) > 0
tot = pop.sum()
boxes = {'the Americas (170 W to 30 W)': (LO > -170) & (LO < -30),
         'Africa and Europe (30 W to 60 E)': (LO >= -30) & (LO < 60),
         'Asia and Oceania (60 E to 170 W)': (LO >= 60) | (LO <= -170)}
for name, m in boxes.items():
    out_n = pop[m & ~inside].sum(); all_n = pop[m].sum()
    print(f'  {name}: {all_n / 1e6:,.0f} million, of whom {out_n / 1e6:,.0f} million outside ({100 * out_n / tot:.2f}% of the world)')
    more[name] = dict(total=float(all_n), outside=float(out_n))
cl = h.unit(*cstar)
inside_l = (h.unit(LA, LO) @ cl) > 0
for name, m in boxes.items():
    out_n = pop[m & ~inside_l].sum()
    print(f'  (land hemisphere) {name}: {out_n / 1e6:,.0f} million outside')
json.dump(more, open(f'{odir}/more.json', 'w'), indent=1)
print('written')
