# The fifteenth sheet scored: the fading of the twilight from 3 to 7 degrees (a month's reading with the Sun 7 degrees
# down less its reading with the Sun 3 degrees down) at every photometer of the first make, north and south, in every
# year from 2016 to 2026 that its files hold, each month less the same month of 2021.
# The reduction is that of the ninth sheet (src/depth.py: job and monthfig, unchanged). Years 2021 to 2024 come from
# the reductions of that sheet (cache2/depth.pkl); the other years are reduced here from data/ida2016 ... ida2020,
# ida2025, ida2026 (on this machine since the dawn page, never reduced at these depths) and data/tw4 (fetched for
# this sheet by src/years_fetch.py). One unit per place: the chip that gives most of its months in 2021; months from
# another chip are left out.
import os, re, sys, glob, pickle, importlib.util
from multiprocessing import Pool
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('depth', B + 'src/depth.py'); DP = importlib.util.module_from_spec(spec); spec.loader.exec_module(DP)
MORE = ('data/ida2016', 'data/ida2017', 'data/ida2018', 'data/ida2019', 'data/ida2020', 'data/ida2025', 'data/ida2026', 'data/tw4') + DP.DIRS
DEPTHS = (3.0, 5.0, 7.0, 8.0); YEARS = tuple(range(2016, 2027)); CACHE = B + 'cache2/years.pkl'
def job(a): return DP.job(a)        # a function handed to the pool must live in this file
def reduce_more():
    jobs = []
    for st in list(DP.SOUTH) + DP.NORTH:
        seen = set()
        for d in MORE:
            for fn in sorted(glob.glob(B + f'{d}/{st}_20??-??.dat')):
                b = os.path.basename(fn); y = int(b.split('_')[1][:4])
                if b in seen or 2021 <= y <= 2024 or y not in YEARS: continue
                seen.add(b); jobs.append((st, y, int(b[-6:-4]), fn, DEPTHS))
    with Pool(12) as p: R = dict(p.map(job, jobs, chunksize=4))
    pickle.dump(R, open(CACHE, 'wb')); print(f'{len(jobs)} files of the other years reduced', file=sys.stderr); return R
if __name__ == '__main__':
    R = dict(pickle.load(open(B + 'cache2/depth.pkl', 'rb')))
    if '--dry' not in sys.argv: R.update(pickle.load(open(CACHE, 'rb')) if os.path.exists(CACHE) and '--again' not in sys.argv else reduce_more())      # --dry: the years already reduced only (2021 to 2024), to try the program before the sheet is sealed
    def fading(st, dp):
        chips = {}
        for (s, y, m), r in R.items():
            if s == st and y == 2021 and r is not None and DP.monthfig(r, dp) is not None and DP.monthfig(r, 3.0) is not None: chips[(r.get('mac') or '')[-8:]] = chips.get((r.get('mac') or '')[-8:], 0) + 1
        if not chips: return {}
        ch = max(chips, key=chips.get); F = {}
        for (s, y, m), r in R.items():
            if s != st or r is None or (r.get('mac') or '')[-8:] != ch: continue
            a, b = DP.monthfig(r, dp), DP.monthfig(r, 3.0)
            if a is not None and b is not None: F[(y, m)] = a - b
        return F
    ALLM = tuple(range(1, 13)); NORTH = DP.NORTH; SOUTH = list(DP.SOUTH)
    for dp in (7.0, 8.0):
        FF = {st: fading(st, dp) for st in SOUTH + NORTH}
        def D(st, y, months=ALLM):          # the mean over the months of a stretch of the month's fading less that of the same month of 2021
            d = [FF[st][(y, m)] - FF[st][(2021, m)] for m in months if (y, m) in FF[st] and (2021, m) in FF[st]]
            return float(np.mean(d)) if len(d) >= max(2, (len(months) + 1) // 2) else None
        def M(sts, y, months=ALLM):
            v = [D(st, y, months) for st in sts]; v = [x for x in v if x is not None]; return (float(np.median(v)), len(v)) if v else (None, 0)
        f = lambda v: '  .  ' if v is None else f'{v:+.2f}'; g = lambda t: 'none' if t[0] is None else f'{t[0]:+.3f} ({t[1]})'
        print(f'THE FADING FROM 3 TO {dp:g} DEGREES, each year less 2021 (the mean over the months both years have, half of them or more; negative: brighter at depth than in 2021; . no figure)')
        for name, sts in (('south', SOUTH), ('north', NORTH)):
            print(f'  {name}' + ' ' * 14 + ''.join(f'{y:>7d}' for y in YEARS if y != 2021))
            for st in sts: print(f"   {DP.SOUTH.get(st, st):<15}" + ''.join(f'{f(D(st, y)):>7}' for y in YEARS if y != 2021))
            print(f"   {'the middle':<15}" + ''.join(f'{f(M(sts, y)[0]):>7}' for y in YEARS if y != 2021)); print(f"   {'places':<15}" + ''.join(f'{M(sts, y)[1]:>7d}' for y in YEARS if y != 2021))
        print('  month by month, the middle over places (three or more) of the month less the same month of 2021, hundredths:')
        for name, sts in (('south', SOUTH), ('north', NORTH)):
            for y in YEARS:
                if y == 2021: continue
                v = [[FF[st][(y, m)] - FF[st][(2021, m)] for st in sts if (y, m) in FF[st] and (2021, m) in FF[st]] for m in ALLM]
                if any(len(x) >= 3 for x in v): print(f'   {name} {y}: ' + ' '.join(f'{100 * np.median(x):+4.0f}' if len(x) >= 3 else '   .' for x in v) + '   | places: ' + ' '.join(f'{len(x):2d}' for x in v))
        if dp != 7.0: continue
        print('\nThe lines of the fifteenth sheet (the fading from 3 to 7 degrees; unrounded figures; marks included)')
        def within(t, w): return t[0] is not None and abs(t[0]) <= w
        a, b = M(NORTH, 2018), M(NORTH, 2019, (1, 2, 3, 4, 5, 6)); ok = a[1] >= 4 and b[1] >= 4
        print(f"N1. north, quiet years: the middle of 2018 and of January to June 2019 both within 0.05 of nothing: {g(a)}, {g(b)}: {'void' if not ok else ('held' if within(a, 0.05) and within(b, 0.05) else 'failed')}")
        late = (8, 9, 10, 11, 12); v = [D(st, 2019, late) - D(st, 2018, late) for st in NORTH if D(st, 2019, late) is not None and D(st, 2018, late) is not None]
        print(f"N2. north, after Raikoke: August to December 2019 less August to December 2018, the middle over the places with both, at -0.03 or below: {('none' if not v else f'{np.median(v):+.3f} ({len(v)})')}: {'void' if len(v) < 4 else ('held' if np.median(v) <= -0.03 else 'failed')}")
        c = M(NORTH, 2025); print(f"N3. north, 2025: the middle at -0.04 or below: {g(c)}: {'void' if c[1] < 4 else ('held' if c[0] <= -0.04 else 'failed')}")
        d = M(NORTH, 2026); print(f"N4. north, 2026: the middle at -0.04 or below: {g(d)}: {'void' if d[1] < 4 else ('held' if d[0] <= -0.04 else 'failed')}")
        q = M(SOUTH, 2019, (1, 2, 3, 4, 5, 6)); print(f"S1. south, January to June 2019, before the smoke and before Ulawun: the middle within 0.05 of nothing: {g(q)}: {'void' if q[1] < 2 else ('held' if within(q, 0.05) else 'failed')}")
        h = M(SOUTH, 2019, (7, 8, 9, 10, 11, 12)); print(f"S2. south, July to December 2019: the middle within 0.06 of nothing: {g(h)}: {'void' if h[1] < 3 else ('held' if within(h, 0.06) else 'failed')}")
        e = M(SOUTH, 2020); print(f"S3. south, the year of the smoke, 2020: the middle at +0.05 or above (darker at depth than 2021): {g(e)}: {'void' if e[1] < 3 else ('held' if e[0] >= 0.05 else 'failed')}   [at -0.05 or below: {'yes' if e[0] is not None and e[0] <= -0.05 else 'no'}]")
        k = M(SOUTH, 2025); print(f"S4. south, 2025: the middle at -0.04 or below: {g(k)}: {'void' if k[1] < 3 else ('held' if k[0] <= -0.04 else 'failed')}")
        k6 = M(SOUTH, 2026); print(f"S5. south, 2026: the middle at -0.04 or below: {g(k6)}: {'void' if k6[1] < 3 else ('held' if k6[0] <= -0.04 else 'failed')}")
        print()
