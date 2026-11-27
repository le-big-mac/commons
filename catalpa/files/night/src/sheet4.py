# The lines of the fourth sheet (expectations-places.md): the dawn page's readings made after the fact, tried on years
# not seen when they were made. Reads cache2/nights<YEAR>.pkl (dawnlib2.py). Usage: sheet4.py YEAR[,YEAR...]
# Run on 2022,2023,2024,2025 it prints the figures the page was written from (the reference).
import sys, pickle, importlib.util, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('sky', '/home/agent1/night/src/sky.py'); sky = importlib.util.module_from_spec(spec); spec.loader.exec_module(sky)
years = [int(y) for y in sys.argv[1].split(',')]; N = []
for y in years:
    try: S = pickle.load(open(f'/home/agent1/night/cache2/nights{y}.pkl', 'rb'))
    except FileNotFoundError: print(f'{y}: no file of nights'); continue
    for c in S:
        st = lambda t: ((sky.gmst_deg(sky.jd(t)) + c['lon']) % 360) / 15.0
        tm = c['dusk'] + dt.timedelta(hours=(c['tenth'] + 0.5) / 10 * c['L']); c['lst'] = st(tm); c['lst0'] = st(c['dusk']); c['lst1'] = st(c['dawn'])
        s = (tm.hour + tm.minute / 60 + tm.second / 3600 + c['lon'] / 15.0) % 24; c['sol'] = s - 24 if s > 12 else s
        c['doy'] = (c['d'] - dt.date(c['d'].year, 1, 1)).days; N.append(c)
print(f"years {sys.argv[1]}: {len(N)} cleaned nights; by year " + ', '.join(f"{y}: {sum(1 for c in N if c['y'] == y)}" for y in years))
MOVERS = ['stars289', 'stars62', 'stars477', 'stars35', 'stars426', 'stars24', 'stars9']; STILL = ['stars36', 'stars19', 'stars4']; TOWNS = ['stars33', 'stars76', 'stars1', 'stars52', 'stars7']; DARK3 = ['stars35', 'stars62', 'stars289']
NAME = {c['st']: c['name'] for c in N}
def autumn(S):
    """1 August to 30 October in the north; at Arkaroola the same season of its own sky is not asked for: its nights are taken on the same dates"""
    return [c for c in S if 213 <= c['doy'] < 304]
def rate(S):
    if len(S) < 20: return None
    x = np.array([c['doy'] for c in S], float); yv = np.array([c['sol'] for c in S]) * 60; a, b = np.polyfit(x, yv, 1); r = yv - (a * x + b)
    return float(a), float(np.sqrt(np.sum(r ** 2) / (len(S) - 2) / np.sum((x - x.mean()) ** 2))), len(S)
def fr(r): return f'{r[0]:+.1f} minutes a day, give or take {r[1]:.1f} ({r[2]} nights)' if r else 'fewer than 20 nights'
def sh(v): v = list(v); return (100 * float(np.mean(v)), int(np.sum(v)), len(v)) if v else (float('nan'), 0, 0)
def f(s): return f'{s[0]:.0f} in 100 ({s[1]} of {s[2]})'
def span(x, spans): return any(lo <= x < hi for lo, hi in spans)
def covers(c, h):
    a, b = c['lst0'], c['lst1']; mid = h + 1.0
    return (a <= mid <= b) if a <= b else (mid >= a or mid <= b)
print('\nP1. the slide from August to October at each of the seven places said to move with the stars (the stars give -3.9; -1.8 or faster counts as moving)')
n_ok = n_have = 0
for st in MOVERS:
    r = rate(autumn([c for c in N if c['st'] == st]))
    if r: n_have += 1; n_ok += r[0] <= -1.8
    print(f'    {NAME.get(st, st):<20}' + fr(r))
print(f'    places with 20 nights or more: {n_have}; of them moving: {n_ok}')
print('P2. the same at the three said not to move, taken together (Northampton, Tucson, La Palma): ' + fr(rate(autumn([c for c in N if c['st'] in STILL]))))
for st in STILL: print(f'    {NAME.get(st, st):<20}' + fr(rate(autumn([c for c in N if c['st'] == st]))))
print('P3. the same in the five towns together: ' + fr(rate(autumn([c for c in N if c['st'] in TOWNS]))))
d3 = [c for c in N if c['st'] in DARK3]
print("P4. the three northern dark places: dawn beginning at star time 22 to 2 h or 12 to 14 h, the last tenth the darkest on " + f(sh([c['tenth'] == 9 for c in d3 if span(c['lst1'], ((22, 24), (0, 2), (12, 14)))])) + '; at 4 to 6 h or 18 to 20 h on ' + f(sh([c['tenth'] == 9 for c in d3 if span(c['lst1'], ((4, 6), (18, 20)))])))
nt = [c for c in N if c['lat'] > 0 and c['cls'] != 'lit']
print('P5. northern places not in towns: of nights whose dark hours take in star time 1 h, the darkest tenth has its middle at 0 to 2 h on ' + f(sh([0 <= c['lst'] < 2 for c in nt if covers(c, 0)])) + '; of those that take in 21 h, at 20 to 22 h on ' + f(sh([20 <= c['lst'] < 22 for c in nt if covers(c, 20)])))
cd = lambda S: float(np.median([np.corrcoef(c['mt'], c['gb'])[0, 1] for c in S])) if S else float('nan')
print(f"P6. how closely a night's ten parts follow the distance from the Milky Way's plane: the four dark places {cd([c for c in N if c['cls'] == 'dark']):+.2f} ({sum(1 for c in N if c['cls'] == 'dark')} nights); the five towns {cd([c for c in N if c['cls'] == 'lit']):+.2f} ({sum(1 for c in N if c['cls'] == 'lit')} nights)")
print('P7. the last tenth the darkest, all nights: ' + f(sh([c['tenth'] == 9 for c in N])) + '; year by year: ' + '; '.join(f"{y}: {sh([c['tenth'] == 9 for c in N if c['y'] == y])[0]:.1f} ({sum(1 for c in N if c['y'] == y)} nights)" for y in years))
big = [y for y in years if sum(1 for c in N if c['y'] == y) >= 150]; low = [y for y in big if sh([c['tenth'] == 9 for c in N if c['y'] == y])[0] < 12.5]
print(f'P8. years with 150 nights or more: {len(big)}; of them with the last tenth the darkest on fewer than 12.5 in 100: {len(low)} {low}')
print('P9. the darkest tenth in the second half, all nights: ' + f(sh([c['tenth'] >= 5 for c in N])))
print('P10. the five towns, the end of the night darker than its beginning: ' + f(sh([c['dd'] > 0 for c in N if c['cls'] == 'lit' and c['ends']])) + '; year by year: ' + '; '.join(f"{y}: {f(sh([c['dd'] > 0 for c in N if c['cls'] == 'lit' and c['ends'] and c['y'] == y]))}" for y in years))
print('\nfor the record, not lines:')
print('   Morata de Jalón, the slide: ' + fr(rate(autumn([c for c in N if c['st'] == 'stars225']))))
print('   the seven together: ' + fr(rate(autumn([c for c in N if c['st'] in MOVERS and c['lat'] > 0]))) + '; the three dark northern places: ' + fr(rate(autumn(d3))))
for k in ('lit', 'between', 'dark'):
    print(f"   {k}: the last tenth the darkest by year: " + '; '.join(f"{y}: {sh([c['tenth'] == 9 for c in N if c['y'] == y and c['cls'] == k])[1]} of {sh([c['tenth'] == 9 for c in N if c['y'] == y and c['cls'] == k])[2]}" for y in years))
print('   nights by place and year:')
for st in TOWNS + STILL + ['stars225'] + ['stars24', 'stars9', 'stars426', 'stars35', 'stars477', 'stars62', 'stars289']:
    print(f"   {NAME.get(st, st):<20}" + ' '.join(f"{y}:{sum(1 for c in N if c['st'] == st and c['y'] == y):>3}" for y in years) + f"   autumn nights {len(autumn([c for c in N if c['st'] == st]))}")
print('   end of the night darker than its beginning: ' + '; '.join(f"{k} {f(sh([c['dd'] > 0 for c in N if c['cls'] == k and c['ends']]))}" for k in ('lit', 'between', 'dark')))
