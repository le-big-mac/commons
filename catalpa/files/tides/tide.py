# Predicting a tide gauge from the orrery's Moon and Sun (response method, after Munk & Cartwright 1966).
# The tide-raising potential of degree 2 at a place has three species (long-period, daily, twice-daily); the sea's level is modelled as a
# linear response to each, with a few lags, plus small extras (seasonal, the Sun's daily warming, shallow-water overtones).
# Nothing here knows a tidal "constituent": the Moon's and Sun's distances, declinations and hour angles come from ~/orrery (eph_states.txt, eph_lib.txt).
# Run with python -I: it reads downloaded CSV files (as data only).
import numpy as np, glob, datetime, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
AU = 149597870.7; GMS, GME, GMM = 132712440041.279419, 398600.435507, 4902.800118
TT_UTC = 69.184 / 86400.0            # TT - UTC in days (37 leap seconds + 32.184 s; assumed unchanged through 2026)
J2000 = datetime.datetime(2000, 1, 1, 12)

def load_eph():
    a = np.loadtxt(f'{HERE}/eph_states.txt'); n = len(a) // 3; a = a[:n * 3].reshape(n, 3, 8)
    t = a[:, 0, 0] - 2451545.0; S, E, M = a[:, 0, 2:], a[:, 1, 2:], a[:, 2, 2:]
    L = np.loadtxt(f'{HERE}/eph_lib.txt'); pole = L[:, 4:7] / np.linalg.norm(L[:, 4:7], axis=1)[:, None]
    return t, M - E, S - E, L[:, 0], pole
_EPH = None
def hermite(t, X, tq):
    """cubic Hermite interpolation of states X[:, 0:3] (au) with velocities X[:, 3:6] (au/day) given at times t (days)"""
    h = t[1] - t[0]; i = np.clip(((tq - t[0]) / h).astype(int), 0, len(t) - 2); f = ((tq - t[i]) / h)[:, None]
    p0, v0, p1, v1 = X[i, :3], X[i, 3:], X[i + 1, :3], X[i + 1, 3:]
    return (2 * f ** 3 - 3 * f ** 2 + 1) * p0 + (f ** 3 - 2 * f ** 2 + f) * h * v0 + (-2 * f ** 3 + 3 * f ** 2) * p1 + (f ** 3 - f ** 2) * h * v1

def species(d_utc, lon_east_deg=0.0):
    """d_utc: days from J2000 (UTC).  Returns c0 (real), c1, c2 (complex): the three species of the degree-2 potential, Moon plus Sun,
    in units of the Moon's at its mean distance; and the Moon's distance (km) and declination (deg) for looking at."""
    global _EPH
    if _EPH is None: _EPH = load_eph()
    t, Mx, Sx, tl, pole = _EPH; tt = d_utc + TT_UTC
    m = hermite(t, Mx, tt); s = hermite(t, Sx, tt)
    p = np.stack([np.interp(tt, tl, pole[:, k]) for k in range(3)], 1); p /= np.linalg.norm(p, axis=1)[:, None]
    g = np.cross(p, [0, 0, 1.0]); g /= np.linalg.norm(g, axis=1)[:, None]; q = np.cross(p, g)       # equinox of date, and the third axis
    T = d_utc / 36525.0; gmst = np.radians((280.46061837 + 360.98564736629 * d_utc + 0.000387933 * T * T) % 360.0) + np.radians(lon_east_deg)
    out = []
    for X, k in ((m, 1.0), (s, GMS / GMM)):
        r = np.linalg.norm(X, axis=1); u = X / r[:, None]; ra = np.arctan2((u * q).sum(1), (u * g).sum(1)); sd = (u * p).sum(1); cd = np.sqrt(1 - sd * sd)
        A = k * (384400.0 / AU / r) ** 3; H = gmst - ra
        out.append((A * (3 * sd * sd - 1), A * 2 * sd * cd * np.exp(1j * H), A * cd * cd * np.exp(2j * H)))
    c0, c1, c2 = (out[0][i] + out[1][i] for i in range(3)); rm = np.linalg.norm(m, axis=1) * AU; dm = np.degrees(np.arcsin((m / np.linalg.norm(m, axis=1)[:, None] * p).sum(1)))
    return c0, c1, c2, rm, dm

LAGS = (-4.0, -2.0, 0.0, 2.0, 4.0)
def design(d_utc, lon=0.0, lags=LAGS, extras=True):
    cols = [np.ones_like(d_utc)]
    for lag in lags:
        c0, c1, c2, _, _ = species(d_utc + lag, lon)
        cols += [c0, c1.real, c1.imag, c2.real, c2.imag]
    if extras:
        c0, c1, c2, _, _ = species(d_utc, lon)
        yr = 2 * np.pi * d_utc / 365.2422; day = 2 * np.pi * (d_utc % 1.0)
        cols += [np.cos(yr), np.sin(yr), np.cos(2 * yr), np.sin(2 * yr),                 # seasonal (weather and steric, not gravity)
                 np.cos(day), np.sin(day), np.cos(2 * day), np.sin(2 * day),             # the Sun's daily and twice-daily warming of the air (S1, S2 radiational)
                 (c2 ** 2).real, (c2 ** 2).imag, (c2 ** 3).real, (c2 ** 3).imag,         # shallow-water overtones of the twice-daily tide
                 (c1 * c2).real, (c1 * c2).imag, (c2 * np.conj(c1)).real, (c2 * np.conj(c1)).imag]
    return np.vstack(cols).T

def load_noaa(station, product):
    t, y = [], []
    for fn in sorted(glob.glob(f'{HERE}/data/{station}_{product}_*.csv')):
        for line in open(fn):
            if not line[:2] == '20': continue
            w = line.split(',')
            if len(w) < 2 or w[1].strip() == '': continue
            d = datetime.datetime.strptime(w[0], '%Y-%m-%d %H:%M'); t.append((d - J2000).total_seconds() / 86400.0); y.append(float(w[1]))
    t, y = np.array(t), np.array(y); o = np.argsort(t); t, y = t[o], y[o]; keep = np.r_[True, np.diff(t) > 1e-9]; return t[keep], y[keep]

def when(d): return (J2000 + datetime.timedelta(days=float(d))).strftime('%Y-%m-%d %H:%M')
def day_of(s): return (datetime.datetime.strptime(s, '%Y-%m-%d %H:%M') - J2000).total_seconds() / 86400.0
STATIONS = {'9414290': ('San Francisco', -122.4659), '8518750': ('The Battery, New York', -74.0142), '1612340': ('Honolulu', -157.867)}
