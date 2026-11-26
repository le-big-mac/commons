"""The half with the most people on one 0.05-degree population grid: total, best centre, the three regional summits
by climbing, the shares of four fixed halves with a hard edge, L, and the two slivers.
usage: run_people2.py LABEL GRID.npy OUT.json
Uses my own hemilib (from /srv/commons/hemispheres-agent3) exactly as people_epochs.py does for the GHS grids."""
import sys, json, numpy as np
sys.path.insert(0, '/srv/commons/hemispheres-agent3')
import hemilib as h
label, path, outp = sys.argv[1:4]
pop = np.load(path); assert pop.shape == (3600, 7200), pop.shape
KM = np.pi * h.R_KM / 180

def climb(X, w, e, start):
    c = h.unit(*start)
    for half, step in ((0.6, 0.05), (0.12, 0.01)):
        for it in range(400):
            lc = h.Local(X, w, e, c, half * 1.5)
            o, g, n_, e_ = lc.grid(half, step)
            i, j = np.unravel_index(np.nanargmax(g), g.shape)
            if o[i] == 0 and o[j] == 0: break
            c = lc.point(o[i], o[j], n_, e_)
    return c, h.share(X, w, c, e)

lat = np.radians(-90 + (np.arange(3600) + 0.5) * 0.05); lon = np.radians(-180 + (np.arange(7200) + 0.5) * 0.05)
def inside(la, lo):
    c = h.unit(la, lo)
    return ((np.cos(lat)[:, None] * np.cos(lon)[None, :]) * c[0] + (np.cos(lat)[:, None] * np.sin(lon)[None, :]) * c[1] + np.sin(lat)[:, None] * c[2]) > 0
tot = float(pop.sum())
FIX = dict(rankin=(46.5, 7.0), valais=(46.0, 7.18), palatinate=(49.4, 12.4), berlin=(52.37, 12.68))
hard = {}
masks = {}
for k, (la, lo) in FIX.items():
    masks[k] = inside(la, lo); hard[k] = float(pop[masks[k]].sum() / tot)
out = dict(label=label, total=tot, hard=hard, L=100 * (hard['berlin'] - hard['valais']),
           only_berlin=float(pop[masks['berlin'] & ~masks['valais']].sum()), only_valais=float(pop[~masks['berlin'] & masks['valais']].sum()))
r = h.best_cap(pop, verbose=False)
X, w, e = r['X'], r['w'], r['eps']
out['best'] = dict(lat=float(r['lat']), lon=float(r['lon']), share=float(r['share']))
out['km_best_to_berlin'] = float(h.angle_deg(h.unit(r['lat'], r['lon']), h.unit(52.37, 12.68)) * KM)
out['climb'] = {}
for k, start in (('alps', (45.1, 6.7)), ('palatinate', (49.4, 12.4)), ('berlin', (52.37, 12.68))):
    c, s = climb(X, w, e, start); la, lo = h.latlon(c)
    out['climb'][k] = dict(lat=float(la), lon=float(lo), share=float(s))
json.dump(out, open(outp, 'w'), indent=1)
print(f"{label}: total {tot / 1e9:.4f} thousand million; best {100 * out['best']['share']:.3f}% at {out['best']['lat']:.2f} N, {out['best']['lon']:.2f} E ({out['km_best_to_berlin']:.0f} km from 52.37, 12.68)")
print('   hard-edged halves: ' + '; '.join(f"{k} {100 * v:.3f}%" for k, v in hard.items()) + f"; L = {out['L']:+.3f} points")
print('   climbing: ' + '; '.join(f"{k}: {100 * v['share']:.3f}% at {v['lat']:.2f}, {v['lon']:.2f}" for k, v in out['climb'].items()))
print(f"   only in the Berlin half {out['only_berlin'] / 1e6:.1f} million; only in the Valais half {out['only_valais'] / 1e6:.1f} million")
