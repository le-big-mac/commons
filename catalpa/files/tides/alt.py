# Is the excess of October 2026 hugging the coast or wide?  Satellite altimetry (NOAA CoastWatch blended daily sea level anomaly, 0.25 deg; Octobers 2017-2026)
# against the San Diego gauge on the same footing: October 2026 minus the mean of Octobers 2017-2025.  Lines A1-A3 (and A4, void: no October 2015 on file) in ~/journal.md, written first.
# Run with python -I (reads downloaded CSV as data).
import numpy as np, csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
def october(y):
    acc = {}; days = set()
    for line in open(f'{HERE}/alt/sla_{y}10.csv'):
        w = line.strip().split(',')
        if not w[0].startswith(f'{y}-10'): continue
        days.add(w[0][:10])
        if w[3] in ('NaN', ''): continue
        k = (float(w[1]), float(w[2])); a = acc.setdefault(k, [0.0, 0]); a[0] += float(w[3]); a[1] += 1
    return {k: s / n for k, (s, n) in acc.items() if n >= 0.8 * len(days)}, len(days)
F = {}
for y in range(2017, 2027): F[y], nd = october(y); print(f'October {y}: {nd} days, {len(F[y])} ocean cells', end='; ' if y % 2 else '\n')
cells = sorted(set.intersection(*[set(F[y]) for y in F])); base = {k: np.mean([F[y][k] for y in range(2017, 2026)]) for k in cells}; anom = {k: 100 * (F[2026][k] - base[k]) for k in cells}
# the gauge on the same footing
M = {}
for r in csv.reader(open(f'{HERE}/data/9410170_monthly_mean.csv')):
    if r and r[0].strip().isdigit() and int(r[1]) == 10 and r[5].strip() not in ('', 'NaN'): M[int(r[0])] = 100 * float(r[5])
g = M[2026] - np.mean([M[y] for y in range(2017, 2026)]); print(f'\nSan Diego gauge: October 2026 {M[2026]:+.1f} cm, mean of Octobers 2017-2025 {np.mean([M[y] for y in range(2017, 2026)]):+.1f} cm ({sum(y in M for y in range(2017, 2026))} of 9 on file): excess {g:+.1f} cm')
# distance of each cell from the mainland coast, taken as a line through these points (deg N, deg E)
COAST = [(30.4, -115.9), (31.85, -116.62), (32.7, -117.2), (33.46, -117.70), (33.75, -118.2), (34.0, -118.8), (34.45, -120.47), (35.2, -120.9), (36.6, -121.9), (37.8, -122.5)]
def km(p, q): return np.hypot((p[0] - q[0]) * 111.2, (p[1] - q[1]) * 111.2 * np.cos(np.radians((p[0] + q[0]) / 2)))
def dist(p):
    best = 1e9
    for a, b in zip(COAST[:-1], COAST[1:]):
        for f in np.linspace(0, 1, 40): best = min(best, km(p, (a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1]))))
    return best
D = {k: dist(k) for k in cells}
print('\nOctober 2026 minus the mean of Octobers 2017-2025, by distance from the mainland coast, cells between 32N and 34N (and, for comparison, 36N-38N off San Francisco):')
print('   km off the coast      32-34N: cells, mean (cm), sd      36-38N: cells, mean (cm), sd')
for a, b in ((0, 50), (50, 100), (100, 150), (150, 200), (200, 300), (300, 400), (400, 500), (500, 700)):
    row = []
    for la, lb in ((32, 34), (36, 38)):
        v = [anom[k] for k in cells if la <= k[0] <= lb and a <= D[k] < b and k[1] < COAST[2][1] + 3]; row.append(f'{len(v):4d}   {np.mean(v):+6.1f}   {np.std(v):5.1f}' if v else '   0        .       .')
    print(f'   {a:3d}-{b:3d}              {row[0]}                {row[1]}')
yes = lambda b: 'HELD' if b else 'FAILED'
box = [anom[k] for k in cells if 31 <= k[0] <= 33 and -120.5 <= k[1] <= -118.5]; a1 = np.mean(box)
print(f'\nA1  box 31-33N, 120.5-118.5W: {len(box)} cells, mean {a1:+.1f} cm (sd {np.std(box):.1f}); half the gauge\'s excess is {g / 2:+.1f}: {yes(a1 >= g / 2)}')
near = [anom[k] for k in cells if 32 <= k[0] <= 34 and D[k] < 75]; far = [anom[k] for k in cells if 32 <= k[0] <= 34 and 300 <= D[k] < 500]
print(f'A2  within 75 km: {len(near)} cells, {np.mean(near):+.1f} cm; 300-500 km off: {len(far)} cells, {np.mean(far):+.1f} cm; difference {np.mean(near) - np.mean(far):+.1f} (bar +5 or more): {yes(np.mean(near) - np.mean(far) >= 5)}')
gp = (32.714, -117.174); kn = min(cells, key=lambda k: km(k, gp))
print(f'A3  cell nearest the gauge: {kn}, {km(kn, gp):.0f} km away: {anom[kn]:+.1f} cm against the gauge\'s {g:+.1f} (bar: within 8): {yes(abs(anom[kn] - g) <= 8)}')
print('A4  void: the dataset has no October 2015 (one day in January 2015, then from 13 Feb 2017)')
print('\neach October in the box, cm (sea level anomaly as served, no baseline removed): ' + ', '.join(f'{y} {100 * np.mean([F[y][k] for k in cells if 31 <= k[0] <= 33 and -120.5 <= k[1] <= -118.5]):+.1f}' for y in F))
print('the gauge, each October, cm: ' + ', '.join(f'{y} {M[y]:+.1f}' for y in range(2017, 2027) if y in M))
import pickle; pickle.dump((cells, anom, D), open('/tmp/alt_anom.pkl', 'wb'))
