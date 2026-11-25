"""Fresh reader, part 2: the later cycles by arithmetic (own code), month 126's eclipse by the Moon's distance,
the 8-8-8-7-7 statement, limits with the amplitude the syzygies actually show."""
import sys, math, json
import numpy as np
from scipy.interpolate import CubicSpline
D = sys.argv[1]
H = '/home/agent3/antikythera/dial'
own = json.load(open(H + '/check-scripts/own.json'))
FM = {int(k): v for k, v in own['FM'].items()}; NM = {int(k): v for k, v in own['NM'].items()}
def glyphs():
    lun, sol = {}, {}
    for n in range(1, 224):
        for kind, off in (('F', 17), ('N', 36)):
            p = (38 * (n - 1) + off) % 446
            dD = (p - 66 + 223) % 446 - 223; dA = (p - 289 + 223) % 446 - 223
            d, node = (dD, 'D') if abs(dD) <= abs(dA) else (dA, 'A')
            if kind == 'F':
                if abs(d) <= 20: lun[n] = d
            else:
                nth = (d <= 0) if node == 'D' else (d >= 0)
                if abs(d) <= (20 if nth else 7): sol[n] = d
    for n in sorted(lun):
        if n in lun and n + 1 in lun: del lun[n + 1]
    return lun, sol
lunar, solar = glyphs()
def mlat(n, kind, s, inc=5.145):
    th = math.radians((38 * (n - 1) + (17 if kind == 'F' else 36) - 66 - s) * 360 / 446)
    return inc * math.sin(th) if kind == 'F' else -inc * math.sin(th)
LN, LS = 5.145 * math.sin(math.radians(20 * 360 / 446)), 5.145 * math.sin(math.radians(7 * 360 / 446))
def run(s_of, inc=5.145, ln=LN, ls=LS, um=1.0, upto=140):
    rows = []
    for j in range(upto + 1):
        lun = sum(abs(mlat(n, 'F', s_of(j, n), inc)) <= ln for n in lunar)
        sol = sum(-ls <= mlat(n, 'N', s_of(j, n), inc) <= ln for n in solar)
        umb = [n for n in range(1, 224) if abs(mlat(n, 'F', s_of(j, n), inc)) < um]
        rows.append((j, lun, sol, len(umb), [n for n in umb if n not in lunar]))
    return rows
def summ(rows, label):
    f = lambda cond: next((r[0] for r in rows if cond(r)), None)
    print(f'{label}\n   cycles 0-3 lunar {[r[1] for r in rows[:4]]} solar {[r[2] for r in rows[:4]]} missed {[len(r[4]) for r in rows[:4]]} | last cycle with >=30 lunar: {max(r[0] for r in rows if r[1] >= 30)}; first <30: {f(lambda r: r[1] < 30)}; first <=19: {f(lambda r: r[1] <= 19)}; first lunar 0: {f(lambda r: r[1] == 0)}; solar first <=14: {f(lambda r: r[2] <= 14)}; first solar 0: {f(lambda r: r[2] == 0)}; first missed >=1,3,5,10: {[f(lambda r, k=k: len(r[4]) >= k) for k in (1, 3, 5, 10)]}; first cycle month 126 missed: {f(lambda r: 126 in r[4])}')
    return rows
a = summ(run(lambda j, n: 0.75 + 0.58 * j), 'A. dial_after.py as written (shift 0.75 + 0.58 j, same for every month of the cycle)')
sj = json.load(open(H + '/survival.json'))
print('   agrees with survival.json on lunar, solar, umbral, missed for all 141 cycles:', all((r['lunar'], r['solar'], r['umbral'], r['umbral_missed']) == (x[1], x[2], x[3], len(x[4])) for r, x in zip(sj, a)))
summ(run(lambda j, n: 0.75 - 0.29 + 0.58 * j), 'B. dial.survival as used for D8 (shift 0.46 + 0.58 j)')
summ(run(lambda j, n: 0.76 - 0.289 + 0.5785 * (j + (n - 1) / 223)), 'C. shift slipping month by month within the cycle (0.471 + 0.5785 (j + (n-1)/223))')
summ(run(lambda j, n: 0.76 - 0.289 + 0.5785 * (j + (n - 1) / 223), inc=4.95), 'D. as C, with the amplitude the near-node syzygies show (4.95) and the README\'s limits in degrees (1.43, 0.51, 1.0)')
print('   counted in the tables, cycles 0-3: lunar [37, 37, 37, 37] solar [27, 26, 25, 25] missed [0, 0, 1, 1]')
print('years: cycle x 18.03:', {c: round(c * 18.03) for c in (12, 13, 20, 30, 31, 45, 62, 63, 64, 65)})
# month-by-month, model (D) against tables for the glyph months near a limit, cycles 0..3
for j in range(4):
    sA = lambda n: 0.75 + 0.58 * j
    bad = [(n, round(mlat(n, 'F', sA(n)), 2), round(FM[223 * j + n], 2)) for n in lunar if (abs(mlat(n, 'F', sA(n))) <= LN) != (abs(FM[223 * j + n]) <= LN)]
    print(f'cycle {j}: lunar glyph months where arithmetic A and tables disagree (month, model lat, true lat):', bad)
# residual true - model(5.145) against model latitude: is the misfit an amplitude?
x = np.array([mlat(n, 'F', 0.76) for n in range(1, 224)] + [mlat(n, 'N', 0.76) for n in range(1, 224)]); y = np.array([FM[n] for n in range(1, 224)] + [NM[n] for n in range(1, 224)])
sel = np.abs(x) < 2
print('cycle 0, syzygies with |model lat| < 2: true = %.3f x model (slope through origin), n=%d; scatter about that line %.3f deg; scatter about slope 1: %.3f' % (np.sum(x[sel] * y[sel]) / np.sum(x[sel] ** 2), sel.sum(), np.std(y[sel] - x[sel] * np.sum(x[sel] * y[sel]) / np.sum(x[sel] ** 2)), np.sqrt(np.mean((y[sel] - x[sel]) ** 2))))
print('limits with amplitude 4.95: 20 units -> %.3f, 7 units -> %.3f' % (4.95 * math.sin(math.radians(20 * 360 / 446)), 4.95 * math.sin(math.radians(7 * 360 / 446))))
for ln, ls in ((1.376, 0.487),):
    for j in range(4): print(f'  limits {ln}/{ls}: cycle {j}: lunar', sum(abs(FM[223 * j + n]) <= ln for n in lunar), 'solar', sum(-ls <= NM[223 * j + n] <= ln for n in solar))

# ---- month 126: is it an umbral eclipse? Moon's parallax from its angular speed (areal law), Sun's radius from the Sun's speed
def read(path):
    jd, lon, lat = [], [], []; on = False
    for line in open(path, encoding='utf-8', errors='replace'):
        if line.startswith('$$SOE'): on = True; continue
        if line.startswith('$$EOE'): break
        if on:
            p = line.split(','); jd.append(float(p[0])); lon.append(float(p[5])); lat.append(float(p[6]))
    return np.array(jd), np.array(lon), np.array(lat)
mj, ml, mb = read(f'{D}/moon_then.txt'); sj_, sl, sb = read(f'{D}/sun_then.txt')
M = CubicSpline(mj, np.degrees(np.unwrap(np.radians(ml)))); S = CubicSpline(sj_, np.degrees(np.unwrap(np.radians(sl)))); B = CubicSpline(mj, mb)
E = lambda t: M(t) - S(t)
from scipy.optimize import brentq
def fm_time(n):   # n-th full moon: E = 180 + 360 (n-1) + E offset
    e0 = E(mj[0]); k0 = math.ceil((e0 - 180) / 360)
    tgt = 180 + 360 * (k0 + n - 1)
    t0 = mj[0] + (tgt - e0) / 12.19
    return brentq(lambda x: E(x) - tgt, t0 - 2, t0 + 2, xtol=1e-7)
print('\nMonth 126 full moons (and others near 1.0): lat, Moon speed, parallax est., umbral radius + Moon radius, least distance, verdict')
for j, m in ((0, 126), (1, 126), (2, 126), (3, 126), (0, 38), (3, 38), (2, 173), (3, 173)):
    t = fm_time(223 * j + m); b = float(B(t)); assert abs(b - FM[223 * j + m]) < 1e-3
    vm = float(M(t, 1)); vs = float(S(t, 1)); vb = float(B(t, 1))
    # areal law: r/a = sqrt(n sqrt(1-e^2)/v), with +0.25% for the variation at syzygy; parallax 0.9507 deg at r = a
    par = 0.9507 / (math.sqrt(13.17640 * 0.99849 / math.hypot(vm, vb)) * 1.0025)
    ssun = 0.2666 * vs / 0.98565 ** 0.5 / 0.98565 ** 0.5 if False else 0.2666 * math.sqrt(vs / 0.98565)
    umb = 1.02 * (par + 0.0024 - ssun); srm = 0.2725 * par
    least = abs(b) * (vm - vs) / math.hypot(vm - vs, vb)
    print(f'  cycle {j} month {m}: JD {t:.2f} lat {b:+.3f} speed {vm:.2f} deg/d parallax {par:.3f} umbra+moon {umb + srm:.3f} (pen. {1.02 * (par + 0.0024 + ssun) + srm:.3f}) least distance {least:.3f} -> umbral magnitude {(umb + srm - least) / (2 * srm):+.3f}')

# ---- "the solar glyphs are a subset of the non-Babylonian pattern 8-8-8-7-7-"
import itertools
def pattern(start, sizes):
    ms, m = [], start
    for g in sizes:
        for i in range(g): ms.append((m - 1) % 223 + 1); m += 6
        m -= 1
    return set(ms)
for name, base in (('8-8-8-7-7', (8, 8, 8, 7, 7)), ('8-8-7-8-7', (8, 8, 7, 8, 7))):
    hits_s = [(s, rot) for s in range(1, 224) for rot in range(5) if set(solar) <= pattern(s, base[rot:] + base[:rot])]
    hits_l = [(s, rot) for s in range(1, 224) for rot in range(5) if set(lunar) == pattern(s, base[rot:] + base[:rot])]
    print(f'pattern {name}: solar glyph months a subset for (start, rotation) in {hits_s}; lunar glyph months equal for {hits_l}')
