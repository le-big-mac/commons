# Is the southern California anomaly the ocean's or one gauge's?  mean(observed - NOAA predicted tide) at three gauges within 150 km, and daily means since 15 Sep.
# Run with python -I (reads downloaded CSV as data).
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from tide import load_noaa, when, day_of
ST = (('9410170', 'San Diego'), ('9410230', 'La Jolla'), ('9410660', 'Los Angeles'), ('9414290', 'San Francisco'))
D = {}
for st, name in ST:
    to, yo = load_noaa(st, 'water_level'); tp, yp = load_noaa(st, 'predictions'); d = yo - np.interp(to, tp, yp); D[st] = (to, d)
end = max(D[s][0].max() for s, _ in ST); print(f'latest observation {when(end)} UTC')
print('mean of (observed - NOAA predicted tide), cm, last 30 days; share of 6-minute samples present; quality flags in the files')
for st, name in ST:
    t, d = D[st]; mk = t > end - 30; print(f'   {name:14s} {100 * d[mk].mean():+6.1f}   {mk.sum() / 7200:.2f}')
print('\ndaily means of (observed - predicted), cm, every third day from 15 Sep:')
t0 = day_of('2026-09-15 00:00'); print('   day          ' + ''.join(f'{n:>15s}' for _, n in ST))
days = np.arange(t0, end, 1.0); M = {}
for st, _ in ST:
    t, d = D[st]; M[st] = np.array([100 * d[(t >= a) & (t < a + 1)].mean() if ((t >= a) & (t < a + 1)).sum() > 120 else np.nan for a in days])
for i in range(0, len(days), 3): print(f'   {when(days[i])[:10]}   ' + ''.join(f'{M[s][i]:+15.1f}' for s, _ in ST))
a, b, c = M['9410170'], M['9410230'], M['9410660']; ok = ~np.isnan(a + b + c)
print(f'\ndaily means, San Diego against La Jolla: correlation {np.corrcoef(a[ok], b[ok])[0, 1]:.3f}, sd of difference {np.std(a[ok] - b[ok]):.1f} cm; against Los Angeles: {np.corrcoef(a[ok], c[ok])[0, 1]:.3f}, {np.std(a[ok] - c[ok]):.1f} cm')
print(f'largest day-to-day change in the daily mean, cm: ' + ', '.join(f'{n} {np.nanmax(np.abs(np.diff(M[s]))):.1f}' for s, n in ST))
