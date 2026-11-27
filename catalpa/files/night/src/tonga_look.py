# A look, after the sixth sheet was scored: the twilight of 2022 and 2023 against the years on either side, instrument
# by instrument. The figure is (2022 + 2023)/2 - (2021 + 2024)/2 of each instrument's yearly twilight figure, in
# magnitudes: a steady drift of the instrument cancels in it exactly. Negative: the twilight read brighter in 2022-23.
# Unsealed. Usage: tonga_look.py FILE.pkl [FILE.pkl ...]
import sys, pickle, csv, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('twsheet', '/home/agent1/night/src/twsheet.py'); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
geo = {r['name']: r for r in csv.DictReader(open('/home/agent1/night/lit/src/p3_stars4all_geolist.csv'), delimiter=';')}
SIX = (1, 3, 5, 7, 9, 11); rows = {}
for fn in sys.argv[1:]:
    R = pickle.load(open(fn, 'rb')); R.pop('meta', None); rows.update(S.table(R, SIX))
def stat(x):
    y = x['yearly']
    if not all(k in y for k in (2021, 2022, 2023, 2024)): return None
    return abs(x['slope']) * ((y[2022] + y[2023]) / 2 - (y[2021] + y[2024]) / 2)
out = []
for st, x in rows.items():
    if not x: continue
    d = stat(x)
    if d is None: continue
    lat = float(geo[st]['latitude']) if st in geo and geo[st]['latitude'] else float('nan')
    out.append((lat, st, d, x['name'][:44], [round(100 * abs(x['slope']) * (x['yearly'][k] - np.mean([x['yearly'][j] for j in (2021, 2022, 2023, 2024)]))) for k in (2021, 2022, 2023, 2024)]))
print('latitude   station    2022-23 less 2021 and 2024   the four years, hundredths of a magnitude from their mean   place')
for lat, st, d, name, ys in sorted(out): print(f'  {lat:+7.2f}  {st:<9}  {d:+.3f}                      {ys[0]:+4d} {ys[1]:+4d} {ys[2]:+4d} {ys[3]:+4d}                              {name}')
for lab, sel in (('south of the equator', lambda la: la < 0), ('the equator to 30 north', lambda la: 0 <= la < 30), ('30 to 36 north', lambda la: 30 <= la < 36), ('north of 36', lambda la: la >= 36)):
    v = [d for lat, st, d, n, ys in out if sel(lat)]
    if v: print(f'{lab}: {len(v)} instruments; middle {np.median(v):+.3f}; from {min(v):+.3f} to {max(v):+.3f}; at -0.08 or below: {sum(1 for x in v if x <= -0.08)}; within 0.05 of nothing: {sum(1 for x in v if abs(x) < 0.05)}')
