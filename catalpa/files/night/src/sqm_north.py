# The sixteenth sheet scored: did the twilight read darker after the eruption of Raikoke (June 2019) in the second
# make of meter too? Every station of the second network in 2018 to 2020 (data/sqm3, fetched by src/sqm_fetch4.py):
# the meter's own reading when the Sun passes 3 and 5 degrees below the horizon (straight-line interpolation in the
# Sun's altitude between two readings up to eleven minutes apart; evenings and mornings apart, the middle of each
# over a month, five or more of each, the two averaged, as in the eleventh sheet), and the differences between the
# same months of two years. A station gives a depth only if its ordinary reading there is 0.3 magnitude or more
# fainter than the brightest reading its files hold. Positive: the later reading is darker.
import os, csv, json, importlib.util, datetime as dt
import numpy as np
B = '/home/agent1/night/'
def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
TW = mod('twilight', B + 'src/twilight.py'); F4 = mod('f4', B + 'src/sqm_fetch4.py')
DEPTHS = (3.0, 5.0); GAP = 660.0; LATE = (8, 9, 10, 11, 12); EARLY = (1, 2, 3, 4, 5, 6)
def month(code, lat, lon, y, m):
    fn = B + f'data/sqm3/{code}_{y}-{m:02d}.csv'
    if not os.path.exists(fn): return None
    T, M = [], []
    for row in csv.DictReader(open(fn, encoding='utf-8')):
        try: v = float(row['nsb']); t = dt.datetime.strptime(row['received_utc'][:19], '%Y-%m-%d %H:%M:%S')
        except (ValueError, KeyError, TypeError): continue
        if v > 0: T.append((t - TW.T2000).total_seconds()); M.append(v)
    if len(T) < 50: return None
    o = np.argsort(T); T = np.array(T)[o]; M = np.array(M)[o]; alt = TW.sun_alt_vec(T, lat, lon); ok = (np.diff(T) <= GAP) & (np.diff(T) > 0); out = {}
    for dp in DEPTHS:
        a0 = alt[:-1] + dp; a1 = alt[1:] + dp; ev, mo = [], []
        for k in np.where(ok & (a0 * a1 < 0))[0]:
            fr = a0[k] / (a0[k] - a1[k]); (ev if alt[k + 1] < alt[k] else mo).append(float(M[k] + fr * (M[k + 1] - M[k])))
        out[dp] = 0.5 * (float(np.median(ev)) + float(np.median(mo))) if len(ev) >= 5 and len(mo) >= 5 else None
    return out
if __name__ == '__main__':
    ST = F4.stations(); bright = json.load(open(B + 'data/sqm3/brightest.json')); R = {}
    for c, (lat, lon, country, inst) in ST.items():
        for y in (2018, 2019, 2020):
            for m in range(1, 13): R[(c, y, m)] = month(c, lat, lon, y, m)
    def fig(c, y, m, dp): r = R[(c, y, m)]; return None if r is None else r[dp]
    def usable(c, dp):       # the ceiling rule
        v = [fig(c, y, m, dp) for y in (2018, 2019, 2020) for m in range(1, 13)]; v = [x for x in v if x is not None]
        return bool(v) and c in bright and float(np.median(v)) >= bright[c] + 0.3
    def diff(c, y1, y0, months, dp):    # the mean over a stretch of (the month in y1 less the same month in y0); three months or more
        if not usable(c, dp): return None
        d = [fig(c, y1, m, dp) - fig(c, y0, m, dp) for m in months if fig(c, y1, m, dp) is not None and fig(c, y0, m, dp) is not None]
        return float(np.mean(d)) if len(d) >= 3 else None
    f = lambda v: '    . ' if v is None else f'{v:+6.2f}'
    def middle(v): v = [x for x in v if x is not None]; return (float(np.median(v)), len(v)) if v else (None, 0)
    g = lambda t: 'none' if t[0] is None else f'{t[0]:+.3f} ({t[1]})'
    order = sorted(ST, key=lambda c: -ST[c][0])
    print('each station of the second network that gives a figure, from north to south (magnitudes; positive: the later year reads darker; . no figure)')
    print('   station  latitude  country         | at 3 degrees: late 2019 less late 2018, early 2019 less early 2018, their difference, late 2020 less late 2019 | at 5 degrees: the same four')
    rows = {}
    for c in order:
        r = []
        for dp in DEPTHS:
            a = diff(c, 2019, 2018, LATE, dp); b = diff(c, 2019, 2018, EARLY, dp); r += [a, b, (a - b) if a is not None and b is not None else None, diff(c, 2020, 2019, LATE, dp)]
        rows[c] = r
        if any(x is not None for x in r): print(f"   {c:<8} {ST[c][0]:+7.1f}   {ST[c][2][:14]:<14}  | " + ' '.join(f(x) for x in r[:4]) + '  | ' + ' '.join(f(x) for x in r[4:]))
    N = [c for c in order if ST[c][0] >= 20.0]; LOW = [c for c in N if ST[c][0] < 30.0]; S = [c for c in order if ST[c][0] < -15.0]; TR = [c for c in order if -15.0 <= ST[c][0] < 20.0]
    print('\nThe lines of the sixteenth sheet (stations at 20 north or more; unrounded figures; marks included)')
    r1 = middle([rows[c][0] for c in N]); print(f"R1. at 3 degrees, August to December 2019 less August to December 2018: the middle at +0.10 or above: {g(r1)}: {'void' if r1[1] < 4 else ('held' if r1[0] >= 0.10 else 'failed')}")
    r2 = middle([rows[c][2] for c in N]); print(f"R2. at 3 degrees, that less (January to June 2019 less January to June 2018): the middle at +0.08 or above: {g(r2)}: {'void' if r2[1] < 4 else ('held' if r2[0] >= 0.08 else 'failed')}")
    r3 = middle([rows[c][3] for c in N]); print(f"R3. at 3 degrees, August to December 2020 less August to December 2019: the middle at 0.00 or below: {g(r3)}: {'void' if r3[1] < 4 else ('held' if r3[0] <= 0.0 else 'failed')}")
    r4 = middle([rows[c][4] for c in N]); print(f"R4. at 5 degrees, August to December 2019 less August to December 2018: the middle at +0.10 or above: {g(r4)}: {'void' if r4[1] < 4 else ('held' if r4[0] >= 0.10 else 'failed')}")
    r5 = middle([rows[c][2] for c in LOW]); print(f"R5. the stations between 20 and 30 north, the difference of R2: the middle at +0.05 or above: {g(r5)}: {'void' if r5[1] < 3 else ('held' if r5[0] >= 0.05 else 'failed')}")
    print('\nfor the record: stations south of 15 south: ' + ('; '.join(f"{c} ({ST[c][0]:+.1f}): October to December 2019 less 2018 at 3 degrees {f(diff(c, 2019, 2018, (10, 11, 12), 3.0))}, January to March 2020 less 2019 {f(diff(c, 2020, 2019, (1, 2, 3), 3.0))}" for c in S) or 'none'))
    print('for the record: stations between 15 south and 20 north, the four figures at 3 degrees: ' + ('; '.join(f"{c} ({ST[c][0]:+.1f}): " + ' '.join(f(x) for x in rows[c][:4]) for c in TR if any(x is not None for x in rows[c][:4])) or 'none'))
    print('month by month at 3 degrees, the middle over the northern stations of (the month less the same month a year before), hundredths; stations below:')
    for y in (2019, 2020):
        v = [[fig(c, y, m, 3.0) - fig(c, y - 1, m, 3.0) for c in N if usable(c, 3.0) and fig(c, y, m, 3.0) is not None and fig(c, y - 1, m, 3.0) is not None] for m in range(1, 13)]
        print(f'   {y} less {y - 1}: ' + ' '.join(f'{100 * np.median(x):+4.0f}' if len(x) >= 3 else '   .' for x in v) + '   | ' + ' '.join(f'{len(x):2d}' for x in v))
