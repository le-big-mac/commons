# The sea standing above its predicted tide on the US West Coast, autumn 2026: four gauges, their whole monthly records, and NOAA's ONI table.
# Predictions N1-N3 in ~/journal.md (25 Nov, 15:39 UTC) were written before any of this was fetched.  Run with python -I (reads downloaded files as data).
import numpy as np, sys, csv, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tide import load_noaa, day_of
names = {'9410170': 'San Diego', '9414290': 'San Francisco', '9432780': 'Charleston, Oregon', '9447130': 'Seattle'}
END = day_of(sys.argv[1]) if len(sys.argv) > 1 else None      # optional: use observations up to this UTC time only (to reproduce a dated run)
print('mean of (observed - NOAA predicted tide), cm: last 30 days, and 15 Sep - 15 Oct 2026')
for st, name in names.items():
    t, y = load_noaa(st, 'water_level'); tp, yp = load_noaa(st, 'predictions')
    if END is not None: y = y[t <= END]; t = t[t <= END]
    r = y - np.interp(t, tp, yp)
    a = (t > t[-1] - 30); b = (t >= day_of('2026-09-15 00:00')) & (t < day_of('2026-10-15 00:00'))
    print(f'   {name:20s} {100 * r[a].mean():+6.1f}   {100 * r[b].mean():+6.1f}   (n = {a.sum()}, {b.sum()})')
print('\nmonthly mean sea level (m above the MSL datum of 1983-2001), from NOAA\'s monthly means: October and the latest months')
for st, name in names.items():
    rows = [r for r in csv.reader(open(f'{HERE}/data/{st}_monthly_mean.csv')) if r and r[0].strip().isdigit()]
    M = {(int(r[0]), int(r[1])): float(r[5]) for r in rows if r[5].strip() not in ('', 'NaN')}
    octs = sorted(((v, y) for (y, m), v in M.items() if m == 10), reverse=True); rank = [y for v, y in octs].index(2026) + 1 if (2026, 10) in M else None
    print(f'   {name:20s} record {min(y for y, m in M)}-2026, {len(octs)} Octobers; Oct 2026 = {M.get((2026, 10), float("nan")):+.3f} m, rank {rank}; top five Octobers: ' + ', '.join(f'{y} {v:+.3f}' for v, y in octs[:5]))
    print(f'        2026 by month: ' + ' '.join(f'{M.get((2026, m), float("nan")):+.3f}' for m in range(1, 11)) + f';  Oct 1997 {M.get((1997, 10), float("nan")):+.3f}, Oct 2015 {M.get((2015, 10), float("nan")):+.3f}, Oct 1982 {M.get((1982, 10), float("nan")):+.3f}, Oct 2025 {M.get((2025, 10), float("nan")):+.3f}')
    ys = np.array([y for v, y in octs]); vs = np.array([v for v, y in octs]); c = np.polyfit(ys, vs, 1); resid = {y: v - np.polyval(c, y) for v, y in octs}    # Octobers alone, straight-line trend removed
    top = sorted(resid.items(), key=lambda kv: -kv[1])[:4]; print(f'        trend {c[0] * 1000:.2f} mm/yr; Octobers furthest above the trend: ' + ', '.join(f'{y} {100 * v:+.1f} cm' for y, v in top))
L = open(f'{HERE}/data/oni.ascii.txt').read().strip().split('\n')
print('\nONI (Nino-3.4), last seasons: ' + '; '.join(' '.join(l.split()[:2]) + ' ' + l.split()[3] for l in L[-6:]))
print('strongest seasons on record: ' + ', '.join(f'{a} {b} {c}' for c, a, b in sorted(((float(l.split()[3]), l.split()[0], l.split()[1]) for l in L[1:]), reverse=True)[:6]))
