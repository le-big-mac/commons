"""For each epoch: the highest point of the people share in each of three regions, by climbing from the summits found
by people_fine.py, and the people in the two slivers. Makes the table of the README.

usage: people_table.py GRID_DIR OUT_DIR
"""
import json
import os
import sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hemilib as h

gdir, odir = sys.argv[1], sys.argv[2]
STARTS = {'western Alps': [(46.0, 7.17), (45.05, 6.69), (44.35, 7.28), (44.86, 7.30), (46.37, 6.74)],
          'Upper Palatinate': [(49.36, 12.40)],
          'Brandenburg': [(52.06, 12.79), (52.37, 12.68), (51.78, 12.31), (51.5, 13.05)]}


def climb(X, w, e, c):
    for half, step in ((0.3, 0.05), (0.06, 0.01)):
        for it in range(500):
            lc = h.Local(X, w, e, c, half * 1.5)
            o, g, n_, e_ = lc.grid(half, step)
            i, j = np.unravel_index(np.nanargmax(g), g.shape)
            if o[i] == 0 and o[j] == 0:
                break
            c = lc.point(o[i], o[j], n_, e_)
        else:
            raise SystemExit('climb did not stop')
    return c, h.share(X, w, c, e)


fine = {r['year']: r for r in json.load(open(f'{odir}/people_fine.json'))}
ep = {r['year']: r for r in json.load(open(f'{odir}/people_epochs.json'))}
rows = []
for year, name in ((1975, 'pop005_1975'), (2000, 'pop005_2000'), (2005, 'pop005_2005'), (2010, 'pop005_2010'), (2015, 'pop005_2015'),
                   (2020, 'pop005'), (2025, 'pop005_2025'), (2030, 'pop005_2030')):
    pop = np.load(f'{gdir}/{name}.npy')
    X, w, e = h.cells(pop)
    row = dict(year=year, total=float(pop.sum()), best=fine[year]['summits'][0], only_berlin=ep[year]['only_berlin_half'], only_swiss=ep[year]['only_swiss_half'])
    for region, starts in STARTS.items():
        best = None
        for st in starts:
            c, s = climb(X, w, e, h.unit(*st))
            la, lo = map(float, h.latlon(c))
            if best is None or s > best['share']:
                best = dict(share=s, lat=la, lon=lo)
        row[region] = best
    rows.append(row)
    print(year, f"best {100 * row['best']['share']:.4f} at {row['best']['lat']:.2f}, {row['best']['lon']:.2f} | " +
          ' | '.join(f"{k} {100 * row[k]['share']:.4f} at {row[k]['lat']:.2f}, {row[k]['lon']:.2f}" for k in STARTS), flush=True)
json.dump(rows, open(f'{odir}/people_table.json', 'w'), indent=1)
