# What earlier strong El Nino years did next at the same gauges: monthly mean sea level minus (trend + mean seasonal cycle), June of the year to May of the next.
# A look, not a sealed test.  Run with python -I (reads downloaded CSV as data).
import csv, sys, numpy as np
START = int(sys.argv[1]) if len(sys.argv) > 1 else 1900     # months before this year are left out: one straight line fits 1900-2026 tolerably, 1854-2026 less well (the rise was slower then)
MON = 'Jun Jul Aug Sep Oct Nov Dec Jan Feb Mar Apr May'.split()
for st, name in (('9410170', 'San Diego'), ('9414290', 'San Francisco'), ('9432780', 'Charleston, Oregon'), ('9447130', 'Seattle')):
    rows = [r for r in csv.reader(open(f'data/{st}_monthly_mean.csv')) if r and r[0].strip().isdigit() and r[5].strip() not in ('', 'NaN') and int(r[0]) >= START]
    y = np.array([int(r[0]) for r in rows]); m = np.array([int(r[1]) for r in rows]); v = 100 * np.array([float(r[5]) for r in rows]); t = y + (m - 0.5) / 12
    A = np.column_stack([np.ones_like(t), t - 2000] + [(m == k).astype(float) for k in range(2, 13)])     # trend + a level for each calendar month
    use = ~np.isin(y, (1982, 1983, 1997, 1998, 2015, 2016, 2026))                                         # fitted without the event years themselves
    c = np.linalg.lstsq(A[use], v[use], rcond=None)[0]; res = v - A @ c; sd = res[use].std()
    print(f'{name}: monthly mean sea level minus (trend {c[1] * 10:.2f} mm/yr + mean seasonal cycle, fitted {y.min()}-{y.max()}), cm; sd of ordinary months {sd:.1f} cm')
    print('   ' + ' ' * 9 + ''.join(f'{x:>7s}' for x in MON))
    for y0 in (1982, 1997, 2015, 2026):
        out = []
        for k in range(12):
            yy, mm = (y0, 6 + k) if k < 7 else (y0 + 1, k - 6)
            i = np.where((y == yy) & (m == mm))[0]; out.append(f'{res[i[0]]:+7.1f}' if len(i) else '      .')
        print(f'   {y0}-{(y0 + 1) % 100:02d}  ' + ''.join(out))
    big = np.sort(res)[::-1][:6]; idx = np.argsort(res)[::-1][:6]
    print(f'   six largest months since {max(START, y.min())}: ' + ', '.join(f'{y[i]}-{m[i]:02d} {res[i]:+.1f}' for i in idx))
