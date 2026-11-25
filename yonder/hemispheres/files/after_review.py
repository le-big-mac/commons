"""Computations made in answer to the review of 21 November; none is scored.

usage: after_review.py GRID_DIR OUT_DIR

 1. How flat the land maximum is, measured on a box wide enough to hold both summits (the scored run's +-3 degree
    box truncated the 0.05 and 0.1 point regions), and the same for people.
 2. The true overlap between the land polygons and the ice-shelf polygons.
 3. L(best) - L(Nantes) and L(best) - L(Ile Dumet) under three readings of "hemisphere centred on a named point".
 4. Every summit of the land share and of the people share within 0.3 points of the best (multi-start search).
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
E2 = 0.00669437999014
NANTES = (47 + 13 / 60, -(1 + 32 / 60))
DUMET = (47 + 24 / 60 + 42 / 3600, -(2 + 37 / 60 + 15 / 3600))
out = {}


def geocentric(lat_deg):
    return np.degrees(np.arctan((1 - E2) * np.tan(np.radians(np.asarray(lat_deg, dtype=np.float64)))))


print('== 1. flatness on wide boxes')
for tag, npz, best_pt, word in (('land', 'wide.npz', (40.819, 1.724), 'land'), ('people', 'wide-people.npz', (52.369, 12.679), 'people')):
    Wd = np.load(f'{odir}/{npz}')
    offs, G, north, east, c0 = Wd['offs'], Wd['G'], Wd['north'], Wd['east'], Wd['c_mid']
    step = offs[1] - offs[0]
    DN, DE = np.meshgrid(offs, offs, indexing='ij')
    T = np.hypot(DN, DE)
    C = np.cos(np.radians(T))[..., None] * c0 + np.sin(np.radians(T))[..., None] * ((DN[..., None] * north + DE[..., None] * east) / np.maximum(T, 1e-12)[..., None])
    dist = h.angle_deg(C, h.unit(*best_pt)) * KM
    out[tag] = {}
    for tol in (0.01, 0.05, 0.1):
        m = (np.nanmax(G) - G) * 100 < tol
        touches = bool(m[0].any() or m[-1].any() or m[:, 0].any() or m[:, -1].any())
        # count connected pieces (4-neighbours)
        seen = np.zeros_like(m); pieces = 0
        for i, j in np.argwhere(m):
            if seen[i, j]:
                continue
            pieces += 1
            stack = [(i, j)]; seen[i, j] = True
            while stack:
                a, b = stack.pop()
                for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    x, y = a + da, b + db
                    if 0 <= x < m.shape[0] and 0 <= y < m.shape[1] and m[x, y] and not seen[x, y]:
                        seen[x, y] = True; stack.append((x, y))
        area = float(m.sum() * (step * KM) ** 2)
        out[tag][str(tol)] = dict(max_km=float(dist[m].max()), area_km2=area, pieces=pieces, touches_edge=touches)
        print(f'  {word}: centres within {tol} points of the best reach {dist[m].max():.0f} km from it, cover {area:,.0f} km2 in {pieces} piece(s)' + ('  (REACHES THE EDGE OF THE BOX)' if touches else ''))

print('== 2. overlap of land and ice-shelf polygons')
land = h.area_weights(np.load(f'{gdir}/land10.npy')); cov_l = np.load(f'{gdir}/land10.npy'); cov_s = np.load(f'{gdir}/shelf10.npy')
both = h.area_weights(np.maximum(cov_l + cov_s - 1, 0)).sum()
shared = h.area_weights(np.minimum(cov_l, cov_s)).sum()
print(f'  cells where coverage of land plus coverage of shelf exceeds 1: {both:,.1f} km2 (a lower bound on the overlap)')
print(f'  the figure printed by the scored run as "overlap" ({shared:,.0f} km2) is the sum of min(land, shelf): cells the two share along their common boundary')
out['overlap_lower_bound_km2'] = float(both)

print('== 3. named points under three readings')
cov = np.load(f'{gdir}/land10.npy')
rows = []
for name, wg, latmap in (('map latitude used as latitude on a sphere (as sealed)', h.area_weights(cov), None),
                         ('equal-area sphere', h.area_weights(cov, h.authalic), h.authalic),
                         ('plane through the centre of the ellipsoid, true areas', h.area_weights(cov, h.authalic), geocentric)):
    X, w, e = h.cells(wg, latmap)
    f = (lambda p: (float(latmap(p[0])), p[1])) if latmap else (lambda p: p)
    S = h.summits(wg, latmap=latmap, tol=0.003)
    best = S[0]['share']
    ln = h.share(X, w, h.unit(*f(NANTES)), e); ld = h.share(X, w, h.unit(*f(DUMET)), e)
    rows.append(dict(name=name, best=best, nantes=ln, dumet=ld))
    print(f'  {name}: best {100 * best:.4f}%; best - Nantes {100 * (best - ln):.4f}; best - Dumet {100 * (best - ld):.4f}; Dumet - Nantes {100 * (ld - ln):+.4f}')
    if latmap is None:
        print('  summits of the land share within 0.3 points of the best:')
        for s in S:
            print(f'      {100 * s["share"]:.4f}% at {s["lat"]:.2f}, {s["lon"]:.2f}' + ('  (edge of last box)' if s['on_edge_of_last_box'] else ''))
        out['land_summits'] = [dict(lat=s['lat'], lon=s['lon'], share=s['share']) for s in S]
out['named'] = rows

print('== 4. summits of the people share, every epoch')
ep = []
for year, name in ((1975, 'pop005_1975'), (2000, 'pop005_2000'), (2005, 'pop005_2005'), (2010, 'pop005_2010'), (2015, 'pop005_2015'),
                   (2020, 'pop005'), (2025, 'pop005_2025'), (2030, 'pop005_2030')):
    pop = np.load(f'{gdir}/{name}.npy')
    S = h.summits(pop, tol=0.003)
    line = f'  {year}: ' + '; '.join(f'{100 * s["share"]:.3f}% at {s["lat"]:.2f}, {s["lon"]:.2f}' for s in S[:6])
    print(line, flush=True)
    ep.append(dict(year=year, total=float(pop.sum()), summits=[dict(lat=s['lat'], lon=s['lon'], share=s['share']) for s in S]))
out['people_summits'] = ep
json.dump(out, open(f'{odir}/after_review.json', 'w'), indent=1)
print('written')
