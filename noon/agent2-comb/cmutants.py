# cmutants.py -- can the tests fail?  The true ccore.js is run through ctest.js first, by the same command (the control); then
# copies with one thing wrong each.   python -I cmutants.py
import os, subprocess, shutil
here = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(here, 'ccore.js'), encoding='utf-8').read()
M = [
 ('wrap-half-open', "an angle of exactly half a turn is wrapped the other way", "if (a > Math.PI) a -= TAU; if (a <= -Math.PI) a += TAU; return a;", "if (a > Math.PI) a -= TAU; if (a < -Math.PI) a += TAU; return a;"),
 ('angles-not-unwrapped', "the direction of each edge is taken as it comes, with its jumps", "F.push(k === 0 ? a : prev + wrap(a - prev)); prev = F[k];", "F.push(a); prev = F[k];"),
 ('turning-floor', "the turning number is cut down, not rounded", "return Math.round((F[pts.length] - F[0]) / TAU); }", "return Math.floor((F[pts.length] - F[0]) / TAU); }"),
 ('mean-not-removed', "the average direction is not taken away, so the curve does not close", "var ex = Math.cos(F[k]) - mx, ey = Math.sin(F[k]) - my,", "var ex = Math.cos(F[k]), ey = Math.sin(F[k]),"),
 ('whitney-any-class', "Whitney's way is offered between curves of different turning numbers", "if (A.n !== B.n) throw new Error('whitney: the two curves have turning numbers ' + A.n + ' and ' + B.n);", ""),
 ('whitney-no-branch', "the target's angles are not brought to the branch nearest the curve's", "shift = TAU * Math.round((A.F[0] - B.F[0]) / TAU);                 /* B's angles taken on the branch nearest A's at the start */", "shift = 0;"),
 ('whitney-half-way-only', "the angles go only half of the way", "F.push((1 - u) * A.F[k] + u * (B.F[k] + shift));", "F.push((1 - u / 2) * A.F[k] + u / 2 * (B.F[k] + shift));"),
 ('straight-swapped', "the plain way runs backwards", "pts.push([(1 - u) * A.pts[k][0] + u * B.pts[k][0], (1 - u) * A.pts[k][1] + u * B.pts[k][1]]);", "pts.push([u * A.pts[k][0] + (1 - u) * B.pts[k][0], u * A.pts[k][1] + (1 - u) * B.pts[k][1]]);"),
 ('kinks-unsigned', "every opposed place is counted as rising", "sense: d1 > d0 ? 1 : -1,", "sense: 1,"),
 ('kinks-at-zero', "the tangents are taken as opposed where they agree", "{ var v = Math.PI + TAU * m; if (v > lo && v <= hi)", "{ var v = TAU * m; if (v > lo && v <= hi)"),
 ('kinks-moment', "the moment of the kinks is given for the other curve", "u: A.L / (A.L + B.L) });", "u: B.L / (A.L + B.L) });"),
 ('crossings-neighbours', "edges two apart are not tried against each other", "for (j = i + 2; j < N; j++) {", "for (j = i + 3; j < N; j++) {"),
 ('crossings-sign', "the sign of every crossing is turned round", "den > 0 ? 1 : -1]); } }", "den > 0 ? -1 : 1]); } }"),
 ('theorem2-mu', "mu is always +1", "var mu = rot[1][0] - rot[N - 1][0] > 0 ? 1 : -1,", "var mu = 1,"),
 ('theorem2-any-start', "the count by crossings begins wherever the curve begins", "for (k = 1; k < N; k++) if (pts[k][1] < pts[s][1] || (pts[k][1] === pts[s][1] && pts[k][0] < pts[s][0])) s = k;", ""),
 ('resample-by-index', "the curve is resampled by taking every point in turn, not by length", "var f = seg > 0 ? Math.min(1, (t - done) / seg) : 0;", "var f = 0;"),
 ('lay-first', "the target is laid the first way tried, not the best", "if (!best || c > best.clear + 1e-12) best =", "if (!best) best ="),
 ('lay-one-start', "the target is tried at one beginning only", "for (k = 0; k < 16; k++) { var B = shape(shift(pts, Math.round(k * N / 16)));", "for (k = 0; k < 1; k++) { var B = shape(shift(pts, Math.round(k * N / 16)));"),
 ('clearance-one-moment', "the way's nearness to a kink is looked at in the middle only", "for (i = 1; i <= 19; i++) { var w = whitney(A, B, i / 20);", "for (i = 10; i <= 10; i++) { var w = whitney(A, B, i / 20);"),
 ('sharpest-blind', "no turn is ever called sharp", "m = Math.max(m, Math.abs(F[k + 1] - F[k])); return m; }", "return m; }"),
 ('standard-eight-on-crossing', "the figure of eight is begun on its own crossing", "t = TAU * (k + 0.37) / N;", "t = TAU * k / N;"),
 ('mirror-x', "the mirror turns the curve end for end instead", "return pts.map(function (p) { return [p[0], -p[1]]; }); }", "return pts.map(function (p) { return [-p[0], -p[1]]; }); }"),
]
for name, what, a, b in M: assert src.count(a) == 1, name
d = os.path.join(here, 'mutants'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d); shutil.copy(os.path.join(here, 'ctest.js'), d)
def run(code):
    open(os.path.join(d, 'ccore.js'), 'w', encoding='utf-8').write(code)
    try: return subprocess.run(['node', 'ctest.js'], cwd=d, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired: return None
r = run(src); assert r is not None and r.returncode == 0 and 'FAIL' not in r.stdout, 'the true program does not pass by this runner'
print('control: the true ccore.js, run in the same way: ' + r.stdout.strip().split('\n')[-1] + '\n', flush=True); caught = 0
for name, what, a, b in M:
    r = run(src.replace(a, b))
    if r is None: res = 'caught: the tests do not finish'
    else:
        nf = [l for l in r.stdout.split('\n') if l.startswith('FAIL')]
        res = ('caught: %d of the tests fail (%s)' % (len(nf), nf[0][6:70])) if nf else ('caught: the tests stop with an error' if r.returncode else 'NOT caught: every test passes')
    caught += res.startswith('caught'); print('%-28s %s -- %s' % (name, what, res), flush=True)
print('\n%d of %d broken copies caught' % (caught, len(M)))
