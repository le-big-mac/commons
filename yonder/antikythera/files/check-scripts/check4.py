"""Eclipse dial test redone with the checker's own code (after.py part D), thresholds varied.
Uses longitudes of date (T) and latitude of date. usage: python -I check4.py"""
import sys, os, math
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import load
sky = load.load()
wrap = lambda x: (np.asarray(x) + 180.0) % 360.0 - 180.0
unwrap = lambda x: np.degrees(np.unwrap(np.radians(x)))

def syz(w):
    m, s = sky[w]['moon'], sky[w]['sun']
    cm = CubicSpline(m['jd'], unwrap(m['T'])); cs = CubicSpline(s['jd'], unwrap(s['T'])); cb = CubicSpline(m['jd'], m['lat'])
    jd = m['jd']; D = wrap(cm(jd) - cs(jd))
    out = {}
    for kind, off in (('new', 0.0), ('full', 180.0)):
        d = wrap(D - off)
        idx = np.where((d[:-1] < 0) & (d[1:] >= 0) & (np.abs(d[:-1]) < 30))[0]
        t = np.array([brentq(lambda x: float(wrap(cm(x) - cs(x) - off)), jd[i], jd[i + 1], xtol=1e-8) for i in idx])
        out[kind] = (t, cb(t))
    return out
sz = {w: syz(w) for w in ('then', 'now')}
for w in sz:
    print(f'{w}: {len(sz[w]["new"][0])} new moons, {len(sz[w]["full"][0])} full moons; first new JD {sz[w]["new"][0][0]:.3f}, last new JD {sz[w]["new"][0][-1]:.3f}; mean month {np.polyfit(np.arange(len(sz[w]["new"][0])), sz[w]["new"][0], 1)[0]:.6f} d')
# lunation number of every new moon, counted from the first new moon of 'then': within a window by order; across the gap by
# the mean month (checked: the count must come out within a small fraction of an integer)
syn_then = np.polyfit(np.arange(len(sz['then']['new'][0])), sz['then']['new'][0], 1)[0]
syn_now = np.polyfit(np.arange(len(sz['now']['new'][0])), sz['now']['new'][0], 1)[0]
t0 = sz['then']['new'][0][0]
gap = (sz['now']['new'][0][0] - t0) / (0.5 * (syn_then + syn_now))
K0 = int(round(gap))
# second way: carry the count through the gap with a quadratic model of the mean new moon time fitted to both windows
kk = np.concatenate([np.arange(len(sz['then']['new'][0])), K0 + np.arange(len(sz['now']['new'][0]))])
tt = np.concatenate([sz['then']['new'][0], sz['now']['new'][0]])
for trial in (K0 - 1, K0, K0 + 1):
    k2 = np.concatenate([np.arange(len(sz['then']['new'][0])), trial + np.arange(len(sz['now']['new'][0]))])
    c = np.polyfit(k2, tt, 2); r = tt - np.polyval(c, k2)
    print(f'   lunation count across the gap {trial}: quadratic fit of new-moon times: rms {np.sqrt(np.mean(r**2)):.4f} d, quadratic coefficient {c[0]:.3e} d per lunation^2')
print(f'gap in mean months {gap:.4f} -> K0 = {K0}')
# The gears' own count of lunations over the span (235/19 per turn of the Sun), had the dial been turned by the Sun:
TA, TB = sky['then']['sun']['jd'][0], sky['now']['sun']['jd'][-1]
for fr, dn in (('S', 2230.48955), ('T', 2230.57569)):
    sky_lun = None
    print(f'   turned by the Sun, frame {fr}: gears count {dn * 235 / 19:.3f} lunations over the span; the sky had {(TB - TA) / (0.5 * (syn_then + syn_now)):.3f}; the dial pointer is {(dn * 235 / 19 - (TB - TA) / (0.5 * (syn_then + syn_now))):+.3f} cells from where one-cell-a-lunation puts it')

def table(w, k0):
    nt, nb = sz[w]['new']; ft, fb = sz[w]['full']
    return k0 + np.arange(len(nt)), nb, k0 + np.searchsorted(nt, ft) - 1, fb

def run(ths, thl, verbose=True):
    kn, nb, kf, fb = table('then', 0)
    Gs = set(int(k) for k in kn[(kn < 223) & (np.abs(nb) < ths)]); Gl = set(int(k) for k in kf[(kf >= 0) & (kf < 223) & (np.abs(fb) < thl)])
    line = [f'thresholds {ths}/{thl}: dial has {len(Gs)} solar, {len(Gl)} lunar cells.']
    for j in (1, 2, 3):
        es = kn[(kn >= 223 * j) & (kn < 223 * (j + 1)) & (np.abs(nb) < ths)]; el = kf[(kf >= 223 * j) & (kf < 223 * (j + 1)) & (np.abs(fb) < thl)]
        line.append(f'cycle {j + 1}: solar {sum(int(k) % 223 in Gs for k in es)}/{len(es)}, lunar {sum(int(k) % 223 in Gl for k in el)}/{len(el)}.')
    kn2, nb2, kf2, fb2 = table('now', K0)
    last = int(kn2[-1]) + 1
    es = kn2[(kn2 >= last - 223) & (np.abs(nb2) < ths)]; el = kf2[(kf2 >= last - 223) & (kf2 < last) & (np.abs(fb2) < thl)]
    hs = sum(int(k) % 223 in Gs for k in es); hl = sum(int(k) % 223 in Gl for k in el)
    line.append(f'last 223 (lunations {last - 223}..{last - 1} = {(last - 223) / 223:.2f} to {last / 223:.2f} Saros after the first new moon): solar {hs}/{len(es)} (chance {len(es) * len(Gs) / 223:.1f}), lunar {hl}/{len(el)} (chance {len(el) * len(Gl) / 223:.1f}).')
    def shifts(ecl, G):
        c = [int(k) % 223 for k in ecl]
        return [sum(((x - sh) % 223) in G for x in c) for sh in range(223)]
    ss, sl = shifts(es, Gs), shifts(el, Gl)
    top_s = sorted(range(223), key=lambda i: -ss[i])[:4]; top_l = sorted(range(223), key=lambda i: -sl[i])[:4]
    line.append('best shifts solar ' + ', '.join(f'{i}:{ss[i]}' for i in top_s) + '; lunar ' + ', '.join(f'{i}:{sl[i]}' for i in top_l) + f'; lunar at 43: {sl[43]}/{len(el)}; solar at 125: {ss[125]}/{len(es)}; both at shift 0, +-1: solar {ss[0]},{ss[1]},{ss[222]} lunar {sl[0]},{sl[1]},{sl[222]}')
    print('\n   '.join(line))
    return Gs, Gl, es, el
for ths, thl in ((1.5, 1.0), (1.4, 0.9), (1.6, 1.1), (1.2, 0.8), (1.8, 1.6)):
    run(ths, thl)
# why none: the Moon's distance from the node at new moon, for the dial's cells and for today's
kn, nb, kf, fb = table('then', 0); kn2, nb2, kf2, fb2 = table('now', K0)
last = int(kn2[-1]) + 1
cells_then = {int(k): b for k, b in zip(kn, nb) if k < 223}
m = kn2 >= last - 223
lat_now_on_glyph = [abs(b) for k, b in zip(kn2[m], nb2[m]) if abs(cells_then[int(k) % 223]) < 1.5]
print(f'the dial\'s 41 solar cells today: |latitude| of the Moon at new moon in those cells: min {min(lat_now_on_glyph):.2f}, median {np.median(lat_now_on_glyph):.2f}, max {max(lat_now_on_glyph):.2f} deg (an eclipse needs < 1.5)')
print(f'arithmetic: 223 synodic months less 242 draconic months = {223 * 29.530589 - 242 * 27.212221:.4f} d = {(223 * 29.530589 - 242 * 27.212221) / 27.212221 * 360:.3f} deg of node-distance per Saros; x 123.2 = {(223 * 29.530589 - 242 * 27.212221) / 27.212221 * 360 * 123.2:.1f} deg; 43 lunations move the node-distance by {43 * 29.530589 / 27.212221 * 360 % 180:.1f} deg mod 180; 125 by {125 * 29.530589 / 27.212221 * 360 % 180:.1f}')
