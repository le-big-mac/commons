"""(a) after.py part B redone with own fits; (b) a second way of setting the mechanism (phases and sizes fitted over
the first window with the rates held at the gears' own), and what it shows today; (c) the circle-fit phase at the
window edges beside the sky's mean longitude from conjunction/opposition samples (check1). Frame S.
usage: python -I check5.py"""
import sys, os, math, json
import numpy as np
from fractions import Fraction as F
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import load
FR = 'S'
sky = load.load(); Z = np.load(os.path.join(HERE, 'fits-S.npz'))
R = math.pi / 180
wrap = lambda x: (np.asarray(x) + 180.0) % 360.0 - 180.0
rms = lambda x: float(np.sqrt(np.mean(np.asarray(x) ** 2)))
TA = sky['then']['sun']['jd'][0]; TB = sky['now']['sun']['jd'][-1]; DT = TB - TA; YRS = DT / 365.25
G = dict(moon=F(254, 19), apsides=F(9 * 53, 19 * 223), mercury=F(1513, 480), venus=F(289, 462), mars=F(133, 284), jupiter=F(315, 344), saturn=F(427, 442))
INF = ('mercury', 'venus'); SUP = ('mars', 'jupiter', 'saturn')
ecc = lambda L, A, e: np.degrees(np.angle(e * np.exp(1j * np.asarray(A) * R) + np.exp(1j * np.asarray(L) * R)))
inferior = lambda Ls, g, rho: np.degrees(np.angle(np.exp(1j * Ls * R) * (1 + rho * np.exp(1j * g * R))))
superior = lambda L, Ls, rho: np.degrees(np.angle(np.exp(1j * L * R) + rho * np.exp(1j * Ls * R)))
f = lambda w, b, k: float(Z[f'{w}_{b}_{k}'])
dn = float(Z['dn'])
# drifts (deg per Julian year) from my own check1 output, typed in: frame S
DRIFT = dict(moon=-262.154, apsides=-335.520, mercury=-6.217, venus=14.395, mars=4.720, jupiter=-1.438, saturn=-9.888)

def series_then(b, dph=0.0, dA=0.0):
    s = sky['then'][b]; jd = s['jd']
    if b == 'moon':
        tau = jd - f('then', 'moon', 'tref')
        return wrap(ecc(f('then', 'moon', 'L0') + f('then', 'moon', 'r') * tau + dph, f('then', 'moon', 'A0') + f('then', 'moon', 'rA') * tau + dA, f('then', 'moon', 'e')) - s[FR])
    Ls = f('then', 'sun', 'L0') + f('then', 'sun', 'r') * (jd - f('then', 'sun', 'tref'))
    ph = f('then', b, 'p0') + f('then', b, 'r') * (jd - f('then', b, 'tref')) + dph
    lam = inferior(Ls, ph, f('then', b, 'rho')) if b in INF else superior(ph, Ls, f('then', b, 'rho'))
    return wrap(lam - s[FR])

print('(a) years of gear drift until rms = sqrt(2) x floor (frame S)')
for b in ('moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn'):
    rate = DRIFT[b] / YRS; rateA = DRIFT['apsides'] / YRS if b == 'moon' else 0.0
    f0 = rms(series_then(b))
    lo, hi = 0.0, 1.0
    while rms(series_then(b, rate * hi, rateA * hi)) < math.sqrt(2) * f0: hi *= 2
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if rms(series_then(b, rate * mid, rateA * mid)) < math.sqrt(2) * f0: lo = mid
        else: hi = mid
    # what the rms is after the full span's drift, on the THEN sky (so only the drift differs)
    full = rms(series_then(b, DRIFT[b], DRIFT['apsides'] if b == 'moon' else 0.0))
    print(f'   {b:8s} floor {f0:.3f}; years {0.5 * (lo + hi):8.1f}; phase error then {rate * 0.5 * (lo + hi):+.2f} deg; (rms on the first window\'s sky with the whole span\'s drift put in: {full:.2f})')

print('(b) the mechanism set with the gears\' own rates over the first window (phases at 1 May 205 BC and sizes free; mean Sun true)')
ms_r_then = float(Z['msr_then']); ms_r_now = float(Z['msr_now'])
ms_L_ta = float(Z['msL_then']) + ms_r_then * (TA - float(Z['mst_then']))
def turns_then(jd): return ms_r_then * (jd - TA) / 360.0
def turns_now(jd): return dn + ms_r_now * (jd - TB) / 360.0
res = {}
# Moon
s = sky['then']['moon']; n = turns_then(s['jd'])
L_ta0 = f('then', 'moon', 'L0') + f('then', 'moon', 'r') * (TA - f('then', 'moon', 'tref'))
A_ta0 = f('then', 'moon', 'A0') + f('then', 'moon', 'rA') * (TA - f('then', 'moon', 'tref'))
fun = lambda x: wrap(ecc(x[0] + 360 * float(G['moon']) * n, x[1] + 360 * float(G['apsides']) * n, x[2]) - s[FR])
best = None
for dL in (-8, -4, 0, 4, 8):
    for dA in (-20, -10, 0, 10, 20):
        r = least_squares(fun, [L_ta0 + dL, A_ta0 + dA, f('then', 'moon', 'e')], x_scale='jac')
        if best is None or r.cost < best.cost: best = r
x = best.x
s2 = sky['now']['moon']; n2 = turns_now(s2['jd'])
e_now = wrap(ecc(x[0] + 360 * float(G['moon']) * n2, x[1] + 360 * float(G['apsides']) * n2, x[2]) - s2[FR])
print(f'   moon     in its own window rms {rms(fun(x)):.3f} (free-rate floor {rms(series_then("moon")):.3f}), largest {np.max(np.abs(fun(x))):.2f}; phase at 205 BC differs from the README\'s setting by {float(wrap(x[0] - L_ta0)):+.2f}; today {e_now[-1]:+.2f}; rms to today {rms(e_now):.2f}')
for p in INF + SUP:
    s = sky['then'][p]; n = turns_then(s['jd']); Ls = ms_L_ta + 360.0 * n
    g = float(G[p]) if p in INF else float(1 - G[p])
    p_ta0 = f('then', p, 'p0') + f('then', p, 'r') * (TA - f('then', p, 'tref'))
    mdl = (lambda ph, Ls_, rho: inferior(Ls_, ph, rho)) if p in INF else (lambda ph, Ls_, rho: superior(ph, Ls_, rho))
    fun = lambda x: wrap(mdl(x[0] + 360 * g * n, Ls, x[1]) - s[FR])
    best = None
    for d in (-6, -3, 0, 3, 6):
        r = least_squares(fun, [p_ta0 + d, f('then', p, 'rho')], x_scale='jac')
        if best is None or r.cost < best.cost: best = r
    x = best.x
    s2 = sky['now'][p]; n2 = turns_now(s2['jd']); Ls2 = ms_L_ta + 360.0 * n2
    e_now = wrap(mdl(x[0] + 360 * g * n2, Ls2, x[1]) - s2[FR])
    print(f'   {p:8s} in its own window rms {rms(fun(x)):.3f} (free-rate floor {rms(series_then(p)):.3f}), largest {np.max(np.abs(fun(x))):.2f}; phase at 205 BC differs from the README\'s setting by {float(wrap(x[0] - p_ta0)):+.2f}; size {x[1]:.5f}; today {e_now[-1]:+.2f}; rms to today {rms(e_now):.2f}, largest {np.max(np.abs(e_now)):.1f}')
