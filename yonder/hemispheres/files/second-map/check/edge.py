"""Task A5: does the comparison of the two halves depend on country totals more than on the spreading inside countries?

usage: python -I edge.py OUT.json NAME=GRID.npy ...        (the first two grids named are also compared cell by cell)

For each grid:
 (a) people within d degrees of arc of the edge of the half centred at 52.37 N 12.68 E, and of the half centred at
     46.0 N 7.18 E, for several d, inside and outside, and by rough region; the most populous half-degree squares
     within 1 degree of each edge (to name the cities);
 (b) the two slivers (only in the Berlin half; only in the Valais half) by rough region;
 (c) a blur test: every 0.05-degree cell's people are spread evenly over a square of side s degrees around it, and the
     difference Berlin minus Valais is counted again. This is what a different spreading at that scale could do.
For the first two grids together:
 (d) hybrids: grid A's totals in blocks of side s, spread inside each block as grid B spreads them (and the reverse).
     If the answer follows the totals at large s, the totals of large areas decide it; if it follows the pattern, the
     spreading inside them does.
"""
import sys, json, os
import numpy as np
from scipy.ndimage import uniform_filter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chk

B = (52.37, 12.68); V = (46.0, 7.18)
LA = np.radians(chk.LAT)[:, None]; LO = np.radians(chk.LON)[None, :]


def signed_deg(c):
    u = chk.unit(*c)
    d = np.cos(LA) * np.cos(LO) * u[0] + np.cos(LA) * np.sin(LO) * u[1] + np.sin(LA) * u[2]
    return np.degrees(np.arcsin(np.clip(d, -1, 1)))          # > 0 inside; = angular distance from the edge


dB = signed_deg(B); dV = signed_deg(V)
inB = dB > 0; inV = dV > 0
LON2 = np.broadcast_to(chk.LON[None, :], dB.shape); LAT2 = np.broadcast_to(chk.LAT[:, None], dB.shape)

REG = [  # name, lon_w, lon_e, lat_s, lat_n   (rough boxes; first match wins)
    ('Philippines and nearby (115-130 E, 3-22 N)', 115, 130, 3, 22),
    ('Malay Peninsula, Singapore, Sumatra, west Borneo (94-115 E, 8 S-9 N)', 94, 115, -8, 9),
    ('other Asia and Pacific east of 90 E', 90, 180, -90, 90),
    ('Pacific west of 110 W', -180, -110, -90, 90),
    ('Mexico and Central America (110-82 W, north of 6 N)', -110, -82, 6, 40),
    ('Ecuador, Peru, south Colombia (82-70 W)', -82, -70, -25, 6),
    ('Bolivia and the inland (70-57 W)', -70, -57, -30, 6),
    ('Brazil east of 57 W, Paraguay, north-east Argentina', -57, -30, -40, 6),
    ('elsewhere', -180, 180, -90, 90)]
regid = np.full(dB.shape, len(REG) - 1, dtype=np.int8)
done = np.zeros(dB.shape, dtype=bool)
for k, (nm, w, e, s, n) in enumerate(REG):
    m = (LON2 >= w) & (LON2 < e) & (LAT2 >= s) & (LAT2 < n) & ~done
    regid[m] = k; done |= m


def by_region(P, mask):
    return {REG[k][0]: float(P[mask & (regid == k)].sum()) for k in range(len(REG)) if (mask & (regid == k)).any() and P[mask & (regid == k)].sum() > 0}


def diffM(P):
    return float(P[inB].sum() - P[inV].sum()) / 1e6


def coarse_top(P, mask, n=14, f=10):
    """most populous half-degree squares among the cells in mask"""
    Q = np.where(mask, P, 0.0).reshape(chk.H // f, f, chk.W // f, f).sum(axis=(1, 3))
    idx = np.argsort(Q.ravel())[::-1][:n]
    outl = []
    for k in idx:
        i, j = divmod(int(k), chk.W // f)
        outl.append((round(-90 + (i + 0.5) * f * chk.CELL, 2), round(-180 + (j + 0.5) * f * chk.CELL, 2), float(Q[i, j])))
    return outl


out = {}
grids = {}
for spec in sys.argv[2:]:
    name, path = spec.split('=')
    P = np.load(path); grids[name] = P
    tot = float(P.sum())
    r = dict(total=tot, diff_millions=diffM(P))
    print(f'===== {name}: total {tot / 1e9:.4f} thousand million; Berlin half minus Valais half {r["diff_millions"]:+.2f} million')
    # (a) near the edges
    for cname, d, ins in (('Berlin', dB, inB), ('Valais', dV, inV)):
        r[f'near_{cname}'] = {}
        print(f'  people within d of the edge of the {cname} half:')
        for dd in (0.05, 0.1, 0.25, 0.5, 1.0, 2.0):
            m = np.abs(d) < dd
            a_in = float(P[m & ins].sum()); a_out = float(P[m & ~ins].sum())
            r[f'near_{cname}'][str(dd)] = dict(inside=a_in, outside=a_out)
            print(f'     d = {dd:4.2f} deg ({dd * 111.2:5.0f} km): {(a_in + a_out) / 1e6:7.2f} million ({a_in / 1e6:6.2f} just inside, {a_out / 1e6:6.2f} just outside)')
        m1 = np.abs(d) < 1.0
        r[f'near_{cname}_1deg_by_region'] = by_region(P, m1)
        print('     within 1 degree, by region: ' + '; '.join(f'{k}: {v / 1e6:.2f} M' for k, v in r[f'near_{cname}_1deg_by_region'].items()))
        top = coarse_top(P, m1)
        r[f'near_{cname}_1deg_top_squares'] = top
        print('     most populous half-degree squares within 1 degree (lat, lon of the square\'s centre, millions): ' + '; '.join(f'({a:.2f}, {b:.2f}) {c / 1e6:.2f}' for a, b, c in top))
    # (b) slivers
    ob = inB & ~inV; ov = inV & ~inB
    r['only_berlin'] = float(P[ob].sum()); r['only_valais'] = float(P[ov].sum())
    r['only_berlin_by_region'] = by_region(P, ob); r['only_valais_by_region'] = by_region(P, ov)
    print(f'  only in the Berlin half {r["only_berlin"] / 1e6:.2f} M: ' + '; '.join(f'{k}: {v / 1e6:.2f}' for k, v in r['only_berlin_by_region'].items()))
    print(f'  only in the Valais half {r["only_valais"] / 1e6:.2f} M: ' + '; '.join(f'{k}: {v / 1e6:.2f}' for k, v in r['only_valais_by_region'].items()))
    # (c) blur
    r['blur'] = {}
    txt = []
    for s in (0.15, 0.25, 0.55, 1.05, 2.05):
        n = int(round(s / chk.CELL))
        Q = uniform_filter(P, size=n, mode='wrap')        # mean over n x n cells = spread evenly over the square, totals kept (rows near the poles are empty)
        Q *= tot / Q.sum()
        r['blur'][str(s)] = diffM(Q); txt.append(f'{s:.2f} deg: {diffM(Q):+.2f}')
    print('  blur test, Berlin minus Valais in millions after spreading each cell over a square of side ' + '; '.join(txt))
    # shift test: move the whole map by one cell (0.05 deg, 5.6 km) in each direction
    sh = {k: diffM(np.roll(P, v, axis=(0, 1))) for k, v in (('north', (1, 0)), ('south', (-1, 0)), ('east', (0, 1)), ('west', (0, -1)))}
    r['shift_one_cell'] = sh
    print('  shift test, the whole map moved by one cell (0.05 deg): ' + '; '.join(f'{k} {v:+.2f}' for k, v in sh.items()))
    out[name] = r

# (d) hybrids between the first two grids
names = list(grids)
if len(names) >= 2:
    A, Bg = grids[names[0]], grids[names[1]]
    print(f'===== hybrids of {names[0]} (A) and {names[1]} (B); Berlin minus Valais, millions: A {diffM(A):+.2f}, B {diffM(Bg):+.2f}')
    out['hybrids'] = {}

    def hybrid(tot_from, pat_from, f):
        H2, W2 = chk.H // f, chk.W // f
        T = tot_from.reshape(H2, f, W2, f).sum(axis=(1, 3))
        Pb = pat_from.reshape(H2, f, W2, f).sum(axis=(1, 3))
        ratio = np.divide(T, Pb, out=np.zeros_like(T), where=Pb > 0)
        Hy = pat_from * np.repeat(np.repeat(ratio, f, axis=0), f, axis=1)
        # blocks where the pattern grid is empty but the totals grid is not: keep the totals grid's own cells
        lost = np.repeat(np.repeat(Pb <= 0, f, axis=0), f, axis=1)
        Hy = np.where(lost, tot_from, Hy)
        return Hy

    for s in (0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0):
        f = int(round(s / chk.CELL))
        if chk.H % f or chk.W % f: continue
        h1 = hybrid(A, Bg, f); h2 = hybrid(Bg, A, f)
        out['hybrids'][str(s)] = dict(A_totals_B_pattern=diffM(h1), B_totals_A_pattern=diffM(h2), check_totals=[float(h1.sum()), float(h2.sum())])
        print(f'   blocks of {s:5.2f} deg: A\'s block totals spread as B: {diffM(h1):+.2f};  B\'s block totals spread as A: {diffM(h2):+.2f}')
    # whole-world scaling only
    print(f'   (blocks = whole world: A spread as B is B itself scaled: {diffM(Bg) * A.sum() / Bg.sum():+.2f}; B spread as A: {diffM(A) * Bg.sum() / A.sum():+.2f})')
    # sliver-by-region differences
    ob = inB & ~inV; ov = inV & ~inB
    for lab, m in (('only in the Berlin half', ob), ('only in the Valais half', ov)):
        ra, rb = by_region(A, m), by_region(Bg, m)
        print(f'   {lab}, A minus B by region (millions): ' + '; '.join(f'{k}: {(ra.get(k, 0) - rb.get(k, 0)) / 1e6:+.2f}' for k in sorted(set(ra) | set(rb))))
json.dump(out, open(sys.argv[1], 'w'), indent=1)
