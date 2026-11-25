"""The mechanism as ideal gears, and the rulers that compare it with a sky.

A sky is a dict: sky[window][body] = dict(jd=..., S=..., T=..., lat=...) with window in ('then', 'now'),
longitudes in degrees: S along the fixed ecliptic of J2000 (against the stars), T along the ecliptic of date
from the equinox of date (against the seasons); lat is the latitude of date (used for the Moon's node only).

Models (all angles in degrees, tau in days from the window's reference instant):
  eccentric  lam = L + q(L - A; e),  q(a; e) = atan2(-e sin a, 1 + e cos a)   (Sun, Moon; A is the apogee)
  inferior   lam = arg( exp(i Ls) + rho exp(i (Ls + g)) )                      (Mercury, Venus; Ls the mean Sun)
  superior   lam = arg( exp(i L)  + rho exp(i Ls) )                            (Mars, Jupiter, Saturn)
"""
import numpy as np
from scipy.optimize import least_squares
import gears

D2R = np.pi / 180.0
EPS0 = 23.4392911 * D2R
BODIES = ('sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn')
PERIOD0 = {'sun': 365.2564, 'moon': 27.32166, 'apsides': 3232.6, 'mercury': 115.8775, 'venus': 583.9214,
           'mars': 686.980, 'jupiter': 4332.59, 'saturn': 10759.2}       # starting values only; the fits are free
RHO0 = {'mercury': 0.387, 'venus': 0.723, 'mars': 1 / 1.524, 'jupiter': 1 / 5.203, 'saturn': 1 / 9.537}


def wrap(x):
    return (np.asarray(x) + 180.0) % 360.0 - 180.0


def read(path):
    """A Horizons observer table (JD TT, astrometric RA/Dec ICRF, ecliptic longitude/latitude of date)."""
    rows, on = [], False
    for line in open(path, encoding='utf-8', errors='replace'):
        if line.startswith('$$SOE'): on = True; continue
        if line.startswith('$$EOE'): break
        if on:
            p = [s.strip() for s in line.split(',')]
            rows.append((float(p[0]), float(p[3]), float(p[4]), float(p[5]), float(p[6])))
    a = np.array(rows)
    ra, de = a[:, 1] * D2R, a[:, 2] * D2R
    lam = np.arctan2(np.sin(ra) * np.cos(EPS0) + np.tan(de) * np.sin(EPS0), np.cos(ra)) / D2R % 360.0
    return dict(jd=a[:, 0], S=lam, T=a[:, 3] % 360.0, lat=a[:, 4])


def q(a, e):
    a = np.asarray(a) * D2R
    return np.arctan2(-e * np.sin(a), 1 + e * np.cos(a)) / D2R


def m_ecc(L, A, e):
    return L + q(L - A, e)


def m_inf(Ls, g, rho):
    return np.angle(np.exp(1j * Ls * D2R) + rho * np.exp(1j * (Ls + g) * D2R)) / D2R


def m_sup(L, Ls, rho):
    return np.angle(np.exp(1j * L * D2R) + rho * np.exp(1j * Ls * D2R)) / D2R


def _best(fun, starts):
    best = None
    for x0 in starts:
        r = least_squares(fun, x0, x_scale='jac')
        if best is None or r.cost < best.cost: best = r
    return best


def stats(res):
    return dict(rms=float(np.sqrt(np.mean(res ** 2))), max=float(np.max(np.abs(res))), mean=float(np.mean(res)))


def fit_sun(jd, lam, tref):
    """Free fit: mean longitude L0 + r tau, eccentricity e, apogee A (fixed over the window)."""
    tau = jd - tref
    r0 = 360.0 / PERIOD0['sun']
    i0 = np.argmin(np.abs(tau))
    def fun(x):
        L0, r, e, A = x
        return wrap(m_ecc(L0 + r * tau, A, e) - lam)
    starts = [(lam[i0], r0, 0.034, A) for A in range(0, 360, 45)]
    b = _best(fun, starts)
    L0, r, e, A = b.x
    if e < 0: e, A = -e, A + 180.0
    return dict(L0=L0 % 360.0, r=r, e=e, A=A % 360.0, res=fun(b.x), tref=tref)


def fit_moon(jd, lam, tref):
    """Free fit: mean longitude L0 + r tau; apogee A0 + rA tau; eccentricity e."""
    tau = jd - tref
    r0, rA0 = 360.0 / PERIOD0['moon'], 360.0 / PERIOD0['apsides']
    i0 = np.argmin(np.abs(tau))
    def fun(x):
        L0, r, e, A0, rA = x
        return wrap(m_ecc(L0 + r * tau, A0 + rA * tau, e) - lam)
    # the rate must be found first on a short stretch, or the phase runs away over 76 years
    short = np.abs(tau) < 400.0
    def fun_s(x):
        L0, r, e, A0, rA = x
        return wrap(m_ecc(L0 + r * tau[short], A0 + rA * tau[short], e) - lam[short])
    best = None
    for dL in (0.0,):
        for A in range(0, 360, 45):
            rs = least_squares(fun_s, (lam[i0] + dL, r0, 0.11, A, rA0), x_scale='jac')
            for span in (2000.0, 8000.0, 1e9):          # widen the stretch step by step
                m = np.abs(tau) < span
                f = lambda x, m=m: wrap(m_ecc(x[0] + x[1] * tau[m], x[3] + x[4] * tau[m], x[2]) - lam[m])
                rs = least_squares(f, rs.x, x_scale='jac')
            if best is None or rs.cost < best.cost: best = rs
    L0, r, e, A0, rA = best.x
    if e < 0: e, A0 = -e, A0 + 180.0
    return dict(L0=L0 % 360.0, r=r, e=e, A0=A0 % 360.0, rA=rA, res=fun(best.x), tref=tref)


def fit_planet(name, jd, lam, tref, sun):
    """Free fit of the epicycle model. Inferior: epicycle phase g0 + r tau on the mean Sun. Superior: deferent
    longitude L0 + r tau, epicycle along the mean Sun. rho is the epicycle's radius over the deferent's."""
    tau = jd - tref
    Ls = sun['L0'] + sun['r'] * (jd - sun['tref'])
    r0 = 360.0 / PERIOD0[name]
    inferior = name in gears.INFERIOR
    def model(x, m=slice(None)):
        p0, r, rho = x
        ph = p0 + r * tau[m]
        return m_inf(Ls[m], ph, rho) if inferior else m_sup(ph, Ls[m], rho)
    best = None
    for p0 in range(0, 360, 15):
        x = np.array([float(p0), r0, RHO0[name]])
        for span in (1500.0, 6000.0, 1e9):
            m = np.abs(tau) < span
            x = least_squares(lambda y, m=m: wrap(model(y, m) - lam[m]), x, x_scale='jac').x
        c = np.sum(wrap(model(x) - lam) ** 2)
        if best is None or c < best[0]: best = (c, x)
    p0, r, rho = best[1]
    if rho < 0: rho, p0 = -rho, p0 + 180.0
    return dict(p0=p0 % 360.0, r=r, rho=rho, res=wrap(model(best[1]) - lam), tref=tref, inferior=inferior)


def kepler_pos(L, e, w, a=1.0):
    """Heliocentric position (complex, in the plane) on an ellipse: mean longitude L, perihelion w (degrees)."""
    M = (np.asarray(L) - w) * D2R
    E = M.copy()
    for _ in range(10): E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    v = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    return a * (1 - e * np.cos(E)) * np.exp(1j * (v + w * D2R))


def kfit_sun(jd, lam, sun):
    """The sky's Earth as an ellipse (for the sky's own mean motions, not for the mechanism): heliocentric mean
    longitude L0 + r tau, eccentricity e, perihelion w. Started from the eccentric fit `sun`."""
    tau = jd - sun['tref']
    def fun(x):
        L0, r, e, w = x
        return wrap(np.angle(-kepler_pos(L0 + r * tau, abs(e), w)) / D2R - lam)
    b = least_squares(fun, (sun['L0'] + 180.0, sun['r'], sun['e'] / 2, sun['A']), x_scale='jac')
    L0, r, e, w = b.x
    if e < 0: e, w = -e, w + 180.0
    return dict(L0=L0 % 360.0, r=r, e=e, w=w % 360.0, res=fun(b.x), tref=sun['tref'])


def kfit_planet(name, jd, lam, earth, circ, sun):
    """The sky's planet as an ellipse seen from the sky's Earth-ellipse: heliocentric mean longitude L0 + r tau,
    eccentricity e, perihelion w, semi-major axis a. Started from the circle fit `circ`."""
    tau = jd - earth['tref']
    E = kepler_pos(earth['L0'] + earth['r'] * tau, earth['e'], earth['w'])
    if circ['inferior']: L0, r, a0 = sun['L0'] + circ['p0'], sun['r'] + circ['r'], circ['rho']
    else: L0, r, a0 = circ['p0'], circ['r'], 1.0 / circ['rho']
    def fun(x):
        l0, rr, e, w, a = x
        return wrap(np.angle(kepler_pos(l0 + rr * tau, min(abs(e), 0.6), w, a) - E) / D2R - lam)
    best = None
    for e0 in (0.05, 0.2):
        for w0 in range(0, 360, 45):
            b = least_squares(fun, (L0, r, e0, float(w0), a0), x_scale='jac')
            if best is None or b.cost < best.cost: best = b
    l0, rr, e, w, a = best.x
    if e < 0: e, w = -e, w + 180.0
    return dict(L0=l0 % 360.0, r=rr, e=e, w=w % 360.0, a=a, res=fun(best.x), tref=earth['tref'])


def node(jd, lat, lam, tref):
    """Ascending node: longitude of the Moon where its latitude crosses zero going north; a straight line through
    those longitudes (the true node swings about the mean one)."""
    i = np.where((lat[:-1] < 0) & (lat[1:] >= 0))[0]
    f = -lat[i] / (lat[i + 1] - lat[i])
    t = jd[i] + f * (jd[i + 1] - jd[i])
    lo = lam[i] + f * wrap(lam[i + 1] - lam[i])
    un = np.unwrap(lo * D2R) / D2R
    r, c = np.polyfit(t - tref, un, 1)
    return dict(N0=c % 360.0, r=r, n=len(i), res=un - (c + r * (t - tref)), tref=tref)


def advance(p_then, r_then, p_now, r_now, dt):
    """Total advance of a phase between the two reference instants, in degrees: the fitted phases fix the fraction,
    the mean of the two fitted rates fixes the whole turns."""
    frac = (p_now - p_then) % 360.0
    k = np.round((0.5 * (r_then + r_now) * dt - frac) / 360.0)
    return frac + 360.0 * k


def analyse(sky, frame, out=print):
    """Everything for one frame ('S' against the stars, 'T' against the seasons). Returns a dict of results."""
    R = {}
    tref = {w: 0.5 * (sky[w]['sun']['jd'][0] + sky[w]['sun']['jd'][-1]) for w in ('then', 'now')}
    dt = tref['now'] - tref['then']
    fit = {w: {} for w in ('then', 'now')}
    kep = {w: {} for w in ('then', 'now')}
    for w in ('then', 'now'):
        s = sky[w]
        fit[w]['sun'] = fit_sun(s['sun']['jd'], s['sun'][frame], tref[w])
        fit[w]['moon'] = fit_moon(s['moon']['jd'], s['moon'][frame], tref[w])
        fit[w]['node'] = node(s['moon']['jd'], s['moon']['lat'], s['moon'][frame], tref[w])
        for p in gears.SYNODIC:
            fit[w][p] = fit_planet(p, s[p]['jd'], s[p][frame], tref[w], fit[w]['sun'])
        # the sky's own mean motions: ellipses (a circle fitted to an ellipse over a window that is not a whole
        # number of orbits gives a mean longitude biased by tenths of a degree, differently in each window)
        kep[w]['earth'] = kfit_sun(s['sun']['jd'], s['sun'][frame], fit[w]['sun'])
        for p in gears.SYNODIC:
            kep[w][p] = kfit_planet(p, s[p]['jd'], s[p][frame], kep[w]['earth'], fit[w][p], fit[w]['sun'])
    R['fit'], R['kep'] = fit, kep
    # The span: from the first instant of the first window to the last instant of the second (for the real
    # tables, 1 May 205 BC to 23 Nov 2026). Each fitted mean phase is a straight line within its window; it is
    # read at the window's outer edge.
    ta, tb = sky['then']['sun']['jd'][0], sky['now']['sun']['jd'][-1]
    dt = tb - ta
    kt, kn = kep['then'], kep['now']
    ft, fn = fit['then'], fit['now']
    def adv(p_then, r_then, p_now, r_now):
        return advance(p_then + r_then * (ta - tref['then']), r_then, p_now + r_now * (tb - tref['now']), r_now, dt)
    # turns of b1 over the span: the mean Sun's advance in this frame
    dn = adv(kt['earth']['L0'], kt['earth']['r'], kn['earth']['L0'], kn['earth']['r']) / 360.0
    R['dn'], R['dt'], R['ta'], R['tb'] = dn, dt, ta, tb
    # drift of each phase: what the gears turn it by, less what the sky turned it by (positive: the pointer is ahead)
    drift = {}
    def d(gear, p_then, r_then, p_now, r_now):
        return 360.0 * float(gear) * dn - adv(p_then, r_then, p_now, r_now)
    drift['moon'] = d(gears.MOON, ft['moon']['L0'], ft['moon']['r'], fn['moon']['L0'], fn['moon']['r'])
    drift['apsides'] = d(gears.APSIDES, ft['moon']['A0'], ft['moon']['rA'], fn['moon']['A0'], fn['moon']['rA'])
    drift['node'] = d(gears.NODE, ft['node']['N0'], ft['node']['r'], fn['node']['N0'], fn['node']['r'])
    for p in gears.SYNODIC:
        if ft[p]['inferior']:       # epicycle phase: the planet's heliocentric mean longitude less the Earth's
            drift[p] = d(gears.SYNODIC[p], kt[p]['L0'] - kt['earth']['L0'], kt[p]['r'] - kt['earth']['r'],
                         kn[p]['L0'] - kn['earth']['L0'], kn[p]['r'] - kn['earth']['r'])
        else:                       # deferent: the planet's heliocentric mean longitude
            drift[p] = d(1 - gears.SYNODIC[p], kt[p]['L0'], kt[p]['r'], kn[p]['L0'], kn[p]['r'])
    # the Sun's mean longitude advance itself (for the precession: frame T less frame S)
    R['sun_advance'] = 360.0 * dn
    R['drift'] = drift
    R['years'] = dt / 365.25
    return R


def pointer_now(R, sky, frame):
    """The mechanism calibrated in the 'then' window (phases and sizes from the free fit there), turned by the gears
    with the mean Sun kept true, read in the 'now' window. Returns the error series (pointer minus sky) per body."""
    ft = R['fit']['then']
    ta, tb, dn0 = R['ta'], R['tb'], R['dn']
    kn = R['kep']['now']['earth']
    def turns(jd):          # turns of b1 since the first instant of the first window
        return dn0 + kn['r'] * (jd - tb) / 360.0
    def at_start(p, r, f):  # a calibrated phase read at that first instant
        return p + r * (ta - f['tref'])
    err = {}
    cal = dict(sunL=at_start(ft['sun']['L0'], ft['sun']['r'], ft['sun']),
               moonL=at_start(ft['moon']['L0'], ft['moon']['r'], ft['moon']),
               moonA=at_start(ft['moon']['A0'], ft['moon']['rA'], ft['moon']))
    for p in gears.SYNODIC: cal[p] = at_start(ft[p]['p0'], ft[p]['r'], ft[p])
    s = sky['now']
    jd = s['sun']['jd']; n = turns(jd)
    Ls = cal['sunL'] + 360.0 * n
    err['sun'] = wrap(m_ecc(Ls, ft['sun']['A'], ft['sun']['e']) - s['sun'][frame])
    jd = s['moon']['jd']; n = turns(jd)
    L = cal['moonL'] + 360.0 * float(gears.MOON) * n
    A = cal['moonA'] + 360.0 * float(gears.APSIDES) * n
    err['moon'] = wrap(m_ecc(L, A, ft['moon']['e']) - s['moon'][frame])
    for p in gears.SYNODIC:
        jd = s[p]['jd']; n = turns(jd)
        Ls = cal['sunL'] + 360.0 * n
        if ft[p]['inferior']:
            g = cal[p] + 360.0 * float(gears.SYNODIC[p]) * n
            lam = m_inf(Ls, g, ft[p]['rho'])
        else:
            L = cal[p] + 360.0 * float(1 - gears.SYNODIC[p]) * n
            lam = m_sup(L, Ls, ft[p]['rho'])
        err[p] = wrap(lam - s[p][frame])
    return err
