# For the page on the darker northern twilight of 2019, after the twentieth sheet: the question that sheet put to
# the second make, put to the first make's northern places already in hand (my reduction: cache2/depth.pkl and
# cache2/years.pkl; one chip a place, the chip of 2021; the two odd units left out, as in raikoke_night.out).
# The reading with the Sun 3 degrees down, August to December of a year less the same months of the year before
# (the mean over the months both years give, three or more), place by place, and the middle over the places
# (three or more), for every pair of years in hand. Then the same places' ageing over the three years from 2018 to
# 2021, which spans the darkening. Magnitudes; positive: the later year reads darker. Nothing here was sealed
# beforehand: these readings had all been seen.
import pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
DP = mod('depth', B + 'src/depth.py')
R = dict(pickle.load(open(B + 'cache2/depth.pkl', 'rb'))); R.update(pickle.load(open(B + 'cache2/years.pkl', 'rb')))
def readings(st, dp=3.0):
    chips = {}
    for (s, y, m), r in R.items():
        if s == st and y == 2021 and r is not None and DP.monthfig(r, dp) is not None: chips[(r.get('mac') or '')[-8:]] = chips.get((r.get('mac') or '')[-8:], 0) + 1
    if not chips: return {}
    ch = max(chips, key=chips.get)
    return {(y, m): DP.monthfig(r, dp) for (s, y, m), r in R.items() if s == st and r is not None and (r.get('mac') or '')[-8:] == ch and DP.monthfig(r, dp) is not None}
T1 = {st: readings(st) for st in DP.NORTH if st not in ('stars4', 'stars426')}; T1 = {st: v for st, v in T1.items() if v}
LATE = (8, 9, 10, 11, 12); pct = lambda mag: 100 * (1 - 10 ** (-0.4 * mag))
def step(st, y1, y0, months, least=3, per=1):
    d = [(T1[st][(y1, m)] - T1[st][(y0, m)]) / per for m in months if (y1, m) in T1[st] and (y0, m) in T1[st]]
    return float(np.mean(d)) if len(d) >= least else None
def middle(v): v = [x for x in v if x is not None]; return (float(np.median(v)), len(v), min(v), max(v)) if len(v) >= 3 else None
if __name__ == '__main__':
    years = sorted({k[0] for st in T1 for k in T1[st]}); print(f'{len(T1)} northern places of the first make in hand; years {years[0]} to {years[-1]}')
    print('August to December of a year less the same months of the year before, at 3 degrees: the middle over the places (their number), per cent of light, the smallest and the largest')
    S = {}
    for y in years[1:]:
        t = middle([step(st, y, y - 1, LATE) for st in T1]); S[y] = t
        print(f'   {y} less {y - 1}: ' + ('fewer than three places' if t is None else f'{t[0]:+.3f} ({t[1]})  {pct(t[0]):+5.1f} per cent   from {t[2]:+.2f} to {t[3]:+.2f}'))
    ordinary = [y for y in years[1:] if y not in (2019, 2020) and S[y] is not None]; o = [S[y][0] for y in ordinary]
    print(f'the {len(ordinary)} pairs of years other than 2019 and 2020: from {min(o):+.3f} to {max(o):+.3f} ({pct(min(o)):+.1f} to {pct(max(o)):+.1f} per cent), the middle {np.median(o):+.3f} ({pct(np.median(o)):+.1f} per cent)')
    print(f'2019: {S[2019][0]:+.3f} ({pct(S[2019][0]):+.1f} per cent), {S[2019][0] / max(o):.1f} times the largest of them; 2020: {S[2020][0]:+.3f} ({pct(S[2020][0]):+.1f} per cent; {100 * (10 ** (-0.4 * S[2020][0]) - 1):.0f} per cent brighter)')
    sy = [(st, y, step(st, y, y - 1, LATE)) for st in T1 for y in ordinary]; sy = [x for x in sy if x[2] is not None]; big = [x for x in sy if x[2] >= S[2019][0]]
    print(f'single places: of {len(sy)} place-years of those pairs, {len(big)} at or above {S[2019][0]:+.3f}: ' + ', '.join(f'{st} {y} {v:+.2f}' for st, y, v in big))
    low19 = min(v for st in T1 for v in [step(st, 2019, 2018, LATE)] if v is not None); n19 = sum(1 for x in sy if x[2] >= low19)
    print(f'   the smallest of the places in 2019 is {low19:+.3f}; of the {len(sy)} place-years of the other pairs {n19} are at or above that: ' + ', '.join(f'{st} {y} {v:+.2f}' for st, y, v in sy if v >= low19))
    neg = [x for x in sy if x[2] <= S[2020][0]]; print(f'   and {len(neg)} at or below {S[2020][0]:+.3f}: ' + ', '.join(f'{st} {y} {v:+.2f}' for st, y, v in neg))
    p19 = [(st, step(st, 2019, 2018, LATE)) for st in T1]; p19 = [x for x in p19 if x[1] is not None]; print('   2019 place by place: ' + ', '.join(f'{st} {v:+.2f}' for st, v in p19))
    p20 = [(st, step(st, 2020, 2019, LATE)) for st in T1]; p20 = [x for x in p20 if x[1] is not None]; print('   2020 place by place: ' + ', '.join(f'{st} {v:+.2f}' for st, v in p20))
    a = middle([step(st, 2021, 2018, range(1, 13), least=6, per=3) for st in T1])
    print(f'the ageing over the three years 2018 to 2021 (2021 less 2018, the same month, six months or more, divided by three): the middle {a[0]:+.3f} a year ({a[1]} places), {pct(a[0]):.1f} per cent; from {a[2]:+.3f} to {a[3]:+.3f}')
