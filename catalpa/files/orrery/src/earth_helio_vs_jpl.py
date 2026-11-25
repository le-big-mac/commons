# My Earth-Moon barycentre against JPL's, HELIOCENTRIC this time (the earlier check used elements about the solar-system barycentre): 412-day means in the seven windows.
import sys, re, numpy as np
back, fwd, hzdir = sys.argv[1:4]
AU = 149597870.7; GE, GMn, GS = 398600.435507, 4902.800118, 132712440041.279419; MU = (GS + GE + GMn) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247; f1, f2 = GE / (GE + GMn), GMn / (GE + GMn)
STARTS = [9500, -29940, -104450, -182980, -292555, -365605, -730490]
num = r'([-+]?\d\.\d+E[-+]\d+)'
def hz(p):
    b = open(p).read().split('$$SOE')[1].split('$$EOE')[0]
    return np.array([[float(x) for x in m.groups()] for m in re.finditer(r'(\d+\.\d+) = [AB]\.[DC]\..*?\n\s*X\s*=\s*' + num + r'\s*Y\s*=\s*' + num + r'\s*Z\s*=\s*' + num + r'\s*\n\s*VX=\s*' + num + r'\s*VY=\s*' + num + r'\s*VZ=\s*' + num, b)])
def mine(path, want):
    B = {0: {}, 3: {}, 4: {}}
    with open(path) as f:
        for line in f:
            k = line[:10]
            if k in want:
                p = line.split(); b = int(p[1])
                if b in B: B[b][k] = [float(x) for x in p[2:]]
    return B
def elements(x):
    r, v = x[:, :3], x[:, 3:]; h = np.cross(r, v); rr = np.linalg.norm(r, axis=1); v2 = (v * v).sum(1); rv = (r * v).sum(1)
    e = ((v2 - MU / rr)[:, None] * r - rv[:, None] * v) / MU; ecc = np.linalg.norm(e, axis=1); a = 1 / (2 / rr - v2 / MU); Om = np.arctan2(h[:, 0], -h[:, 1])
    n = np.stack([np.cos(Om), np.sin(Om), 0 * Om], 1); m = np.cross(h / np.linalg.norm(h, axis=1)[:, None], n)
    w = np.arctan2((e * m).sum(1), (e * n).sum(1)); f = np.arctan2((r * m).sum(1), (r * n).sum(1)) - w
    E = 2 * np.arctan2(np.sqrt(1 - ecc) * np.sin(f / 2), np.sqrt(1 + ecc) * np.cos(f / 2)); return a, ecc, Om + w, Om + w + E - ecc * np.sin(E)
wrap = lambda x: (x + np.pi) % (2 * np.pi) - np.pi
print('heliocentric Earth-Moon barycentre, mine - JPL, 412-day means [sd of the daily differences]')
print('   T (cy)   eccentricity (1e-9)        perihelion (arcsec)      mean longitude (arcsec)     semi-major axis (m)      JPL mean eccentricity')
for d in STARTS:
    Hs, He, Hm = (hz(f'{hzdir}/hz_{d}_{b}.txt') for b in (10, 399, 301)); jd = Hm[:, 0]; keys = [f'{x:.2f}' for x in jd]; B = mine(fwd if d > 0 else back, set(keys))
    ok = np.array([all(k in B[b] for b in B) for k in keys]); S, E, M = (np.array([B[b][k] for k, o in zip(keys, ok) if o]) for b in (0, 3, 4))
    em = elements(f1 * E + f2 * M - S); ej = elements((f1 * He[:, 1:] + f2 * Hm[:, 1:] - Hs[:, 1:])[ok]); T = -(jd[ok].mean() - 2451545.0) / 36525
    de = (em[1] - ej[1]) * 1e9; dw = wrap(em[2] - ej[2]) * AS; dL = wrap(em[3] - ej[3]) * AS; da = (em[0] - ej[0]) * AU * 1e3
    print(f'  {T:7.3f}    {de.mean():+8.2f} [{de.std():7.2f}]       {dw.mean():+8.4f} [{dw.std():.4f}]       {dL.mean():+8.4f} [{dL.std():.4f}]       {da.mean():+9.2f} [{da.std():.2f}]          {ej[1].mean():.7f}')
