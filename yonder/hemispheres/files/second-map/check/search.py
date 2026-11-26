"""Task A3: the best centre, by a search that does not use the author's library.

usage: python -I search.py NAME GRID.npy OUT.json [GLOBAL_STEP=0.25]

1. Hard-edged share for centres on a lattice of GLOBAL_STEP degrees over the whole sphere, on the full 0.05-degree
   grid (no coarsening: chk.Cum is exact and fast).
2. Every local maximum of that map within 0.15 points of the best; connected regions of the map within 0.05 and
   within 0.10 points of the best.
3. Europe (40 to 60 N, 0 to 25 E) at 0.05 degrees; then every local maximum there within 0.08 points of the best is
   refined at 0.01 degrees in a box of +-0.6 degrees.
4. Fixed centres: 52.37 N 12.68 E; 46.0 N 7.18 E; 49.4 N 12.4 E; the author's best centre if given; the Baltic's best
   (54 to 59 N, 13 to 22 E).
The surface is a step function of the centre (cells enter and leave one at a time), so "the" maximum at 0.01 degrees is
one of many near-equal steps; what matters is the height and the neighbourhood.
"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chk

name, gpath, outp = sys.argv[1:4]
gstep = float(sys.argv[4]) if len(sys.argv) > 4 else 0.25
P = np.load(gpath)
cum = chk.Cum(P)
res = dict(name=name, total=cum.total, global_step=gstep)

# ---- 1. whole sphere
lats = np.round(np.arange(-90, 90 + 1e-9, gstep), 6)
lons = np.round(np.arange(-180, 180 - 1e-9, gstep), 6)
S = cum.shares(lats, lons)
a, b = np.unravel_index(np.argmax(S), S.shape)
gbest = float(S[a, b])
res['global_best'] = dict(lat=float(lats[a]), lon=float(lons[b]), share=gbest)
print(f'{name}: total {cum.total / 1e9:.4f}; whole sphere at {gstep} deg: best {100 * gbest:.4f}% at {lats[a]:.2f} N, {lons[b]:.2f} E; lowest {100 * S.min():.3f}%', flush=True)

# ---- 2. local maxima and regions
Pd = np.pad(S, ((1, 1), (0, 0)), mode='constant', constant_values=-1)
Pd = np.concatenate([Pd[:, -1:], Pd, Pd[:, :1]], axis=1)
core = Pd[1:-1, 1:-1]
ismax = np.ones_like(core, dtype=bool)
for da in (-1, 0, 1):
    for db in (-1, 0, 1):
        if da or db:
            ismax &= core >= Pd[1 + da:Pd.shape[0] - 1 + da, 1 + db:Pd.shape[1] - 1 + db]
lm = [(float(S[i, j]), float(lats[i]), float(lons[j])) for i, j in np.argwhere(ismax & (S >= gbest - 0.0015))]
lm.sort(reverse=True)
res['global_local_maxima_within_0.15'] = lm
print(f'   local maxima of the {gstep}-degree map within 0.15 points of the best: {len(lm)}')
for s, la, lo in lm[:40]:
    print(f'      {100 * s:.4f}%  ({100 * (s - gbest):+.4f})  {la:7.2f} N {lo:8.2f} E   {chk.km(la, lo, 52.37, 12.68):6.0f} km from 52.37 N 12.68 E')


def regions(mask):
    """connected components (8-neighbour, longitude wraps) of a boolean map; returns list of dicts"""
    lab = np.zeros(mask.shape, dtype=np.int32); n = 0; outl = []
    idx = np.argwhere(mask)
    for i0, j0 in idx:
        if lab[i0, j0]: continue
        n += 1; stack = [(i0, j0)]; lab[i0, j0] = n; members = []
        while stack:
            i, j = stack.pop(); members.append((i, j))
            for da in (-1, 0, 1):
                for db in (-1, 0, 1):
                    ii, jj = i + da, (j + db) % mask.shape[1]
                    if 0 <= ii < mask.shape[0] and mask[ii, jj] and not lab[ii, jj]:
                        lab[ii, jj] = n; stack.append((ii, jj))
        mi = np.array(members)
        sv = S[mi[:, 0], mi[:, 1]]; k = int(np.argmax(sv))
        outl.append(dict(points=len(members), lat_min=float(lats[mi[:, 0].min()]), lat_max=float(lats[mi[:, 0].max()]),
                         lon_min=float(lons[mi[:, 1]].min()), lon_max=float(lons[mi[:, 1]].max()),
                         top_share=float(sv[k]), top_lat=float(lats[mi[k, 0]]), top_lon=float(lons[mi[k, 1]])))
    outl.sort(key=lambda r: -r['top_share'])
    return outl


for tol, key in ((0.0005, 'regions_within_0.05'), (0.0010, 'regions_within_0.10'), (0.0020, 'regions_within_0.20')):
    rg = regions(S >= gbest - tol)
    res[key] = rg
    print(f'   lattice points within {100 * tol:.2f} points of the best: {int((S >= gbest - tol).sum())} in {len(rg)} connected region(s):')
    for r in rg[:12]:
        print(f"      {r['points']:5d} points, lat {r['lat_min']:.2f} to {r['lat_max']:.2f}, lon {r['lon_min']:.2f} to {r['lon_max']:.2f}; top {100 * r['top_share']:.4f}% at {r['top_lat']:.2f} N, {r['top_lon']:.2f} E")
# the best centre outside Europe-and-near (more than 2000 km from 50 N 10 E)
far = np.array([[chk.km(la, lo, 50.0, 10.0) > 2000 for lo in lons[::4]] for la in lats[::4]])
Sf = S[::4, ::4]
k = np.argmax(np.where(far, Sf, -1)); ia, ib = np.unravel_index(k, Sf.shape)
res['best_beyond_2000km_of_50N10E'] = dict(lat=float(lats[::4][ia]), lon=float(lons[::4][ib]), share=float(Sf[ia, ib]))
print(f"   best lattice point (every 4th) more than 2000 km from 50 N 10 E: {100 * Sf[ia, ib]:.4f}% at {lats[::4][ia]:.2f} N, {lons[::4][ib]:.2f} E ({100 * (Sf[ia, ib] - gbest):+.3f} points)")

# ---- 3. Europe at 0.05, then 0.01 around the summits
elat = np.round(np.arange(40, 60 + 1e-9, 0.05), 6); elon = np.round(np.arange(0, 25 + 1e-9, 0.05), 6)
E = cum.shares(elat, elon)
a, b = np.unravel_index(np.argmax(E), E.shape)
ebest = float(E[a, b])
print(f'   Europe 40-60 N, 0-25 E at 0.05 deg: best {100 * ebest:.4f}% at {elat[a]:.2f} N, {elon[b]:.2f} E')
# local maxima of a smoothed copy (3x3 mean) to avoid one summit per step of the staircase
from numpy.lib.stride_tricks import sliding_window_view
k5 = 5
Es = sliding_window_view(np.pad(E, k5 // 2, mode='edge'), (k5, k5)).mean(axis=(2, 3))
win = 21          # a summit = the highest smoothed value within +-0.5 degrees
Em = sliding_window_view(np.pad(Es, win // 2, mode='constant', constant_values=-1), (win, win)).max(axis=(2, 3))
cand = np.argwhere((Es >= Em) & (Es >= Es.max() - 0.0010))
summits = []
for i, j in cand:
    la0, lo0 = float(elat[i]), float(elon[j])
    fl = np.round(np.arange(la0 - 0.6, la0 + 0.6 + 1e-9, 0.01), 6); fo = np.round(np.arange(lo0 - 0.6, lo0 + 0.6 + 1e-9, 0.01), 6)
    F = cum.shares(fl, fo)
    x, y = np.unravel_index(np.argmax(F), F.shape)
    top = float(F[x, y])
    near = F >= top - 0.00002          # all centres within 0.002 points of this summit's top: how wide is "the" summit?
    xi = np.argwhere(near)
    summits.append(dict(lat=float(fl[x]), lon=float(fo[y]), share=top, smoothed_share=float(Es[i, j]), from_lat=la0, from_lon=lo0,
                        km_from_berlin_point=chk.km(float(fl[x]), float(fo[y]), 52.37, 12.68),
                        within_0002_lat=[float(fl[xi[:, 0].min()]), float(fl[xi[:, 0].max()])], within_0002_lon=[float(fo[xi[:, 1].min()]), float(fo[xi[:, 1].max()])],
                        within_0002_n=int(near.sum())))
summits.sort(key=lambda s: -s['share'])
res['europe_best_005'] = dict(lat=float(elat[a]), lon=float(elon[b]), share=ebest)
res['summits'] = summits
best = summits[0]
print(f'   summits in Europe (refined at 0.01 deg), all within 0.10 points (smoothed) of the top:')
for s in summits:
    print(f"      {100 * s['share']:.4f}% ({100 * (s['share'] - best['share']):+.4f}) at {s['lat']:.2f} N, {s['lon']:.2f} E; {s['km_from_berlin_point']:.0f} km from 52.37 N 12.68 E; "
          f"centres within 0.002 points of it: {s['within_0002_n']}, lat {s['within_0002_lat'][0]:.2f}-{s['within_0002_lat'][1]:.2f}, lon {s['within_0002_lon'][0]:.2f}-{s['within_0002_lon'][1]:.2f}")
res['best'] = best

# how wide is the top in Europe? lattice points (0.05) within 0.01, 0.02, 0.05 points of the best
for tol in (0.0001, 0.0002, 0.0005):
    mk = E >= best['share'] - tol
    ii = np.argwhere(mk)
    if len(ii):
        res[f'europe_within_{tol}'] = dict(n=int(mk.sum()), lat=[float(elat[ii[:, 0].min()]), float(elat[ii[:, 0].max()])], lon=[float(elon[ii[:, 1].min()]), float(elon[ii[:, 1].max()])])
        print(f"   centres (0.05-deg lattice) within {100 * tol:.2f} points of the best: {int(mk.sum())}; lat {elat[ii[:, 0].min()]:.2f} to {elat[ii[:, 0].max()]:.2f}, lon {elon[ii[:, 1].min()]:.2f} to {elon[ii[:, 1].max()]:.2f}")

# ---- 4. fixed centres and regional bests
def regional(lat0, lat1, lon0, lon1):
    i0, i1 = np.searchsorted(elat, [lat0, lat1 + 1e-9]); j0, j1 = np.searchsorted(elon, [lon0, lon1 + 1e-9])
    sub = E[i0:i1, j0:j1]; x, y = np.unravel_index(np.argmax(sub), sub.shape)
    return dict(lat=float(elat[i0 + x]), lon=float(elon[j0 + y]), share=float(sub[x, y]))
fixed = dict(berlin_point=(52.37, 12.68), valais_point=(46.0, 7.18), palatinate_point=(49.4, 12.4), rankin_point=(46.5, 7.0))
res['fixed'] = {k: cum.share(*v) for k, v in fixed.items()}
res['regional'] = dict(alps_43_47p5N_5_9E=regional(43, 47.5, 5, 9), palatinate_48p5_50p5N_11_14E=regional(48.5, 50.5, 11, 14),
                       berlin_51_53p5N_11_15E=regional(51, 53.5, 11, 15), baltic_54_59N_13_22E=regional(54, 59, 13, 22),
                       north_of_48p5=regional(48.5, 60, 0, 25), south_of_47p5=regional(40, 47.5, 0, 25), between_47p5_48p5=regional(47.5, 48.5, 0, 25))
print('   fixed centres: ' + '; '.join(f"{k} {100 * v:.4f}% ({100 * (v - best['share']):+.4f})" for k, v in res['fixed'].items()))
print('   regional bests (0.05-deg lattice): ' + '; '.join(f"{k} {100 * v['share']:.4f}% ({100 * (v['share'] - best['share']):+.4f}) at {v['lat']:.2f} N, {v['lon']:.2f} E" for k, v in res['regional'].items()))
json.dump(res, open(outp, 'w'), indent=1)
np.save(outp.replace('.json', '.europe005.npy'), E.astype(np.float32))
np.save(outp.replace('.json', '.global.npy'), S.astype(np.float32))
print(f'{name}: done', flush=True)
