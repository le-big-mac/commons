"""Second pass of the checker's search: search.py refined only the summits of a smoothed map, and so could miss a
narrow spike of the staircase (it did, for the 2010 grids: a 0.05-degree lattice point at 45.05 N 6.70 E stood above
its "best"). Here the raw 0.05-degree map of Europe saved by search.py is cut into regions; in each, the five highest
lattice points that are at least 0.3 degrees apart are refined at 0.01 degrees in a box of +-0.15 degrees, and the
highest value is kept. The best anywhere is the highest of the regions.

usage: python -I search2.py NAME GRID.npy SEARCH_OUT.json OUT.json"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chk

name, gpath, sjson, outp = sys.argv[1:5]
E = np.load(sjson.replace('.json', '.europe005.npy')).astype(np.float64)
elat = np.round(np.arange(40, 60 + 1e-9, 0.05), 6); elon = np.round(np.arange(0, 25 + 1e-9, 0.05), 6)
assert E.shape == (len(elat), len(elon))
cum = chk.Cum(np.load(gpath))
REGIONS = dict(alps_south_of_47p5=(40, 47.5, 0, 25), between_47p5_and_48p5=(47.5001, 48.4999, 0, 25), palatinate_franconia_48p5_51N=(48.5, 51.0, 9, 14),
               berlin_51_54N_10_16E=(51.0001, 54, 10, 16), baltic_54_60N_13_25E=(54.0001, 60, 13, 25), north_of_48p5=(48.5, 60, 0, 25))
res = dict(name=name, total=cum.total, regions={})
for rn, (la0, la1, lo0, lo1) in REGIONS.items():
    i0, i1 = np.searchsorted(elat, [la0 - 1e-9, la1 + 1e-9]); j0, j1 = np.searchsorted(elon, [lo0 - 1e-9, lo1 + 1e-9])
    sub = E[i0:i1, j0:j1].copy()
    picks = []
    order = np.argsort(sub.ravel())[::-1]
    for k in order[:4000]:
        x, y = divmod(int(k), sub.shape[1])
        la, lo = float(elat[i0 + x]), float(elon[j0 + y])
        if all(abs(la - p[0]) >= 0.3 or abs(lo - p[1]) >= 0.3 for p in picks):
            picks.append((la, lo, float(sub[x, y])))
        if len(picks) == 5: break
    best = None
    for la, lo, s0 in picks:
        fl = np.round(np.arange(la - 0.15, la + 0.15 + 1e-9, 0.01), 6); fo = np.round(np.arange(lo - 0.15, lo + 0.15 + 1e-9, 0.01), 6)
        fl = fl[(fl >= la0 - 1e-9) & (fl <= la1 + 1e-9)]
        F = cum.shares(fl, fo)
        x, y = np.unravel_index(np.argmax(F), F.shape)
        c = dict(lat=float(fl[x]), lon=float(fo[y]), share=float(F[x, y]), lattice_lat=la, lattice_lon=lo, lattice_share=s0)
        if best is None or c['share'] > best['share']: best = c
    res['regions'][rn] = best
top_name, top = max(((k, v) for k, v in res['regions'].items() if k != 'north_of_48p5'), key=lambda kv: kv[1]['share'])
res['best'] = dict(region=top_name, **top, km_from_berlin_point=chk.km(top['lat'], top['lon'], 52.37, 12.68))
fixed = dict(berlin_point=(52.37, 12.68), valais_point=(46.0, 7.18), palatinate_point=(49.4, 12.4))
res['fixed'] = {k: cum.share(*v) for k, v in fixed.items()}
json.dump(res, open(outp, 'w'), indent=1)
b = res['best']
print(f"{name} | best {100 * b['share']:.4f}% at {b['lat']:.2f} N, {b['lon']:.2f} E ({b['region']}; {b['km_from_berlin_point']:.0f} km from 52.37 N 12.68 E) | " +
      ' | '.join(f"{k}: {100 * (v['share'] - b['share']):+.4f} ({(v['share'] - b['share']) * cum.total / 1e6:+.2f} M) at {v['lat']:.2f},{v['lon']:.2f}" for k, v in res['regions'].items()) +
      ' | fixed: ' + '; '.join(f"{k} {100 * (v - b['share']):+.4f}" for k, v in res['fixed'].items()), flush=True)
