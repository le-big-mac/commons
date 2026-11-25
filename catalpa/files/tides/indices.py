# The two El Nino indices at the same season in the four strongest events, and San Francisco's monthly mean of (observed - NOAA's predicted tide) since October 2025.
# Prints the figures the write-up quotes, so that they trace to a file.  Run with python -I (reads downloaded files as data).
import numpy as np, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); from tide import load_noaa, J2000
import datetime
def table(fn, col):
    out = {}
    for l in open(f'{HERE}/data/{fn}').read().strip().split('\n')[1:]:
        w = l.split(); out[(w[0], int(w[1]))] = float(w[col])
    return out
oni, roni = table('oni.ascii.txt', 3), table('roni.ascii.txt', 2)
print('August-October (ASO) of each event year, and the event\'s highest season:')
print('year    traditional index (ONI)   relative index (RONI)    highest ONI season of the event   highest RONI season')
for y in (1982, 1997, 2015, 2026):
    ev = lambda t: max(((v, s, yy) for (s, yy), v in t.items() if (yy == y and s in ('JJA', 'JAS', 'ASO', 'SON', 'OND', 'NDJ')) or (yy == y + 1 and s in ('DJF', 'JFM'))), default=(np.nan, '', 0))
    a, b = ev(oni), ev(roni); print(f'{y}        {oni.get(("ASO", y), np.nan):5.2f}                    {roni.get(("ASO", y), np.nan):5.2f}                  {a[0]:.2f} ({a[1]} {a[2]})                   {b[0]:.2f} ({b[1]} {b[2]})')
print('seasons in the ONI table at or above 2.46: ' + ', '.join(f'{s} {y} {v:.2f}' for (s, y), v in sorted(oni.items(), key=lambda kv: -kv[1]) if v >= 2.46))
print('seasons in the RONI table at or above 1.97: ' + str(sum(v >= 1.97 for v in roni.values())) + ' of ' + str(len(roni)))
t, y = load_noaa('9414290', 'water_level'); tp, yp = load_noaa('9414290', 'predictions'); r = 100 * (y - np.interp(t, tp, yp)); d = [J2000 + datetime.timedelta(days=float(x)) for x in t[::240]]
ym = np.array([(J2000 + datetime.timedelta(days=float(x))).year * 100 + (J2000 + datetime.timedelta(days=float(x))).month for x in t])
print('\nSan Francisco, monthly mean of (observed - NOAA predicted tide), cm: ' + ', '.join(f'{k // 100}-{k % 100:02d} {r[ym == k].mean():+.1f}' for k in sorted(set(ym))))
