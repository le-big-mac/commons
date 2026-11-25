"""twoheights.py: is the depth at one height tied to the depth at another as the equation says?   python -I twoheights.py
Done after the first referee's report, which said that my four tests of the picture do not look at two heights at once; and done
again after the second addition's referee pointed out what a mean over a stretch does to a variance. Not sealed, and not refereed.
For the equation dT/dy = nu T_xx + noise, started level, the covariance of the depth at one place at heights y1 < y2 is
    D / (2 sqrt(pi nu)) x [sqrt(y1 + y2) - sqrt(y2 - y1)],
which at y1 = y2 is the variance D sqrt(y / (2 pi nu)). On a ring of length W the mean of the ring is left out of what I measure,
which takes D y1 / W off the covariance and D y / W off each variance. So the correlation between two heights has neither D nor nu
in it, but for that small term (nu = 1/3 and W = 32,768 are used for it).
What was kept of the front at a height is, for each column 2 wide, the mean depth of its points in a slab 4 thick. The covariance
of two such slabs far apart is the covariance of the depths. But the variance of a column's mean is less than the variance of
depth at a point: a mean over a slab 4 thick and a column 2 wide smooths the depth (the equation itself puts the first at
0.52 D; the measured difference is printed below). My first reckoning divided the covariance by the column means' own variances
and set that against the formula for points, and so found the equation "1 to 9 parts in 100 low". Here both are given:
  (1) covariance over the column means' variances (as first reckoned);
  (2) covariance over the variances of depth among the points of the same heights (from the same windows' profiles: bands 1 thick,
      less what the band's thickness adds), which is what the formula is about.
Twelve windows; pairs of slabs whose heights are in the ratio 2^(1/8), 2^(1/4), 2^(1/2), 2, 4 and 8, the lower at 250 or above.
Needs the raw files of slabs (runs/snap-*.bin) and the profiles; what it finds for each window and pair is kept in twoheights.json."""
import glob, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); KEPT = os.path.join(HERE, 'twoheights.json'); NU = 1 / 3.0; THICK = 1.326 ** 2 / 12
raws = sorted(glob.glob(os.path.join(HERE, 'runs', 'snap-*.bin')))
STEPS = (1, 2, 4, 8, 16, 24)
if raws:
    kept = {'windows': []}
    for sf in raws:
        o = json.load(open(sf.replace('snap-', 'run-').replace('.bin', '.json'))); hs = o['snap_heights']; raw = np.fromfile(sf, dtype=np.float64).reshape(len(hs), int(o['C'])); pairs = []
        prof = np.loadtxt(sf.replace('snap-', 'profile-').replace('.bin', '.txt')); vb = {h: float(prof[h:h + 4, 3].mean() - THICK) for h in hs}; vc = {h: float(np.nanvar(raw[k])) for k, h in enumerate(hs)}
        for m in STEPS:
            for k in range(len(hs) - m):
                if hs[k + m] >= 250:
                    a, b = raw[k], raw[k + m]; ok = ~np.isnan(a) & ~np.isnan(b); cov = float(np.cov(a[ok], b[ok], ddof=0)[0, 1])
                    pairs.append([m, hs[k] + 2, hs[k + m] + 2, cov, vc[hs[k]], vc[hs[k + m]], vb[hs[k]], vb[hs[k + m]]])
        kept['windows'].append({'seed': o['seed'], 'W': o['W'], 'pairs': pairs})
    json.dump(kept, open(KEPT, 'w'))
kept = json.load(open(KEPT)); W = kept['windows'][0]['W']
def predicted(y1, y2):         # y1 < y2; D divides out
    c = (math.sqrt(y1 + y2) - math.sqrt(y2 - y1)) / (2 * math.sqrt(math.pi * NU)) - y1 / W
    v = lambda y: math.sqrt(y / (2 * math.pi * NU)) - y / W
    return c / math.sqrt(v(y1) * v(y2))
GROUPS = ((0, 4000), (4000, 16000), (16000, 64000), (64000, 10 ** 9))
def table(which, title):
    print(title); print('  ratio      upper under 4,000     4,000 to 16,000     16,000 to 64,000     64,000 and up')
    pos = 0; cells = 0
    for m in STEPS:
        row = []
        for lo, hi in GROUPS:
            per = []
            for w in kept['windows']:
                d = [p[3] / math.sqrt(p[4] * p[5] if which == 1 else p[6] * p[7]) - predicted(p[2], p[1]) for p in w['pairs'] if p[0] == m and lo <= p[1] - 2 < hi]
                if d: per.append(np.mean(d))
            if len(per) < 2: row.append('       -        '); continue
            row.append('%+.4f (%.4f)' % (np.mean(per), np.std(per, ddof=1) / math.sqrt(len(per)))); cells += 1; pos += np.mean(per) > 0
        print('  %-8s   %s' % ('2^(%d/8)' % m, '    '.join(row)))
    print('  measured is above predicted in %d of the %d cells' % (pos, cells)); return pos, cells
print('%d windows. Measured less predicted correlation between the depths of a column at two heights, by the ratio of the heights and by the upper height' % len(kept['windows']))
print('(mean over pairs and windows; standard error from the windows).\n')
table(1, '(1) As first reckoned: the covariance of the column means over their own variances.')
print()
table(2, '(2) The covariance of the column means over the variances of depth among the points at the two heights.')
print('\nWhat a column\'s mean loses: variance of depth among points less variance of the column means (mean over windows), by height: ' + '; '.join(
    '%.2f at %d' % (np.mean([np.mean([p[6] - p[4] for p in w['pairs'] if p[0] == 1 and abs(p[1] - 2 - h) < 3]) for w in kept['windows']]), h) for h in (127996, 63998, 31999, 16000, 8000, 4000, 2000, 1000)))
print('The equation gives 0.52 D = 0.56 for the mean over the slab\'s thickness alone (D / (2 sqrt(pi nu)) x (8/15) sqrt(4)); the mean across the column\'s width takes off more, and the few points of a column add some back.')
print('\nBy the ratio of the heights, the upper at 16,000 or above: predicted; measured by (1) and by (2) (standard error from the windows); (2) over predicted')
worst = 0
for m in STEPS:
    r1 = []; r2 = []; pr = []
    for w in kept['windows']:
        mine = [p for p in w['pairs'] if p[0] == m and p[1] >= 16002]; r1.append(np.mean([p[3] / math.sqrt(p[4] * p[5]) for p in mine])); r2.append(np.mean([p[3] / math.sqrt(p[6] * p[7]) for p in mine])); pr = [predicted(p[2], p[1]) for p in mine]
    pm = float(np.mean(pr)); m2 = float(np.mean(r2)); worst = max(worst, abs(m2 / pm - 1))
    print('  %-8s   %.4f      %.4f (%.4f)      %.4f (%.4f)      %.3f' % ('2^(%d/8)' % m, pm, np.mean(r1), np.std(r1, ddof=1) / math.sqrt(len(r1)), m2, np.std(r2, ddof=1) / math.sqrt(len(r2)), m2 / pm))
print('by (2) the measured correlation is within %.1f in 100 of the predicted at every ratio, the upper height at 16,000 or above' % (100 * worst))
