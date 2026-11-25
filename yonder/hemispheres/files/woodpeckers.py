"""The hemisphere holding the most woodpecker species, from per-box species counts fetched by gbif_fetch.py.

usage: woodpeckers.py BOX_DIR OUT_DIR

A species is present in a 5 x 5 degree box if it has at least K records there (K = 5 is the scored choice; 1 and 20
are shown for comparison). Each species counts 1, spread equally over its boxes. W(c) = share of that total within
90 degrees of c, a box being represented by its centre, with a soft edge one box wide (hemilib.share).
"""
import glob
import json
import os
import re
import sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hemilib as h

bdir, odir = sys.argv[1], sys.argv[2]
KM = np.pi * h.R_KM / 180
boxes = {}
records = 0
for p in glob.glob(os.path.join(bdir, 'box_*.json')):
    m = re.match(r'box_(-?\d+)_(-?\d+)\.json$', os.path.basename(p))
    south, west = int(m.group(1)), int(m.group(2))
    d = json.load(open(p, encoding='utf-8'))
    counts = {}
    for fac in d.get('facets', []):
        assert fac['field'] == 'SPECIES_KEY', fac['field']
        for c in fac['counts']:
            counts[int(c['name'])] = int(c['count'])
    assert len(counts) < 1000, 'facet limit reached'
    boxes[(south, west)] = counts
    records += int(d['count'])
assert len(boxes) == 36 * 72, f'{len(boxes)} boxes, expected 2592'
print(f'boxes {len(boxes)}; records in all boxes {records:,} (a record on a shared edge is counted in both boxes)')
out = {'records': records}
maps = {}
for K in (5, 1, 20):
    species = {}
    for (south, west), counts in boxes.items():
        for key, n in counts.items():
            if n >= K:
                species.setdefault(key, []).append((south, west))
    wg = np.zeros((36, 72))
    rich = np.zeros((36, 72), dtype=int)
    for key, bl in species.items():
        for south, west in bl:
            wg[(south + 90) // 5, (west + 180) // 5] += 1 / len(bl)
            rich[(south + 90) // 5, (west + 180) // 5] += 1
    X, w, e = h.cells(wg)
    lats, lons, S = h.share_map(X, w, e, 1.0)
    a, b = np.unravel_index(np.argmax(S), S.shape)
    c0 = h.unit(lats[a], lons[b])
    # refine: every 0.1 degree within 2 degrees of the best 1-degree centre
    best, bc = S[a, b], c0
    for dla in np.arange(-2, 2.01, 0.1):
        for dlo in np.arange(-2, 2.01, 0.1):
            la = lats[a] + dla
            if abs(la) > 90:
                continue
            c = h.unit(la, lons[b] + dlo)
            s = h.share(X, w, c, e)
            if s > best:
                best, bc = s, c
    la, lo = h.latlon(bc)
    near = (S > S.max() - 0.01)
    LA, LO = np.meshgrid(lats, lons, indexing='ij')
    spread = float(h.angle_deg(h.unit(LA[near], LO[near]), bc).max() * KM)
    print(f'K = {K}: species present somewhere {len(species)}; best hemisphere holds {100 * best:.2f}% of them, centre {la:.1f}, {lo:.1f}; '
          f'least {100 * S.min():.2f}%; centres within 1 point of the best reach {spread:,.0f} km from it; richest box {rich.max()} species')
    out[f'K{K}'] = dict(species=len(species), share=float(best), lat=float(la), lon=float(lo), least=float(S.min()), spread_km=spread,
                        richest_box=int(rich.max()), keys=sorted(species) if K == 5 else None)
    if K == 5:
        maps = dict(wp_lats=lats, wp_lons=lons, wp_S=S, wp_rich=rich, wp_w=wg)
        # regional tallies of the species weight, for the note
        blat = -87.5 + 5 * np.arange(36); blon = -177.5 + 5 * np.arange(72)
        BLA, BLO = np.meshgrid(blat, blon, indexing='ij')
        tot = wg.sum()
        reg = {'Americas (west of 30 W)': BLO < -30, 'Europe and Africa (30 W to 60 E)': (BLO >= -30) & (BLO < 60), 'Asia and beyond (east of 60 E)': BLO >= 60}
        for name, msk in reg.items():
            print(f'    {name}: {100 * wg[msk].sum() / tot:.1f}% of the species total')
json.dump(out, open(os.path.join(odir, 'woodpeckers.json'), 'w'), indent=1)
np.savez_compressed(os.path.join(odir, 'woodpecker-maps.npz'), **maps)
print('written')
