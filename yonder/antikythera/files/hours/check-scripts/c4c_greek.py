"""Item 4/6: the longitude kept to 10..40 E. Which start is at the 3.0 h boundary; the 22 and I-J sets among ALL starts in that range;
the three whole cycles at one fixed longitude; the 35 starts of the dial note's looser reading."""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, own, phases
cat = own.catalogue(-299, 100)
cj = np.array([r['jd'] for r in cat]); cd = np.array([r['dt'] for r in cat])
K0 = -27255.5
def poly_dt(jd):          # the polynomial as in hours.py (retyped): to reproduce the author's boundary cases
    u = (-4712 + (jd + 0.5) / 365.25) / 100.0
    return 10583.6 - 1014.41 * u + 33.78311 * u ** 2 - 5.952053 * u ** 3 - 0.1798452 * u ** 4 + 0.022174192 * u ** 5 + 0.0090316521 * u ** 6
def uts(k, g, which):
    out = []
    for m, kind, h in g:
        t = phases.true_phase(K0 + k + m - 1 + (0.5 if kind == 'S' else 0.0))
        d = float(np.interp(t, cj, cd)) if which == 'cat' else poly_dt(t)
        out.append(((t - d / 86400.0 + 0.5) % 1.0) * 24.0)
    return out
S = json.load(open(os.path.join(HERE, 'c4_all.json')))
K = sorted(int(k) for k in S['18'])
g22 = own.glyphs(); g18 = own.glyphs(drop=own.OUT4)
bc = lambda k: 1 - math.floor(-4712 + (phases.true_phase(K0 + k) + 0.5) / 365.25)
SIX = {299: -1162, 223: -223, 205: 0, 187: 223, 183: 270, 169: 446, 165: 493, 147: 716, 129: 939, 111: 1162, 93: 1385, 89: 1432, 71: 1655, 53: 1878, 35: 2101, 17: 2324}
L = np.arange(10, 40.0001, 0.25)
for which in ('cat', 'poly'):
    G = {k: own.best([h for m, kind, h in g18], uts(k, g18, which), L) for k in K}
    order = sorted(K, key=lambda k: G[k][0])
    near = [(round(G[k][0], 3), bc(k), k, G[k][1]) for k in order if 2.9 < G[k][0] < 3.1]
    print(f'Delta T {which}: under 3.0 h: {sum(G[k][0] < 3.0 for k in K)}; rank of 205 BC {1 + order.index(0)}; starts between 2.9 and 3.1: {near}')
    if which == 'cat':
        print('   all under 3.0 (score, BC, k, lon, k mod 223):', [(round(G[k][0], 2), bc(k), k, G[k][1], k % 223) for k in order if G[k][0] < 3.0])
# 22 hours among all starts with the longitude kept
G22 = {k: own.best([h for m, kind, h in g22], uts(k, g22, 'cat'), L) for k in K}
o22 = sorted(K, key=lambda k: G22[k][0])
print(f'\n22 hours, longitude 10..40: 205 BC {G22[0][0]:.2f} at {G22[0][1]}, rank {1 + o22.index(0)}; better: {[(round(G22[k][0], 2), bc(k), k, G22[k][1]) for k in o22[:o22.index(0)]][:12]} ...; the sixteen under 4.4: {[b for b, k in SIX.items() if G22[k][0] < 4.4]}')
# the three whole cycles at one fixed longitude
for lon in (25.3, 26.25, 23.75, 30.0, 19.5):
    r18 = [round(own.best([h for m, kind, h in g18], uts(k, g18, 'cat'), np.array([lon]))[0], 2) for k in (-669, 0, 669)]
    r22 = [round(own.best([h for m, kind, h in g22], uts(k, g22, 'cat'), np.array([lon]))[0], 2) for k in (-669, 0, 669)]
    print(f'at {lon} E exactly: 259, 205, 151 BC: 18 hours {r18}; 22 hours {r22}')
# narrower Greek ranges
for lo, hi in ((15, 30), (15, 35), (20, 30)):
    LL = np.arange(lo, hi + 1e-9, 0.25)
    r = [tuple(round(x, 2) for x in own.best([h for m, kind, h in g18], uts(k, g18, 'cat'), LL)) for k in (-669, 0, 669)]
    n = sum(own.best([h for m, kind, h in g18], uts(k, g18, 'cat'), LL)[0] < 3.0 for k in K)
    print(f'range {lo}..{hi} E, 18 hours: 259, 205, 151 BC {r}; all starts under 3.0 h: {n}')
# with the Exeligmos dial: 8 or 16 hours added to the engraved hours, longitude kept 10..40
print('\nwith 8 or 16 hours added to the engraved hours (the Exeligmos dial), longitude kept 10..40 E, 18 hours:')
for b in (241, 223, 205, 187, 169, 151):
    k = {241: -446, 223: -223, 205: 0, 187: 223, 169: 446, 151: 669}[b]
    row = []
    for add in (0, 8, 16):
        g = [(m, kind, (h + add) % 24) for m, kind, h in g18]
        row.append(tuple(round(x, 2) for x in own.best([h for m, kind, h in g], uts(k, g, 'cat'), L)))
    print(f'   {b} BC: +0 h {row[0]}, +8 h {row[1]}, +16 h {row[2]}')
