"""study.py: the thirteen sealed lines, each computed from the runs and judged.   python -I study.py > study.out
Reads runs/discs-small.jsonl (the discs of batch.sh), runs/large.jsonl (batch2.sh), runs/polygons.jsonl (batch4.sh), runs/profiles/ (twenty radial profiles at
a million points; made here if missing), and runs the grid and the stretched clouds itself."""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); P = lambda *a: os.path.join(HERE, *a)
def load(name):
    out = []
    for l in open(P('runs', name)):
        l = l.strip()
        if l: out.append(json.loads(l))
    return out
R = load('discs-small.jsonl') + load('large.jsonl') + load('polygons.jsonl')
def sel(shape, n): return [r for r in R if r['shape'] == shape and r['n'] == n]
def mean(v): return sum(v) / len(v)
def sd(v): m = mean(v); return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))
def se(v): return sd(v) / math.sqrt(len(v))
def stat(rows, key): v = [r[key] for r in rows]; return mean(v), se(v)
verdicts = []
def line(n, kind, odds, held, text):
    verdicts.append((n, kind, odds, held))
    print('LINE %d (%s, odds %s): %s. %s\n' % (n, kind, odds, 'HELD' if held else 'FAILED', text))

sizes = sorted(set(r['n'] for r in R if r['shape'] == 'disc'))
print('The discs: n, clouds, mean layers, sd of layers, and the three estimates of alpha (mean, standard error)')
for n in sizes:
    rows = sel('disc', n); N = [r['layers'] for r in rows]
    print('  n = %9d  clouds %4d  layers %10.2f  sd %6.2f  a_tot %.5f (%.5f)  a_prof %.5f (%.5f)  a_size %.5f (%.5f)' % (
        (n, len(rows), mean(N), sd(N)) + stat(rows, 'a_tot') + stat(rows, 'a_prof') + stat(rows, 'a_size')))
big = max(n for n in sizes if len(sel('disc', n)) >= 8)
B = sel('disc', big)
ap, ape = stat(B, 'a_prof'); at, ate = stat(B, 'a_tot'); az, aze = stat(B, 'a_size')
print('\nThe largest n with at least 8 clouds: %d (%d clouds)\n' % (big, len(B)))

# ---- 1 ----
terms = [tuple(map(int, l.split())) for l in open(os.path.expanduser('~/peel-data/oeis-b/b290966.txt')) if re.match(r'^\d+ \d+', l)]
bad = 0
for g, a in terms:
    L = json.loads(subprocess.run([P('peel'), 'grid', str(g), '0', '-plain', '-vertices'], capture_output=True, text=True).stdout)['layers']
    if L != a: bad += 1
first15 = [a for g, a in terms[:15]]
line(1, 'read', 0.9, first15 == [1, 1, 3, 3, 6, 6, 9, 9, 12, 12, 15, 15, 19, 19, 23] and bad == 0,
     'the OEIS lists %d terms; mine differ in %d; the first fifteen are %s.' % (len(terms), bad, ', '.join(map(str, first15))))
# ---- 2, 3 ----
line(2, 'read', 0.85, 1.320 <= ap <= 1.345, 'mean a_prof at n = %d is %.5f (standard error %.5f, %d clouds).' % (big, ap, ape, len(B)))
line(3, 'guessed', 0.55, 1.3300 <= ap <= 1.3367, 'mean a_prof is %.5f; 4/3 is 1.33333; the difference is %.5f, or %.0f standard errors.' % (ap, 4 / 3 - ap, (4 / 3 - ap) / ape))
# ---- 4 ----
line(4, 'guessed', 0.6, abs(at / ap - 1) <= 0.005 and abs(az / ap - 1) <= 0.005,
     'a_tot %.5f (%.5f), a_size %.5f (%.5f), a_prof %.5f: they differ from a_prof by %.3f%% and %.3f%%.' % (at, ate, az, aze, ap, 100 * (at / ap - 1), 100 * (az / ap - 1)))
# ---- 5 ----
os.makedirs(P('runs', 'profiles'), exist_ok=True)
ps = []
for s in range(1, 21):
    f = P('runs', 'profiles', 'disc-1000000-%d.txt' % s)
    if not os.path.exists(f): subprocess.run([P('peel'), 'disc', '1000000', str(555000 + s), '-profile', f], capture_output=True, text=True)
    rows = [tuple(map(float, l.split())) for l in open(f)]
    rows = [(r, c, d) for r, c, d in rows if 0.3 <= r <= 0.9]
    def fit(p):          # weighted least squares of d against A (1 - r^p), no intercept: returns (sum of squares, A)
        u = [1 - r ** p for r, c, d in rows]
        A = sum(c * ui * d for ui, (r, c, d) in zip(u, rows)) / sum(c * ui * ui for ui, (r, c, d) in zip(u, rows))
        return sum(c * (d - A * ui) ** 2 for ui, (r, c, d) in zip(u, rows)), A
    lo, hi = 1.0, 1.8
    for _ in range(60):          # golden-section search for the best p
        m1, m2 = lo + 0.382 * (hi - lo), lo + 0.618 * (hi - lo)
        if fit(m1)[0] < fit(m2)[0]: hi = m2
        else: lo = m1
    ps.append((lo + hi) / 2)
line(5, 'read', 0.8, 1.31 <= mean(ps) <= 1.36, 'the best power, twenty clouds of a million points (depth averaged in rings of width 0.0016, fitted without an intercept): mean %.4f, from %.4f to %.4f.' % (mean(ps), min(ps), max(ps)))
# ---- 6 ----
M6 = sel('disc', 1000000); c1 = mean([r['first'] for r in M6]) / 100.0; c2 = mean([r['mean20to40'] for r in M6]) / 100.0
line(6, 'read', 0.7, 3.33 <= c1 <= 3.43 and 3.10 <= c2 <= 3.30, 'at a million points (%d clouds): layer 1 has %.4f times n^(1/3) points, layers 20 to 40 have %.4f.' % (len(M6), c1, c2))
# ---- 7 ----
a4 = stat(sel('disc', 10000), 'a_tot')
line(7, 'guessed', 0.55, abs(a4[0] / at - 1) <= 0.02, 'mean a_tot at ten thousand points is %.5f (%.5f); at the largest n %.5f: a difference of %.2f%%.' % (a4[0], a4[1], at, 100 * (a4[0] / at - 1)))
# ---- 8 ----
pts = []
for n in (10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7):
    rows = sel('disc', n); pts.append((math.log(n), math.log(sd([r['layers'] for r in rows])), len(rows)))
mx = mean([p[0] for p in pts]); my = mean([p[1] for p in pts])
beta = sum((p[0] - mx) * (p[1] - my) for p in pts) / sum((p[0] - mx) ** 2 for p in pts)
enough = all(p[2] >= 100 for p in pts[:3]) and pts[3][2] >= 30
line(8, 'guessed', 0.5, enough and 0.15 <= beta <= 0.30, 'the standard deviation of the count is %s layers at n = 10^4, 10^5, 10^6, 10^7 (%s clouds); as a power of n the exponent is %.3f (2/9 is 0.222).' % (
    ', '.join('%.2f' % math.exp(p[1]) for p in pts), ', '.join(str(p[2]) for p in pts), beta))
# ---- 9, 10, 11, 12 ----
D6, S6, T6 = sel('disc', 1000000), sel('square', 1000000), sel('triangle', 1000000)
nd, ns, nt = stat(D6, 'layers'), stat(S6, 'layers'), stat(T6, 'layers')
line(9, 'worked', 0.8, len(S6) >= 20 and len(T6) >= 20 and ns[0] > nd[0] and nt[0] > ns[0], 'at a million points: disc %.1f layers (%.1f), square %.1f (%.1f), triangle %.1f (%.1f); %d, %d and %d clouds.' % (nd + ns + nt + (len(D6), len(S6), len(T6))))
rs, rt = ns[0] / nd[0], nt[0] / nd[0]
line(10, 'guessed', 0.6, 1.02 <= rs <= 1.10, 'the square has %.2f%% more layers than the disc.' % (100 * (rs - 1)))
line(11, 'guessed', 0.5, 1.08 <= rt <= 1.30, 'the triangle has %.2f%% more layers than the disc.' % (100 * (rt - 1)))
h, q = stat(S6, 'ratio_half'), stat(S6, 'ratio_ninetenths')
line(12, 'guessed', 0.5, h[0] > 1.05 and q[0] < 1.05, 'square clouds of a million points: farthest over nearest point of the layer at half depth %.4f (%.4f), at nine tenths %.4f (%.4f).' % (h + q))
# ---- 13 ----
tried = same = 0
for shape in ('disc', 'square', 'triangle'):
    for n, s in ((2000, 1), (20000, 2), (200000, 3)):
        a = subprocess.run([P('peel-wide'), shape, str(n), str(s), '-plain', '-depths', '-'], capture_output=True, text=True).stdout.split('\n')
        b = subprocess.run([P('peel-wide'), shape, str(n), str(s), '-plain', '-affine', '-depths', '-'], capture_output=True, text=True).stdout.split('\n')
        da = [l.split()[2] for l in a if len(l.split()) == 3]; db = [l.split()[2] for l in b if len(l.split()) == 3]
        moved = sum(1 for la, lb in zip(a, b) if len(la.split()) == 3 and la.split()[0] != lb.split()[0])
        tried += 1; same += (len(da) == n and da == db and moved > n * 0.9)
line(13, 'read', 0.97, tried == 9 and same == 9, 'nine clouds (three shapes; 2,000, 20,000 and 200,000 points), each peeled as it is and again after (x, y) -> (3x + y, y): every point has the same depth in %d of %d.' % (same, tried))
held = sum(1 for v in verdicts if v[3]); brier = sum((v[2] - (1 if v[3] else 0)) ** 2 for v in verdicts) / len(verdicts)
print('HELD %d of %d. Brier score %.3f.' % (held, len(verdicts), brier))
for k in ('read', 'worked', 'guessed'):
    v = [x for x in verdicts if x[1] == k]
    print('  %s: %d of %d held (lines %s; * failed)' % (k, sum(1 for x in v if x[3]), len(v), ', '.join(str(x[0]) + ('' if x[3] else '*') for x in v)))
