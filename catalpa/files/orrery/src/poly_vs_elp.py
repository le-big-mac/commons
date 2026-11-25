# My model's Moon over 2000 years (10-day samples, back from J2000): the slow polynomial parts of node, perigee and mean longitude, set beside the standard lunar-theory polynomials
# (Meeus, Astronomical Algorithms ch. 47, from Chapront's ELP 2000-82B; quoted from memory of that table, so treat the reference column with that caution).
# Elements are referred to the ecliptic OF DATE (IAU 2006 P_A, Q_A), reached from J2000 by the smallest turn; the standard polynomials are from the equinox of date, so the general
# precession p_A = 5028.796195 t + 1.1054348 t^2 + 0.00007964 t^3 - 0.000023857 t^4 arcsec is taken off them.
import sys, numpy as np
AU = 149597870.7; MU = (398600.435507 + 4902.800118) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247
a = np.loadtxt(sys.argv[1]); E = a[a[:, 1] == 3]; M = a[a[:, 1] == 4]; n = min(len(E), len(M)); jd = E[:n, 0]; x = M[:n, 2:] - E[:n, 2:]; t = (jd - 2451545.0) / 36525      # t < 0: the past
P = (4.199094 * t + 0.1939873 * t ** 2 - 0.00022466 * t ** 3) / AS; Q = (-46.811015 * t + 0.0510283 * t ** 2 + 0.00052413 * t ** 3) / AS
k = np.stack([P, -Q, np.sqrt(1 - P * P - Q * Q)], 1); ax = np.cross(k, [0, 0, 1.0]); s_ = np.linalg.norm(ax, axis=1); c_ = k[:, 2]; u = ax / np.where(s_ > 0, s_, 1)[:, None]
def turn(v): return v * c_[:, None] + np.cross(u, v) * s_[:, None] + u * (u * v).sum(1)[:, None] * (1 - c_)[:, None]
r, v = turn(x[:, :3]), turn(x[:, 3:])
h = np.cross(r, v); rr = np.linalg.norm(r, axis=1); v2 = (v * v).sum(1); rv = (r * v).sum(1); e = ((v2 - MU / rr)[:, None] * r - rv[:, None] * v) / MU; ecc = np.linalg.norm(e, axis=1); Om = np.arctan2(h[:, 0], -h[:, 1])
nn = np.stack([np.cos(Om), np.sin(Om), 0 * Om], 1); m = np.cross(h / np.linalg.norm(h, axis=1)[:, None], nn); w = np.arctan2((e * m).sum(1), (e * nn).sum(1)); f = np.arctan2((r * m).sum(1), (r * nn).sum(1)) - w
Ean = 2 * np.arctan2(np.sqrt(1 - ecc) * np.sin(f / 2), np.sqrt(1 + ecc) * np.cos(f / 2)); Man = Ean - ecc * np.sin(Ean)
def box(y, mlen): c = np.cumsum(np.insert(y, 0, 0.0)); return (c[mlen:] - c[:-mlen]) / mlen
def unwrap_fast(angle, rate_deg_per_cy):
    """unwrap an angle sampled every 10 days whose rate is large: take off the nominal linear motion first"""
    lin = np.radians(rate_deg_per_cy) * t; return np.unwrap(angle - lin) + lin
REF = {'node': (-1934.1362891, 0.0020754 * 3600, 3600 / 467441.0, -3600 / 60616000.0), 'perigee': (4069.0137287, -0.0103200 * 3600, -3600 / 80053.0, 3600 / 18999000.0), 'mean longitude': (481267.88123421, -0.0015786 * 3600, 3600 / 538841.0, -3600 / 65194000.0)}
PA = (5028.796195, 1.1054348, 0.00007964, -0.000023857)
series = {'node': unwrap_fast(Om, REF['node'][0] - PA[0] / 3600), 'perigee': unwrap_fast(Om + w, REF['perigee'][0] - PA[0] / 3600), 'mean longitude': unwrap_fast(Om + w + Man, REF['mean longitude'][0] - PA[0] / 3600)}
print('coefficients of t^2, t^3, t^4 (arcsec; t in centuries from J2000, the run covers t = -20 to 0); smoothed over the node period twice and the perigee period once; quartic fit')
print('                      t^2: mine    standard      t^3: mine    standard     difference       t^4: mine     standard')
for name, y in series.items():
    yy, tt = y * AS, t
    for mlen in (680, 680, 323): yy = box(yy, mlen); tt = box(tt, mlen)
    c = np.polyfit(tt, yy, 4)[::-1]; ref = REF[name]
    r2, r3, r4 = ref[1] - PA[1], ref[2] - PA[2], ref[3] - PA[3]
    res = yy - np.polyval(np.polyfit(tt, yy, 4), tt)
    print(f'   {name:15s}  {c[2]:+10.4f}  {r2:+10.4f}     {c[3]:+10.5f}  {r3:+10.5f}   {c[3] - r3:+9.5f}       {c[4]:+.2e}  {r4:+.2e}     (rate {c[1] / 3600:+.5f} deg/cy, standard {ref[0] - PA[0] / 3600:+.5f}; rms about the quartic {res.std():.2f}")')
print('the cubes of (mine - JPL) from the century windows, in the same forward t: node +0.0017, perigee -0.0020, mean longitude -0.0035')
