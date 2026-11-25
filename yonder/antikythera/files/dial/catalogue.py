"""After the reader's report (not sealed): the dial against catalogued eclipses in place of my latitude rules.
The catalogue is NASA's Five Millennium Catalog of Lunar and Solar Eclipses (Espenak and Meeus), the pages for
-0299 to -0200 and -0199 to -0100. Each catalogued eclipse is matched to the nearest full moon (lunar) or new moon
(solar) of the JPL tables and so to a month of the dial.
usage: catalogue.py DATADIR CATDIR      (run under -I through runpy)"""
import sys, os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, dial, mech
DATA, CAT = sys.argv[1], sys.argv[2]
MON = {m: i + 1 for i, m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}


def jd_julian(y, m, d):
    if m <= 2: y -= 1; m += 12
    return np.floor(365.25 * (y + 4716)) + np.floor(30.6001 * (m + 1)) + d - 1524.5


def read_cat(names):
    rows = []
    pat = re.compile(r'^\s*(\d{5})\s+(-?\d{4})\s+([A-Z][a-z]{2})\s+(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s+-?\d+\s+-?\d+\s+\d+\s+(\S+)\s+\S+\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)(?:\s+(-?\d+\.\d+))?')
    for name in names:
        for line in open(os.path.join(CAT, name), encoding='utf-8', errors='replace'):
            m = pat.match(re.sub(r'<[^>]*>', '', line))
            if not m: continue
            y, mo, d = int(m.group(2)), MON[m.group(3)], int(m.group(4))
            t = jd_julian(y, mo, d) + (int(m.group(5)) + int(m.group(6)) / 60 + int(m.group(7)) / 3600) / 24
            rows.append(dict(cat=m.group(1), date=f'{y} {m.group(3)} {d:02d}', jd=float(t), kind=m.group(8)[0], gamma=float(m.group(9)),
                             mag1=float(m.group(10)), mag2=float(m.group(11)) if m.group(11) else None))
    return rows


assert abs(jd_julian(-204, 5, 12) - 1646678.5) < 1e-9
lunar, solar = dial.glyph_months()
moon = mech.read(os.path.join(DATA, 'moon_then.txt')); sun = mech.read(os.path.join(DATA, 'sun_then.txt'))
sz = dial.syzygies(moon, sun)
ft = sz['full'][0]; nt = sz['new'][0]
FM, NM = dial.number(sz)
ntn = np.array([np.searchsorted(ft, t) for t in nt])          # dial month of each new moon (the full moon before it)

LE = read_cat(['LE-0299--0200.html', 'LE-0199--0100.html'])
SE = read_cat(['SE-0299--0200.html', 'SE-0199--0100.html'])
print(f'catalogue rows read: {len(LE)} lunar, {len(SE)} solar (the two centuries)')
t0, t1 = ft[0] - 1.0, ft[4 * 223] - 1.0                          # cycles 0 to 3
out = {}
worst = 0.0
for j in range(4):
    lo, hi = ft[223 * j] - 1.0, ft[223 * (j + 1)] - 1.0
    le = [e for e in LE if lo <= e['jd'] < hi]; se = [e for e in SE if lo <= e['jd'] < hi]
    for e in le:
        k = int(np.argmin(np.abs(ft - e['jd']))); e['month'] = k + 1 - 223 * j; e['dt'] = float(e['jd'] - ft[k]); e['lat'] = FM[k + 1]
    for e in se:
        k = int(np.argmin(np.abs(nt - e['jd']))); e['month'] = int(ntn[k]) - 223 * j; e['dt'] = float(e['jd'] - nt[k]); e['lat'] = float(sz['new'][1][k])
    worst = max([worst] + [abs(e['dt']) for e in le + se])
    assert all(1 <= e['month'] <= 223 for e in le + se)
    assert len({e['month'] for e in le}) == len(le) and len({e['month'] for e in se}) == len(se)
    um = [e for e in le if e['kind'] in 'PT']; pe = [e for e in le if e['kind'] == 'N']
    lm = {e['month']: e for e in le}; sm = {e['month']: e for e in se}
    r = dict(
        lunar_all=len(le), umbral=len(um), umbral_on_glyph=sum(e['month'] in lunar for e in um),
        umbral_missed=[(e['month'], e['date'], e['kind'], e['mag2']) for e in um if e['month'] not in lunar],
        penumbral=len(pe), penumbral_on_glyph=sum(e['month'] in lunar for e in pe),
        glyph_lunar_any=sum(n in lm for n in lunar), glyph_lunar_umbral=sum(n in lm and lm[n]['kind'] in 'PT' for n in lunar),
        glyph_lunar_none=[n for n in sorted(lunar) if n not in lm],
        glyph_lunar_penumbral=[(n, lm[n]['mag1']) for n in sorted(lunar) if n in lm and lm[n]['kind'] == 'N'],
        solar_all=len(se), solar_on_glyph=sum(e['month'] in solar for e in se),
        solar_central=sum(e['kind'] in 'ATH' for e in se), solar_central_on_glyph=sum(e['month'] in solar for e in se if e['kind'] in 'ATH'),
        glyph_solar_any=sum(n in sm for n in solar), glyph_solar_none=[n for n in sorted(solar) if n not in sm],
        solar_left_out=[(e['month'], e['kind'], e['gamma']) for e in se if e['month'] not in solar],
    )
    out[j] = r
    print(f'\ncycle {j} ({18.03 * j:.0f} years on): catalogue has {r["lunar_all"]} lunar eclipses ({r["umbral"]} partial or total, {r["penumbral"]} penumbral) and {r["solar_all"]} solar ({r["solar_central"]} central)')
    print(f'  partial or total lunar eclipses in a month with a lunar glyph: {r["umbral_on_glyph"]} of {r["umbral"]}; missed (month, date, kind, umbral magnitude): {r["umbral_missed"]}')
    print(f'  penumbral lunar eclipses in a month with a lunar glyph: {r["penumbral_on_glyph"]} of {r["penumbral"]}')
    print(f'  of the 38 lunar glyph months: {r["glyph_lunar_any"]} had a catalogued lunar eclipse of any kind, {r["glyph_lunar_umbral"]} a partial or total one; '
          f'penumbral only (month, penumbral magnitude): {r["glyph_lunar_penumbral"]}; none at all: {r["glyph_lunar_none"]}')
    print(f'  solar eclipses in a month with a solar glyph: {r["solar_on_glyph"]} of {r["solar_all"]}; central ones: {r["solar_central_on_glyph"]} of {r["solar_central"]}')
    print(f'  of the 28 solar glyph months: {r["glyph_solar_any"]} had a catalogued solar eclipse somewhere on Earth; none: {r["glyph_solar_none"]}')
    g = [x[2] for x in r['solar_left_out']]
    print(f'  the {len(g)} solar eclipses in months without a solar glyph: gamma {min(g):+.2f} to {max(g):+.2f}; with the Moon\'s shadow north of the Earth\'s centre (gamma > 0): {sum(x > 0 for x in g)}')
    gin = [e['gamma'] for e in se if e['month'] in solar]
    print(f'  the {len(gin)} in months with a solar glyph: gamma {min(gin):+.2f} to {max(gin):+.2f}')
print(f'\nlargest difference between a catalogued instant of greatest eclipse and the matched full or new moon of the tables: {worst * 24:.2f} hours')
# month 126 through the four cycles
for j in range(4):
    lo = ft[223 * j + 125]
    e = [x for x in LE if abs(x['jd'] - lo) < 1.0]
    print(f'month 126, cycle {j}: ' + (f'{e[0]["date"]}, kind {e[0]["kind"]}, penumbral magnitude {e[0]["mag1"]}, umbral magnitude {e[0]["mag2"]}, gamma {e[0]["gamma"]}' if e else 'no eclipse in the catalogue'))
json.dump(out, open(os.path.join(HERE, 'catalogue.json'), 'w'))
