# The test of 26 Nov: does the cubic drift of my constant-oblateness Moon against DE441 (node, perigee) vanish against DE431, which has no t^2 term in the Earth's J2?
# Twenty 412-day windows, one per century back to the year 0, daily samples: the same windows and the same runs of my model as src/moon_vs_jpl_cen.py used.
# DE441 comes from the Horizons files in data/hzcen (ecliptic of J2000, au, au/day); DE431 from its own text files through src/de431.py (ICRF, km), turned to the ecliptic here.
# usage: python -I moon_vs_de431.py <my states file> [<another states file> ...]
import sys, re, os, numpy as np; HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import de431
AU = 149597870.7; MU = (398600.435507 + 4902.800118) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247; EPS = np.radians(84381.448 / 3600)       # the obliquity Horizons uses for its ecliptic frame
HZ = HERE + '/../data/hzcen'; STARTS = [int(x) for x in open(HERE + '/../cen_starts.txt').read().split()]
num = r'([-+]?\d\.\d+E[-+]\d+)'
def hz(p):
    b = open(p).read().split('$$SOE')[1].split('$$EOE')[0]
    return np.array([[float(x) for x in m.groups()] for m in re.finditer(r'(\d+\.\d+) = [AB]\.[DC]\..*?\n\s*X\s*=\s*' + num + r'\s*Y\s*=\s*' + num + r'\s*Z\s*=\s*' + num + r'\s*\n\s*VX=\s*' + num + r'\s*VY=\s*' + num + r'\s*VZ=\s*' + num, b)])
def elements(r, v):
    h = np.cross(r, v); rr = np.linalg.norm(r, axis=1); v2 = (v * v).sum(1); rv = (r * v).sum(1)
    e = ((v2 - MU / rr)[:, None] * r - rv[:, None] * v) / MU; ecc = np.linalg.norm(e, axis=1); a = 1 / (2 / rr - v2 / MU); inc = np.arccos(h[:, 2] / np.linalg.norm(h, axis=1)); Om = np.arctan2(h[:, 0], -h[:, 1])
    n = np.stack([np.cos(Om), np.sin(Om), 0 * Om], 1); m = np.cross(h / np.linalg.norm(h, axis=1)[:, None], n)
    w = np.arctan2((e * m).sum(1), (e * n).sum(1)); f = np.arctan2((r * m).sum(1), (r * n).sum(1)) - w
    Ean = 2 * np.arctan2(np.sqrt(1 - ecc) * np.sin(f / 2), np.sqrt(1 + ecc) * np.cos(f / 2)); return a, ecc, inc, Om, Om + w, Om + w + Ean - ecc * np.sin(Ean)
wrap = lambda x: (x + np.pi) % (2 * np.pi) - np.pi
def to_ecl(x): c, s = np.cos(EPS), np.sin(EPS); return np.stack([x[:, 0], c * x[:, 1] + s * x[:, 2], -s * x[:, 1] + c * x[:, 2]], 1)
eph = de431.load(['ascm01000.431', 'ascp00000.431', 'ascp01000.431'])
def mine(fn):
    E, M = {}, {}
    with open(fn) as f:
        for line in f:
            p = line.split()
            if p[1] == '3': E[p[0]] = [float(x) for x in p[2:]]
            elif p[1] == '4': M[p[0]] = [float(x) for x in p[2:]]
    return E, M
runs = {fn.split('/')[-1]: mine(fn) for fn in sys.argv[1:]}
def diff(ea, eb): return [(wrap(ea[k] - eb[k]) * AS).mean() for k in (5, 4, 3)] + [((ea[2] - eb[2]) * AS).mean()]        # mean longitude, perigee, node, inclination (arcsec)
T = []; tab = {}; last = None
for d in STARTS:
    Hm, He = hz(f'{HZ}/hz_{d}_301.txt'), hz(f'{HZ}/hz_{d}_399.txt'); jd = Hm[:, 0]; keys = [f'{x:.2f}' for x in jd]
    j441 = Hm[:, 1:] - He[:, 1:]; r, v = de431.moon(jd, eph); j431 = np.hstack([to_ecl(r) / AU, to_ecl(v) / AU])
    e441 = elements(j441[:, :3], j441[:, 3:]); e431 = elements(j431[:, :3], j431[:, 3:]); t = -(jd.mean() - 2451545.0) / 36525
    if any(sum(1 for k in keys if k in E and k in M) < 400 for E, M in runs.values()):
        print(f'window starting day {d} (T = {t:.2f}): a run of mine has fewer than 400 of its {len(keys)} days; left out of the fits, as in moon_vs_jpl_cen.py'); last = (t, diff(e431, e441)); continue
    T.append(t); tab.setdefault('DE431 - DE441', []).append(diff(e431, e441)); em = {}
    for name, (E, M) in runs.items():
        ok = np.array([k in E and k in M for k in keys])
        me = np.array([M[k] for k, o in zip(keys, ok) if o]) - np.array([E[k] for k, o in zip(keys, ok) if o]); em[name] = (elements(me[:, :3], me[:, 3:]), ok)
        tab.setdefault(f'{name} - DE441', []).append(diff(em[name][0], [x[ok] for x in e441])); tab.setdefault(f'{name} - DE431', []).append(diff(em[name][0], [x[ok] for x in e431]))
    names = list(runs)
    if len(names) == 2 and np.all(em[names[0]][1] == em[names[1]][1]): tab.setdefault(f'{names[0]} - {names[1]} (my two runs)', []).append(diff(em[names[0]][0], em[names[1]][0]))
if last: print(f'DE431 - DE441 in that window (no run of mine needed): mean longitude {last[1][0]:+.2f}, perigee {last[1][1]:+.2f}, node {last[1][2]:+.2f}, inclination {last[1][3]:+.3f} arcsec')
T = np.array(T)
def fit(y, powers):
    A = np.vstack([T ** p for p in powers]).T; c = np.linalg.lstsq(A, y, rcond=None)[0]; return c, np.sqrt(((y - A @ c) ** 2).mean())
for name, rows in tab.items():
    R = np.array(rows); print(f'\n=== {name} (arcsec; T in centuries back from 2000)')
    print('   T:        ' + ' '.join(f'{t:7.2f}' for t in T))
    for k, lab in enumerate(('mean longitude', 'perigee', 'node', 'inclination')):
        y = R[:, k]; print(f'   {lab:14s} ' + ' '.join(f'{x:+7.2f}' for x in y))
        if lab == 'inclination': continue
        c, rms = fit(y, (0, 1, 3)); c2, rms2 = fit(y, (0, 1, 2, 3)); c3, rms3 = fit(y, (0, 1, 2))
        print(f'        c + a T + b T^3:  b = {c[2]:+.5f}  (a = {c[1]:+.4f}, c = {c[0]:+.3f}; rms {rms:.3f})    with T^2 as well:  T^2 {c2[2]:+.5f}, T^3 {c2[3]:+.5f} (rms {rms2:.3f})    without T^3: T^2 {c3[2]:+.5f} (rms {rms3:.3f})')
