"""far/after.py: what I looked at after the verdicts (nothing here was sealed).   python -I after.py > after.out   (or: python -I after.py try)
It runs study.py first, silently, and uses its windows and its functions, so that nothing is defined twice."""
import contextlib, io, math, os, runpy, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()): G = runpy.run_path(os.path.join(HERE, 'study.py'))
W, SHORT, LONG, LOW, TALL, SC, THICK, H4, H2 = (G[k] for k in ('W', 'SHORT', 'LONG', 'LOW', 'TALL', 'SC', 'THICK', 'H4', 'H2'))
pool, expo, boot, ratio, slope_of, ms, wander, offsets_at, PERIOD, STEP, FIRST, NEAR, K600 = (G[k] for k in ('pool', 'expo', 'boot', 'ratio', 'slope_of', 'ms', 'wander', 'offsets_at', 'PERIOD', 'STEP', 'FIRST', 'NEAR', 'K600'))
ALPHA = 1.3259
S1S = [w for w in SHORT if w['seeding'] == 1]; S1T = [w for w in LONG if w['seeding'] == 1]; S2T = [w for w in LONG if w['seeding'] == 2]
GROUPS = [g for g in (('first batch, to %d' % LOW, S1S), ('first batch, to %d' % TALL, S1T), ('second batch, to %d' % TALL, S2T)) if len(g[1]) >= 2]
def dens(w, lo, hi): return float(w['c'][lo:hi].sum() / (PERIOD * (hi - lo)))
def fm(v): m, s = ms(v); return '%.6f (%.6f)' % (m, s)

print('A. The two batches side by side (the first started every column\'s random stream in a way that let neighbours share starting words; the second did not)')
for nm, S in GROUPS:
    y, mu, v = pool(S, LOW)
    print('   %-26s %2d windows: exponent of the variance %d to %d: %.3f; variance over root depth at %d: %.3f; slope of mean depth over %d to %d: %s' % (
        nm + ':', len(S), H4, LOW, expo(y, v - THICK, H4, LOW, 'steps'), LOW, ratio(S, LOW, 0.01), LOW // 2, LOW, fm(slope_of(w, LOW / 2, LOW) for w in S)))
zs = [(w['c'].sum() - PERIOD * w['HM']) / math.sqrt(PERIOD * w['HM']) for w in W]
print('   points in each window against the area (in standard deviations of a count of independent points): %s' % ', '.join('%+.1f' % z for z in zs))
print('      sum of their squares %.1f for %d windows; mean %+.2f' % (sum(z * z for z in zs), len(zs), np.mean(zs)))

print('\nB. The constant')
print('   each window\'s slope over its upper half goes with how many points that half happened to hold:')
for nm, S in (('windows to %d' % LOW, SHORT), ('windows to %d' % TALL, LONG)):
    if len(S) < 3: continue
    sl = np.array([w['slope'] for w in S]); rho = np.array([dens(w, w['HM'] // 2, w['HM']) for w in S]); b, a = np.polyfit(rho - 1, sl, 1); res = sl - (a + b * (rho - 1))
    print('   %-18s correlation %.2f; slope = %.6f + %.3f x (density - 1), where (2/3) x 1.3259 = 0.884; spread of the slopes %.6f, and about that line %.6f' % (nm + ':', np.corrcoef(rho, sl)[0, 1], a, b, sl.std(ddof=1), res.std(ddof=len(S) - (len(S) - 2))))
def corrected(w, lo=None, hi=None):
    lo = lo if lo is not None else w['HM'] // 2; hi = hi if hi is not None else w['HM']; return slope_of(w, lo, hi) / dens(w, lo, hi) ** (2.0 / 3)
rows = [('the %d windows to %d' % (len(SHORT), LOW), [w['slope'] for w in SHORT], [corrected(w) for w in SHORT]),
        ('the %d windows to %d' % (len(LONG), TALL), [w['slope'] for w in LONG], [corrected(w) for w in LONG]),
        ('all %d, each its upper half' % len(W), [w['slope'] for w in W], [corrected(w) for w in W]),
        ('all %d over %d to %d' % (len(W), LOW // 2, LOW), [slope_of(w, LOW / 2, LOW) for w in W], [corrected(w, LOW // 2, LOW) for w in W]),
        ('all %d over %d to %d' % (len(W), H4, LOW), [slope_of(w, H4, LOW) for w in W], [corrected(w, H4, LOW) for w in W]),
        ('the %d tall over %d to %d' % (len(LONG), H4, TALL), [slope_of(w, H4, TALL) for w in LONG], [corrected(w, H4, TALL) for w in LONG])]
for nm, S in GROUPS:
    if S != SHORT and S != LONG: rows.append((nm, [w['slope'] for w in S], [corrected(w) for w in S]))      # a batch that is one of the sets above is not listed twice
def endtoend(w, h0, h1):
    y = np.arange(w['HM']) + 0.5; a = slice(h0 - NEAR, h0); b = slice(h1 - NEAR, h1)
    da = (w['c'][a] * w['mu'][a]).sum() / w['c'][a].sum(); db = (w['c'][b] * w['mu'][b]).sum() / w['c'][b].sum()
    ya = (w['c'][a] * y[a]).sum() / w['c'][a].sum(); yb = (w['c'][b] * y[b]).sum() / w['c'][b].sum(); return float((db - da) / (yb - ya))
def endcorr(w, h0, h1): return endtoend(w, h0, h1) / dens(w, h0 - NEAR // 2, h1 - NEAR // 2) ** (2.0 / 3)
rows.append(('end to end, all %d, %d to top' % (len(W), H4), [endtoend(w, H4, w['HM']) for w in W], [endcorr(w, H4, w['HM']) for w in W]))
rows.append(('end to end, all %d, %d to %d' % (len(W), H4, LOW), [endtoend(w, H4, LOW) for w in W], [endcorr(w, H4, LOW) for w in W]))
rows.append(('end to end, %d tall, %d to %d' % (len(LONG), H4, TALL), [endtoend(w, H4, TALL) for w in LONG], [endcorr(w, H4, TALL) for w in LONG]))
rows.append(('end to end, %d tall, %d to %d' % (len(LONG), LOW, TALL), [endtoend(w, LOW, TALL) for w in LONG], [endcorr(w, LOW, TALL) for w in LONG]))
print('   every pooling I can think of: the slope as it is, and the slope divided by (density of the same stretch)^(2/3) (mean, standard error from the spread of the windows);')
print('   "end to end" is the rise of the mean depth between two heights (%d bands below each) over the height between:' % NEAR)
for nm, a, b in rows: print('      %-34s %s      %s' % (nm + ':', fm(a), fm(b)))
plain = [ms(a)[0] for nm, a, b in rows]; corr = [ms(b)[0] for nm, a, b in rows]
print('   as they are the poolings run from %.6f to %.6f; with the density taken out, from %.6f to %.6f. The study beside this folder gave 1.3259 +- 0.0001.' % (min(plain), max(plain), min(corr), max(corr)))
print('   the slope doubling by doubling (mean over the windows that reach, standard error), as it is and with the density taken out:')
e = H2 // 2
while e * 2 <= TALL:
    S = W if e * 2 <= LOW else LONG
    print('      %6d to %6d (%2d windows): %s      %s' % (e, e * 2, len(S), fm(slope_of(w, e, e * 2) for w in S), fm(corrected(w, e, e * 2) for w in S))); e *= 2

print('\nC. The variance of depth at a height, all windows that reach')
print('   height, variance, over root depth, over height^(1/2), over height^(2/3) (the last two as multiples of their values at %d)' % H4)
y, mu, v = pool(W, TALL); v = v - THICK
def at(h): n = max(2, int(0.01 * h)); return float(v[h - n:h].mean()), float(mu[h - n:h].mean())
v4 = at(H4)[0]; h = H4 // 8
while h <= TALL:
    vv, dd = at(h); print('      %6d  %7.2f   %.3f   %.3f   %.3f' % (h, vv, vv / math.sqrt(dd), (vv / math.sqrt(h)) / (v4 / math.sqrt(H4)), (vv / h ** (2 / 3.0)) / (v4 / H4 ** (2 / 3.0)))); h *= 2
for lo, hi in ((H4 // 4, H4), (H4, LOW), (H4, TALL), (LOW // 4, TALL), (LOW, TALL)):
    S = W if hi <= LOW else LONG; yy, m_, vv = pool(S, hi); e1 = expo(yy, vv - THICK, lo, hi, 'steps')
    iv = boot(S, lambda SS: expo(*[pool(SS, hi)[i] for i in (0, 2)], lo, hi, 'steps'))
    print('   exponent over %6d to %6d (%2d windows): %.3f   [95%% of resamplings of the windows: %.3f to %.3f]' % (lo, hi, len(S), e1, iv[0], iv[1]))

def ex3(S, lo, hi): yy_, mm_, vv_ = pool(S, hi); return expo(yy_, vv_ - THICK, lo, hi, 'steps')
print('   line A3, the last doubling, by batch (steps): %s' % '; '.join('%s, %d to %d: %.3f%s' % (nm, lo, hi, ex3(S, lo, hi), ' (window by window %s)' % ', '.join('%.3f' % expo(np.arange(w['HM']) + 0.5, w['var'] - THICK, lo, hi, 'steps') for w in S) if len(S) <= 3 else '')
      for nm, S, lo, hi in (('the first batch\'s %d tall windows' % len(S1T), S1T, TALL // 2, TALL), ('the second batch\'s %d' % len(S2T), S2T, TALL // 2, TALL), ('the first batch\'s %d short' % len(S1S), S1S, LOW // 2, LOW)) if len(S) >= 2))
print('\nD. The wander of a window\'s mean depth, and the count of points')
ch = []; dn = []
for w in W:
    off = offsets_at(w); nodes = list(range(FIRST, w['HM'] + 1, STEP))
    for i in range(len(nodes) - 1):
        ch.append(off[i + 1] - off[i]); dn.append((w['c'][nodes[i] - NEAR // 2:nodes[i + 1] - NEAR // 2].sum() - PERIOD * STEP) / PERIOD)
ch = np.array(ch); dn = np.array(dn); b0 = float((ch * dn).mean() / (dn * dn).mean())
b = float(np.cov(ch, dn, ddof=1)[0, 1] / dn.var(ddof=1)); res = (ch - ch.mean()) - b * (dn - dn.mean()); seb = math.sqrt(res.var(ddof=2) / ((len(ch) - 1) * dn.var(ddof=1)))
Dall = PERIOD * ch.var(ddof=1) / STEP; Dn = PERIOD * dn.var(ddof=1) / STEP
print('   %d changes over steps of %d. D (period x variance of the changes / step) = %.3f.' % (len(ch), STEP, Dall))
print('   the same for the excess of points in the stretch between (per unit of width): %.3f, where independent points give 1.' % Dn)
print('   correlation of the two %.3f; a change of %.3f (%.3f) layers for each excess point per unit width (the slope of the one on the other, about their means), where (2/3) x 1.3259 = 0.884 is what the density alone would do.' % (np.corrcoef(ch, dn)[0, 1], b, seb))
print('      (a line through the origin gives %.3f: the changes have a mean of %+.3f a step, because the offsets are taken with 1.3259 and the slope is 1.32596; that was my first figure, and the referee showed it was lifted.)' % (b0, ch.mean()))
print('   so of D = %.3f, the count of points carries %.3f and %.3f is left (the arrangement of the points).' % (Dall, Dall - PERIOD * res.var(ddof=1) / STEP, PERIOD * res.var(ddof=1) / STEP))
print('   independent points, each adding (2/3) x 1.3259 layers per unit of width, would carry (4/9) x 1.3259^2 = %.3f.' % (4 / 9.0 * 1.3259 ** 2))
print('   %.3f D = %.3f, against the variance of depth over root depth: %s' % (K600, K600 * Dall, ', '.join('%.3f at %d' % (ratio(W if h <= LOW else LONG, h, 0.01), h) for h in (H4, LOW // 4, LOW, TALL))))
# three small corrections, which the referee's blind step showed me how to compute
samp = []
for w in W:
    nodes = list(range(FIRST, w['HM'] + 1, STEP)); sg = [float((w['var'][h - NEAR:h] - THICK).mean()) for h in nodes]
    samp += [(sg[i] + sg[i + 1]) / (NEAR * STEP) for i in range(len(nodes) - 1)]
samp = float(np.mean(samp)); damp = 1 - NEAR / (3.0 * STEP); Dc = (Dall - samp) / damp
print('   corrections to D. The mean of a band is taken at the random places of its points, which adds (variance at one end + variance at the other) / (band x step) to D: %.4f here (band %d, step %d).' % (samp, NEAR, STEP))
print('      A band %d thick averages the walk over its thickness, which multiplies D by 1 - band / (3 x step) = %.4f. With both: D = %.3f, and %.3f D = %.3f.' % (NEAR, damp, Dc, K600, K600 * Dc))
for h in (LOW, TALL):
    S = W if h <= LOW else LONG; yy, mm, vv = pool(S, h); n = max(2, int(0.01 * h)); meas = float((vv[h - n:h] - THICK).mean()); dep = float(mm[h - n:h].mean()); ring = Dc * (h - n / 2.0) / PERIOD
    print('      at %d: the variance measured about each window\'s own mean is %.2f; the equation gives %.3f D sqrt(depth) = %.2f for the whole line, less D y / period = %.2f for the ring\'s own mean: %.2f. Predicted over measured: %.3f' % (
        h, meas, K600, K600 * Dc * math.sqrt(dep), ring, K600 * Dc * math.sqrt(dep) - ring, (K600 * Dc * math.sqrt(dep) - ring) / meas))
print('   a random walk? D from steps of %s' % ', '.join('%d: %.3f (%d changes)' % ((st,) + wander(W, st)) for st in (STEP // 8, STEP // 4, STEP // 2, STEP, STEP * 2, STEP * 4)))
def dcorr(st):
    sm = []
    for w in W:
        nodes = list(range(FIRST, w['HM'] + 1, st)); sg = [float((w['var'][h - NEAR:h] - THICK).mean()) for h in nodes]; sm += [(sg[i] + sg[i + 1]) / (NEAR * st) for i in range(len(nodes) - 1)]
    return (wander(W, st)[0] - float(np.mean(sm))) / (1 - NEAR / (3.0 * st))
print('      with the two corrections above made at each step: %s' % ', '.join('%d: %.3f' % (st, dcorr(st)) for st in (STEP // 8, STEP // 4, STEP // 2, STEP, STEP * 2, STEP * 4)))

if G.get('SNAP'):
    SNAP, hs, sk, ku, va, gcurve, reach, LAGS, wcol = (G[k] for k in ('SNAP', 'hs', 'sk', 'ku', 'va', 'gcurve', 'reach', 'LAGS', 'wcol'))
    def shape(s): return 1 - math.exp(-s * s) + s * math.sqrt(math.pi) * math.erfc(s)
    print('\nE. The slabs of the second batch (%d windows)' % len(SNAP))
    print('   skewness and excess of kurtosis of the column means, every second slab (mean over the windows and its standard error):')
    for h in hs:
        if h >= 250 // SC and hs.index(h) % 2 == 0: print('      %6d: %+.3f (%.3f)   %+.3f (%.3f)' % (h, np.mean(sk[h]), np.std(sk[h], ddof=1) / math.sqrt(len(sk[h])), np.mean(ku[h]), np.std(ku[h], ddof=1) / math.sqrt(len(ku[h]))))
    for lo, hi in ((1000 // SC, 4000 // SC), (4000 // SC, 16000 // SC), (16000 // SC, 64000 // SC), (64000 // SC, TALL)):
        hh = [h for h in hs if lo <= h < hi]
        if not hh: continue
        per = [float(np.mean([sk[h][i] for h in hh])) for i in range(len(SNAP))]
        print('   skewness over the slabs from %d to under %d (%d slabs): %+.4f (%.4f, from the %d windows)' % (lo, hi, len(hh), np.mean(per), np.std(per, ddof=1) / math.sqrt(len(per)), len(per)))
    print('   the mean square difference between columns r apart, over twice the variance times the shape 1 - exp(-s^2) + s sqrt(pi) erfc(s), s = r / sqrt(8 y / 3):')
    print('      height   ' + ' '.join('%6d' % (j * wcol) for j in LAGS if j >= 2))
    for k, h in enumerate(hs):
        if k % 8 == 0 and h >= 1000 // SC:
            g, plateau = gcurve(k); print('      %6d   ' % h + ' '.join('%6.3f' % (g[i] / (plateau * shape(LAGS[i] * wcol / math.sqrt(8 * (h + 2) / 3.0)))) for i in range(len(LAGS)) if LAGS[i] >= 2))
    worst = (0, 0, 0); nsl = 0
    for k, h in enumerate(hs):
        if h >= 1000 // SC:
            g, plateau = gcurve(k); nsl += 1
            for i in range(len(LAGS)):
                if LAGS[i] * wcol >= 48:
                    d = g[i] / (plateau * shape(LAGS[i] * wcol / math.sqrt(8 * (h + 2) / 3.0))) - 1
                    if abs(d) > abs(worst[0]): worst = (d, h, LAGS[i] * wcol)
    print('   over all %d slabs from %d up and every distance from 48 to %d: the measured value is furthest from the predicted, by %+.3f of it, at height %d and %d apart' % (nsl, 1000 // SC, LAGS[-1] * wcol, worst[0], worst[1], worst[2]))
    rh = [(h + 2, reach(k)) for k, h in enumerate(hs) if h >= 1000 // SC]; p = np.polyfit(np.log([a for a, b in rh]), np.log([b for a, b in rh]), 1)
    print('   the reach as a power of the height over %d to %d: exponent %.3f (one half for this kind of front, two thirds for the other); the smoothing constant it implies, (reach / 0.3497)^2 / (8 y): %s' % (
        rh[-1][0], rh[0][0], p[0], ', '.join('%.3f at %d' % ((b / 0.3497) ** 2 / (8 * a), a) for a, b in rh[::8])))
    print('   variance of the column means of a slab against the variance of depth in the bands at the same height (the same windows): ' + ', '.join(
        '%.1f and %.1f at %d' % (va[h], np.mean([w['var'][h:h + 4].mean() - THICK for w in SNAP]), h) for h in hs[::8] if h >= 1000 // SC))
