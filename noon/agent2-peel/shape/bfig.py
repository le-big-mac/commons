"""bfig.py: the plate of the fourth sheet, small.svg, and the numbers on it, bfig.json.   python -I bfig.py
For discs of exactly n points, the variance of the count over the theory's, against n^(-1/3), so that very many points are at the
left edge and 100 points at the right. Dots: the third sheet's five sizes (blue) and the fourth sheet's three (orange), one standard
error either way. Solid line: the straight line c n^(1/3) + b fitted to the variances of all eight sizes, over the theory's
c n^(1/3). Dashed lines: the theory as it stood (1 at every size) and the third sheet's own line (fitted to its five sizes) carried
down to where the fourth sheet's clouds are: what a constant said before they were peeled."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study3, study4, theory, after4
S = after4.gather(); SIZES = list(S); CTH = theory.predictions('disc', 1.0)['exact']; b, e, chi, dof = after4.series(S, SIZES, 2)
J = {'sizes': {str(n): [S[n]['v'] / S[n]['tv'], S[n]['vse'] / S[n]['tv'], S[n]['K'], 4 if n in study4.NEW else 3] for n in SIZES}, 'fit': {'c': float(b[0]), 'c_se': float(e[0]), 'b': float(b[1]), 'b_se': float(e[1]), 'chi2': chi, 'dof': dof, 'a': float(b[0] / CTH), 'a_se': float(e[0] / CTH), 'slope': float(b[1] / CTH)},
     'third': [study4.C5 / CTH, study4.B5 / CTH], 'theory_c': CTH}
SURF, INK, INK2, MUTED, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9'; BLUE, ORANGE = '#2a78d6', '#eb6834'
WID, HGT = 900, 520; X0, X1, YB, YT = 84, 860, 420, 128; XLO, XHI = 0.0, 0.23; VLO, VHI = 0.88, 1.04; out = []
fx = lambda x: X0 + (X1 - X0) * (x - XLO) / (XHI - XLO); fy = lambda v: YB + (YT - YB) * (v - VLO) / (VHI - VLO)
def T(x, y, s, size=12, fill=INK2, anchor='start', weight='normal'): out.append('<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s" font-weight="%s">%s</text>' % (x, y, size, fill, anchor, weight, s))
out.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif">' % (WID, HGT, WID, HGT))
out.append('<rect id="surface" x="0" y="0" width="%d" height="%d" fill="%s"/>' % (WID, HGT, SURF))
lo, hi = min(SIZES), max(SIZES)
if len(SIZES) == 8 and chi <= 16.8 and -0.050 <= b[1] <= -0.035: title = 'A line %.1f in 100 steeper than the theory&#8217;s, less %.2f, fits from %s points to %s' % (100 * (b[0] / CTH - 1), -b[1], format(lo, ','), format(hi, ','))
elif len(SIZES) == 8: title = 'From %s points to %s the lean is not one straight line (chi-square %.0f on %d)' % (format(lo, ','), format(hi, ','), chi, dof)
else: title = 'The lean at %d sizes' % len(SIZES)
J['title'] = title; T(40, 32, title, 16, INK, 'start', '600')
T(40, 54, 'Discs of exactly n points: the variance of the count over what the theory gives, against n to the power &#8722;1/3.', 12, INK2)
ses = [J['sizes'][str(n)][1] for n in SIZES]; T(40, 71, 'Bars: one standard error either way (%.3f to %.3f; most are hidden by their dots). The solid line is c&#183;n^(1/3) + b fitted to all eight variances.' % (min(ses), max(ses)), 12, INK2)
out.append('<circle class="key" cx="46" cy="98" r="5" fill="%s"/>' % BLUE); T(58, 102, 'the third sheet&#8217;s discs', 12, INK2)
out.append('<circle class="key" cx="226" cy="98" r="5" fill="%s"/>' % ORANGE); T(238, 102, 'the fourth sheet&#8217;s discs', 12, INK2)
out.append('<line x1="412" y1="98" x2="442" y2="98" stroke="%s" stroke-width="2"/>' % INK); T(450, 102, 'the line fitted', 12, INK2)
out.append('<line x1="556" y1="98" x2="586" y2="98" stroke="%s" stroke-width="1.5" stroke-dasharray="6 4"/>' % MUTED); T(594, 102, 'the theory; the third sheet&#8217;s line carried down', 12, INK2)
for k in range(9):
    v = 0.88 + 0.02 * k; out.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>' % (X0, fy(v), X1, fy(v), GRID)); out.append('<text class="ytick" data-v="%.2f" x="%d" y="%.1f" font-size="11" fill="%s" text-anchor="end">%.2f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, v))
for n, lab in ((None, 'very many'), (300000, ''), (100000, '100,000'), (30000, ''), (10000, '10,000'), (3000, '3,000'), (1000, '1,000'), (300, '300'), (100, '100')):
    x = 0.0 if n is None else n ** (-1 / 3.0); out.append('<line class="tick" data-n="%s" x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1"/>' % (n if n else 0, fx(x), YB, fx(x), YB + 5, MUTED))
    if lab: out.append('<text class="xtick" data-n="%s" x="%.1f" y="%d" font-size="11" fill="%s" text-anchor="middle">%s</text>' % (n if n else 0, fx(x), YB + 20, MUTED, lab))
T((X0 + X1) / 2, YB + 42, 'points in the cloud (placed at n to the power &#8722;1/3; the unlabelled marks are 300,000 and 30,000)', 12, INK2, 'middle')
out.append('<line id="plain" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="1.5" stroke-dasharray="6 4"><title>the theory as it stood: 1 at every size</title></line>' % (fx(XLO), fy(1.0), fx(XHI), fy(1.0), MUTED))
a3, s3 = J['third']; out.append('<line id="third" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="1.5" stroke-dasharray="6 4"><title>the third sheet\'s line, fitted to 3,000 to 300,000 points and carried down: %.4f %+.3f n^(-1/3)</title></line>' % (fx(XLO), fy(a3), fx(XHI), fy(a3 + s3 * XHI), MUTED, a3, s3))
T(fx(0.19), fy(1.0) - 7, 'the theory', 11, MUTED, 'middle'); T(fx(0.168), fy(a3 + s3 * 0.168) + 30, 'the third sheet&#8217;s line, carried down', 11, MUTED, 'end')
a, s = J['fit']['a'], J['fit']['slope']
out.append('<line id="fit" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="2"><title>fitted to all eight sizes: variance = %.5f n^(1/3) %+.4f; over the theory\'s, %.4f %+.3f n^(-1/3)</title></line>' % (fx(0), fy(a), fx(lo ** (-1 / 3.0)), fy(a + s * lo ** (-1 / 3.0)), INK, b[0], b[1], a, s))
out.append('<circle id="adot" cx="%.1f" cy="%.2f" r="5" fill="%s" stroke="%s" stroke-width="2"><title>where the fitted line ends, for very many points: %.4f, give or take %.4f</title></circle>' % (fx(0), fy(a), INK, SURF, a, J['fit']['a_se']))
T(fx(0) + 10, fy(a) - 12, '%.4f (%.4f)' % (a, J['fit']['a_se']), 11, INK2)
T(fx(0.105), fy(a + s * 0.105) - 34, 'variance = %.4f&#183;n^(1/3) &#8722; %.3f' % (b[0], -b[1]), 12, INK, 'start'); T(fx(0.105), fy(a + s * 0.105) - 18, 'where the theory has %.4f&#183;n^(1/3)' % CTH, 11, INK2, 'start')
for n in SIZES:
    x = n ** (-1 / 3.0); r, se, K, sheet = J['sizes'][str(n)]; col = ORANGE if sheet == 4 else BLUE
    out.append('<line class="bar" data-n="%d" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="2"/>' % (n, fx(x), fy(r - se), fx(x), fy(r + se), col))
    out.append('<circle class="dot" data-n="%d" cx="%.1f" cy="%.2f" r="5" fill="%s" stroke="%s" stroke-width="2"><title>%s discs of %s points: %.4f, give or take %.4f</title></circle>' % (n, fx(x), fy(r), col, SURF, format(K, ','), format(n, ','), r, se))
out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>' % (X0, YB, X1, YB, MUTED))
out.append('</svg>')
json.dump(J, open(os.path.join(HERE, 'bfig.json'), 'w'), indent=1)
open(os.path.join(HERE, 'small.svg'), 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('small.svg written: %d sizes; variance = %.5f (%.5f) n^(1/3) %+.4f (%.4f), chi-square %.1f on %d' % (len(SIZES), b[0], e[0], b[1], e[1], chi, dof))
