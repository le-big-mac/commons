"""Second reader, step 4: README table against my count; rises in the partial-or-total column; the 16 starts against
Carman & Evans's Table 10 (month-13 solar eclipse, date and Saros series); a start near December 178 BC; the read glyphs alone.
usage: run4.py README IJPAPER CATDIR [CATDIR...]"""
import sys, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import cat2, lists2

README, PAPER, CATS = sys.argv[1], sys.argv[2], sys.argv[3:]
K0 = json.load(open(os.path.join(HERE, 'k0.json')))['K0']
res = json.load(open(os.path.join(HERE, 'mycount.json')))
FL, FS, info, _ = lists2.freeth()
t5 = lists2.ij_table5(PAPER)
IL = [r[0] for r in t5 if r[1] == 'Y']; IS = [r[0] for r in t5 if r[3] == 'Y']
RL = [r[0] for r in t5 if r[1] == 'Y' and not r[2]]; RS = [r[0] for r in t5 if r[3] == 'Y' and not r[4]]
LE, _, _ = cat2.load('LE', CATS, verbose=False); SE, _, _ = cat2.load('SE', CATS, verbose=False)
LM = {int(round(cat2.k_of(r['jd']) - 0.5)) - K0 + 1: r for r in LE}
SM = {int(round(cat2.k_of(r['jd']))) - K0: r for r in SE}

# 1. the README's first table
txt = open(README, encoding='utf-8').read()
rows = re.findall(r'^\| (\d+) \(([\d,]+)\) \| (\d+), (\d+) \| (\d+), (\d+) \| (\d+), (\d+) \| (\d+), (\d+) \|$', txt, flags=re.M)
bad = []
for r in rows:
    j = int(r[0]); f, i = res['F'][j], res['IJ'][j]
    want = (f['A'], i['A'], f['Aum'], i['Aum'], f['U'], i['U'], f['S'], i['S'])
    got = tuple(int(x) for x in r[2:])
    yrs = int(r[1].replace(',', ''))
    jd = cat2.mean_phase_jde(K0 + 0.5 + 223 * j) - cat2.mean_phase_jde(K0 + 0.5)
    if want != got or abs(yrs - jd / 365.25) > 0.6: bad.append((j, yrs, round(jd / 365.25, 1), got, want))
print(f'README catalogue table: {len(rows)} rows read; rows that differ from my count or whose years are off by more than 0.6: {bad}')

# 2. rises in each column
for name in ('F', 'IJ'):
    R = res[name]
    for k in ('A', 'Aum', 'S'):
        print(f'{name}: rises in {k}:', [(b['cycle'], a[k], b[k]) for a, b in zip(R, R[1:]) if b[k] > a[k]])
    print(f'{name}: falls in U (misses):', [(b['cycle'], a['U'], b['U']) for a, b in zip(R, R[1:]) if b['U'] < a['U']][:12], '...')

# 3. the right-way starts and the solar eclipse of their month 13
def cal(jd):
    """Julian calendar date string from JD"""
    z = int(np.floor(jd + 0.5)); a = z; b = a + 1524; c = int((b - 122.1) // 365.25); d = int(np.floor(365.25 * c)); e = int((b - d) // 30.6001)
    day = b - d - int(np.floor(30.6001 * e)); mon = e - 1 if e < 14 else e - 13; yr = c - 4716 if mon > 2 else c - 4715
    return yr, mon, day
print('\nright-way starts of the README (Freeth list) and the solar eclipse in their month 13 (catalogue date, type, gamma, Saros series):')
for k in (-1162, -223, 0, 223, 270, 446, 493, 716, 939, 1162, 1385, 1432, 1655, 1878, 2101, 2324):
    e = SM.get(k + 13)
    y, m, d = cal(cat2.mean_phase_jde(K0 + 0.5 + k))
    print(f'   k {k:6d}: mean first full moon {y}-{m:02d}-{d:02d}; month 13 solar: ' + (f"{e['date']} {e['typ']} gamma {e['gamma']:+.3f} Saros {e['saros']}" if e else 'none'))
print('   month 13 solar eclipse in whole cycles -7..+6 from 205 BC:', [(j, SM[223 * j + 13]['date'], SM[223 * j + 13]['saros']) if 223 * j + 13 in SM else (j, None) for j in range(-7, 7) if 223 * j + 13 > min(SM)])

# 4. a start with the new moon of 22 December 178 BC at the head of month 1 (Voulgaris et al.), and its neighbours
e178 = [r for r in SE if r['y'] == -177 and r['mo'] == 12]
print('\nsolar eclipses of December -177 (178 BC) in the catalogue:', [(r['date'], r['typ'], r['saros'], r['gamma']) for r in e178])
if e178:
    n178 = int(round(cat2.k_of(e178[0]['jd']))) - K0        # dial month (205 BC count) whose END holds that new moon
    print(f'   that new moon closes month {n178} of the 205 BC count (cycle {(n178 - 1) // 223}, cell {(n178 - 1) % 223 + 1}); cells after 205 BC start: {n178}')
    for lab, k in (('month 1 = the month that this new moon OPENS (first full moon in January 177 BC)', n178), ('month 1 = the month this new moon closes', n178 - 1)):
        for name, L, S in (('Freeth', FL, FS), ('IJ', IL, IS)):
            A = sum(k + n in LM for n in L); Sn = sum(k + n in SM for n in S)
            U = sum(1 for n in range(1, 224) if k + n in LM and LM[k + n]['umag'] > 0 and n not in L)
            print(f'   {lab}; k = {k}: {name}: A {A} of 38, S {Sn} of 28, U {U}')

# 5. the glyphs read on the fragments alone: how many starts 300 BC - 1 BC give every one an eclipse?
def cal_year(jd):
    return cal(jd)[0]
Ks = [k for k in range(-1300, 2800) if -299 <= cal_year(cat2.mean_phase_jde(K0 + 0.5 + k)) <= 0]
allany = [k for k in Ks if all(k + n in LM for n in RL) and all(k + n in SM for n in RS)]
all14 = [k for k in Ks if sum(k + n in LM for n in RL) >= 14 and all(k + n in SM for n in RS)]
allumb = [k for k in Ks if all(k + n in LM and LM[k + n]['umag'] > 0 for n in RL) and all(k + n in SM for n in RS)]
maxumb = max(sum(k + n in LM and LM[k + n]['umag'] > 0 for n in RL) for k in Ks)
print(f'\nread glyphs only (15 lunar, 12 solar), {len(Ks)} starts: every glyph month with an eclipse of any kind: {len(allany)} starts; at least 14 lunar and all 12 solar: {len(all14)}; '
      f'every lunar glyph month with a PARTIAL OR TOTAL eclipse and every solar with an eclipse: {len(allumb)}; the most lunar read months with a partial or total eclipse at any start: {maxumb} of 15')
print('   years BC of the starts with every read glyph matched:', [1 - cal_year(cat2.mean_phase_jde(K0 + 0.5 + k)) for k in allany])
