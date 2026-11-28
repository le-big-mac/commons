# The seventeenth sheet, its first part, scored: did the Korean units of the second make change in mid-2019? Their
# readings on moonless nights (the Sun 18 degrees or more down, the Moon below the horizon; every tenth reading),
# the middle of each night with twenty readings or more, and for a month the clear-night level: the reading that
# three quarters of its nights are brighter than (five nights or more). A station's figure is the mean over
# September, October and November of 2019 less the same month of 2018 (two months or more).
import os, csv, importlib.util, datetime as dt
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('f4', B + 'src/sqm_fetch4.py'); F4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(F4)
TW = F4.TW
def month(code, lat, lon, y, m):
    fn = B + f'data/sqm4/{code}_{y}-{m:02d}.csv'
    if not os.path.exists(fn): return None
    T, M = [], []
    for row in csv.DictReader(open(fn, encoding='utf-8')):
        try: v = float(row['nsb']); t = dt.datetime.strptime(row['received_utc'][:19], '%Y-%m-%d %H:%M:%S')
        except (ValueError, KeyError, TypeError): continue
        if v > 0: T.append((t - TW.T2000).total_seconds()); M.append(v)
    nights = {}
    for k in range(0, len(T), 10):
        if TW.sky.moon_alt(TW.T2000 + dt.timedelta(seconds=float(T[k])), lat, lon) > 0: continue
        nights.setdefault(int((T[k] + lon * 240.0 - 43200.0) // 86400), []).append(M[k])
    v = [float(np.median(x)) for x in nights.values() if len(x) >= 20]
    return (float(np.percentile(v, 75)), float(np.percentile(v, 50)), len(v)) if len(v) >= 5 else None
if __name__ == '__main__':
    ST = {c: v for c, v in F4.stations().items() if v[2] == 'Korea'}; AUT = (9, 10, 11); out = {}
    print('the Korean stations at night, September to November 2019 less 2018 (magnitudes; positive: darker): the clear-night level, the middle night, months')
    for c in sorted(ST, key=lambda c: -ST[c][0]):
        R = {(y, m): month(c, ST[c][0], ST[c][1], y, m) for y in (2018, 2019) for m in AUT}
        d = [(R[(2019, m)][0] - R[(2018, m)][0], R[(2019, m)][1] - R[(2018, m)][1]) for m in AUT if R[(2019, m)] and R[(2018, m)]]
        if len(d) >= 2: out[c] = (float(np.mean([x[0] for x in d])), float(np.mean([x[1] for x in d]))); print(f'   {c:<6} {ST[c][0]:+6.1f}  {out[c][0]:+.3f}  {out[c][1]:+.3f}  ({len(d)} months)')
    v = [x[0] for x in out.values()]
    print('\nThe first line of the seventeenth sheet (unrounded; mark included)')
    print(f"K1. the clear-night level at the middle of the Korean stations, September to November 2019 less 2018, within 0.08 of nothing: {('none' if not v else f'{np.median(v):+.3f} ({len(v)})')}: {'void' if len(v) < 3 else ('held' if abs(np.median(v)) <= 0.08 else 'failed')}")
