"""The run for the sealed sheet (expectations.md): the 22 engraved hours against real full and new moons, every start from 300 BC to 1 BC.
usage: hours_run.py      (run under -I through runpy; no data files: the hours are in hours.py and the syzygies are computed)"""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, hours
from phases import true_phase
SIXTEEN = {299: -1162, 223: -223, 205: 0, 187: 223, 183: 270, 169: 446, 165: 493, 147: 716, 129: 939, 111: 1162, 93: 1385, 89: 1432, 71: 1655, 53: 1878, 35: 2101, 17: 2324}
OUT4 = ('13S', '120M', '125M', '184M')
g22 = hours.glyphs_real(); g18 = hours.glyphs_real(drop=OUT4)
assert len(g22) == 22 and len(g18) == 18
K = hours.starts()
year = lambda k: 1 - math.floor(hours.year_of(true_phase(hours.K0_FULL + k + 1)))
for bc, k in SIXTEEN.items(): assert year(k) == bc, (bc, k, year(k))
res = {}
for name, g in (('18', g18), ('22', g22)):
    sc = {k: hours.score(k, g) for k in K}
    order = sorted(K, key=lambda k: sc[k][0])
    res[name] = dict(scores={str(k): [round(sc[k][0], 4), sc[k][1]] for k in K})
    print(f'\n== with the {name} hours: {len(K)} starts; median score {np.median([sc[k][0] for k in K]):.2f} h, spread (sd) {np.std([sc[k][0] for k in K]):.2f} h')
    print('   the sixteen (year BC: score h, longitude E, rank among all):')
    for bc, k in SIXTEEN.items():
        print(f'     {bc:3d} BC  k = {k:5d}: {sc[k][0]:5.2f} h at {sc[k][1]:+7.1f}   rank {1 + order.index(k)}')
    best16 = min(SIXTEEN, key=lambda bc: round(sc[SIXTEEN[bc]][0], 2))
    print(f'   best of the sixteen: {best16} BC; 205 BC: {sc[0][0]:.2f} h at {sc[0][1]:+.1f} E, rank {1 + order.index(0)} of {len(K)} ({sum(sc[k][0] < sc[0][0] for k in K)} starts score strictly lower)')
    print('   the best fifteen of all starts (score, k, year BC, longitude, Saros and months from 205 BC):')
    for k in order[:15]:
        m = k // 223 if k >= 0 else -((-k) // 223)
        print(f'     {sc[k][0]:5.2f}  k = {k:5d}  {year(k):3d} BC  {sc[k][1]:+7.1f}   {m:+d} Saros {k - 223 * m:+d} months')
    print(f'   767 months after 205 BC (k = 767, {year(767)} BC): {sc[767][0]:.2f} h; 767 before (k = -767, {year(-767)} BC): {sc[-767][0]:.2f} h')
    print('   whole Saros cycles from 205 BC (cycles: score, longitude):', '; '.join(f'{k // 223:+d}: {sc[k][0]:.2f}, {sc[k][1]:+.0f}' for k in K if k % 223 == 0))
    res[name]['best16'] = best16
# the differences at 205 BC, glyph by glyph, at its best longitude for the 18
s, lon = hours.score(0, g18)
print(f'\n== 205 BC, glyph by glyph (hour engraved on a 24-hour clock; local time of the real full or new moon at {lon:+.1f} E; difference):')
for m, kind, h in g22:
    ut = ((hours.syzygy_ut_hours(0, m, kind) + 0.5) % 1.0) * 24.0
    d = float(hours.wrap(h - ut - lon / 15.0))
    print(f'     {m:3d}{kind}  {h:2d} h   {(ut + lon / 15.0) % 24:5.2f} h   {d:+5.2f}' + ('   (one of the four set aside)' if f'{m}{kind}' in OUT4 else ''))
json.dump(res, open(os.path.join(HERE, 'hours_run.json'), 'w'))
