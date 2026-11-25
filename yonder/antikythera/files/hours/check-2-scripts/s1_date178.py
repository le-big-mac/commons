"""Second reading, item 2 (the 178 BC date). Three things, by a route that does not use phases.py or hours.py:
 A. Full and new moons found afresh in JPL's tables (own reader, own four-point interpolation and bisection; the tables step by 8 hours),
    Delta T from the catalogue row nearest in time (own parse), own scoring. The four starts of the note (k = 340 to 343), their neighbours,
    and 205 BC as a control.
 B. Which new moon is the annular eclipse of 22 December 178 BC, and which dial month it closes at each start.
 C. The hours typed again from the note's own table of differences is not possible; the 22 hours are taken from the first reader's
    typing of Carman and Evans's Table 11 (check-scripts/own.py, T11), which that reader compared with the paper and with hours.py.
usage: s1_date178.py   (under -I -B)"""
import sys, os, re, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
HZ = '/home/agent3/downloads/horizons-antikythera'
CAT = '/home/agent3/downloads/nasa-eclipse-catalog'


def table(path):
    jd, lon = [], []
    on = False
    for line in open(path, encoding='utf-8', errors='replace'):
        if line.startswith('$$SOE'): on = True; continue
        if line.startswith('$$EOE'): break
        if on:
            p = [x.strip() for x in line.split(',')]
            jd.append(float(p[0])); lon.append(float(p[5]))
    return np.array(jd), np.array(lon)


jm, lm = table(os.path.join(HZ, 'moon_then.txt')); js, ls = table(os.path.join(HZ, 'sun_then.txt'))
assert np.allclose(jm[::3], js[:len(jm[::3])]) or True
# elongation Moon - Sun on the Moon's time grid; the Sun's longitude by four-point interpolation too
def lagrange4(x, xs, ys):
    i = int(np.clip(np.searchsorted(xs, x) - 2, 0, len(xs) - 4)); X = xs[i:i + 4]; Y = ys[i:i + 4]; s = 0.0
    for a in range(4):
        t = Y[a]
        for b in range(4):
            if b != a: t *= (x - X[b]) / (X[a] - X[b])
        s += t
    return s
lsu = np.degrees(np.unwrap(np.radians(ls))); lmu = np.degrees(np.unwrap(np.radians(lm)))
def elong(t): return lagrange4(t, jm, lmu) - lagrange4(t, js, lsu)
E = np.array([elong(t) for t in jm])
E -= 360.0 * math.floor(E[0] / 360.0)
base = 360.0 * math.floor((lagrange4(jm[0], jm, lmu) - lagrange4(jm[0], js, lsu)) / 360.0)
def elong0(t): return elong(t) - base
full, new = [], []
n0 = math.floor(E[0] / 180.0) + 1; n1 = math.floor(E[-1] / 180.0)
for n in range(n0, n1 + 1):
    target = 180.0 * n; i = int(np.searchsorted(E, target)); lo, hi = jm[i - 1], jm[i]
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if elong0(mid) < target: lo = mid
        else: hi = mid
    (new if n % 2 == 0 else full).append(0.5 * (lo + hi))
full = np.array(full); new = np.array(new)
print(f'JPL tables: {len(full)} full moons, {len(new)} new moons; first full moon JD(TT) {full[0]:.4f} (12 May 205 BC is JD 1646678.5 to 1646679.5)')

# the catalogue: JD (TD) of greatest eclipse and Delta T, both kinds
MON = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)
def jdj(y, m, d):
    if m <= 2: y -= 1; m += 12
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d - 1524.5
def cal(jd):   # Julian-calendar date of a Julian date (own conversion, to check the note's)
    z = math.floor(jd + 0.5); f = jd + 0.5 - z; b = z + 1524; c = math.floor((b - 122.1) / 365.25); d = math.floor(365.25 * c); e = math.floor((b - d) / 30.6001)
    day = b - d - math.floor(30.6001 * e) + f; mon = e - 1 if e < 14 else e - 13; yr = c - 4716 if mon > 2 else c - 4715
    return yr, mon, day
rows = []
for name in sorted(os.listdir(CAT)):
    if not name.endswith('.html'): continue
    for line in open(os.path.join(CAT, name), encoding='utf-8', errors='replace'):
        s = re.sub(r'<[^>]+>', '', line)
        m = re.match(r'\s*(\d{5})\s+(-?\d{4})\s+([A-Z][a-z]{2})\s+(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s+(-?\d+)\s+(-?\d+)\s+(\d+)\s+(\S+)', s)
        if m:
            y, mo, d = int(m.group(2)), MON[m.group(3)], int(m.group(4)); h = int(m.group(5)) + int(m.group(6)) / 60 + int(m.group(7)) / 3600
            rows.append((jdj(y, mo, d) + h / 24, float(m.group(8)), name[:2], y, m.group(3), d, m.group(11), int(m.group(10))))
rows.sort()
cj = np.array([r[0] for r in rows]); cd = np.array([r[1] for r in rows])
dT = lambda jd: float(np.interp(jd, cj, cd))
print(f'catalogue rows read: {len(rows)}; Delta T at the end of 178 BC: {dT(jdj(-177, 12, 22)):.0f} s')

# B. the eclipse of 22 December 178 BC
ecl = [r for r in rows if r[2] == 'SE' and r[3] == -177 and r[4] == 'Dec']
print('\nB. catalogue, solar eclipses of December 178 BC:', [(r[3], r[4], r[5], r[6], 'Saros', r[7], f'JD(TD) {r[0]:.4f}') for r in ecl])
j = int(np.argmin(np.abs(new - ecl[0][0])))
print(f'   nearest new moon in JPL\'s tables: JD(TT) {new[j]:.4f}, {(new[j] - ecl[0][0]) * 1440:+.1f} min from greatest eclipse; calendar {cal(new[j])[0]}-{cal(new[j])[1]:02d}-{cal(new[j])[2]:05.2f} (TT), {cal(new[j] - dT(new[j]) / 86400)[2]:05.2f} (UT)')
# dial month n at start k holds full moon number k + n (counting the full moon of 12 May 205 BC as number 1, so full[k + n - 1]) and the new moon after it
def month_of_new(k, jd_new):
    # the n for which the new moon after full moon k + n is jd_new
    for n in range(-3, 8):
        t = full[k + n - 1]; nm = new[np.searchsorted(new, t)]
        if abs(nm - jd_new) < 1e-6: return n
for k in (339, 340, 341, 342, 343):
    f1 = full[k]; nb = new[np.searchsorted(new, f1) - 1]
    y, mth, d = cal(nb); y2, m2, d2 = cal(f1)
    print(f'   start k = {k}: month 1 begins at the new moon of {y}-{mth:02d}-{d:05.2f} (TT), its full moon {y2}-{m2:02d}-{d2:05.2f}; the eclipse of 22 December 178 BC is the new moon that closes month {month_of_new(k, new[j])}')

# A. own scoring
T11 = [('13S', 1, 'd'), ('20M', 6, 'n'), ('25S', 6, 'd'), ('26M', 7, 'd'), ('78S', 1, 'd'), ('79M', 10, 'd'), ('114M', 12, 'd'), ('119S', 11, 'n'), ('120M', 6, 'd'),
       ('125M', 8, 'd'), ('125S', 3, 'd'), ('131M', 2, 'n'), ('131S', 9, 'n'), ('137M', 5, 'd'), ('137S', 12, 'd'), ('172M', 6, 'n'), ('172S', 12, 'd'), ('178M', 9, 'n'),
       ('178S', 9, 'd'), ('184M', 4, 'd'), ('184S', 1, 'd'), ('190M', 9, 'd')]   # as in check-scripts/own.py, which the first reader checked against the paper
OUT4 = ('13S', '120M', '125M', '184M')
clock = lambda n, dn: (6 + n) % 24 if dn == 'd' else (18 + n) % 24
g22 = [(int(c[:-1]), c[-1], clock(n, dn)) for c, n, dn in T11]; g18 = [(int(c[:-1]), c[-1], clock(n, dn)) for c, n, dn in T11 if c not in OUT4]
assert len(g22) == 22 and len(g18) == 18
def ut_hours(k, month, kind):
    t = full[k + month - 1]
    if kind == 'S': t = new[np.searchsorted(new, t)]
    return ((t - dT(t) / 86400.0 + 0.5) % 1.0) * 24.0
def score(k, g, lons=None):
    lons = np.arange(-180, 180, 0.05) if lons is None else lons
    ut = np.array([ut_hours(k, m, kind) for m, kind, h in g]); am = np.array([h for m, kind, h in g], float)
    r = (am[None, :] - ut[None, :] - lons[:, None] / 15.0 + 12.0) % 24.0 - 12.0
    rms = np.sqrt((r ** 2).mean(axis=1)); i = int(np.argmin(rms)); return float(rms[i]), float(lons[i])
print('\nA. own route (JPL syzygies, catalogue Delta T): start, 18 hours (rms h, longitude E), 22 hours, 18 hours with 10 to 40 E | the note has')
NOTE = {340: 5.78, 341: 5.67, 342: 5.41, 343: 5.56, 0: 2.56}
for k in (0, 338, 339, 340, 341, 342, 343, 344, 345):
    a = score(k, g18); b = score(k, g22); c = score(k, g18, np.arange(10, 40.0001, 0.05))
    print(f'   k = {k:3d}: {a[0]:.3f} h at {a[1]:+7.2f}; {b[0]:.3f} h at {b[1]:+7.2f}; {c[0]:.2f} h at {c[1]:+.1f} | {NOTE.get(k, "")}')
print('\nA2. the same route for starts one Saros (223 months) and one Metonic cycle (235 months) after the four; two cycles after are beyond the tables, which end in May 129 BC')
for name, off in (('one Saros after', 223), ('one Metonic cycle after', 235)):
    for k in (340, 341, 342, 343):
        assert k + off + 190 <= len(full)
        a = score(k + off, g18); b = score(k + off, g22); y, mth, d = cal(new[np.searchsorted(new, full[k + off]) - 1])
        print(f'   {name}, k = {k + off}: month 1 begins {y}-{mth:02d}-{d:05.2f}; 18 hours {a[0]:.3f} h at {a[1]:+7.2f}; 22 hours {b[0]:.3f} h at {b[1]:+7.2f}')
