"""Second reader, step 8: the README's sensitivity sentence (limits) by my own syzygies; months 37/38, 125/126, 172/173 in the catalogue.
usage: run8.py JPLDIR IJPAPER CATDIR [CATDIR...]"""
import sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cat2, lists2
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
JPL, PAPER, CATS = sys.argv[1], sys.argv[2], sys.argv[3:]
K0 = json.load(open(os.path.join(HERE, 'k0.json')))['K0']
FL, FS, info, _ = lists2.freeth()
def read_h(path):
    jd, lon, lat = [], [], []; on = False
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.startswith('$$SOE'): on = True; continue
            if line.startswith('$$EOE'): break
            if on:
                p = line.split(','); jd.append(float(p[0])); lon.append(float(p[5])); lat.append(float(p[6]))
    return np.array(jd), np.array(lon), np.array(lat)
mj, ml, mb = read_h(os.path.join(JPL, 'moon_then.txt')); sj, sl, sb = read_h(os.path.join(JPL, 'sun_then.txt'))
fm_lon = CubicSpline(mj, np.unwrap(np.radians(ml))); fs_lon = CubicSpline(sj, np.unwrap(np.radians(sl))); fm_lat = CubicSpline(mj, mb)
el = lambda t: fm_lon(t) - fs_lon(t); e0, e1 = el(mj[0]), el(mj[-1])
def roots(phase):
    out = []; m = int(np.ceil((e0 - phase) / (2 * np.pi)))
    while phase + 2 * np.pi * m <= e1:
        out.append(brentq(lambda t: el(t) - phase - 2 * np.pi * m, mj[0], mj[-1], xtol=1e-7)); m += 1
    return np.array(out)
full, new = roots(np.pi), roots(0.0); new = new[new > full[0]]
FM = {i + 1: float(fm_lat(t)) for i, t in enumerate(full)}; NM = {i + 1: float(fm_lat(t)) for i, t in enumerate(new)}
for ln, ls in ((1.4305, 0.5066), (1.376, 0.487), (1.35, 0.478), (1.50, 0.531)):
    print(f'limits {ln} / {ls}: lunar', [sum(abs(FM[223 * j + n]) <= ln for n in FL) for j in range(4)], 'solar', [sum(-ls <= NM[223 * j + n] <= ln for n in FS) for j in range(4)])
print('month 125 full-moon latitude less the limit:', [round(FM[223 * j + 125] - 1.4305, 3) for j in range(4)], '; less 1.376:', round(FM[125] - 1.376, 3))
# amplitude of latitude at syzygy within 2 deg
LE, _, _ = cat2.load('LE', CATS, verbose=False)
LM = {int(round(cat2.k_of(r['jd']) - 0.5)) - K0 + 1: r for r in LE}
for a, b in ((37, 38), (125, 126), (172, 173), (213, 214)):
    for n in (a, b):
        print(f'month {n} lunar, cycles -3..6:', [(LM[223 * j + n]['typ'][0] + f"{LM[223 * j + n]['pmag']:.2f}") if 223 * j + n in LM else '-' for j in range(-3, 7)], '; full-moon latitude cycle 0:', round(FM[n], 2))
