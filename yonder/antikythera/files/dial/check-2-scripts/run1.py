"""Second reader, step 1: parse the catalogue my own way; integrity; the lunation-number shortcut against
(a) Meeus's mean phases for every row and (b) full/new moons found by me in the JPL tables for the first 76 years.
usage: run1.py JPLDIR CATDIR [CATDIR...]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import cat2

JPL, CATS = sys.argv[1], sys.argv[2:]
LE, lf, lp = cat2.load('LE', CATS)
SE, sf, sp = cat2.load('SE', CATS)

for name, rows in (('LE', LE), ('SE', SE)):
    cats = [r['cat'] for r in rows]
    print(f'{name}: catalogue numbers {min(cats)} to {max(cats)}; consecutive in date order: {cats == list(range(cats[0], cats[0] + len(cats)))}; '
          f'duplicates: {len(cats) - len(set(cats))}; luna numbers strictly increasing: {all(a["luna"] < b["luna"] for a, b in zip(rows, rows[1:]))}; '
          f'duplicate luna numbers: {len(rows) - len(set(r["luna"] for r in rows))}')
    print(f'   first {rows[0]["date"]} (cat {rows[0]["cat"]}, luna {rows[0]["luna"]}), last {rows[-1]["date"]} (cat {rows[-1]["cat"]}, luna {rows[-1]["luna"]})')
    kinds = {}
    for r in rows: kinds[r['typ']] = kinds.get(r['typ'], 0) + 1
    print(f'   type column values: {dict(sorted(kinds.items()))}')
    # the gap between consecutive rows in days: should be a multiple of ~29.53 (1, 5 or 6 lunations)
    gaps = {}
    for a, b in zip(rows, rows[1:]):
        g = round((b['jd'] - a['jd']) / 29.530589)
        gaps[g] = gaps.get(g, 0) + 1
        assert b['luna'] - a['luna'] == g, (a, b)
    print(f'   gaps between consecutive eclipses in lunations (by date) and how many: {dict(sorted(gaps.items()))}; each equals the difference of luna numbers')

# type against magnitude (lunar)
bad = [r for r in LE if (r['typ'][0] == 'N') != (r['umag'] < 0) or (r['typ'][0] == 'T') != (r['umag'] >= 1.0)]
print(f'LE: type letter against umbral magnitude (N: < 0; P: 0 to 1; T: >= 1): disagreements {len(bad)}', [(r['date'], r['typ'], r['umag']) for r in bad[:5]])
# solar: is the "central" notion the same as type in A, T, H?  Non-central umbral eclipses have |gamma| > ~0.997
nc = [r for r in SE if r['typ'][0] in 'ATH' and abs(r['gamma']) > 0.9972]
print(f'SE: A/T/H rows with |gamma| > 0.9972 (non-central by the usual limit): {len(nc)}; their type codes: {sorted(set(r["typ"] for r in nc))}')

# (a) Meeus mean phase for every row
for name, rows, half in (('LE', LE, 0.5), ('SE', SE, 0.0)):
    dev = np.array([cat2.k_of(r['jd']) - half - r['luna'] for r in rows])
    print(f'{name}: Meeus k (less {half}) minus the catalogue luna number: min {dev.min():+.4f}, max {dev.max():+.4f} lunations; all round to 0: {bool(np.all(np.round(dev) == 0))}')
    # around 1582 and around year 0
    for lo, hi, lab in ((1582, 1583, 'AD 1582-83'), (-1, 1, 'years -1 to 1')):
        sub = [(r['date'], r['luna'], round(cat2.k_of(r['jd']) - half - r['luna'], 3)) for r in rows if lo <= r['y'] <= hi]
        print(f'   {lab}:', sub)

# (b) the JPL tables: my own syzygies (cubic interpolation of the elongation)
def read_h(path):
    jd, lon, lat = [], [], []
    on = False
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.startswith('$$SOE'): on = True; continue
            if line.startswith('$$EOE'): break
            if on:
                p = line.split(',')
                jd.append(float(p[0])); lon.append(float(p[5])); lat.append(float(p[6]))
    return np.array(jd), np.array(lon), np.array(lat)

from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
mj, ml, mb = read_h(os.path.join(JPL, 'moon_then.txt'))
sj, sl, sb = read_h(os.path.join(JPL, 'sun_then.txt'))
mlu = np.unwrap(np.radians(ml)); slu = np.unwrap(np.radians(sl))
fm_lon = CubicSpline(mj, mlu); fs_lon = CubicSpline(sj, slu); fm_lat = CubicSpline(mj, mb)
el = lambda t: fm_lon(t) - fs_lon(t)             # elongation, radians, unwrapped, increasing
e0 = el(mj[0]); e1 = el(mj[-1])
full, new = [], []
m = int(np.ceil((e0 - np.pi) / (2 * np.pi)))
while True:
    target = np.pi + 2 * np.pi * m
    if target > e1: break
    if target >= e0: full.append(brentq(lambda t: el(t) - target, mj[0], mj[-1], xtol=1e-7))
    m += 1
m = int(np.ceil(e0 / (2 * np.pi)))
while True:
    target = 2 * np.pi * m
    if target > e1: break
    if target >= e0: new.append(brentq(lambda t: el(t) - target, mj[0], mj[-1], xtol=1e-7))
    m += 1
full, new = np.array(full), np.array(new)
print(f'JPL tables: {len(full)} full moons, {len(new)} new moons; first full moon JD {full[0]:.4f} (12 May 205 BC 0h is {cat2.jd_from_date(-204, 5, 12, False)}); first new moon JD {new[0]:.4f}')
k0 = cat2.k_of(full[0])
print(f'Meeus k of that first full moon: {k0:.4f}; so the full moon of dial month 1 is lunation {int(np.floor(k0))} + 0.5, and month n lunar = luna + {1 - int(np.floor(k0))}, solar = luna + {-int(np.floor(k0))}')
K0 = int(np.floor(k0))
# month of each new moon = number of full moons before it
new_month = np.searchsorted(full, new)          # the n-th full moon (1-based n) precedes it
worst = 0.0; diffL = {}; diffS = {}; nL = nS = 0
for r in LE:
    if full[0] - 1 <= r['jd'] <= full[-1] + 1:
        i = int(np.argmin(np.abs(full - r['jd']))); dt = abs(full[i] - r['jd']); worst = max(worst, dt)
        d = (i + 1) - r['luna']; diffL[d] = diffL.get(d, 0) + 1; nL += 1
        r['lat_tab'] = float(fm_lat(full[i]))
for r in SE:
    if new[0] - 1 <= r['jd'] <= new[-1] + 1:
        i = int(np.argmin(np.abs(new - r['jd']))); dt = abs(new[i] - r['jd']); worst = max(worst, dt)
        d = int(new_month[i]) - r['luna']; diffS[d] = diffS.get(d, 0) + 1; nS += 1
        r['lat_tab'] = float(fm_lat(new[i]))
print(f'in the span of the tables: {nL} lunar eclipses, dial month minus luna number: {diffL}; {nS} solar, {diffS}; worst |greatest eclipse - syzygy| {worst * 24:.2f} h')
# is every syzygy with small latitude an eclipse and vice versa? (a sanity check that no catalogue row is missing in the first 76 years)
fl = fm_lat(full); nl = fm_lat(new)
le_set = {round(r['jd'] * 2) for r in LE}
has = lambda rows, t: any(abs(r['jd'] - t) < 1 for r in rows)
LEw = [r for r in LE if full[0] - 1 <= r['jd'] <= full[-1] + 1]; SEw = [r for r in SE if new[0] - 1 <= r['jd'] <= new[-1] + 1]
lat_ecl = [abs(fl[i]) for i in range(len(full)) if has(LEw, full[i])]; lat_non = [abs(fl[i]) for i in range(len(full)) if not has(LEw, full[i])]
print(f'full moons of the tables with a catalogued lunar eclipse: {len(lat_ecl)}, largest |latitude| {max(lat_ecl):.3f}; without: {len(lat_non)}, smallest |latitude| {min(lat_non):.3f}')
lat_ecl = [abs(nl[i]) for i in range(len(new)) if has(SEw, new[i])]; lat_non = [abs(nl[i]) for i in range(len(new)) if not has(SEw, new[i])]
print(f'new moons of the tables with a catalogued solar eclipse: {len(lat_ecl)}, largest |latitude| {max(lat_ecl):.3f}; without: {len(lat_non)}, smallest |latitude| {min(lat_non):.3f}')
# gamma sign against the Moon's latitude at the new moon
agree = sum((r['gamma'] > 0) == (r['lat_tab'] > 0) for r in SEw); print(f'solar eclipses in the tables\' span: sign of gamma equals sign of the Moon\'s latitude at new moon in {agree} of {len(SEw)}')
dis = [(r['date'], r['gamma'], round(r['lat_tab'], 3)) for r in SEw if (r['gamma'] > 0) != (r['lat_tab'] > 0)]; print('   disagreements:', dis)
agree = sum((r['gamma'] > 0) == (r['lat_tab'] > 0) for r in LEw); print(f'lunar eclipses: sign of gamma equals sign of the Moon\'s latitude at full moon in {agree} of {len(LEw)}')
json.dump(dict(K0=K0, full0=float(full[0])), open(os.path.join(HERE, 'k0.json'), 'w'))
