# My Moon against JPL's (DE441 via Horizons), directly: geocentric osculating elements at the same instants, daily over 412 days
# (two turns of the 206-day term in the perigee, 14 synodic and 15 anomalistic months), in each backward window and one forward.
# usage: python -I moon_vs_jpl.py <my backward states file> <my forward states file> <dir with hz_<day>_<body>.txt> [label]
import sys, re, numpy as np
back, fwd, hzdir = sys.argv[1:4]; label = sys.argv[4] if len(sys.argv) > 4 else ''
AU = 149597870.7; MU = (398600.435507 + 4902.800118) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247
STARTS = [9500, -29940, -104450, -182980, -292555, -365605, -730490]
num = r'([-+]?\d\.\d+E[-+]\d+)'
def hz(p):
    b = open(p).read().split('$$SOE')[1].split('$$EOE')[0]; out = []
    for m in re.finditer(r'(\d+\.\d+) = [AB]\.[DC]\..*?\n\s*X\s*=\s*' + num + r'\s*Y\s*=\s*' + num + r'\s*Z\s*=\s*' + num + r'\s*\n\s*VX=\s*' + num + r'\s*VY=\s*' + num + r'\s*VZ=\s*' + num, b):
        out.append([float(x) for x in m.groups()])
    return np.array(out)
def mine(path, want):
    """states of Earth (3) and Moon (4) at the wanted JDs (two decimals) from a state file"""
    E, M = {}, {}
    with open(path) as f:
        for line in f:
            k = line[:10]
            if k in want:
                p = line.split()
                if p[1] == '3': E[k] = [float(x) for x in p[2:]]
                elif p[1] == '4': M[k] = [float(x) for x in p[2:]]
    return E, M
def elements(r, v):
    h = np.cross(r, v); rr = np.linalg.norm(r, axis=1); v2 = (v * v).sum(1); rv = (r * v).sum(1)
    e = ((v2 - MU / rr)[:, None] * r - rv[:, None] * v) / MU; ecc = np.linalg.norm(e, axis=1)
    a = 1 / (2 / rr - v2 / MU); inc = np.arccos(h[:, 2] / np.linalg.norm(h, axis=1)); Om = np.arctan2(h[:, 0], -h[:, 1])
    n = np.stack([np.cos(Om), np.sin(Om), 0 * Om], 1); m = np.cross(h / np.linalg.norm(h, axis=1)[:, None], n)
    w = np.arctan2((e * m).sum(1), (e * n).sum(1)); f = np.arctan2((r * m).sum(1), (r * n).sum(1)) - w
    Ean = 2 * np.arctan2(np.sqrt(1 - ecc) * np.sin(f / 2), np.sqrt(1 + ecc) * np.cos(f / 2)); Man = Ean - ecc * np.sin(Ean)
    return a, ecc, inc, Om, Om + w, Om + w + Man
wrap = lambda x: (x + np.pi) % (2 * np.pi) - np.pi
rows = []
print(f'{label}  (mine - JPL), averaged over 412 days; T = centuries before J2000; angles in arcsec; standard deviation of the daily differences in brackets')
print('   T (cy)    mean longitude      perigee             node               inclination    eccentricity (1e-6)   semi-major axis (km)')
for d in STARTS:
    Hm, He = hz(f'{hzdir}/hz_{d}_301.txt'), hz(f'{hzdir}/hz_{d}_399.txt'); jd = Hm[:, 0]; want = {f'{x:.2f}' for x in jd}
    E, M = mine(fwd if d > 0 else back, want); keys = [f'{x:.2f}' for x in jd]; ok = [k in E and k in M for k in keys]
    if sum(ok) < 400: print(f'   window {d}: only {sum(ok)} matching instants'); continue
    ok = np.array(ok); me = np.array([M[k] for k, o in zip(keys, ok) if o]) - np.array([E[k] for k, o in zip(keys, ok) if o]); jp = (Hm[:, 1:] - He[:, 1:])[ok]
    em = elements(me[:, :3], me[:, 3:]); ej = elements(jp[:, :3], jp[:, 3:]); T = -(jd[ok].mean() - 2451545.0) / 36525
    dL = wrap(em[5] - ej[5]) * AS; dw = wrap(em[4] - ej[4]) * AS; dO = wrap(em[3] - ej[3]) * AS; di = (em[2] - ej[2]) * AS; de = (em[1] - ej[1]) * 1e6; da = (em[0] - ej[0]) * AU
    rows.append((T, dL.mean(), dw.mean(), dO.mean(), di.mean(), de.mean(), da.mean()))
    print(f'  {T:7.3f}   {dL.mean():+9.2f} [{dL.std():6.2f}]   {dw.mean():+9.2f} [{dw.std():6.2f}]   {dO.mean():+8.2f} [{dO.std():5.2f}]   {di.mean():+6.3f} [{di.std():.3f}]   {de.mean():+7.3f} [{de.std():.3f}]   {da.mean():+8.4f} [{da.std():.4f}]')
R = np.array(rows); T = R[:, 0]
if len(R) >= 4:
    A = np.vstack([T, T * T]).T
    cL = np.linalg.lstsq(A, R[:, 1], rcond=None)[0]; cw = np.linalg.lstsq(A, R[:, 2], rcond=None)[0]; cO = np.linalg.lstsq(A, R[:, 3], rcond=None)[0]
    lw = (T * R[:, 2]).sum() / (T * T).sum(); lO = (T * R[:, 3]).sum() / (T * T).sum()
    print(f'fits through zero at J2000 (T counted into the past, so a quantity that runs FAST in my model shows a NEGATIVE difference in the past):')
    print(f'   mean longitude: {cL[0]:+.2f} T {cL[1]:+.3f} T^2 arcsec     (the eclipse times implied -4.28 T - 0.467 T^2)')
    print(f'   perigee: {cw[0]:+.2f} T {cw[1]:+.3f} T^2;  straight line alone {lw:+.2f} T   -> my perigee rate minus JPL\'s: {-lw:+.2f} arcsec per century')
    print(f'   node:    {cO[0]:+.2f} T {cO[1]:+.3f} T^2;  straight line alone {lO:+.2f} T   -> my node rate minus JPL\'s: {-lO:+.2f} arcsec per century')
    for Tq in (5, 10, 20):
        i = np.argmin(abs(T - Tq)); exp = -(4.28 * T[i] + 0.467 * T[i] ** 2); print(f'   at T = {T[i]:.2f}: mean-longitude difference {R[i, 1]:+.1f}, eclipse times implied {exp:+.1f}  (ratio {R[i, 1] / exp:.2f})')
