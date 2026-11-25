"""Second reader, step 3: the scan of other start dates by my own route, and the tables' latitudes for the disputed months.
usage: run3.py JPLDIR IJPAPER CATDIR [CATDIR...]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import cat2, lists2

JPL, PAPER, CATS = sys.argv[1], sys.argv[2], sys.argv[3:]
K0 = json.load(open(os.path.join(HERE, 'k0.json')))['K0']
FL, FS, info, _ = lists2.freeth()
t5 = lists2.ij_table5(PAPER)
IL = [r[0] for r in t5 if r[1] == 'Y']; IS = [r[0] for r in t5 if r[3] == 'Y']
LE, _, _ = cat2.load('LE', CATS, verbose=False); SE, _, _ = cat2.load('SE', CATS, verbose=False)
LM = {int(round(cat2.k_of(r['jd']) - 0.5)) - K0 + 1: r for r in LE}
SM = {int(round(cat2.k_of(r['jd']))) - K0: r for r in SE}


def cal_year(jd):
    """astronomical year of a JD in the Julian calendar (exact, by stepping from the date routine)"""
    y = int(np.floor((jd - 1721057.5) / 365.25))            # close guess; JD 1721057.5 = 0 Jan 1 (Julian)
    while cat2.jd_from_date(y + 1, 1, 1, False) <= jd: y += 1
    while cat2.jd_from_date(y, 1, 1, False) > jd: y -= 1
    return y


def start_jd(k):                                             # mean full moon k lunations from the dial's first
    return cat2.mean_phase_jde(K0 + 0.5 + k)


Ks = [k for k in range(-1300, 2800) if -299 <= cal_year(start_jd(k)) <= 0]
print(f'{len(Ks)} starts whose (mean) first full moon falls in the years -299 to 0 (300 BC to 1 BC): k {Ks[0]} to {Ks[-1]}; '
      f'the catalogue pages begin {LE[0]["date"]} (lunar) and {SE[0]["date"]} (solar)')
print(f'   k = 0 mean full moon JD {start_jd(0):.2f}, year {cal_year(start_jd(0))}')

# orientation: for solar glyph months with an eclipse, does gamma's sign agree with the model's north/south?
def model_ns(n):
    """(distance, north?) of month n's new moon in the eclipse year model, glyph or not"""
    p = (38 * (n - 1) + 36) % 446
    dD = ((p - 66 + 223) % 446) - 223; dA = ((p - 289 + 223) % 446) - 223
    if abs(dD) <= abs(dA): return dD, dD <= 0
    return dA, dA >= 0


def orient(k, S):
    ok = tot = 0
    for n in S:
        d, north = model_ns(n)
        if k + n in SM and d != 0:
            tot += 1; ok += north == (SM[k + n]['gamma'] > 0)
    return ok, tot


for name, L, S in (('Freeth', FL, FS), ('IJ', IL, IS)):
    Lset, Sset = set(L), set(S)
    sc = {}
    for k in Ks:
        A = sum(k + n in LM for n in L); Sn = sum(k + n in SM for n in S)
        U = sum(1 for n in range(1, 224) if k + n in LM and LM[k + n]['umag'] > 0 and n not in Lset)
        N = sum(1 for n in range(1, 224) if k + n in SM and SM[k + n]['gamma'] > 0 and n not in Sset)
        Sth = sum(1 for n in range(1, 224) if k + n in SM and SM[k + n]['gamma'] < 0 and n not in Sset)
        sc[k] = (A, Sn, U, N, Sth)
    a0, s0, u0, n0, _ = sc[0]
    print(f'\n{name}: k = 0 scores A {a0}, S {s0}, U {u0}, N {n0}, (southern solar eclipses unmarked: {sc[0][4]})')
    tot = sorted(sc[k][0] + sc[k][1] for k in Ks)
    print(f'   A + S over all starts: median {tot[len(tot) // 2]}; mean {np.mean(tot):.1f}; share scoring 0: {np.mean(np.array(tot) == 0):.3f}; '
          f'share scoring at least 10: {np.mean(np.array(tot) >= 10):.3f}; at least 33: {np.mean(np.array(tot) >= 33):.3f}; at least 60: {np.mean(np.array(tot) >= 60):.3f}; '
          f'at least {a0 + s0}: {int(np.sum(np.array(tot) >= a0 + s0))}; equal 66: {int(np.sum(np.array(tot) == 66))}')
    hist = {}
    for t in tot: hist[t // 6 * 6] = hist.get(t // 6 * 6, 0) + 1
    print(f'   histogram of A + S in bins of 6: {dict(sorted(hist.items()))}')
    g3 = [k for k in Ks if sc[k][0] >= a0 and sc[k][1] >= s0 and sc[k][2] <= u0]
    print(f'   at least as good on A, S, U: {len(g3)}; of these scoring every glyph ({len(L)} and {len(S)}): {sum(sc[k][0] == len(L) and sc[k][1] == len(S) for k in g3)}')
    Nv = sorted(sc[k][3] for k in g3)
    print(f'   their N values: {Nv}')
    print('   each good start: k, year BC, k mod 223, (A, S, U, N, southern unmarked), gamma-sign agreement with the model in solar glyph months')
    for k in g3:
        ok, tt = orient(k, S)
        print(f'      {k:6d}  {1 - cal_year(start_jd(k)):3d} BC  cycles {k // 223:3d} + {k % 223:3d} months   {sc[k]}   orientation {ok}/{tt}')
    right = [k for k in g3 if orient(k, S)[0] > orient(k, S)[1] / 2]
    print(f'   nodes the right way round (by gamma sign): {len(right)}; of these N = 0: {[ (k, 1 - cal_year(start_jd(k))) for k in right if sc[k][3] == 0]}; N = 1 or 2: {sum(sc[k][3] in (1, 2) for k in right)}; '
          f'scoring every glyph: {sum(sc[k][0] == len(L) and sc[k][1] == len(S) for k in right)}; years BC of those with N 1 or 2: {[1 - cal_year(start_jd(k)) for k in right if sc[k][3] in (1, 2)]}')
    # with N <= n0 imposed but nothing about A/S/U perfect: what the northern unmarked eclipses are for the right-way starts
    for k in right:
        if 0 < sc[k][3] <= 2:
            det = [(n, SM[k + n]['typ'], SM[k + n]['mag'], SM[k + n]['gamma']) for n in range(1, 224) if k + n in SM and SM[k + n]['gamma'] > 0 and n not in Sset]
            print(f'      k {k}: northern unmarked (month, type, magnitude, gamma): {det}')
    whole = [k for k in Ks if k % 223 == 0]
    print('   whole cycles: ' + '; '.join(f'{k // 223}: {sc[k][:4]}' for k in whole))
    # other ways of asking "as well as 205 BC"
    print(f'   starts with A + S >= {a0 + s0}: {sum(sc[k][0] + sc[k][1] >= a0 + s0 for k in Ks)}; with A >= {a0} and S >= {s0}: {sum(sc[k][0] >= a0 and sc[k][1] >= s0 for k in Ks)}; '
          f'with A + S >= {a0 + s0} and U <= {u0} and right way round: {sum(1 for k in Ks if sc[k][0] + sc[k][1] >= a0 + s0 and sc[k][2] <= u0 and orient(k, S)[0] > orient(k, S)[1] / 2)}')

# cycle 1, Freeth: which northern eclipse is unmarked
k = 223
print('\nFreeth, cycle 1: northern solar eclipses in unmarked months:', [(n, SM[k + n]['date'], SM[k + n]['typ'], SM[k + n]['mag'], SM[k + n]['gamma']) for n in range(1, 224) if k + n in SM and SM[k + n]['gamma'] > 0 and n not in FS])
k = 446
print('Freeth, cycle 2:', [(n, SM[k + n]['date'], SM[k + n]['typ'], SM[k + n]['mag'], SM[k + n]['gamma']) for n in range(1, 224) if k + n in SM and SM[k + n]['gamma'] > 0 and n not in FS])
k = -223
print('Freeth, cycle -1: lunar glyph months with penumbral only:', [(n, LM[k + n]['typ'], LM[k + n]['pmag']) for n in FL if k + n in LM and LM[k + n]['umag'] < 0], '; month 125:', LM.get(k + 125, {}).get('date'), LM.get(k + 125, {}).get('typ'), LM.get(k + 125, {}).get('pmag'))
print('Freeth, cycle -1: solar glyph month 13:', SM.get(k + 13, {}).get('date'), SM.get(k + 13, {}).get('typ'), '; solar months without eclipse in cycles -5..-1:', {j: [n for n in FS if 223 * j + n not in SM] for j in range(-5, 0)})

# last 223 months to Nov 2026 and cycle 123, by the catalogue
for lab, months in (('months 27366 to 27588 (the 223 to November 2026), each in its cell', range(27366, 27589)), ('cycle 123 (months 27430 to 27652)', range(27430, 27653))):
    cellL = {(n - 1) % 223 + 1 for n in months if n in LM}; cellS = {(n - 1) % 223 + 1 for n in months if n in SM}
    print(f'{lab}: lunar eclipses {len(cellL)}, in Freeth lunar cells {len(cellL & set(FL))}, IJ {len(cellL & set(IL))}; solar eclipses {len(cellS)}, in Freeth solar cells {len(cellS & set(FS))}, IJ {len(cellS & set(IS))}')

# ---------- the tables: latitude at the syzygies of the disputed months (my own syzygies)
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
def read_h(path):
    jd, lon, lat = [], [], []
    on = False
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.startswith('$$SOE'): on = True; continue
            if line.startswith('$$EOE'): break
            if on:
                p = line.split(','); jd.append(float(p[0])); lon.append(float(p[5])); lat.append(float(p[6]))
    return np.array(jd), np.array(lon), np.array(lat)
mj, ml, mb = read_h(os.path.join(JPL, 'moon_then.txt')); sj, sl, sb = read_h(os.path.join(JPL, 'sun_then.txt'))
fm_lon = CubicSpline(mj, np.unwrap(np.radians(ml))); fs_lon = CubicSpline(sj, np.unwrap(np.radians(sl))); fm_lat = CubicSpline(mj, mb)
el = lambda t: fm_lon(t) - fs_lon(t)
e0, e1 = el(mj[0]), el(mj[-1])
def roots(phase):
    out = []; m = int(np.ceil((e0 - phase) / (2 * np.pi)))
    while phase + 2 * np.pi * m <= e1:
        out.append(brentq(lambda t: el(t) - phase - 2 * np.pi * m, mj[0], mj[-1], xtol=1e-7)); m += 1
    return np.array(out)
full, new = roots(np.pi), roots(0.0)
new = new[new > full[0]]                        # the n-th new moon follows the n-th full moon
FMlat = {i + 1: float(fm_lat(t)) for i, t in enumerate(full)}; NMlat = {i + 1: float(fm_lat(t)) for i, t in enumerate(new)}
assert all(full[i] < new[i] < full[i + 1] for i in range(len(new) - 1))
print('\nfrom the JPL tables (my syzygies), cycles 0 to 3:')
for n, d, lab in ((213, FMlat, 'full moon'), (214, FMlat, 'full moon'), (196, NMlat, 'new moon'), (207, NMlat, 'new moon'), (125, FMlat, 'full moon'), (31, NMlat, 'new moon'), (13, NMlat, 'new moon'), (78, NMlat, 'new moon'), (126, FMlat, 'full moon')):
    print(f'   month {n} {lab}: latitudes', [round(d[223 * j + n], 3) for j in range(4)])
LIM_N = 5.145 * np.sin(np.radians(20 * 360 / 446)); LIM_S = 5.145 * np.sin(np.radians(7 * 360 / 446))
print(f'   limits {LIM_N:.4f} and {LIM_S:.4f}')
for name, L, S in (('Freeth', FL, FS), ('IJ', IL, IS), ('read', [r[0] for r in t5 if r[1] == 'Y' and not r[2]], [r[0] for r in t5 if r[3] == 'Y' and not r[4]])):
    print(f'   {name}: lunar inside', [sum(abs(FMlat[223 * j + n]) <= LIM_N for n in L) for j in range(4)], 'solar inside', [sum(-LIM_S <= NMlat[223 * j + n] <= LIM_N for n in S) for j in range(4)],
          '; solar outside by cycle', [[n for n in S if not (-LIM_S <= NMlat[223 * j + n] <= LIM_N)] for j in range(4)])
