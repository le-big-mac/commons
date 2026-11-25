"""After the reader's report (check.md): my own look at its main findings, before changing the text.
usage: after_check.py DATADIR      (run under -I through runpy; reads the Sun and Moon tables)"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, dial, eym, mech
DATA = sys.argv[1]
lunar, solar = dial.glyph_months()
moon = mech.read(os.path.join(DATA, 'moon_then.txt')); sun = mech.read(os.path.join(DATA, 'sun_then.txt'))
sz = dial.syzygies(moon, sun)
FM, NM = dial.number(sz)

# 1. survival.json: where the lines reach half and none
rows = json.load(open(os.path.join(HERE, 'survival.json')))
f = lambda key, v: next(r for r in rows if r[key] <= v)
for key, tot in (('lunar', 38), ('solar', 28)):
    h, z = f(key, tot // 2), f(key, 0)
    print(f'1. {key}: down to half ({tot // 2}) at cycle {h["cycle"]} = {h["years"]:.0f} yr; none at cycle {z["cycle"]} = {z["years"]:.0f} yr')

# 2. the amplitude of latitude at syzygy: least squares for amplitude with the shift free, all syzygies and those near the nodes
def amp(j, near=None):
    best = None
    for s in np.arange(-3, 6.001, 0.01):
        x, y = [], []
        for n in range(1, 224):
            for d, kind in ((FM, 'full'), (NM, 'new')):
                if 223 * j + n in d:
                    m = dial.model_lat(n, kind, s) / dial.INC; t = d[223 * j + n]
                    if near is None or abs(t) < near: x.append(m); y.append(t)
        x, y = np.array(x), np.array(y); a = float(x @ y / (x @ x)); c = float(np.mean((y - a * x) ** 2))
        if best is None or c < best[0]: best = (c, s, a, len(x))
    return best
for j in range(4):
    c, s, a, k = amp(j); c2, s2, a2, k2 = amp(j, 2.0)
    print(f'2. cycle {j}: amplitude {a:.3f} deg (shift {s:+.2f}, rms {np.sqrt(c):.3f}, {k} syzygies); within 2 deg of the ecliptic: {a2:.3f} (shift {s2:+.2f}, {k2} syzygies)')
A = 4.95
print(f'   with {A}: 20 units = {A * np.sin(np.radians(20 * 360 / 446)):.3f} deg, 7 units = {A * np.sin(np.radians(7 * 360 / 446)):.3f} deg')

# 3. new moons within 1.5 deg in cycle 0 that the dial leaves out
out = sorted((NM[n], n) for n in range(1, 224) if abs(NM[n]) < 1.5 and n not in solar)
print(f'3. cycle 0: {len(out)} new moons within 1.5 deg without a solar glyph; latitudes {out[0][0]:+.2f} to {out[-1][0]:+.2f}; north of the ecliptic: {sum(b > 0 for b, n in out)}')

# 4. the counts with other limits
for ln, ls in ((1.35, 0.478), (1.376, 0.487), (dial.LIM_N, dial.LIM_S), (1.50, 0.531)):
    L = [sum(abs(FM[223 * j + n]) <= ln for n in lunar) for j in range(4)]
    S = [sum(-ls <= NM[223 * j + n] <= ln for n in solar) for j in range(4)]
    print(f'4. limits {ln:.3f} / {ls:.3f}: lunar {L}, solar {S}')
for u in (0.9, 1.0, 1.1):
    r = []
    for j in range(4):
        um = [n for n in range(1, 224) if abs(FM[223 * j + n]) < u]
        r.append(f'{sum(n in lunar for n in um)}/{len(um)}' + (f' missed {[n for n in um if n not in lunar]}' if any(n not in lunar for n in um) else ''))
    print(f'4. dark line {u}: {r}')

# 5. the Moon's speed at the full moons of month 126 (a measure of its distance: about 11.8 deg/day at apogee, 15.3 at perigee)
jd = moon['jd']; lon = np.unwrap(np.radians(moon['T'])) * 180 / np.pi
ft = sz['full'][0]
for j in range(4):
    k = 223 * j + 126 - 1; t = ft[k]
    v = (np.interp(t + 0.25, jd, lon) - np.interp(t - 0.25, jd, lon)) / 0.5
    print(f'5. cycle {j}, month 126: full moon JD {t:.2f}, latitude {FM[223 * j + 126]:+.3f}, Moon moving {v:.2f} deg/day')

# 6. the arithmetic against the tables for cycles 0 to 3, with 5.145 and with 4.95 (limits in degrees unchanged)
for inc in (5.145, 4.95):
    Ls, Ss = [], []
    for j in range(4):
        s = 0.75 + 0.58 * j
        Ls.append(sum(abs(dial.model_lat(n, 'full', s)) * inc / dial.INC <= dial.LIM_N for n in lunar))
        Ss.append(sum(-dial.LIM_S <= dial.model_lat(n, 'new', s) * inc / dial.INC <= dial.LIM_N for n in solar))
    print(f'6. arithmetic with amplitude {inc}: lunar {Ls}, solar {Ss}')
# 7. D8's tie
for name, sh in (('dial.survival (shift at the start of the cycle)', lambda j: 0.75 - 0.29 + 0.58 * j), ('dial_after (mid-cycle)', lambda j: 0.75 + 0.58 * j)):
    for j in (12, 13, 14):
        s = sh(j); d = sorted(abs(abs(dial.model_lat(n, 'full', s)) - dial.LIM_N) for n in lunar)[0]
        print(f'7. {name}: cycle {j}, shift {s!r}: {sum(abs(dial.model_lat(n, "full", s)) <= dial.LIM_N for n in lunar)} of 38; nearest month to the limit is {d:.2e} deg from it')
