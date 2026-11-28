# The twentieth sheet scored: how unusual was the darker twilight of late 2019 in the second make of meter, set
# against the years before it? Every northern station of the second network, 2015 to 2020 (data/sqm5 for 2015 to
# 2017, fetched by src/sqm_fetch6.py; data/sqm3 for 2018 to 2020, fetched by src/sqm_fetch4.py): the meter's own
# reading when the Sun passes 3 degrees below the horizon, reduced as in the sixteenth sheet (straight-line
# interpolation in the Sun's altitude between two readings up to eleven minutes apart; evenings and mornings apart,
# the middle of each over a month, five or more of each, the two averaged), and the differences between the same
# months of two years. Two rules besides: a station gives a figure only if its ordinary reading at 3 degrees is 0.3
# magnitude or more fainter than the brightest reading its files hold, and only if every row of the months used
# carries one and the same serial number (not an empty one). Positive: the later reading is darker.
# With --inhand only the years already seen (2018 to 2020) are read.
import os, sys, csv, json, importlib.util, datetime as dt
import numpy as np
B = '/home/agent1/night/'
def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
TW = mod('twilight', B + 'src/twilight.py'); F4 = mod('f4', B + 'src/sqm_fetch4.py')
DP = 3.0; GAP = 660.0; LATE = (8, 9, 10, 11, 12); SMOKE = (9, 10, 11, 12)
INHAND = '--inhand' in sys.argv
YEARS = (2018, 2019, 2020) if INHAND else (2015, 2016, 2017, 2018, 2019, 2020)
DIRS = {2015: 'data/sqm5/', 2016: 'data/sqm5/', 2017: 'data/sqm5/', 2018: 'data/sqm3/', 2019: 'data/sqm3/', 2020: 'data/sqm3/'}
def norm(s): return (s or '').strip().lstrip('0')
def month(code, lat, lon, y, m):
    fn = B + DIRS[y] + f'{code}_{y}-{m:02d}.csv'
    if not os.path.exists(fn): return None
    T, M, S = [], [], []
    for row in csv.DictReader(open(fn, encoding='utf-8')):
        try: v = float(row['nsb']); t = dt.datetime.strptime(row['received_utc'][:19], '%Y-%m-%d %H:%M:%S')
        except (ValueError, KeyError, TypeError): continue
        if v > 0: T.append((t - TW.T2000).total_seconds()); M.append(v); S.append(norm(row.get('sqmle_serial_number')))
    if len(T) < 50: return None
    o = np.argsort(T); T = np.array(T)[o]; M = np.array(M)[o]; alt = TW.sun_alt_vec(T, lat, lon); ok = (np.diff(T) <= GAP) & (np.diff(T) > 0)
    a0 = alt[:-1] + DP; a1 = alt[1:] + DP; ev, mo = [], []
    for k in np.where(ok & (a0 * a1 < 0))[0]:
        fr = a0[k] / (a0[k] - a1[k]); (ev if alt[k + 1] < alt[k] else mo).append(float(M[k] + fr * (M[k + 1] - M[k])))
    if len(ev) < 5 or len(mo) < 5: return None
    return (0.5 * (float(np.median(ev)) + float(np.median(mo))), frozenset(S))
if __name__ == '__main__':
    ST = F4.stations(); bright = {}
    for d in ('data/sqm3/', 'data/sqm5/'):
        p = B + d + 'brightest.json'
        if os.path.exists(p) and not (INHAND and d == 'data/sqm5/'):
            for c, v in json.load(open(p)).items(): bright[c] = min(bright.get(c, 99.0), v)
    R = {(c, y, m): month(c, lat, lon, y, m) for c, (lat, lon, country, inst) in ST.items() for y in YEARS for m in range(1, 13)}
    def fig(c, y, m): r = R.get((c, y, m)); return None if r is None else r[0]
    def usable(c):          # the ceiling rule, over every year read
        v = [fig(c, y, m) for y in YEARS for m in range(1, 13)]; v = [x for x in v if x is not None]
        return bool(v) and c in bright and float(np.median(v)) >= bright[c] + 0.3
    def one_serial(c, pairs):   # every row of the months used carries one and the same serial number, not an empty one
        s = set()
        for y, m in pairs: s |= R[(c, y, m)][1]
        return len(s) == 1 and '' not in s
    def diff(c, y1, y0, months):    # the mean over a stretch of (the month in y1 less the same month in y0); three months or more
        if not usable(c): return None, 'ceiling'
        ms = [m for m in months if fig(c, y1, m) is not None and fig(c, y0, m) is not None]
        if len(ms) < 3: return None, 'months'
        if not one_serial(c, [(y, m) for m in ms for y in (y1, y0)]): return None, 'serial'
        return float(np.mean([fig(c, y1, m) - fig(c, y0, m) for m in ms])), ''
    def between(c, y0):     # a year less the mean of the years on either side, September to December; three months or more; one serial
        ys = (y0 - 1, y0, y0 + 1)
        if not usable(c) or not all(y in YEARS for y in ys): return None
        ms = [m for m in SMOKE if all(fig(c, y, m) is not None for y in ys)]
        if len(ms) < 3 or not one_serial(c, [(y, m) for m in ms for y in ys]): return None
        return float(np.mean([fig(c, y0, m) - 0.5 * (fig(c, y0 - 1, m) + fig(c, y0 + 1, m)) for m in ms]))
    f = lambda v: '     . ' if v is None else f'{v:+7.3f}'
    def middle(v): v = [x for x in v if x is not None]; return (float(np.median(v)), len(v)) if v else (None, 0)
    g = lambda t: 'none' if t[0] is None else f'{t[0]:+.3f} ({t[1]})'
    N = sorted((c for c in ST if ST[c][0] >= 20.0), key=lambda c: -ST[c][0]); PAIRS = [y for y in YEARS if y - 1 in YEARS]; MID = [y for y in YEARS if y - 1 in YEARS and y + 1 in YEARS]
    D = {(c, y): diff(c, y, y - 1, LATE) for c in N for y in PAIRS}
    print('each northern station of the second network (20 north or more) that gives a figure, from north to south')
    print('magnitudes at 3 degrees, August to December of the year less August to December of the year before; positive: darker; . no figure (c ceiling, m months, s serial)')
    print('   station  latitude  country        ' + ' '.join(f'{y:>8d}' for y in PAIRS) + ('   | September to December, the year less the mean of the years on either side: ' + ' '.join(str(y) for y in MID)))
    X = {c: between(c, 2017) for c in N}; C = {(c, y): between(c, y) for c in N for y in MID}
    for c in N:
        r = [D[(c, y)] for y in PAIRS]
        if any(x[0] is not None for x in r) or any(C[(c, y)] is not None for y in MID) or any(x[1] == 'serial' for x in r):
            print(f"   {c:<8} {ST[c][0]:+7.1f}   {ST[c][2][:14]:<14} " + ' '.join((f(x[0]) + ' ') if x[0] is not None else f'     .{x[1][:1] or " "} ' for x in r) + '  | ' + ' '.join(f(C[(c, y)]) for y in MID))
    S = {y: middle([D[(c, y)][0] for c in N]) for y in PAIRS}
    print('\nthe middle over the stations, year by year (the number of stations in brackets; fewer than four: not given)')
    for y in PAIRS: print(f"   S({y}) = {g(S[y])}{'' if S[y][1] >= 4 else '   not given'}")
    print('the year less the mean of the years on either side, September to December, the middle over the stations (four or more)')
    for y in MID: t = middle([C[(c, y)] for c in N]); print(f"   C({y}) = {g(t)}{'' if t[1] >= 4 else '   not given'}")
    if INHAND: sys.exit(0)
    print('\nThe lines of the twentieth sheet (unrounded figures; marks included)')
    before = [S[y][0] for y in (2016, 2017, 2018) if S[y][1] >= 4]
    v1 = 'void' if len(before) < 2 else ('held' if max(before) < 0.10 else 'failed')
    print(f"G1. every S of 2016, 2017 and 2018 that can be given (two or more) is below +0.10: the largest {'none' if not before else f'{max(before):+.3f}'} of {len(before)}: {v1}")
    v2 = 'void' if len(before) < 2 or S[2019][1] < 4 else ('held' if S[2019][0] - max(before) >= 0.05 else 'failed')
    print(f"G2. S(2019) is above the largest of them by 0.05 or more: S(2019) {g(S[2019])}, the margin {'none' if v2 == 'void' else f'{S[2019][0] - max(before):+.3f}'}: {v2}")
    sy = [D[(c, y)][0] for c in N for y in (2016, 2017, 2018) if D[(c, y)][0] is not None]; hi = sum(1 for x in sy if x >= 0.14)
    v3 = 'void' if len(sy) < 10 else ('held' if hi / len(sy) < 0.20 else 'failed')
    print(f"G3. of the station-years of 2016, 2017 and 2018 (ten or more), fewer than one in five is at +0.14 or above: {hi} of {len(sy)}: {v3}")
    x4 = middle([X[c] for c in N]); v4 = 'void' if x4[1] < 4 else ('held' if x4[0] >= 0.03 else 'failed')
    print(f"G4. C(2017), September to December 2017 less the mean of 2016 and 2018, the middle over the stations (four or more), at +0.03 or above: {g(x4)}: {v4}")
    EU = [c for c in N if ST[c][0] >= 40.0 and -15.0 <= ST[c][1] <= 40.0]; x5 = middle([X[c] for c in EU]); v5 = 'void' if x5[1] < 1 else ('held' if x5[0] >= 0.05 else 'failed')
    print(f"G5. the same at the stations in Europe (one or more) at +0.05 or above: {g(x5)} [{', '.join(c for c in EU if X[c] is not None)}]: {v5}")
    print('\nfor the record, not lines:')
    sy19 = [D[(c, 2019)][0] for c in N if D[(c, 2019)][0] is not None]
    print(f"   station-years at +0.14 or above: 2016 to 2018 {hi} of {len(sy)}; 2019 {sum(1 for x in sy19 if x >= 0.14)} of {len(sy19)}")
    if sy: print(f"   the station-years of 2016 to 2018: the middle {np.median(sy):+.3f}, the quarters {np.percentile(sy, 25):+.3f} and {np.percentile(sy, 75):+.3f}, the ends {min(sy):+.3f} and {max(sy):+.3f}")
    print('   month by month, the middle over the stations of (the month less the same month a year before), hundredths; the number of stations after the bar')
    for y in PAIRS:
        v = [[fig(c, y, m) - fig(c, y - 1, m) for c in N if usable(c) and fig(c, y, m) is not None and fig(c, y - 1, m) is not None and one_serial(c, [(y, m), (y - 1, m)])] for m in range(1, 13)]
        print(f'   {y} less {y - 1}: ' + ' '.join(f'{100 * np.median(x):+4.0f}' if len(x) >= 3 else '   .' for x in v) + '   | ' + ' '.join(f'{len(x):2d}' for x in v))
