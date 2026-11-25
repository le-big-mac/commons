"""Checker's own circle models, free fits ('floor'), calibration at the first instant, turning by the gears, and
the reading today. Nothing imported from mech.py or gears.py. Frame given as argv[1] (S or T).
usage: python -I check2.py S"""
import sys, os, math, json
import numpy as np
from fractions import Fraction as F
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import load

FR = sys.argv[1] if len(sys.argv) > 1 else 'S'
sky = load.load()
R = math.pi / 180
wrap = lambda x: (np.asarray(x) + 180.0) % 360.0 - 180.0
unwrap = lambda x: np.degrees(np.unwrap(np.radians(x)))
rms = lambda x: float(np.sqrt(np.mean(np.asarray(x) ** 2)))
TA = sky['then']['sun']['jd'][0]; TB = sky['now']['sun']['jd'][-1]; DT = TB - TA
G = dict(moon=F(254, 19), apsides=F(9 * 53, 19 * 223),
         mercury=F(1513, 480), venus=F(289, 462), mars=F(133, 284), jupiter=F(315, 344), saturn=F(427, 442))
INF = ('mercury', 'venus'); SUP = ('mars', 'jupiter', 'saturn')
PREC = 360.0 / (25772.0 * 365.25) if FR == 'T' else 0.0     # nominal, for seeds only


# --- models, written afresh ---
def ecc(L, A, e):
    """a body on a circle of radius 1 about a centre displaced e from the observer towards the apogee A:
    direction of  e*exp(iA) + exp(iL)  (degrees)"""
    z = e * np.exp(1j * np.asarray(A) * R) + np.exp(1j * np.asarray(L) * R)
    return np.degrees(np.angle(z))


def inferior(Ls, g, rho):
    """epicycle of radius rho whose centre is the mean Sun at distance 1; g the planet's angle on it from the Sun's line"""
    z = np.exp(1j * Ls * R) * (1 + rho * np.exp(1j * g * R))
    return np.degrees(np.angle(z))


def superior(L, Ls, rho):
    """deferent of radius 1, mean longitude L; epicycle of radius rho whose radius stays parallel to the mean Sun"""
    z = np.exp(1j * L * R) + rho * np.exp(1j * Ls * R)
    return np.degrees(np.angle(z))


def mean_sun(w):
    s = sky[w]['sun']; tref = 0.5 * (s['jd'][0] + s['jd'][-1]); tau = s['jd'] - tref
    y = unwrap(s[FR])
    cols = [np.ones_like(tau), tau]
    for k in (1, 2, 3):
        cols += [np.cos(2 * np.pi * k * tau / 365.2596), np.sin(2 * np.pi * k * tau / 365.2596)]
    A = np.column_stack(cols); c, *_ = np.linalg.lstsq(A, y, rcond=None)
    return dict(L0=c[0], r=c[1], tref=tref)


def fit_sun(w):
    s = sky[w]['sun']; tref = 0.5 * (s['jd'][0] + s['jd'][-1]); tau = s['jd'] - tref; lam = s[FR]
    ms = mean_sun(w)
    best = None
    for A0 in range(0, 360, 30):
        f = lambda x: wrap(ecc(x[0] + x[1] * tau, x[3], x[2]) - lam)
        r = least_squares(f, [ms['L0'], ms['r'], 0.034, float(A0)], x_scale='jac')
        if best is None or r.cost < best.cost: best = r
    L0, r, e, A = best.x
    if e < 0: e, A = -e, A + 180
    return dict(L0=L0, r=r, e=e, A=A % 360, tref=tref, res=wrap(ecc(L0 + r * tau, A, e) - lam))


def fit_moon(w):
    s = sky[w]['moon']; tref = 0.5 * (s['jd'][0] + s['jd'][-1]); tau = s['jd'] - tref; lam = s[FR]
    y = unwrap(lam); sl, ic = np.polyfit(tau, y, 1)
    rA0 = 360.0 / 3232.6 + PREC
    best = None
    f = lambda x: wrap(ecc(x[0] + x[1] * tau, x[3] + x[4] * tau, x[2]) - lam)
    for A0 in range(0, 360, 20):
        # stage 1: only the apogee phase free, others at seeds; stage 2: all free
        f1 = lambda a: wrap(ecc(ic + sl * tau, a[0] + rA0 * tau, 0.11) - lam)
        a = least_squares(f1, [float(A0)], x_scale='jac').x[0]
        r = least_squares(f, [ic, sl, 0.11, a, rA0], x_scale='jac')
        if best is None or r.cost < best.cost: best = r
    L0, r, e, A0, rA = best.x
    if e < 0: e, A0 = -e, A0 + 180
    return dict(L0=L0, r=r, e=e, A0=A0 % 360, rA=rA, tref=tref, res=f([L0, r, e, A0, rA]))


P0 = dict(mercury=87.9691, venus=224.7008, mars=686.9796, jupiter=4332.589, saturn=10759.22)
RHO0 = dict(mercury=0.38, venus=0.72, mars=0.65, jupiter=0.19, saturn=0.105)


def fit_planet(p, w, sun):
    s = sky[w][p]; tref = 0.5 * (s['jd'][0] + s['jd'][-1]); tau = s['jd'] - tref; lam = s[FR]
    Ls = sun['L0'] + sun['r'] * (s['jd'] - sun['tref'])
    if p in INF:
        r0 = 360.0 / P0[p] - 360.0 / 365.256363
        model = lambda x: inferior(Ls, x[0] + x[1] * tau, x[2])
    else:
        r0 = 360.0 / P0[p] + PREC
        model = lambda x: superior(x[0] + x[1] * tau, Ls, x[2])
    best = None
    for ph in range(0, 360, 12):
        m1 = np.abs(tau) < 3000
        x = least_squares(lambda a: wrap(model([a[0], r0, RHO0[p]]) - lam)[m1], [float(ph)], x_scale='jac').x
        r = least_squares(lambda x: wrap(model(x) - lam), [x[0], r0, RHO0[p]], x_scale='jac')
        if best is None or r.cost < best.cost: best = r
    p0, r, rho = best.x
    if rho < 0: rho, p0 = -rho, p0 + 180
    return dict(p0=p0 % 360, r=r, rho=rho, tref=tref, res=wrap(model([p0, r, rho]) - lam))


def advance(p_then, p_now, r_then, r_now):
    frac = (p_now - p_then) % 360.0
    return frac + 360.0 * round((0.5 * (r_then + r_now) * DT - frac) / 360.0)


ms = {w: mean_sun(w) for w in ('then', 'now')}
dn = advance(ms['then']['L0'] + ms['then']['r'] * (TA - ms['then']['tref']), ms['now']['L0'] + ms['now']['r'] * (TB - ms['now']['tref']),
             ms['then']['r'], ms['now']['r']) / 360.0
print(f'frame {FR}: turns of the mean Sun (my harmonic fit) {dn:.5f}')
fit = {w: {} for w in ('then', 'now')}
for w in ('then', 'now'):
    fit[w]['sun'] = fit_sun(w)
    fit[w]['moon'] = fit_moon(w)
    for p in INF + SUP:
        fit[w][p] = fit_planet(p, w, fit[w]['sun'])
print('free fits (floor): then rms, largest | now rms, largest | size then, now (for Sun/Moon also arcsin in degrees)')
for b in ('sun', 'moon') + INF + SUP:
    a, c = fit['then'][b], fit['now'][b]
    sz = (a['e'], c['e']) if 'e' in a else (a['rho'], c['rho'])
    extra = f'  arcsin {math.degrees(math.asin(sz[0])):.4f} | {math.degrees(math.asin(sz[1])):.4f}' if 'e' in a else ''
    print(f'  {b:8s} {rms(a["res"]):7.4f} {np.max(np.abs(a["res"])):7.3f} | {rms(c["res"]):7.4f} {np.max(np.abs(c["res"])):7.3f} | {sz[0]:.5f} {sz[1]:.5f}{extra}')
print(f'  Sun apogee then {fit["then"]["sun"]["A"]:.2f}, now {fit["now"]["sun"]["A"]:.2f}: moved {float(wrap(fit["now"]["sun"]["A"] - fit["then"]["sun"]["A"])):+.2f} deg in this frame')

# --- the mechanism: calibrated at TA from the 'then' free fit, turned by the gears with the mean Sun kept true ---
ft, fn = fit['then'], fit['now']
at = lambda f, key, rk: f[key] + f[rk] * (TA - f['tref'])
def turns(jd): return dn + ms['now']['r'] * (jd - TB) / 360.0
err = {}
jd = sky['now']['sun']['jd']; n = turns(jd)
Ls_ptr = at(ft['sun'], 'L0', 'r') + 360.0 * n
err['sun'] = wrap(ecc(Ls_ptr, ft['sun']['A'], ft['sun']['e']) - sky['now']['sun'][FR])
jdm = sky['now']['moon']['jd']; nm = turns(jdm)
Lm = at(ft['moon'], 'L0', 'r') + 360.0 * float(G['moon']) * nm
Am = at(ft['moon'], 'A0', 'rA') + 360.0 * float(G['apsides']) * nm
err['moon'] = wrap(ecc(Lm, Am, ft['moon']['e']) - sky['now']['moon'][FR])
parts = {}
for p in INF + SUP:
    g = G[p] if p in INF else 1 - G[p]
    ph = at(ft[p], 'p0', 'r') + 360.0 * float(g) * n
    lam = inferior(Ls_ptr, ph, ft[p]['rho']) if p in INF else superior(ph, Ls_ptr, ft[p]['rho'])
    err[p] = wrap(lam - sky['now'][p][FR])
    # taken apart at the last instant, as after2.py does but with my fits
    Ls_now = fn['sun']['L0'] + fn['sun']['r'] * (TB - fn['sun']['tref'])
    ph_now = fn[p]['p0'] + fn[p]['r'] * (TB - fn[p]['tref'])
    mdl = (lambda a, b, c: inferior(b, a, c)) if p in INF else (lambda a, b, c: superior(a, b, c))
    theory = float(wrap(mdl(ph_now, Ls_now, fn[p]['rho']) - sky['now'][p][FR][-1]))
    dph = float(wrap(ph[-1] - ph_now))
    eff = float(wrap(mdl(ph_now + dph, Ls_now, fn[p]['rho']) - mdl(ph_now, Ls_now, fn[p]['rho'])))
    size = float(wrap(mdl(ph_now + dph, Ls_now, ft[p]['rho']) - mdl(ph_now + dph, Ls_now, fn[p]['rho'])))
    parts[p] = (theory, dph, eff, size)
print('the mechanism read over the 76 years to today: mean error, rms about zero, largest, today; rms over floor')
for b in ('sun', 'moon') + INF + SUP:
    e = err[b]
    print(f'  {b:8s} {np.mean(e):9.3f} {rms(e):8.3f} {np.max(np.abs(e)):8.3f} {e[-1]:9.3f}   {rms(e) / rms(ft[b]["res"]):7.2f}')
print('today taken apart: theory (today\'s own best circle fit, residual today); phase of pointer minus today\'s best-fit phase; its effect in full; effect of the old epicycle size; sum')
for p in INF + SUP:
    t, d, e, s = parts[p]
    print(f'  {p:8s} theory {t:+6.2f}  phase {d:+7.2f}  effect {e:+6.2f}  size {s:+6.2f}  sum {t + e + s:+6.2f}   (today {err[p][-1]:+.2f})')
json.dump({b: float(err[b][-1]) for b in err}, open(os.path.join(HERE, f'today-mine-{FR}.json'), 'w'))
np.savez_compressed(os.path.join(HERE, f'fits-{FR}.npz'), **{f'{w}_{b}_{k}': v for w in fit for b in fit[w] for k, v in fit[w][b].items() if k != 'res'}, dn=dn,
                    msr_then=ms['then']['r'], msr_now=ms['now']['r'], msL_then=ms['then']['L0'], msL_now=ms['now']['L0'], mst_then=ms['then']['tref'], mst_now=ms['now']['tref'])
