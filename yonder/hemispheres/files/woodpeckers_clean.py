"""The woodpecker share again, after the review: three species keys that are not species are dropped.

usage: woodpeckers_clean.py BOX_DIR NAMES_DIR OUT_DIR

Dropped (found by the reviewer of 21 November; I had caught only the first):
  10341635  "Dendrocopos leucotos x major"   a hybrid
  12107555  "Picus spec"                      a placeholder name
   7340167  "Picoides fumigatus"              a second key for Leuconotopicus fumigatus (9000455)
With an empty drop list this reproduces woodpeckers.py (K = 5), which is checked first. Not scored.
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

bdir, ndir, odir = sys.argv[1], sys.argv[2], sys.argv[3]
DROP = {10341635, 12107555, 7340167}
EXTINCT = {'Campephilus imperialis', 'Campephilus principalis'}
K = 5
boxes = {}
for p in glob.glob(os.path.join(bdir, 'box_*.json')):
    m = re.match(r'box_(-?\d+)_(-?\d+)\.json$', os.path.basename(p))
    d = json.load(open(p, encoding='utf-8'))
    boxes[(int(m.group(1)), int(m.group(2)))] = {int(c['name']): int(c['count']) for fac in d.get('facets', []) for c in fac['counts']}
assert len(boxes) == 2592
names = {}
for p in glob.glob(os.path.join(ndir, '*.json')):
    d = json.load(open(p, encoding='utf-8'))
    names[int(d['key'])] = d.get('canonicalName') or d.get('scientificName')


def run(drop, label):
    species = {}
    for (south, west), counts in boxes.items():
        for key, n in counts.items():
            if n >= K and key not in drop:
                species.setdefault(key, []).append((south, west))
    wg = np.zeros((36, 72))
    for key, bl in species.items():
        for south, west in bl:
            wg[(south + 90) // 5, (west + 180) // 5] += 1 / len(bl)
    X, w, e = h.cells(wg)
    lats, lons, S = h.share_map(X, w, e, 1.0)
    a, b = np.unravel_index(np.argmax(S), S.shape)
    best, bc = S[a, b], h.unit(lats[a], lons[b])
    for dla in np.arange(-3, 3.01, 0.1):
        for dlo in np.arange(-3, 3.01, 0.1):
            c = h.unit(lats[a] + dla, lons[b] + dlo)
            s = h.share(X, w, c, e)
            if s > best:
                best, bc = s, c
    la, lo = h.latlon(bc)
    interior = abs(la - lats[a]) < 2.95 and abs(lo - lons[b]) < 2.95
    # how many species lie wholly inside, wholly outside, or across the edge (box centres, hard edge)
    inside = outside = across = 0
    for key, bl in species.items():
        d = np.array([h.unit(south + 2.5, west + 2.5) @ bc for south, west in bl])
        if (d > 0).all():
            inside += 1
        elif (d <= 0).all():
            outside += 1
        else:
            across += 1
    blon = -177.5 + 5 * np.arange(72)
    BLO = np.broadcast_to(blon, (36, 72))
    tot = wg.sum()
    sect = [100 * wg[BLO < -30].sum() / tot, 100 * wg[(BLO >= -30) & (BLO < 60)].sum() / tot, 100 * wg[BLO >= 60].sum() / tot]
    print(f'{label}: {len(species)} species; best {100 * best:.2f}% at {la:.2f}, {lo:.2f}' + ('' if interior else ' (AT THE EDGE OF THE REFINEMENT WINDOW)')
          + f'; least {100 * (1 - best):.2f}%; wholly inside {inside}, wholly outside {outside}, across the edge {across}; '
          f'sectors west of 30 W / 30 W to 60 E / east of 60 E: {sect[0]:.1f} / {sect[1]:.1f} / {sect[2]:.1f}')
    return dict(label=label, species=len(species), share=float(best), lat=float(la), lon=float(lo), inside=inside, outside=outside, across=across, sectors=sect, wg=wg)


r0 = run(set(), 'as scored (no key dropped)')
r1 = run(DROP, 'three non-species dropped')
ext = {k for k, v in names.items() if v in EXTINCT}
assert len(ext) == 2, ext
r2 = run(DROP | ext, 'also without the two extinct or probably extinct species')
for key in sorted(DROP):
    print('dropped', key, names.get(key))
# shares of the cleaned total at other centres
X, w, e = h.cells(r1['wg'])
for name, p in (('land centre 40.82 N 1.72 E', (40.82, 1.72)), ('people centre 52.37 N 12.68 E', (52.37, 12.68)), ('tropical Atlantic 5 N 30 W', (5, -30))):
    print(f'cleaned list, half centred on the {name}: {100 * h.share(X, w, h.unit(*p), e):.2f}%')
lat = -87.5 + 5 * np.arange(36); lon = -177.5 + 5 * np.arange(72)
LA, LO = np.meshgrid(lat, lon, indexing='ij')
out_m = (h.unit(LA, LO) @ h.unit(r1['lat'], r1['lon'])) <= 0
print(f"cleaned list, outside the best half: Americas {100 * r1['wg'][out_m & (LO < -30)].sum() / r1['wg'].sum():.1f}%, Asia {100 * r1['wg'][out_m & (LO >= 60)].sum() / r1['wg'].sum():.1f}%")
json.dump([{k: v for k, v in r.items() if k != 'wg'} for r in (r0, r1, r2)], open(os.path.join(odir, 'woodpeckers_clean.json'), 'w'), indent=1)
