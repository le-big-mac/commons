"""qtest.py: the fifth sheet's scoring script tried on made-up runs before the sheet is sealed.   python -I qtest.py [a copy of study5.py]
Made-up worlds, each a folder of thirteen files of counts written here (whole numbers drawn round a chosen mean and spread). study5.py
is run on each folder as it will be run on the real one (SHAPE_AFTER); its verdicts and figures are compared with the bands written
out again here and the figures computed here from the same files."""
import json, math, os, shutil, subprocess, sys, tempfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import theory
C5 = 0.08227; RATIO = 1.0197; LAT = (83, 90, 98, 105, 113, 120); npass = nfail = 0
STUDY = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, 'study5.py'); SDIR = os.path.dirname(STUDY)
SIZE = dict([('disc-%d' % n, 200000) for n in LAT] + [('cdisc-1000', 400000), ('triangle-300', 400000), ('triangle-1000', 400000), ('triangle-3000', 200000), ('rtriangle-300', 400000), ('rtriangle-1000', 400000), ('rtriangle-3000', 200000)])
def check(name, cond):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name)
def base(key):
    sh, n = key.split('-'); n = int(n); return (C5 * n ** (1 / 3.0)) if sh == 'disc' else RATIO * theory.predictions('disc' if sh == 'cdisc' else sh, n)['exact']
def world(d, rng, B, short=None):
    """B[key]: the B this world gives the set; the counts are whole numbers about a mean, their spread trimmed until the file's variance is the one asked for to about 0.0003"""
    for key, K in SIZE.items():
        sh, n = key.split('-'); n = int(n); v = base(key) + B[key]; m = round(0.47 * n ** (2 / 3.0)) + 0.37; K = K if key != short else int(K * 0.97)
        z = rng.standard_normal(K); s2 = max(v - 1 / 12.0, 0.02)
        for _ in range(12): x = np.rint(m + math.sqrt(s2) * z).astype(int); s2 = max(s2 + v - float(x.var(ddof=1)), 0.02)      # the spread is trimmed until the file's own variance is the one asked for
        x = np.rint(m + math.sqrt(s2) * z).astype(int)
        open(os.path.join(d, 'n5-%s.jsonl' % key), 'w').write(''.join('{"shape": "%s", "kind": "exact", "maker": "made up", "n0": %d, "n": %d, "seed": %d, "layers": %d}\n' % (sh, n, n, i, c) for i, c in enumerate(x)))
def mine(d):
    """the figures and the verdicts, written out again: nothing here is taken from study5.py"""
    B = {}
    for key, K in SIZE.items():
        x = np.array([json.loads(l)['layers'] for l in open(os.path.join(d, 'n5-%s.jsonl' % key))], float); B[key] = None if len(x) < 0.999 * K else float(x.var(ddof=1)) - base(key)
    g = lambda k: B[k]; ok = lambda *ks: all(B[k] is not None for k in ks); L = ['disc-%d' % n for n in LAT]; v = {}
    pred = {83: -0.0467, 90: -0.0294, 98: -0.0450, 105: -0.0320, 113: -0.0435, 120: -0.0346}
    v['Q1'] = ((g('disc-90') + g('disc-105') + g('disc-120')) / 3 - (g('disc-83') + g('disc-98') + g('disc-113')) / 3 >= 0.008) if ok(*L) else None
    v['Q2'] = all(abs(g('disc-%d' % n) - pred[n]) <= 0.004 for n in LAT) if ok(*L) else None
    v['Q3'] = (abs(g('cdisc-1000') + 0.0450) <= 0.006) if ok('cdisc-1000') else None
    v['Q4'] = (g('triangle-1000') - g('cdisc-1000') <= -0.020) if ok('triangle-1000', 'cdisc-1000') else None
    v['Q5'] = (abs(g('triangle-1000') - g('cdisc-1000')) <= 0.006) if ok('triangle-1000', 'cdisc-1000') else None
    v['Q6'] = (g('triangle-1000') - g('rtriangle-1000') <= -0.012) if ok('triangle-1000', 'rtriangle-1000') else None
    v['Q7'] = (abs(g('rtriangle-1000') - g('cdisc-1000')) <= 0.008) if ok('rtriangle-1000', 'cdisc-1000') else None
    v['Q8'] = (g('triangle-300') <= -0.0551) if ok('triangle-300') else None
    v['Q9'] = (g('triangle-3000') <= -0.0621) if ok('triangle-3000') else None
    return B, {k: (None if x is None else bool(x)) for k, x in v.items()}
def Bw(lat, cd, t, r): return dict([('disc-%d' % n, lat[n]) for n in LAT] + [('cdisc-1000', cd)] + [('triangle-%d' % n, t[n]) for n in t] + [('rtriangle-%d' % n, r[n]) for n in r])
SW = {83: -0.0467, 90: -0.0294, 98: -0.0450, 105: -0.0320, 113: -0.0435, 120: -0.0346}; LV = {n: -0.0424 for n in LAT}; D3 = {300: -0.0401, 1000: -0.0450, 3000: -0.0471}
WORLDS = [('the count swings, corners add 0.045', Bw(SW, -0.045, {n: D3[n] - 0.045 for n in D3}, D3), None, 'YYYYnYYYY'),
          ('the count runs level, the same amount for every shape', Bw(LV, -0.045, D3, D3), None, 'nnYnYnYnn'),
          ('a swing of half the size, the same share, the control 0.01 out', Bw({n: (SW[n] + LV[n]) / 2 for n in LAT}, -0.035, {300: -0.0479, 1000: -0.0538, 3000: -0.0563}, {300: -0.0439, 1000: -0.0493, 3000: -0.0516}), None, 'nnnnnnnnn'),
          ('the swing the other way up; the triangle 0.03 above the disc, the rounded triangle 0.02 below', Bw({n: LV[n] - (SW[n] - LV[n]) for n in LAT}, -0.045, {n: D3[n] + 0.03 for n in D3}, {n: D3[n] - 0.02 for n in D3}), None, 'nnYnnnnnn'),
          ('the count swings, corners add 0.045, the 1,000-point triangles short', Bw(SW, -0.045, {n: D3[n] - 0.045 for n in D3}, D3), 'triangle-1000', None)]
if __name__ == '__main__':
    top = tempfile.mkdtemp(prefix='noon-qtest-%d-' % os.getpid())
    try:
        for k, (lab, B, short, want) in enumerate(WORLDS):
            d = os.path.join(top, 'w%d' % k); os.makedirs(d); world(d, np.random.default_rng(500 + k), B, short)
            r = subprocess.run([sys.executable, '-I', STUDY], capture_output=True, text=True, env=dict(os.environ, SHAPE_AFTER=d)); jp = os.path.join(SDIR, 'study5-other.json'); js = json.load(open(jp)) if r.returncode == 0 and os.path.exists(jp) else None
            if js is None: check('%s: study5.py ran' % lab, False); continue
            Bm, v = mine(d); got = {t: {'held': True, 'failed': False, 'not run': None}[js['lines'][t]['verdict']] for t in v}; word = ''.join('-' if v[t] is None else 'Y' if v[t] else 'n' for t in sorted(v))
            check('%s: study5.py ran, and its nine verdicts are the ones the bands written out here give (%s)' % (lab, word), got == v)
            if short is None:
                check('%s: the verdicts are the ones this world was made to give (%s)' % (lab, want), word == want)
                check('%s: every B agrees with mine to 1e-9' % lab, all(abs(js['sets'][key]['B'] - Bm[key]) < 1e-9 for key in SIZE))
            else: check('%s: Q4, Q5 and Q6 are "not run" and the rest are judged' % lab, [t for t in sorted(v) if v[t] is None] == ['Q4', 'Q5', 'Q6'] and js['notrun'] == 3 and js['held'] + js['failed'] == 6)
            shutil.rmtree(d, ignore_errors=True)
    finally:
        shutil.rmtree(top, ignore_errors=True)
        if os.path.exists(os.path.join(SDIR, 'study5-other.json')): os.remove(os.path.join(SDIR, 'study5-other.json'))
    print('%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
