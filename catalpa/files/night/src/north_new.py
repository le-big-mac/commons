# The nineteenth sheet scored: the darker twilight of late 2019 at northern photometers of the first make that had
# never been fetched here (data/tw5, by src/north_fetch.py). The reading itself with the Sun 3 and 7 degrees down
# (the ninth sheet's reduction, src/depth.py's job and monthfig, unchanged) and the moonless night (as in
# src/raikoke_night2.py: the Sun 18 degrees or more down, the Moon below the horizon, every tenth reading, the
# middle of each night with twenty readings or more; for a month the night that three quarters are brighter than,
# five nights or more). A place is used only if all the months it gives carry one chip. A place's figure for a
# stretch is the mean over the months both years give (two or more of the three). Positive: the later year darker.
import os, re, sys, glob, pickle, importlib.util, datetime as dt
from multiprocessing import Pool
import numpy as np
B = '/home/agent1/night/'
def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
DP = mod('depth', B + 'src/depth.py'); NF = mod('nf', B + 'src/north_fetch.py'); TW = DP.TW
POS = {}
for line in open(B + 'data/listing/north_new_probe.txt'):
    if ':' in line: st, lat, lon = line.split(':')[0].split(); POS[st] = (float(lat), float(lon))
def job(a):
    st, y, m, fn = a; key, r = DP.job((st, y, m, fn, (3.0, 7.0)))
    if r is None: return key, None
    out = dict(mac=(r.get('mac') or '')[-8:], d3=DP.monthfig(r, 3.0), d7=DP.monthfig(r, 7.0), night=None)
    txt = open(fn, encoding='utf-8', errors='replace').read(); head, body = txt.split('# END OF HEADER', 1); mp = re.search(r'# Position: ([-\d.]+), ([-\d.]+)', head)
    lat, lon = (float(mp.group(1)), float(mp.group(2))) if mp else POS[st]; T, F = [], []
    for line in body.splitlines():
        p = line.split(';')
        if len(p) < 7: continue
        try: f = float(p[4]); t = dt.datetime.strptime(p[0][:19], '%Y-%m-%dT%H:%M:%S')
        except ValueError: continue
        if f > 0: T.append((t - TW.T2000).total_seconds()); F.append(f)
    if len(T) >= 100:
        T = np.array(T); M = 20.5 - 2.5 * np.log10(np.array(F)); alt = TW.sun_alt_vec(T, lat, lon); nights = {}
        for k in np.where(alt < -18.0)[0][::10]:
            if TW.sky.moon_alt(TW.T2000 + dt.timedelta(seconds=float(T[k])), lat, lon) > 0: continue
            nights.setdefault(int((T[k] + lon * 240.0 - 43200.0) // 86400), []).append(M[k])
        v = [float(np.median(x)) for x in nights.values() if len(x) >= 20]
        if len(v) >= 5: out['night'] = float(np.percentile(v, 75))
    return key, out
if __name__ == '__main__':
    sts = NF.chosen(); jobs = [(st, int(os.path.basename(fn).split('_')[1][:4]), int(fn[-6:-4]), fn) for st in sts for fn in sorted(glob.glob(B + f'data/tw5/{st}_20??-??.dat'))]
    with Pool(12) as p: R = dict(p.map(job, jobs, chunksize=2))
    pickle.dump(R, open(B + 'cache2/north_new.pkl', 'wb'))
    SPR, AUT = (3, 4, 5), (9, 10, 11); f = lambda v: '    . ' if v is None else f'{v:+6.2f}'
    def one_chip(st): return len({r['mac'] for (s, y, m), r in R.items() if s == st and r is not None}) == 1
    def diff(st, y1, y0, months, what):
        d = [R[(st, y1, m)][what] - R[(st, y0, m)][what] for m in months if R.get((st, y1, m)) and R.get((st, y0, m)) and R[(st, y1, m)][what] is not None and R[(st, y0, m)][what] is not None]
        return float(np.mean(d)) if len(d) >= 2 else None
    print(f'{len(sts)} photometers chosen; {len(jobs)} files; positive: the later year reads darker (magnitudes; . no figure)')
    print('   place      latitude  one chip | at 3 degrees: autumn 2019 less 2018, spring 2019 less 2018, their difference, autumn 2020 less 2019 | at 7 degrees: autumn 2019 less 2018 | the clear night: autumn 2019 less 2018')
    rows = {}
    for st in sts:
        a = diff(st, 2019, 2018, AUT, 'd3'); b = diff(st, 2019, 2018, SPR, 'd3'); oc = one_chip(st)
        r = [a, b, (a - b) if a is not None and b is not None else None, diff(st, 2020, 2019, AUT, 'd3'), diff(st, 2019, 2018, AUT, 'd7'), diff(st, 2019, 2018, AUT, 'night')]
        print(f"   {st:<10} {POS[st][0]:+7.1f}   {'yes' if oc else 'NO '}     | " + ' '.join(f(x) for x in r[:4]) + ' | ' + f(r[4]) + ' | ' + f(r[5]))
        if oc: rows[st] = r
    def middle(i): v = [rows[s][i] for s in rows if rows[s][i] is not None]; return (float(np.median(v)), len(v)) if v else (None, 0)
    g = lambda t: 'none' if t[0] is None else f'{t[0]:+.3f} ({t[1]})'
    print('\nThe lines of the nineteenth sheet (places with one chip; unrounded figures; marks included)')
    m1 = middle(0); print(f"F1. at 3 degrees, September to November 2019 less 2018: the middle at +0.10 or above: {g(m1)}: {'void' if m1[1] < 8 else ('held' if m1[0] >= 0.10 else 'failed')}")
    m2 = middle(2); print(f"F2. at 3 degrees, that less (March to May 2019 less 2018), place by place: the middle at +0.08 or above: {g(m2)}: {'void' if m2[1] < 6 else ('held' if m2[0] >= 0.08 else 'failed')}")
    m3 = middle(4); print(f"F3. at 7 degrees, September to November 2019 less 2018: the middle at +0.10 or above: {g(m3)}: {'void' if m3[1] < 8 else ('held' if m3[0] >= 0.10 else 'failed')}")
    m4 = middle(5); print(f"F4. the clear night, September to November 2019 less 2018: the middle within 0.08 of nothing: {g(m4)}: {'void' if m4[1] < 6 else ('held' if abs(m4[0]) <= 0.08 else 'failed')}")
    m5 = middle(3); print(f"F5. at 3 degrees, September to November 2020 less 2019: the middle at -0.05 or below: {g(m5)}: {'void' if m5[1] < 6 else ('held' if m5[0] <= -0.05 else 'failed')}")
    am = [rows[s][0] for s in rows if rows[s][0] is not None and POS[s][1] < -30.0]; print(f"F6. the photometers in North America, F1's figure: the middle at +0.05 or above: {('none' if not am else f'{np.median(am):+.3f} ({len(am)})')}: {'void' if len(am) < 2 else ('held' if np.median(am) >= 0.05 else 'failed')}")
    print('\nfor the record: how many places stand at +0.10 or above by F1\'s figure: ' + f"{sum(1 for s in rows if rows[s][0] is not None and rows[s][0] >= 0.10)} of {sum(1 for s in rows if rows[s][0] is not None)}" + '; the same by latitude: north of 45: ' + g((lambda v: (float(np.median(v)), len(v)) if v else (None, 0))([rows[s][0] for s in rows if rows[s][0] is not None and POS[s][0] >= 45])) + '; 35 to 45: ' + g((lambda v: (float(np.median(v)), len(v)) if v else (None, 0))([rows[s][0] for s in rows if rows[s][0] is not None and 35 <= POS[s][0] < 45])) + '; south of 35: ' + g((lambda v: (float(np.median(v)), len(v)) if v else (None, 0))([rows[s][0] for s in rows if rows[s][0] is not None and POS[s][0] < 35])))
