"""ftest.py: tests of cell2.c.   python -I ftest.py      (the binary is ./cell2, or the one named in the environment as CELL2)"""
import json, math, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); BIN = os.environ.get('CELL2', os.path.join(HERE, 'cell2')); PY = sys.executable
TMP = tempfile.mkdtemp(prefix='agent2-far-'); npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail else ''))
def run(*args):
    r = subprocess.run([BIN] + [str(a) for a in args], capture_output=True, text=True, timeout=180)
    return (json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None), r
# 0. cases worked by hand: points given in the program's own whole-number units (the lift is y + x^2), peeled with walls to the end
def depths(pts):
    f = os.path.join(TMP, 'pts.txt'); open(f, 'w').write(''.join('%d %d\n' % p for p in pts)); o, r = run(8, 2, 1, 1, '-points', f); return o['depths'] if o else r.stderr
HAND = [([(0, 0), (2, 3), (4, 0)], [1, 1, 1], 'the parabola through (0,0) and (4,0) is y = 4 - (x-2)^2: a point at (2,3) is under it and comes off with them'),
        ([(0, 0), (2, 10), (4, 0)], [1, 2, 1], 'a point at (2,10) is over it and waits'),
        ([(0, 0), (2, 4), (4, 0)], [1, 2, 1], 'a point at (2,4) is exactly on it and waits (the program takes corners only; random points all but never meet this)'),
        ([(0, 0), (5, 0), (5, 3)], [1, 1, 2], 'two points one above the other at the right-hand wall: the upper waits'),
        ([(0, 0), (5, 3), (5, 0)], [1, 2, 1], 'the same given in another order'),
        ([(0, 3), (0, 0), (5, 0)], [2, 1, 1], 'and at the left-hand wall'),
        ([(x, y) for y in (0, 1, 2) for x in range(5)], [1] * 5 + [2] * 5 + [3] * 5, 'three rows of five, one above the other: a row to a layer'),
        ([(0, 0), (3000000, 8999999999999), (6000000, 0)], [1, 1, 1], 'three points six million apart, the middle one 1 under the parabola through the others (the numbers pass 2^63: the 128-bit path)'),
        ([(0, 0), (3000000, 9000000000001), (6000000, 0)], [1, 2, 1], 'the middle one 1 over it'),
        ([(0, 0), (3000000, 0), (6000000, 0)], [1, 1, 1], 'the middle one far under it (64-bit products would wrap round here)'),
        ([(7, 7)], [1], 'one point'), ([(1, 5), (2, 5)], [1, 1], 'two points')]
bad = [(pts, want, depths(pts)) for pts, want, why in HAND if depths(pts) != want]
ok('twelve cases worked by hand (%s)' % '; '.join(why for pts, want, why in HAND[:10]), not bad, bad)
# 1. the streaming way against the plain way (all points made beforehand, every layer the hull of all that is left)
bad = []; compared = 0
for C, w, HM, seed in ((256, 2, 30, 1), (256, 2, 30, 2), (512, 1.5, 60, 7), (360, 1, 25, 3), (2048, 2, 150, 5), (512, 2, 200, 9), (400, 3, 40, 4)):
    o, _ = run(C, w, HM, seed, '-check'); compared += o['check_compared'] if o else 0
    if not o or o['check_differ'] != 0 or o['check_compared'] < 0.8 * C * w * HM or o['plain_layers'] != o['layers']: bad.append((C, w, HM, seed))
ok('streaming = plain, point for point, on seven windows (%d points compared; one high enough for columns to drop their spent points)' % compared, not bad, bad)
# 2. against an outside peeling in Python: three copies, exact whole numbers, its own chain
bad = []
for C, w, HM, seed in ((180, 2, 8, 3), (256, 1.5, 12, 4), (200, 2, 10, 8)):
    d = os.path.join(TMP, 'dump.txt'); o, _ = run(C, w, HM, seed, '-check', '-dump', d)
    r = subprocess.run([PY, '-I', os.path.join(HERE, 'ref.py'), d], capture_output=True, text=True)
    if not o or r.returncode != 0 or 'different from cell2: 0' not in r.stdout: bad.append((C, w, HM, seed, r.stdout.strip()[:80]))
ok('streaming = an outside peeling in Python (three copies, exact numbers), on three windows', not bad, bad)
# 3. what is written out is what was counted: bands of the profile recomputed from the dumped depths; the slope recomputed from the profile
d = os.path.join(TMP, 'dump.txt'); pf = os.path.join(TMP, 'prof.txt'); sf = os.path.join(TMP, 'snap.bin'); o, _ = run(512, 2, 40, 6, '-check', '-dump', d, '-profile', pf, '-snap', sf)
lines = open(d).read().split('\n'); WU, HMU = map(int, lines[0].split()); bands = {}
for l in lines[1:]:
    if l.strip():
        x, y, dep = map(int, l.split())
        if y <= HMU and (y >> 21) < 40: b = bands.setdefault(y >> 21, [0, 0, 0]); b[0] += 1; b[1] += dep; b[2] += dep * dep
xs = [int(l.split()[0]) % 2048 for l in lines[1:] if l.strip()]; eighth = [0] * 8
for x in xs: eighth[x // 256] += 1
chi = sum((e - len(xs) / 8.0) ** 2 / (len(xs) / 8.0) for e in eighth)
ok('across its column a point is anywhere alike: %d points by eighths of the column, chi-square %.1f on 7' % (len(xs), chi), chi < 24.3 and len(xs) > 40000, eighth)
prof = {int(l.split()[0]): list(map(float, l.split()[1:])) for l in open(pf) if l.strip()}
good = all(b in prof and prof[b][0] == v[0] and abs(prof[b][1] - v[1] / v[0]) < 1e-5 and abs(prof[b][2] - (v[2] / v[0] - (v[1] / v[0]) ** 2)) < 1e-4 for b, v in bands.items()) and len(prof) == 40
n = sy = sd = syy = syd = 0
for b, (c, mu, var) in prof.items():
    if b >= 20: y = b + 0.5; n += c; sy += c * y; sd += c * mu; syy += c * y * y; syd += c * y * mu
slope = (syd - sy * sd / n) / (syy - sy * sy / n)
ok('the profile written out (points, mean depth, variance of depth in each band 1 high) is recomputed from the dumped depths; the slope reported is the slope of the profile over its upper half', good and abs(slope - o['slope_upper_half']) < 2e-6 and WU == 512 * 2048, (good, slope, o['slope_upper_half']))
# 3b. the slabs: the mean depth of each column's points in each slab, recomputed from the dumped depths
import array
raw = array.array('d'); raw.frombytes(open(sf, 'rb').read()); hs = o['snap_heights']; acc = {}
for l in lines[1:]:
    if l.strip():
        x, y, dep = map(int, l.split())
        if y <= HMU:
            for k, h in enumerate(hs):
                if h <= (y >> 21) < h + 4: a = acc.setdefault((k, x // 2048), [0, 0]); a[0] += 1; a[1] += dep
wrong = 0; empty = 0
for k in range(len(hs)):
    for c in range(512):
        v = raw[k * 512 + c]; a = acc.get((k, c))
        if a is None: empty += 1; wrong += not math.isnan(v)
        else: wrong += not abs(v - a[1] / a[0]) < 1e-9
ok('the slabs written out (%d slabs, the top one at %d; the mean depth of each column in each, %d of %d without a point) are recomputed from the dumped depths; none overlaps another' % (len(hs), hs[0], empty, len(hs) * 512),
   len(raw) == len(hs) * 512 and wrong == 0 and hs[0] == 36 and len(hs) >= 6 and all(a - b >= 4 for a, b in zip(hs, hs[1:])) and 0 < empty < 0.01 * len(raw), (wrong, empty, hs))
o2, _ = run(512, 2, 40, 6, '-check', '-profile', os.path.join(TMP, 'prof2.txt'))
ok('asking for the slabs changes nothing else: the same line of JSON but for them, the same profile', {k: v for k, v in o.items() if k != 'snap_heights'} == o2 and open(pf).read() == open(os.path.join(TMP, 'prof2.txt')).read())
# 4. shearing changes no depth, and the shear is a real one
bad = []
for C, HM, seed, S in ((200, 20, 1, 4096), (200, 20, 2, -6000), (300, 12, 3, 1), (180, 30, 4, 20480)):
    o, _ = run(C, 2, HM, seed, '-sheartest', S)
    if not o or o['differ'] != 0 or o['moved'] < 0.99 * o['points'] or o['layers'] != o['layers_sheared'] or o['points'] < 0.8 * C * 2 * HM or abs(o['slope'] - S / 2048.0) > 1e-3: bad.append((C, HM, seed, S, o))
ok('a window sheared by slopes of 2, -2.93, 0.0005 and 10 keeps the depth of every point (peeled to the end, with walls); nearly every point is really moved', not bad, bad)
bad = []
for C, HM, seed, S in ((1200, 15, 5, 3000), (1500, 10, 6, -204800)):
    o, _ = run(C, 2, HM, seed, '-sheartest', S)
    if not o or o['differ'] != 0 or o['moved'] < 0.99 * o['points'] or o['layers'] != o['layers_sheared'] or o['W'] < 2400: bad.append((C, HM, seed, S, o))
ok('the same on windows 2,400 and 3,000 wide, where the last points left are far enough apart for the 128-bit arithmetic, with slopes of 1.46 and -100', not bad, bad)
bad = []
for C, HM, seed, S in ((200, 20, 1, 2 ** 40), (2500, 5, 3, 2 ** 40), (2500, 5, 4, -(2 ** 40)), (2500, 5, 5, 2 ** 40)):
    o, _ = run(C, 2, HM, seed, '-sheartest', S)
    if not o or o['differ'] != 0 or o['moved'] < 0.99 * o['points'] or o['layers'] != o['layers_sheared'] or o['points'] < 0.8 * C * 2 * HM: bad.append((C, HM, seed, S, o))
ok('the two ways of doing the arithmetic agree: with a shear of 2^40 units every turn of the sheared window goes by the 128-bit path and every turn of the unsheared one by the 64-bit path (but for the last, far-apart points of a window 5,000 wide), and no depth differs (four windows)', not bad, bad)
o, _ = run(400, 2, 40, 1, '-bendtest', 1024); o2, _ = run(400, 2, 40, 1, '-sheartest', 1024)
ok('a control: bending the window (every point up by x^2/4, which is no symmetry) changes most depths (%d of %d) and the count of layers (%d to %d), where the shear of the same window changes none' % (o['differ'], o['points'], o['layers'], o['layers_sheared']),
   o['differ'] > 0.5 * o['points'] and o['layers_sheared'] < 0.95 * o['layers'] and o2['differ'] == 0 and o2['points'] == o['points'])
# the margin: what is proved enough is enough, and less is not
base, _ = run(512, 2, 40, 6, '-check'); m0, _ = run(512, 2, 40, 6, '-check', '-margin', 0); m25, _ = run(512, 2, 40, 6, '-check', '-margin', 0.25); m3, _ = run(512, 2, 40, 6, '-check', '-margin', 3); neg = run(512, 2, 40, 6, '-check', '-margin', -1)[1]
strip = lambda o: {k: v for k, v in o.items() if k not in ('candidates', 'made', 'seconds')}
ok('the margin of the candidates: with none the check finds %d wrong depths of %d, with half of what is proved %d, with six times as much none and the same answer as without the option; with less than none the run stops (exit 4)' % (m0['check_differ'], m0['check_compared'], m25['check_differ']),
   base['check_differ'] == 0 and m0['check_differ'] > 100 and m25['check_differ'] > 0 and m3['check_differ'] == 0 and strip(m3) == strip(base) and m3['candidates'] > base['candidates'] and m3['made'] > base['made'] and neg.returncode == 4, (strip(m3), strip(base), neg.returncode))
# 5. the density and the slope: 1024 x 2 wide, 300 high
pf = os.path.join(TMP, 'prof5.txt'); o, _ = run(1024, 2, 300, 12, '-profile', pf); made_per_area = o['made'] / (2048.0 * 300)
rows5 = [list(map(float, l.split())) for l in open(pf) if l.strip()]; cnt = [r[1] for r in rows5]; top_mean, top_sd = rows5[-1][2], math.sqrt(rows5[-1][3]); dens = sum(cnt) / (2048.0 * 300); worst = max(abs(c - 2048) / math.sqrt(2048) for c in cnt); disp = sum((c - sum(cnt) / len(cnt)) ** 2 for c in cnt) / (len(cnt) - 1) / (sum(cnt) / len(cnt))
ok('one point to the unit of area (%.4f over 614,400; the worst band of 300 is %.1f standard deviations from 2048; the variance of the count in a band over its mean is %.2f, as for points thrown independently), no more than 5 in 100 made beyond the top (%.3f), a slope near 1.326 (%.4f), and as many layers in all (%d) as the deepest point at the top needs (mean depth there %.1f, standard deviation %.1f)' % (dens, worst, disp, made_per_area, o['slope_upper_half'], o['layers'], top_mean, top_sd),
   abs(dens - 1) < 4 / math.sqrt(614400) and len(cnt) == 300 and worst < 4.5 and 0.75 < disp < 1.25 and 1.0 < made_per_area < 1.05 and 1.31 < o['slope_upper_half'] < 1.34 and top_mean < o['layers'] < top_mean + 6 * top_sd, (dens, worst, made_per_area, o['layers'], top_mean, top_sd))
# 6. the same seed gives the same window; another seed another; the period and the column width are as asked
a, _ = run(256, 2, 30, 1); b, _ = run(256, 2, 30, 1); c, _ = run(256, 2, 30, 2)
ok('the same seed gives the same run, another seed another; the period is columns times width', a == b and a['made'] != c['made'] and a['W'] == 512.0 and run(360, 1.5, 10, 1)[0]['W'] == 540.0)
# 6b. the first batch's seeding is kept: with -seeding 1 the program gives, digit for digit, what the build that ran the first fifteen long windows gave
want = json.load(open(os.path.join(HERE, 'asrun', 'run-2048-2-300-77.json'))); pf1 = os.path.join(TMP, 'prof-asrun.txt'); got, _ = run(2048, 2, 300, 77, '-seeding', 1, '-profile', pf1)
new, _ = run(2048, 2, 300, 77)
ok('with -seeding 1 the program gives what the build of the first batch gave on a window 4,096 wide and 300 high (the same line of JSON but for the seconds, the same profile); without it, another window, marked seeding 2',
   bool(got) and {k: v for k, v in got.items() if k != 'seconds'} == {k: v for k, v in want.items() if k != 'seconds'} and open(pf1).read() == open(os.path.join(HERE, 'asrun', 'profile-2048-2-300-77.txt')).read()
   and new.get('seeding') == 2 and 'seeding' not in got and new['made'] != got['made'])
# 6b'. and the second batch's build: its profile and its slabs on the same small window, byte for byte
pf2 = os.path.join(TMP, 'prof-asrun2.txt'); sf2 = os.path.join(TMP, 'snap-asrun2.bin'); got2, _ = run(2048, 2, 300, 77, '-profile', pf2, '-snap', sf2); want2 = json.load(open(os.path.join(HERE, 'asrun2', 'run-2048-2-300-77.json')))
ok('and what the build of the second batch gave on the same window: the same line of JSON but for the seconds, the same profile, the same file of slabs',
   bool(got2) and {k: v for k, v in got2.items() if k != 'seconds'} == {k: v for k, v in want2.items() if k != 'seconds'} and open(pf2).read() == open(os.path.join(HERE, 'asrun2', 'profile-2048-2-300-77.txt')).read()
   and open(sf2, 'rb').read() == open(os.path.join(HERE, 'asrun2', 'snap-2048-2-300-77.bin'), 'rb').read())
# 6c. the rippled floor: no point below y = A (1 + cos(2 pi x / L)), points right down to it, and the streaming still agrees with the plain way
d = os.path.join(TMP, 'dumpf.txt'); o, _ = run(512, 2, 60, 3, '-check', '-floor', 10, 128, '-dump', d); below = 0; low20 = 0; crest = []; trough = []
for l in open(d).read().split('\n')[1:]:
    if l.strip():
        x, y, dep = map(int, l.split()); xr, yr = x / 1024.0, y / 2097152.0
        if yr < 10 * (1 + math.cos(2 * math.pi * xr / 128)) - 1e-6: below += 1
        if yr < 20: low20 += 1
        m = xr % 128
        if m < 4 or m > 124: crest.append(yr)
        if 60 < m < 68: trough.append(yr)
ok('a rippled floor (10 high, 128 long, on a window 1,024 wide): no point below it; over the crests the lowest point is at %.2f and over the troughs at %.2f; %d points below 20 where the room under 20 is 10,240; and the streaming agrees with the plain way on %d points' % (min(crest), min(trough), low20, o['check_compared']),
   bool(o) and o['check_differ'] == 0 and o['check_compared'] > 40000 and below == 0 and 19.7 < min(crest) < 20.6 and min(trough) < 1.0 and abs(low20 - 10240) < 400, (below, min(crest), min(trough), low20))
# 7. what is refused
ok('refused: an odd number of columns, a period under 360, a height of nothing, an unknown option, a seeding that is neither, a ripple whose length does not divide the period',
   all(run(*args)[1].returncode == 2 for args in ((255, 2, 30, 1), (100, 2, 30, 1), (256, 2, 0, 1), (256, 2, 30, 1, '-what'), (256, 2, 30, 1, '-seeding', 3), (512, 2, 30, 1, '-floor', 10, 100))) and run(512, 2, 30, 1, '-floor', 10, 128)[1].returncode == 0)
import shutil; shutil.rmtree(TMP)
print('\n%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
