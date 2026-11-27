# The twilight measure (twilight.py) on the sixteen photometers of the dawn page, every monthly file of 2016 to 2026
# that is on disk. A reproduction with my own code of what the checker found after the fact; nothing here is sealed.
# Writes cache2/twilight16.pkl and prints the table.
import os, glob, pickle, importlib.util, datetime as dt
import numpy as np
from multiprocessing import Pool
spec = importlib.util.spec_from_file_location('twilight', '/home/agent1/night/src/twilight.py'); TW = importlib.util.module_from_spec(spec); spec.loader.exec_module(TW)
HOME = {'stars1': (40.4246043, -3.560279), 'stars4': (28.6865, -17.7665), 'stars7': (42.81732, -1.64543), 'stars9': (38.409226, -4.894376),
        'stars19': (32.223877, -110.767532), 'stars24': (27.90083333, -15.51472222), 'stars33': (40.4478574, -3.6637624), 'stars35': (45.93, 13.91),
        'stars36': (42.3177194, -72.4757444), 'stars52': (36.8787604, -2.4418338), 'stars62': (42.02459, 0.734797), 'stars76': (39.478898, -0.376524),
        'stars225': (41.474, -1.4821), 'stars289': (38.1657813, -2.3268926), 'stars426': (28.29871203, -16.50948217), 'stars477': (-30.3116867, 139.3358408)}
NAME = {'stars33': "Madrid ring road", 'stars76': "Valencia", 'stars1': "Coslada", 'stars52': "Almería", 'stars7': "Pamplona", 'stars36': "Northampton, USA", 'stars4': "La Palma, a town", 'stars19': "Tucson, USA",
        'stars9': "Añora", 'stars225': "Morata de Jalón", 'stars24': "Temisas", 'stars426': "Teide Observatory", 'stars62': "Àger", 'stars35': "Otlica", 'stars477': "Arkaroola", 'stars289': "Nerpio"}
def job(a):
    st, y, m, fn = a
    r = TW.reduce(fn)
    if r is not None and r.get('pos') is None: r = TW.reduce(fn, *HOME[st])
    return (st, y, m), r
if __name__ == '__main__':
    # the vector Sun against sky.py's
    rng = np.random.default_rng(1); worst = 0.0
    for _ in range(300):
        t = dt.datetime(2016, 1, 1) + dt.timedelta(seconds=float(rng.uniform(0, 11 * 365.25 * 86400))); la = float(rng.uniform(-45, 50)); lo = float(rng.uniform(-180, 180))
        worst = max(worst, abs(float(TW.sun_alt_vec([(t - TW.T2000).total_seconds()], la, lo)[0]) - TW.sky.sun_alt(t, la, lo)))
    print(f'the array form of the Sun against sky.py, 300 random moments and places: worst difference {worst:.6f} degree')
    jobs = []
    for d in sorted(glob.glob('/home/agent1/night/data/ida*')):
        if d.endswith('p'): continue
        for fn in sorted(glob.glob(d + '/stars*_????-??.dat')):
            b = os.path.basename(fn); st = b.split('_')[0]; y = int(b.split('_')[1][:4]); m = int(b[-6:-4])
            if st in HOME: jobs.append((st, y, m, fn))
    with Pool(10) as p: R = dict(p.map(job, jobs, chunksize=8))
    print(len(jobs), 'files;', sum(1 for r in R.values() if r and TW.month_value(r)), 'months with five evening and five morning crossings or more')
    order = ['stars33', 'stars76', 'stars1', 'stars52', 'stars7', 'stars36', 'stars19', 'stars9', 'stars225', 'stars4', 'stars24', 'stars426', 'stars35', 'stars477', 'stars62', 'stars289']
    print('\nplace                slope    months  years         reading darker, magnitudes a year  (plain error)   evening alone   morning alone   scatter of a month')
    for st in order:
        V = {}; E = {}; Mo = {}; sl = []
        for (s, y, m), r in R.items():
            if s != st or r is None: continue
            mv = TW.month_value(r)
            if mv: V[(y, m)] = mv[0]; E[(y, m)] = mv[1]; Mo[(y, m)] = mv[2]; sl += r['sl']
        if not V: print(f'{NAME[st]:<20} no months'); continue
        s = float(np.median(sl)); d = TW.drift(V, s); de = TW.drift(E, s); dm = TW.drift(Mo, s); ys = sorted({y for y, m in V})
        print(f'{NAME[st]:<20} {s:+5.2f}   {len(V):>5}   {ys[0]}-{ys[-1]}   ' + (f'{d[0]:+.3f}  ({d[1]:.3f})   {de[0]:+.3f}   {dm[0]:+.3f}   {d[3]:.3f}' if d else 'too few months'))
    pickle.dump(R, open('/home/agent1/night/cache2/twilight16.pkl', 'wb'))
    # the night by the same reduction, beside the frozen method's cleaned nights; and both drifts from four months a year only
    def station(st, months=None):
        V = {}; sl = []; nights = []
        for (s, y, m), r in R.items():
            if s != st or r is None or (months and m not in months): continue
            mv = TW.month_value(r)
            if mv: V[(y, m)] = mv[0]; sl += r['sl']
            nights += [(y, m) + n for n in r.get('nights', [])]
        if not V or not nights: return None
        sp = np.array([n[5] for n in nights]); floor = np.percentile(sp, 20); g = {}
        for (y, m, d, L, lev, s_) in nights:
            if s_ <= 2 * floor: g.setdefault((y, m), []).append(lev)
        NM = {k: float(np.median(v)) for k, v in g.items() if len(v) >= 2}
        return TW.drift(V, float(np.median(sl))), TW.drift(NM, 1.0), len(V), len(NM)
    print('\nplace                twilight drift, all months   night drift, all months (months)      twilight, four months a year   night, four months a year (months)')
    a_t, a_n, f_t, f_n = [], [], [], []
    for st in order:
        A = station(st); F4 = station(st, (2, 5, 8, 11))
        if not A or not A[0]: print(f'{NAME[st]:<20} -'); continue
        row = f'{NAME[st]:<20} {A[0][0]:+.3f} ({A[0][1]:.3f})                ' + (f'{A[1][0]:+.3f} ({A[1][1]:.3f}) ({A[3]})' if A[1] else '      -          ') + '             '
        row += (f'{F4[0][0]:+.3f} ({F4[0][1]:.3f})' if F4 and F4[0] else '      -      ') + '               ' + (f'{F4[1][0]:+.3f} ({F4[1][1]:.3f}) ({F4[3]})' if F4 and F4[1] else '      -')
        print(row)
        if A[1]: a_t.append(A[0][0]); a_n.append(A[1][0])
        if F4 and F4[0] and F4[1]: f_t.append(F4[0][0]); f_n.append(F4[1][0])
    for lab, t_, n_ in (('all months', a_t, a_n), ('four months a year', f_t, f_n)):
        t_ = np.array(t_); n_ = np.array(n_); print(f'{lab}: {len(t_)} places; night against twilight: correlation {np.corrcoef(t_, n_)[0, 1]:+.2f}, slope {np.polyfit(t_, n_, 1)[0]:.2f}; reading darker by 0.04 or more: {int(np.sum(t_ >= 0.04))}; steady within 0.025: {int(np.sum(np.abs(t_) < 0.025))}; brighter by 0.04 or more: {int(np.sum(t_ <= -0.04))}; middle twilight drift {np.median(t_):+.3f}')
    print('\nyear by year: the middle of the months\' figures, in hundredths of a magnitude from the place\'s own mean over all its years (positive: reading darker); months in brackets')
    for st in order:
        V = {}; sl = []
        for (s, y, m), r in R.items():
            if s != st or r is None: continue
            mv = TW.month_value(r)
            if mv: V[(y, m)] = mv[0]; sl += r['sl']
        if not V: continue
        s = abs(float(np.median(sl))); mon = {m: np.mean([v for (y, mm), v in V.items() if mm == m]) for m in range(1, 13) if any(mm == m for y, mm in V)}
        print(f'{NAME[st]:<20}' + ' '.join(f"{y}:{100 * s * np.mean([V[(yy, m)] - mon[m] for (yy, m) in V if yy == y]):+4.0f}({sum(1 for (yy, m) in V if yy == y)})" for y in sorted({y for y, m in V})))
