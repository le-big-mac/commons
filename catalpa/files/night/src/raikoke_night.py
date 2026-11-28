# After the sixteenth sheet, at the checker's asking (check/check-twilight-13.md): my own reduction of two things
# it found. (1) Did the first make's units change? Their moonless-night readings (the ninth sheet's reduction keeps
# each night's reading; cache2/years.pkl, cache2/depth.pkl), late 2019 less late 2018, place by place.
# (2) The twilight's change by the Sun's depth from 3 to 11 degrees, the same months. For the depths not yet
# reduced for 2018 to 2020 (9, 10, 11) the files are reduced here by the ninth sheet's function. Not a test.
import os, sys, glob, pickle, importlib.util
from multiprocessing import Pool
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('depth', B + 'src/depth.py'); DP = importlib.util.module_from_spec(spec); spec.loader.exec_module(DP)
def job(a): return DP.job(a)
CACHE = B + 'cache2/raikoke_deep.pkl'; DEEP = (4.0, 6.0, 9.0, 10.0, 11.0)
if __name__ == '__main__':
    R = dict(pickle.load(open(B + 'cache2/years.pkl', 'rb')))
    if os.path.exists(CACHE): R2 = pickle.load(open(CACHE, 'rb'))
    else:
        jobs = []
        for st in DP.NORTH:
            for d in ('data/ida2018', 'data/ida2019', 'data/ida2020'):
                for fn in sorted(glob.glob(B + f'{d}/{st}_20??-??.dat')):
                    b = os.path.basename(fn); jobs.append((st, int(b.split('_')[1][:4]), int(b[-6:-4]), fn, DEEP))
        with Pool(12) as p: R2 = dict(p.map(job, jobs, chunksize=4))
        pickle.dump(R2, open(CACHE, 'wb'))
    def fig(st, y, m, dp):
        r = (R2 if dp in DEEP else R).get((st, y, m)); return None if r is None else DP.monthfig(r, dp)
    def night(st, y, m, q=50):
        r = R.get((st, y, m)); v = None if r is None else r.get('night'); return float(np.percentile(v, q)) if v and len(v) >= 5 else None
    LATE = (8, 9, 10, 11, 12); AUT = (9, 10, 11); f = lambda v: '    . ' if v is None else f'{v:+6.2f}'
    def diff(get, st, months, *a):
        d = [get(st, 2019, m, *a) - get(st, 2018, m, *a) for m in months if get(st, 2019, m, *a) is not None and get(st, 2018, m, *a) is not None]; return float(np.mean(d)) if len(d) >= 2 else None
    print('late 2019 less late 2018 at each northern place of the first make that has both (magnitudes; positive: darker)')
    print('   place       the twilight, September to November, by the depth of the Sun:   3      4      5      6      7      8      9     10     11   | the moonless night, August to December: its middle, and its darkest quarter')
    rows = {}
    for st in DP.NORTH:
        tw = [diff(fig, st, AUT, dp) for dp in (3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0)]; nn = [diff(night, st, LATE, 50), diff(night, st, LATE, 75)]
        if any(x is not None for x in tw): rows[st] = (tw, nn); print(f'   {st:<10}' + ' ' * 59 + ' '.join(f(x) for x in tw) + '   | ' + ' '.join(f(x) for x in nn))
    def mid(i, j=None):
        v = [(rows[s][0][i] if j is None else rows[s][1][j]) for s in rows]; v = [x for x in v if x is not None]; return f'{np.median(v):+.2f} ({len(v)})' if v else 'none'
    print('   the middle over the places: the twilight ' + ', '.join(mid(i) for i in range(9)) + '; the night ' + ', '.join(mid(0, j) for j in range(2)))
    print('   the middle with the two odd units (stars4, stars426) left out: the twilight ' + ', '.join((lambda v: f'{np.median(v):+.2f} ({len(v)})')([rows[s][0][i] for s in rows if s not in ('stars4', 'stars426') and rows[s][0][i] is not None]) for i in range(9)) + '; the night ' + ', '.join((lambda v: f'{np.median(v):+.2f} ({len(v)})')([rows[s][1][j] for s in rows if s not in ('stars4', 'stars426') and rows[s][1][j] is not None]) for j in range(2)))
