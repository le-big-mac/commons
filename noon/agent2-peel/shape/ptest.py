"""ptest.py: the fourth sheet's scoring script tried on made-up runs before the sheet is sealed.   python -I ptest.py [a copy of study4.py]
(As sealed it took no argument: ptest-as-sealed.py. The argument is for p4mutants.py, which tries broken copies. Two worlds were added
after the first run of broken copies: see WORLDS.)
Five made-up worlds (four as sealed), each a folder of four files of counts written here (whole numbers drawn round a chosen mean and spread; for four
points, one layer or two with a chosen share): the constant; the theory as it stood, with a program that loses a layer in 100
four-point clouds; the power -0.52; the constant with one file short; and (added later) one that sits on the far side of three bands. study4.py is run on each folder as it will be run on the
real one (SHAPE_AFTER), and its verdicts and figures are compared with the bands written out again here and the figures computed
here from the same files."""
import json, math, os, shutil, subprocess, sys, tempfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ruler4, theory
C5 = 0.08227; SYL = 1 - 35 / (12 * math.pi ** 2); npass = nfail = 0
STUDY = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, 'study4.py'); SDIR = os.path.dirname(STUDY)
def check(name, cond):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name)
def write(d, n, x): open(os.path.join(d, 'n4-disc-%d.jsonl' % n), 'w').write(''.join('{"shape": "disc", "kind": "exact", "maker": "made up", "n0": %d, "n": %d, "seed": %d, "layers": %d}\n' % (n, n, i, v) for i, v in enumerate(x)))
def world(d, rng, var, excess, share, short=None):
    for n in (100, 300, 1000):
        m = theory.predictions('disc', n)['mean'] + excess(n); K = 400000 if n != short else 390000; write(d, n, np.rint(m + math.sqrt(max(var(n) - 1 / 12.0, 0.01)) * rng.standard_normal(K)).astype(int))
    write(d, 4, np.where(rng.random(400000) < share, 1, 2))
def mine(d):
    """the figures and the verdicts, written out again: nothing here is taken from study4.py"""
    f = {}
    for n in (4, 100, 300, 1000):
        x = np.array([json.loads(l)['layers'] for l in open(os.path.join(d, 'n4-disc-%d.jsonl' % n))], float); f[n] = None if len(x) < 399600 else (x.mean(), x.var(ddof=1), (x == 1).mean())
    b = {n: (None if f[n] is None else f[n][1] - C5 * n ** (1 / 3.0)) for n in (100, 300, 1000)}; ex = {n: (None if f[n] is None else f[n][0] - 1.3259 * (n / math.pi) ** (2 / 3.0) * 0.75) for n in (100, 300, 1000)}; v = {}
    v['P0'] = None if f[4] is None else 0.7020 <= f[4][2] <= 0.7070
    v['P1'] = None if b[1000] is None else -0.057 <= b[1000] <= -0.037; v['P2'] = None if b[300] is None else -0.057 <= b[300] <= -0.037; v['P3'] = None if b[100] is None else -0.057 <= b[100] <= -0.037
    v['P4'] = None if any(b[n] is None for n in b) else max(b.values()) <= -0.025; v['P5'] = None if b[100] is None or b[1000] is None else b[100] - b[1000] >= 0.004
    v['P6'] = None if ex[1000] is None else 0.130 <= ex[1000] <= 0.165; v['P7'] = None if ex[100] is None else ex[100] >= 0.245
    return b, ex, v
RD = ruler4.readings(); MN = ruler4.MEANS
WORLDS = [('the constant', RD['a constant (power -1/3)'], MN['c + d n^(-1/3)'], SYL, None, 'YYYYYnYY'), ('the theory as it stood, a layer lost in 100 four-point clouds', RD['the theory as it stood'], MN['a tenth of a layer'], SYL + 0.01, None, 'nnnnnYnn'),
          ('the power -0.52, the mean by n^(-1/6)', RD['power -0.52'], MN['c + d n^(-1/6)'], SYL, None, 'YYnnYnYn'), ('the constant, the 300-point file short', RD['a constant (power -1/3)'], MN['c + d n^(-1/3)'], SYL, 300, 'YY-YY-nYY'.replace('-', '')),
          # added after the first run of broken copies let three through (P0 open below, P4 by any one size, P6 open above): a world on the other side of each
          ('B rising from -0.045 to -0.010, the mean a fifth of a layer over, a layer gained in 100 four-point clouds', lambda n: C5 * n ** (1 / 3.0) + {100: -0.010, 300: -0.030, 1000: -0.045}[n], lambda n: 0.20, SYL - 0.01, None, 'nYnnnYnn')]
top = tempfile.mkdtemp(prefix='noon-ptest-%d-' % os.getpid())
try:
    for k, (lab, var, excess, share, short, want) in enumerate(WORLDS):
        d = os.path.join(top, 'w%d' % k); os.makedirs(d); world(d, np.random.default_rng(400 + k), var, excess, share, short)
        r = subprocess.run([sys.executable, '-I', STUDY], capture_output=True, text=True, env=dict(os.environ, SHAPE_AFTER=d)); js = json.load(open(os.path.join(SDIR, 'study4-other.json'))) if r.returncode == 0 and os.path.exists(os.path.join(SDIR, 'study4-other.json')) else None; b, ex, v = mine(d)
        if js is None: check('%s: study4.py ran' % lab, False); continue
        got = {t: {'held': True, 'failed': False, 'not run': None}[js['lines'][t]['verdict']] for t in v}
        check('%s: study4.py ran, and its eight verdicts are the ones the bands written out here give (%s)' % (lab, ''.join('-' if v[t] is None else 'Y' if v[t] else 'n' for t in sorted(v))), r.returncode == 0 and got == {t: (None if v[t] is None else bool(v[t])) for t in v})
        if short is None:
            check('%s: the verdicts are the ones this world was made to give (%s)' % (lab, want), ''.join('Y' if v[t] else 'n' for t in sorted(v)) == want)
            check('%s: B and the mean\'s excess agree with mine to 1e-9 at the three sizes' % lab, all(abs(js['sizes'][str(n)]['B'] - b[n]) < 1e-9 and abs(js['sizes'][str(n)]['excess'] - ex[n]) < 1e-9 for n in (100, 300, 1000)))
            e = js['sizes']['100']['vse']; check('%s: the resampled error of the variance at 100 points, %.5f, is near the normal figure %.5f' % (lab, e, js['sizes']['100']['v'] * math.sqrt(2 / 4e5)), 0.8 < e / (js['sizes']['100']['v'] * math.sqrt(2 / 4e5)) < 1.25)
        else:
            check('%s: P2, P4 are "not run" and the rest are judged' % lab, [t for t in sorted(v) if v[t] is None] == ['P2', 'P4'] and js['notrun'] == 2 and js['held'] + js['failed'] == 6)
finally:
    shutil.rmtree(top, ignore_errors=True)
    if os.path.exists(os.path.join(SDIR, 'study4-other.json')): os.remove(os.path.join(SDIR, 'study4-other.json'))
print('%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
