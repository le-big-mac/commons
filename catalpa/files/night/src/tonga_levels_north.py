# The page says: "a meter that had changed would show the same change at every depth". Three things to try that on.
#  A. A change made up: at three steady northern photometers every reading of 2022 is made 0.3 magnitude brighter;
#     what does the figure say at the levels 13.0, 14.0 and 15.0?
#  B. The northern photometers through the same three levels (the files of 2021 to 2024, six months a year), and in
#     particular the few that stand furthest from no change at 14.0 (tonga_north.out).
#  C. How many northern photometers show the southern order (15.0 brighter than 14.0 brighter than 13.0) with any size.
import glob, os, pickle, importlib.util, io, contextlib
import numpy as np
from multiprocessing import Pool
spec = importlib.util.spec_from_file_location('twilight', '/home/agent1/night/src/twilight.py'); TW = importlib.util.module_from_spec(spec); spec.loader.exec_module(TW)
spec = importlib.util.spec_from_file_location('tw16', '/home/agent1/night/src/twilight16.py'); T16 = importlib.util.module_from_spec(spec); spec.loader.exec_module(T16)
LEVELS = (13.0, 14.0, 15.0); PLANT = ('stars602', 'stars489', 'stars246')
def job(a):
    st, y, m, fn, level, plant = a; TW.LEVEL = level
    loss = (lambda T: np.full(len(T), -0.3)) if (plant and y == 2022) else None
    r = TW.reduce(fn, loss=loss)
    if r is not None and r.get('pos') is None and st in T16.HOME: r = TW.reduce(fn, *T16.HOME[st], loss=loss)
    if r is None: return (st, y, m, level, plant), None
    mv = TW.month_value(r)
    return (st, y, m, level, plant), (mv[0] if mv else None, mv[1] if mv else None, mv[2] if mv else None, float(np.median(r['sl'])) if r['sl'] else None, r.get('mac'))
def pct(mag): return 100 * (10 ** (-0.4 * mag) - 1)
def figure(R, st, level, plant=False, months=(5, 7, 9, 11), which=0):
    rows = {(y, m): R[(s, y, m, l, p)] for (s, y, m, l, p) in R if s == st and l == level and p == plant and R[(s, y, m, l, p)] and R[(s, y, m, l, p)][which] is not None}
    if not rows: return None, {}
    chips = {}
    for k, v in rows.items(): chips.setdefault((v[4] or '')[-8:], []).append(k)
    keep = max(chips.values(), key=len); V = {k: rows[k][which] for k in keep}; sl = [abs(rows[k][3]) for k in keep if rows[k][3] is not None]
    if not sl: return None, {}
    s = float(np.median(sl)); a = {}
    for m in months:
        base = [V[(yy, m)] for yy in (2021, 2024) if (yy, m) in V]
        if (2022, m) in V and base: a[m] = s * (V[(2022, m)] - float(np.mean(base)))
    return (float(np.mean(list(a.values()))) if len(a) >= 2 else None), a
if __name__ == '__main__':
    with contextlib.redirect_stdout(io.StringIO()):
        spec = importlib.util.spec_from_file_location('tonga_page', '/home/agent1/night/src/tonga_page.py'); TP = importlib.util.module_from_spec(spec); spec.loader.exec_module(TP)
    NORTH = TP.north + TP.canary; lat = {st: TP.S[st]['lat'] for st in NORTH}
    jobs = []
    for st in NORTH:
        fs = []
        for d in ('data/ida', 'data/ida2021', 'data/ida2022', 'data/ida2023', 'data/tw', 'data/tw2'): fs += glob.glob(f'/home/agent1/night/{d}/{st}_202[1-4]-??.dat')
        seen = set()
        for fn in sorted(fs):
            b = os.path.basename(fn)
            if b in seen: continue
            seen.add(b); y = int(b.split('_')[1][:4]); m = int(b[-6:-4])
            if m in (1, 3, 5, 7, 9, 11):
                for level in LEVELS:
                    jobs.append((st, y, m, fn, level, False))
                    if st in PLANT: jobs.append((st, y, m, fn, level, True))
    with Pool(10) as p: R = dict(p.map(job, jobs, chunksize=4))
    pickle.dump(R, open('/home/agent1/night/cache2/tonga_levels_north.pkl', 'wb'))
    print(f'{len(NORTH)} photometers north of the equator; {len(jobs)} reductions')
    print('\nA. a change made up: every reading of 2022 made 0.3 magnitude brighter; the figure for May to November 2022 less what it was before the planting')
    for st in PLANT:
        row = f'   {st:<9}'
        for level in LEVELS:
            f1, _ = figure(R, st, level, True); f0, _ = figure(R, st, level, False)
            row += f'  at {level}: {f1 - f0:+.2f}' if f1 is not None and f0 is not None else f'  at {level}: -'
        print(row)
    print('\nB. each northern photometer, May to November 2022 against the same months of 2021 and 2024, at the three levels (magnitudes; negative: brighter), from the brightest at 14.0')
    F = {st: [figure(R, st, level)[0] for level in LEVELS] for st in NORTH}
    for st in sorted((s for s in NORTH if F[s][1] is not None), key=lambda s: F[s][1]):
        v = F[st]; mark = ''
        if None not in v: mark = 'the southern order' if v[2] < v[1] < v[0] else ('the other order' if v[2] > v[1] > v[0] else '')
        print(f"   {st:<9} {lat[st]:+6.1f}   " + '  '.join(f'{x:+.2f}' if x is not None else '   . ' for x in v) + f'   {mark}')
    full = [st for st in NORTH if None not in F[st]]
    print(f'\nC. with the figure at all three levels: {len(full)}; in the southern order (15.0 brighter than 14.0 brighter than 13.0): {sum(1 for s in full if F[s][2] < F[s][1] < F[s][0])}; in that order and brighter by 0.10 or more at 14.0: {sum(1 for s in full if F[s][2] < F[s][1] < F[s][0] and F[s][1] <= -0.10)} ({", ".join(s for s in full if F[s][2] < F[s][1] < F[s][0] and F[s][1] <= -0.10)})')
    print('   the middle of them at 13.0, 14.0, 15.0: ' + ', '.join(f'{np.median([F[s][i] for s in full]):+.3f}' for i in range(3)))
    print('\nD. the ones furthest from no change, month by month of 2022 at the three levels (hundredths of a magnitude), and evening and morning apart at 14.0')
    for st in ('stars8', 'stars4', 'stars71', 'stars33', 'stars225'):
        if st not in NORTH: continue
        for level in LEVELS:
            _, a = figure(R, st, level); print(f"   {st:<9} at {level}: " + ' '.join(f"{m:02d} {100 * a[m]:+4.0f}" if m in a else f'{m:02d}    .' for m in (5, 7, 9, 11)))
        e, _ = figure(R, st, 14.0, which=1); mo, _ = figure(R, st, 14.0, which=2)
        print(f"   {st:<9} evening {e if e is None else round(e, 2)}, morning {mo if mo is None else round(mo, 2)}")
