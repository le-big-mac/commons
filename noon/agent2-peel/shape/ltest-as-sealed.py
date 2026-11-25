"""ltest.py: is study3.py a fair ruler? Made-up runs drawn from readings whose verdicts are known beforehand.   python -I ltest.py [STUDY3.py]
The counts are whole numbers drawn from the normal law and rounded (1/12 taken off the variance beforehand).
  plain      the theory as it stands: r = 1 at every size
  lean       the lean read from the earlier clouds: r = 1.018 - 0.64 n^(-1/3)
  half       half that lean: r = 1.009 - 0.32 n^(-1/3)   (the slope sits on L1's edge: its verdict is not asked)
  D          a larger D and no lean: r = 1.012 at every size
  wrong way  r = 0.99 + 0.5 n^(-1/3)
  mean       the plain theory, but the mean count 0.3 of a layer above the formula at every size
  missing    the lean, with the 300,000 file missing; short: the lean, with the 10,000 file a tenth short
Five draws of each; in each draw every verdict asked must come out as written."""
import json, math, os, shutil, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import theory
STUDY = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, 'study3.py'); OUTJ = os.path.join(os.path.dirname(STUDY), 'study3-other.json')
ASKED = {3000: 400000, 10000: 400000, 30000: 400000, 100000: 300000, 300000: 150000}; LINE = (4 / 3.0 * theory.D - theory.DC) / theory.ALPHA ** 2
READ = {'plain': lambda n: 1.0, 'lean': lambda n: 1.018 - 0.64 * n ** (-1 / 3.0), 'half': lambda n: 1.009 - 0.32 * n ** (-1 / 3.0), 'D': lambda n: 1.012, 'wrong way': lambda n: 0.99 + 0.5 * n ** (-1 / 3.0)}
def make(folder, reading, seed, drop=None, short=None, lift=0.1):
    os.makedirs(folder); rng = np.random.default_rng(seed)
    for n, K in ASKED.items():
        if n == drop: continue
        if n == short: K = int(0.9 * K)
        m = theory.predictions('disc', n)['mean'] + lift; v = READ[reading](n) * LINE * m ** 2 / n; x = np.round(rng.normal(m, math.sqrt(v - 1 / 12.0), K)).astype(int)
        open(os.path.join(folder, 'n3-disc-%d.jsonl' % n), 'w').write(''.join('{"layers": %d}\n' % c for c in x))
def verdicts(folder):
    if os.path.exists(OUTJ): os.remove(OUTJ)
    subprocess.run([sys.executable, '-I', STUDY], env=dict(os.environ, SHAPE_AFTER=folder), capture_output=True, text=True)
    if not os.path.exists(OUTJ): return {}, {}
    j = json.load(open(OUTJ)); os.remove(OUTJ); return {k: v['verdict'] for k, v in j['lines'].items()}, j
CASES = [('plain', 'plain', {}, {'L1': 'failed', 'L2': 'failed', 'L3': 'held', 'L4': 'failed', 'L5': 'failed', 'L6': 'held', 'L7': 'failed'}),
         ('lean', 'lean', {}, {'L1': 'held', 'L2': 'held', 'L3': 'held', 'L5': 'held', 'L6': 'held', 'L7': 'held'}),
         ('half', 'half', {}, {'L3': 'held', 'L6': 'held'}),
         ('D', 'D', {}, {'L1': 'failed', 'L2': 'failed', 'L4': 'held', 'L5': 'failed', 'L7': 'held'}),
         ('wrong way', 'wrong way', {}, {'L1': 'failed', 'L2': 'failed', 'L5': 'failed', 'L7': 'failed'}),
         ('mean', 'plain', {'lift': 0.3}, {'L6': 'failed', 'L1': 'failed'}),
         ('missing', 'lean', {'drop': 300000}, {'L1': 'not run', 'L4': 'not run', 'L7': 'not run', 'L6': 'not run', 'L2': 'held', 'L5': 'held'}),
         ('short', 'lean', {'short': 10000}, {'L1': 'not run', 'L2': 'not run', 'L7': 'not run', 'L6': 'not run', 'L5': 'held'})]
passed = failed = 0; tmp = '/dev/shm/agent2-ltest-%d' % os.getpid(); held4 = 0
for draw in range(5):
    for i, (label, reading, kw, want) in enumerate(CASES):
        folder = os.path.join(tmp, '%d-%d' % (draw, i)); make(folder, reading, 100 * draw + i, **kw); got, j = verdicts(folder); shutil.rmtree(folder)
        ok = all(got.get(k) == v for k, v in want.items()); passed += ok; failed += (not ok)
        if label == 'lean': held4 += got.get('L4') == 'held'
        if draw == 0 and label == 'lean':
            okf = abs(j['fit']['slope'] + 0.64) < 4 * j['fit']['slope_se'] and abs(j['fit']['intercept'] - 1.018) < 4 * j['fit']['intercept_se'] and 0.08 < j['fit']['slope_se'] < 0.16 and all(abs(j['sizes'][str(n)]['r'] - READ['lean'](n)) < 4 * j['sizes'][str(n)]['rse'] for n in ASKED); passed += okf; failed += (not okf)
            print('%s  the fit gives back the lean that was put in: slope %+.3f (%.3f), value for very many points %.4f (%.4f); every r within 4 of its errors' % ('pass' if okf else 'FAIL', j['fit']['slope'], j['fit']['slope_se'], j['fit']['intercept'], j['fit']['intercept_se']))
        print('%s  draw %d, %-9s: %s   [%s]' % ('pass' if ok else 'FAIL', draw + 1, label, ', '.join('%s %s' % kv for kv in want.items()), ' '.join('%s:%s' % (k, got.get(k, '?')[0]) for k in ('L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7'))))
shutil.rmtree(tmp, ignore_errors=True)
print('under the lean L4 (r at 300,000 above 1.004) held in %d draws of 5: it is asked of no reading, being a coin under half the lean' % held4)
print('%d passed, %d failed' % (passed, failed)); sys.exit(1 if failed else 0)
