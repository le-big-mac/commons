"""dfigtest.py: disc.svg read back. Every dot's place is turned into a value through the plate's own tick labels and compared with
dfig.json and with study.out; every curve is compared with dtheory.py; every mark and every label is inside the picture.   python -I dfigtest.py"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dtheory as th
svg = open(os.path.join(HERE, 'disc.svg'), encoding='utf-8').read(); J = json.load(open(os.path.join(HERE, 'dfig.json'))); study = open(os.path.join(HERE, 'study.out')).read(); N = 10 ** 6
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail else ''))
def part(i): return re.search(r'<g id="%s">(.*?)</g>' % i, svg, re.S).group(1)
def axes(g):
    xt = [(float(v), float(x)) for v, x in re.findall(r'<text class="xtick" data-v="([^"]+)" x="([\d.]+)"', g)]; yt = [(float(v), float(y) - 4) for v, y in re.findall(r'<text class="ytick" data-v="([^"]+)" x="[\d.]+" y="([\d.]+)"', g)]
    assert all(abs(float(a) - float(b)) < 1e-9 for a, b in re.findall(r'<text class="[xy]tick" data-v="([^"]+)"[^>]*>([^<]+)</text>', g))            # the label shown is the value it stands at
    X = lambda px: xt[0][0] + (xt[-1][0] - xt[0][0]) * (px - xt[0][1]) / (xt[-1][1] - xt[0][1]); Y = lambda py: yt[0][0] + (yt[-1][0] - yt[0][0]) * (py - yt[0][1]) / (yt[-1][1] - yt[0][1]); return X, Y
def dots(g, cls, X, Y): return [(X(float(cx)), Y(float(cy))) for cx, cy in re.findall(r'<circle class="%s" cx="([\d.]+)" cy="([\d.]+)"' % cls, g)]
def line(g, cid, X, Y): return [(X(float(a)), Y(float(b))) for a, b in (q.split(',') for q in re.search(r'<polyline id="%s" points="([^"]+)"' % cid, g).group(1).split())]
def table(kind):          # the rows of study.out for a million points of this kind: radius, ring's mean variance, variance round the ring, and the four ratios of the parts
    blk = study[re.search(r'^%s, n = 1000000, \d+ clouds\.' % re.escape(kind), study, re.M).start():]; blk = blk[:blk.index('the count of layers')]
    return [(float(a), float(b), float(c)) for a, b, c in re.findall(r'^\s+(\d\.\d\d) \|\s+([\d.]+) \([\d.]+\)\s+[\d.]+\s+[\d.]+ \|\s+([\d.]+)', blk, re.M)]
L = part('left'); X, Y = axes(L); tc, te = table('number left to chance'), table('exactly n points')
for cls, key, tab, name in (('chance', 'chance', tc, 'number left to chance'), ('exact', 'exact', te, 'exactly a million')):
    d = dots(L, cls, X, Y)
    ok('left plate, %s: 19 dots, each read back through the tick labels to its radius and to the value in dfig.json, which is the table of study.out' % name,
       len(d) == 19 and all(abs(r - R) < 0.003 and abs(v - J[key][i]) < 0.03 for i, ((r, v), R) in enumerate(zip(d, J['radii']))) and all(abs(t[1] - J[key][i]) < 0.0006 and abs(t[0] - J['radii'][i]) < 1e-9 for i, t in enumerate(tab)), d[:3])
for cid, cov, name in (('pred-chance', th.cov_chance, 'left to chance'), ('pred-exact', th.cov_fixed, 'exactly n')):
    c = line(L, cid, X, Y); ok('   the predicted curve drawn for %s is dtheory\'s at each of its %d points' % (name, len(c)), len(c) > 150 and all(abs(v - (th.annulus(cov, r, r, N) if 0.012 < r < 0.988 else cov(r, r, N))) < 0.05 for r, v in c))
Mi = part('middle'); X, Y = axes(Mi); d = dots(Mi, 'round', X, Y)
ok('middle plate: 19 dots read back to the variance round the ring of dfig.json and of study.out', len(d) == 19 and all(abs(v - J['round'][i]) < 0.1 for i, (r, v) in enumerate(d)) and all(abs(t[2] - J['round'][i]) < 0.006 for i, t in enumerate(te)))
c = line(Mi, 'pred-round', X, Y); lv = line(Mi, 'level', X, Y)
ok('   its predicted curve is dtheory\'s sum of the parts, and the dashed one 0.65 x sqrt(0.75 x 1.3259 x (n/pi)^(2/3) x (1 - r^(4/3)))', all(abs(v - th.local(r, N, mmax=400)) < 0.15 for r, v in c) and all(abs(v - 0.65 * math.sqrt(0.75 * 1.3259 * (N / math.pi) ** (2 / 3.0) * (1 - max(r, 0) ** (4 / 3.0)))) < 0.2 for r, v in lv))
R_ = part('right'); X, Y = axes(R_); good = True
for m in (1, 2, 3):
    d = dots(R_, 'part%d' % m, X, Y); c = line(R_, 'pred-part%d' % m, X, Y)
    good = good and len(d) == 19 and all(abs(v - J['parts'][str(m)][i]) < 0.02 for i, (r, v) in enumerate(d)) and all(abs(v - th.mode(m, r, N)) < (0.02 if r > 0.03 else 0.06) for r, v in c)        # close to the centre the first part's curve is steep, and a tenth of a pixel across is more
ok('right plate: three sets of 19 dots read back to dfig.json, and three curves that are dtheory\'s parts', good)
far = max(abs(J['round'][i] / th.local(J['radii'][i], N) - 1) for i in range(19)); farp = max(abs(J['parts'][str(m)][i] / th.mode(m, J['radii'][i], N) - 1) for m in (1, 2) for i in range(1, 17))
ok('what the plates show: round the ring every dot is within %.1f in 100 of its curve; the first and second parts within %.0f in 100 from 0.10 to 0.85' % (100 * far, 100 * farp), far < 0.04 and farp < 0.06)
W_, H_ = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', svg).groups()); xs = [float(v) for v in re.findall(r'\bc?x[12]?="([\d.]+)"', svg)]; ys = [float(v) for v in re.findall(r'\bc?y[12]?="([\d.]+)"', svg)]
pl = [tuple(map(float, q.split(','))) for m in re.findall(r'points="([^"]+)"', svg) for q in m.split()]
ok('every mark is inside the picture (%d by %d), and every dot and curve inside its plate' % (W_, H_), all(0 <= v <= W_ for v in xs) and all(0 <= v <= H_ for v in ys) and all(0 <= a <= W_ and 120 <= b <= 390 for a, b in pl) and all(120 <= float(cy) <= 390 for cy in re.findall(r'<circle class="(?:chance|exact|round|part\d)" cx="[\d.]+" cy="([\d.]+)"', svg)))
ok('no words in a series colour; the colours used are those that were validated', not re.search(r'<text[^>]*fill="#(2a78d6|eb6834|86b6ef|0d366b)"', svg) and all(c in svg for c in ('#2a78d6', '#eb6834', '#86b6ef', '#0d366b')))
print('\n%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
