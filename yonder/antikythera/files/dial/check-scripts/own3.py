"""Fresh reader, part 3: every full moon of cycles 0-3 classed umbral or not with the Moon's distance estimated
from its angular speed (areal law), instead of the flat 1.0 deg; and which fall in unmarked months."""
import sys, math
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
D = sys.argv[1]
def read(path):
    jd, lon, lat = [], [], []; on = False
    for line in open(path, encoding='utf-8', errors='replace'):
        if line.startswith('$$SOE'): on = True; continue
        if line.startswith('$$EOE'): break
        if on:
            p = line.split(','); jd.append(float(p[0])); lon.append(float(p[5])); lat.append(float(p[6]))
    return np.array(jd), np.array(lon), np.array(lat)
lunar = [2, 8, 14, 20, 26, 32, 37, 43, 49, 55, 61, 67, 73, 79, 84, 90, 96, 102, 108, 114, 120, 125, 131, 137, 143, 149, 155, 161, 167, 172, 178, 184, 190, 196, 202, 208, 214, 219]
def classify(w, nmonths, label_cells):
    mj, ml, mb = read(f'{D}/moon_{w}.txt'); sj, sl, sb = read(f'{D}/sun_{w}.txt')
    M = CubicSpline(mj, np.degrees(np.unwrap(np.radians(ml)))); S = CubicSpline(sj, np.degrees(np.unwrap(np.radians(sl)))); B = CubicSpline(mj, mb)
    E = lambda t: M(t) - S(t)
    e = E(mj); k = math.ceil((e[0] - 180) / 360); out = []
    n = 1
    while 180 + 360 * k < e[-1] and n <= nmonths:
        tgt = 180 + 360 * k; i = np.searchsorted(e, tgt)
        t = brentq(lambda x: E(x) - tgt, mj[i - 1], mj[i], xtol=1e-7)
        b = float(B(t)); vm = float(M(t, 1)); vs = float(S(t, 1)); vb = float(B(t, 1))
        par = 0.9507 / (math.sqrt(13.17640 * 0.99849 / math.hypot(vm, vb)) * 1.0025)
        ssun = 0.2666 * math.sqrt(vs / 0.98565)
        lim_u = 1.02 * (par + 0.0024 - ssun) + 0.2725 * par
        least = abs(b) * (vm - vs) / math.hypot(vm - vs, vb)
        out.append((n, t, b, par, lim_u, least)); n += 1; k += 1
    return out
then = classify('then', 892, None)
pars = [x[3] for x in then]
print('parallax estimates over 892 full moons: min %.3f max %.3f mean %.3f (true range about 0.899 to 1.025, mean 0.951)' % (min(pars), max(pars), sum(pars) / len(pars)))
for j in range(4):
    rows = [x for x in then if 223 * j < x[0] <= 223 * j + 223]
    um = [(x[0] - 223 * j, round(x[2], 2), round((x[4] - x[5]) / (2 * 0.2725 * x[3]), 2)) for x in rows if x[5] < x[4]]
    marg = [u for u in um if abs(u[2]) < 0.06] + [(x[0] - 223 * j, round(x[2], 2), round((x[4] - x[5]) / (2 * 0.2725 * x[3]), 2)) for x in rows if 0 <= x[5] - x[4] < 0.06 * 2 * 0.2725 * x[3]]
    print(f'cycle {j}: umbral full moons by distance-aware limit: {len(um)}; in a lunar glyph month: {sum(u[0] in lunar for u in um)}; unmarked: {[u for u in um if u[0] not in lunar]}; within 0.06 magnitude of the edge (month, lat, magnitude): {marg}')
    flat = [x[0] - 223 * j for x in rows if abs(x[2]) < 1.0]
    print(f'         flat 1.0 deg proxy: {len(flat)}; classed differently by the two: {sorted(set(flat) ^ set(u[0] for u in um))}')
# check the estimate on modern eclipses with known umbral magnitudes: 2026-08-28 partial 0.930; 2023-10-28 partial 0.122; 2021-11-19 partial 0.974; 2019-07-16 partial 0.653; 2024-09-18 partial 0.085; 2017-08-07 partial 0.246; 2012-06-04 partial 0.370; 2013-04-25 partial 0.015
now = classify('now', 940, None)
known = {2461280.67: 0.930, 2460245.34: 0.122, 2459537.88: 0.974, 2458681.40: 0.653, 2460571.61: 0.085, 2457973.26: 0.246, 2456082.96: 0.370, 2456408.34: 0.015}
for jd0, mag in known.items():
    x = min(now, key=lambda r: abs(r[1] - jd0))
    print('  modern check: JD %.2f (dt %.2f) lat %+.3f parallax est %.3f my umbral magnitude %+.3f catalogue (from memory) %.3f' % (x[1], x[1] - jd0, x[2], x[3], (x[4] - x[5]) / (2 * 0.2725 * x[3]), mag))
