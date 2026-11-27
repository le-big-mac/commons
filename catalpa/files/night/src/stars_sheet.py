# The lines of the third sheet (expectations-stars.md): does the darkest part of the night keep time by the stars under
# darker skies and by the clock in towns? Reads cache/nights<YEAR>.pkl, which years_cache.py makes from the photometer
# files by the frozen method (dawnlib.py). Usage: stars_sheet.py REF1,REF2 TEST1,TEST2
#   the first list is the years the rates were learned on (2024,2025); the second the years the lines are about.
# Run with the same list twice it prints the reference figures. Nothing in it depends on which years are given.
import sys, pickle, importlib.util, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('sky', '/home/agent1/night/src/sky.py'); sky = importlib.util.module_from_spec(spec); spec.loader.exec_module(sky)
def get(years):
    N = []
    for y in years:
        for c in pickle.load(open(f'/home/agent1/night/cache/nights{y}.pkl', 'rb')):
            c['y'] = int(y); tm = c['dusk'] + dt.timedelta(hours=(c['tenth'] + 0.5) / 10 * c['L'])
            st = lambda t: ((sky.gmst_deg(sky.jd(t)) + c['lon']) % 360) / 15.0
            c['lst'] = st(tm); c['lst0'] = st(c['dusk']); c['lst1'] = st(c['dawn'])
            sol = (tm.hour + tm.minute / 60 + tm.second / 3600 + c['lon'] / 15.0) % 24; c['sol'] = sol - 24 if sol > 12 else sol
            c['doy'] = (c['d'] - dt.date(c['d'].year, 1, 1)).days; N.append(c)
    return N
REF = get(sys.argv[1].split(',')); TEST = get(sys.argv[2].split(','))
print(f"learned on {sys.argv[1]} ({len(REF)} cleaned nights); lines about {sys.argv[2]} ({len(TEST)} cleaned nights; by year: " + ', '.join(f"{y}: {sum(1 for c in TEST if c['y'] == y)}" for y in sorted({c['y'] for c in TEST})) + ')')
def north(N, kinds): return [c for c in N if c['lat'] > 0 and c['cls'] in kinds]
def rate(S):
    """minutes a day by which the middle of the darkest tenth moves, by the Sun's clock, with its standard error"""
    if len(S) < 20: return None
    x = np.array([c['doy'] for c in S], float); yv = np.array([c['sol'] for c in S]) * 60
    a, b = np.polyfit(x, yv, 1); r = yv - (a * x + b); se = np.sqrt(np.sum(r ** 2) / (len(S) - 2) / np.sum((x - x.mean()) ** 2)); return float(a), float(se), len(S)
def autumn(S): return [c for c in S if 213 <= c['doy'] < 304]          # 1 August to 30 October (31 October in a leap year)
def covers(c, h):
    a, b = c['lst0'], c['lst1']; mid = h + 1.0
    return (a <= mid <= b) if a <= b else (mid >= a or mid <= b)
def inspan(x, spans): return any(lo <= x < hi for lo, hi in spans)
def share(v): return (100 * float(np.mean(v)), int(np.sum(v)), len(v)) if len(v) else (float('nan'), 0, 0)
def fmt(s): return f'{s[0]:.0f} in 100 ({s[1]} of {s[2]})'
out = {}
r_dark = rate(autumn(north(TEST, ('dark',)))); r_lit = rate(autumn(north(TEST, ('lit',)))); r_btw = rate(autumn(north(TEST, ('between',))))
f = lambda r: (f'{r[0]:+.1f} minutes a day, give or take {r[1]:.1f} ({r[2]} nights)' if r else 'too few nights (fewer than 20)')
print('\nS1. August to October, the three northern dark places: how fast the darkest part moves by the Sun\'s clock (the stars give -3.9): ' + f(r_dark))
print('S2. the same, the five towns: ' + f(r_lit))
print('S3. the same, the seven places between: ' + f(r_btw))
nt = north(TEST, ('between', 'dark'))
bad = [c['tenth'] == 9 for c in nt if inspan(c['lst1'], ((4, 6), (18, 20)))]; good = [c['tenth'] == 9 for c in nt if inspan(c['lst1'], ((22, 24), (0, 2), (12, 14)))]
print('S4. northern places not in towns, nights whose dawn begins at star time 4 to 6 h or 18 to 20 h: the last tenth the darkest on ' + fmt(share(bad)))
print('S5. the same places, dawn beginning at star time 22 to 2 h or 12 to 14 h: the last tenth the darkest on ' + fmt(share(good)))
a = [0 <= c['lst'] < 2 for c in nt if covers(c, 0)]; b = [20 <= c['lst'] < 22 for c in nt if covers(c, 20)]
print('S6. the same places: of nights whose dark hours take in star time 1 h, the darkest tenth has its middle at 0 to 2 h on ' + fmt(share(a)) + '; of those that take in 21 h, at 20 to 22 h on ' + fmt(share(b)))
sep = [c['tenth'] == 9 for c in TEST if c['lat'] > 0 and c['d'].month == 9]
print('S7. September, all northern places: the last tenth the darkest on ' + fmt(share(sep)))
cd = [float(np.corrcoef(c['mt'], c['gb'])[0, 1]) for c in TEST if c['cls'] == 'dark']; cl = [float(np.corrcoef(c['mt'], c['gb'])[0, 1]) for c in TEST if c['cls'] == 'lit']
print(f'S8. how closely the ten parts of a night follow the distance of the point overhead from the Milky Way\'s plane (correlation, middle night): the four dark places {np.median(cd):+.2f} ({len(cd)} nights); the five towns {np.median(cl):+.2f} ({len(cl)} nights)')
tn = np.array([c['tenth'] for c in TEST])
print('S9. all nights, every place: the last tenth the darkest on ' + fmt(share(tn == 9)))
print('S10. all nights: the darkest tenth is the ninth or the last on ' + fmt(share(tn >= 8)))
print('S11. all nights: the darkest tenth falls in the second half on ' + fmt(share(tn >= 5)))
ark = [c for c in TEST if c['st'] == 'stars477']; v = [16 <= c['lst'] < 20 for c in ark if covers(c, 17)]
print('S12. Arkaroola: of nights whose dark hours take in star time 18 h, when the middle of the Milky Way is overhead there, the darkest tenth has its middle at 16 to 20 h on ' + fmt(share(v)) + f'; all its nights: {len(ark)}')
v = [c['dd'] > 0 for c in TEST if c['cls'] == 'lit' and c['ends']]
print('S13. the five towns: the end of the night darker than its beginning on ' + fmt(share(v)))
# not a line: the share foretold from the star time at which dawn begins, with rates learned on the reference years
refnt = north(REF, ('between', 'dark')); spans = [(h, h + 2) for h in range(0, 24, 2)]
p = {}
for lo, hi in spans:
    v = [c['tenth'] == 9 for c in refnt if lo <= c['lst1'] < hi]; p[lo] = float(np.mean(v)) if v else float(np.mean([c['tenth'] == 9 for c in refnt]))
def foretold(S): return 100 * float(np.mean([p[int(c['lst1'] // 2) * 2] for c in S])) if S else float('nan')
print('\nfor the record, not lines:')
act = share([c['tenth'] == 9 for c in nt])
print(f'   northern places not in towns, all nights: the last tenth the darkest on {fmt(act)}; foretold from the star time of dawn, by the rates of the reference years: {foretold(nt):.1f} in 100')
for y in sorted({c['y'] for c in TEST}):
    S = [c for c in nt if c['y'] == y]; print(f'      {y}: {fmt(share([c["tenth"] == 9 for c in S]))}; foretold {foretold(S):.1f}')
print('   the darkest tenth by star time, northern places not in towns: nights with it there / nights whose dark hours take in the middle of the span')
print('   ' + ' '.join(f"{h}-{h + 2}h:{sum(1 for c in nt if h <= c['lst'] < h + 2)}/{sum(1 for c in nt if covers(c, h))}" for h in range(0, 24, 2)))
print('   by star time at the start of dawn: nights / last tenth the darkest')
print('   ' + ' '.join(f"{h}-{h + 2}h:{sum(1 for c in nt if h <= c['lst1'] < h + 2)}/{sum(1 for c in nt if h <= c['lst1'] < h + 2 and c['tenth'] == 9)}" for h in range(0, 24, 2)))
tw = north(TEST, ('lit',))
print('   the five towns, by star time at the start of dawn: ' + ' '.join(f"{h}-{h + 2}h:{sum(1 for c in tw if h <= c['lst1'] < h + 2)}/{sum(1 for c in tw if h <= c['lst1'] < h + 2 and c['tenth'] == 9)}" for h in range(0, 24, 2)))
print('   by month, all places: cleaned nights / last tenth the darkest')
for y in sorted({c['y'] for c in TEST}): print(f'   {y}: ' + ' '.join(f"{m}:{sum(1 for c in TEST if c['y'] == y and c['d'].month == m)}/{sum(1 for c in TEST if c['y'] == y and c['d'].month == m and c['tenth'] == 9)}" for m in range(1, 13)))
for y in sorted({c['y'] for c in TEST}):
    t = np.array([c['tenth'] for c in TEST if c['y'] == y]); print(f'   {y}, all nights ({len(t)}): the last tenth the darkest on {100 * np.mean(t == 9):.1f} in 100; the ninth or the last {100 * np.mean(t >= 8):.1f}; the second half {100 * np.mean(t >= 5):.1f}')
for k in ('lit', 'between', 'dark'):
    v = [c['dd'] > 0 for c in TEST if c['cls'] == k and c['ends']]; print(f'   end of the night darker than its beginning, {k}: {fmt(share(v))}')
for lab, lo, hi in (('March to June', 60, 181),):
    for k in ('lit', 'between', 'dark'): print(f'   {lab}, {k}: ' + f(rate([c for c in north(TEST, (k,)) if lo <= c['doy'] < hi])))
