# Does my Earth's orbit plane (the ecliptic of date) drift from JPL's, and does the Moon's plane follow it?
# Mean orbit normals over 412 days: heliocentric Earth-Moon barycentre, and geocentric Moon; mine minus JPL, in arcsec on the J2000 ecliptic (x, y).
# usage: python -I plane_vs_jpl.py <my backward states> <my forward states> <dir with hz files>
import sys, re, numpy as np
back, fwd, hzdir = sys.argv[1:4]
AS = 206264.806247; GE, GMn = 398600.435507, 4902.800118; f1, f2 = GE / (GE + GMn), GMn / (GE + GMn)
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
def normal(r, v):
    h = np.cross(r, v); h /= np.linalg.norm(h, axis=1)[:, None]; return h
print('   T (cy)   Earth-Moon orbit pole, mine - JPL (arcsec): x, y, size   [inclination of that plane to J2000 ecliptic]   Moon orbit pole, mine - JPL: x, y, size    Moon pole minus Earth pole difference: x, y')
rows = []
for d in STARTS:
    Hs, He, Hm = (hz(f'{hzdir}/hz_{d}_{b}.txt') for b in (10, 399, 301)); jd = Hm[:, 0]; keys = [f'{x:.2f}' for x in jd]; B = mine(fwd if d > 0 else back, set(keys))
    ok = np.array([all(k in B[b] for b in B) for k in keys]); S, E, M = (np.array([B[b][k] for k, o in zip(keys, ok) if o]) for b in (0, 3, 4))
    emb_m = f1 * E + f2 * M - S; emb_j = (f1 * He[:, 1:] + f2 * Hm[:, 1:] - Hs[:, 1:])[ok]; mo_m = M - E; mo_j = (Hm[:, 1:] - He[:, 1:])[ok]
    ne_m, ne_j = normal(emb_m[:, :3], emb_m[:, 3:]).mean(0), normal(emb_j[:, :3], emb_j[:, 3:]).mean(0); nm_m, nm_j = normal(mo_m[:, :3], mo_m[:, 3:]).mean(0), normal(mo_j[:, :3], mo_j[:, 3:]).mean(0)
    de = (ne_m - ne_j) * AS; dm = (nm_m - nm_j) * AS; T = -(jd[ok].mean() - 2451545.0) / 36525; inc = np.degrees(np.arccos(ne_j[2] / np.linalg.norm(ne_j))) * 3600
    rows.append((T, de[0], de[1], dm[0], dm[1]))
    print(f'  {T:7.3f}    {de[0]:+8.4f} {de[1]:+8.4f}  {np.hypot(de[0], de[1]):7.4f}     [{inc:8.2f}"]          {dm[0]:+8.4f} {dm[1]:+8.4f}  {np.hypot(dm[0], dm[1]):7.4f}        {dm[0] - de[0]:+8.4f} {dm[1] - de[1]:+8.4f}')
