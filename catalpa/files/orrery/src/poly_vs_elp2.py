# A third witness: my model's Moon minus the standard lunar-theory polynomials (Meeus, Astronomical Algorithms ch. 47, after Chapront's ELP 2000-82B; quoted from memory -
# the L', perigee and node polynomials used here reproduce the M' and F polynomials of the same table, which is the check I can make without the book).
# The difference is smoothed over the node period twice and the perigee period once and fitted with a constant, t, t^2, t^3 (t in centuries from J2000, negative = past).
import sys, numpy as np
AU = 149597870.7; MU = (398600.435507 + 4902.800118) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247
a = np.loadtxt(sys.argv[1]); E = a[a[:, 1] == 3]; M = a[a[:, 1] == 4]; n = min(len(E), len(M)); jd = E[:n, 0]; x = M[:n, 2:] - E[:n, 2:]; t = (jd - 2451545.0) / 36525
P = (4.199094 * t + 0.1939873 * t ** 2 - 0.00022466 * t ** 3) / AS; Q = (-46.811015 * t + 0.0510283 * t ** 2 + 0.00052413 * t ** 3) / AS
k = np.stack([P, -Q, np.sqrt(1 - P * P - Q * Q)], 1); ax = np.cross(k, [0, 0, 1.0]); s_ = np.linalg.norm(ax, axis=1); c_ = k[:, 2]; u = ax / np.where(s_ > 0, s_, 1)[:, None]
def turn(v): return v * c_[:, None] + np.cross(u, v) * s_[:, None] + u * (u * v).sum(1)[:, None] * (1 - c_)[:, None]
r, v = turn(x[:, :3]), turn(x[:, 3:])
h = np.cross(r, v); rr = np.linalg.norm(r, axis=1); v2 = (v * v).sum(1); rv = (r * v).sum(1); e = ((v2 - MU / rr)[:, None] * r - rv[:, None] * v) / MU; ecc = np.linalg.norm(e, axis=1); Om = np.arctan2(h[:, 0], -h[:, 1])
nn = np.stack([np.cos(Om), np.sin(Om), 0 * Om], 1); m = np.cross(h / np.linalg.norm(h, axis=1)[:, None], nn); w = np.arctan2((e * m).sum(1), (e * nn).sum(1)); f = np.arctan2((r * m).sum(1), (r * nn).sum(1)) - w
Ean = 2 * np.arctan2(np.sqrt(1 - ecc) * np.sin(f / 2), np.sqrt(1 + ecc) * np.cos(f / 2)); Man = Ean - ecc * np.sin(Ean)
pA = (5028.796195 * t + 1.1054348 * t ** 2 + 0.00007964 * t ** 3 - 0.000023857 * t ** 4) / AS          # general precession in longitude, to refer my angles to the equinox of date
STD = {'node': np.radians(125.0445479 - 1934.1362891 * t + 0.0020754 * t ** 2 + t ** 3 / 467441 - t ** 4 / 60616000),
       'perigee': np.radians(83.3532465 + 4069.0137287 * t - 0.0103200 * t ** 2 - t ** 3 / 80053 + t ** 4 / 18999000),
       'mean longitude': np.radians(218.3164477 + 481267.88123421 * t - 0.0015786 * t ** 2 + t ** 3 / 538841 - t ** 4 / 65194000)}
MINE = {'node': Om + pA, 'perigee': Om + w + pA, 'mean longitude': Om + w + Man + pA}
def box(y, mlen): c = np.cumsum(np.insert(y, 0, 0.0)); return (c[mlen:] - c[:-mlen]) / mlen
jplcube = {'node': +0.0017, 'perigee': -0.0020, 'mean longitude': -0.0035}; ok = True
print('mine - standard polynomial, smoothed; fit c0 + c1 t + c2 t^2 + c3 t^3 over -19.5 < t < -0.5 (arcsec):')
for name in ('mean longitude', 'perigee', 'node'):
    d = np.unwrap(MINE[name] - STD[name]); d = (d - 2 * np.pi * np.round(d[0] / (2 * np.pi))) * AS; yy, tt = d, t
    for mlen in (680, 680, 323): yy = box(yy, mlen); tt = box(tt, mlen)
    mk = (tt > -19.5) & (tt < -0.5); c = np.polyfit(tt[mk], yy[mk], 3)[::-1]; res = yy[mk] - np.polyval(np.polyfit(tt[mk], yy[mk], 3), tt[mk])
    blk = (np.floor(-tt[mk] / 2) % 2 == 0); ca = np.polyfit(tt[mk][blk], yy[mk][blk], 3)[::-1]; cb = np.polyfit(tt[mk][~blk], yy[mk][~blk], 3)[::-1]
    print(f'   {name:15s} c0 = {c[0]:+7.2f}  c1 = {c[1]:+8.3f}  c2 = {c[2]:+8.4f}  c3 = {c[3]:+.5f} (alternate blocks {ca[3]:+.5f}, {cb[3]:+.5f})   rms {res.std():.2f}"      [mine - JPL: c3 = {jplcube[name]:+.4f}]')
    ok &= (np.sign(c[3]) == np.sign(jplcube[name])) and (1 / 1.5 <= abs(c[3] / jplcube[name]) <= 1.5)
print('H1: ' + ('HELD' if ok else 'FAILED'))
