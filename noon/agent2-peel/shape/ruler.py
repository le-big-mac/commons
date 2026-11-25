"""ruler.py: is study.py a fair ruler? Made-up folders of runs, drawn from rules whose verdicts are known beforehand, are put
through it.   python -I ruler.py [STUDY.py]      (another copy of the scoring script may be named: ymutants.py does)
Folder 1 is drawn from the theory itself: every line must hold. Folder 2 from W1 (the variance goes as the mean), folder 3 from
W2 (psi level along each curve), folder 4 from W3 (the variance goes as the square of the mean for every shape), folder 5 from W4
(the count's share is not removed with exactly n): each must fail the lines the sheet says it would. Folder 6 is the theory with a
batch missing: its lines must come out "not run". The counts are whole numbers drawn from the normal law and rounded (rounding adds
1/12 to a variance; it is taken off beforehand).
The sheet says S5 (squares over discs) would fail W1. The first run of this file showed that it would not always: W1 puts the
figure at 1.048, the band begins at 1.058, and the error of the figure with 16,000 squares is 0.015; one draw in three here passed.
So S5 is not asked of W1 below, and the write-up says so.
Four cruder folders were added so that every one of the sixteen lines is failed by something (without them a scoring script
with a band left wide open on S1, S2, S6, S9, S10, S12 or S13 would pass): 7, every mean but the discs' 1 in 1,000 too high;
8a and 8b, the variance of one control and then of the other 8 in 100 off the disc's (one at a time, so that a line of two
parts is seen to fail when one part does: the first run of ymutants.py let three faults through for want of that); 9, every
variance 10 in 100 too large; 10, every shape's variance
three times as far from the disc's as the theory says. And 11: the theory, with the triangles' file cut short at 40,000 clouds
of 50,000, whose lines must come out "not run"."""
import json, os, shutil, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import theory
STUDY = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, 'study.py'); OUTJ = os.path.join(os.path.dirname(STUDY), 'study-other.json')
ASKED = {'exact-triangle-100000': 50000, 'exact-rtriangle-100000': 50000, 'exact-disc-100000': 30000, 'exact-square-100000': 16000, 'exact-hexagon-100000': 16000, 'exact-ellipse-100000': 8000,
         'exact-halfdisc-100000': 8000, 'exact-quarter-100000': 8000, 'exact-disc0-100000': 20000, 'chance-disc-100000': 20000, 'chance-triangle-100000': 20000, 'chance-square-100000': 8000,
         'exact-triangle-30000': 50000, 'exact-rtriangle-30000': 50000, 'exact-disc-30000': 30000}
def variance(rule, kind, shape, n0):
    sh = 'disc' if shape == 'disc0' else shape; p = theory.predictions(sh, n0); d = theory.predictions('disc', n0); key = 'chance' if kind == 'chance' else 'exact'
    if rule == 'theory': return p[key]
    if rule == 'W1': return d[key] * p['mean'] / d['mean']
    if rule == 'W2': return theory.predictions(sh, n0, I=theory.TH[sh]['lower'])[key]
    if rule == 'W3': return d[key] * (p['mean'] / d['mean']) ** 2
    if rule == 'W4': return p['chance']
    if rule == 'means': return p[key]
    if rule == 'ellipse': return p[key] * (1.08 if sh == 'ellipse' else 1)
    if rule == 'disc0': return p[key] * (0.92 if shape == 'disc0' else 1)
    if rule == 'size': return 1.10 * p[key]
    if rule == 'tripled': return d[key] * (1 + 3 * (p[key] / d[key] - 1))
def make(folder, rule, seed, leave_out=()):
    rng = np.random.default_rng(seed); os.makedirs(folder)
    for name, K in ASKED.items():
        if name in leave_out: continue
        if 'short:' + name in leave_out: K = int(0.8 * K)
        kind, shape, n0 = name.split('-'); n0 = int(n0); m = theory.predictions('disc' if shape == 'disc0' else shape, n0)['mean']; v = variance(rule, kind, shape, n0)
        if rule == 'means' and shape != 'disc': m *= 1.001
        x = np.round(rng.normal(m, np.sqrt(v - 1 / 12.0), K)).astype(int)
        with open(os.path.join(folder, name + '.jsonl'), 'w') as f:
            for i in range(K): f.write(json.dumps({'shape': shape, 'kind': kind, 'n0': n0, 'n': n0 if kind == 'exact' else n0 + int(rng.integers(-300, 300)), 'seed': i + 1, 'layers': int(x[i]), 'same': 1 if i % 200 == 0 else -1}) + '\n')
def verdicts(folder):
    if os.path.exists(OUTJ): os.remove(OUTJ)
    subprocess.run([sys.executable, '-I', STUDY], env=dict(os.environ, SHAPE_RUNS=folder), capture_output=True, text=True)
    if not os.path.exists(OUTJ): return {}
    o = json.load(open(OUTJ)); os.remove(OUTJ); return {k: v['verdict'] for k, v in o['lines'].items()}
ALL = ['S%d' % i for i in range(1, 17)]
CASES = [('the theory', 'theory', (), {t: 'held' for t in ALL}),
         ('W1, the variance goes as the mean', 'W1', (), {'S4': 'failed', 'S7': 'failed', 'S8': 'failed', 'S11': 'failed', 'S16': 'failed'}),
         ('W2, psi level along each curve', 'W2', (), {'S4': 'failed', 'S5': 'failed'}),
         ('W3, the variance goes as the square of the mean', 'W3', (), {'S7': 'failed', 'S8': 'failed', 'S4': 'held', 'S5': 'held', 'S11': 'held'}),
         ('W4, the count\'s share not removed', 'W4', (), {'S3': 'failed', 'S14': 'failed', 'S15': 'failed'}),
         ('the theory, batch C missing', 'theory', ('chance-disc-100000', 'chance-triangle-100000', 'chance-square-100000', 'exact-triangle-30000', 'exact-rtriangle-30000', 'exact-disc-30000'),
          {'S8': 'not run', 'S11': 'not run', 'S12': 'not run', 'S13': 'not run', 'S15': 'not run', 'S16': 'not run', 'S7': 'held', 'S4': 'held', 'S1': 'held'}),
         ('every mean but the discs\' 1 in 1,000 too high', 'means', (), {'S1': 'failed', 'S2': 'failed'}),
         ('the ellipse\'s variance 8 in 100 above the disc\'s', 'ellipse', (), {'S9': 'failed', 'S4': 'held', 'S7': 'held'}),
         ('the variance of the discs from the other generator 8 in 100 below', 'disc0', (), {'S9': 'failed', 'S4': 'held', 'S7': 'held'}),
         ('every variance 10 in 100 too large', 'size', (), {'S3': 'failed', 'S13': 'failed', 'S14': 'failed', 'S15': 'failed', 'S4': 'held', 'S7': 'held'}),
         ('every shape\'s variance three times as far from the disc\'s as the theory says', 'tripled', (), {'S4': 'failed', 'S5': 'failed', 'S6': 'failed', 'S10': 'failed', 'S11': 'failed', 'S12': 'failed'}),
         ('the theory, the triangles\' file cut short', 'theory', ('short:exact-triangle-100000',), {'S2': 'not run', 'S4': 'not run', 'S7': 'not run', 'S14': 'not run', 'S16': 'not run', 'S5': 'held', 'S8': 'held'})]
passed = failed = 0; tmp = '/dev/shm/agent2-ruler-%d' % os.getpid()
for trial in range(3):                     # three draws of each folder
    for i, (label, rule, out, want) in enumerate(CASES):
        folder = os.path.join(tmp, '%d-%d' % (trial, i)); make(folder, rule, 1000 * trial + i, out); got = verdicts(folder); shutil.rmtree(folder)
        ok = all(got.get(k) == v for k, v in want.items()); passed += ok; failed += (not ok)
        print('%s  draw %d, %s: %s   [held: %s; failed: %s; not run: %s]' % ('pass' if ok else 'FAIL', trial + 1, label, ', '.join('%s %s' % (k, v) for k, v in want.items()) if len(want) < 16 else 'all sixteen held',
              ' '.join(k for k in ALL if got.get(k) == 'held'), ' '.join(k for k in ALL if got.get(k) == 'failed') or 'none', ' '.join(k for k in ALL if got.get(k) == 'not run') or 'none'))
shutil.rmtree(tmp, ignore_errors=True)
print('%d passed, %d failed' % (passed, failed)); sys.exit(1 if failed else 0)
