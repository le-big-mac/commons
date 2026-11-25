"""Second reader, step 11: when cycle 122 ended (new moon of month 27429), from the modern JPL tables. usage: run11.py JPLDIR"""
import sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cat2
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
JPL = sys.argv[1]
def read_h(path):
    jd, lon = [], []; on = False
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.startswith('$$SOE'): on = True; continue
            if line.startswith('$$EOE'): break
            if on:
                p = line.split(','); jd.append(float(p[0])); lon.append(float(p[5]))
    return np.array(jd), np.array(lon)
mj, ml = read_h(os.path.join(JPL, 'moon_now.txt')); sj, sl = read_h(os.path.join(JPL, 'sun_now.txt'))
fm = CubicSpline(mj, np.unwrap(np.radians(ml))); fs = CubicSpline(sj, np.unwrap(np.radians(sl)))
el = lambda t: (fm(t) - fs(t))
K0 = json.load(open(os.path.join(HERE, 'k0.json')))['K0']
for n, lab in ((27429, 'last month of cycle 122'), (27430, 'first month of cycle 123'), (27207, 'first month of cycle 122')):
    kf = K0 + 0.5 + (n - 1); kn = kf + 0.5
    for k, what in ((kf, 'full moon'), (kn, 'new moon')):
        t0 = cat2.mean_phase_jde(k)
        target = np.pi if what == 'full moon' else 0.0
        g = lambda t: ((el(t) - target + np.pi) % (2 * np.pi)) - np.pi
        t = brentq(g, t0 - 1.0, t0 + 1.0)
        # Gregorian date
        z = int(np.floor(t + 0.5)); a = int((z - 1867216.25) // 36524.25); A = z + 1 + a - a // 4; B = A + 1524; C = int((B - 122.1) // 365.25); D = int(np.floor(365.25 * C)); E = int((B - D) // 30.6001)
        day = B - D - int(np.floor(30.6001 * E)); mon = E - 1 if E < 14 else E - 13; yr = C - 4716 if mon > 2 else C - 4715
        print(f'{lab} (month {n}) {what}: JD {t:.3f} TT = {yr}-{mon:02d}-{day:02d} {((t + 0.5) % 1) * 24:.1f}h TT')
