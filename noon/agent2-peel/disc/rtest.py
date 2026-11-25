"""rtest.py: tests of rings.c and make.py.   python -I rtest.py     (RINGS in the environment names another build of rings)"""
import json, math, os, subprocess, sys, tempfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RINGS = os.environ.get('RINGS', os.path.join(HERE, 'rings')); PEEL = os.path.join(HERE, '..', 'peel'); R = 536870912.0
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail else ''))
def rings(text, *args):
    r = subprocess.run([RINGS] + [str(a) for a in args], input=text, capture_output=True, text=True, timeout=120)
    return (json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None), r
# 1. cases worked by hand: a few points put exactly
H = '{"shape":"disc","n":%d,"seed":9,"layers":7}\n'
pts = [(R / 2, 0, 7), (0, R / 2, 5), (0.509 * R, 0, 99), (-0.4925 * R, 0, 3), (0, -0.1 * R, 2)]
o, _ = rings(H % len(pts) + ''.join('%d %d %d\n' % (round(x), round(y), d) for x, y, d in pts), 1000); A0 = 0.75 * 1.3259 * (1000 / math.pi) ** (2 / 3.0)
r9 = o['rings'][9]; r1 = o['rings'][1]
ok('by hand: three points in the annulus at 0.5 (at angles 0, 90 and 180 degrees, depths 7, 5, 3), one just outside it (0.509) left out: 3 points, depths summing to 15, squares to 83',
   o['n'] == 5 and o['seed'] == 9 and o['layers'] == 7 and r9[0] == 3 and r9[2] == 15 and r9[3] == 83 and abs(r9[4] - (0.5 + 0.5 + 0.4925)) < 1e-6 and abs(r9[6] - (3.5 + 2.5 + 3 * 0.4925)) < 1e-6, r9[:7])
ok('   their cosines and sines: sum of cos(theta) = 1 + 0 - 1, of sin = 1; of depth x cos(theta) = 7 - 3, of depth x sin = 5; for twice the angle 1 - 1 + 1 and 7 - 5 + 3; for three times 1 + 0 - 1, sin -1, depth x cos 7 - 3, depth x sin -5; four times 3 and 15',
   all(abs(a - b) < 1e-6 for a, b in zip(r9[7:], [0, 1, 4, 5, 1, 0, 5, 0, 0, -1, 4, -5, 3, 0, 15, 0])), r9[7:])
ok('   the profile taken off is 0.75 x 1.3259 x (N0/pi)^(2/3) x (1 - rho^(4/3)), with N0 as given and not the number of points that came', abs(r9[1] - (15 - A0 * ((1 - 0.5 ** (4 / 3.0)) * 2 + 1 - 0.4925 ** (4 / 3.0)))) < 1e-6 and abs(r1[1] - (2 - A0 * (1 - 0.1 ** (4 / 3.0)))) < 1e-6 and r1[0] == 1 and abs(r1[8] + 1) < 1e-9 and abs(r1[10] + 2) < 1e-9)
o2, _ = rings(H % len(pts) + ''.join('%d %d %d\n' % (round(x), round(y), d) for x, y, d in pts), 1000, 0.01)
ok('   with a half-width of 0.01 the point at 0.509 is in', o2['rings'][9][0] == 4 and o2['half'] == 0.01 and o['half'] == 0.008)
# 2. a real cloud, every sum recomputed in Python
r = subprocess.run([PEEL, 'disc', '30000', '4242', '-depths', '-'], capture_output=True, text=True); o, _ = rings(r.stdout, 30000)
a = np.array([l.split() for l in r.stdout.split('\n')[1:] if l.strip()], dtype=float); rho = np.hypot(a[:, 0], a[:, 1]) / R; th = np.arctan2(a[:, 1], a[:, 0]); d = a[:, 2]; A0 = 0.75 * 1.3259 * (30000 / math.pi) ** (2 / 3.0); worst = 0; total = 0
for k in range(19):
    c = 0.05 * (k + 1); m = np.abs(rho - c) <= 0.008; total += int(m.sum())
    want = [m.sum(), (d[m] - A0 * (1 - rho[m] ** (4 / 3.0))).sum(), d[m].sum(), (d[m] ** 2).sum(), rho[m].sum(), (rho[m] ** 2).sum(), (rho[m] * d[m]).sum()]
    for mm in (1, 2, 3, 4): want += [np.cos(mm * th[m]).sum(), np.sin(mm * th[m]).sum(), (d[m] * np.cos(mm * th[m])).sum(), (d[m] * np.sin(mm * th[m])).sum()]
    worst = max(worst, max(abs(x - y) / max(1.0, abs(y)) for x, y in zip(o['rings'][k], want)))
ok('a cloud of 30,000 points: all 19 x 23 sums as numpy finds them from the same points (%d points fall in annuli; the worst difference is %.1e of the sum)' % (total, worst), worst < 1e-9 and o['n'] == 30000 and 8000 < total < 11000 and len(o['rings']) == 19 and all(len(x) == 23 for x in o['rings']), worst)
# 3. what is refused
ok('refused: no summary line; fewer points than the summary says; a half-width of nothing or over 0.025; no size', rings('1 2 3\n', 1000)[1].returncode == 3 and rings(H % 4 + '1 2 3\n', 1000)[1].returncode == 3 and rings(H % 1 + '1 2 3\n', 1000, 0)[1].returncode == 2 and rings(H % 1 + '1 2 3\n', 1000, 0.03)[1].returncode == 2 and rings(H % 1 + '1 2 3\n')[1].returncode == 2)
# 4. make.py: exact clouds have exactly N0 points and the seeds asked; chance clouds a number that scatters as the Poisson law's, the same every time for the same seed
tmp = tempfile.mkdtemp(prefix='agent2-rtest-'); PY = sys.executable
def mk(kind, n0, K, seed0):
    f = os.path.join(tmp, '%s-%d-%d.jsonl' % (kind, n0, seed0)); r = subprocess.run([PY, '-I', os.path.join(HERE, 'make.py'), kind, str(n0), str(K), str(seed0), f, '8'], capture_output=True, text=True); return [json.loads(l) for l in open(f)], r.stdout
e, eo = mk('exact', 2000, 40, 111000); c, co = mk('chance', 2000, 400, 222000); c2, _ = mk('chance', 2000, 400, 222000)
ns = np.array([x['n'] for x in c])
ok('make.py, exactly n: 40 clouds of 2,000 points each, seeds 111001 to 111040, none failed', len(e) == 40 and all(x['n'] == 2000 and x['n0'] == 2000 for x in e) and sorted(x['seed'] for x in e) == list(range(111001, 111041)) and '0 failed' in eo)
ok('make.py, the number left to chance: 400 clouds, mean number %.1f and variance %.0f where the Poisson law has 2,000 and 2,000; the same numbers again from the same seed; the profile taken off is for 2,000' % (ns.mean(), ns.var(ddof=1)),
   len(c) == 400 and abs(ns.mean() - 2000) < 4 * math.sqrt(2000 / 400.0) and 0.75 < ns.var(ddof=1) / 2000 < 1.3 and sorted((x['seed'], x['n']) for x in c) == sorted((x['seed'], x['n']) for x in c2) and all(x['n0'] == 2000 for x in c) and len(set(ns)) > 50)
z, zo = mk('exact', 0, 3, 333000)
ok('make.py says how many clouds failed: three clouds of no points are three failures, and nothing is written for them', len(z) == 0 and '3 clouds asked, 3 failed' in zo and '0 failed' in co)
import shutil; shutil.rmtree(tmp)
print('\n%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
