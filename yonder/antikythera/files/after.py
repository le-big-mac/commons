"""Looks after the sealed sheet was scored (nothing here was sealed). usage: after.py DATADIR
A. the measured rates beside JPL's approximate elements (Table 2a, 3000 BC to 3000 AD), by plain arithmetic;
B. how long each pointer stayed good: the years of gear drift that add as much error as the circle theory has;
C. today's display, pointer by pointer, in signs of thirty degrees along the J2000 ecliptic;
D. the eclipse dial, turned one cell a lunation: do its months of eclipse still hold?"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import gears, mech
from mech import wrap, D2R

DATA = sys.argv[1]
J = {f: json.load(open(os.path.join(HERE, f'results-{f}.json'))) for f in 'ST'}
S = J['S']
yrs = S['years']

print('A. Rates by arithmetic from JPL "Approximate Positions of the Planets", Table 2a, mean longitude rates in')
print('   degrees per Julian century, ecliptic and equinox of J2000 (fetched 23 Nov 2026):')
LR = {'mercury': 149472.67486623, 'venus': 58517.81560260, 'earth': 35999.37306329, 'mars': 19140.29934243,
      'jupiter': 3034.90371757, 'saturn': 1222.11494724}
print('   planet: synodic cycles per turn of the Sun (sky | gears); error of the gears, deg per Julian year, by')
print('   arithmetic | measured in the tables | printed in the 2021 paper; arithmetic over printed')
for p in gears.SYNODIC:
    s_true = (LR[p] - LR['earth']) / LR['earth'] if p in gears.INFERIOR else (LR['earth'] - LR[p]) / LR['earth']
    e_ar = 360.0 * (float(gears.SYNODIC[p]) - s_true) * LR['earth'] / 36000.0
    e_me = S['drift'][p] / yrs if p in gears.INFERIOR else -S['drift'][p] / yrs
    print(f'   {p:8s} {s_true:.8f} | {float(gears.SYNODIC[p]):.8f}   {e_ar:+.6f} | {e_me:+.6f} | {gears.PAPER_EY[p]:+.6f}   {abs(e_ar) / abs(gears.PAPER_EY[p]):.3f}')
print('   (Jupiter and Saturn swing slowly against each other, about a third and four-fifths of a degree over some')
print('   nine centuries; the tables at two dates catch that swing, the long-run rates do not.)')

sky = {w: {b: mech.read(os.path.join(DATA, f'{b}_{w}.txt')) for b in mech.BODIES} for w in ('then', 'now')}
ft = S['fit']['then']
rms = lambda x: float(np.sqrt(np.mean(np.asarray(x) ** 2)))

print('\nB. How long each pointer stayed good (frame S; frame T for the Moon also). The calibrated mechanism of the')
print('   first window, its phase put wrong by the drift of Y years, against the first window\'s sky: the Y at which')
print('   the rms error is the square root of two times the floor, that is, the gears add as much as the theory.')
def series(body, frame, dphase, dA=0.0):
    s = sky['then']; F = J[frame]['fit']['then']
    sun = F['sun']
    if body == 'moon':
        jd = s['moon']['jd']; tau = jd - F['moon']['tref']
        L = F['moon']['L0'] + F['moon']['r'] * tau + dphase
        A = F['moon']['A0'] + F['moon']['rA'] * tau + dA
        return wrap(mech.m_ecc(L, A, F['moon']['e']) - s['moon'][frame])
    jd = s[body]['jd']; tau = jd - F[body]['tref']
    Ls = sun['L0'] + sun['r'] * (jd - sun['tref'])
    ph = F[body]['p0'] + F[body]['r'] * tau + dphase
    lam = mech.m_inf(Ls, ph, F[body]['rho']) if body in gears.INFERIOR else mech.m_sup(ph, Ls, F[body]['rho'])
    return wrap(lam - s[body][frame])
def halflife(body, frame):
    rate = J[frame]['drift'][body] / yrs
    rateA = J[frame]['drift']['apsides'] / yrs if body == 'moon' else 0.0
    f0 = rms(series(body, frame, 0.0))
    lo, hi = 0.0, 1.0
    while rms(series(body, frame, rate * hi, rateA * hi)) < np.sqrt(2) * f0:
        hi *= 2
        if hi > 1e5: return f0, rate, float('inf')
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if rms(series(body, frame, rate * mid, rateA * mid)) < np.sqrt(2) * f0: lo = mid
        else: hi = mid
    return f0, rate, 0.5 * (lo + hi)
for body, frame in (('moon', 'S'), ('moon', 'T'), ('mercury', 'S'), ('venus', 'S'), ('mars', 'S'), ('jupiter', 'S'), ('saturn', 'S'),
                    ('mercury', 'T'), ('venus', 'T'), ('mars', 'T'), ('jupiter', 'T'), ('saturn', 'T')):
    f0, rate, Y = halflife(body, frame)
    print(f'   {body:8s} frame {frame}: floor rms {f0:6.3f} deg; drift {rate:+.5f} deg a year; years until the gears match the theory: {Y:8.1f}')

print('\nC. Today (23 Nov 2026, 12h TT), frame S: where each pointer stands and where the body is, in signs of 30')
print('   degrees along the ecliptic of J2000 counted from its equinox (not the constellations, not the signs of date)')
SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
def sign(x):
    x = x % 360.0
    return f'{SIGNS[int(x // 30)]} {x % 30:4.1f}'
today = {}
for b in mech.BODIES:
    lam = float(sky['now'][b]['S'][-1])
    ptr = (lam + S['today'][b]) % 360.0
    today[b] = (ptr, lam)
    print(f'   {b:8s} pointer {ptr:7.2f} ({sign(ptr):16s})   sky {lam:7.2f} ({sign(lam):16s})   pointer minus sky {S["today"][b]:+8.2f}')
json.dump(today, open(os.path.join(HERE, 'today.json'), 'w'), indent=1)
el = wrap(sky['now']['venus']['S'][-1] - sky['now']['sun']['S'][-1]); el2 = wrap(sky['now']['mars']['S'][-1] - sky['now']['sun']['S'][-1])
print(f'   Venus stands {float(el):+.1f} deg from the Sun today, Mars {float(el2):+.1f}.')
jdv = sky['now']['venus']['jd']; ev = wrap(sky['now']['venus']['S'] - sky['now']['sun']['S'])
i = np.where((ev[:-1] > 0) & (ev[1:] <= 0) & (np.abs(ev[:-1]) < 20))[0]
print(f'   Venus\'s last passage between us and the Sun in the table: JD {jdv[i[-1]]:.1f}, {jdv[-1] - jdv[i[-1]]:.0f} days before today.')

print('\nD. The eclipse dial, one cell a lunation (223 cells). Proxy for an eclipse: at new moon the Moon within 1.5')
print('   deg of the ecliptic (a solar eclipse somewhere on Earth), at full moon within 1.0 deg (the Moon in the')
print('   Earth\'s shadow). An ideal dial is engraved from the first 223 lunations after 1 May 205 BC.')
def syzygies(w):
    m, s = sky[w]['moon'], sky[w]['sun']
    sunT = np.interp(m['jd'], s['jd'], np.unwrap(s['T'] * D2R) / D2R)
    D = wrap(m['T'] - sunT)
    out = {}
    for kind, off in (('new', 0.0), ('full', 180.0)):
        d = wrap(D - off)
        i = np.where((d[:-1] < 0) & (d[1:] >= 0) & (d[1:] - d[:-1] < 90))[0]
        f = -d[i] / (d[i + 1] - d[i])
        out[kind] = (m['jd'][i] + f * (m['jd'][i + 1] - m['jd'][i]), m['lat'][i] + f * (m['lat'][i + 1] - m['lat'][i]))
    return out
sz = {w: syzygies(w) for w in ('then', 'now')}
t0 = sz['then']['new'][0][0]
syn_then = np.polyfit(np.arange(len(sz['then']['new'][0])), sz['then']['new'][0], 1)[0]
syn_now = np.polyfit(np.arange(len(sz['now']['new'][0])), sz['now']['new'][0], 1)[0]
gap = (sz['now']['new'][0][0] - t0) / (0.5 * (syn_then + syn_now))
print(f'   mean synodic month then {syn_then:.6f} d, now {syn_now:.6f} d; lunations from the first new moon then to the first now: {gap:.3f}')
K0 = int(round(gap))
def table(w, k0):
    new_t, new_b = sz[w]['new']; full_t, full_b = sz[w]['full']
    k_new = k0 + np.arange(len(new_t))
    # a full moon belongs to the lunation whose new moon came before it
    k_full = k0 + np.searchsorted(new_t, full_t) - 1
    return (k_new, np.abs(new_b) < 1.5), (k_full, np.abs(full_b) < 1.0)
(kn, sn), (kf, lf) = table('then', 0)
G_sol = set((kn[(kn < 223) & sn] % 223).tolist()); G_lun = set((kf[(kf >= 0) & (kf < 223) & lf] % 223).tolist())
print(f'   the ideal dial: {len(G_sol)} cells with a solar glyph, {len(G_lun)} with a lunar one, of 223')
def test(label, k, flag, G, lo, hi):
    m = (k >= lo) & (k < hi)
    ecl = k[m & flag]
    hit = sum((int(x) % 223) in G for x in ecl)
    return f'{label}: {len(ecl):2d} eclipses, {hit:2d} on a glyph cell (by chance {len(ecl) * len(G) / 223:4.1f})'
for j in (1, 2, 3):
    print(f'   Saros {j} after engraving ({18.03 * j:5.1f} years on):  solar {test("", kn, sn, G_sol, 223 * j, 223 * (j + 1))};  lunar {test("", kf, lf, G_lun, 223 * j, 223 * (j + 1))}')
(kn2, sn2), (kf2, lf2) = table('now', K0)
last = int(kn2[-1]) + 1
print(f'   the 223 lunations to today (Saros {(last - 223) / 223:.1f} to {last / 223:.1f} after engraving):  solar {test("", kn2, sn2, G_sol, last - 223, last)};  lunar {test("", kf2, lf2, G_lun, last - 223, last)}')
# how far have the eclipse months moved round the dial? best shift of the glyph pattern
def best_shift(k, flag, G, lo, hi):
    m = (k >= lo) & (k < hi); ecl = [int(x) % 223 for x in k[m & flag]]
    sc = [(sum(((c - sh) % 223) in G for c in ecl), sh) for sh in range(223)]
    return max(sc), len(ecl)
(b, sh), n = best_shift(kn2, sn2, G_sol, last - 223, last)
print(f'   solar: turning the glyph pattern by {sh} cells would catch {b} of {n};', end=' ')
(b, sh), n = best_shift(kf2, lf2, G_lun, last - 223, last)
print(f'lunar: by {sh} cells, {b} of {n}')
