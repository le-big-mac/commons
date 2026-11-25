"""disc/after.py: what I looked at after the verdicts; nothing here was sealed.   python -I after.py > after.out
(DISC_RUNS=DIR python -I after.py does the same on the clouds in DIR, to try the script.)"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dtheory as th
from dlib import RUNS, RAD, K, load, lines, var, sev, corr, secorr, pred_ring, pred_corr, sizes_in, NAME
sizes = sizes_in(); DATA = {(kind, n): load(kind, n) for kind in ('chance', 'exact') for n in sizes}
MID = [r for r in RAD if 0.2 - 1e-9 <= r <= 0.8 + 1e-9]
def spread(d, f, n=200, seed=3):
    """the standard error of f(clouds), by resampling whole clouds with replacement (the referee showed that my first way, splitting the clouds in ten, gave errors that were themselves uncertain by a quarter and at 200 clouds a third too small)"""
    rng = np.random.default_rng(seed); N = d['clouds'] if isinstance(d, dict) else d
    return float(np.std([f(rng.integers(0, N, N)) for _ in range(n)], ddof=1))
HALFW = 0.008
def loss(r, n, d=None): return (th.D if d is None else d) * (n / math.pi) ** (1 / 3.0) * r ** (-1 / 3.0) * HALFW / (6 * math.pi)      # what the mean over a NARROW annulus takes off a ripple's mean square (and off the ring's mean's variance)
def cov_mode(m):
    """the equation's covariance of the m-th ripple at two radii: the inner amplitude is the outer one shrunk by (inner/outer)^(m^2/3), plus what was gathered between"""
    return lambda r1, r2, n: th.mode(m, max(r1, r2), n) * (min(r1, r2) / max(r1, r2)) ** (m * m / 3.0)
def mode_ann(m, r, n): return th.annulus(cov_mode(m), r, r, n, half=HALFW)            # the ripple's mean square as measured: its amplitude is a mean over the annulus
def corr_ann(m, ro, ri, n): return th.annulus(cov_mode(m), ro, ri, n, half=HALFW) / math.sqrt(mode_ann(m, ro, n) * mode_ann(m, ri, n))

print('A. The noise, measured in the discs alone. With the number of points left to chance the variance of the ring\'s mean should be 0.1630 D n^(1/3) (1 - r^(2/3)):')
print('   D from the 13 annuli from 0.2 to 0.8 (each variance over what D = 1 would give; their mean; the standard error by resampling the clouds)')
def d_of(d, n, idx=None):
    q = d['Q'] if idx is None else d['Q'][idx]; return float(np.mean([np.var(q[:, K(r)], ddof=1) / (pred_ring('chance', r, n) / th.D) for r in MID]))
for n in sizes:
    d = DATA[('chance', n)]
    if not d: continue
    print('   n = %8d: D = %.3f (%.3f)      [the level problem: 1.081, good to about 0.06]' % (n, d_of(d, n), spread(d, lambda ix: d_of(d, n, ix))))
    inner = [r for r in RAD if 0.3 - 1e-9 <= r <= 0.5 + 1e-9]; outer = [r for r in RAD if 0.6 - 1e-9 <= r <= 0.95 + 1e-9]
    print('                 measured over predicted by stretch of radius: %.3f from 0.3 to 0.5, %.3f from 0.6 to 0.95 (a wrong D would give the same in both)' % (np.mean([var(d['Q'][:, K(r)]) / pred_ring('chance', r, n) for r in inner]), np.mean([var(d['Q'][:, K(r)]) / pred_ring('chance', r, n) for r in outer])))
print('   and with exactly n points, what is left when the predicted part of the count of points is taken off (the rest of D, predicted %.3f):' % th.DR)
for n in sizes:
    d = DATA[('exact', n)]
    if not d: continue
    def rest(idx=None):
        q = d['Q'] if idx is None else d['Q'][idx]
        return float(np.mean([(np.var(q[:, K(r)], ddof=1) - th.annulus(th.cov_fixed, r, r, n, d=th.DC)) / (th.annulus(th.cov_chance, r, r, n, d=1.0)) for r in MID]))      # cov_fixed with d = DC leaves only the count's part
    print('   n = %8d: the rest of D = %.3f (%.3f)' % (n, rest(), spread(d, rest)))

print('\nB. Measured over predicted at every size, the annuli from 0.2 to 0.8 together (mean of the 13 ratios; least and greatest; then the standard error of the mean, by resampling the clouds). The ripples here are set against the single-radius formula; see M:')
tenth = spread
for (kind, n), d in DATA.items():
    if not d: continue
    rr = [var(d['Q'][:, K(r)]) / pred_ring(kind, r, n) for r in MID]; vv = [float(d['V'][:, K(r)].mean()) / th.local(r, n) for r in MID]
    pm = {m: [float(d['P'][m][:, K(r)].mean()) / th.mode(m, r, n) for r in MID] for m in (1, 2, 3, 4)}
    e_r = tenth(d, lambda ix: np.mean([np.var(d['Q'][ix][:, K(r)], ddof=1) / pred_ring(kind, r, n) for r in MID])); e_v = tenth(d, lambda ix: np.mean([d['V'][ix][:, K(r)].mean() / th.local(r, n) for r in MID]))
    e_p = {m: tenth(d, lambda ix: np.mean([d['P'][m][ix][:, K(r)].mean() / th.mode(m, r, n) for r in MID])) for m in (1, 2, 3, 4)}
    print('   %-22s n = %8d: ring\'s mean %.3f (%.3f to %.3f; %.3f); round the ring %.3f (%.3f to %.3f; %.3f); parts 1 to 4: %s' % (NAME[kind], n, np.mean(rr), min(rr), max(rr), e_r, np.mean(vv), min(vv), max(vv), e_v, ', '.join('%.3f (%.3f to %.3f; %.3f)' % (np.mean(pm[m]), min(pm[m]), max(pm[m]), e_p[m]) for m in (1, 2, 3, 4))))

print('\nC. (Withdrawn. I had taken off the ripples "what the finite number of points in an annulus adds", the whole variance of depth in the annulus over the number of its points. The referee showed the sign to be wrong: see M and ripplecheck.out.)')

print('\nD. A random walk inward? With the number left to chance the changes of the ring\'s mean from one annulus to the next should be independent. Correlation between successive changes, annuli 0.2 to 0.8:')
for n in sizes:
    d = DATA[('chance', n)]
    if not d: continue
    inc = np.diff(d['Q'][:, K(0.2):K(0.8) + 1][:, ::-1], axis=1)          # from 0.8 inward
    cs = [float(np.corrcoef(inc[:, i], inc[:, i + 1])[0, 1]) for i in range(inc.shape[1] - 1)]
    rs = [r for r in RAD if 0.2 - 1e-9 <= r <= 0.8 + 1e-9][::-1]; C = lambda a, b: th.annulus(th.cov_chance, a, b, n); pc = []
    for i in range(len(rs) - 2):
        a, b, c = rs[i], rs[i + 1], rs[i + 2]; cov = C(a, b) - C(a, c) - C(b, b) + C(b, c); v1 = C(a, a) + C(b, b) - 2 * C(a, b); v2 = C(b, b) + C(c, c) - 2 * C(b, c); pc.append(cov / math.sqrt(v1 * v2))
    print('   n = %8d: mean of the %d correlations %+.3f (one over the root of the number of clouds is %.3f); least %+.3f, greatest %+.3f. An annulus has a width, and the mean over it of a walk with independent steps gives %+.3f' % (n, len(cs), np.mean(cs), 1 / math.sqrt(d['clouds']), min(cs), max(cs), np.mean(pc)))

print('\nE. Is the ring\'s mean bell-shaped? Skewness and excess of kurtosis across clouds at r = 0.5 (a normal sample of that size would give 0, give or take sqrt(6/clouds) and sqrt(24/clouds)):')
for (kind, n), d in DATA.items():
    if not d: continue
    z = d['Q'][:, K(0.5)]; z = (z - z.mean()) / z.std(); print('   %-22s n = %8d: %+.3f (%.3f), %+.3f (%.3f)' % (NAME[kind], n, (z ** 3).mean(), math.sqrt(6.0 / len(z)), (z ** 4).mean() - 3, math.sqrt(24.0 / len(z))))

print('\nF. The count of layers at every size (variance over n^(1/3), its standard error; predicted):')
for (kind, n), d in DATA.items():
    if d: print('   %-22s n = %8d: %.4f (%.4f); %.4f' % (NAME[kind], n, var(d['layers']) / n ** (1 / 3.0), sev(d['layers']) / n ** (1 / 3.0), th.S(1) * (th.D if kind == 'chance' else th.D - 0.75 * th.DC)))
for n in sizes:
    a, b = DATA[('chance', n)], DATA[('exact', n)]
    if a and b:
        L = b['layers'].mean(); print('   n = %8d: the two differ by %.4f; the chance in the number of points alone adds (4/9) x count^2 / n / n^(1/3) = %.4f' % (n, (var(a['layers']) - var(b['layers'])) / n ** (1 / 3.0), 4 / 9.0 * L * L / n / n ** (1 / 3.0)))

print('\nG. The width of the annulus (I had not varied it). The first 300 clouds of exactly 10^6 points, peeled again with the annulus half and twice as wide; measured over predicted (the prediction made for each width), annuli 0.2 to 0.8:')
import dlib
base = DATA.get(('exact', 10 ** 6))
if base is not None and os.path.exists(os.path.join(HERE, 'runs-width', 'exact-1000000-half0.004.jsonl')):
    first = np.array([sd <= 7000300 for sd in base['seeds']])
    for half, lab in ((0.004, 'half-width 0.004'), (0.008, 'half-width 0.008 (the sheet\'s; the same 300 clouds)'), (0.016, 'half-width 0.016')):
        if half == 0.008: q = base['Q'][first]; v = base['V'][first]; p1 = base['P'][1][first]
        else:
            rows = [json.loads(l) for l in open(os.path.join(HERE, 'runs-width', 'exact-1000000-half%g.jsonl' % half))]; a = np.array([r['rings'] for r in rows]); cnt = a[:, :, 0]; q = a[:, :, 1] / cnt
            sdd = a[:, :, 3] - a[:, :, 2] ** 2 / cnt; srr = a[:, :, 5] - a[:, :, 4] ** 2 / cnt; srd = a[:, :, 6] - a[:, :, 4] * a[:, :, 2] / cnt; v = (sdd - srd ** 2 / srr) / (cnt - 2); dbar = a[:, :, 2] / cnt
            c = 2 * (a[:, :, 9] - dbar * a[:, :, 7]) / cnt; s_ = 2 * (a[:, :, 10] - dbar * a[:, :, 8]) / cnt; p1 = (c ** 2 + s_ ** 2) / 4
        rr = np.mean([np.var(q[:, K(r)], ddof=1) / th.annulus(th.cov_fixed, r, r, 10 ** 6, half=half) for r in MID]); vv = np.mean([v[:, K(r)].mean() / th.local(r, 10 ** 6) for r in MID]); pp = np.mean([p1[:, K(r)].mean() / th.mode(1, r, 10 ** 6) for r in MID])
        print('   %-52s %d clouds: ring\'s mean %.3f; round the ring %.3f; first part %.3f' % (lab + ':', len(q), rr, vv, pp))

print('\nH. The level problem with the discs\' D. From A, the two larger samples together:')
ds = []
for n in sizes:
    d = DATA[('chance', n)]
    if d and d['clouds'] >= 1000: ds.append((d_of(d, n), spread(d, lambda ix, d=d, n=n: d_of(d, n, ix))))
if ds:
    w = [1 / e ** 2 for v, e in ds]; Dd = sum(wi * v for wi, (v, e) in zip(w, ds)) / sum(w); De = 1 / math.sqrt(sum(w)); k600 = math.sqrt(3 / (2 * math.pi * 1.3259))
    print('   IF the equation is exact on 0.2 to 0.8 of the radius, D = %.3f (%.3f) from the discs: %.1f of its standard errors from the 1.081 used.' % (Dd, De, (Dd - th.D) / De))
    print('   with that D the predictions for clouds whose number is left to chance rise by %.1f in 100; for exactly n points by %.1f, %.1f and %.1f in 100 at r = 0.2, 0.5, 0.8, and the count of layers by %.1f in 100 (%.4f to %.4f)' % (
        100 * (Dd / th.D - 1), *[100 * (th.annulus(th.cov_fixed, r, r, 10 ** 6, d=Dd) / th.annulus(th.cov_fixed, r, r, 10 ** 6) - 1) for r in (0.2, 0.5, 0.8)], 100 * ((Dd - 0.75 * th.DC) / (th.D - 0.75 * th.DC) - 1), th.S(1) * (th.D - 0.75 * th.DC), th.S(1) * (Dd - 0.75 * th.DC)))

print('\nI. Other shapes (the first study\'s clouds; no prediction of mine): the variance of the count of layers over n^(1/3)')
for name in ('polygons.jsonl',):
    R_ = [json.loads(l) for l in open(os.path.join(HERE, '..', 'runs', name)) if l.strip()]
    for shape in ('square', 'triangle'):
        out = []
        for n in sorted(set(r['n'] for r in R_ if r['shape'] == shape)):
            L = np.array([r['layers'] for r in R_ if r['shape'] == shape and r['n'] == n], float); out.append('%.3f (%.3f) at n = %d, %d clouds' % (np.var(L, ddof=1) / n ** (1 / 3.0), np.var(L, ddof=1) * math.sqrt(2.0 / (len(L) - 1)) / n ** (1 / 3.0), n, len(L)))
        print('   %-9s %s      (a disc of exactly n points: 0.081)' % (shape + ':', '; '.join(out)))

print('\nJ. A ripple at two radii. The equation says the part with m waves at an inner radius is the same part at an outer one, shrunk by (inner/outer)^(m^2/3), plus what was gathered between:')
print('   so its two amplitudes (the cos and the sin) are each correlated across clouds by (inner/outer)^(m^2/3) x sqrt(g_m(outer) / g_m(inner)), with no constant in it. Measured (standard error by resampling the clouds), predicted for two single radii, and predicted for two annuli of the width used:')
def amps(kind, n, m):
    rows = [json.loads(l) for l in lines(kind, n)]; a = np.array([r['rings'] for r in rows]); cnt = a[:, :, 0]; dbar = a[:, :, 2] / cnt
    return 2 * (a[:, :, 5 + 4 * m] - dbar * a[:, :, 3 + 4 * m]) / cnt, 2 * (a[:, :, 6 + 4 * m] - dbar * a[:, :, 4 + 4 * m]) / cnt
worstJ = (0, ''); aboveJ = [0, 0]; worstA = (0, ''); aboveA = [0]
for n in sizes:
    if not DATA.get(('exact', n)) or DATA[('exact', n)]['clouds'] < 1000: continue
    for m in (1, 2, 3):
        c, s_ = amps('exact', n, m); out = []
        for ro, ri in ((0.8, 0.3), (0.9, 0.5), (0.6, 0.2), (0.5, 0.4)):
            def cr(ix=slice(None)): return 0.5 * (np.corrcoef(c[ix][:, K(ro)], c[ix][:, K(ri)])[0, 1] + np.corrcoef(s_[ix][:, K(ro)], s_[ix][:, K(ri)])[0, 1])
            meas = float(cr()); se = spread(len(c), cr, 100); pred = (ri / ro) ** (m * m / 3.0) * math.sqrt(th.g(m, ro) / th.g(m, ri))
            pa = corr_ann(m, ro, ri, n)        # the mean over an annulus lowers both variances and hardly touches the covariance of two distant annuli
            out.append('%.1f and %.1f: %.3f (%.3f), %.3f, %.3f' % (ro, ri, meas, se, pred, pa)); aboveJ[0] += meas > pred; aboveJ[1] += 1; aboveA[0] += meas > pa
            if pred > 0.05 and abs(meas - pred) > abs(worstJ[0]): worstJ = (meas - pred, 'n = %d, %d waves, %.1f and %.1f' % (n, m, ro, ri))
            if pred > 0.05 and abs(meas - pa) > abs(worstA[0]): worstA = (meas - pa, 'n = %d, %d waves, %.1f and %.1f' % (n, m, ro, ri))
        print('   exactly n = %8d, %d wave%s:  %s' % (n, m, '' if m == 1 else 's', ';  '.join(out)))
print('   against the single-radius prediction: the largest difference, measured less predicted: %+.3f (%s); measured is above predicted in %d of the %d cases' % (worstJ + tuple(aboveJ)))
print('   against the prediction for annuli: the largest difference %+.3f (%s); measured is above it in %d of the %d (the cases share clouds and radii: they are not %d trials)' % (worstA + (aboveA[0], aboveJ[1], aboveJ[1])))

print('\nK. Every one of the 19 annuli, n = 10^6: the furthest that measured over predicted goes from 1')
for kind in ('chance', 'exact'):
    d = DATA.get((kind, 10 ** 6))
    if not d: continue
    rr = [(abs(var(d['Q'][:, k]) / pred_ring(kind, r, 10 ** 6) - 1), r) for k, r in enumerate(RAD)]; vv = [(abs(float(d['V'][:, k].mean()) / th.local(r, 10 ** 6) - 1), r) for k, r in enumerate(RAD)]
    print('   %-22s ring\'s mean: %.3f (at %.2f); round the ring: %.3f (at %.2f)' % (NAME[kind], max(rr)[0], max(rr)[1], max(vv)[0], max(vv)[1]))

print('\nL. The shortfall round a ring: a part of the whole, or a fixed amount? (The referee, in its blind step, expected a fixed amount: the sum over ripples runs to any number of waves, and the equation cannot hold for ripples shorter than a few of the local units a = (r/rho)^(1/3).)')
print('   predicted less measured, in squared layers (standard error of the measured mean, from the spread of the clouds), and as parts in 100 of the predicted; then what the sum loses if cut at r/a waves and at pi r/a waves:')
for n in sizes:
    ds = [DATA[(k, n)] for k in ('chance', 'exact') if DATA.get((k, n))]
    if not ds: continue
    out = []
    for r in (0.3, 0.5, 0.7):
        v = np.concatenate([d['V'][:, K(r)] for d in ds]); meas = float(v.mean()); se = float(v.std(ddof=1) / math.sqrt(len(v))); pred = th.local(r, n)
        a = (r / (n / math.pi)) ** (1 / 3.0); pref = 2 * th.D * (n / math.pi) ** (1 / 3.0) / (2 * math.pi)
        def tail(mc): mc = int(mc); return pref * (sum(th.g(m, r) for m in range(mc + 1, 20000)) + 1.5 * r ** (2 / 3.0) / 20000)
        out.append('r = %.1f: %.2f (%.2f), %.1f in 100; cuts %.2f and %.2f' % (r, pred - meas, se, 100 * (pred - meas) / pred, tail(r / a), tail(math.pi * r / a)))
    print('   n = %8d, both kinds (%d clouds): %s' % (n, sum(d['clouds'] for d in ds), ';   '.join(out)))

if DATA.get(('chance', 10 ** 7)) and DATA.get(('exact', 10 ** 7)):
    a_, b_ = DATA[('chance', 10 ** 7)], DATA[('exact', 10 ** 7)]; f = lambda d, ix: np.mean([d['V'][ix][:, K(r)].mean() / th.local(r, 10 ** 7) for r in MID])
    va, vb = f(a_, slice(None)), f(b_, slice(None)); ea, eb = spread(a_, lambda ix: f(a_, ix)), spread(b_, lambda ix: f(b_, ix))
    print('   n = 10^7: the two kinds of cloud should agree round the ring. Number left to chance %.3f (%.3f), exactly n %.3f (%.3f) of the predicted: they differ by %+.3f (%.3f), %.1f standard errors.' % (va, ea, vb, eb, va - vb, math.hypot(ea, eb), (va - vb) / math.hypot(ea, eb)))

print('\nM. The ripples as they were measured (after the referee). A ripple\'s amplitude is a mean over the annulus, which lowers its mean square (for a narrow annulus by D rho^(1/3) r^(-1/3) h / (6 pi), the same for every number of waves;')
print('   here the equation\'s own covariance between radii is averaged over the annulus, which is exact). And it was taken from the raw depth, whose slope across the annulus lowers it by a further third of slope^2 h^2 / (3 x points)')
print('   (the referee\'s pencil; ripplecheck.out). Measured over the equation\'s figure for the annulus less that third, annuli 0.2 to 0.8 (standard error by resampling the clouds):')
for (kind, n), d in DATA.items():
    if not d: continue
    slope = (d['tot'] - d['V']) / d['cnt']                 # slope^2 h^2 / 3 over the number of points, annulus by annulus and cloud by cloud
    MA = {(m, r): mode_ann(m, r, n) for m in (1, 2, 3, 4) for r in MID}
    def ratio(m, ix=slice(None)): return float(np.mean([d['P'][m][ix][:, K(r)].mean() / (MA[(m, r)] - slope[ix][:, K(r)].mean() / 3) for r in MID]))
    print('   %-22s n = %8d: parts 1 to 4: %s      [the two together take off %s in 100 at r = 0.5]' % (NAME[kind], n, ', '.join('%.3f (%.3f)' % (ratio(m), spread(d, lambda ix, m=m: ratio(m, ix), 100)) for m in (1, 2, 3, 4)),
          ', '.join('%.1f' % (100 * (1 - (MA[(m, 0.5)] - slope[:, K(0.5)].mean() / 3) / th.mode(m, 0.5, n))) for m in (1, 2, 3, 4))))
    if n == 10 ** 6 and kind == 'exact': print('                          at r = 0.5 alone: %s' % ', '.join('%.3f (%.3f)' % (float(d['P'][m][:, K(0.5)].mean() / (MA[(m, 0.5)] - slope[:, K(0.5)].mean() / 3)), float(d['P'][m][:, K(0.5)].std(ddof=1) / math.sqrt(d['clouds']) / MA[(m, 0.5)])) for m in (1, 2, 3, 4)))
