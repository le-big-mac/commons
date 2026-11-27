"""My own working of what the two programs of the map print and place, from out/wide.npz, without the study's library:
the two summits on the grid, their shares, the gap, the distance, and where Nantes, Ile Dumet and Tarragona fall on the map
(km east and north of its middle). Then the points of the chart from the JSON files. No plotting. Reads only.
usage: recompute_hemi.py WIDE.npz SECOND_MAP_OUT_DIR"""
import sys, json, math, os
import numpy as np
R_KM = 6371.0088                     # the mean radius of the Earth; the study's library uses the same figure (hemilib.py line 12)
KM = math.pi * R_KM / 180
W = np.load(sys.argv[1])
print('arrays in the file:', {k: W[k].shape for k in W.files})
offs, G, north, east, c0 = W['offs'], W['G'], W['north'], W['east'], W['c_mid']
ext = offs * KM
print(f'grid: {G.shape}, offsets {offs[0]:+.3f} to {offs[-1]:+.3f} degrees in steps of {offs[1] - offs[0]:.4f}, i.e. {ext[0]:+.1f} to {ext[-1]:+.1f} km, step {ext[1] - ext[0]:.2f} km')
print('middle of the map (c_mid): lat %.4f lon %.4f; |north| %.6f |east| %.6f; north.east %.2e; north.c %.2e' % (
    math.degrees(math.asin(c0[2])), math.degrees(math.atan2(c0[1], c0[0])), np.linalg.norm(north), np.linalg.norm(east), north @ east, north @ c0))
def unit(lat, lon):
    la, lo = math.radians(lat), math.radians(lon)
    return np.array([math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la)])
def project(lat, lon):               # distance along the great circle from the middle, split into east and north: my own writing of it
    v = unit(lat, lon)
    t = math.degrees(math.acos(max(-1.0, min(1.0, float(v @ c0)))))
    s = math.sin(math.radians(max(t, 1e-12)))
    return t * float(v @ east) / s * KM, t * float(v @ north) / s * KM
iy, ix = np.unravel_index(np.nanargmax(G), G.shape)
south = (ext[ix], ext[iy])
nx, ny = project(47.42, -2.36)
best = (-1, None)
for j in range(G.shape[0]):
    for i in range(G.shape[1]):
        if (ext[i] - nx) ** 2 + (ext[j] - ny) ** 2 < 150 ** 2 and not np.isnan(G[j, i]) and G[j, i] > best[0]: best = (G[j, i], (j, i))
jy, jx = best[1]
northp = (ext[jx], ext[jy])
gap = (G[iy, ix] - G[jy, jx]) * 100
print(f'southern summit (the highest cell of the grid): ({south[0]:+.1f}, {south[1]:+.1f}) km, share {100 * G[iy, ix]:.4f}%')
print(f'northern summit (the highest cell within 150 km of 47.42 N 2.36 W, which falls at ({nx:+.1f}, {ny:+.1f}) km): ({northp[0]:+.1f}, {northp[1]:+.1f}) km, share {100 * G[jy, jx]:.4f}%')
print(f'gap {gap:.4f} points of the world\'s land; distance between them on the map {math.hypot(south[0] - northp[0], south[1] - northp[1]):.1f} km')
for land in (146.74,):
    print(f'  with the note\'s {land} million km2 of land: {gap / 100 * land * 1e6:,.0f} km2  (lettering: "46,000 km2 less (0.03% of the world\'s land)", "81.2% of the world\'s")')
# is the northern point a summit of its own (higher than all eight neighbours)?
nb = G[jy - 1:jy + 2, jx - 1:jx + 2]
print('  the northern cell is the highest of its 3 x 3 block:', bool(G[jy, jx] == np.nanmax(nb)), '; cells of the grid with loss under 0.01 points:', int(((np.nanmax(G) - G) * 100 < 0.01).sum()),
      '; loss at the northern summit', f'{(np.nanmax(G) - G[jy, jx]) * 100:.4f}')
PLACES = {'Nantes': (47 + 13 / 60, -(1 + 32 / 60)), 'Ile Dumet': (47 + 24 / 60 + 42 / 3600, -(2 + 37 / 60 + 15 / 3600)), 'Tarragona': (41.119, 1.245),
          'Brittany (name, wide map)': (48.25, -3.3), 'Catalonia (name, wide map)': (41.95, 1.2)}
pts = {'southern summit': south, 'northern summit': northp}
for k, (la, lo) in PLACES.items(): pts[k] = project(la, lo)
for k, (x, y) in pts.items(): print(f'  {k:28s} at ({x:+8.1f}, {y:+8.1f}) km')
print(f'  Ile Dumet to the northern summit: {math.hypot(pts["Ile Dumet"][0] - northp[0], pts["Ile Dumet"][1] - northp[1]):.1f} km; Nantes to it: {math.hypot(pts["Nantes"][0] - northp[0], pts["Nantes"][1] - northp[1]):.1f} km; '
      f'Tarragona to the southern summit: {math.hypot(pts["Tarragona"][0] - south[0], pts["Tarragona"][1] - south[1]):.1f} km')
json.dump({k: [float(v[0]), float(v[1])] for k, v in pts.items()} | {'ext0': float(ext[0]), 'ext1': float(ext[-1])}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'places_km.json'), 'w'), indent=1)
# the loss at a few places, and the levels of the lines
loss = (np.nanmax(G) - G) * 100
print('loss on the grid: least %.4f, greatest %.3f points; cells without a value: %d' % (np.nanmin(loss), np.nanmax(loss), int(np.isnan(loss).sum())))
# ---- the chart
od = sys.argv[2]
SER = {'ghs': (1975, 2000, 2005, 2010, 2015, 2020, 2025, 2030), 'g1': (2000, 2010, 2020), 'g2': (2015, 2020, 2025, 2030)}
print('\nchart: only_berlin minus only_valais, in millions; and what 5 million is of that file\'s total')
vals = {}
for key, years in SER.items():
    for y in years:
        p = os.path.join(od, f'{key}-{y}.json')
        if not os.path.exists(p): print('  MISSING', p); continue
        r = json.load(open(p))
        d = (r['only_berlin'] - r['only_valais']) / 1e6
        vals[f'{key}-{y}'] = d
        print(f'  {key:3s} {y}: {d:+7.2f} million   (total {r["total"] / 1e9:.3f} thousand million; 5 million is {100 * 5e6 / r["total"]:.3f}% of it)')
others = sorted(f for f in os.listdir(od) if f.endswith('.json') and f[:-5] not in vals)
print('  JSON files in the folder that the chart does not draw:', others)
json.dump(vals, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'chart_values.json'), 'w'), indent=1)
