"""The summits of the people share in every epoch, searched finely; and the wide map of the 2020 share.

usage: people_fine.py GRID_DIR OUT_DIR

Written after the third review (21 November), which showed that hemilib.summits() keeps one point per +-4 degree
box and so loses nearby, nearly equal summits (it had put the summit of 2000-2010 at 46.0 N, 7.2 E when slightly
higher ones lie 110-185 km to the south). Here every local maximum of the 0.25-degree lattice in each box is
climbed separately (steps of 0.05 then 0.01 degree), and all summits within 0.06 points of the best are listed.
Also writes OUT_DIR/wide-people.npz (the 2020 share on a lattice of 0.1 degree, +-8 degrees around 49.5 N, 9.5 E),
which an earlier, unsaved command had made at 0.2 degree.
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


def local_maxima(G):
    core = G[1:-1, 1:-1]
    m = np.ones_like(core, dtype=bool)
    for da in (-1, 0, 1):
        for db in (-1, 0, 1):
            if da or db:
                m &= core >= G[1 + da:G.shape[0] - 1 + da, 1 + db:G.shape[1] - 1 + db]
    return [(i + 1, j + 1) for i, j in np.argwhere(m)]


def fine_summits(pop, tol_coarse=0.004, tol_box=0.0015, keep=0.0006):
    Xc, wc, ec = h.cells(h.coarsen(pop, 10))
    lats, lons, S = h.share_map(Xc, wc, ec, 1.0)
    P = np.pad(S, ((1, 1), (0, 0)), mode='edge'); P = np.concatenate([P[:, -1:], P, P[:, :1]], axis=1)
    cand = [(lats[i - 1], lons[j - 1]) for i, j in local_maxima(P) if P[i, j] >= S.max() - tol_coarse]
    X, w, e = h.cells(pop)
    found = []
    for la0, lo0 in cand:
        loc = h.Local(X, w, e, h.unit(la0, lo0), 6.0)
        offs, G, north, east = loc.grid(4.0, 0.25)
        gm = np.nanmax(G)
        for i, j in local_maxima(G):
            if G[i, j] < gm - tol_box:
                continue
            c, s = climb(X, w, e, loc.point(offs[i], offs[j], north, east))
            if not any(h.angle_deg(c, f[1]) < 0.15 for f in found):
                found.append((s, c))
    found.sort(key=lambda f: -f[0])
    best = found[0][0]
    return [(s, *map(float, h.latlon(c))) for s, c in found if s >= best - keep], X, w, e


out = []
for year, name in ((1975, 'pop005_1975'), (2000, 'pop005_2000'), (2005, 'pop005_2005'), (2010, 'pop005_2010'), (2015, 'pop005_2015'),
                   (2020, 'pop005'), (2025, 'pop005_2025'), (2030, 'pop005_2030')):
    pop = np.load(f'{gdir}/{name}.npy')
    S, X, w, e = fine_summits(pop)
    print(f'{year}: ' + '; '.join(f'{100 * s:.4f}% at {la:.2f}, {lo:.2f}' for s, la, lo in S), flush=True)
    out.append(dict(year=year, total=float(pop.sum()), summits=[dict(share=s, lat=la, lon=lo) for s, la, lo in S]))
    if year == 2020:
        c_mid = h.unit(49.5, 9.5)
        loc = h.Local(X, w, e, c_mid, 12.0)
        offs, G, north, east = loc.grid(8.0, 0.1)
        np.savez_compressed(f'{odir}/wide-people.npz', offs=offs, G=G, north=north, east=east, c_mid=c_mid)
        best_c = h.unit(S[0][1], S[0][2])
        DN, DE = np.meshgrid(offs, offs, indexing='ij'); T = np.hypot(DN, DE)
        C = np.cos(np.radians(T))[..., None] * c_mid + np.sin(np.radians(T))[..., None] * ((DN[..., None] * north + DE[..., None] * east) / np.maximum(T, 1e-12)[..., None])
        dist = h.angle_deg(C, best_c) * KM
        for tol in (0.01, 0.05, 0.1):
            m = (S[0][0] - G) * 100 < tol
            print(f'    2020: centres within {tol} points of the best reach {dist[m].max():.0f} km from it (lattice of 0.1 degree)', flush=True)
json.dump(out, open(f'{odir}/people_fine.json', 'w'), indent=1)
print('written')
