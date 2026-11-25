# A closer look after glider_score.py (not sealed): the anomaly by 25-km bins of distance and by line, for the warm Octobers.  Run with python -I.
import numpy as np, os
HERE = os.path.dirname(os.path.abspath(__file__)); R = np.load(f'{HERE}/glider/profiles_oct.npy'); R = R[np.isfinite(R[:, 5])]; yr, day, lat, lon, km, D, z26, T100, T200, u, v, line, dep, D200, pmax = R.T     # profiles reaching 490 dbar only
box = (lat >= 32) & (lat <= 34.5); along = (v - u) / np.sqrt(2); kb = np.floor(km / 25).astype(int)
print('profiles by line (90 = off Dana Point, 80 = off Point Conception, 0 = neither, e.g. the along-shore line), 20-100 km, by year:')
for y in sorted(set(yr.astype(int))): print(f'   {y}: ' + ', '.join(f'line {l}: {int((box & (yr == y) & (km >= 20) & (km < 100) & (line == l)).sum())}' for l in (90, 80, 0)))
def clim(l, k, x):
    mk = box & (line == l) & (kb == k) & (yr >= 2017) & (yr <= 2025) & np.isfinite(x); return x[mk].mean() if mk.sum() >= 30 and len(set(yr[mk])) >= 4 else np.nan
for l in (90, 80):
    print(f'\nline {l}: anomaly from the 2017-2025 mean of the same 25-km bin.  dynamic height 0/500 (cm) | poleward depth-averaged flow (m/s) | profiles')
    print('   km:        ' + ''.join(f'{25 * k:4d}-{25 * k + 25:<4d}       ' for k in range(0, 14)))
    for y in (2014, 2015, 2023, 2026):
        row = ''
        for k in range(0, 14):
            mk = box & (line == l) & (kb == k) & (yr == y); c = clim(l, k, D); ca = clim(l, k, along)
            row += f'{D[mk].mean() - c:+5.1f}|{np.nanmean(along[mk]) - ca:+5.2f}|{mk.sum():<3d} ' if mk.sum() >= 5 and np.isfinite(c) else '        .        '
        print(f'   {y}   {row}')
    print('   mean 2017-25 height: ' + ''.join(f'{clim(l, k, D):8.1f}         ' for k in range(0, 14)))
# how much of the top-500-m rise is in the top 200 m?  (thermocline pushed down)  mean temperature 0-200 dbar anomaly, 20-100 km
print('\nmean temperature of the top 200 dbar, 20-100 km, anomaly from the 2017-2025 mean of the same line and bin (C):')
for y in (2014, 2015, 2023, 2026):
    a = [T200[i] - clim(int(line[i]), kb[i], T200) for i in np.where(box & (yr == y) & (km >= 20) & (km < 100))[0]]; print(f'   {y}: {np.nanmean(a):+.2f}  (n = {np.isfinite(a).sum()})')
