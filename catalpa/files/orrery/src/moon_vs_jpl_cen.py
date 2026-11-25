# The shape of the drift: my Moon against JPL's in twenty 412-day windows, one per century back to the year 0 (daily samples).
# usage: python -I moon_vs_jpl_cen.py <my states (daily, in the windows)> <dir with hz_<day>_<body>.txt> <file with the window start days>
import sys, re, numpy as np
states, hzdir, startsfile = sys.argv[1:4]
AU = 149597870.7; MU = (398600.435507 + 4902.800118) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247
STARTS = [int(x) for x in open(startsfile).read().split()]
num = r'([-+]?\d\.\d+E[-+]\d+)'
def hz(p):
    b = open(p).read().split('$$SOE')[1].split('$$EOE')[0]
    return np.array([[float(x) for x in m.groups()] for m in re.finditer(r'(\d+\.\d+) = [AB]\.[DC]\..*?\n\s*X\s*=\s*' + num + r'\s*Y\s*=\s*' + num + r'\s*Z\s*=\s*' + num + r'\s*\n\s*VX=\s*' + num + r'\s*VY=\s*' + num + r'\s*VZ=\s*' + num, b)])
E, M = {}, {}
with open(states) as f:
    for line in f:
        p = line.split()
        if p[1] == '3': E[p[0]] = [float(x) for x in p[2:]]
        elif p[1] == '4': M[p[0]] = [float(x) for x in p[2:]]
def elements(r, v):
    h = np.cross(r, v); rr = np.linalg.norm(r, axis=1); v2 = (v * v).sum(1); rv = (r * v).sum(1)
    e = ((v2 - MU / rr)[:, None] * r - rv[:, None] * v) / MU; ecc = np.linalg.norm(e, axis=1); a = 1 / (2 / rr - v2 / MU); inc = np.arccos(h[:, 2] / np.linalg.norm(h, axis=1)); Om = np.arctan2(h[:, 0], -h[:, 1])
    n = np.stack([np.cos(Om), np.sin(Om), 0 * Om], 1); m = np.cross(h / np.linalg.norm(h, axis=1)[:, None], n)
    w = np.arctan2((e * m).sum(1), (e * n).sum(1)); f = np.arctan2((r * m).sum(1), (r * n).sum(1)) - w
    Ean = 2 * np.arctan2(np.sqrt(1 - ecc) * np.sin(f / 2), np.sqrt(1 + ecc) * np.cos(f / 2)); return a, ecc, inc, Om, Om + w, Om + w + Ean - ecc * np.sin(Ean)
wrap = lambda x: (x + np.pi) % (2 * np.pi) - np.pi
rows = []
print('   T (cy)   mean longitude   perigee     node      inclination   eccentricity (1e-6)   [mine - JPL, 412-day means; arcsec]     JPL node (deg)')
for d in STARTS:
    Hm, He = hz(f'{hzdir}/hz_{d}_301.txt'), hz(f'{hzdir}/hz_{d}_399.txt'); jd = Hm[:, 0]; keys = [f'{x:.2f}' for x in jd]; ok = np.array([k in E and k in M for k in keys])
    if ok.sum() < 400: print(f'   window {d}: {ok.sum()} matching instants'); continue
    me = np.array([M[k] for k, o in zip(keys, ok) if o]) - np.array([E[k] for k, o in zip(keys, ok) if o]); jp = (Hm[:, 1:] - He[:, 1:])[ok]
    em = elements(me[:, :3], me[:, 3:]); ej = elements(jp[:, :3], jp[:, 3:]); T = -(jd[ok].mean() - 2451545.0) / 36525
    r = (T, (wrap(em[5] - ej[5]) * AS).mean(), (wrap(em[4] - ej[4]) * AS).mean(), (wrap(em[3] - ej[3]) * AS).mean(), ((em[2] - ej[2]) * AS).mean(), ((em[1] - ej[1]) * 1e6).mean(), np.degrees(np.angle(np.exp(1j * ej[3]).mean())) % 360)
    rows.append(r); print(f'  {r[0]:6.2f}    {r[1]:+9.2f}    {r[2]:+8.2f}   {r[3]:+8.2f}    {r[4]:+7.3f}      {r[5]:+7.3f}                                                  {r[6]:6.1f}')
R = np.array(rows); T = R[:, 0]
def fit(y, powers, extra=None):
    A = np.vstack([T ** p for p in powers] + ([] if extra is None else extra)).T; c = np.linalg.lstsq(A, y, rcond=None)[0]; return c, np.sqrt(((y - A @ c) ** 2).mean())
for name, col in (('mean longitude', 1), ('perigee', 2), ('node', 3)):
    y = R[:, col]; print(f'{name}:')
    for powers in ((1, 2), (1, 3), (1, 2, 3), (3,), (2,), (1, 2, 3, 4)):
        c, rms = fit(y, powers); print('    ' + ' '.join(f'{ci:+.5f} T^{p}' for ci, p in zip(c, powers)) + f'    rms residual {rms:.3f}"')
    c, rms = fit(y, (1, 3)); res = y - np.vstack([T, T ** 3]).T @ c; print('    residuals from a T + b T^3, epoch by epoch: ' + ' '.join(f'{x:+.2f}' for x in res))
    if col == 3:
        nd = np.radians(R[:, 6]); c2, rms2 = fit(y, (1, 3), [T * np.cos(nd), T * np.sin(nd)]); print(f'    with a term in step with the node, growing with T:  {c2[0]:+.5f} T {c2[1]:+.5f} T^3 {c2[2]:+.4f} T cos(node) {c2[3]:+.4f} T sin(node);  rms {rms2:.3f}"')
        print(f'W1  node, a T + b T^3: rms residual {rms:.3f}" (bar: under 0.3): ' + ('HELD' if rms < 0.3 else 'FAILED'))
