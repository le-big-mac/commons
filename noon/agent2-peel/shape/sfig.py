"""sfig.py: the plate of this part, shape.svg, and the numbers drawn on it, sfig.json.   python -I sfig.py
For each shape, clouds of exactly n points: the variance of the count of layers times n over the square of its mean, with one
standard error either way (by resampling clouds), at 100,000 points and, for three shapes, at 30,000; a short black bar where the
theory puts each shape; and the ceiling that the equation gives every convex shape, (4 D / 3 - (4/9) alpha^2) / alpha^2 with D = 1.081.
Open dots are the fresh clouds of 100,000 points peeled after the scoring (fresh.py): by the same generator as the column's filled dot,
or (the quarter disc's second open dot, the triangle's and the square's) by another."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study, theory, fresh
FRESH = {'disc': ['disc-cloud'], 'disc0': ['disc-peel'], 'triangle': ['triangle-peel'], 'square': ['square-peel'], 'halfdisc': ['halfdisc-cloud'], 'quarter': ['quarter-cloud', 'quarter-numpy']}
COLS = [('disc', 'disc', 0), ('disc0', 'disc, other', 0), ('ellipse', 'ellipse', 0), ('triangle', 'triangle', 0), ('square', 'square', 0), ('hexagon', 'hexagon', 0),
        ('halfdisc', 'half disc', 1), ('quarter', 'quarter disc', 1), ('rtriangle', 'round-cornered', 2)]
CEIL = (4 / 3.0 * theory.D - theory.DC) / theory.ALPHA ** 2
J = {'ceiling': CEIL, 'columns': []}
for sh, label, grp in COLS:
    p = theory.predictions('disc' if sh == 'disc0' else sh, 1e5); c = {'shape': sh, 'label': label, 'group': grp, 'theory': p['exact'] / p['mean'] ** 2 * 1e5}
    for n0 in (100000, 30000):
        name = 'exact-%s-%d' % (sh, n0)
        if study.F.get(name) is not None and study.complete(name): v, se = study.stat(lambda m, v: v / m ** 2 * n0, name); c[str(n0)] = [v, se, study.F[name]['K']]
    c['fresh'] = [[k, r['w'], r['wse'], r['K'], r['maker']] for k in FRESH.get(sh, []) for r in [fresh.reckon(k)] if r is not None]
    J['columns'].append(c)
json.dump(J, open(os.path.join(HERE, 'sfig.json'), 'w'), indent=1)
SURF, INK, INK2, MUTED, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9'; BLUE, ORANGE = '#2a78d6', '#eb6834'
WID, HGT = 1000, 560; X0, X1, YB, YT = 78, 962, 400, 128; VLO, VHI = 0.340, 0.400; out = []
fy = lambda v: YB + (YT - YB) * (v - VLO) / (VHI - VLO)
def T(x, y, s, size=12, fill=INK2, anchor='start', weight='normal', cls=None): out.append('<text%s x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s" font-weight="%s">%s</text>' % (' class="%s"' % cls if cls else '', x, y, size, fill, anchor, weight, s))
out.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif">' % (WID, HGT, WID, HGT))
out.append('<rect id="surface" x="0" y="0" width="%d" height="%d" fill="%s"/>' % (WID, HGT, SURF))
T(40, 32, 'Five shapes at one ceiling; the round-cornered triangle below it, as worked out beforehand', 16, INK, 'start', '600')
T(40, 54, 'The spread of the count of layers set against its mean: variance &#215; n / mean&#178;, for clouds of exactly n points. Bars: one standard error either way.', 12, INK2)
out.append('<circle class="key" cx="566" cy="84" r="5" fill="%s" stroke="%s" stroke-width="2"/>' % (SURF, BLUE)); T(578, 88, 'fresh clouds of 100,000 points, peeled afterwards (in no verdict)', 12, INK2)
# the key
out.append('<circle class="key" cx="46" cy="84" r="5" fill="%s"/>' % BLUE); T(58, 88, '100,000 points', 12, INK2)
out.append('<circle class="key" cx="176" cy="84" r="5" fill="%s"/>' % ORANGE); T(188, 88, '30,000 points', 12, INK2)
out.append('<line x1="296" y1="84" x2="326" y2="84" stroke="%s" stroke-width="3"/>' % INK); T(334, 88, 'where the theory puts the shape', 12, INK2)
for v in (0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.40):
    out.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>' % (X0, fy(v), X1, fy(v), GRID)); out.append('<text class="ytick" data-v="%.2f" x="%d" y="%.1f" font-size="11" fill="%s" text-anchor="end">%.2f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, v))
out.append('<line id="ceiling" x1="%d" y1="%.2f" x2="%d" y2="%.2f" stroke="%s" stroke-width="1.5" stroke-dasharray="7 4"><title>the ceiling: (4 D / 3 - (4/9) alpha^2) / alpha^2 = %.4f</title></line>' % (X0, fy(CEIL), X1, fy(CEIL), INK2, CEIL))
T(X1, YT - 8, 'dashed: the ceiling the equation gives with D = 1.081, %.4f' % CEIL, 12, INK2, 'end')
# the columns: three groups with a gap between
xs = []; x = X0 + 62
for i, (sh, label, grp) in enumerate(COLS):
    if i and COLS[i - 1][2] != grp: x += 44
    xs.append(x); x += 88
def outline(sh, cx, cy, s):
    """the shape's edge as a path, about (cx, cy), about 2 s across"""
    P = []
    if sh in ('disc', 'disc0'): P = [(math.cos(t), math.sin(t)) for t in [2 * math.pi * k / 60 for k in range(60)]]
    elif sh == 'ellipse': P = [(1.25 * math.cos(t), 1.25 * math.sin(t) / 3) for t in [2 * math.pi * k / 60 for k in range(60)]]
    elif sh == 'triangle': P = [(-1.1, -0.635), (1.1, -0.635), (0, 1.27)]
    elif sh == 'square': P = [(-0.85, -0.85), (0.85, -0.85), (0.85, 0.85), (-0.85, 0.85)]
    elif sh == 'hexagon': P = [(math.cos(math.pi * k / 3), math.sin(math.pi * k / 3)) for k in range(6)]
    elif sh == 'halfdisc': P = [(1.2 * math.cos(math.pi * k / 30), 1.2 * math.sin(math.pi * k / 30) - 0.5) for k in range(31)]
    elif sh == 'quarter': P = [(-0.75, -0.75)] + [(1.7 * math.cos(math.pi / 2 * k / 20) - 0.75, 1.7 * math.sin(math.pi / 2 * k / 20) - 0.75) for k in range(21)]
    elif sh == 'rtriangle':
        rin = 0.52; rr = rin / 4; a = 2 * math.sqrt(3) * rin; V = [(a / 2, -rin), (0, 2 * rin), (-a / 2, -rin)]
        for j in range(3): P += [(V[j][0] + rr * math.cos(math.radians(-90 + 120 * j + 6 * k)), V[j][1] + rr * math.sin(math.radians(-90 + 120 * j + 6 * k))) for k in range(21)]
    return '<path class="icon" d="M%s Z" fill="none" stroke="%s" stroke-width="1.5" stroke-linejoin="round"/>' % (' L'.join('%.1f %.1f' % (cx + s * px, cy - s * py) for px, py in P), INK2)
for (sh, label, grp), x, c in zip(COLS, xs, J['columns']):
    out.append('<g class="col" data-shape="%s">' % sh)
    out.append('<line class="theory" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="3"><title>%s: the theory puts it at %.4f</title></line>' % (x - 24, fy(c['theory']), x + 24, fy(c['theory']), INK, label, c['theory']))
    for n0, colour, dx in ((100000, BLUE, -9 if '30000' in c else 0), (30000, ORANGE, 9)):
        if str(n0) not in c: continue
        v, se, K = c[str(n0)]
        out.append('<line class="bar%d" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="2"/>' % (n0, x + dx, fy(v - se), x + dx, fy(v + se), colour))
        out.append('<circle class="dot%d" cx="%.1f" cy="%.2f" r="5" fill="%s" stroke="%s" stroke-width="2"><title>%s, %s clouds of %s points: %.4f, give or take %.4f</title></circle>' % (n0, x + dx, fy(v), colour, SURF, label, format(K, ','), format(n0, ','), v, se))
    for j, (k, w, wse, K, maker) in enumerate(c['fresh']):
        xo = x + (27 if '30000' in c else 18) + 16 * j
        out.append('<line class="fbar" data-set="%s" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="1.5"/>' % (k, xo, fy(w - wse), xo, fy(w + wse), BLUE))
        out.append('<circle class="fdot" data-set="%s" cx="%.1f" cy="%.2f" r="4.5" fill="%s" stroke="%s" stroke-width="2"><title>%s, %s fresh clouds of 100,000 points by %s, peeled after the scoring: %.4f, give or take %.4f</title></circle>' % (k, xo, fy(w), SURF, BLUE, label, format(K, ','), maker, w, wse))
    out.append(outline(sh, x, 440, 17)); T(x, 482, label, 12, INK2, 'middle', cls='xlabel')
    if sh == 'disc0': T(x, 497, 'points', 12, INK2, 'middle', cls='xlabel')
    if sh == 'rtriangle': T(x, 497, 'triangle', 12, INK2, 'middle', cls='xlabel')
    out.append('</g>')
def brace(xa, xb, text):
    out.append('<line x1="%.1f" y1="522" x2="%.1f" y2="522" stroke="%s" stroke-width="1"/>' % (xa - 30, xb + 30, MUTED)); T((xa + xb) / 2, 540, text, 12, INK2, 'middle')
brace(xs[0], xs[5], 'shapes the theory puts at the ceiling'); brace(xs[6], xs[7], 'a little below'); brace(xs[8], xs[8], 'furthest below')
out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>' % (X0, YB, X1, YB, MUTED))
out.append('</svg>')
open(os.path.join(HERE, 'shape.svg'), 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('shape.svg written; ceiling %.4f; %d columns' % (CEIL, len(xs)))
