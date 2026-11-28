# After the sixteenth sheet, at the checker's asking: did the first make's units change in mid-2019? Their own
# moonless-night readings, August to December 2019 less 2018, by my reduction from the files (data/ida2018,
# data/ida2019): readings with the Sun 18 degrees or more down and the Moon below the horizon, every tenth one,
# the middle of each night (twenty readings or more), then over a month the middle night and the night that
# three quarters are brighter than (five nights or more). Not a test.
import os, re, glob, importlib.util, datetime as dt
from multiprocessing import Pool
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('depth', B + 'src/depth.py'); DP = importlib.util.module_from_spec(spec); spec.loader.exec_module(DP)
TW = DP.TW
def job(a):
    st, y, m, fn = a
    txt = open(fn, encoding='utf-8', errors='replace').read()
    if '# END OF HEADER' not in txt: return (st, y, m), None
    head, body = txt.split('# END OF HEADER', 1); mp = re.search(r'# Position: ([-\d.]+), ([-\d.]+)', head)
    if mp: lat, lon = float(mp.group(1)), float(mp.group(2))
    elif st in DP.HOME: lat, lon = DP.HOME[st]
    elif st in DP.geo and DP.geo[st]['latitude']: lat, lon = float(DP.geo[st]['latitude']), float(DP.geo[st]['longitude'])
    else: return (st, y, m), None
    T, F = [], []
    for line in body.splitlines():
        p = line.split(';')
        if len(p) < 7: continue
        try: f = float(p[4]); t = dt.datetime.strptime(p[0][:19], '%Y-%m-%dT%H:%M:%S')
        except ValueError: continue
        if f > 0: T.append((t - TW.T2000).total_seconds()); F.append(f)
    if len(T) < 100: return (st, y, m), None
    T = np.array(T); M = 20.5 - 2.5 * np.log10(np.array(F)); alt = TW.sun_alt_vec(T, lat, lon); idx = np.where(alt < -18.0)[0][::10]; nights = {}
    for k in idx:
        tc = TW.T2000 + dt.timedelta(seconds=float(T[k]))
        if TW.sky.moon_alt(tc, lat, lon) > 0: continue
        nights.setdefault(int((T[k] + lon * 240.0 - 43200.0) // 86400), []).append(M[k])      # a night belongs to the local day it began on
    v = [float(np.median(x)) for x in nights.values() if len(x) >= 20]
    return (st, y, m), ((float(np.percentile(v, 50)), float(np.percentile(v, 75)), len(v)) if len(v) >= 5 else None)
if __name__ == '__main__':
    jobs = [(st, y, int(os.path.basename(fn)[-6:-4]), fn) for st in DP.NORTH for y in (2018, 2019) for fn in sorted(glob.glob(B + f'data/ida{y}/{st}_{y}-??.dat'))]
    with Pool(12) as p: R = dict(p.map(job, jobs, chunksize=2))
    LATE = (8, 9, 10, 11, 12); f = lambda v: '    . ' if v is None else f'{v:+6.2f}'
    print('the first make, moonless night, August to December 2019 less 2018 (magnitudes; positive: darker): the middle night, the darker nights, and the months both years give')
    A, Bq = [], []
    for st in DP.NORTH:
        d = [(R[(st, 2019, m)][0] - R[(st, 2018, m)][0], R[(st, 2019, m)][1] - R[(st, 2018, m)][1]) for m in LATE if R.get((st, 2019, m)) and R.get((st, 2018, m))]
        if len(d) >= 2:
            a, b = float(np.mean([x[0] for x in d])), float(np.mean([x[1] for x in d])); print(f'   {st:<10} {f(a)} {f(b)}   ({len(d)} months)')
            if st not in ('stars4', 'stars426'): A.append(a); Bq.append(b)
    print(f'   the middle over the places (the two odd units left out): {np.median(A):+.2f} and {np.median(Bq):+.2f} ({len(A)} places); places within 0.08 of nothing by the middle night: {sum(abs(x) <= 0.08 for x in A)}')
