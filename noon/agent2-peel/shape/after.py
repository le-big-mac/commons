"""after.py: what was looked at after the sealed lines were scored. Nothing here was sealed.   python -I after.py
A  every file: the mean against alpha rho^(2/3) T, and how far off in parts of 10,000
B  w n = variance x n / mean^2 for every shape, with the theory's figure for that shape and the ceiling 0.3754 / 0.8199
C  the rounded triangle against the triangle, at both sizes and together
D  one D for every shape? the D that each file gives IF the theory's I and T are right (so no test of the theory by itself)
E  left to chance less exactly n: it must be (4/9) m^2 / n whatever D is
F  30,000 against 100,000: the variance must grow as n^(1/3)
G  is the count normally spread? skewness and excess kurtosis
H  the clouds peeled both ways
I  the lines "over the disc's" with the other discs, and with both sets of discs, in the disc's place; and how near each verdict sat to its band's end
J  a test of another sort: among clouds whose number is left to chance, the count against the number of points (the slope must be
   (2/3) m / n, and what is left over must have the variance of clouds of exactly n)
K  more discs, quarter discs and half discs, peeled after the scoring because two sets stood furthest from their lines (runs-after/; fresh.py)
L  after the referee: clouds from two other generators of points, and every lawful pooling of measured over theory at 100,000 points
Errors are by resampling whole clouds (study.boot)."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study, theory
F = {k: v for k, v in study.F.items() if v is not None}
def shape_of(name): s = name.split('-')[1]; return 'disc' if s == 'disc0' else s
def bs(fn, *names):
    args = []; b = []
    for n in names: args += [F[n]['m'], F[n]['v']]; bb = study.boot(n); b += [bb[0], bb[1]]
    return float(fn(*args)), float(np.std(fn(*b), ddof=1))
print('A  the means')
print('   file                        mean (se)            alpha rho^(2/3) T    off by, in 10,000 (se)')
for name, f in F.items():
    p = theory.predictions(shape_of(name), f['n0'])['mean']; bm = study.boot(name)[0]
    print('   %-26s %9.3f (%.3f)    %9.3f            %+.2f (%.2f)' % (name, f['m'], bm.std(ddof=1), p, (f['m'] / p - 1) * 1e4, bm.std(ddof=1) / p * 1e4))
print()
print('B  w n = variance x n / mean^2')
print('   file                        w n (se)            theory for the shape   the ceiling   measured over theory (se)')
pool = {'exact': [], 'chance': []}
for name, f in F.items():
    kind = name.split('-')[0]; sh = shape_of(name); p = theory.predictions(sh, f['n0']); key = 'chance' if kind == 'chance' else 'exact'; th = p[key] / p['mean'] ** 2 * f['n0']
    ceil = (4 / 3 * theory.D - (theory.DC if kind == 'exact' else 0)) / theory.ALPHA ** 2; val, se = bs(lambda m, v: v / m ** 2 * f['n0'], name)
    print('   %-26s %.4f (%.4f)     %.4f                 %.4f        %.4f (%.4f)' % (name, val, se, th, ceil, val / th, se / th))
    if sh not in ('rtriangle', 'halfdisc', 'quarter') and f['n0'] == 100000: pool[kind].append((val, se, th))
for kind in ('exact', 'chance'):
    if pool[kind]:
        w = np.array([1 / s ** 2 for v, s, t in pool[kind]]); vals = np.array([v for v, s, t in pool[kind]]); mean = float((w * vals).sum() / w.sum()); chi = float((w * (vals - mean) ** 2).sum())
        print('   the shapes at the ceiling (%s, 100,000; %d files) together: %.4f (%.4f); theory %.4f; do they agree with one another? chi-square %.1f on %d' % (kind, len(vals), mean, 1 / math.sqrt(w.sum()), pool[kind][0][2], chi, len(vals) - 1))
print()
print('C  the rounded triangle against the triangle: w over w (theory 0.9547; if the variance went as the square of the mean, 1)')
wr = lambda m1, v1, m2, v2: (v1 / m1 ** 2) / (v2 / m2 ** 2); got = []
for n0 in (100000, 30000):
    a, b = 'exact-rtriangle-%d' % n0, 'exact-triangle-%d' % n0
    if a in F and b in F: val, se = bs(wr, a, b); got.append((val, se)); print('   %7d points: %.4f (%.4f); %.1f errors from 0.9547, %.1f from 1' % (n0, val, se, (val - 0.9547) / se, (val - 1) / se))
if len(got) == 2:
    w = [1 / s ** 2 for v, s in got]; mean = (w[0] * got[0][0] + w[1] * got[1][0]) / (w[0] + w[1]); se = 1 / math.sqrt(w[0] + w[1])
    print('   both sizes together: %.4f (%.4f); %.1f errors from 0.9547, %.1f from 1; the two sizes differ by %.1f of their errors' % (mean, se, (mean - 0.9547) / se, (mean - 1) / se, (got[0][0] - got[1][0]) / math.hypot(got[0][1], got[1][1])))
    for n0 in (100000, 30000):
        a, b, d = 'exact-rtriangle-%d' % n0, 'exact-triangle-%d' % n0, 'exact-disc-%d' % n0
        if d in F: print('   %7d points, each against the disc of that size: w of the triangle over the disc\'s %.4f (%.4f), theory 1; of the rounded triangle %.4f (%.4f), theory 0.9547' % ((n0,) + bs(wr, b, d) + bs(wr, a, d)))
print('   the rounded triangle at 100,000 against each of the other shapes that the theory puts at the ceiling, the unkindest (nearest 1) first; theory 0.9547 for each')
rows = []
for sh in ('disc', 'disc0', 'ellipse', 'triangle', 'square', 'hexagon'):
    b = 'exact-%s-100000' % sh
    if 'exact-rtriangle-100000' in F and b in F: val, se = bs(wr, 'exact-rtriangle-100000', b); rows.append((val, se, sh))
for val, se, sh in sorted(rows, reverse=True): print('      against the %-9s %.4f (%.4f); %.1f errors below 1' % (sh, val, se, (1 - val) / se))
if rows and pool['exact']:
    w = np.array([1 / s_ ** 2 for v, s_, t in pool['exact']]); vals = np.array([v for v, s_, t in pool['exact']]); pm = float((w * vals).sum() / w.sum()); pse = 1 / math.sqrt(w.sum()); rv, rse = bs(lambda m, v: v / m ** 2 * 1e5, 'exact-rtriangle-100000')
    print('      against the six together (%.4f, error %.4f): %.4f (%.4f); %.1f errors below 1' % (pm, pse, rv / pm, rv / pm * math.hypot(rse / rv, pse / pm), (1 - rv / pm) / (rv / pm * math.hypot(rse / rv, pse / pm))))
print()
print('D  the D each file gives, the theory\'s T and I taken as right (the level problem gave 1.081)')
for name, f in F.items():
    kind = name.split('-')[0]; sh = shape_of(name); t = theory.TH[sh]; rho = f['n0'] / math.pi
    fn = (lambda m, v: (v / rho ** (1 / 3.0) + (theory.DC * t['T'] ** 2 / math.pi if kind == 'exact' else 0)) / t['I']); val, se = bs(fn, name)
    print('   %-26s D = %.4f (%.4f)' % (name, val, se))
print()
print('E  the variance left to chance less the variance with exactly n, against (4/9) m^2 / n (which needs no D)')
for sh in ('disc', 'triangle', 'square'):
    a, b = 'chance-%s-100000' % sh, 'exact-%s-100000' % sh
    if a in F and b in F:
        val, se = bs(lambda m1, v1, m2, v2: v1 - v2, a, b); th = 4 / 9.0 * F[b]['m'] ** 2 / 1e5
        print('   %-9s %.4f (%.4f)   (4/9) m^2/n = %.4f   ratio %.4f (%.4f)' % (sh, val, se, th, val / th, se / th))
print()
print('F  the variance at 100,000 over the variance at 30,000 (theory (10/3)^(1/3) = %.4f)' % (10 / 3.0) ** (1 / 3.0))
for sh in ('disc', 'triangle', 'rtriangle'):
    a, b = 'exact-%s-100000' % sh, 'exact-%s-30000' % sh
    if a in F and b in F: print('   %-9s %.4f (%.4f)' % ((sh,) + bs(lambda m1, v1, m2, v2: v1 / v2, a, b)))
print()
print('G  the spread\'s shape: skewness and excess kurtosis (errors as for a normal law: sqrt(6/K), sqrt(24/K))')
for name, f in F.items():
    z = (f['x'] - f['m']) / f['x'].std(); print('   %-26s %+.3f (%.3f)   %+.3f (%.3f)' % (name, (z ** 3).mean(), math.sqrt(6 / f['K']), (z ** 4).mean() - 3, math.sqrt(24 / f['K'])))
print()
print('H  clouds peeled both ways (every 200th): %d, of which the two ways agreed on every point\'s depth in %d' % (sum(f['both'] for f in F.values()), sum(f['agree'] for f in F.values())))

print()
print('I  the ratios "over the disc\'s" (exactly n, 100,000) with each set of discs below the line, and with both together (50,000 discs)')
if all(k in F for k in ('exact-disc-100000', 'exact-disc0-100000')):
    a, b = F['exact-disc-100000'], F['exact-disc0-100000']; both = np.concatenate([a['x'] - a['m'], b['x'] - b['m']]); vboth = float((both ** 2).sum() / (len(both) - 2)); print('   variance of the discs: cloud.c %.4f, peel\'s own %.4f, both (each about its own mean) %.4f; theory %.4f' % (a['v'], b['v'], vboth, theory.predictions('disc', 1e5)['exact']))
    print('   shape       over cloud.c\'s discs   over peel\'s own   over both      theory')
    for sh in ('triangle', 'square', 'hexagon', 'ellipse', 'halfdisc', 'quarter', 'rtriangle'):
        n = 'exact-%s-100000' % sh
        if n in F: v1, s1 = bs(lambda m1, v1, m2, v2: v1 / v2, n, 'exact-disc-100000'); v2, s2 = bs(lambda m1, v1, m2, v2: v1 / v2, n, 'exact-disc0-100000'); print('   %-10s  %.4f (%.4f)         %.4f (%.4f)   %.4f         %.4f' % (sh, v1, s1, v2, s2, F[n]['v'] / vboth, theory.predictions(sh, 1e5)['exact'] / theory.predictions('disc', 1e5)['exact']))
print('   how near each verdict sat to the nearer end of its band, in the figure\'s own errors (study.json)')
import json
sj = json.load(open(os.path.join(HERE, 'study.json'))); near = []
for tag, l in sj['lines'].items():
    for part in l.get('parts', []):
        if part['lo'] < -1e8: continue
        near.append((min(part['value'] - part['lo'], part['hi'] - part['value']) / part['se'], tag, part['part']))
print('   ' + '; '.join('%s %s %.1f' % (t, pt, d) for d, t, pt in sorted(near)[:8]))
print()
print('J  the count against the number of points, among clouds whose number is left to chance (100,000 on average)')
print('   shape      slope of the count on the number (se)    (2/3) m / n     what is left over: variance (se)   the variance of clouds of exactly n (se)')
for sh in ('disc', 'triangle', 'square'):
    c, e = 'chance-%s-100000' % sh, 'exact-%s-100000' % sh
    if c in F and e in F:
        x, y = F[c]['n'], F[c]['x']; K = len(x); rng = np.random.default_rng([7, K]); 
        def fit(ix): xx, yy = x[ix], y[ix]; b = np.cov(xx, yy)[0, 1] / xx.var(ddof=1); r = yy - yy.mean() - b * (xx - xx.mean()); return b, r.var(ddof=2)
        b0, r0 = fit(np.arange(K)); bb = np.array([fit(rng.integers(0, K, K)) for _ in range(400)])
        print('   %-9s  %.6f (%.6f)                      %.6f        %.4f (%.4f)                    %.4f (%.4f)' % (sh, b0, bb[:, 0].std(ddof=1), 2 / 3.0 * F[c]['m'] / 1e5, r0, bb[:, 1].std(ddof=1), F[e]['v'], study.boot(e)[1].std(ddof=1)))
print()
import fresh
ceil_ = (4 / 3 * theory.D - theory.DC) / theory.ALPHA ** 2; wn5 = lambda m_, v_: v_ / m_ ** 2 * 1e5
six_m, six_se, _ = fresh.pool([bs(wn5, 'exact-%s-100000' % sh_) for sh_ in ('disc', 'disc0', 'ellipse', 'triangle', 'square', 'hexagon')])
def show(key, first=None):
    r = fresh.reckon(key)
    if r is None: print('   %-16s not made' % key); return
    t = '   %-16s %6d clouds by %-7s variance %.4f (%.4f), theory %.4f; w n %.4f (%.4f); from its own line %.4f: %+.1f errors; from the ceiling %.4f: %+.1f' % (key, r['K'], r['maker'] + ':', r['v'], r['vse'], r['theory_v'], r['w'], r['wse'], r['line'], (r['w'] - r['line']) / r['wse'], ceil_, (r['w'] - ceil_) / r['wse'])
    if first: w0, w0se = bs(wn5, first); t += '; the sheet\'s %d clouds gave %.4f (%.4f), %.1f errors from these' % (F[first]['K'], w0, w0se, (w0 - r['w']) / math.hypot(r['wse'], w0se))
    print(t)
print('K  fresh clouds of exactly 100,000 points, made after the scoring and in no verdict (runs-after/): first 30,000 discs and 16,000 quarter discs (batchK.sh),')
print('   then, the quarter disc having stayed high, 60,000 more of them and 40,000 half discs (batchK2.sh); all by cloud.c, as the sheet\'s were')
for key, first in (('disc-cloud', 'exact-disc-100000'), ('quarter-cloud-a', 'exact-quarter-100000'), ('quarter-cloud-b', 'exact-quarter-100000'), ('quarter-cloud', 'exact-quarter-100000'), ('halfdisc-cloud', 'exact-halfdisc-100000')): show(key, first)
print()
print('L  after the referee: is the excess at 100,000 points the generator\'s, or the quarter disc\'s alone? Clouds from the first study\'s own generator (no cloud.c) and quarter discs from numpy\'s (batchL.sh)')
for key in ('disc-peel', 'square-peel', 'triangle-peel', 'quarter-numpy'): show(key)
def ratio_sheet(n): sh_ = shape_of(n); th = theory.predictions(sh_, F[n]['n0']); thw = th['exact'] / th['mean'] ** 2 * F[n]['n0']; w_, s_ = bs(lambda m_, v_: v_ / m_ ** 2 * F[n]['n0'], n); return (w_ / thw, s_ / thw)
def ratio_fresh(key): r = fresh.reckon(key); return (r['w'] / r['line'], r['wse'] / r['line'])
S5 = {n: ratio_sheet(n) for n in F if n.startswith('exact-') and n.endswith('-100000')}; S3 = {n: ratio_sheet(n) for n in F if n.endswith('-30000')}
FR = {k: ratio_fresh(k) for k in ('disc-cloud', 'quarter-cloud', 'halfdisc-cloud', 'disc-peel', 'square-peel', 'triangle-peel', 'quarter-numpy') if fresh.reckon(k) is not None}
def line(label, pairs):
    if not pairs: print('      %-86s none' % label); return
    m_, s_, chi = fresh.pool(pairs); print('      %-86s %2d sets  %.4f (%.4f)  %+.1f errors from 1; chi-square among them %.1f on %d' % (label, len(pairs), m_, s_, (m_ - 1) / s_, chi, len(pairs) - 1))
print('   measured w n over the shape\'s own line, sets of exactly n points weighted together (100,000 points unless said)')
line('the sheet\'s nine sets', list(S5.values()))
line('the sheet\'s nine and the three fresh sets by cloud.c (as before the referee)', list(S5.values()) + [FR[k] for k in ('disc-cloud', 'quarter-cloud', 'halfdisc-cloud') if k in FR])
line('every set at 100,000, the sheet\'s and all the fresh', list(S5.values()) + list(FR.values()))
line('the same without any quarter disc', [v for n, v in S5.items() if 'quarter' not in n] + [v for k, v in FR.items() if 'quarter' not in k])
line('the same without any quarter disc and without the sheet\'s disc set', [v for n, v in S5.items() if 'quarter' not in n and n != 'exact-disc-100000'] + [v for k, v in FR.items() if 'quarter' not in k])
line('quarter discs: the sheet\'s and the fresh by cloud.c', [S5['exact-quarter-100000']] + [FR[k] for k in ('quarter-cloud',) if k in FR])
line('quarter discs by numpy', [FR[k] for k in ('quarter-numpy',) if k in FR])
line('quarter discs, all', [S5['exact-quarter-100000']] + [FR[k] for k in ('quarter-cloud', 'quarter-numpy') if k in FR])
line('everything by cloud.c but the quarter discs', [v for n, v in S5.items() if 'quarter' not in n and 'disc0' not in n] + [FR[k] for k in ('disc-cloud', 'halfdisc-cloud') if k in FR])
line('everything by the first study\'s own generator (the sheet\'s disc0 and the three fresh sets)', [S5['exact-disc0-100000']] + [FR[k] for k in ('disc-peel', 'square-peel', 'triangle-peel') if k in FR])
line('the fresh sets only, none of them chosen for being high (discs, half discs, own discs, squares, triangles)', [FR[k] for k in ('disc-cloud', 'halfdisc-cloud', 'disc-peel', 'square-peel', 'triangle-peel') if k in FR])
line('30,000 points: the sheet\'s three sets', list(S3.values()))
