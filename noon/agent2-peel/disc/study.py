"""disc/study.py: the twelve sealed lines of expectations.md, each computed from runs/ and judged by its letter.
   python -I study.py > study.out
   DISC_RUNS=DIR python -I study.py      the tables only, for whatever sizes are in DIR (to try the script on small clouds)
Each line of runs/KIND-N.jsonl is one cloud (rings.c): for each of 19 annuli (radius 0.05, 0.10, ..., 0.95, each +- 0.008) the sums
[points, depth - profile, depth, depth^2, rho, rho^2, rho x depth, then for m = 1..4: cos, sin, depth x cos, depth x sin of m theta]."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dtheory as th
from dlib import RUNS, TRY, RAD, K, load, var, sev, corr, secorr, pred_ring, pred_corr, sizes_in, NAME
sizes = sizes_in()
DATA = {(kind, n): load(kind, n) for kind in ('chance', 'exact') for n in sizes}
print('The clouds: ' + '; '.join('%s, n = %d: %d clouds (points in a cloud %d to %d; in the annulus at 0.5 about %d)' % (NAME[k], n, d['clouds'], d['npts'].min(), d['npts'].max(), d['cnt'][:, K(0.5)].mean()) for (k, n), d in DATA.items() if d))
print('D = %.3f, its part that is the count of points %.3f. Predicted values are dtheory.py\'s, for the annulus as measured.\n' % (th.D, th.DC))
for (kind, n), d in DATA.items():
    if not d: continue
    print('%s, n = %d, %d clouds.   radius | variance of the ring\'s mean: measured (its standard error), predicted, ratio | variance round the ring: measured, predicted, ratio | parts m = 1, 2, 3, 4: measured over predicted' % (NAME[kind], n, d['clouds']))
    for k, r in enumerate(RAD):
        q = d['Q'][:, k]; v = float(d['V'][:, k].mean()); pr = pred_ring(kind, r, n); pl = th.local(r, n)
        print('   %.2f | %8.3f (%.3f)  %8.3f  %.3f | %7.2f  %7.2f  %.3f | %s' % (r, var(q), sev(q), pr, var(q) / pr, v, pl, v / pl, '  '.join('%.3f' % (float(d['P'][m][:, k].mean()) / th.mode(m, r, n)) for m in (1, 2, 3, 4))))
    L = d['layers']; print('   the count of layers: mean %.2f, variance %.3f, over n^(1/3) %.4f (%.4f); predicted %.4f' % (L.mean(), var(L), var(L) / n ** (1 / 3.0), sev(L) / n ** (1 / 3.0), th.S(1) * (th.D if kind == 'chance' else th.D - 0.75 * th.DC)))
    print('   the ring\'s means at two radii, correlation across clouds, measured (standard error by resampling the clouds) and predicted: ' + '; '.join('%.1f and %.1f: %.3f (%.3f), %.3f' % (a, b, corr(d, a, b), secorr(d, a, b, 200), pred_corr(kind, a, b, n)) for a, b in ((0.8, 0.3), (0.9, 0.5), (0.6, 0.2), (0.5, 0.1))))
    print()
if TRY: sys.exit(0)

# ---------- the verdicts, by the letter of the sheet ----------
verdicts = []
def line(n, kind, odds, held, text):
    verdicts.append((n, kind, odds, held)); print('LINE C%d (%s, odds %s): %s. %s\n' % (n, kind, odds, {True: 'HELD', False: 'FAILED', None: 'HALF'}[held], text))
M = 10 ** 6; CH, EX = DATA[('chance', M)], DATA[('exact', M)]
assert [DATA[(k, n)]['clouds'] for k in ('chance', 'exact') for n in (10 ** 5, 10 ** 6, 10 ** 7)] == [4000, 2000, 200] * 2, 'the design of the sheet'
def within(meas, want, tol): return abs(meas / want - 1) <= tol
def show(vals, wants): return ', '.join('%.2f against %s (%+.0f in 100)' % (v, w, 100 * (v / float(w) - 1)) for v, w in zip(vals, wants))
R5 = (0.2, 0.35, 0.5, 0.65, 0.8)
v1 = [var(CH['Q'][:, K(r)]) for r in R5]; w1 = ('11.54', '8.82', '6.48', '4.36', '2.40')
line(1, 'worked', 0.7, all(within(v, float(w), 0.15) for v, w in zip(v1, w1)), 'number left to chance, n = 10^6, the variance of the ring\'s mean at r = 0.2, 0.35, 0.5, 0.65, 0.8: %s; the line asked for within 15 in 100 at every one. (Each measured variance is good to about %.0f in 100.)' % (show(v1, w1), 100 * math.sqrt(2.0 / 1999)))
v2 = [var(EX['Q'][:, K(r)]) for r in R5]; w2 = ('4.09', '3.40', '3.01', '2.54', '1.77')
line(2, 'worked', 0.6, all(within(v, float(w), 0.25) for v, w in zip(v2, w2)), 'exactly n = 10^6: %s; the line asked for within 25 in 100 at every one.' % show(v2, w2))
r3 = var(EX['Q'][:, K(0.5)]) / var(CH['Q'][:, K(0.5)])
line(3, 'worked', 0.7, 0.40 <= r3 <= 0.54, 'at r = 0.5 the variance with exactly n points is %.3f of the variance with the number left to chance (0.464 predicted; each variance is good to 3 in 100, so the ratio to about 0.02); the line asked for 0.40 to 0.54.' % r3)
c4a, c4b = corr(CH, 0.8, 0.3), corr(EX, 0.8, 0.3)
line(4, 'worked', 0.65, 0.44 <= c4a <= 0.57 and 0.08 <= c4b <= 0.30, 'the ring\'s means at r = 0.8 and r = 0.3 are correlated by %.3f (%.3f) with the number left to chance, where the line asked for 0.44 to 0.57 (0.505 predicted), and by %.3f (%.3f) with exactly n points, where it asked for 0.08 to 0.30 (0.187 predicted).' % (c4a, secorr(CH, 0.8, 0.3), c4b, secorr(EX, 0.8, 0.3)))
v5 = [(n, var(DATA[('chance', n)]['Q'][:, K(0.5)]) / n ** (1 / 3.0), sev(DATA[('chance', n)]['Q'][:, K(0.5)]) / n ** (1 / 3.0)) for n in (10 ** 5, 10 ** 6, 10 ** 7)]
line(5, 'worked', 0.65, all(within(q, 0.0648, 0.20) for n, q, s in v5), 'number left to chance, r = 0.5: the variance of the ring\'s mean over n^(1/3) is %s; the line asked for within 20 in 100 of 0.0648 at each.' % '; '.join('%.4f (%.4f) at n = %d (%+.0f in 100)' % (q, s, n, 100 * (q / 0.0648 - 1)) for n, q, s in v5))
v6 = [float(EX['V'][:, K(r)].mean()) for r in (0.3, 0.5, 0.7)]; w6 = ('24.0', '25.0', '22.3')
line(6, 'worked', 0.55, all(within(v, float(w), 0.15) for v, w in zip(v6, w6)), 'exactly n = 10^6, the variance round the ring at r = 0.3, 0.5, 0.7: %s; the line asked for within 15 in 100 at every one.' % show(v6, w6))
v7 = [float(EX['P'][m][:, K(0.5)].mean()) for m in (1, 2, 3)]; w7 = ('5.13', '2.78', '1.35')
line(7, 'worked', 0.6, all(within(v, float(w), 0.20) for v, w in zip(v7, w7)), 'exactly n = 10^6, r = 0.5, the first, second and third parts: %s; the line asked for within 20 in 100 at every one.' % show(v7, w7))
v8 = var(CH['Q'][:, K(0.9)]); l8 = [float(d['V'][:, K(0.9)].mean()) for d in (CH, EX)]; ok8 = [within(v8, 1.16, 0.15) and within(l, 14.6, 0.15) for l in l8]
line(8, 'guessed', 0.5, True if all(ok8) else False if not any(ok8) else None, 'at r = 0.9, n = 10^6: the variance of the ring\'s mean (number left to chance) is %.3f against 1.16 (%+.0f in 100); the variance round the ring is %.2f with the number left to chance and %.2f with exactly n, against 14.6 (%+.0f and %+.0f in 100; the sheet does not say which kind). The line asked for both within 15 in 100.' % (
    v8, 100 * (v8 / 1.16 - 1), l8[0], l8[1], 100 * (l8[0] / 14.6 - 1), 100 * (l8[1] / 14.6 - 1)))
l9 = [(float(d['V'][:, K(0.1)].mean()), float(d['P'][1][:, K(0.1)].mean())) for d in (CH, EX)]; ok9 = [within(a, 17.3, 0.20) and within(b, 5.83, 0.25) for a, b in l9]
line(9, 'guessed', 0.5, True if all(ok9) else False if not any(ok9) else None, 'at r = 0.1, n = 10^6: the variance round the ring is %.2f (number left to chance) and %.2f (exactly n) against 17.3 (%+.0f and %+.0f in 100), and the first part %.2f and %.2f against 5.83 (%+.0f and %+.0f in 100; the sheet does not say which kind). The line asked for within 20 and 25 in 100.' % (
    l9[0][0], l9[1][0], 100 * (l9[0][0] / 17.3 - 1), 100 * (l9[1][0] / 17.3 - 1), l9[0][1], l9[1][1], 100 * (l9[0][1] / 5.83 - 1), 100 * (l9[1][1] / 5.83 - 1)))
q10 = var(EX['layers']) / 100.0; line(10, 'read', 0.9, 0.073 <= q10 <= 0.090, 'with exactly 10^6 points the variance of the count of layers over n^(1/3) is %.4f (%.4f), from %d clouds; the line asked for 0.073 to 0.090 (the first study: 0.0816; the equation: 0.0807).' % (q10, sev(EX['layers']) / 100.0, EX['clouds']))
q11 = var(CH['layers']) / 100.0; line(11, 'worked', 0.9, 0.160 <= q11 <= 0.195, 'with the number left to chance it is %.4f (%.4f); the line asked for 0.160 to 0.195 (0.176 predicted).' % (q11, sev(CH['layers']) / 100.0))
E5 = DATA[('exact', 10 ** 5)]; v12 = float(E5['V'][:, K(0.5)].mean())
line(12, 'guessed', 0.5, within(v12, 11.6, 0.15), 'at n = 10^5, exactly n points, r = 0.5, the variance round the ring is %.2f against 11.6 (%+.0f in 100); the line asked for within 15 in 100.' % (v12, 100 * (v12 / 11.6 - 1)))
held = sum(1 for v in verdicts if v[3] is True); halfn = sum(1 for v in verdicts if v[3] is None)
brier = sum((v[2] - (1 if v[3] is True else 0.5 if v[3] is None else 0)) ** 2 for v in verdicts) / len(verdicts)
print('HELD %d of %d, HALF %d, FAILED %d. Brier score %.3f (a half counted as a half).' % (held, len(verdicts), halfn, len(verdicts) - held - halfn, brier))
for k in ('read', 'worked', 'guessed'):
    v = [x for x in verdicts if x[1] == k]; print('  %s: %d of %d held (lines %s; * failed, ~ half)' % (k, sum(1 for x in v if x[3] is True), len(v), ', '.join('C' + str(x[0]) + ('' if x[3] is True else '~' if x[3] is None else '*') for x in v)))
