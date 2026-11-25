# Two cheap candidates for the excess in San Diego's October 2026 sea level: the air's pressure (inverted barometer, about 1 cm per hPa) and the water's warmth.
# October means of hourly air pressure and water temperature at San Diego and La Jolla, every year on file.  Predictions P1-P3 in ~/journal.md (25 Nov, 15:46 UTC), written first.
# Run with python -I (reads downloaded CSV as data).
import numpy as np, glob, os, csv
HERE = os.path.dirname(os.path.abspath(__file__))
def octmean(st, prod, y):
    fn = f'{HERE}/data/{st}_{prod}_{y}10.csv'
    if not os.path.exists(fn): return np.nan, 0
    v = []
    for line in open(fn):
        w = line.split(',')
        if line[:2] in ('19', '20') and len(w) > 1 and w[1].strip() != '':
            try: v.append(float(w[1]))
            except ValueError: pass
    return (np.mean(v), len(v)) if len(v) >= 0.6 * 744 else (np.nan, len(v))
YEARS = range(1990, 2027); T = {}
for st, name in (('9410170', 'San Diego'), ('9410230', 'La Jolla')):
    for prod in ('air_pressure', 'water_temperature'):
        T[(st, prod)] = {y: octmean(st, prod, y)[0] for y in YEARS}
print('October means (blank: fewer than 60% of the hours on file)')
print('year    San Diego hPa   La Jolla hPa   San Diego C   La Jolla C')
for y in YEARS:
    r = [T[(s, p)][y] for p in ('air_pressure', 'water_temperature') for s in ('9410170', '9410230')]
    if all(np.isnan(r)): continue
    print(f'{y}    ' + ''.join(f'{x:14.2f}' if not np.isnan(x) else ' ' * 14 for x in r))
yes = lambda b: 'HELD' if b else 'FAILED'
print()
for st, name in (('9410170', 'San Diego'), ('9410230', 'La Jolla')):
    p = T[(st, 'air_pressure')]; ok = [y for y in YEARS if not np.isnan(p[y])]; others = [p[y] for y in ok if y != 2026]
    if 2026 in ok: print(f'{name}: air pressure Oct 2026 {p[2026]:.2f} hPa; mean of {len(ok)} Octobers {np.mean([p[y] for y in ok]):.2f}; of the {len(others)} others {np.mean(others):.2f} (sd {np.std(others):.2f}); 2026 minus all {p[2026] - np.mean([p[y] for y in ok]):+.2f} hPa' + (f'; 2015 minus all {p[2015] - np.mean([p[y] for y in ok]):+.2f}' if 2015 in ok else ''))
    w = T[(st, 'water_temperature')]; ok = [y for y in YEARS if not np.isnan(w[y])]; base = [w[y] for y in ok if y not in (1997, 2015, 2026)]
    if 2026 in ok:
        rank = sorted(ok, key=lambda y: -w[y]); print(f'{name}: water temperature Oct 2026 {w[2026]:.2f} C; Oct 2015 {w.get(2015, np.nan):.2f}; Oct 1997 {w.get(1997, np.nan):.2f}; mean of the {len(base)} other Octobers {np.mean(base):.2f} (sd {np.std(base):.2f}); warmest five: ' + ', '.join(f'{y} {w[y]:.2f}' for y in rank[:5]))
p = T[('9410170', 'air_pressure')]; ok = [y for y in YEARS if not np.isnan(p[y])]; d = p[2026] - np.mean([p[y] for y in ok])
print(f'\nP1  San Diego Oct 2026 pressure minus the mean of all {len(ok)} Octobers fetched: {d:+.2f} hPa (bar: within 3): {yes(abs(d) <= 3)}')
st = '9410230' if not np.isnan(T[('9410230', 'water_temperature')][2015] + T[('9410230', 'water_temperature')][2026]) else '9410170'
w = T[(st, 'water_temperature')]; base = [w[y] for y in YEARS if not np.isnan(w[y]) and y not in (1997, 2015, 2026)]
print(f'P2  gauge {st}: Oct 2026 {w[2026]:.2f} C against Oct 2015 {w[2015]:.2f} C (bar: 2026 higher): {yes(w[2026] > w[2015])}')
print(f'P3  gauge {st}: Oct 2026 minus the mean of {len(base)} other Octobers: {w[2026] - np.mean(base):+.2f} C (bar: +2.0 or more): {yes(w[2026] - np.mean(base) >= 2.0)}')
