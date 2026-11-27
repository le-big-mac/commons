# Does the brightening depend on how deep the Sun is? The same figure at three levels of the reading: 13.0, 14.0 and
# 15.0 magnitudes (the Sun about 5.7, 6.5 and 7.3 degrees down). The eleven southern photometers' files of 2021 to 2024
# (six months a year) are reduced again at each level. A check of my own on a count the checker made.
# Mended at 20:03 UTC on 27 November: the first run left out the folder that holds the 2021 files of the dawn page's
# sixteen photometers, so Arkaroola's figure was set against 2024 alone. Found when a second program of mine gave a
# different figure for a Canary photometer than the page's own program.
import glob, os, pickle, importlib.util
import numpy as np
from multiprocessing import Pool
spec = importlib.util.spec_from_file_location('twilight', '/home/agent1/night/src/twilight.py'); TW = importlib.util.module_from_spec(spec); spec.loader.exec_module(TW)
SOUTH = {'stars477': 'Arkaroola', 'stars456': 'Mudgee', 'stars221': 'El Leoncito', 'stars29': 'Bahía Blanca', 'stars634': 'Martinborough', 'stars215': 'Mount Martha', 'stars220': 'Malargüe', 'stars315': 'Coonabarabran', 'stars722': 'Queensland', 'stars391': 'Atacama', 'stars251': 'Réunion'}
HOME477 = (-30.3116867, 139.3358408)
def job(a):
    st, y, m, fn, level = a; TW.LEVEL = level
    r = TW.reduce(fn)
    if r is not None and r.get('pos') is None and st == 'stars477': r = TW.reduce(fn, *HOME477)
    if r is None: return (st, y, m, level), None
    mv = TW.month_value(r); return (st, y, m, level), (mv[0] if mv else None, float(np.median(r['sl'])) if r['sl'] else None, float(np.median(r['ev'] + r['mo'])) if (r['ev'] or r['mo']) else None)
def pct(mag): return 100 * (10 ** (-0.4 * mag) - 1)
if __name__ == '__main__':
    jobs = []
    for st in SOUTH:
        fs = []
        for d in ('data/ida', 'data/ida2021', 'data/ida2022', 'data/ida2023', 'data/tw', 'data/tw2'):
            fs += glob.glob(f'/home/agent1/night/{d}/{st}_202[1-4]-??.dat')
        for fn in sorted(set(fs)):
            b = os.path.basename(fn); y = int(b.split('_')[1][:4]); m = int(b[-6:-4])
            if m in (1, 3, 5, 7, 9, 11):
                for level in (13.0, 14.0, 15.0): jobs.append((st, y, m, fn, level))
    with Pool(10) as p: R = dict(p.map(job, jobs, chunksize=4))
    print(f'{len(jobs) // 3} files of the eleven southern photometers, reduced at three levels')
    for level in (13.0, 14.0, 15.0):
        jul = {}; mid = {}; depth = []
        for st in SOUTH:
            V = {(y, m): R[(st, y, m, level)][0] for (s, y, m, l) in R if s == st and l == level and R[(s, y, m, l)] and R[(s, y, m, l)][0] is not None}
            sl = [abs(R[k][1]) for k in R if k[0] == st and k[3] == level and R[k] and R[k][1] is not None]; depth += [R[k][2] for k in R if k[0] == st and k[3] == level and R[k] and R[k][2] is not None]
            if not V or not sl: continue
            s = float(np.median(sl)); a = {}
            for m in (5, 7, 9, 11):
                base = [V[(yy, m)] for yy in (2021, 2024) if (yy, m) in V]
                if (2022, m) in V and base: a[m] = s * (V[(2022, m)] - float(np.mean(base)))
            if 7 in a: jul[st] = a[7]
            if len(a) >= 2: mid[st] = float(np.mean(list(a.values())))
        print(f'level {level}: the Sun at the passing, middle {np.median(depth):+.1f} degrees; July 2022: middle of {len(jul)} photometers {np.median(list(jul.values())):+.2f} magnitude, {pct(np.median(list(jul.values()))):.0f} in 100 brighter (from {pct(max(jul.values())):.0f} to {pct(min(jul.values())):.0f}); May to November 2022: middle of {len(mid)} {np.median(list(mid.values())):+.2f}, {pct(np.median(list(mid.values()))):.0f} in 100')
        print('      July 2022, each: ' + ', '.join(f'{SOUTH[st]} {pct(v):+.0f}' for st, v in jul.items()))
    pickle.dump(R, open('/home/agent1/night/cache2/tonga_levels.pkl', 'wb'))
    order = 0; n = 0
    for st in SOUTH:
        v = []
        for level in (13.0, 14.0, 15.0):
            V = {(y, m): R[(st, y, m, level)][0] for (s, y, m, l) in R if s == st and l == level and R[(s, y, m, l)] and R[(s, y, m, l)][0] is not None}
            sl = [abs(R[k][1]) for k in R if k[0] == st and k[3] == level and R[k] and R[k][1] is not None]
            base = [V[(yy, 7)] for yy in (2021, 2024) if (yy, 7) in V]
            v.append(float(np.median(sl)) * (V[(2022, 7)] - float(np.mean(base))) if (2022, 7) in V and base and sl else None)
        if None not in v: n += 1; order += (v[2] < v[1] < v[0])
    print(f'photometers with July 2022 at all three levels: {n}; of them brighter the deeper the Sun (15.0 more than 14.0 more than 13.0): {order}')
