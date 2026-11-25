"""Check of the ridge map's data: wide.npz (shares of land for centres on a grid around 44.5 N, 0.5 E)."""
import sys, numpy as np
W = np.load(sys.argv[1])
offs, G, north, east, c0 = W['offs'], W['G'], W['north'], W['east'], W['c_mid']
R = 6371.0088; KM = np.pi * R / 180
LAND = 146735767.0
def unit(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])
def latlon(v):
    return float(np.degrees(np.arcsin(v[2]))), float(np.degrees(np.arctan2(v[1], v[0])))
def point(dn, de):
    t = np.hypot(dn, de)
    if t == 0: return c0
    d = (dn * north + de * east) / t
    return np.cos(np.radians(t)) * c0 + np.sin(np.radians(t)) * d
def proj(lat, lon):
    v = unit(lat, lon); t = np.degrees(np.arccos(np.clip(v @ c0, -1, 1)))
    s = np.sin(np.radians(max(t, 1e-12)))
    return t * (v @ east) / s, t * (v @ north) / s      # degrees east, north
def gc(a, b):
    return float(np.degrees(np.arccos(np.clip(unit(*a) @ unit(*b), -1, 1))) * KM)
print('grid', G.shape, 'offs', offs[0], offs[-1], 'step', offs[1] - offs[0], 'centre', latlon(c0), 'nan cells', int(np.isnan(G).sum()))
iy, ix = np.unravel_index(np.nanargmax(G), G.shape)
S = latlon(point(offs[iy], offs[ix]))
print(f'best on grid: {100 * G[iy, ix]:.4f}% at {S[0]:.2f}, {S[1]:.2f}; x,y km = {offs[ix] * KM:+.0f}, {offs[iy] * KM:+.0f}')
# northern summit: best within 150 km of 47.42, -2.36
pe, pn = proj(47.42, -2.36)
Y, X = np.meshgrid(offs, offs, indexing='ij')
near = (X - pe) ** 2 + (Y - pn) ** 2 < (150 / KM) ** 2
Gn = np.where(near, np.nan_to_num(G, nan=-1), -1); jy, jx = np.unravel_index(np.argmax(Gn), G.shape)
N = latlon(point(offs[jy], offs[jx]))
print(f'northern summit on grid: {100 * G[jy, jx]:.4f}% at {N[0]:.2f}, {N[1]:.2f}; x,y km = {offs[jx] * KM:+.0f}, {offs[jy] * KM:+.0f}')
gap = (G[iy, ix] - G[jy, jx])
print(f'gap {100 * gap:.4f} points = {gap * LAND:,.0f} km2 of {LAND:,.0f}; distance between the two on the sphere {gc(S, N):.0f} km; on the map {np.hypot(offs[ix] - offs[jx], offs[iy] - offs[jy]) * KM:.0f} km')
print(f'note summits 40.83,1.72 and 47.42,-2.36: {gc((40.83, 1.72), (47.42, -2.36)):.1f} km apart; 40.82,1.72: {gc((40.82, 1.72), (47.42, -2.36)):.1f}')
print(f'land in best half {G[iy, ix] * LAND:,.0f}; in northern {G[jy, jx] * LAND:,.0f}')
# values at named places (bilinear)
def at(lat, lon):
    e, n = proj(lat, lon)
    fx = (e - offs[0]) / (offs[1] - offs[0]); fy = (n - offs[0]) / (offs[1] - offs[0])
    i, j = int(np.floor(fy)), int(np.floor(fx)); a, b = fy - i, fx - j
    return (1 - a) * (1 - b) * G[i, j] + (1 - a) * b * G[i, j + 1] + a * (1 - b) * G[i + 1, j] + a * b * G[i + 1, j + 1]
for name, p in (('Nantes', (47 + 13 / 60, -(1 + 32 / 60))), ('Ile Dumet', (47 + 24 / 60 + 42 / 3600, -(2 + 37 / 60 + 15 / 3600))), ('Tarragona', (41.119, 1.245)),
                ('Nerac', (44.136, 0.339)), ('Affholder 1st Breton', (47.40, -2.32)), ('Affholder 1st Med', (40.82, 1.74)), ('Affholder 2nd Breton', (47.412, -2.493)), ('Affholder 2nd Med', (40.68, 1.59)),
                ('note Catalan', (40.83, 1.72)), ('note Breton', (47.42, -2.36))):
    v = at(*p)
    print(f'  {name:22s} {100 * v:.4f}%  loss {100 * (G[iy, ix] - v):.4f} points = {(G[iy, ix] - v) * LAND:,.0f} km2; {gc(p, S):.0f} km from grid best, {gc(p, N):.0f} km from grid northern summit; from note summits {gc(p, (40.83, 1.72)):.1f} / {gc(p, (47.42, -2.36)):.1f} km')
# the col: highest path between the two summits = max over paths of min G. Flood from the top.
import heapq
Gz = np.nan_to_num(G, nan=-1)
seen = np.zeros(G.shape, bool); heap = [(-Gz[iy, ix], iy, ix)]; low = Gz[iy, ix]; colpos = None
while heap:
    v, y, x = heapq.heappop(heap)
    if seen[y, x]: continue
    seen[y, x] = True
    if -v < low: low = -v; colpos = (y, x)
    if (y, x) == (jy, jx): break
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            yy, xx = y + dy, x + dx
            if 0 <= yy < G.shape[0] and 0 <= xx < G.shape[1] and not seen[yy, xx]:
                heapq.heappush(heap, (-Gz[yy, xx], yy, xx))
cl = latlon(point(offs[colpos[0]], offs[colpos[1]]))
print(f'col between the summits: {100 * low:.4f}% at {cl[0]:.2f}, {cl[1]:.2f}: {100 * (G[iy, ix] - low):.4f} points below the best = {(G[iy, ix] - low) * LAND:,.0f} km2; {100 * (G[jy, jx] - low):.4f} below the northern summit; {gc(cl, (44.136, 0.339)):.0f} km from Nerac')
# sizes of the patches inside the contours
loss = (G[iy, ix] - Gz) * 100
from collections import deque
def comps(mask):
    lab = np.zeros(mask.shape, int); k = 0; out = []
    for y0, x0 in np.argwhere(mask):
        if lab[y0, x0]: continue
        k += 1; q = deque([(y0, x0)]); lab[y0, x0] = k; cells = []
        while q:
            y, x = q.popleft(); cells.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < mask.shape[0] and 0 <= xx < mask.shape[1] and mask[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = k; q.append((yy, xx))
        out.append(cells)
    return out
for lev in (0.01, 0.05, 0.1):
    cs = comps(loss < lev)
    print(f'loss < {lev}: {len(cs)} patch(es)')
    for c in cs:
        ys = np.array([offs[y] for y, x in c]); xs = np.array([offs[x] for y, x in c])
        ext = [latlon(point(ys[k], xs[k])) for k in (np.argmax(ys), np.argmin(ys))]
        print(f'    {len(c)} cells, about {len(c) * (0.1 * KM) ** 2:,.0f} km2; northmost {ext[0][0]:.2f},{ext[0][1]:.2f}; southmost {ext[1][0]:.2f},{ext[1][1]:.2f}; length N-S {np.ptp(ys) * KM:.0f} km, E-W {np.ptp(xs) * KM:.0f} km')
# where the labels sit
print('labels (km east, km north of the middle) -> lat, lon')
for name, x, y in (('FRANCE', 250, 270), ('SPAIN', -430, -600), ('ITALY', 690, 150), ('ENGLAND', -100, 830), ('Bay of Biscay', -520, 60), ('Mediterranean Sea', 420, -700)):
    p = latlon(point(y / KM, x / KM)); print(f'  {name:18s} {p[0]:.2f} N, {p[1]:.2f} E')
print('range of loss over the map: max', float(np.nanmax(loss)))
