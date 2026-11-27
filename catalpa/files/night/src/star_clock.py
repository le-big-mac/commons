# A look (unsealed; 2024 and 2025 had both been seen): does the darkest part of the night keep time by the Sun or by the stars?
# For each cleaned night, the middle of its darkest tenth is given two ways: in hours from local midnight by the Sun
# (the middle between that night's dusk and dawn is not used; local mean solar midnight is), and in star time
# (local sidereal time, the right ascension that is overhead). A thing fixed to the stars comes 3.94 minutes earlier each
# day by the Sun's clock; a thing fixed to people's habits or to the Sun does not move by star time's rate.
# Reads cache/nights<YEAR>.pkl. Usage: star_clock.py 2024 2025 [...]
import sys, pickle, importlib.util, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('sky', '/home/agent1/night/src/sky.py'); sky = importlib.util.module_from_spec(spec); spec.loader.exec_module(sky)
N = []
for y in sys.argv[1:]:
    for c in pickle.load(open(f'/home/agent1/night/cache/nights{y}.pkl', 'rb')): c['y'] = int(y); N.append(c)
for c in N:
    tm = c['dusk'] + dt.timedelta(hours=(c['tenth'] + 0.5) / 10 * c['L'])
    c['lst'] = ((sky.gmst_deg(sky.jd(tm)) + c['lon']) % 360) / 15.0
    sol = (tm.hour + tm.minute / 60 + tm.second / 3600 + c['lon'] / 15.0) % 24; c['sol'] = sol - 24 if sol > 12 else sol     # hours from local mean midnight
    c['doy'] = (c['d'] - dt.date(c['d'].year, 1, 1)).days
    c['lst0'] = ((sky.gmst_deg(sky.jd(c['dusk'])) + c['lon']) % 360) / 15.0; c['lst1'] = ((sky.gmst_deg(sky.jd(c['dawn'])) + c['lon']) % 360) / 15.0
north = [c for c in N if c['lat'] > 0]
print('A. northern places, by month: middle of the darkest tenth, by the Sun (hours from local midnight) and by the stars (hours of star time); middle night of each month, both years together')
print('   month   lit: nights  Sun   stars  | between: nights  Sun   stars  | dark: nights  Sun   stars')
def cmed(v):   # circular median of hours of star time: the value minimising the summed circular distance
    v = np.array(v); best = min(v, key=lambda x: np.sum(np.minimum(np.abs(v - x), 24 - np.abs(v - x)))); return float(best)
for m in range(1, 13):
    row = f'   {m:>5}  '
    for k in ('lit', 'between', 'dark'):
        S = [c for c in north if c['cls'] == k and c['d'].month == m]
        row += (f'{len(S):>10}  {np.median([c["sol"] for c in S]):+5.1f}  {cmed([c["lst"] for c in S]):5.1f}   | ' if len(S) >= 3 else f'{len(S):>10}      -      -   | ')
    print(row)
print('\nB. how fast the darkest part moves through the night as the season goes on (minutes a day by the Sun\'s clock; a thing fixed to the stars gives -3.9, a thing fixed to the Sun about 0)')
def rate(S):
    if len(S) < 12: return None
    x = np.array([c['doy'] + 365 * (c['y'] - min(cc['y'] for cc in S)) * 0 for c in S], float); yv = np.array([c['sol'] for c in S]) * 60
    a, b = np.polyfit(x, yv, 1); r = yv - (a * x + b); se = np.sqrt(np.sum(r ** 2) / (len(S) - 2) / np.sum((x - x.mean()) ** 2)); return a, se, len(S)
for lab, lo, hi in (('July to October', 182, 304), ('August to October', 213, 304), ('November to February', None, None), ('March to June', 60, 181)):
    for k in ('lit', 'between', 'dark'):
        if lo is None:
            S = [dict(c, doy=(c['doy'] if c['doy'] > 200 else c['doy'] + 365)) for c in north if c['cls'] == k and c['d'].month in (11, 12, 1, 2)]
        else: S = [c for c in north if c['cls'] == k and lo <= c['doy'] < hi]
        r = rate(S); print(f'   {lab:<22}{k:<8}' + (f'{r[0]:+5.1f} minutes a day, give or take {r[1]:.1f} ({r[2]} nights)' if r else 'too few nights'))
print('\nC. star time of the darkest part, northern places not in towns (between and dark), both years: nights by two-hour span of star time')
S = [c for c in north if c['cls'] != 'lit']
print('   span        nights with their darkest tenth there   nights whose dark hours reach that span at all   share')
for h in range(0, 24, 2):
    inn = sum(1 for c in S if h <= c['lst'] < h + 2)
    def covers(c):
        a, b = c['lst0'], c['lst1']; mid = h + 1.0
        return (a <= mid <= b) if a <= b else (mid >= a or mid <= b)
    cov = sum(1 for c in S if covers(c)); print(f'   {h:>2} to {h + 2:<2}h   {inn:>6}   {cov:>24}   {100 * inn / cov if cov else float("nan"):>18.0f} in 100')
print('\nD. the same for the five towns')
S = [c for c in north if c['cls'] == 'lit']
for h in range(0, 24, 2):
    inn = sum(1 for c in S if h <= c['lst'] < h + 2)
    def covers(c):
        a, b = c['lst0'], c['lst1']; mid = h + 1.0
        return (a <= mid <= b) if a <= b else (mid >= a or mid <= b)
    cov = sum(1 for c in S if covers(c)); print(f'   {h:>2} to {h + 2:<2}h   {inn:>6}   {cov:>24}   {100 * inn / cov if cov else float("nan"):>18.0f} in 100')
print('\nE. Arkaroola (32 degrees south), both years: star time of the darkest part, nights by two-hour span')
S = [c for c in N if c['st'] == 'stars477']
print('   ' + ' '.join(f"{h}-{h + 2}h:{sum(1 for c in S if h <= c['lst'] < h + 2)}" for h in range(0, 24, 2)))
print('\nF. when is the last tenth the darkest? northern places not in towns: by star time at the start of dawn, in two-hour spans: nights / last tenth the darkest')
S = [c for c in north if c['cls'] != 'lit']
print('   ' + ' '.join(f"{h}-{h + 2}h:{sum(1 for c in S if h <= c['lst1'] < h + 2)}/{sum(1 for c in S if h <= c['lst1'] < h + 2 and c['tenth'] == 9)}" for h in range(0, 24, 2)))
for y in sorted({c['y'] for c in N}):
    print(f'   {y}: ' + ' '.join(f"{h}-{h + 2}h:{sum(1 for c in S if c['y'] == y and h <= c['lst1'] < h + 2)}/{sum(1 for c in S if c['y'] == y and h <= c['lst1'] < h + 2 and c['tenth'] == 9)}" for h in range(0, 24, 2)))
S = [c for c in north if c['cls'] == 'lit']
print('   towns: ' + ' '.join(f"{h}-{h + 2}h:{sum(1 for c in S if h <= c['lst1'] < h + 2)}/{sum(1 for c in S if h <= c['lst1'] < h + 2 and c['tenth'] == 9)}" for h in range(0, 24, 2)))
