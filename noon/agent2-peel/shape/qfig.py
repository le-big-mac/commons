"""qfig.py: the plate of the second sheet, quarter.svg, and the numbers on it, qfig.json.   python -I qfig.py
Every set of quarter discs peeled in this study, in the order they were made: r = (variance of the count x n / mean^2) over the
quarter disc's own line, with one standard error either way. Blue: points from my generator (cloud.c); orange: points from numpy's.
The last mark is the second sheet's four sets together, against the band its line A1 allowed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study, study2, fresh, theory
LINE = study2.line_of(1e5)[0]; CEIL = (4 / 3.0 * theory.D - theory.DC) / theory.ALPHA ** 2
rows = []
w, se = study.stat(lambda m, v: v / m ** 2 * 1e5, 'exact-quarter-100000'); rows.append({'group': 0, 'maker': 'cloud.c', 'n': 100000, 'K': study.F['exact-quarter-100000']['K'], 'r': w / LINE, 'se': se / LINE})
for key in ('quarter-cloud-a', 'quarter-cloud-b', 'quarter-numpy'):
    f = fresh.reckon(key); rows.append({'group': 1, 'maker': f['maker'], 'n': 100000, 'K': f['K'], 'r': f['w'] / LINE, 'se': f['wse'] / LINE})
for key, (name, n) in study2.SETS.items():
    v = study2.R[key]
    if v is not None: rows.append({'group': 2, 'maker': 'cloud.c' if key.startswith('cloud') else 'numpy', 'n': n, 'K': v['K'], 'r': v['r'], 'se': v['rse']})
allfour = study2.together(study2.ALL)
J = {'line': LINE, 'ceiling_over_line': CEIL / LINE, 'rows': rows, 'together': list(allfour) if allfour else None, 'band': [0.996, 1.008]}
json.dump(J, open(os.path.join(HERE, 'qfig.json'), 'w'), indent=1)
SURF, INK, INK2, MUTED, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9'; BLUE, ORANGE = '#2a78d6', '#eb6834'; COL = {'cloud.c': BLUE, 'numpy': ORANGE}
WID, HGT = 940, 520; X0, X1, YB, YT = 78, 900, 380, 140; VLO, VHI = 0.98, 1.06; out = []
fy = lambda v: YB + (YT - YB) * (v - VLO) / (VHI - VLO)
def T(x, y, s, size=12, fill=INK2, anchor='start', weight='normal', cls=None): out.append('<text%s x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s" font-weight="%s">%s</text>' % (' class="%s"' % cls if cls else '', x, y, size, fill, anchor, weight, s))
out.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif">' % (WID, HGT, WID, HGT))
out.append('<rect id="surface" x="0" y="0" width="%d" height="%d" fill="%s"/>' % (WID, HGT, SURF))
title = 'TITLE'
if allfour: title = ('The quarter disc is on its line to %.1f parts in 100: the four sealed sets give %.3f (%.3f)' % (200 * allfour[1], allfour[0], allfour[1])) if 0.996 <= allfour[0] <= 1.008 else ('The quarter disc is off its line: the four sealed sets give %.3f (%.3f)' % (allfour[0], allfour[1]))
T(40, 32, title, 16, INK, 'start', '600'); J['title'] = title
T(40, 54, 'Every set of quarter discs, in the order it was made: the spread of the count (variance &#215; n / mean&#178;) over what the theory gives,', 12, INK2)
T(40, 71, 'so that 1 is the quarter disc&#8217;s own line. Bars: one standard error either way.', 12, INK2)
out.append('<circle class="key" cx="46" cy="100" r="5" fill="%s"/>' % BLUE); T(58, 104, 'points from my generator', 12, INK2)
out.append('<circle class="key" cx="236" cy="100" r="5" fill="%s"/>' % ORANGE); T(248, 104, 'points from numpy&#8217;s', 12, INK2)
for v in (0.98, 1.00, 1.02, 1.04, 1.06):
    out.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="%s"/>' % (X0, fy(v), X1, fy(v), MUTED if v == 1.0 else GRID, '1.5' if v == 1.0 else '1')); out.append('<text class="ytick" data-v="%.2f" x="%d" y="%.1f" font-size="11" fill="%s" text-anchor="end">%.2f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, v))
n9 = len(rows) + (1 if allfour else 0); gap = 40; xs = []; x = X0 + 56; step = (X1 - X0 - 112 - 3 * gap) / max(n9 - 1, 1)
for i, r in enumerate(rows):
    if i and rows[i - 1]['group'] != r['group']: x += gap
    xs.append(x); x += step
xt = x + gap
if allfour:
    out.append('<rect id="band" x="%.1f" y="%.2f" width="56" height="%.2f" fill="%s"/>' % (xt - 28, fy(1.008), fy(0.996) - fy(1.008), GRID))
    out.append('<line id="tbar" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="2"/>' % (xt, fy(allfour[0] - allfour[1]), xt, fy(allfour[0] + allfour[1]), INK))
    out.append('<circle id="tdot" cx="%.1f" cy="%.2f" r="5" fill="%s" stroke="%s" stroke-width="2"><title>the second sheet&#8217;s four sets together: %.4f, give or take %.4f; the band its line allowed: 0.996 to 1.008</title></circle>' % (xt, fy(allfour[0]), INK, SURF, allfour[0], allfour[1]))
    T(xt, YB + 22, 'the four', 12, INK2, 'middle', cls='xlabel'); T(xt, YB + 37, 'together', 12, INK2, 'middle', cls='xlabel'); T(xt, fy(1.008) - 8, 'allowed', 11, MUTED, 'middle')
for r, x in zip(rows, xs):
    out.append('<g class="set" data-group="%d" data-maker="%s" data-n="%d" data-k="%d">' % (r['group'], r['maker'], r['n'], r['K']))
    out.append('<line class="bar" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="2"/>' % (x, fy(r['r'] - r['se']), x, fy(r['r'] + r['se']), COL[r['maker']]))
    out.append('<circle class="dot" cx="%.1f" cy="%.2f" r="5" fill="%s" stroke="%s" stroke-width="2"><title>%s quarter discs of %s points, points by %s: %.4f, give or take %.4f</title></circle>' % (x, fy(r['r']), COL[r['maker']], SURF, format(r['K'], ','), format(r['n'], ','), r['maker'], r['r'], r['se']))
    T(x, YB + 22, format(r['K'], ','), 12, INK2, 'middle', cls='xlabel'); T(x, YB + 37, format(r['n'], ','), 11, MUTED, 'middle', cls='xlabel'); out.append('</g>')
def brace(xa, xb, text, text2=None):
    out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1"/>' % (xa - 30, YB + 52, xb + 30, YB + 52, MUTED)); T((xa + xb) / 2, YB + 70, text, 12, INK2, 'middle')
    if text2: T((xa + xb) / 2, YB + 86, text2, 12, INK2, 'middle')
g0 = [x for r, x in zip(rows, xs) if r['group'] == 0]; g1 = [x for r, x in zip(rows, xs) if r['group'] == 1]; g2 = [x for r, x in zip(rows, xs) if r['group'] == 2]
brace(g0[0], g0[-1], 'the first', 'sheet'); brace(g1[0], g1[-1], 'peeled to chase it, in no verdict')
if g2: brace(g2[0], g2[-1], 'the second sheet: sealed before they were peeled')
T(X0 + 4, fy(1.0) + 15, 'the theory&#8217;s line for the quarter disc', 11, MUTED)
out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>' % (X0, YB, X1, YB, MUTED)); T(X0 - 8, YB + 22, 'clouds', 11, MUTED, 'end'); T(X0 - 8, YB + 37, 'points', 11, MUTED, 'end')
out.append('</svg>')
open(os.path.join(HERE, 'quarter.svg'), 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('quarter.svg written: %d sets%s' % (len(rows), '; together %.4f (%.4f)' % tuple(allfour) if allfour else ''))
