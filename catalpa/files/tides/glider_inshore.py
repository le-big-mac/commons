# The last 50 km: steric height of the surface relative to 200 dbar, from every glider profile that reaches 200 dbar, in 5-km bins of distance on the line off Dana Point (line 90).
# Line G4 in ~/journal.md (25 Nov), written before this was computed.  Run with python -I.
import numpy as np, os
HERE = os.path.dirname(os.path.abspath(__file__)); R = np.load(f'{HERE}/glider/profiles_oct.npy'); yr, day, lat, lon, km, D, z26, T100, T200, u, v, line, dep, D200, pmax = R.T
along = (v - u) / np.sqrt(2)
for l in (90, 80):
    box = (lat >= 32) & (lat <= 34.5) & (line == l); kb = np.floor(km / 5).astype(int)
    def clim(k, x):
        mk = box & (kb == k) & (yr >= 2017) & (yr <= 2025) & np.isfinite(x); return x[mk].mean() if mk.sum() >= 15 and len(set(yr[mk])) >= 3 else np.nan
    print(f'line {l}: steric height 0/200 dbar, anomaly from the 2017-2025 mean of the same 5-km bin (cm) | poleward flow anomaly (m/s) | profiles;  last row: profiles in 2017-2025')
    print('   km:    ' + ''.join(f'{5 * k:3d}-{5 * k + 5:<3d}          ' for k in range(0, 12)))
    res = {}
    for y in (2015, 2023, 2026):
        row = ''
        for k in range(0, 12):
            mk = box & (kb == k) & (yr == y); c = clim(k, D200); ca = clim(k, along)
            if mk.sum() >= 5 and np.isfinite(c): res[(y, k)] = D200[mk].mean() - c; row += f'{D200[mk].mean() - c:+5.1f}|{np.nanmean(along[mk]) - ca:+5.2f}|{mk.sum():<3d}  '
            else: row += f'    . ({mk.sum():2d})     '
        print(f'   {y}  {row}')
    print('          ' + ''.join(f'{int((box & (kb == k) & (yr >= 2017) & (yr <= 2025)).sum()):<17d}' for k in range(0, 12)))
    if l == 90:
        ks = sorted(k for (y, k) in res if y == 2026); inner = ks[0] if ks else None; ref = [res[(2026, k)] for k in (4, 5) if (2026, k) in res]
        if inner is not None and ref and inner < 4:
            d = res[(2026, inner)] - np.mean(ref); print(f'G4  innermost bin with data in October 2026: {5 * inner}-{5 * inner + 5} km, {res[(2026, inner)]:+.1f} cm; at 20-30 km {np.mean(ref):+.1f} cm; difference {d:+.1f} (bar +5 or more): {"HELD" if d >= 5 else "FAILED"}')
        else: print('G4  void: no bin inside 20 km with five profiles in October 2026')
# how much of the 0/500 height is in the top 200?  same profiles, both references, 20-100 km
mk = np.isfinite(D) & (lat >= 32) & (lat <= 34.5) & (km >= 20) & (km < 100)
for y in (2015, 2026): print(f'{y}: 20-100 km, profiles reaching 490 dbar: mean height 0/500 {D[mk & (yr == y)].mean():.1f} cm, 0/200 {D200[mk & (yr == y)].mean():.1f} cm; the 2017-2025 means: {D[mk & (yr >= 2017) & (yr <= 2025)].mean():.1f}, {D200[mk & (yr >= 2017) & (yr <= 2025)].mean():.1f}')
print('shallowest sea floor a glider met (deepest pressure of a dive), by 5-km bin on line 90, all years: ' + ', '.join(f'{5 * k}-{5 * k + 5}: {np.percentile(pmax[(line == 90) & (np.floor(km / 5) == k)], 10):.0f}' for k in range(0, 8) if ((line == 90) & (np.floor(km / 5) == k)).sum() > 10))
