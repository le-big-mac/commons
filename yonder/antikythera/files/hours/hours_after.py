"""After the sealed run (not sealed): four things the run raised.
A. The sixteen with the longitude kept in the Greek world (10 to 40 degrees east), and how many of all starts then do as well as 205 BC.
B. How far the Moon's and the Sun's anomalies have moved, against 205 BC, at the starts that fit the hours best.
C. The hours as Iversen and Jones (2019) read them, where they differ from Carman and Evans's or add to them.
D. Lunar and solar hours separately at 205 BC.
usage: hours_after.py     (under -I through runpy)"""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, hours
from phases import true_phase
SIXTEEN = {299: -1162, 223: -223, 205: 0, 187: 223, 183: 270, 169: 446, 165: 493, 147: 716, 129: 939, 111: 1162, 93: 1385, 89: 1432, 71: 1655, 53: 1878, 35: 2101, 17: 2324}
OUT4 = ('13S', '120M', '125M', '184M')
g22 = hours.glyphs_real(); g18 = hours.glyphs_real(drop=OUT4)
K = hours.starts()
year = lambda k: 1 - math.floor(hours.year_of(true_phase(hours.K0_FULL + k + 1)))

print('A. Longitude kept between 10 and 40 degrees east (the 18 hours):')
scg = {k: hours.score(k, g18, lon_range=(10, 40)) for k in K}
for bc, k in SIXTEEN.items(): print(f'     {bc:3d} BC: {scg[k][0]:5.2f} h at {scg[k][1]:+5.1f}')
order = sorted(K, key=lambda k: scg[k][0])
print(f'   205 BC: rank {1 + order.index(0)} of {len(K)}; starts scoring under 3.0 h: {sum(scg[k][0] < 3.0 for k in K)}; the best ten (score, year BC, k, longitude):',
      [(round(scg[k][0], 2), year(k), k, scg[k][1]) for k in order[:10]])
print('   of the sixteen, under 3.0 h with the longitude free:', [bc for bc, k in SIXTEEN.items() if hours.score(k, g18)[0] < 3.0], '; with it kept in the Greek world:', [bc for bc, k in SIXTEEN.items() if scg[k][0] < 3.0])

print('\nB. Anomalies at the full moon of month 1, against their values at the start of 205 BC (degrees; Meeus mean elements):')
def anomalies(k):
    kk = hours.K0_FULL + k + 1; T = kk / 1236.85
    M = (2.5534 + 29.10535670 * kk - 0.0000014 * T * T) % 360          # Sun's mean anomaly
    Mp = (201.5643 + 385.81693528 * kk + 0.0107582 * T * T) % 360      # Moon's mean anomaly
    return M, Mp
M0, Mp0 = anomalies(0)
w = lambda x: (x + 180) % 360 - 180
sc = {k: hours.score(k, g18) for k in K}
best = sorted(K, key=lambda k: sc[k][0])[:15]
print(f'   at 205 BC: Moon {Mp0:.1f} (180 is apogee), Sun {M0:.1f}')
for k in best + [0, 223, -223, 446, 767]:
    M, Mp = anomalies(k)
    print(f'     k = {k:5d} ({year(k):3d} BC): score {sc[k][0]:.2f} h; Moon {w(Mp - Mp0):+6.1f}, Sun {w(M - M0):+6.1f}')
dM = np.array([w(anomalies(k)[1] - Mp0) for k in K]); dS = np.array([w(anomalies(k)[0] - M0) for k in K]); s = np.array([sc[k][0] for k in K])
good = s < 2.3
print(f'   the {int(good.sum())} starts under 2.3 h: Moon\'s anomaly against 205 BC from {dM[good].min():+.0f} to {dM[good].max():+.0f} (mean {dM[good].mean():+.1f}); Sun\'s from {dS[good].min():+.0f} to {dS[good].max():+.0f} (mean {dS[good].mean():+.1f})')

print('\nC. Iversen and Jones (2019), their list of readings before section 4: 8M 2d, 8S 1d or 4d, 67M 8n, 72S 2n, 119S 12n (for 11n), 120M 12d (for 6d), 125M 8d (the same)')
conv = lambda n, dn: (6 + n) % 24 if dn == 'd' else (18 + n) % 24
def variant(extra, changed):
    g = []
    for m, kind, h in g22:
        key = f'{m}{kind}'
        g.append((m, kind, conv(*changed[key]) if key in changed else h))
    return g + [(m, kind, conv(n, dn)) for (m, kind, n, dn) in extra]
for name, extra, changed in (('Carman and Evans, all 22', [], {}),
                             ('with 120M read as 12d and 119S as 12n', [], {'120M': (12, 'd'), '119S': (12, 'n')}),
                             ('and with 8M 2d, 8S 1d, 67M 8n, 72S 2n added (26 hours)', [(8, 'M', 2, 'd'), (8, 'S', 1, 'd'), (67, 'M', 8, 'n'), (72, 'S', 2, 'n')], {'120M': (12, 'd'), '119S': (12, 'n')}),
                             ('the same with 8S 4d', [(8, 'M', 2, 'd'), (8, 'S', 4, 'd'), (67, 'M', 8, 'n'), (72, 'S', 2, 'n')], {'120M': (12, 'd'), '119S': (12, 'n')})):
    g = variant(extra, changed)
    row = {bc: hours.score(k, g) for bc, k in SIXTEEN.items() if bc in (223, 205, 187, 169)}
    rest = min(hours.score(k, g)[0] for bc, k in SIXTEEN.items() if bc not in (223, 205, 187, 169))
    print(f'   {name}: ' + '; '.join(f'{bc} BC {v[0]:.2f} h at {v[1]:+.0f}' for bc, v in row.items()) + f'; best of the other twelve {rest:.2f} h')
    s0, lon = hours.score(0, g)
    if extra or changed:
        for m, kind, h in g:
            if f'{m}{kind}' in ('120M', '119S', '8M', '8S', '67M', '72S'):
                ut = ((hours.syzygy_ut_hours(0, m, kind) + 0.5) % 1.0) * 24.0
                print(f'        at 205 BC, {m}{kind}: engraved {h} h, real {(ut + lon / 15) % 24:.2f} h, difference {float(hours.wrap(h - ut - lon / 15)):+.2f}')

print('\nD. 205 BC, lunar and solar hours apart (of the 18; longitude free for each set):')
for name, g in (('9 lunar', [x for x in g18 if x[1] == 'M']), ('9 solar', [x for x in g18 if x[1] == 'S'])):
    v = hours.score(0, g); print(f'   {name}: {len(g)} hours, {v[0]:.2f} h at {v[1]:+.1f}')

print('\nE. The starts that fit the 18 hours better than 205 BC, and the months:')
better = [k for k in K if sc[k][0] < sc[0][0]]
inv = {v: b for b, v in SIXTEEN.items()}
print(f'   {len(better)} starts score lower than 205 BC; of them among the sixteen: {[inv[k] for k in better if k in inv]} BC')
print('   longitudes of the four, and the step from each to the next (degrees):', [(bc, sc[SIXTEEN[bc]][1]) for bc in (223, 205, 187, 169)],
      [round(((sc[SIXTEEN[b]][1] - sc[SIXTEEN[a]][1] + 180) % 360) - 180, 1) for a, b in ((223, 205), (205, 187), (187, 169))])
print(f'   the Saros is 6585.3211 days: 0.3211 of a day is {0.3211 * 360:.1f} degrees of the Earth\'s turning')
print('   under 3.0 h with the longitude free, all starts:', sum(sc[k][0] < 3.0 for k in K), '; under 2.3 h:', sum(sc[k][0] < 2.3 for k in K))
print('   with the longitude between 10 and 40 E, the sixteen in order:', sorted((round(scg[k][0], 2), bc) for bc, k in SIXTEEN.items())[:4])
