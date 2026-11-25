# Score G1-G3 from the glider profiles (glider.py first), then look at where and how deep the excess is.  Run with python -I.
import numpy as np, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); DIR = sys.argv[1] if len(sys.argv) > 1 else 'oct'
R = np.load(f'{HERE}/glider/profiles_{DIR}.npy'); R = R[np.isfinite(R[:, 5])]; yr, day, lat, lon, km, D, z26, T100, T200, u, v, line, dep, D200, pmax = R.T     # profiles reaching 490 dbar only
box = (lat >= 32) & (lat <= 34.5); BANDS = ((20, 100), (100, 200), (200, 350)); YEARS = sorted(set(yr.astype(int)))
along = (v - u) / np.sqrt(2)            # depth-averaged current toward the north-west, roughly along this coast and toward the pole
def cell(y, a, b, x=D):
    mk = box & (yr == y) & (km >= a) & (km < b) & np.isfinite(x); return x[mk], mk
print(f'profiles reaching 490 dbar, 32-34.5N, {DIR}: dynamic height of the surface relative to 500 dbar (cm), mean over profiles; n = profiles (days with any)')
print('year   ' + ''.join(f'  {a:3d}-{b:3d} km: n (days)  mean    sd  ' for a, b in BANDS))
M = {}
for y in YEARS:
    row = ''
    for a, b in BANDS:
        x, mk = cell(y, a, b); nd = len(set(np.floor(day[mk]))); M[(y, a)] = (x.mean() if len(x) >= 20 else np.nan, len(x))
        row += f'      {len(x):4d} ({nd:2d})   {x.mean() if len(x) else np.nan:6.1f}  {x.std() if len(x) else np.nan:5.1f}  '
    print(f'{y}   {row}')
yes = lambda b: 'HELD' if b else 'FAILED'
def base(a): 
    v_ = [M[(y, a)][0] for y in range(2017, 2026) if (y, a) in M and np.isfinite(M[(y, a)][0])]; return (np.mean(v_), len(v_)) if len(v_) >= 5 else (np.nan, len(v_))
g1 = M.get((2026, 20), (np.nan,))[0] - M.get((2015, 20), (np.nan,))[0]; b20, n20 = base(20); b200, n200 = base(200)
g2 = M.get((2026, 20), (np.nan,))[0] - b20; g3 = g2 - (M.get((2026, 200), (np.nan,))[0] - b200)
print(f'\nG1  20-100 km, October 2026 minus October 2015: {g1:+.1f} cm (bar +8 or more): ' + ('VOID (a month has fewer than 20 profiles)' if not np.isfinite(g1) else yes(g1 >= 8)))
print(f'G2  20-100 km, October 2026 minus the mean of {n20} Octobers of 2017-2025: {g2:+.1f} cm (bar +12 or more): ' + ('VOID' if not np.isfinite(g2) else yes(g2 >= 12)))
print(f'G3  that anomaly at 20-100 km minus the one at 200-350 km ({n200} Octobers): {g3:+.1f} cm (bar +8 or more): ' + ('VOID' if not np.isfinite(g3) else yes(g3 >= 8)))
# ---- the look: remove where the glider happened to be.  Climatology by line and 25-km distance bin from 2017-2025; anomalies averaged by day, then over days.
print('\n-- a look, not sealed: anomaly from a 2017-2025 mean for the same line and the same 25-km bin of distance (so that a year is not high merely for where its glider was) --')
kb = np.floor(km / 25).astype(int); clim = {}
for key in set(zip(line.astype(int), kb)):
    mk = box & (line == key[0]) & (kb == key[1]) & (yr >= 2017) & (yr <= 2025)
    if mk.sum() >= 30 and len(set(yr[mk])) >= 4: clim[key] = (D[mk].mean(), np.nanmean(z26[mk]), T100[mk].mean(), np.nanmean(along[mk]))
A = np.full((len(D), 4), np.nan)
for i in range(len(D)):
    c = clim.get((int(line[i]), kb[i]))
    if c and box[i]: A[i] = (D[i] - c[0], z26[i] - c[1], T100[i] - c[2], along[i] - c[3])
print('year   ' + ''.join(f'  {a:3d}-{b:3d} km: days  height cm (se)   sigma 26.0 deeper by, m   T at 100 m, C   poleward flow, m/s ' for a, b in BANDS[:2]) + '   200-350 km: days  height cm (se)')
for y in YEARS:
    row = ''
    for a, b in BANDS:
        mk = (yr == y) & (km >= a) & (km < b) & np.isfinite(A[:, 0]); days = sorted(set(np.floor(day[mk])))
        if len(days) < 3: row += '        .' + ' ' * (70 if a < 200 else 12); continue
        dm = np.array([np.nanmean(A[mk & (np.floor(day) == d_)], axis=0) for d_ in days]); m = np.nanmean(dm, axis=0); se = dm[:, 0].std() / np.sqrt(len(days))
        row += f'       {len(days):3d}    {m[0]:+6.1f} ({se:3.1f})' + (f'            {m[1]:+6.1f}              {m[2]:+5.2f}          {m[3]:+6.3f}        ' if a < 200 else '')
    print(f'{y}   {row}')
print('(se: scatter of the daily means over the root of the number of days; neighbouring days are not independent, so it is too small)')
