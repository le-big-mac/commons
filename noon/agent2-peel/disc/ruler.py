"""ruler.py: dlib.py (what study.py and after.py compute from the clouds) tried on made-up clouds whose answers are known.
   python -I ruler.py
200 made-up clouds of 60,000 points thrown evenly in the disc. The depth of a point is the profile that rings.c takes off, plus
  - a number q1 for the whole cloud (variance 1), plus another q2 inside radius 0.55 only (variance 3): so the ring's mean has
    variance 1 outside 0.55 and 4 inside it, and the means at 0.8 and 0.3 are correlated by one half;
  - a cos(theta) + b sin(theta), a with variance 14 and b with variance 2 (so the first part is (14 + 2)/4 = 4), and the like
    with twice the angle and variance 2 each (the second part 1); nothing with three or four times the angle;
  - for each point a draw of variance 9; and the whole rounded to a whole number (variance 1/12).
So the variance round a ring is 8 + 2 + 9 + 1/12 = 19.08. The points are written out as peel writes them and passed through rings."""
import json, math, os, subprocess, sys, tempfile, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); tmp = tempfile.mkdtemp(prefix='agent2-druler-'); os.environ['DISC_RUNS'] = tmp; sys.path.insert(0, HERE)
import dlib
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail else ''))
drawn = []; N, CLOUDS, R = 60000, 200, 536870912.0; A0 = 0.75 * 1.3259 * (N / math.pi) ** (2 / 3.0); rng = np.random.default_rng(2026)
with open(os.path.join(tmp, 'exact-%d.jsonl' % N), 'w') as out:
    for i in range(CLOUDS):
        rho = np.sqrt(rng.random(N)); th_ = rng.random(N) * 2 * math.pi; q1, q2 = rng.normal(0, 1), rng.normal(0, math.sqrt(3)); a, b = rng.normal(0, math.sqrt(14)), rng.normal(0, math.sqrt(2)); c2, s2 = rng.normal(0, math.sqrt(2), 2); drawn.append((q1, q2, a, b, c2, s2))
        d = A0 * (1 - rho ** (4 / 3.0)) + q1 + q2 * (rho < 0.55) + a * np.cos(th_) + b * np.sin(th_) + c2 * np.cos(2 * th_) + s2 * np.sin(2 * th_) + rng.normal(0, 3, N)
        x = np.rint(rho * np.cos(th_) * R).astype(np.int64); y = np.rint(rho * np.sin(th_) * R).astype(np.int64); di = np.rint(d).astype(np.int64); layers = int(round(700 + rng.normal(0, 5)))
        text = '{"shape":"disc","n":%d,"seed":%d,"layers":%d}\n' % (N, i + 1, layers) + '\n'.join('%d %d %d' % t for t in zip(x.tolist(), y.tolist(), di.tolist())) + '\n'
        r = subprocess.run([os.path.join(HERE, 'rings'), str(N)], input=text, capture_output=True, text=True); assert r.returncode == 0, r.stderr; out.write(r.stdout)
d = dlib.load('exact', N); K = dlib.K
ok('200 made-up clouds read back: 200 clouds of 60,000 points, 19 annuli', d['clouds'] == CLOUDS and d['Q'].shape == (CLOUDS, 19) and (d['npts'] == N).all())
mq = [float(d['Q'][:, K(r)].mean()) for r in (0.3, 0.8)]; dq = np.array(drawn)
ok('the ring\'s mean is the depth less the profile: its mean over the clouds is %.2f at 0.3 and %.2f at 0.8, where the numbers given to these clouds have means %.2f and %.2f (the profile itself is some hundreds)' % (mq[0], mq[1], (dq[:, 0] + dq[:, 1]).mean(), dq[:, 0].mean()),
   abs(mq[0] - (dq[:, 0] + dq[:, 1]).mean()) < 0.1 and abs(mq[1] - dq[:, 0].mean()) < 0.1 and A0 > 300)
vo = [dlib.var(d['Q'][:, K(r)]) for r in (0.6, 0.7, 0.8, 0.9)]; vi = [dlib.var(d['Q'][:, K(r)]) for r in (0.2, 0.3, 0.4, 0.5)]
dr = np.array(drawn); qo = float(np.var(dr[:, 0], ddof=1)); qi = float(np.var(dr[:, 0] + dr[:, 1], ddof=1))
ok('the variance of the ring\'s mean: %s outside 0.55, where these clouds were given %.2f (1 on the average of many), and %s inside, where they were given %.2f (4)' % (', '.join('%.2f' % v for v in vo), qo, ', '.join('%.2f' % v for v in vi), qi),
   all(abs(v / qo - 1) < 0.06 for v in vo) and all(abs(v / qi - 1) < 0.04 for v in vi))
c = dlib.corr(d, 0.8, 0.3); ok('the ring\'s means at 0.8 and 0.3 are correlated by %.3f (one half put in; standard error by resampling %.3f)' % (c, dlib.secorr(d, 0.8, 0.3, 200)), abs(c - 0.5) < 0.13 and abs(dlib.corr(d, 0.8, 0.7) - 1) < 0.03)
p1 = float(((dr[:, 2] ** 2 + dr[:, 3] ** 2) / 4).mean()); p2 = float(((dr[:, 4] ** 2 + dr[:, 5] ** 2) / 4).mean()); vput = 9 + 1 / 12.0 + 2 * p1 + 2 * p2      # what these 200 clouds were in fact given
V = [float(d['V'][:, K(r)].mean()) for r in (0.1, 0.3, 0.5, 0.7, 0.9)]
ok('the variance round the ring: %s at 0.1, 0.3, 0.5, 0.7, 0.9, where these 200 clouds were given %.2f (19.08 on the average of many), the slope of the profile across the annulus taken out by the fitted line' % (', '.join('%.2f' % v for v in V), vput), all(abs(v / vput - 1) < 0.015 for v in V))
add = float((d['tot'] / d['cnt'])[:, K(0.5)].mean()); P = [float(d['P'][m][:, K(0.5)].mean()) for m in (1, 2, 3, 4)]
ok('the parts at 0.5: %.2f and %.2f, where these clouds were given %.2f and %.2f (4 and 1 on the average of many) and the finite number of points adds %.3f; and %.3f and %.3f for the third and fourth, where nothing was put in' % (P[0], P[1], p1, p2, add, P[2], P[3]),
   abs(P[0] / (p1 + add) - 1) < 0.02 and abs(P[1] / (p2 + add) - 1) < 0.04 and 0.6 * add < P[2] < 1.5 * add and 0.6 * add < P[3] < 1.5 * add and 0.02 < add < 0.05)
ok('the count of layers: variance %.1f (25 put in, and 1/12 for the rounding)' % dlib.var(d['layers']), abs(dlib.var(d['layers']) / 25.08 - 1) < 0.25)
ok('the predictions the scripts set beside the clouds are the sheet\'s: at 0.5 and a million points %.2f with the number left to chance and %.2f with exactly n; the correlations between 0.8 and 0.3, %.3f and %.3f' % (
    dlib.pred_ring('chance', 0.5, 10 ** 6), dlib.pred_ring('exact', 0.5, 10 ** 6), dlib.pred_corr('chance', 0.8, 0.3, 10 ** 6), dlib.pred_corr('exact', 0.8, 0.3, 10 ** 6)),
   '%.2f' % dlib.pred_ring('chance', 0.5, 10 ** 6) == '6.48' and '%.2f' % dlib.pred_ring('exact', 0.5, 10 ** 6) == '3.01' and '%.3f' % dlib.pred_corr('chance', 0.8, 0.3, 10 ** 6) == '0.505' and '%.3f' % dlib.pred_corr('exact', 0.8, 0.3, 10 ** 6) == '0.187')
ok('the standard error given for a variance is the variance times sqrt(2 / (clouds - 1))', abs(dlib.sev(d['layers']) / (dlib.var(d['layers']) * math.sqrt(2.0 / 199)) - 1) < 1e-12)
shutil.rmtree(tmp)
print('\n%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
