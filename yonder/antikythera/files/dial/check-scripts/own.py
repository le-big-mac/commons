"""Fresh reader's own route: syzygies by cubic spline on elongation, month numbers by elongation count,
lunation count across the gap by Meeus's mean-lunation polynomial, model from the paper's words."""
import sys, math
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq, minimize_scalar, least_squares
D = sys.argv[1]

def read(path):
    jd, lon, lat = [], [], []
    on = False
    for line in open(path, encoding='utf-8', errors='replace'):
        if line.startswith('$$SOE'): on = True; continue
        if line.startswith('$$EOE'): break
        if on:
            p = line.split(',')
            jd.append(float(p[0])); lon.append(float(p[5])); lat.append(float(p[6]))
    return np.array(jd), np.array(lon), np.array(lat)

def syz(w):
    mj, ml, mb = read(f'{D}/moon_{w}.txt'); sj, sl, sb = read(f'{D}/sun_{w}.txt')
    assert np.all(np.diff(mj) > 0) and np.all(np.diff(sj) > 0)
    print(w, 'moon rows', len(mj), 'step', np.unique(np.round(np.diff(mj), 6)), 'sun rows', len(sj), 'max |sun lat| deg', np.abs(sb).max())
    mu = np.degrees(np.unwrap(np.radians(ml))); su = np.degrees(np.unwrap(np.radians(sl)))
    S = CubicSpline(sj, su); M = CubicSpline(mj, mu); B = CubicSpline(mj, mb)
    E = lambda t: M(t) - S(t)
    e = E(mj)
    assert np.all(np.diff(e) > 0)
    out = []   # (kind, count index, jd, lat)
    k = math.ceil(e[0] / 180.0)
    while k * 180.0 < e[-1]:
        tgt = k * 180.0
        i = np.searchsorted(e, tgt)
        t = brentq(lambda x: E(x) - tgt, mj[i - 1], mj[i], xtol=1e-7)
        out.append(('new' if k % 2 == 0 else 'full', k, t, float(B(t))))
        k += 1
    return out

def meeus_k(jde):
    """lunation number (k integer = new moon, k+0.5 = full) nearest to jde by Meeus ch. 49 mean phase."""
    k = (jde - 2451550.09766) / 29.530588861
    for _ in range(5):
        T = k / 1236.85
        m = 2451550.09766 + 29.530588861 * k + 0.00015437 * T**2 - 0.000000150 * T**3 + 0.00000000073 * T**4
        k += (jde - m) / 29.530588861
    return k

then, now = syz('then'), syz('now')
f0 = next(s for s in then if s[0] == 'full')
print('first full moon then: JD', round(f0[2], 3), ' = 12 May 205 BC if between 1646678.5 and 1646679.5; lat', round(f0[3], 3))
g0 = next(s for s in now if s[0] == 'full')
print('first full moon now: JD', round(g0[2], 3), ' Meeus k then', round(meeus_k(f0[2]), 3), 'k now', round(meeus_k(g0[2]), 3), 'difference', round(meeus_k(g0[2]) - meeus_k(f0[2]), 3))
gap = round(meeus_k(g0[2]) - meeus_k(f0[2]))
print('simple: (JD diff)/29.530589 =', round((g0[2] - f0[2]) / 29.530589, 3), ' lunations taken:', gap)

def number(sz, first_month):
    kf = next(s for s in sz if s[0] == 'full')[1]
    FM, NM, FT, NT = {}, {}, {}, {}
    for kind, k, t, b in sz:
        if kind == 'full': n = first_month + (k - kf) // 2; FM[n] = b; FT[n] = t
        else:
            n = first_month + (k - 1 - kf) // 2          # the conjunction that follows full moon n
            if k - 1 - kf >= 0: NM[n] = b; NT[n] = t
    return FM, NM, FT, NT
FM, NM, FT, NT = number(then, 1)
FM2, NM2, FT2, NT2 = number(now, 1 + gap)
assert all(0 < NT[n] - FT[n] < 16.5 for n in NT), 'new moon of month n follows its full moon by about half a month'
print('months then:', min(FM), 'to', max(FM), '; now:', min(FM2), 'to', max(FM2), '; last full moon now JD', round(FT2[max(FT2)], 2), '; last new moon month', max(NM2))
# known modern eclipses as a check of the "now" ruler: total lunar 2025 Sep 7 (JD 2460926.26), 2026 Mar 3 (2461102.98), partial 2026 Aug 28 (2461280.67); solar 2026 Aug 12 (2461265.24), 2024 Apr 8 (2460409.26)
for name, jd0, dct, tt in (('lunar 2025-09-07', 2460926.26, FM2, FT2), ('lunar 2026-03-03', 2461102.98, FM2, FT2), ('lunar 2026-08-28', 2461280.67, FM2, FT2), ('solar 2026-08-12', 2461265.24, NM2, NT2), ('solar 2024-04-08', 2460409.26, NM2, NT2)):
    n = min(tt, key=lambda m: abs(tt[m] - jd0)); print('  ', name, 'month', n, 'cell', (n - 1) % 223 + 1, 'dt days', round(tt[n] - jd0, 2), 'lat', round(dct[n], 3))

# ---- the model from the paper's words, coded apart
def my_glyphs(drop='second'):
    lun, sol = {}, {}
    for n in range(1, 224):
        for kind, off in (('F', 17), ('N', 36)):
            p = (38 * (n - 1) + off) % 446
            dD = (p - 66 + 223) % 446 - 223; dA = (p - 289 + 223) % 446 - 223
            d, node = (dD, 'D') if abs(dD) <= abs(dA) else (dA, 'A')
            if kind == 'F':
                if abs(d) <= 20: lun[n] = (d, node)
            else:
                is_north = (d <= 0) if node == 'D' else (d >= 0)   # Sun (and new Moon) before the descending node: Moon north
                if abs(d) <= (20 if is_north else 7): sol[n] = (d, node)
    pairs = [n for n in sorted(lun) if n + 1 in lun]
    for n in pairs:
        if drop == 'second': del lun[n + 1]
        elif drop == 'first': del lun[n]
    return lun, sol, pairs
lunar, solar, pairs = my_glyphs()
print('my model: lunar', len(lunar), 'solar', len(solar), 'glyph months', len(set(lunar) | set(solar)), 'consecutive pairs', pairs, '(223 wraps to 1?', 223 in lunar and 1 in lunar, ')')
sys.path.insert(0, '/home/agent3/antikythera/dial'); sys.path.insert(0, '/home/agent3/antikythera')
import dial, mech
dl, ds = dial.glyph_months()
print('same months as dial.glyph_months():', sorted(dl) == sorted(lunar), sorted(ds) == sorted(solar))
def groups(ms):
    ms = sorted(ms); gaps = [(ms[(i + 1) % len(ms)] - ms[i]) % 223 for i in range(len(ms))]
    g, cur = [], 1
    # rotate so that we start after a 5-gap
    i0 = next(i for i, x in enumerate(gaps) if x != 6) + 1
    order = [(i0 + i) % len(ms) for i in range(len(ms))]
    out, cur = [], 0
    for i in order:
        cur += 1
        if gaps[i] != 6: out.append((cur, gaps[i])); cur = 0
    return out
print('lunar groups (size, gap after):', groups(lunar))
print('  if the FIRST of a pair were dropped:', groups(my_glyphs('first')[0]))
# solar with symmetric limit 20 for pattern
sym = [n for n in range(1, 224) if min(abs(((38 * (n - 1) + 36) % 446 - c + 223) % 446 - 223) for c in (66, 289)) <= 20]
print('new moons within 20 units either side:', len(sym), 'groups', groups(sym), '; model solar a subset:', set(solar) <= set(sym))
print('solar glyph months by side: north', sum(1 for n in solar if (solar[n][0] <= 0) == (solar[n][1] == 'D') or solar[n][0] == 0), 'of', len(solar))

# ---- compare my syzygies with dial.syzygies / dial.number
res = dial.syzygies(mech.read(f'{D}/moon_then.txt'), mech.read(f'{D}/sun_then.txt'))
dFM, dNM = dial.number(res)
print('vs dial.py (then): months', len(FM), len(dFM), len(NM), len(dNM), '; max |lat diff| full', max(abs(FM[n] - dFM[n]) for n in FM if n in dFM), 'new', max(abs(NM[n] - dNM[n]) for n in NM if n in dNM),
      '; max |time diff| full (days)', float(np.max(np.abs(np.array([FT[n] for n in sorted(FT)]) - res['full'][0]))))

INC = 5.145
def lim(u, inc=INC): return inc * math.sin(math.radians(u * 360 / 446))
LN, LS = lim(20), lim(7)
print('limits: 20 units =', round(20 * 360 / 446, 3), 'deg ->', round(LN, 4), '(exact asin form', round(math.degrees(math.asin(math.sin(math.radians(INC)) * math.sin(math.radians(20 * 360 / 446)))), 4), '); 7 units =', round(7 * 360 / 446, 3), '->', round(LS, 4))

def tally(FMx, NMx, base, ln=LN, ls=LS, um=1.0):
    L = sum(abs(FMx[base + n]) <= ln for n in lunar); S = sum(-ls <= NMx[base + n] <= ln for n in solar)
    umb = [n for n in range(1, 224) if base + n in FMx and abs(FMx[base + n]) < um]
    return L, S, len(umb), sum(n in lunar for n in umb), [n for n in umb if n not in lunar]
print('\nRecount, limits 1.43 / -0.51..1.43 / umbral 1.0:')
for j in range(4): print('  cycle', j, tally(FM, NM, 223 * j))
last = max(FM2)
FMr = {(n - 1) % 223 + 1: FM2[n] for n in range(last - 222, last + 1)}; NMr = {(n - 1) % 223 + 1: NM2[n] for n in range(last - 222, last + 1) if n in NM2}
print('  now: last', last, 'cells with NM', len(NMr), 'solar glyph cells lacking a new moon', [n for n in solar if n not in NMr])
print('  now', (sum(abs(FMr[n]) <= LN for n in lunar), sum(-LS <= NMr[n] <= LN for n in solar if n in NMr), sum(abs(FMr[n]) < 1 for n in FMr), sum(abs(FMr[n]) < 1 and n in lunar for n in FMr)),
      '; smallest |lat| of a lunar glyph full moon now', round(min(abs(FMr[n]) for n in lunar), 2), '; solar glyph new moons now: range', round(min(NMr[n] for n in solar if n in NMr), 2), round(max(NMr[n] for n in solar if n in NMr), 2), 'nearest to the band', sorted(round(NMr[n], 2) for n in solar if n in NMr and -1.2 < NMr[n] < 2.2))
print('\nSensitivity (cycle: lunar ok, solar ok, umbral n, umbral on glyph, missed):')
for ln in (1.35, LN, 1.50):
    for j in range(4): print(f'  north/lunar limit {ln:.2f}, south {ln * LS / LN:.3f}: cycle {j}', tally(FM, NM, 223 * j, ln, ln * LS / LN)[:2])
for um in (0.9, 1.0, 1.1):
    for j in range(4): print(f'  umbral {um}: cycle {j}', tally(FM, NM, 223 * j, um=um)[2:])
print('\ncycle 0 detail:')
print('  lunar glyph months failing:', [(n, lunar[n], round(FM[n], 3)) for n in sorted(lunar) if abs(FM[n]) > LN])
print('  solar glyph months failing:', [(n, solar[n], round(NM[n], 3)) for n in sorted(solar) if not -LS <= NM[n] <= LN])
print('  new moons inside limits, no glyph:', [(n, round(NM[n], 3)) for n in range(1, 224) if -LS <= NM[n] <= LN and n not in solar])
print('  full moons within 1.43, no glyph:', [(n, round(FM[n], 3)) for n in range(1, 224) if abs(FM[n]) <= LN and n not in lunar])
w15 = [n for n in range(1, 224) if abs(NM[n]) < 1.5]
print('  new moons within 1.5:', len(w15), 'on glyph', sum(n in solar for n in w15), '; the unmarked ones:', [(n, round(NM[n], 2)) for n in w15 if n not in solar])
print('  solar glyph months latitudes sorted:', sorted(round(NM[n], 2) for n in solar))
print('  lunar glyph months |lat| largest 8:', sorted((round(abs(FM[n]), 3), n) for n in lunar)[-8:])
for j in range(4):
    print(f'  cycle {j}: month 126 FM lat {FM[223*j+126]:+.3f}; month 38 {FM[223*j+38]:+.3f}; month 173 {FM[223*j+173]:+.3f}; month 125 {FM[223*j+125]:+.3f}; lunar months within 0.05 of 1.43:', [(n, round(FM[223*j+n], 3)) for n in sorted(lunar) if abs(abs(FM[223*j+n]) - LN) < 0.06],
          '; solar failing:', [(n, round(NM[223*j+n], 3)) for n in sorted(solar) if not -LS <= NM[223*j+n] <= LN])

# ---- the shift, my own fit (continuous), with and without a free amplitude
def mlat(n, kind, s, inc=INC):
    p = 38 * (n - 1) + (17 if kind == 'F' else 36)
    th = math.radians((p - 66 - s) * 360 / 446)
    return inc * math.sin(th) if kind == 'F' else -inc * math.sin(th)
print('\nShift fits (units): fixed 5.145 | free amplitude (shift, amplitude) | near-node only (|lat|<2), free amplitude | rms deg')
sh = []
for j in range(4):
    obs = [(n, 'F', FM[223 * j + n]) for n in range(1, 224)] + [(n, 'N', NM[223 * j + n]) for n in range(1, 224)]
    r1 = least_squares(lambda x: [b - mlat(n, k, x[0]) for n, k, b in obs], [0.0])
    r2 = least_squares(lambda x: [b - mlat(n, k, x[0], x[1]) for n, k, b in obs], [0.0, 5.0])
    near = [o for o in obs if abs(o[2]) < 2.0]
    r3 = least_squares(lambda x: [b - mlat(n, k, x[0], x[1]) for n, k, b in near], [0.0, 5.0])
    sh.append(r1.x[0])
    print(f'  cycle {j}: {r1.x[0]:+.3f} (rms {math.sqrt(2 * r1.cost / len(obs)):.3f}) | {r2.x[0]:+.3f}, {r2.x[1]:.3f} (rms {math.sqrt(2 * r2.cost / len(obs)):.3f}) | {r3.x[0]:+.3f}, {r3.x[1]:.3f} (n={len(near)}, rms {math.sqrt(2 * r3.cost / len(near)):.3f})')
rate = np.polyfit(range(4), sh, 1)
print('  drift per cycle', round(rate[0], 4), 'units =', round(rate[0] * 360 / 446, 4), 'deg; line crosses zero at cycle', round(-rate[1] / rate[0], 2), '; line at cycle -1:', round(rate[1] - rate[0], 3), 'units =', round((rate[1] - rate[0]) * 360 / 446, 3), 'deg; cycle +1 measured', round(sh[1] * 360 / 446, 3), 'deg')
print('  by the books: 223 syn - 242 drac = ', 223 * 29.530588853 - 242 * 27.212220817, 'days ->', (242 * 27.212220817 - 223 * 29.530588853) * 360 / 27.212220817, 'deg =', (242 * 27.212220817 - 223 * 29.530588853) * 360 / 27.212220817 * 446 / 360, 'units; with epoch -200 month lengths (syn 29.5305843, drac 27.2122123):', (242 * 27.2122123 - 223 * 29.5305843) * 360 / 27.2122123)
import json
json.dump(dict(FM={str(k): v for k, v in FM.items()}, NM={str(k): v for k, v in NM.items()}, sh=sh), open('/home/agent3/antikythera/dial/check-scripts/own.json', 'w'))
