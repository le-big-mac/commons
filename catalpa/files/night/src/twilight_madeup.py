# The twilight measure on made-up changes planted in real readings, before any sheet is sealed on it.
#  A. a step: every reading of 2024 made 0.3 (then 0.6) magnitude darker at five photometers; how much darker does the
#     twilight say 2024 is than the other years, beyond what it said before?
#  B. a drift: a steady photometer made to read 0.08 magnitude a year darker from 2020 on; what drift comes out,
#     from all months and from six months a year?
#  C. nothing: the drift of each of the eight steady photometers from six months a year against all months.
import glob, os, pickle, importlib.util
import numpy as np
from multiprocessing import Pool
spec = importlib.util.spec_from_file_location('twilight', '/home/agent1/night/src/twilight.py'); TW = importlib.util.module_from_spec(spec); spec.loader.exec_module(TW)
spec = importlib.util.spec_from_file_location('tw16', '/home/agent1/night/src/twilight16.py'); T16 = importlib.util.module_from_spec(spec); spec.loader.exec_module(T16)
Y2020 = (TW.dt.datetime(2020, 1, 1) - TW.T2000).total_seconds(); YEAR = 365.25 * 86400
def files(st):
    out = []
    for d in sorted(glob.glob('/home/agent1/night/data/ida*')):
        if d.endswith('p'): continue
        for fn in sorted(glob.glob(d + f'/{st}_????-??.dat')): b = os.path.basename(fn); out.append((int(b.split('_')[1][:4]), int(b[-6:-4]), fn))
    return out
def job(a):
    st, y, m, fn, kind, amount = a
    if kind == 'step': loss = (lambda T: np.full(len(T), amount)) if y == 2024 else None
    elif kind == 'drift': loss = lambda T: amount * np.maximum(T - Y2020, 0) / YEAR
    else: loss = None
    r = TW.reduce(fn, loss=loss)
    if r is not None and r.get('pos') is None: r = TW.reduce(fn, *T16.HOME[st], loss=loss)
    return (st, y, m, kind, amount), r
def series(R, st, kind, amount, months=None):
    V = {}; sl = []
    for (s, y, m, k, a), r in R.items():
        if s != st or k != kind or a != amount or r is None or (months and m not in months): continue
        mv = TW.month_value(r)
        if mv: V[(y, m)] = mv[0]; sl += r['sl']
    return V, abs(float(np.median(sl)))
if __name__ == '__main__':
    base = pickle.load(open('/home/agent1/night/cache2/twilight16.pkl', 'rb'))
    jobs = []
    for st in ('stars289', 'stars36', 'stars52', 'stars24', 'stars1'):
        for y, m, fn in files(st):
            if y == 2024:
                for amt in (0.3, 0.6): jobs.append((st, y, m, fn, 'step', amt))
    for st in ('stars36', 'stars52', 'stars24'):
        for y, m, fn in files(st): jobs.append((st, y, m, fn, 'drift', 0.08))
    with Pool(10) as p: R = dict(p.map(job, jobs, chunksize=4))
    def basev(st, months=None):
        V = {}; sl = []
        for (s, y, m), r in base.items():
            if s != st or r is None or (months and m not in months): continue
            mv = TW.month_value(r)
            if mv: V[(y, m)] = mv[0]; sl += r['sl']
        return V, abs(float(np.median(sl)))
    print('A. a step planted in 2024: the twilight\'s figure for 2024, in magnitudes, less what it was before the planting')
    for st in ('stars289', 'stars36', 'stars52', 'stars24', 'stars1'):
        V0, s0 = basev(st); row = f'   {T16.NAME[st]:<20}'
        for amt in (0.3, 0.6):
            V1, s1 = series(R, st, 'step', amt); d = [s0 * (V1[k] - V0[k]) for k in V1 if k in V0]
            row += f'planted {amt}: found {np.mean(d):.2f} (over {len(d)} months, {min(d):.2f} to {max(d):.2f})   '
        print(row)
    print('B. a drift of 0.08 magnitude a year planted from 2020 on in three steady photometers')
    SIX = (1, 3, 5, 7, 9, 11)
    for st in ('stars36', 'stars52', 'stars24'):
        V0, s0 = basev(st); V1, s1 = series(R, st, 'drift', 0.08); W0 = {k: v for k, v in V0.items() if k[0] >= 2020}; W1 = {k: v for k, v in V1.items() if k[0] >= 2020}
        a0 = TW.drift(W0, s0); a1 = TW.drift(W1, s0); b0 = TW.drift({k: v for k, v in W0.items() if k[1] in SIX}, s0); b1 = TW.drift({k: v for k, v in W1.items() if k[1] in SIX}, s0)
        print(f'   {T16.NAME[st]:<20}from 2020, all months: before {a0[0]:+.3f}, after {a1[0]:+.3f} (added {a1[0] - a0[0]:+.3f}); six months a year: before {b0[0]:+.3f}, after {b1[0]:+.3f} (added {b1[0] - b0[0]:+.3f})')
    print('C. six months a year (January, March, May, July, September, November) against all months, every photometer, as it is')
    for st in T16.HOME:
        V0, s0 = basev(st); a = TW.drift(V0, s0); b = TW.drift({k: v for k, v in V0.items() if k[1] in SIX}, s0)
        print(f'   {T16.NAME[st]:<20}all months {a[0]:+.3f} ({a[1]:.3f}); six months {b[0]:+.3f} ({b[1]:.3f}); difference {b[0] - a[0]:+.3f}')
