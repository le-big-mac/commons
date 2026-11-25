"""after.py: what was looked at after the sealed lines were judged. None of this was sealed.   python -I after.py > after.out
Reads runs/discs-small.jsonl, runs/large.jsonl, runs/polygons.jsonl, runs/cell/cell.jsonl and runs/cell/profile-*.txt,
runs/grid/*.json (made by gridruns.sh)."""
import json, math, os, glob, random
HERE = os.path.dirname(os.path.abspath(__file__)); P = lambda *a: os.path.join(HERE, *a)
def load(*name): return [json.loads(l) for l in open(P('runs', *name)) if l.strip()]
R = load('discs-small.jsonl') + load('large.jsonl') + load('polygons.jsonl')
def sel(shape, n): return [r for r in R if r['shape'] == shape and r['n'] == n]
def mean(v): return sum(v) / len(v)
def sd(v): m = mean(v); return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))
def se(v): return sd(v) / math.sqrt(len(v))
sizes = sorted(set(r['n'] for r in R if r['shape'] == 'disc'))

# ---------- A. the constant ----------
print('A. The constant from the discs: every cloud of a million points or more, the three estimates')
for key in ('a_tot', 'a_prof', 'a_size'):
    num = den = 0; parts = []
    for n in sizes:
        if n < 10 ** 6: continue
        v = [r[key] for r in sel('disc', n)]; w = 1 / se(v) ** 2; num += w * mean(v); den += w; parts.append('%.5f' % mean(v))
    print('   %-7s by size: %s; weighted mean %.5f, standard error %.5f; 4/3 is %.0f standard errors above' % (key, ', '.join(parts), num / den, 1 / math.sqrt(den), (4 / 3 - num / den) * math.sqrt(den)))
print('   the three estimates rest on the same clouds, so they are not three witnesses; the cell problem (B) is another')
print('   are the sizes alike? a_tot at 10^6, 3x10^6, 10^7, 3x10^7, 10^8 against their weighted mean: chi-square %.1f on 4 degrees of freedom' % (
    (lambda ms: sum(((m - sum(m2 / s2 ** 2 for m2, s2 in ms) / sum(1 / s2 ** 2 for m2, s2 in ms)) / s) ** 2 for m, s in ms))([(mean([r['a_tot'] for r in sel('disc', n)]), se([r['a_tot'] for r in sel('disc', n)])) for n in sizes if n >= 10 ** 6])))
print('   small clouds: a_tot falls to the limit, a_prof and a_size rise to it:')
for n in sizes:
    rows = sel('disc', n)
    print('      n = %9d: a_tot %.5f  a_prof %.5f  a_size %.5f   (layers %.2f against 0.9945 (n/pi)^(2/3) = %.2f)' % (n, mean([r['a_tot'] for r in rows]), mean([r['a_prof'] for r in rows]), mean([r['a_size'] for r in rows]),
          mean([r['layers'] for r in rows]), 0.75 * 1.326 * (n / math.pi) ** (2 / 3)))

# ---------- B. the cell problem ----------
print('\nB. The cell problem (points above a flat floor, peeled by parabolas): the slope of depth against height')
C = load('cell', 'cell.jsonl'); num = den = 0
for HM in sorted(set(c['HM'] for c in C)):
    v = [c['alpha_02'] for c in C if c['HM'] == HM]; v5 = [c['alpha_05'] for c in C if c['HM'] == HM]
    print('   height %5d: %d windows of %.1f million measured points; slope over 0.2 to 1 of the height %.5f (%.5f); over 0.5 to 1: %.5f (%.5f)' % (HM, len(v), mean([c['measured'] for c in C if c['HM'] == HM]) / 1e6, mean(v), se(v), mean(v5), se(v5)))
    if HM >= 500: w = 1 / se(v) ** 2; num += w * mean(v); den += w
print('   heights 500 and up, weighted: %.5f, standard error %.5f; 4/3 is %.0f standard errors above' % (num / den, 1 / math.sqrt(den), (4 / 3 - num / den) * math.sqrt(den)))

# ---------- C. how much the count varies ----------
print('\nC. The spread of the count of layers across clouds')
pts = [(n, sd([r['layers'] for r in sel('disc', n)]), len(sel('disc', n))) for n in sizes]
print('   n, standard deviation of the count, clouds: ' + '; '.join('%.0e: %.2f (%d)' % p for p in pts))
def slope(pp): mx = mean([math.log(p[0]) for p in pp]); my = mean([math.log(p[1]) for p in pp]); return sum((math.log(p[0]) - mx) * (math.log(p[1]) - my) for p in pp) / sum((math.log(p[0]) - mx) ** 2 for p in pp)
rng = random.Random(1)
def boot(ns):
    out = []
    for _ in range(400):
        pp = []
        for n in ns:
            v = [r['layers'] for r in sel('disc', n)]; b = [rng.choice(v) for _ in v]; pp.append((n, sd(b)))
        out.append(slope(pp))
    out.sort(); return out[10], out[389]
for label, ns in (('all nine sizes', sizes), ('the four sealed sizes, 10^4 to 10^7', [10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7]), ('10^6 and up', [n for n in sizes if n >= 10 ** 6])):
    lo, hi = boot(ns)
    print('   as a power of n, %s: exponent %.3f (95%% of resamplings between %.3f and %.3f); 1/6 is 0.167 and 2/9 is 0.222' % (label, slope([p for p in pts if p[0] in ns]), lo, hi))
print('   in the cell problem: the variance of depth among points at one height (taking off what the thickness of the band adds), as a power of the height')
for HM in sorted(set(c['HM'] for c in C)):
    acc = {}
    for f in glob.glob(P('runs', 'cell', 'profile-%d-*.txt' % int(HM * 1.25))):
        for l in open(f):
            y, c, mu, var = map(float, l.split()); b = round(y / (HM / 400.0) - 0.5); a = acc.setdefault(b, [0, 0, 0]); a[0] += c; a[1] += c * y; a[2] += c * var
    delta = HM / 400.0; pp = []
    for b in sorted(acc):
        c, sy, sv = acc[b]; y = sy / c; v = sv / c - (1.326 * delta) ** 2 / 12
        if 0.2 * HM <= y <= HM and v > 0: pp.append((y, v))
    e = slope(pp)
    print('   height %5d: variance at 0.2, 0.5 and 1 of the height: %s; exponent of the variance %.3f, so of the standard deviation %.3f' % (HM, ', '.join('%.2f' % min(pp, key=lambda q: abs(q[0] - f * HM))[1] for f in (0.2, 0.5, 1.0)), e, e / 2))

# ---------- D. the sizes of layers ----------
print('\nD. Points on the first layer and on layers 20 to 40, as multiples of the cube root of n (Renyi and Sulanke: 3.3832 for the first; the formula with 1.326: 3.2353)')
for n in sizes:
    rows = sel('disc', n); c = n ** (1 / 3)
    print('   n = %9d: first %.4f (%.4f)   layers 20 to 40: %.4f' % (n, mean([r['first'] for r in rows]) / c, se([r['first'] for r in rows]) / c, mean([r['mean20to40'] for r in rows]) / c))
print('   2 pi^(2/3) / 1.326 = %.4f; 2 pi^(2/3) / (4/3) = %.4f; Gamma(5/3) (2/3)^(1/3) pi^(-1/3) 2 pi = %.4f' % (2 * math.pi ** (2 / 3) / 1.326, 2 * math.pi ** (2 / 3) / (4 / 3), math.gamma(5 / 3) * (2 / 3) ** (1 / 3) * math.pi ** (-1 / 3) * 2 * math.pi))

# ---------- E. shapes ----------
print('\nE. Squares and triangles of the disc\'s area against discs holding as many points (layers; ratio to the disc)')
for n in (10 ** 5, 10 ** 6, 10 ** 7):
    d = [r['layers'] for r in sel('disc', n)]
    for shape in ('square', 'triangle'):
        v = [r['layers'] for r in sel(shape, n)]
        if v: print('   n = %8d  %-8s %2d clouds: %.1f layers (%.1f); disc %.1f; ratio %.4f (%.4f)' % (n, shape, len(v), mean(v), se(v), mean(d), mean(v) / mean(d), math.sqrt((se(v) / mean(v)) ** 2 + (se(d) / mean(d)) ** 2) * mean(v) / mean(d)))
for n in (10 ** 5, 10 ** 6, 10 ** 7):
    v = sel('square', n)
    if v: print('   square, n = %8d: farthest over nearest point of the layer at half depth %.4f, at nine tenths %.4f' % (n, mean([r['ratio_half'] for r in v]), mean([r['ratio_ninetenths'] for r in v])))
    v = sel('disc', n)
    print('   disc,   n = %8d: the same ratios %.4f and %.4f (a layer is never a perfect circle: this is the floor)' % (n, mean([r['ratio_half'] for r in v]), mean([r['ratio_ninetenths'] for r in v])))

# ---------- F. the grid: a constant that is proved ----------
print('\nF. Grid points, vertices only. Rote, Rueber and Saghafian (2024) proved the grid\'s constant, (pi^2 / (2 zeta(3)))^(1/3) = 1.60121, for parabolas')
cg = (math.pi ** 2 / (2 * 1.2020569031595942)) ** (1 / 3)
G = [json.loads(open(f).read()) for f in sorted(glob.glob(P('runs', 'grid', '*.json'))) if os.path.getsize(f) > 0]
for g in sorted(G, key=lambda g: (g['kind'], g['size'])):
    if g['kind'] == 'disc':
        print('   grid points in a disc of radius %4d (%d points): %d layers; divided by (3/4) radius^(4/3): %.4f (the grid constant, if the flow holds for a disc: %.4f)' % (g['size'], g['n'], g['layers'], g['layers'] / (0.75 * g['size'] ** (4 / 3)), cg))
    else:
        T = g['layers'] / (cg * g['size'] ** (4 / 3))
        print('   the %4d x %4d grid: %d layers; divided by the constant and side^(4/3): %.4f; over the same for a disc of area 1, %.4f: %.4f' % (g['size'], g['size'], g['layers'], T, 0.75 * math.pi ** (-2 / 3), T / (0.75 * math.pi ** (-2 / 3))))
print('   (the last column should tend to what random points give for a square against a disc, in E, if both follow the same flow)')

# ---------- G. choices of mine, varied (made while going through my list of questions) ----------
print('\nG. Choices of mine, varied')
prof = [[tuple(map(float, l.split())) for l in open(f)] for f in sorted(glob.glob(P('runs', 'profiles', 'disc-1000000-*.txt')))]
K6 = (1e6 / math.pi) ** (2 / 3)
def slope_over(rows, lo, hi):
    rows = [(1 - r ** (4 / 3), c, d) for r, c, d in rows if lo <= r <= hi]; W = sum(c for u, c, d in rows); mu = sum(c * u for u, c, d in rows) / W; md = sum(c * d for u, c, d in rows) / W
    return sum(c * (u - mu) * (d - md) for u, c, d in rows) / sum(c * (u - mu) ** 2 for u, c, d in rows)
print('   the slope estimate at a million points (%d clouds, depth averaged in rings) over other stretches of radius:' % len(prof))
for lo, hi in ((0.3, 0.9), (0.1, 0.5), (0.5, 0.9), (0.05, 0.95), (0.6, 0.98), (0.0, 0.3)):
    v = [4 / 3 * slope_over(rows, lo, hi) / K6 for rows in prof]
    print('      radius %.2f to %.2f: %.5f (%.5f)' % (lo, hi, mean(v), se(v)))
M = load('extra', 'cell-margins.jsonl')
print('   the cell problem at height 500 with the margin left out at each side halved and doubled (four windows each; the batch used 20 widths of the parabola):')
for mg in sorted(set(round(c['margin']) for c in M)):
    v = [c['alpha_02'] for c in M if round(c['margin']) == mg]; print('      margin %4d: %.5f (%.5f)' % (mg, mean(v), se(v)))
v = [c['alpha_02'] for c in C if c['HM'] == 500]; print('      margin %4d: %.5f (%.5f)   (the batch, eight windows)' % (round([c['margin'] for c in C if c['HM'] == 500][0]), mean(v), se(v)))
Z = [int(l) for l in open(P('runs', 'extra', 'sizes-1e7.txt'))]; N = len(Z); n = sum(Z)
print('   the sizes of layers against the formula c sqrt(1 - k/N) with c = 2 pi^(2/3) n^(1/3) / 1.326, one cloud of %d points, %d layers: mean of size / formula in ten bands of depth' % (n, N))
c0 = 2 * math.pi ** (2 / 3) * n ** (1 / 3) / 1.326
print('      ' + ', '.join('%.4f' % mean([Z[k - 1] / (c0 * math.sqrt(1 - (k - 0.5) / N)) for k in range(1 + int(b * N / 10), 1 + int((b + 1) * N / 10))]) for b in range(10)))
print('      the first five layers: ' + ', '.join(str(z) for z in Z[:5]) + '; the formula gives %.1f; the last five: ' % c0 + ', '.join(str(z) for z in Z[-5:]))
print('   the rule in peel.c that stops the sector method when 0 is no longer inside the inner hull: a copy without it gave the same depths on nine clouds (three shapes; 30,000, 30,000 and 300,000 points), so it never decided anything there')
print('   another generator and another grid: the page\'s core (mulberry32, coordinates to 2^21) on discs of 10,000 points gives ' + [l for l in open(P('pagefacts.out')) if l.startswith('disc 10000')][0].split(':')[1].split(';')[0].strip() + '; peel.c (xoshiro256**, 2^29) gives mean %.2f (%.2f)' % (mean([r['layers'] for r in sel('disc', 10 ** 4)]), se([r['layers'] for r in sel('disc', 10 ** 4)])))

# ---------- H. after the referee's report: its points recomputed here ----------
print('\nH. After the referee')
def pool(rows, key):
    num = den = 0
    for HM in sorted(set(c['HM'] for c in rows)):
        v = [c[key] for c in rows if c['HM'] == HM]; w = 1 / se(v) ** 2; num += w * mean(v); den += w
    return num / den, 1 / math.sqrt(den)
print('   the cell problem pooled four ways (weighted by the scatter at each height):')
for label, rows, key in (('slope over 0.2 to 1 of the height, heights 500 and up (26 windows; what I first quoted)', [c for c in C if c['HM'] >= 500], 'alpha_02'),
                         ('slope over 0.2 to 1 of the height, all 34 windows', C, 'alpha_02'),
                         ('slope over 0.5 to 1 of the height, heights 500 and up', [c for c in C if c['HM'] >= 500], 'alpha_05'),
                         ('slope over 0.5 to 1 of the height, all 34 windows', C, 'alpha_05')):
    print('      %s: %.5f (%.5f)' % ((label,) + pool(rows, key)))
allc = [c['alpha_02'] for c in C] + [c['alpha_05'] for c in C]
print('      the windows of height 200 alone: %.5f (%.5f); every pooled figure lies between %.4f and %.4f' % (mean([c['alpha_02'] for c in C if c['HM'] == 200]), se([c['alpha_02'] for c in C if c['HM'] == 200]),
      min(pool(r, k)[0] for r, k in ((C, 'alpha_02'), (C, 'alpha_05'), ([c for c in C if c['HM'] >= 500], 'alpha_02'), ([c for c in C if c['HM'] >= 500], 'alpha_05'))),
      max(pool(r, k)[0] for r, k in ((C, 'alpha_02'), (C, 'alpha_05'), ([c for c in C if c['HM'] >= 500], 'alpha_02'), ([c for c in C if c['HM'] >= 500], 'alpha_05')))))
print('   do the sizes from a million up agree with each other? chi-square on 4 degrees of freedom: ' + ', '.join('%s %.1f' % (key, (lambda ms: sum(((m - sum(m2 / s2 ** 2 for m2, s2 in ms) / sum(1 / s2 ** 2 for m2, s2 in ms)) / s) ** 2 for m, s in ms))(
      [(mean([r[key] for r in sel('disc', n)]), se([r[key] for r in sel('disc', n)])) for n in sizes if n >= 10 ** 6])) for key in ('a_tot', 'a_prof', 'a_size')))
print('   a_size is tied to a_tot: the sizes of the layers add up to n, so if they follow c sqrt(1 - k/N) then c = 3n/(2N) and the two estimates are one. At 10^8: a_tot %.5f, a_size %.5f' % (mean([r['a_tot'] for r in sel('disc', 10 ** 8)]), mean([r['a_size'] for r in sel('disc', 10 ** 8)])))
# the spread, fitted with weights
P9 = [(n, sd([r['layers'] for r in sel('disc', n)]), len(sel('disc', n))) for n in sizes]
def wfit(pp, fixed=None):
    xs = [math.log(n) for n, s, k in pp]; ys = [math.log(s) for n, s, k in pp]; ws = [2.0 * (k - 1) for n, s, k in pp]        # the error of log sd is 1/sqrt(2(k-1))
    W = sum(ws); mx = sum(w * x for w, x in zip(ws, xs)) / W; my = sum(w * y for w, y in zip(ws, ys)) / W
    if fixed is None:
        b = sum(w * (x - mx) * (y - my) for w, x, y in zip(ws, xs, ys)) / sum(w * (x - mx) ** 2 for w, x in zip(ws, xs)); eb = 1 / math.sqrt(sum(w * (x - mx) ** 2 for w, x in zip(ws, xs)))
    else: b = fixed; eb = 0
    chi = sum(w * (y - my - b * (x - mx)) ** 2 for w, x, y in zip(ws, xs, ys))
    return b, eb, chi
b, eb, chi = wfit(P9)
print('   the spread of the count, fitted with each size weighted by its number of clouds: exponent %.3f (%.3f), chi-square %.1f on 7' % (b, eb, chi))
print('      with the exponent fixed: 1/6 gives chi-square %.1f on 8; 1/5 gives %.1f; 2/9 gives %.1f' % (wfit(P9, 1 / 6)[2], wfit(P9, 1 / 5)[2], wfit(P9, 2 / 9)[2]))
b2, eb2, chi2 = wfit([p for p in P9 if p[0] >= 10 ** 6])
print('      from a million points up only: exponent %.2f (%.2f)' % (b2, eb2))
print('      variance of the count over n^(1/3): ' + ', '.join('%.3f' % (s * s / n ** (1 / 3)) for n, s, k in P9) + '   (10^4 to 10^8)')
NN = [(mean([r['layers'] for r in sel('disc', n)]), s * s) for n, s, k in P9]
print('      variance of the count over the square root of the count: ' + ', '.join('%.3f' % (v / math.sqrt(N)) for N, v in NN))
# the cell problem: variance of depth at a height, all heights pooled
allpp = []
for HM in sorted(set(c['HM'] for c in C)):
    acc = {}
    for f in glob.glob(P('runs', 'cell', 'profile-%d-*.txt' % int(HM * 1.25))):
        for l in open(f):
            y, c, mu, var = map(float, l.split()); bb = round(y / (HM / 400.0) - 0.5); a = acc.setdefault(bb, [0, 0, 0, 0]); a[0] += c; a[1] += c * y; a[2] += c * var; a[3] += c * mu
    delta = HM / 400.0
    for bb in sorted(acc):
        c, sy, sv, sm = acc[bb]; y = sy / c; v = sv / c - (1.326 * delta) ** 2 / 12
        if y >= 0.1 * HM and v > 0: allpp.append((y, v, sm / c))
def ex(lo, hi): pp = [(y, v) for y, v, d in allpp if lo <= y <= hi]; return slope(pp)
print('   the cell problem, all five window heights together: variance of depth at a height as a power of the height: exponent %.2f over heights 20 to 4000, %.2f over 1000 to 4000, %.2f over 20 to 1000' % (ex(20, 4000), ex(1000, 4000), ex(20, 1000)))
print('      variance of depth over the square root of the depth: %.2f at depth near 100, %.2f near 1000, %.2f near 4000' % tuple(min(allpp, key=lambda q: abs(q[2] - t))[1] / math.sqrt(min(allpp, key=lambda q: abs(q[2] - t))[2]) for t in (100, 1000, 4000)))
print('   Calder and Smart, Theorem 2.12, bound the fluctuation of the depth at height r in the cell problem by (log r)^3 r^(1/2); what I see, about r^(0.26), is inside that')
