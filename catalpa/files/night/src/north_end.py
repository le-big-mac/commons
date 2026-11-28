# The twenty-first sheet scored: had the darker twilight of late 2019 gone by the spring of 2020 at the photometers
# of the nineteenth sheet, which were tested unseen? Their files in data/tw5 (src/north_fetch.py and, for March to
# May 2020, src/north_fetch2.py), reduced by the nineteenth sheet's own function (src/north_new.py's job): the
# reading with the Sun 3 degrees down, evenings and mornings apart, the middle of each over a month, five or more
# of each, the two averaged. A place's figure for a stretch is the mean over the months both years give (two or
# more of the three). A place is used in a comparison only if every month used carries one chip.
# Left out by the sheet, before any spring of 2020 was fetched: Vienna (stars65: its own jump in May 2019), the
# three places north of 60 degrees (stars34, stars86, stars91: not fit for the spring), and, in comparisons with
# 2018 only, the photometer that was moved before the spring of 2019 (stars64). Positive: the later year darker.
# With --inhand only the months fetched for the nineteenth sheet are read.
import os, sys, glob, pickle, importlib.util
from multiprocessing import Pool
import numpy as np
B = '/home/agent1/night/'
def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
NN = mod('north_new', B + 'src/north_new.py')
def job(a): return NN.job(a)
OUT = ('stars65', 'stars34', 'stars86', 'stars91'); MOVED = ('stars64',); SPR, AUT = (3, 4, 5), (9, 10, 11); INHAND = '--inhand' in sys.argv
if __name__ == '__main__':
    sts = [st for st in NN.NF.chosen() if st not in OUT]
    jobs = [(st, int(os.path.basename(fn).split('_')[1][:4]), int(fn[-6:-4]), fn) for st in sts for fn in sorted(glob.glob(B + f'data/tw5/{st}_20??-??.dat')) if not (INHAND and '_2020-0' in fn)]
    with Pool(8) as p: R = dict(p.map(job, jobs, chunksize=2))
    if not INHAND: pickle.dump(R, open(B + 'cache2/north_end.pkl', 'wb'))
    def diff(st, y1, m1, y0, m0):
        ms = [m for m in m1 if R.get((st, y1, m)) and R.get((st, y0, m)) and R[(st, y1, m)]['d3'] is not None and R[(st, y0, m)]['d3'] is not None]
        if len(ms) < 2 or len({R[(st, y, m)]['mac'] for m in ms for y in (y1, y0)}) != 1: return None
        return float(np.mean([R[(st, y1, m)]['d3'] - R[(st, y0, m)]['d3'] for m in ms]))
    f = lambda v: '     . ' if v is None else f'{v:+7.3f}'
    def middle(v): v = [x for x in v if x is not None]; return (float(np.median(v)), len(v)) if v else (None, 0)
    g = lambda t: 'none' if t[0] is None else f'{t[0]:+.3f} ({t[1]})'
    print(f'{len(sts)} photometers; {len(jobs)} files; magnitudes at 3 degrees; positive: the later year reads darker; . no figure')
    print('   place      latitude | autumn 2019 less autumn 2018 | spring 2019 less spring 2018 | spring 2020 less spring 2018 | spring 2020 less spring 2019 | autumn 2019 less 2018, less spring 2020 less 2018')
    rows = {}
    for st in sts:
        a = diff(st, 2019, AUT, 2018, AUT); b = None if st in MOVED else diff(st, 2019, SPR, 2018, SPR)
        c = None if (st in MOVED or INHAND) else diff(st, 2020, SPR, 2018, SPR); d = None if INHAND else diff(st, 2020, SPR, 2019, SPR)
        rows[st] = (a, b, c, d, (a - c) if a is not None and c is not None else None)
        if any(x is not None for x in rows[st]): print(f'   {st:<9} {NN.POS[st][0]:+7.1f}  | ' + ' | '.join(f(x) for x in rows[st]))
    if INHAND: print('for the record, in hand before the sheet: spring 2019 less spring 2018, the middle ' + g(middle([rows[s][1] for s in sts]))); sys.exit(0)
    e1 = middle([rows[s][2] for s in sts]); e2 = middle([rows[s][4] for s in sts]); e3 = middle([rows[s][3] for s in sts])
    print('\nThe lines of the twenty-first sheet (unrounded figures; marks included)')
    print(f"E1. spring 2020 less spring 2018, the middle over the places (four or more), at +0.12 or below: {g(e1)}: {'void' if e1[1] < 4 else ('held' if e1[0] <= 0.12 else 'failed')}")
    print(f"E2. autumn 2019 less autumn 2018, less that figure, place by place: the middle (four or more) at +0.15 or above: {g(e2)}: {'void' if e2[1] < 4 else ('held' if e2[0] >= 0.15 else 'failed')}")
    print(f"E3. spring 2020 less spring 2019, the middle over the places (five or more), at +0.10 or below: {g(e3)}: {'void' if e3[1] < 5 else ('held' if e3[0] <= 0.10 else 'failed')}")
    print('\nfor the record, not lines:')
    print('   month by month, 2020 less 2019, the middle over the places (their number): ' + '; '.join(f"{nm} {g(middle([R[(s, 2020, m)]['d3'] - R[(s, 2019, m)]['d3'] for s in sts if R.get((s, 2020, m)) and R.get((s, 2019, m)) and R[(s, 2020, m)]['d3'] is not None and R[(s, 2019, m)]['d3'] is not None and R[(s, 2020, m)]['mac'] == R[(s, 2019, m)]['mac']]))}" for nm, m in (('March', 3), ('April', 4), ('May', 5))))
    print('   the three places north of 60 degrees, left out of the lines: ' + '; '.join(f"{st} ({NN.POS[st][0]:+.1f})" for st in ('stars34', 'stars86', 'stars91')) + ': not reduced here')
