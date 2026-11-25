"""ruler.py: study.py tried on made-up windows whose answers are known.   python -I ruler.py
Two sets of fifteen made-up profiles (twelve to 64,000 and three to 128,000, like the real ones), without noise:
  set 1: mean depth 1.3259 y + 0.4, variance 0.75 y^(1/2) (+ what the band adds): every line of the sheet must be HELD, with the numbers put in;
  set 2: mean depth (4/3) y + 0.5 y^(1/3), variance 0.05 y^(2/3): lines A2 to A6 must all be FAILED, with the numbers put in.
A1 (the shear) is run on the real program both times and is not what is tried here."""
import json, math, os, re, subprocess, sys, tempfile, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); THICK = 1.326 ** 2 / 12
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail else ''))
def make(d, mean, var):
    for HM, seeds in ((64000, range(1, 13)), (128000, range(1, 4))):
        y = np.arange(HM) + 0.5; mu = mean(y); v = var(y) + THICK; sl = float(np.polyfit(y[HM // 2:], mu[HM // 2:], 1)[0])
        for s in seeds:
            with open(os.path.join(d, 'profile-%d-%d.txt' % (HM, s)), 'w') as f:
                for b in range(HM): f.write('%d 32768 %.6f %.6f\n' % (b, mu[b], v[b]))
            json.dump({'HM': HM, 'seed': s, 'W': 32768.0, 'wcol': 2.0, 'layers': int(mu[-1]) + 60, 'slope_upper_half': round(sl, 6)}, open(os.path.join(d, 'run-%d-%d.json' % (HM, s)), 'w'))
def study(d):
    r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'study.py')], capture_output=True, text=True, env=dict(os.environ, FAR_RUNS=d))
    if r.returncode: print(r.stderr[-600:])
    return r.stdout
def verdict(out, k): m = re.search(r'LINE A%d \([a-z]+, odds [0-9.]+\): ([A-Z]+)\. (.*)' % k, out); return (m.group(1), m.group(2)) if m else ('', '')
def nums(text): return [float(x) for x in re.findall(r'[-+]?\d+\.\d+', text)]

d1 = tempfile.mkdtemp(prefix='agent2-ruler1-'); make(d1, lambda y: 1.3259 * y + 0.4, lambda y: 0.75 * np.sqrt(y)); o1 = study(d1); shutil.rmtree(d1)
v = {k: verdict(o1, k) for k in range(1, 7)}
ok('set 1 (a half power, 1.3259, no correction): all six lines HELD', all(v[k][0] == 'HELD' for k in range(1, 7)), [v[k][0] for k in v])
def a2rows(out): return [nums(l.split(':', 1)[1])[:4] for l in out.split('\n') if 'bands' in l and 'steps' in l and l.startswith('    ') and ':' in l and 'Fitted' not in l]
r2 = a2rows(o1); n2 = nums(v[2][1])
ok('   A2 gives the exponent put in, 0.500, for each of the four sets of windows and both ways of fitting when what the band adds is taken off; left in, it is a shade lower (%.3f to %.3f over all)' % (n2[0], n2[1]),
   len(r2) == 4 and all(r[0] == 0.5 and r[2] == 0.5 and 0.498 <= r[1] <= 0.5 and 0.498 <= r[3] <= 0.5 for r in r2) and n2[1] == 0.5, r2)
n3 = nums(v[3][1]); ok('   A3 gives 0.500 for the last doubling of each kind (%s)' % ', '.join('%.3f' % x for x in n3[:6]), all(x == 0.5 for x in n3[:6]) and len(n3) == 7)
n4 = nums(v[4][1]); want = 0.75 / math.sqrt(1.3259)
ok('   A4 gives 0.75 / sqrt(1.3259) = %.3f at each top (%s)' % (want, ', '.join('%.3f' % x for x in n4[:3])), all(abs(x - want) < 0.0015 for x in n4[:5]))
n5 = nums(v[5][1]); ok('   A5 gives the slope put in, 1.325900, every way (%.6f to %.6f)' % (n5[2], n5[3]), n5[2] == 1.3259 and n5[3] == 1.3259 and '5 give' in v[5][1])
n6 = nums(v[6][1]); ok('   A6 gives no change (%s)' % ', '.join('%+.2f' % x for x in n6[:3]), all(abs(x) < 0.005 for x in n6[:3]))
rows = [l for l in o1.split('\n') if ' at 64000' in l and 'constant' in l]
ok('   and the offset put in, 0.40, at each height of the table', len(rows) == 3 and all(all(abs(x - 0.40) < 0.006 for x in nums(l.split(':', 2)[2].split(';')[0])[0::1] if abs(x) < 3) for l in rows), rows[:1])

d2 = tempfile.mkdtemp(prefix='agent2-ruler2-'); make(d2, lambda y: (4.0 / 3) * y + 0.5 * np.cbrt(y), lambda y: 0.05 * np.cbrt(y) ** 2); o2 = study(d2); shutil.rmtree(d2)
v = {k: verdict(o2, k) for k in range(1, 7)}
ok('set 2 (a two-thirds power, 4/3, a correction growing as the cube root): lines A2 to A6 all FAILED', all(v[k][0] == 'FAILED' for k in range(2, 7)) and v[1][0] == 'HELD', [v[k][0] for k in v])
r2 = a2rows(o2); n2 = nums(v[2][1])
ok('   A2 gives 0.667 with what the band adds taken off, and less with it left in (%.3f to %.3f over all)' % (n2[0], n2[1]), len(r2) == 4 and all(r[0] == 0.667 and r[2] == 0.667 and 0.655 < r[1] < 0.667 and 0.655 < r[3] < 0.667 for r in r2), r2)
n3 = nums(v[3][1]); ok('   A3 gives 0.667 for each last doubling', all(x == 0.667 for x in n3[:6]))
n4 = nums(v[4][1]); w64 = 0.05 * 63680.0 ** (2 / 3.0) / math.sqrt(4 / 3.0 * 63680); w128 = 0.05 * 127360.0 ** (2 / 3.0) / math.sqrt(4 / 3.0 * 127360)
ok('   A4 gives what the made-up law gives at the two tops, %.3f and %.3f (%.3f, %.3f, %.3f)' % (w64, w128, n4[0], n4[1], n4[2]), abs(n4[0] - w64) < 0.003 and abs(n4[1] - w64) < 0.003 and abs(n4[2] - w128) < 0.003)
n5 = nums(v[5][1]); ok('   A5: none of the five ways inside; slopes a little over 4/3 (%.6f to %.6f)' % (n5[2], n5[3]), '0 give' in v[5][1] and 1.33333 < n5[2] <= n5[3] < 1.3336)
def want6(top):
    y = np.arange(top) + 0.5; mu = (4.0 / 3) * y + 0.5 * np.cbrt(y); a = float(np.polyfit(y[top // 2:], mu[top // 2:], 1)[0]); off = mu - a * y
    return float(off[top - 100:].mean() - off[3950:4050].mean())
n6 = nums(v[6][1]); ok('   A6 gives the change the made-up law gives: %+.2f to 64,000 and %+.2f to 128,000 (%+.2f, %+.2f)' % (want6(64000), want6(128000), n6[0], n6[1]), abs(n6[0] - want6(64000)) < 0.02 and abs(n6[1] - want6(128000)) < 0.02)
print('\n%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
