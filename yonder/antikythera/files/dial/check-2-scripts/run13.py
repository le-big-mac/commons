"""Third reading, step 2: Freeth 2014 Table S5 by my own route, and his 'matching exercises' as far as the pages on disk allow.
usage: run13.py IJPAPER CATDIR [CATDIR...]"""
import sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cat2, lists2
PAPER, CATS = sys.argv[1], sys.argv[2:]
K0 = json.load(open(os.path.join(HERE, 'k0.json')))['K0']
FM0 = json.load(open(os.path.join(HERE, 'k0.json')))['full0']           # JD (TT) of the full moon of 12 May 205 BC, from the JPL table
FL, FS, info, _ = lists2.freeth()
t5 = lists2.ij_table5(PAPER); IL = [r[0] for r in t5 if r[1] == 'Y']; IS = [r[0] for r in t5 if r[3] == 'Y']
RL = [r[0] for r in t5 if r[1] == 'Y' and not r[2]]; RS = [r[0] for r in t5 if r[3] == 'Y' and not r[4]]
CL = [20, 26, 61, 67, 79, 114, 120, 125, 131, 137, 172, 178, 184, 190]; CS = [13, 25, 72, 78, 119, 125, 131, 137, 172, 178, 184]   # Carman & Evans's lists
LE, _, _ = cat2.load('LE', CATS, verbose=False); SE, _, _ = cat2.load('SE', CATS, verbose=False)
LM = {int(round(cat2.k_of(r['jd']) - 0.5)) - K0 + 1: r for r in LE}
SM = {int(round(cat2.k_of(r['jd']))) - K0: r for r in SE}

def score(k, L, S):
    Ls, Ss = set(L), set(S)
    return (sum(k + n in LM for n in L), sum(k + n in SM for n in S),
            sum(1 for n in range(1, 224) if k + n in LM and LM[k + n]['umag'] > 0 and n not in Ls),
            sum(1 for n in range(1, 224) if k + n in SM and SM[k + n]['gamma'] > 0 and n not in Ss),
            sum(1 for n in range(1, 224) if k + n in SM and SM[k + n]['gamma'] < 0 and n not in Ss))

S5 = [(-240, 5, 5, 15, 53, 54.12, 100.05, 25.26), (-222, 5, 16, 23, 23, 54.59, 100.06, 36.01), (-204, 5, 12, 13, 21, 55.06, 100.09, 46.75),
      (-186, 5, 23, 19, 45, 55.54, 100.15, 57.50), (-168, 6, 3, 2, 8, 56.01, 100.22, 68.24), (-48, 1, 1, 2, 48, 54.40, 100.13, 277.38),
      (-30, 1, 11, 10, 43, 54.82, 100.08, 288.19), (-12, 1, 22, 18, 32, 55.24, 100.05, 298.99)]
kf0 = cat2.k_of(FM0)                                   # Meeus k of the dial's first full moon (x.5)
print(f'the dial\'s first full moon: JD {FM0:.4f} TT, Meeus k {kf0:.4f}')
print('Table S5 row | JD of the printed date | Meeus lunation of that instant less that of 12 May 205 BC | phase | nearest full moon k | date of the mean full moon k | A, S, U, N, southern unmarked (Freeth) | (IJ)')
def greg_or_jul(jd):
    z = int(np.floor(jd + 0.5)); b = z + 1524; c = int((b - 122.1) // 365.25); d = int(np.floor(365.25 * c)); e = int((b - d) // 30.6001)
    day = b - d - int(np.floor(30.6001 * e)); mon = e - 1 if e < 14 else e - 13; yr = c - 4716 if mon > 2 else c - 4715
    return f'{yr}-{mon:02d}-{day:02d} {((jd + 0.5) % 1) * 24:04.1f}h'
prev = None
for y, mo, d, h, mi, node, diam, sun in S5:
    jd = cat2.jd_from_date(y, mo, d, False) + (h + mi / 60) / 24            # UT; delta T about 3.5 h then, which is 0.005 lunation
    x = cat2.k_of(jd + 12600 / 86400) - kf0
    k = int(round(x)); ph = x - k
    what = 'full moon' if abs(ph) < 0.1 else ('NEW moon, half a lunation after full moon k' if abs(ph - 0.5) < 0.1 or abs(ph + 0.5) < 0.1 else '?')
    if abs(ph - 0.5) < 0.1: k = int(np.floor(x))
    mf = cat2.mean_phase_jde(K0 + 0.5 + k)
    step = '' if prev is None else f' (step from the row above: node {node - prev[0]:+.2f} deg, mean Sun {sun - prev[1]:+.2f} deg, {(jd - prev[2]):.2f} d = {(jd - prev[2]) / 29.530589:.3f} lunations)'
    prev = (node, sun, jd)
    print(f'  {y}-{mo:02d}-{d:02d} {h:02d}:{mi:02d} | {jd:.3f} | {x:+.3f} | {what} | k = {k} = {k // 223} cycles + {k % 223} months | {greg_or_jul(mf)} | {score(k, FL, FS)} | {score(k, IL, IS)}{step}')
    # the first lunar eclipse after that start, to pin the true full moons: month 2 has a lunar glyph
    e = LM.get(k + 2)
    if e: print(f'        lunar eclipse in month 2 of that start: {e["date"]} {e["hms"]} TD ({e["typ"]}); so full moon 1 fell about {greg_or_jul(e["jd"] - 29.53)} (one mean month earlier)')

# membership
def year(k):
    jd = cat2.mean_phase_jde(K0 + 0.5 + k); yv = int(np.floor((jd - 1721057.5) / 365.25))
    while cat2.jd_from_date(yv + 1, 1, 1, False) <= jd: yv += 1
    while cat2.jd_from_date(yv, 1, 1, False) > jd: yv -= 1
    return yv
Ks = [k for k in range(-1300, 2800) if -299 <= year(k) <= 0]
sc = {k: score(k, FL, FS) for k in Ks}
a0, s0, u0 = sc[0][:3]
right = lambda k: sc[k][3] < sc[k][4]
g16 = [k for k in Ks if sc[k][0] >= a0 and sc[k][1] >= s0 and sc[k][2] <= u0 and right(k)]
g35 = [k for k in Ks if sc[k][0] + sc[k][1] >= a0 + s0 and sc[k][2] <= u0 and right(k)]
eight = [-446, -223, 0, 223, 446, 1925, 2148, 2371]
print(f'\nof Freeth\'s eight (as full moons): in my 16: {[1 - year(k) for k in eight if k in g16]}; in the 35 of the looser reading: {[1 - year(k) for k in eight if k in g35]}; in neither: {[1 - year(k) for k in eight if k not in g35]}')
print(f'my 16 that are not among his eight: {[1 - year(k) for k in g16 if k not in eight]}')

# his matching exercises, on the 300 years the pages cover
def allmatch(k, L, S, umbral=False):
    return all((k + n in LM and (not umbral or LM[k + n]['umag'] > 0)) for n in L) and all(k + n in SM for n in S)
print(f'\n"matching exercise", {len(Ks)} starts from 300 BC to 1 BC (Freeth: just under 5,000 months, 400 BC to 1 BC):')
for lab, L, S in (('full EYM sequence (38 lunar, 28 solar)', FL, FS), ('Iversen & Jones full list', IL, IS), ('glyphs read on the fragments, Iversen & Jones (15, 12)', RL, RS), ('surviving glyphs as Carman & Evans list them (14, 11)', CL, CS)):
    m = [k for k in Ks if allmatch(k, L, S)]; mu = [k for k in Ks if allmatch(k, L, S, umbral=True)]
    print(f'   {lab}: every glyph has an eclipse of its kind in its month at {len(m)} starts ({sum(right(k) for k in m)} the right way round); with penumbral eclipses barred: {len(mu)}; is 205 BC one of them: {0 in m}')
    print(f'       per century (3rd, 2nd, 1st BC): {[sum(1 for k in m if lo < 1 - year(k) <= hi) for lo, hi in ((200, 300), (100, 200), (0, 100))]}')

# the south limit at 6 in place of 7 (Note S3)
def glyphs(south):
    sol = []
    for n in range(1, 224):
        p = (38 * (n - 1) + 36) % 446
        dD = ((p - 66 + 223) % 446) - 223; dA = ((p - 289 + 223) % 446) - 223
        d, node = (dD, 'D') if abs(dD) <= abs(dA) else (dA, 'A')
        north = (d <= 0) if node == 'D' else (d >= 0)
        if abs(d) <= (20 if north else south): sol.append(n)
    return sol
print('\nsolar glyph months lost when the south limit is 6 units in place of 7:', sorted(set(glyphs(7)) - set(glyphs(6))), '; gained:', sorted(set(glyphs(6)) - set(glyphs(7))), '; count', len(glyphs(6)))
print('degrees: 20 EYu * 180/223 =', round(20 * 180 / 223, 2), '; 7 EYu * 180/223 =', round(7 * 180 / 223, 2), '; 7 * 360/470 =', round(7 * 360 / 470, 2), '; latitude 0.0720 * 20 =', 0.0720 * 20, ', 0.0720 * 7 =', round(0.0720 * 7, 3))
print('node column of Table S5 against the model input 53.27:', [round(r[5] - 53.27, 2) for r in S5], '; per Saros within the first five:', round((56.01 - 54.12) / 4, 4), '; with the dial start 2 EYu after NM0 the input would be', round(68 * 365.25 / 470 / 365.25 * 379.4, 2))
