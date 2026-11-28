# The southern twilight by the depth of the Sun: a second measure, direct where the page's is by crossings.
#
# For each monthly file, every time the Sun passes a given depth below the horizon (DEPTHS, in degrees) between two
# readings less than 200 seconds apart, the reading there (the raw count on the fixed scale, 20.5 - 2.5 log10 of the
# frequency, as on the page) is taken by straight-line interpolation in the Sun's altitude: evenings (the Sun going
# down) and mornings apart. A month's figure at a depth is the mean of its middle evening reading and its middle
# morning reading, if it has five or more of each. A month's anomaly is its figure less the mean of the same calendar
# month of 2021 and 2024, whichever the instrument has: magnitudes, negative for a brighter twilight. An instrument is
# the chip with the most months at its station.
#   From 8 degrees down, only twilights with the Moon below the horizon at that moment are used.
#   A place gives a depth only if its middle comparison-year reading there is 2.0 magnitudes or more brighter than the
#   middle of its moonless nights (so that its own night sky is under a sixth of the light).
# The sheet's figure P is the mean of the anomalies of June, July and August 2022 (two of the three or more).
#
# usage: depth.py OUT.pkl DEPTH [DEPTH ...]     (reduces the files; several depths at once)
#        depth.py OUT.pkl                        (prints the tables from OUT.pkl)
import sys, os, re, glob, pickle, math, datetime as dt, importlib.util
import numpy as np
from multiprocessing import Pool
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('twilight', B + 'src/twilight.py'); TW = importlib.util.module_from_spec(spec); spec.loader.exec_module(TW)
spec = importlib.util.spec_from_file_location('tw16', B + 'src/twilight16.py'); T16 = importlib.util.module_from_spec(spec); spec.loader.exec_module(T16)
import csv
geo = {r['name']: r for r in csv.DictReader(open(B + 'lit/src/p3_stars4all_geolist.csv'), delimiter=';')}
SOUTH = {'stars251': 'Réunion', 'stars391': 'Atacama', 'stars722': 'Queensland', 'stars477': 'Arkaroola', 'stars315': 'Coonabarabran', 'stars221': 'El Leoncito', 'stars456': 'Mudgee', 'stars220': 'Malargüe', 'stars215': 'Mount Martha', 'stars29': 'Bahía Blanca', 'stars634': 'Martinborough'}
NORTH = ['stars246', 'stars347', 'stars47', 'stars602', 'stars489', 'stars1', 'stars19', 'stars225', 'stars24', 'stars289', 'stars33', 'stars35', 'stars36', 'stars4', 'stars426', 'stars52', 'stars62', 'stars7', 'stars76', 'stars9']
HOME = dict(T16.HOME); HOME['stars477'] = (-30.3116867, 139.3358408)
DIRS = ('data/ida', 'data/ida2021', 'data/ida2022', 'data/ida2023', 'data/tw', 'data/tw2', 'data/tw3')
def job(a):
    st, y, m, fn, depths = a
    txt = open(fn, encoding='utf-8', errors='replace').read()
    if '# END OF HEADER' not in txt: return (st, y, m), None
    head, body = txt.split('# END OF HEADER', 1)
    mp = re.search(r'# Position: ([-\d.]+), ([-\d.]+)', head); mm = re.search(r'# TESS MAC address: (\S+)', head)
    if mp: lat, lon = float(mp.group(1)), float(mp.group(2))
    elif st in HOME: lat, lon = HOME[st]
    elif st in geo and geo[st]['latitude']: lat, lon = float(geo[st]['latitude']), float(geo[st]['longitude'])
    else: return (st, y, m), None
    T, F = [], []
    for line in body.splitlines():
        p = line.split(';')
        if len(p) < 7: continue
        try: f = float(p[4]); t = dt.datetime.strptime(p[0][:19], '%Y-%m-%dT%H:%M:%S')
        except ValueError: continue
        if f > 0: T.append((t - TW.T2000).total_seconds()); F.append(f)
    out = dict(mac=mm.group(1) if mm else None, d={})
    if len(T) < 100: return (st, y, m), out
    o = np.argsort(T); T = np.array(T)[o]; M = 20.5 - 2.5 * np.log10(np.array(F)[o]); alt = TW.sun_alt_vec(T, lat, lon)
    ok = (np.diff(T) < 200) & (np.diff(T) > 0)
    for dp in depths:
        a0 = alt[:-1] + dp; a1 = alt[1:] + dp; i = np.where(ok & (a0 * a1 < 0))[0]
        ev, mo, evm, mom = [], [], [], []
        for k in i:
            fr = a0[k] / (a0[k] - a1[k]); val = float(M[k] + fr * (M[k + 1] - M[k])); tc = TW.T2000 + dt.timedelta(seconds=float(T[k] + fr * (T[k + 1] - T[k])))
            moon = TW.sky.moon_alt(tc, lat, lon) > 0
            if alt[k + 1] < alt[k]: ev.append(val); evm.append(moon)
            else: mo.append(val); mom.append(moon)
        out['d'][dp] = (ev, mo, evm, mom)
    nights = TW.reduce(fn, lat, lon)['nights'] if 6.0 in depths or 7.0 in depths or len(depths) > 2 else []
    out['night'] = [n[2] for n in nights]
    return (st, y, m), out
def reduce_all(outp, depths):
    old = pickle.load(open(outp, 'rb')) if os.path.exists(outp) else {}
    jobs = []
    for st in list(SOUTH) + NORTH:
        seen = set()
        for d in DIRS:
            for fn in sorted(glob.glob(B + f'{d}/{st}_202[1-4]-??.dat')):
                b = os.path.basename(fn)
                if b in seen: continue
                seen.add(b); jobs.append((st, int(b.split('_')[1][:4]), int(b[-6:-4]), fn, depths))
    with Pool(12) as p: R = dict(p.map(job, jobs, chunksize=4))
    for k, r in R.items():       # keep depths reduced earlier
        if r is not None and k in old and old[k] is not None:
            dd = dict(old[k]['d']); dd.update(r['d']); r['d'] = dd
            if not r.get('night'): r['night'] = old[k].get('night', [])
    pickle.dump(R, open(outp, 'wb')); print(f'{len(jobs)} files reduced at the depths {depths}', file=sys.stderr)
def monthfig(r, dp, which=None):
    if r is None or dp not in r['d']: return None
    ev, mo, evm, mom = r['d'][dp]
    if dp >= 8.0: ev = [v for v, mn in zip(ev, evm) if not mn]; mo = [v for v, mn in zip(mo, mom) if not mn]
    if which == 'ev': return float(np.median(ev)) if len(ev) >= 5 else None
    if which == 'mo': return float(np.median(mo)) if len(mo) >= 5 else None
    return 0.5 * (float(np.median(ev)) + float(np.median(mo))) if len(ev) >= 5 and len(mo) >= 5 else None
def series(R, st, dp, which=None):
    chips = {}
    for (s, y, m), r in R.items():
        if s == st and r is not None and monthfig(r, 6.0 if 6.0 in r['d'] else dp) is not None: chips.setdefault((r.get('mac') or '')[-8:], []).append((y, m))
    if not chips: return {}, None, None
    ch = max(chips, key=lambda c: len(chips[c])); V = {}; night = []
    for (s, y, m), r in R.items():
        if s != st or r is None or (r.get('mac') or '')[-8:] != ch: continue
        v = monthfig(r, dp, which); night += r.get('night', [])
        if v is not None: V[(y, m)] = v
    flank = [v for (y, m), v in V.items() if y in (2021, 2024)]; nl = float(np.median(night)) if night else None
    if not flank or (nl is not None and float(np.median(flank)) > nl - 2.0): return {}, (float(np.median(flank)) if flank else None), nl
    out = {}
    for (y, m), v in V.items():
        base = [V[(yy, m)] for yy in (2021, 2024) if (yy, m) in V]
        if base: out[(y, m)] = v - float(np.mean(base))
    return out, float(np.median(flank)), nl
def P(a):
    v = [a[(2022, m)] for m in (6, 7, 8) if (2022, m) in a]; return float(np.mean(v)) if len(v) >= 2 else None
def tables(outp):
    R = pickle.load(open(outp, 'rb')); depths = sorted({dp for r in R.values() if r is not None for dp in r['d']})
    print(f'depths in {os.path.basename(outp)}: ' + ', '.join(f'{d:g}' for d in depths) + f'; files: {len(R)}')
    PS = {}; PN = {}; lev = {}
    print('\nA. the eleven southern photometers: P (June to August 2022 less the same months of 2021 and 2024; magnitudes; negative: brighter) at each depth of the Sun; . no figure')
    print('   ' + ' ' * 16 + ''.join(f'{d:7g}°' for d in depths))
    for st, name in SOUTH.items():
        row = []
        for dp in depths:
            a, fl, nl = series(R, st, dp); p = P(a); PS[(st, dp)] = p; lev[(st, dp)] = fl; row.append(f'{p:+8.2f}' if p is not None else '       .')
        print(f'   {name:<16}' + ''.join(row))
    mid = {}
    for dp in depths:
        v = [PS[(st, dp)] for st in SOUTH if PS[(st, dp)] is not None]; mid[dp] = (float(np.median(v)), len(v)) if v else (None, 0)
    print('   the middle      ' + ''.join(f'{mid[dp][0]:+8.2f}' if mid[dp][0] is not None else '       .' for dp in depths))
    print('   places          ' + ''.join(f'{mid[dp][1]:8d}' for dp in depths))
    print('   the comparison-year reading at each depth, the middle of the places (the level, magnitudes): ' + ', '.join(f"{dp:g}°: {np.median([lev[(st, dp)] for st in SOUTH if lev[(st, dp)] is not None]):.2f}" for dp in depths))
    print('\nB. the twenty northern photometers with every month: the middle of P at each depth, and how many give it')
    for dp in depths:
        for st in NORTH: PN[(st, dp)] = P(series(R, st, dp)[0])
    nm = {dp: [PN[(st, dp)] for st in NORTH if PN[(st, dp)] is not None] for dp in depths}
    print('   the middle      ' + ''.join(f'{np.median(nm[dp]):+8.2f}' if nm[dp] else '       .' for dp in depths))
    print('   photometers     ' + ''.join(f'{len(nm[dp]):8d}' for dp in depths))
    print('\nC. evening alone and morning alone, the middle of the southern P')
    for w, nmw in (('ev', 'evening'), ('mo', 'morning')):
        row = []
        for dp in depths:
            v = [p for p in (P(series(R, st, dp, w)[0]) for st in SOUTH) if p is not None]; row.append(f'{np.median(v):+8.2f}' if len(v) >= 5 else '       .')
        print(f'   {nmw:<16}' + ''.join(row))
    return depths, PS, mid, nm
def verdict(ok, n, need): return 'void (too few)' if n < need else ('held' if ok else 'failed')
if __name__ == '__main__':
    outp = sys.argv[1]
    if len(sys.argv) > 2: reduce_all(outp, [float(x) for x in sys.argv[2:]])
    depths, PS, mid, nm = tables(outp)
    if all(d in depths for d in (3.0, 4.0, 5.0, 8.0, 9.0, 10.0)):
        g = lambda dp: mid[dp][0]; n = lambda dp: mid[dp][1]
        print('\nThe lines of the ninth sheet (comparisons on unrounded figures, the mark itself included)')
        both = [st for st in SOUTH if PS[(st, 5.0)] is not None and PS[(st, 6.0)] is not None]; sm = sum(1 for st in both if abs(PS[(st, 5.0)]) < abs(PS[(st, 6.0)]))
        print(f'X1. at 5 degrees the change is smaller in size than at 6 degrees at 8 or more places: {sm} of {len(both)}: {verdict(sm >= 8, len(both), 9)}')
        print(f'X2. the middle at 5 degrees between -0.24 and -0.06: {g(5.0):+.3f}: {verdict(-0.24 <= g(5.0) <= -0.06, n(5.0), 7)}')
        print(f'X3. the middle at 4 degrees at -0.10 or above: {g(4.0):+.3f}: {verdict(g(4.0) >= -0.10, n(4.0), 7)}')
        print(f'X4. a dimming: the middle at 3 or at 4 degrees at +0.05 or above: {g(3.0):+.3f}, {g(4.0):+.3f}: {verdict(g(3.0) >= 0.05 or g(4.0) >= 0.05, min(n(3.0), n(4.0)), 7)}')
        print(f'X5. the middle at 8 degrees between -0.58 and -0.85: {g(8.0):+.3f}: {verdict(-0.85 <= g(8.0) <= -0.58, n(8.0), 7)}')
        print(f'X6. the middle at 9 degrees brighter than at 8: {g(9.0):+.3f} against {g(8.0):+.3f}: {verdict(g(9.0) < g(8.0), min(n(8.0), n(9.0)), 6)}')
        print(f'X7. the middle at 10 degrees at -0.70 or below: {g(10.0) if g(10.0) is None else round(g(10.0), 3)}: {verdict(g(10.0) is not None and g(10.0) <= -0.70, n(10.0), 5)}')
        s1 = None if g(10.0) is None else abs(g(10.0) - g(9.0)); s0 = abs(g(8.0) - g(7.0))
        print(f'X8. the step from 9 to 10 degrees smaller in size than the step from 7 to 8: {s1 if s1 is None else round(s1, 3)} against {s0:.3f}: {verdict(s1 is not None and s1 < s0, min(n(9.0), n(10.0)), 5)}')
        mono = all(g(b) < g(a) for a, b in ((5.0, 6.0), (6.0, 7.0), (7.0, 8.0), (8.0, 9.0)))
        print(f'X9. brighter at each step from 5 to 9 degrees at the middle: {", ".join(f"{g(d):+.2f}" for d in (5.0, 6.0, 7.0, 8.0, 9.0))}: {verdict(mono, min(n(d) for d in (5.0, 6.0, 7.0, 8.0, 9.0)), 6)}')
        nmid = {dp: float(np.median(nm[dp])) for dp in (4.0, 5.0, 6.0, 7.0, 8.0, 9.0) if nm[dp]}
        print(f'X10. the northern middle within 0.12 of nothing at every depth from 4 to 9 degrees: {", ".join(f"{d:g}: {v:+.2f}" for d, v in nmid.items())}: {verdict(all(abs(v) <= 0.12 for v in nmid.values()), min(len(nm[d]) for d in (4.0, 5.0, 6.0, 7.0, 8.0, 9.0)), 10)}')
