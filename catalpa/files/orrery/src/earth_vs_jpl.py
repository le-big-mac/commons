# My Earth-Moon barycentre against JPL's, in the same seven windows: osculating elements about the solar-system barycentre (differences only matter).
# usage: python -I earth_vs_jpl.py <my backward states> <my forward states> <dir with hz files>
import sys, re, numpy as np
back, fwd, hzdir = sys.argv[1:4]
AU = 149597870.7; GE, GMn, GS = 398600.435507, 4902.800118, 132712440041.279419; MU = (GS + GE + GMn) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247
STARTS = [9500, -29940, -104450, -182980, -292555, -365605, -730490]
num = r'([-+]?\d\.\d+E[-+]\d+)'
def hz(p):
    b = open(p).read().split('$$SOE')[1].split('$$EOE')[0]
    return np.array([[float(x) for x in m.groups()] for m in re.finditer(r'(\d+\.\d+) = [AB]\.[DC]\..*?\n\s*X\s*=\s*' + num + r'\s*Y\s*=\s*' + num + r'\s*Z\s*=\s*' + num + r'\s*\n\s*VX=\s*' + num + r'\s*VY=\s*' + num + r'\s*VZ=\s*' + num, b)])
def mine(path, want):
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
    e = ((v2 - MU / rr)[:, None] * r - rv[:, None] * v) / MU; ecc = np.linalg.norm(e, axis=1); a = 1 / (2 / rr - v2 / MU)
    Om = np.arctan2(h[:, 0], -h[:, 1]); n = np.stack([np.cos(Om), np.sin(Om), 0 * Om], 1); m = np.cross(h / np.linalg.norm(h, axis=1)[:, None], n)
    w = np.arctan2((e * m).sum(1), (e * n).sum(1)); f = np.arctan2((r * m).sum(1), (r * n).sum(1)) - w
    Ean = 2 * np.arctan2(np.sqrt(1 - ecc) * np.sin(f / 2), np.sqrt(1 + ecc) * np.cos(f / 2)); return a, ecc, np.arccos(h[:, 2] / np.linalg.norm(h, axis=1)), Om + w, Om + w + Ean - ecc * np.sin(Ean)
wrap = lambda x: (x + np.pi) % (2 * np.pi) - np.pi
print('Earth-Moon barycentre, mine - JPL, 412-day means [sd of daily differences]')
print('   T (cy)    position difference (km): mean size, largest    mean longitude (arcsec)   perihelion (arcsec)   eccentricity (1e-9)    inclination to J2000 ecliptic (arcsec)')
for d in STARTS:
    Hm, He = hz(f'{hzdir}/hz_{d}_301.txt'), hz(f'{hzdir}/hz_{d}_399.txt'); jd = Hm[:, 0]; keys = [f'{x:.2f}' for x in jd]; E, M = mine(fwd if d > 0 else back, set(keys))
    ok = np.array([k in E and k in M for k in keys]); f1, f2 = GE / (GE + GMn), GMn / (GE + GMn)
    me = f1 * np.array([E[k] for k, o in zip(keys, ok) if o]) + f2 * np.array([M[k] for k, o in zip(keys, ok) if o]); jp = (f1 * He[:, 1:] + f2 * Hm[:, 1:])[ok]
    dr = np.linalg.norm(me[:, :3] - jp[:, :3], axis=1) * AU; em = elements(me[:, :3], me[:, 3:]); ej = elements(jp[:, :3], jp[:, 3:]); T = -(jd[ok].mean() - 2451545.0) / 36525
    dL = wrap(em[4] - ej[4]) * AS; dw = wrap(em[3] - ej[3]) * AS; de = (em[1] - ej[1]) * 1e9; di = (em[2] - ej[2]) * AS
    print(f'  {T:7.3f}      {dr.mean():9.2f}  {dr.max():9.2f}              {dL.mean():+8.4f} [{dL.std():.4f}]      {dw.mean():+8.3f} [{dw.std():.3f}]     {de.mean():+8.2f} [{de.std():.2f}]      {di.mean():+.5f} [{di.std():.5f}]')
