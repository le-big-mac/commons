"""The hemisphere with most people in eight epochs of GHS-POP R2023A (1975 to 2030), and the two summits in each.

usage: people_epochs.py GRID_DIR OUT_DIR
Not scored. Tests one explanation: that the published "western Switzerland" centre and mine near Berlin differ
because the world's population moved, not because one of the computations is wrong.
"""
import json
import os
import sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hemilib as h

gdir, odir = sys.argv[1], sys.argv[2]
KM = np.pi * h.R_KM / 180
GENEVA = (46.36, 6.75)
BERLIN = (52.37, 12.68)


def climb(X, w, e, start):
    c = h.unit(*start)
    for half, step in ((0.6, 0.05), (0.12, 0.01)):
        for it in range(400):
            lc = h.Local(X, w, e, c, half * 1.5)
            o, g, n_, e_ = lc.grid(half, step)
            i, j = np.unravel_index(np.nanargmax(g), g.shape)
            if o[i] == 0 and o[j] == 0:
                break
            c = lc.point(o[i], o[j], n_, e_)
    return c, h.share(X, w, c, e)


_lat = -90 + (np.arange(3600) + 0.5) * 0.05; _lon = -180 + (np.arange(7200) + 0.5) * 0.05
_LA, _LO = np.meshgrid(_lat, _lon, indexing='ij')
_V = h.unit(_LA, _LO)
INS = (_V @ h.unit(46.0, 7.18)) > 0      # the Swiss summit of 1975 and 2000
INB = (_V @ h.unit(52.37, 12.68)) > 0    # the summit near Berlin of 2020
del _V, _LA, _LO
rows = []
for year, name in ((1975, 'pop005_1975'), (2000, 'pop005_2000'), (2005, 'pop005_2005'), (2010, 'pop005_2010'), (2015, 'pop005_2015'),
                   (2020, 'pop005'), (2025, 'pop005_2025'), (2030, 'pop005_2030')):
    path = f'{gdir}/{name}.npy'
    if not os.path.exists(path):
        print(year, 'grid missing'); continue
    pop = np.load(path)
    r = h.best_cap(pop, verbose=False)
    X, w, e = r['X'], r['w'], r['eps']
    out = dict(year=year, total=float(pop.sum()), best=dict(lat=r['lat'], lon=r['lon'], share=r['share']))
    line = f'{year}: {pop.sum() / 1e9:.3f} billion; best {100 * r["share"]:.3f}% at {r["lat"]:.2f}, {r["lon"]:.2f}'
    for tag, start in (('geneva', GENEVA), ('berlin', BERLIN)):
        c, s = climb(X, w, e, start)
        la, lo = h.latlon(c)
        out[tag] = dict(lat=float(la), lon=float(lo), share=s, fixed=h.share(X, w, h.unit(*start), e))
        line += f' | climbing from {start}: {100 * s:.3f}% at {la:.2f}, {lo:.2f} (at the starting point itself {100 * out[tag]["fixed"]:.3f}%)'
    # the two slivers by which the fixed Swiss-centred and Berlin-centred halves differ
    asia = float(pop[INB & ~INS].sum()); amer = float(pop[~INB & INS].sum())
    out['only_berlin_half'] = asia; out['only_swiss_half'] = amer
    line += f' | only in the Berlin half {asia / 1e6:.1f} M, only in the Swiss half {amer / 1e6:.1f} M'
    print(line, flush=True)
    rows.append(out)
json.dump(rows, open(f'{odir}/people_epochs.json', 'w'), indent=1)
