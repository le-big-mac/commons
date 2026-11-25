# What is the force residual at the year 0 made of?  Fit it with: the Earth-oblateness force itself (a change of J2), its derivative with the pole's tilt, and with the pole's longitude.
# usage: python -I force_fit.py <dir> <start day> <lib file> <label>
import sys, re, os, subprocess, numpy as np
hzdir, d0, libfile, label = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
BODIES = [10, 199, 299, 399, 301, 4, 5, 6, 7, 8, 9]; AU = 149597870.7; GMEM = (398600.435507 + 4902.800118) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247
num = r'([-+]?\d\.\d+E[-+]\d+)'
def hz(p):
    b = open(p).read().split('$$SOE')[1].split('$$EOE')[0]
    return np.array([[float(x) for x in m.groups()] for m in re.finditer(r'(\d+\.\d+) = [AB]\.[DC]\..*?\n\s*X\s*=\s*' + num + r'\s*Y\s*=\s*' + num + r'\s*Z\s*=\s*' + num + r'\s*\n\s*VX=\s*' + num + r'\s*VY=\s*' + num + r'\s*VZ=\s*' + num, b)])
S = [hz(f'{hzdir}/hz_{d0}_{b}.txt') for b in BODIES]; n = len(S[0]); h = 1 / 48.0; jd = S[0][0, 0] + h * np.arange(n); t = jd - 2451545.0
L = np.loadtxt(libfile); L = L[np.argsort(L[:, 0])]; L = L[(L[:, 0] >= t[0] - 1) & (L[:, 0] <= t[-1] + 1)]
rate = np.polyfit(L[:, 0], L[:, 1], 1)[0]; th = np.interp(t, L[:, 0], L[:, 1] - rate * L[:, 0]) + rate * t; pole = np.array([np.interp(t, L[:, 0], L[:, 4 + k]) for k in range(3)]).T
def model(pole_, extra=None, tag='x'):
    inp = f'/tmp/accfit_{d0}_{tag}.txt'
    with open(inp, 'w') as f:
        for i in range(n): f.write(f'{jd[i]:.9f} ' + ' '.join(' '.join(f'{v:.17e}' for v in S[b][i, 1:]) for b in range(11)) + f' {th[i]:.15e} ' + ' '.join(f'{v:.17e}' for v in pole_[i]) + '\n')
    env = dict(os.environ, J2='1', TIDE='195', LFIG='3', POLE='1', CASS='1', K2E='0.30', K2M='0.024', ACCIN=inp); env.update(extra or {})
    A = np.array([[float(x) for x in l.split()] for l in subprocess.run(['./orrery_acc', 'data/ic.txt', '1', '0.05', '2', '1', 'state'], env=env, capture_output=True, text=True, check=True).stdout.strip().split('\n')])
    return A[:, 4:7] - A[:, 1:4]
c = np.array([1 / 280, -4 / 105, 1 / 5, -4 / 5, 0, 4 / 5, -1 / 5, 4 / 105, -1 / 280]); ddt = lambda v: sum(c[k + 4] * v[4 + k:n - 4 + k] for k in range(-4, 5)) / h; sl = slice(4, n - 4)
aj = ddt(S[4][:, 4:7]) - ddt(S[3][:, 4:7]); base = model(pole, tag='base'); r = (S[4][:, 1:4] - S[3][:, 1:4])[sl]; a0 = GMEM / (r * r).sum(1); res = (aj - base[sl]) / a0[:, None]
# basis: change of J2 by a fraction; pole tilted away from the J2000 ecliptic pole by 1 arcsec x k; pole turned about the J2000 ecliptic pole
dJ = (model(pole, {'J2FAC': '1.01'}, 'j2') - base)[sl] / 0.01 / a0[:, None]
z = np.array([0, 0, 1.0]); e_t = pole - (pole @ z)[:, None] * z; e_t /= np.linalg.norm(e_t, axis=1)[:, None]            # horizontal direction of the pole
d = 100 / AS; tilt = pole * np.cos(d) + (e_t * pole[:, 2:3] - z * np.linalg.norm(pole[:, :2], axis=1)[:, None]) * np.sin(d)   # rotate the pole away from z by d
lon = np.stack([pole[:, 0] * np.cos(d) - pole[:, 1] * np.sin(d), pole[:, 0] * np.sin(d) + pole[:, 1] * np.cos(d), pole[:, 2]], 1)
dT = (model(tilt, tag='tilt') - base)[sl] / 100 / a0[:, None]; dL = (model(lon, tag='lon') - base)[sl] / 100 / a0[:, None]          # per arcsec
tot = (res ** 2).sum(); print(f'== {label}: residual rms {np.sqrt(tot / len(res)) * 1e10:.2f}e-10 of the main attraction (all three components)')
def fit(names, cols):
    X = np.stack([c_.ravel() for c_ in cols], 1); coef = np.linalg.lstsq(X, res.ravel(), rcond=None)[0]; left = res.ravel() - X @ coef
    return coef, 1 - (left ** 2).sum() / tot, np.sqrt((left ** 2).sum() / len(res)) * 1e10
B = {'oblateness stronger by a fraction f': dJ, 'pole tilted further from the J2000 ecliptic pole (arcsec)': dT, 'pole turned on about the ecliptic pole (arcsec)': dL}
for k, v in B.items():
    coef, ev, rms = fit([k], [v]); print(f'   {k:58s} alone: {coef[0]:+.4g}   explains {100 * ev:5.1f}% of the variance; residual left {rms:.2f}e-10')
for pair in ((0, 1), (0, 2), (1, 2), (0, 1, 2)):
    ks = [list(B)[i] for i in pair]; coef, ev, rms = fit(ks, [B[k] for k in ks]); print('   ' + ' + '.join(k.split(' (')[0] for k in ks) + ': ' + ', '.join(f'{x:+.4g}' for x in coef) + f'   explains {100 * ev:5.1f}%; left {rms:.2f}e-10')
