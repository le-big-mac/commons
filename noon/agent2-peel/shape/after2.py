"""after2.py: what was looked at after the second sheet was scored. Nothing here was sealed.   python -I after2.py
A  every set of quarter discs of this study, pooled every lawful way (the kindest to "on its line" last)
B  the new sets' mean counts against alpha rho^(2/3) T; skewness and excess kurtosis
C  the chase's cloud.c quarter discs (76,000) against the second sheet's (120,000): the same program, generator and size
D  the patient search (floorlong.py), start by start, beside the sealed search
E  after the referee's last report: the lean between 100,000 and 30,000 points, every set of exactly n points of both sheets and
   of the clouds between them pooled several lawful ways (the first sheet's 8,000 quarter discs left out throughout: they are why
   I looked); the two generators over every lawful quarter disc; and what the second sheet's bands could not have seen"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study, study2, fresh, theory
ARGV = sys.argv; sys.argv = [ARGV[0]]; import floor, floorlong; sys.argv = ARGV
LINE = study2.line_of(1e5)[0]; w, se = study.stat(lambda m, v: v / m ** 2 * 1e5, 'exact-quarter-100000')
S = {'the first sheet\'s 8,000 (cloud.c, 100,000)': (w / LINE, se / LINE, 8000, 'cloud.c', 100000, 'sheet1')}
for key, lab in (('quarter-cloud-a', 'chased: 16,000 (cloud.c, 100,000)'), ('quarter-cloud-b', 'chased: 60,000 (cloud.c, 100,000)'), ('quarter-numpy', 'chased: 60,000 (numpy, 100,000)')):
    f = fresh.reckon(key); S[lab] = (f['w'] / LINE, f['wse'] / LINE, f['K'], f['maker'], 100000, 'chase')
for key, (name, n) in study2.SETS.items(): v = study2.R[key]; S['the second sheet: 120,000 (%s)' % key] = (v['r'], v['rse'], v['K'], 'cloud.c' if key.startswith('cloud') else 'numpy', n, 'sheet2')
print('A  quarter discs: r = spread of the count over the theory\'s, set by set, and pooled')
for lab, v in S.items(): print('   %-46s %.4f (%.4f)' % (lab, v[0], v[1]))
def line(label, pick):
    sel = [(v[0], v[1]) for v in S.values() if pick(v)]; K = sum(v[2] for v in S.values() if pick(v)); m, s, chi = fresh.pool(sel)
    print('   %-78s %d sets, %7s clouds: %.4f (%.4f), %+.1f errors from 1; chi-square among them %.1f on %d' % (label, len(sel), format(K, ','), m, s, (m - 1) / s, chi, len(sel) - 1)); return m, s
line('every set', lambda v: True)
line('every set but the first sheet\'s 8,000 (which is why I looked)', lambda v: v[5] != 'sheet1')
line('the chase alone (three sets)', lambda v: v[5] == 'chase')
line('the second sheet alone (four sets, sealed)', lambda v: v[5] == 'sheet2')
line('cloud.c, 100,000 points, all', lambda v: v[3] == 'cloud.c' and v[4] == 100000)
line('cloud.c, 100,000 points, without the first 8,000', lambda v: v[3] == 'cloud.c' and v[4] == 100000 and v[5] != 'sheet1')
line('numpy, 100,000 points, all', lambda v: v[3] == 'numpy' and v[4] == 100000)
line('30,000 points (two sets)', lambda v: v[4] == 30000)
line('100,000 points, without the first 8,000', lambda v: v[4] == 100000 and v[5] != 'sheet1')
print()
print('B  the second sheet\'s sets: the mean count over alpha rho^(2/3) T, in parts of 10,000; skewness and excess kurtosis (errors sqrt(6/K), sqrt(24/K))')
for key, (name, n) in study2.SETS.items():
    v = study2.R[key]; x = fresh.counts(name); z = (x - x.mean()) / x.std()
    print('   %-18s mean %+.2f (%.2f)   skewness %+.3f (%.3f)   kurtosis %+.3f (%.3f)' % (key, (v['m'] / v['theory_m'] - 1) * 1e4, v['mse'] / v['theory_m'] * 1e4, (z ** 3).mean(), math.sqrt(6 / len(x)), (z ** 4).mean() - 3, math.sqrt(24 / len(x))))
print()
a = fresh.reckon('quarter-cloud'); b = study2.R['cloud.c, 100,000']; ra, sa = a['w'] / LINE, a['wse'] / LINE
print('C  cloud.c\'s quarter discs of 100,000 points: the chase\'s 76,000 gave %.4f (%.4f), the second sheet\'s 120,000 gave %.4f (%.4f): %.1f errors apart' % (ra, sa, b['r'], b['rse'], (ra - b['r']) / math.hypot(sa, b['rse'])))
print('   the two together, 196,000 clouds: %.4f (%.4f)' % fresh.pool([(ra, sa), (b['r'], b['rse'])])[:2])
print()
print('D  the searches: where each start ended')
sealed = json.load(open(os.path.join(HERE, 'floor.json')))['runs']
def shape_of(x):
    d = floor.describe(np.array(x)); per = sum(L for a_, L in d['sides']); big = sorted([(a_, L / per) for a_, L in d['sides'] if L / per > 0.03]); angs = sorted(round((big[(i + 1) % len(big)][0] - big[i][0]) % 360) for i in range(len(big)))
    return len(big), len(d['sides']), d['rho'], [180 - a_ for a_ in angs]
print('   search   start  from                                             Q at the start   least (240 angles)   generations   at 1,440 angles   sides over 3 in 100 (all)   rho     corners (degrees)')
for r in sealed:
    nb, na, rho, cor = shape_of(r['x']); print('   sealed   %-2d     %-48s %.5f          %.5f              %3d           %s           %d (%d)                     %.3f   %s' % (r['seed'], r['start'], r['start_Q'], r['best_Q'], r['generations'], ('%.5f' % r['fine_Q']) if 'fine_Q' in r else '   -   ', nb, na, rho, ', '.join(str(c) for c in cor)))
long = [json.load(open(os.path.join(HERE, 'floorlong-%d.json' % k))) for k in range(1, 11) if os.path.exists(os.path.join(HERE, 'floorlong-%d.json' % k))]
for r in long:
    nb, na, rho, cor = shape_of(r['x']); print('   patient  %-2d     %-48s %.5f          %.5f              %3d           %.5f           %d (%d)                     %.3f   %s' % (r['seed'], r['start'], r['start_Q'], r['best_Q'], r['generations'], r['fine_Q'], nb, na, rho, ', '.join(str(c) for c in cor)))
if long:
    allf = [(r['fine_Q'], 'sealed %d' % r['seed']) for r in sealed if 'fine_Q' in r] + [(r['fine_Q'], 'patient %d' % r['seed']) for r in long]; print('   %d of the patient search\'s ten starts are in. The least of both searches at 1,440 angles: %.5f (%s); the next: %.5f (%s)' % ((len(long),) + sorted(allf)[0] + sorted(allf)[1]))
    print('   ended at a triangle with round corners: %d of the sealed search\'s 8 starts, %d of the patient search\'s %d' % (sum(1 for r in sealed if shape_of(r['x'])[0] == 3), sum(1 for r in long if shape_of(r['x'])[0] == 3), len(long)))

print()
print('E  measured over each set\'s own line, sets weighted together; the lean is the figure at 100,000 less the figure at 30,000')
F1 = {n: v for n, v in study.F.items() if v is not None and n.startswith('exact-')}
def r1(n): sh = n.split('-')[1]; sh = 'disc' if sh == 'disc0' else sh; n0 = F1[n]['n0']; p = theory.predictions(sh, n0); ln = p['exact'] / p['mean'] ** 2 * n0; w_, s_ = study.stat(lambda m_, v_: v_ / m_ ** 2 * n0, n); return (w_ / ln, s_ / ln)
def rf(k): f = fresh.reckon(k); return (f['w'] / f['line'], f['wse'] / f['line'])
q2 = {k: (v['r'], v['rse']) for k, v in study2.R.items()}
other5 = [r1(n) for n in F1 if n.endswith('-100000') and 'quarter' not in n] + [rf(k) for k in ('disc-cloud', 'halfdisc-cloud', 'disc-peel', 'square-peel', 'triangle-peel')]; other3 = [r1(n) for n in F1 if n.endswith('-30000')]
qs5 = [q2['cloud.c, 100,000'], q2['numpy, 100,000']]; qs3 = [q2['cloud.c, 30,000'], q2['numpy, 30,000']]; chase = [rf('quarter-cloud-a'), rf('quarter-cloud-b'), rf('quarter-numpy')]
like5 = [r1('exact-%s-100000' % s_) for s_ in ('disc', 'triangle', 'rtriangle')]
print('   what                                                              sets   at 100,000          at 30,000           the lean            in its errors')
LEAN = {}
for lab, a_, b_ in (('quarter discs, the second sheet\'s only', qs5, qs3), ('quarter discs, with the chase', qs5 + chase, qs3), ('other shapes, every set', other5, other3), ('other shapes, the three run at both sizes on the first sheet', like5, other3),
                    ('the second sheet\'s quarter discs and the other shapes', qs5 + other5, qs3 + other3), ('everything', qs5 + chase + other5, qs3 + other3)):
    ma, sa_, _ = fresh.pool(a_); mb, sb_, _ = fresh.pool(b_); LEAN[lab] = (ma, sa_, mb, sb_, ma - mb, math.hypot(sa_, sb_), len(a_) + len(b_))
    print('   %-64s  %2d     %.4f (%.4f)     %.4f (%.4f)     %+.4f (%.4f)    %.1f' % (lab, len(a_) + len(b_), ma, sa_, mb, sb_, ma - mb, math.hypot(sa_, sb_), (ma - mb) / math.hypot(sa_, sb_)))
ev = LEAN['everything']; print('   everything at 100,000 stands %.2f (%.2f) in 100 above the theory, %.1f errors; at 30,000 %.2f (%.2f) below, %.1f errors' % ((ev[0] - 1) * 100, ev[1] * 100, (ev[0] - 1) / ev[1], (1 - ev[2]) * 100, ev[3] * 100, (1 - ev[2]) / ev[3]))
c1 = theory.predictions('disc', 1.0)['exact']; b_over = ev[4] / (30000 ** (-1 / 3.0) - 100000 ** (-1 / 3.0)); top = ev[0] + b_over * 100000 ** (-1 / 3.0); Dp = (top * (4 / 3.0 * theory.D - theory.DC) + theory.DC) * 0.75
print('   if the lean is a constant taken from the variance (variance = c n^(1/3) - b): b = %.3f for a disc, and the level for very many points %.3f of the theory\'s, which is D = %.3f in place of %.3f' % (b_over * c1, top, Dp, theory.D))
print('      (the second addition read D = 1.095 (0.016) from the insides of discs); at 10,000 points that reading puts the level at %.3f, at 1,000,000 at %.3f' % (top - b_over * 10000 ** (-1 / 3.0), top - b_over * 1e6 ** (-1 / 3.0)))
gc, gcs, _ = fresh.pool([rf('quarter-cloud-a'), rf('quarter-cloud-b'), q2['cloud.c, 100,000'], q2['cloud.c, 30,000']]); gn, gns, _ = fresh.pool([rf('quarter-numpy'), q2['numpy, 100,000'], q2['numpy, 30,000']])
print('   the two generators over every quarter disc but the first 8,000: cloud.c %.4f (%.4f) less numpy %.4f (%.4f) = %+.4f (%.4f), %.1f errors' % (gc, gcs, gn, gns, gc - gn, math.hypot(gcs, gns), (gc - gn) / math.hypot(gcs, gns)))
g2, g2s, _ = fresh.pool([rf('quarter-cloud-b'), q2['cloud.c, 100,000']]); print('   cloud.c\'s quarter discs of 100,000 points without the first 8,000 and without the 16,000 that sent me for more: %.4f (%.4f), %.1f errors up' % (g2, g2s, (g2 - 1) / g2s))
from statistics import NormalDist
N = NormalDist(); hold = lambda mu, se_, lo, hi: N.cdf((hi - mu) / se_) - N.cdf((lo - mu) / se_)
t4 = study2.together(study2.ALL); dse = math.hypot(study2.together(['cloud.c, 100,000', 'cloud.c, 30,000'])[1], study2.together(['numpy, 100,000', 'numpy, 30,000'])[1]); s4 = study2.R['cloud.c, 100,000']['rse']
print('   what the bands could not have seen: A1 holds %.0f times in 100 if r is truly 1.005; A2 or A3 %.0f times in 100 if the difference is truly 0.006; A4 %.0f times in 100 if r is truly 1.007' % (100 * hold(1.005, t4[1], 0.996, 1.008), 100 * hold(0.006, dse, -0.010, 0.010), 100 * hold(1.007, s4, 0.992, 1.012)))
