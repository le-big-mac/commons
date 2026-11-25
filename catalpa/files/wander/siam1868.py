# The eclipse of 18 August 1868 at Wah-koa, Siam, from my own integration of the Sun, Earth and Moon (~/orrery, run_1868.sh), with the Earth's axis the integration carries.
# Local circumstances for an observer on the ellipsoid: contacts, duration, local times; the central line; the geocentric instant of greatest eclipse.
# Expectations K1-K4 in ~/journal.md (25 Nov), written before the run.
import numpy as np, sys
sys.path.insert(0, '/home/agent1/orrery/src'); import eclipse2
AU = 149597870.7; C = 299792.458 * 86400 / AU; EPS0 = np.radians(23.4392911); H = 0.05
RSUN = 696000.0 / AU; RE_KM = 6378.137; FLAT = 1 / 298.257223563
K_IAU, K_SMALL = 0.2725076, 0.272281          # the Moon's radius in Earth radii: the IAU value, and the smaller one NASA's catalogue uses for the umbra
DT = 2.3 / 86400.0                            # TT - UT in days (Espenak & Meeus polynomial for 1860-1900 gives 2.3 s at 1868.63)
a = np.loadtxt('/home/agent1/orrery/states_1868.txt'); n = len(a) // 11; a = a[:n * 11].reshape(n, 11, 8); o = np.argsort(a[:, 0, 0]); a = a[o]
JD = a[:, 0, 0]; S, E, M = a[:, 0, 2:], a[:, 3, 2:], a[:, 4, 2:]
L = np.loadtxt('/home/agent1/orrery/lib_1868.txt'); L = L[np.argsort(L[:, 0])]; TL = L[:, 0] + 2451545.0; POLE = L[:, 4:7] / np.linalg.norm(L[:, 4:7], axis=1)[:, None]
def st(X, jd):
    i = int(np.clip((jd - JD[0]) / H, 0, n - 2)); f = (jd - JD[i]) / H; p0, v0, p1, v1 = X[i, :3], X[i, 3:], X[i + 1, :3], X[i + 1, 3:]
    return (2 * f ** 3 - 3 * f ** 2 + 1) * p0 + (f ** 3 - 2 * f ** 2 + f) * H * v0 + (-2 * f ** 3 + 3 * f ** 2) * p1 + (f ** 3 - f ** 2) * H * v1
def VE(jd): return (st(E, jd + 0.001) - st(E, jd - 0.001)) / 0.002        # the Earth's velocity, au/day
def pole(jd): p = np.array([np.interp(jd, TL, POLE[:, k]) for k in range(3)]); return p / np.linalg.norm(p)
X0 = np.array([1.0, 0, 0]); Z0 = np.array([0, np.sin(EPS0), np.cos(EPS0)]); Y0 = np.cross(Z0, X0)      # the equator and equinox of J2000 in the integration's (ecliptic) frame
def frame(jd_tt):
    """Earth-fixed axes (Greenwich meridian on the equator, 90 E, the pole) as inertial unit vectors at this instant"""
    p = pole(jd_tt); k = np.cross(Z0, p); x1 = X0 + np.cross(k, X0) + np.cross(k, np.cross(k, X0)) / (1 + Z0 @ p)      # x-axis carried from J2000 by the smallest turn that takes the old pole to the new
    s = -(p @ X0) * (p @ Y0) / 2; y1 = np.cross(p, x1); cio = x1 * np.cos(s) - y1 * np.sin(s)                          # the non-rotating origin (s is 0.2 arcsec here)
    du = (jd_tt - DT) - 2451545.0; era = 2 * np.pi * ((0.7790572732640 + 1.00273781191135448 * du) % 1.0)               # Earth rotation angle from UT1
    xg = cio * np.cos(era) + np.cross(p, cio) * np.sin(era); return xg, np.cross(p, xg), p, cio, era
def site(lat_d, lon_d, h_m=5.0):
    la, lo = np.radians(lat_d), np.radians(lon_d); e2 = FLAT * (2 - FLAT); N = RE_KM / np.sqrt(1 - e2 * np.sin(la) ** 2); h = h_m / 1000
    return np.array([(N + h) * np.cos(la) * np.cos(lo), (N + h) * np.cos(la) * np.sin(lo), (N * (1 - e2) + h) * np.sin(la)]) / AU
def look(jd_tt, xyz, k=K_IAU):
    """separation of the Moon's and Sun's centres seen from the site, and their angular radii (rad)"""
    xg, yg, p, _, _ = frame(jd_tt); O = st(E, jd_tt) + xyz[0] * xg + xyz[1] * yg + xyz[2] * p
    tS = 0.0058; tM = 1.5e-5
    for _ in range(3): dS = st(S, jd_tt - tS) - O; tS = np.linalg.norm(dS) / C; dM = st(M, jd_tt - tM) - O; tM = np.linalg.norm(dM) / C
    th = np.arccos(np.clip(dS @ dM / np.linalg.norm(dS) / np.linalg.norm(dM), -1, 1)); return th, np.arcsin(RSUN / np.linalg.norm(dS)), np.arcsin(k * RE_KM / AU / np.linalg.norm(dM)), dS, (xg, yg, p)
def contacts(xyz, k=K_IAU, t0=None):
    t0 = t0 if t0 is not None else JD[0] + 0.3; ts = np.arange(t0, JD[-1] - 0.3, 20 / 86400.0); f = np.array([look(t, xyz, k)[:3] for t in ts])
    i = f[:, 0].argmin(); tmid = ts[i]
    def root(g, lo, hi):
        for _ in range(60):
            mid = (lo + hi) / 2
            if (g(lo) > 0) == (g(mid) > 0): lo = mid
            else: hi = mid
        return (lo + hi) / 2
    um = lambda t: (lambda r: r[0] - (r[2] - r[1]))(look(t, xyz, k)); pe = lambda t: (lambda r: r[0] - (r[2] + r[1]))(look(t, xyz, k))
    for _ in range(40):                                           # refine the instant of least separation
        tmid = min((tmid - 1 / 86400.0, tmid, tmid + 1 / 86400.0), key=lambda t: look(t, xyz, k)[0])
    out = {'mid': tmid, 'min_sep': look(tmid, xyz, k)[0], 'total': um(tmid) < 0}
    out['c1'], out['c4'] = root(pe, tmid - 0.09, tmid), root(pe, tmid, tmid + 0.09)
    if out['total']: out['c2'], out['c3'] = root(um, tmid - 0.004, tmid), root(um, tmid, tmid + 0.004)
    return out
def hms(x_days):
    s = (x_days % 1.0) * 86400; return f'{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{s % 60:04.1f}'
def clocks(jd_tt, lon_d, xyz):
    """UT, local mean time, Bangkok mean time (100d30'E), and local apparent solar time (the Sun's own hour angle at the site)"""
    ut = jd_tt - DT + 0.5; th, sS, sM, dS, (xg, yg, p) = look(jd_tt, xyz); _, _, _, cio, era = frame(jd_tt)
    u = dS / np.linalg.norm(dS); u = u + VE(jd_tt) / C; u /= np.linalg.norm(u)            # aberration: the Sun is seen ~20 arcsec behind, which is 1.3 s of apparent time
    ra = np.arctan2(u @ np.cross(p, cio), u @ cio); ha = (era + np.radians(lon_d) - ra + np.pi) % (2 * np.pi) - np.pi
    return ut, ut + lon_d / 360.0, ut + 100.5 / 360.0, 0.5 + ha / (2 * np.pi)
def axis_ground(jd_tt):
    """where the line from the Sun's centre through the Moon's meets the ellipsoid: geodetic latitude, longitude (deg), or None"""
    xg, yg, p, _, _ = frame(jd_tt); e = st(E, jd_tt); tM = np.linalg.norm(st(M, jd_tt) - e) / C; m = st(M, jd_tt - tM); tS = tM + np.linalg.norm(m - st(S, jd_tt)) / C; s_ = st(S, jd_tt - tS)
    u = (m - s_) / np.linalg.norm(m - s_); B = np.array([xg, yg, p]); q = B @ (m - e) * AU; d = B @ u; sc = np.array([1, 1, 1 / (1 - FLAT)]); q2, d2 = q * sc, d * sc
    b = q2 @ d2; c = q2 @ q2 - RE_KM ** 2; disc = b * b - (d2 @ d2) * c
    if disc < 0: return None
    lam = (-b - np.sqrt(disc)) / (d2 @ d2); g = q + lam * d; lon = np.degrees(np.arctan2(g[1], g[0])); e2 = FLAT * (2 - FLAT); lat = np.degrees(np.arctan2(g[2], (1 - e2) * np.hypot(g[0], g[1]))); return lat, lon
def km_between(a, b): return np.hypot((a[0] - b[0]) * 110.6, (a[1] - b[1]) * 111.3 * np.cos(np.radians((a[0] + b[0]) / 2)))
if __name__ == '__main__':
    print('states', n, 'epochs from JD', JD[0], 'to', JD[-1], '(TT); pole rows', len(L))
    ev = eclipse2.find('/home/agent1/orrery/states_1868.txt')
    for jd, g in ev: print(f'geocentric greatest eclipse: {eclipse2.cal(jd)} TT (JD {jd:.6f}), gamma {g:+.4f}')
    SITES = (('French camp (Stephan): 11d42\'35"N, 99d47\'44"E', 11 + 42 / 60 + 35 / 3600, 99 + 47 / 60 + 44 / 3600), ("the King's computed point: 11d41'40\"N, 99d41'E", 11 + 41 / 60 + 40 / 3600, 99 + 41 / 60),
             ("the King's invitation to Ord: 11d39'N, 99d42'E", 11 + 39 / 60, 99.7))
    for name, lat, lon in SITES:
        xyz = site(lat, lon); c = contacts(xyz); print(f'\n{name}')
        if not c['total']: print('   not total here'); continue
        for key, lab in (('c1', 'first contact'), ('c2', 'totality begins'), ('mid', 'least separation'), ('c3', 'totality ends'), ('c4', 'last contact')):
            ut, lmt, bmt, lat_ = clocks(c[key], lon, xyz); print(f'   {lab:17s} UT {hms(ut)}   local mean time {hms(lmt)}   Bangkok mean time {hms(bmt)}   local apparent time {hms(lat_)}')
        d1 = (c['c3'] - c['c2']) * 86400; c_s = contacts(xyz, K_SMALL, c['mid'] - 0.2); d2 = (c_s['c3'] - c_s['c2']) * 86400
        th, sS, sM, dS, (xg, yg, p) = look(c['mid'], xyz); alt = np.degrees(np.arcsin((dS / np.linalg.norm(dS)) @ (xyz[0] * xg + xyz[1] * yg + xyz[2] * p) / np.linalg.norm(xyz)))
        print(f'   duration of totality {int(d1 // 60)} m {d1 % 60:04.1f} s (IAU lunar radius); {int(d2 // 60)} m {d2 % 60:04.1f} s (smaller radius); least separation {np.degrees(c["min_sep"]) * 3600:.1f} arcsec; Sun about {alt:.0f} deg up (geocentric zenith)')
        # nearest point of the central line
        best = min(((km_between((lat, lon), g), t, g) for t in np.arange(c['mid'] - 0.004, c['mid'] + 0.004, 0.5 / 86400.0) for g in [axis_ground(t)] if g), key=lambda r: r[0])
        print(f'   nearest point of the central line: {best[2][0]:.4f} N, {best[2][1]:.4f} E, {best[0]:.1f} km away' + (', the line passing to the ' + ('north' if best[2][0] > lat else 'south')))
    print('\nthe central line near the west coast of the Gulf: ' + '; '.join(f'{g[1]:.3f}E {g[0]:.3f}N' for t in np.arange(ev[0][0] - 0.0075, ev[0][0] - 0.0035, 0.0005) for g in [axis_ground(t)] if g))
