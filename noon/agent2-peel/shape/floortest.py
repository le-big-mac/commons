"""floortest.py: tests of floor.py (the search for the lowest shape) and of study2.py's scoring.   python -I floortest.py [DIR]
DIR (default: this folder) holds the floor.py and study2.py under test; a copy with a fault planted can be put through the same
tests (floormutants.py).
(In the made-up runs a line about a difference, A2 or A3, fails by chance about once in sixty draws with nothing there to find;
it is asked to hold only where the case is about it.)"""
import json, math, os, shutil, subprocess, sys, tempfile
import numpy as np
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); DIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE
sys.path.insert(0, DIR); import floor as F
passed = failed = 0
def check(name, ok, detail=''):
    global passed, failed
    if ok: passed += 1
    else: failed += 1
    print('%s  %s%s' % ('pass' if ok else 'FAIL', name, ('   [' + str(detail) + ']') if detail != '' else ''))
def area(P): return 0.5 * sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))
far = np.full(24, 5.0)
h = far.copy(); h[[0, 6, 12, 18]] = [1, 2, 1, 2]; P = F.polygon(h)
check('polygon: four lines at 0, 90, 180, 270 degrees give the rectangle 2 by 4, counter-clockwise, and lines far off give no side', P is not None and len(P) == 4 and abs(area(P) - 8) < 1e-9 and sorted((round(p[0], 6), round(p[1], 6)) for p in P) == [(-1, -2), (-1, 2), (1, -2), (1, 2)], P)
h = far.copy(); h[[2, 10, 18]] = 1.0; P = F.polygon(h); check('polygon: lines at 30, 150, 270 degrees at distance 1 give the equilateral triangle of inradius 1 (area 3 sqrt 3)', P is not None and len(P) == 3 and abs(area(P) - 3 * math.sqrt(3)) < 1e-9)
h = np.full(24, 1.0); P = F.polygon(h); check('polygon: all 24 lines at distance 1 give the regular 24-gon about the unit circle', P is not None and len(P) == 24 and abs(area(P) - 24 * math.tan(math.pi / 24)) < 1e-9)
h = far.copy(); h[[0, 6, 12, 18]] = 1.0; h[3] = 1.2; P = F.polygon(h); check('polygon: a fifth line at 45 degrees cuts the corner of the square (five corners, area 4 less the corner)', P is not None and len(P) == 5 and abs(area(P) - (4 - 0.5 * (2 - 1.2 * math.sqrt(2)) ** 2 * 1.0)) < 1e-9, area(P) if P else None)
h = np.full(24, 100.0); check('polygon: lines too far off to bound anything are refused', F.polygon(h) is None)
x = F.triangle_start(); d = F.describe(x)
check('describe: the starting triangle has three sides, with normals at 30, 150, 270 degrees, each of length sqrt(4 pi / sqrt 3), area pi, rho 0.2', d is not None and sorted(a for a, L in d['sides']) == [30, 150, 270] and all(abs(L - math.sqrt(4 * math.pi / math.sqrt(3))) < 1e-9 for a, L in d['sides']) and abs(area(d['corners']) - math.pi) < 1e-9 and abs(d['rho'] - 0.2) < 1e-12)
w_tri = (3 * math.sqrt(4 * math.pi / math.sqrt(3)) / (2 * math.sqrt(3))); check('describe: how many times wider one way than another, for the swollen triangle (its width is between its height and its side)', d is not None and abs(d['aspect'] - (math.sqrt(4 * math.pi / math.sqrt(3)) + 0.4) / (w_tri + 0.4)) < 1e-9, d and d['aspect'])
y = x.copy(); y[:24] += 0.7; y2 = x.copy(); y2[:24] = np.log(np.exp(x[:24]) + 0.3 * F.NX - 0.2 * F.NY)
check('describe: scaling every distance, or moving the origin, gives the same shape', all(abs(a[1] - b[1]) < 1e-9 for a, b in zip(sorted(F.describe(y)['sides']), sorted(d['sides']))) and all(abs(a[1] - b[1]) < 1e-9 for a, b in zip(sorted(F.describe(y2)['sides']), sorted(d['sides']))))
h = far.copy(); h[[0, 12]] = 1.0; h[[6, 18]] = 0.2; z = np.concatenate([np.log(h), [math.log(0.2)]]); check('Q_of: a rectangle five times as long as wide is refused; so is a rounding above 1.5 or below 0.001', F.Q_of(z) == 2.0 and F.Q_of(np.concatenate([x[:24], [math.log(1.6)]])) == 2.0 and F.Q_of(np.concatenate([x[:24], [math.log(0.0005)]])) == 2.0)
with ThreadPoolExecutor(max_workers=4) as ex:
    hs = far.copy(); hs[[0, 6, 12, 18]] = 1.0; hh = far.copy(); hh[[0, 4, 8, 12, 16, 20]] = 1.0
    vals = list(ex.map(F.Q_of, [x, np.concatenate([np.log(hs), [math.log(0.2)]]), np.concatenate([np.log(hh), [math.log(0.2)]]), np.concatenate([x[:24], [math.log(0.02)]]), np.concatenate([np.log(hs), [math.log(0.002)]])]))
check('Q_of at 240 angles: the triangle, square and hexagon swollen by 0.2 and the triangle by 0.02 are within 0.0004 of ceiling.out (1.30558, 1.31681, 1.32580, 1.32206); a square hardly rounded is near 4/3', all(abs(v - t) < 4e-4 for v, t in zip(vals[:4], (1.30558, 1.31681, 1.32580, 1.32206))) and abs(vals[4] - 4 / 3.0) < 2e-3, ['%.5f' % v for v in vals])
# the evolution strategy on a function whose least place is known: 25 numbers, a bowl about a point, some directions flat
target = np.linspace(-1, 1, 25); real = F.Q_of
def bowl(x_): s_ = float(((x_[:20] - target[:20]) ** 2 * np.linspace(1, 30, 20)).sum()); return 1.0 + 0.9 * s_ / (1 + s_)      # between 1 and 1.9: the search treats 2 as "refused"
F.Q_of = bowl
with ThreadPoolExecutor(max_workers=2) as ex: (fb, xb), hist = F.cma(np.zeros(25), 0.3, 1, ex, lam=24, gens=400)
check('cma: on a bowl in 20 of 25 directions (five flat, widths 1 to 30) it comes within 0.001 of the least value, 1, from a start where the value is above 1.8, and stops by itself', fb < 1.001 and np.abs(xb[:20] - target[:20]).max() < 0.05 and len(hist) < 400 and hist[0] > 1.8, (fb, len(hist), hist[0]))
F.Q_of = lambda x_: float(2.0 if x_[0] > 0.5 else 1.5 - 0.3 * math.exp(-((x_ - 0.3) ** 2).sum()))
with ThreadPoolExecutor(max_workers=2) as ex: (fb2, xb2), hist2 = F.cma(np.zeros(25), 0.15, 2, ex, lam=24, gens=400)
check('cma: with refusals (the value 2) over part of the space it still finds the least, 1.2, to 0.002', abs(fb2 - 1.2) < 2e-3, fb2)
with ThreadPoolExecutor(max_workers=2) as ex: (fb3, xb3), hist3 = F.cma(np.zeros(25), 0.15, 2, ex, lam=24, gens=400)
check('cma: the same seed gives the same search', fb3 == fb2 and hist3 == hist2)
def rough(x_): d_ = float(((x_ - 0.3) ** 2).sum()); return 1.5 - 0.3 * math.exp(-d_) + 0.02 * (math.sin(1e4 * float(x_.sum())) * 43758.5453 % 1.0)      # a bowl with a rough bottom: the last generation is seldom the best
F.Q_of = rough
with ThreadPoolExecutor(max_workers=2) as ex: (fb4, xb4), hist4 = F.cma(np.zeros(25), 0.15, 3, ex, lam=24, gens=60)
check('cma: what it returns is the best of all generations (the least value in its history, and the value of the shape returned), on a bowl with a rough bottom', fb4 == min(hist4) and abs(rough(xb4) - fb4) < 1e-12 and hist4[-1] > fb4, (fb4, min(hist4), hist4[-1]))
F.Q_of = real
# study2.py on made-up runs and made-up records of a search
TMP = tempfile.mkdtemp(prefix='agent2-floortest-', dir='/dev/shm'); sys.path.insert(0, HERE); import theory
def runs(folder, level, drop=None, short=None):
    os.makedirs(folder); rng = np.random.default_rng(int(os.path.basename(folder)[1:]) + 77)
    for name, n in (('q2-cloud-quarter-100000', 100000), ('q2-numpy-quarter-100000', 100000), ('q2-cloud-quarter-30000', 30000), ('q2-numpy-quarter-30000', 30000)):
        if name == drop: continue
        p = theory.predictions('quarter', n); v = p['exact'] * level(name, n); K = 100000 if name == short else 120000; x = np.round(rng.normal(p['mean'], math.sqrt(v - 1 / 12.0), K)).astype(int)
        with open(os.path.join(folder, name + '.jsonl'), 'w') as f: f.write(''.join('{"layers": %d}\n' % c for c in x))
def record(path, best, sides, rho, lows, nfine=5, cut=None):
    hh = np.full(24, 5.0); hh[list(sides)] = 1.0
    if cut is not None: hh[cut[0]] = cut[1]                # one more line, cutting a little off a corner
    xx = [float(v) for v in np.log(hh)] + [math.log(rho)]
    json.dump({'runs': [dict({'seed': s, 'start': 'x', 'start_Q': 1.33, 'best_Q': lows[s - 1], 'x': xx, 'generations': 50, 'history': []}, **({'fine_Q': best + 0.002 * (s - 1)} if s <= nfine else {})) for s in range(1, 9)]}, open(path, 'w'))
def verdicts(folder, floorfile):
    o = os.path.join(DIR, 'study2-other.json')
    if os.path.exists(o): os.remove(o)
    subprocess.run([sys.executable, '-I', os.path.join(DIR, 'study2.py')], env=dict(os.environ, SHAPE_AFTER=folder, FLOOR=floorfile), capture_output=True, text=True)
    if not os.path.exists(o): return {}
    j = json.load(open(o)); os.remove(o); LAST['sets'] = j.get('sets', {}); LAST['floor'] = j.get('floor', {}); return {k: v['verdict'] for k, v in j['lines'].items()}
LAST = {}
tri, quad = (2, 10, 18), (0, 6, 12, 18); same = [1.3058] * 8
CASES = [('the theory, a little above its line (1.002); a rounded triangle at 1.3055, rho 0.22, every start near', lambda nm, n: 1.002, None, None, (1.3055, tri, 0.22, same), {'A1': 'held', 'A2': 'held', 'A3': 'held', 'A4': 'held', 'B1': 'held', 'B2': 'held', 'B3': 'held', 'B4': 'held'}),
         ('quarter discs 2.5 in 100 above their line everywhere', lambda nm, n: 1.025, None, None, (1.3055, tri, 0.22, same), {'A1': 'failed', 'A4': 'failed', 'A2': 'held', 'A3': 'held'}),
         ('quarter discs 1.2 in 100 above their line everywhere (A4 may or may not fail)', lambda nm, n: 1.012, None, None, (1.3055, tri, 0.22, same), {'A1': 'failed'}),
         ('cloud.c\'s quarter discs 1.6 in 100 more variable than numpy\'s', lambda nm, n: 1.016 if 'cloud' in nm else 1.0, None, None, (1.3055, tri, 0.22, same), {'A2': 'failed', 'A3': 'held'}),
         ('an excess of 1.6 in 100 at 100,000 points only', lambda nm, n: 1.016 if n == 100000 else 1.0, None, None, (1.3055, tri, 0.22, same), {'A3': 'failed', 'A2': 'held'}),
         ('quarter discs 1.2 in 100 below their line', lambda nm, n: 0.988, None, None, (1.3055, tri, 0.22, same), {'A1': 'failed'}),
         ('the new cloud.c set at 100,000 alone 2 in 100 high, the others on the line', lambda nm, n: 1.02 if (n == 100000 and 'cloud' in nm) else 1.0, None, None, (1.3055, tri, 0.22, same), {'A4': 'failed', 'A1': 'held'}),
         ('one file missing', lambda nm, n: 1.002, 'q2-numpy-quarter-30000', None, (1.3055, tri, 0.22, same), {'A1': 'not run', 'A2': 'not run', 'A3': 'not run', 'A4': 'held'}),
         ('one file a sixth short', lambda nm, n: 1.002, None, 'q2-cloud-quarter-100000', (1.3055, tri, 0.22, same), {'A1': 'not run', 'A4': 'not run'}),
         ('the search found 1.3010 at a rounded quadrilateral, from one random start only', lambda nm, n: 1.002, None, None, (1.3010, quad, 0.22, [1.3058, 1.3058, 1.3058, 1.3010, 1.3058, 1.3058, 1.3058, 1.3058]), {'B1': 'failed', 'B2': 'failed', 'B3': 'not run', 'B4': 'failed'}),
         ('the search found a rounded triangle with rho 0.5; two random starts near', lambda nm, n: 1.002, None, None, (1.3050, tri, 0.5, [1.3052, 1.31, 1.31, 1.3060, 1.3069, 1.32, 1.32, 1.32]), {'B1': 'held', 'B2': 'held', 'B3': 'failed', 'B4': 'held'}),
         ('the search found a rounded triangle with one corner cut by a side of 2 in 100 of its flat edge: still a triangle', lambda nm, n: 1.002, None, None, (1.3052, tri, 0.22, same, 5, (6, 1.94)), {'B1': 'held', 'B2': 'held', 'B3': 'held'}),
         ('the three starts at the triangle end near the least and only one random start does', lambda nm, n: 1.002, None, None, (1.3052, tri, 0.22, [1.3052, 1.3053, 1.3054, 1.3060, 1.31, 1.32, 1.32, 1.32]), {'B1': 'held', 'B4': 'failed'}),
         ('the search not finished (three shapes run again, not five)', lambda nm, n: 1.002, None, None, (1.3055, tri, 0.22, same, 3), {'B1': 'not run', 'B2': 'not run', 'B3': 'not run', 'B4': 'not run', 'A1': 'held'})]
for i, (label, level, drop, short, rec, want) in enumerate(CASES):
    folder = os.path.join(TMP, 'c%d' % i); runs(folder, level, drop, short); fj = os.path.join(TMP, 'f%d.json' % i); record(fj, *rec); got = verdicts(folder, fj)
    check('study2 on made-up runs: %s: %s' % (label, ', '.join('%s %s' % kv for kv in want.items())), all(got.get(k) == v for k, v in want.items()), {k: got.get(k) for k in want})
    if i == 0:
        ok_r = True
        for key, (name, n) in (('cloud.c, 100,000', ('q2-cloud-quarter-100000', 100000)), ('numpy, 30,000', ('q2-numpy-quarter-30000', 30000))):
            xs = np.array([json.loads(l)['layers'] for l in open(os.path.join(folder, name + '.jsonl'))], float); p_ = theory.predictions('quarter', n); mine = xs.var(ddof=1) * n / xs.mean() ** 2 / (p_['exact'] / p_['mean'] ** 2 * n)
            ok_r = ok_r and key in LAST['sets'] and LAST['sets'][key] is not None and abs(LAST['sets'][key]['r'] - mine) < 1e-9 and abs(LAST['sets'][key]['rse'] / (mine * math.sqrt(2 / 120000.0)) - 1) < 0.1 and abs(p_['exact'] / p_['mean'] ** 2 * n - 0.37408) < 1e-5
        check('study2: a set\'s r is its variance x n / mean^2 over the quarter disc\'s own line, 0.37408, and its error is near sqrt(2/K) of it', ok_r)
        check('study2: the record of the least shape: its value, its start, its rho, three sides', abs(LAST['floor'].get('least', 0) - 1.3055) < 1e-9 and LAST['floor'].get('seed') == 1 and abs(LAST['floor'].get('rho', 0) - 0.22) < 1e-9 and len(LAST['floor'].get('sides', [])) == 3)
shutil.rmtree(TMP)
print('%d passed, %d failed' % (passed, failed)); sys.exit(1 if failed else 0)
