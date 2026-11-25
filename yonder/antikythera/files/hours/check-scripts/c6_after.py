"""Item 6: the after-the-fact part with the checker's own scoring (catalogue Delta T; Meeus syzygies via the author's phases.py, and the
checker's JPL syzygies where the 'then' tables reach).  Iversen and Jones's readings typed by the checker from their edition
(paper.txt lines 707-775): cell 8 Moon daytime 2nd, Sun 1st (or 4th); cell 67 Moon nighttime 8th; cell 72 Sun n[ighttime] 2nd;
cell 119 Sun nighttime 12th; cell 120 Moon daytime 12th(?)."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, own, phases

cat = own.catalogue(-299, 100)
cj = np.array([r['jd'] for r in cat]); cd = np.array([r['dt'] for r in cat])
dT = lambda jd: float(np.interp(jd, cj, cd))
K0 = -27255.5
full, new = own.syz('then')
def ut_meeus(k, month, kind):
    t = phases.true_phase(K0 + k + month - 1 + (0.5 if kind == 'S' else 0.0))
    return ((t - dT(t) / 86400.0 + 0.5) % 1.0) * 24.0
def ut_jpl(k, month, kind):
    t = full[k + month - 1]
    if kind == 'S': t = new[np.searchsorted(new, t)]
    return ((t - dT(t) / 86400.0 + 0.5) % 1.0) * 24.0
def score(k, g, lons=None, ut=ut_meeus):
    return own.best([h for m, kind, h in g], [ut(k, m, kind) for m, kind, h in g], lons)

SIX = {299: -1162, 223: -223, 205: 0, 187: 223, 183: 270, 169: 446, 165: 493, 147: 716, 129: 939, 111: 1162, 93: 1385, 89: 1432, 71: 1655, 53: 1878, 35: 2101, 17: 2324}
FOUR = (223, 205, 187, 169)
g22 = own.glyphs(); g18 = own.glyphs(drop=own.OUT4)
def variant(base, changed, extra):
    g = [(m, kind, own.rule(*changed[f'{m}{kind}']) if f'{m}{kind}' in changed else h) for m, kind, h in base]
    return g + [(m, kind, own.rule(n, dn)) for m, kind, n, dn in extra]
CH = {'120M': (12, 'd'), '119S': (12, 'n')}
sets = [
 ('README as coded: 26 hours with 72S 2d, 8S 1d', variant(g22, CH, [(8, 'M', 2, 'd'), (8, 'S', 1, 'd'), (67, 'M', 8, 'n'), (72, 'S', 2, 'd')])),
 ('README as coded: 26 hours with 72S 2d, 8S 4d', variant(g22, CH, [(8, 'M', 2, 'd'), (8, 'S', 4, 'd'), (67, 'M', 8, 'n'), (72, 'S', 2, 'd')])),
 ('I-J edition: 26 hours with 72S 2n (night), 8S 1d', variant(g22, CH, [(8, 'M', 2, 'd'), (8, 'S', 1, 'd'), (67, 'M', 8, 'n'), (72, 'S', 2, 'n')])),
 ('I-J edition: 26 hours with 72S 2n (night), 8S 4d', variant(g22, CH, [(8, 'M', 2, 'd'), (8, 'S', 4, 'd'), (67, 'M', 8, 'n'), (72, 'S', 2, 'n')])),
 ('Jones 2020 concordance: 72S 5n, 8S 1d', variant(g22, CH, [(8, 'M', 2, 'd'), (8, 'S', 1, 'd'), (67, 'M', 8, 'n'), (72, 'S', 5, 'n')])),
 ('22 with 120M 12d and 119S 12n only', variant(g22, CH, [])),
 ('Carman and Evans, all 22', g22),
]
for name, g in sets:
    row = {bc: score(SIX[bc], g) for bc in FOUR}
    rest = min((score(k, g)[0], bc) for bc, k in SIX.items() if bc not in FOUR)
    s0, lon = row[205]
    print(f'{name} ({len(g)} hours): ' + '; '.join(f'{bc} BC {v[0]:.2f} at {v[1]:+.0f}' for bc, v in row.items()) + f'; best of the other twelve {rest[0]:.2f} ({rest[1]} BC); 259 BC {score(-669, g)[0]:.2f}; 151 BC {score(669, g)[0]:.2f}')
    if len(g) > 22 or 'only' in name:
        d = {f'{m}{kind}': float(own.wrap12(h - ut_meeus(0, m, kind) - lon / 15)) for m, kind, h in g}
        dj = {f'{m}{kind}': float(own.wrap12(h - ut_jpl(0, m, kind) - lon / 15)) for m, kind, h in g}
        print(f'      at 205 BC (longitude {lon:+.1f}): ' + ', '.join(f'{c} {d[c]:+.2f} (JPL {dj[c]:+.2f})' for c in ('120M', '119S', '8M', '8S', '67M', '72S') if c in d))
        gl = score(0, g, np.arange(10, 40.001, 0.25))
        print(f'      205 BC with the longitude kept to 10..40 E: {gl[0]:.2f} at {gl[1]:+.1f}; with JPL syzygies, free: {score(0, g, ut=ut_jpl)[0]:.2f}')

# 120M alone, at the longitude of the 18
s, lon = score(0, g18)
for h, lab in ((own.rule(6, 'd'), '6d'), (own.rule(12, 'd'), '12d')):
    print(f'120M as {lab} at the longitude of the 18 ({lon:+.2f}): {float(own.wrap12(h - ut_meeus(0, 120, "M") - lon / 15)):+.2f} h (JPL {float(own.wrap12(h - ut_jpl(0, 120, "M") - lon / 15)):+.2f})')
# "removes one of the four outliers": the 19 = the 18 plus 120M as 12d
g19 = g18 + [(120, 'M', own.rule(12, 'd'))]
print('the 18 plus 120M read 12d (19 hours):', '; '.join(f'{bc} BC {score(SIX[bc], g19)[0]:.2f} at {score(SIX[bc], g19)[1]:+.0f}' for bc in FOUR))

# the Greek-longitude scores, 22 hours, and whole cycles
print('\n22 hours, longitude 10..40 E, the sixteen:', sorted((round(score(k, g22, np.arange(10, 40.001, 0.25))[0], 2), bc) for bc, k in SIX.items())[:4])
print('whole cycles -3, 0, +3 with longitude 10..40 E:  18 hours:', [tuple(round(x, 2) for x in score(k, g18, np.arange(10, 40.001, 0.25))) for k in (-669, 0, 669)],
      ' 22 hours:', [tuple(round(x, 2) for x in score(k, g22, np.arange(10, 40.001, 0.25))) for k in (-669, 0, 669)])
print('whole cycles -3, 0, +3 with longitude free:  18:', [tuple(round(x, 2) for x in score(k, g18)) for k in (-669, 0, 669)], ' 22:', [tuple(round(x, 2) for x in score(k, g22)) for k in (-669, 0, 669)])
for name, g in sets[2:5]:
    print(f'   {name}: -3, 0, +3 with longitude 10..40 E:', [tuple(round(x, 2) for x in score(k, g, np.arange(10, 40.001, 0.25))) for k in (-669, 0, 669)])
# lunar and solar apart, 205 BC
for nm, kk in (('9 lunar', 'M'), ('9 solar', 'S')):
    g = [x for x in g18 if x[1] == kk]
    print(f'205 BC {nm}: Meeus {score(0, g)}, JPL {score(0, g, ut=ut_jpl)}')
