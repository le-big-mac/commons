"""sfigtest.py: shape.svg read back. Every dot, bar and black mark is turned into a value through the plate's own tick labels and
compared with what study.py and theory.py give from the runs; the words of the title are checked against the numbers; and the
picture is drawn by a browser to see that every word is inside it and none lies on another.   python -I sfigtest.py"""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study, theory, fresh
svg = open(os.path.join(HERE, 'shape.svg'), encoding='utf-8').read(); J = json.load(open(os.path.join(HERE, 'sfig.json')))
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail else ''))
yt = [(float(v), float(y) - 4) for v, y in re.findall(r'<text class="ytick" data-v="([^"]+)" x="[\d.]+" y="([\d.]+)"', svg)]
ok('the seven tick labels show the values they stand at', len(yt) == 7 and all(abs(float(a) - float(b)) < 1e-9 for a, b in re.findall(r'<text class="ytick" data-v="([^"]+)"[^>]*>([^<]+)</text>', svg)))
Y = lambda py: yt[0][0] + (yt[-1][0] - yt[0][0]) * (py - yt[0][1]) / (yt[-1][1] - yt[0][1])
cols = re.findall(r'<g class="col" data-shape="(\w+)">(.*?)</g>', svg, re.S)
ok('nine columns, in the order disc, disc0, ellipse, triangle, square, hexagon, half disc, quarter disc, rounded triangle', [c[0] for c in cols] == ['disc', 'disc0', 'ellipse', 'triangle', 'square', 'hexagon', 'halfdisc', 'quarter', 'rtriangle'])
CEIL = (4 / 3.0 * theory.D - theory.DC) / theory.ALPHA ** 2
m = re.search(r'<line id="ceiling" x1="[\d.]+" y1="([\d.]+)"', svg); ok('the dashed line is at the ceiling, (4 D/3 - (4/9) alpha^2) / alpha^2 = %.4f, and its label says that figure and which D' % CEIL, m is not None and abs(Y(float(m.group(1))) - CEIL) < 1e-4 and 'dashed: the ceiling the equation gives with D = %.3f, %.4f' % (theory.D, CEIL) in svg)
FRESH = {'disc': ['disc-cloud'], 'disc0': ['disc-peel'], 'triangle': ['triangle-peel'], 'square': ['square-peel'], 'halfdisc': ['halfdisc-cloud'], 'quarter': ['quarter-cloud', 'quarter-numpy']}; nopen = 0
vals = {}
for sh, g in cols:
    th = theory.predictions('disc' if sh == 'disc0' else sh, 1e5); want_th = th['exact'] / th['mean'] ** 2 * 1e5
    t = re.search(r'<line class="theory" x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)"', g); xc = (float(t.group(1)) + float(t.group(3))) / 2
    ok('%s: the black mark is where theory.py puts the shape (%.4f)' % (sh, want_th), abs(Y(float(t.group(2))) - want_th) < 1e-4)
    for n0 in (100000, 30000):
        name = 'exact-%s-%d' % (sh, n0); d = re.search(r'<circle class="dot%d" cx="([\d.]+)" cy="([\d.]+)"' % n0, g); b = re.search(r'<line class="bar%d" x1="([\d.]+)" y1="([\d.]+)" x2="[\d.]+" y2="([\d.]+)"' % n0, g)
        have = study.F.get(name) is not None and study.complete(name)
        if not have: ok('%s: no dot at %d points, there being no such file' % (sh, n0), d is None and b is None); continue
        v, se = study.stat(lambda mm, vv: vv / mm ** 2 * n0, name); vals[(sh, n0)] = (v, se)
        ok('%s, %d points: the dot is at the variance x n / mean^2 of the runs (%.4f), its bar one standard error either way (%.4f), both in its own column' % (sh, n0, v, se),
           d is not None and b is not None and abs(Y(float(d.group(2))) - v) < 1e-4 and abs(Y(float(b.group(2))) - (v - se)) < 1.5e-4 and abs(Y(float(b.group(3))) - (v + se)) < 1.5e-4 and abs(float(d.group(1)) - xc) < 20 and abs(float(b.group(1)) - float(d.group(1))) < 0.01)
    made = [k for k in FRESH.get(sh, []) if fresh.reckon(k) is not None]; drawn = re.findall(r'<circle class="fdot" data-set="([\w-]+)" cx="([\d.]+)" cy="([\d.]+)" r="[\d.]+" fill="([^"]+)" stroke="([^"]+)"', g); bars = {k: (float(a), float(b), float(c_)) for k, a, b, c_ in re.findall(r'<line class="fbar" data-set="([\w-]+)" x1="([\d.]+)" y1="([\d.]+)" x2="[\d.]+" y2="([\d.]+)"', g)}
    ok('%s: an open dot for each fresh set of this shape that was made (%s), and no other' % (sh, ', '.join(made) or 'none'), [d_[0] for d_ in drawn] == made)
    for k, cx_, cy_, fill_, stroke_ in drawn:
        r = fresh.reckon(k); nopen += 1
        ok('%s, fresh set %s (%d clouds by %s): the open dot is at its variance x n / mean^2 (%.4f), with a bar one error either way (%.4f), open and blue, to the right of the filled dots of its column' % (sh, k, r['K'], r['maker'], r['w'], r['wse']),
           r['shape'] == ('disc' if sh == 'disc0' else sh) and abs(Y(float(cy_)) - r['w']) < 1e-4 and abs(Y(bars[k][1]) - (r['w'] - r['wse'])) < 1.5e-4 and abs(Y(bars[k][2]) - (r['w'] + r['wse'])) < 1.5e-4 and abs(bars[k][0] - float(cx_)) < 0.01 and fill_ == '#fcfcfb' and stroke_ == '#2a78d6' and 12 < float(cx_) - xc < 50)
    labels = re.findall(r'<text class="xlabel"[^>]*>([^<]+)</text>', g); pts = [tuple(float(v) for v in q.split()) for q in re.search(r'<path class="icon" d="M([^Z]+) Z"', g).group(1).split(' L')]
    ys = sorted(p_[1] for p_ in pts); xs_ = sorted(p_[0] for p_ in pts); top = [p_ for p_ in pts if p_[1] < ys[0] + 0.5]; bottom = [p_ for p_ in pts if p_[1] > ys[-1] - 0.5]
    want = {'disc': (['disc'], 60), 'disc0': (['disc, other', 'points'], 60), 'ellipse': (['ellipse'], 60), 'triangle': (['triangle'], 3), 'square': (['square'], 4), 'hexagon': (['hexagon'], 6), 'halfdisc': (['half disc'], 31), 'quarter': (['quarter disc'], 22), 'rtriangle': (['round-cornered', 'triangle'], 63)}[sh]
    Hh = ys[-1] - ys[0]; wide = lambda sel: (max(p_[0] for p_ in sel) - min(p_[0] for p_ in sel)) if sel else 0.0
    wt_, wb_ = wide([p_ for p_ in pts if p_[1] < ys[0] + 0.25 * Hh]), wide([p_ for p_ in pts if p_[1] > ys[-1] - 0.25 * Hh])          # how wide the outline is in its top quarter and in its bottom quarter (y runs downward)
    ends_low = all(any(abs(p_[0] - xe) < 0.15 and abs(p_[1] - ys[-1]) < 0.15 for p_ in pts) for xe in (xs_[0], xs_[-1]))                 # its leftmost and rightmost points are its lowest
    right_way = {'triangle': wt_ < 0.3 * wb_ and ends_low, 'rtriangle': wt_ < 0.5 * wb_ and (xs_[-1] - xs_[0]) > 1.05 * Hh, 'halfdisc': ends_low and wt_ < wb_, 'quarter': any(abs(p_[0] - xs_[0]) < 0.15 and abs(p_[1] - ys[-1]) < 0.15 for p_ in pts) and not any(abs(p_[0] - xs_[-1]) < 2 and abs(p_[1] - ys[0]) < 2 for p_ in pts),
                 'ellipse': (xs_[-1] - xs_[0]) > 2.5 * (ys[-1] - ys[0]), 'disc': abs((xs_[-1] - xs_[0]) - (ys[-1] - ys[0])) < 0.5, 'disc0': abs((xs_[-1] - xs_[0]) - (ys[-1] - ys[0])) < 0.5, 'square': abs((xs_[-1] - xs_[0]) - (ys[-1] - ys[0])) < 0.5, 'hexagon': (xs_[-1] - xs_[0]) > (ys[-1] - ys[0])}[sh]
    ok('%s: under the column, its own label (%s) and its own outline (%d corners, the right way up), centred on the column' % (sh, ' / '.join(want[0]), want[1]), labels == want[0] and len(pts) == want[1] and right_way and abs((xs_[0] + xs_[-1]) / 2 - xc) < 6, (labels, len(pts), right_way))
    for n0, colour in ((100000, '#2a78d6'), (30000, '#eb6834')):
        cc_ = re.search(r'<circle class="dot%d"[^>]*fill="([^"]+)"' % n0, g); bc_ = re.search(r'<line class="bar%d"[^>]*stroke="([^"]+)"' % n0, g)
        if cc_: ok('%s, %d points: the dot and its bar are in the colour the key gives that size' % (sh, n0), cc_.group(1) == colour and bc_.group(1) == colour)
keys = re.findall(r'<circle class="key"[^>]*fill="([^"]+)"(?: stroke="([^"]+)" stroke-width="2")?/>\s*<text[^>]*>([^<]+)</text>', svg)
ok('the key: blue for 100,000 points, orange for 30,000, an open blue ring for the fresh clouds, a black bar for the theory', sorted(keys) == sorted([('#2a78d6', '', '100,000 points'), ('#eb6834', '', '30,000 points'), ('#fcfcfb', '#2a78d6', 'fresh clouds of 100,000 points, peeled afterwards (in no verdict)')]) and 'where the theory puts the shape' in svg, keys)
ok('%d open dots in all, one for every fresh set that fresh.py knows and that was made, but the two halves of the quarter discs drawn as one' % nopen, nopen == sum(1 for k in fresh.SETS if k not in ('quarter-cloud-a', 'quarter-cloud-b') and fresh.reckon(k) is not None))
thv = {sh: theory.predictions('disc' if sh == 'disc0' else sh, 1e5) for sh, g in cols}; thw = {sh: p_['exact'] / p_['mean'] ** 2 * 1e5 for sh, p_ in thv.items()}
ok('the three groups named under the plate are what the theory says: the first six columns at the ceiling (five shapes), the next two within 1 in 100 below, the last the lowest', all(abs(thw[sh] - CEIL) < 5e-5 for sh in ('disc', 'disc0', 'ellipse', 'triangle', 'square', 'hexagon')) and all(0 < CEIL - thw[sh] < 0.01 * CEIL for sh in ('halfdisc', 'quarter')) and thw['rtriangle'] == min(thw.values())
   and all(t_ in svg for t_ in ('shapes the theory puts at the ceiling', 'a little below', 'furthest below')) and 'Five shapes at one ceiling' in svg and 'exactly n points' in svg and 'one standard error either way' in svg)
ok('dots at 30,000 points for the disc, the triangle and the rounded triangle only', sorted(sh for sh, n0 in vals if n0 == 30000) == ['disc', 'rtriangle', 'triangle'])
# the words of the title against the numbers
six = [vals[(sh, 100000)] for sh in ('disc', 'disc0', 'ellipse', 'triangle', 'square', 'hexagon')]; rt = vals[('rtriangle', 100000)]
ok('title, "five shapes at one ceiling": each of the six sets of clouds of those five shapes is within three of its own errors of the ceiling', all(abs(v - CEIL) < 3 * se for v, se in six), ', '.join('%+.1f' % ((v - CEIL) / se) for v, se in six))
ok('title, "the round-cornered triangle below it": more than four of its errors below the ceiling, and below each of the six', (CEIL - rt[0]) > 4 * rt[1] and all(rt[0] < v for v, se in six), '%.1f errors below' % ((CEIL - rt[0]) / rt[1]))
th = theory.predictions('rtriangle', 1e5); ok('title, "as worked out beforehand": within two of its errors of the theory\'s figure for it', abs(rt[0] - th['exact'] / th['mean'] ** 2 * 1e5) < 2 * rt[1])
ok('sfig.json holds the same numbers', all(abs(c[str(n0)][0] - vals[(c['shape'], n0)][0]) < 1e-12 for c in J['columns'] for n0 in (100000, 30000) if str(n0) in c) and sum(1 for c in J['columns'] for n0 in (100000, 30000) if str(n0) in c) == len(vals))
env = dict(os.environ, LD_LIBRARY_PATH=os.path.expanduser('~/web/sysroot/usr/lib/x86_64-linux-gnu'))
r = subprocess.run(['node', 'shot-svg.js', os.path.join(HERE, 'shape.svg'), '1000', '560', os.path.join(HERE, 'shape.png')], cwd=os.path.expanduser('~/web'), env=env, capture_output=True, text=True)
ok('drawn by a browser: no script errors, every line of words inside the picture, none lying on another', 'PICTURE: ok' in r.stdout and 'outside the picture: []' in r.stdout and 'overlapping: []' in r.stdout, r.stdout[-200:])
print('%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
