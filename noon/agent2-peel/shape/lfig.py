"""lfig.py: the plate of the third sheet, lean.svg, and the numbers on it, lfig.json.   python -I lfig.py
For discs of exactly n points, r (variance of the count x n / mean^2, over the theory's 0.37544) against n^(-1/3), so that very
many points are at the left edge. Dots: the third sheet's five sizes, one standard error either way. The dashed lines are the
two readings written on the sheet before the clouds were peeled: plain (r = 1) and the lean read from the earlier clouds
(r = 1.018 - 0.64 n^(-1/3)). The solid line is the least-squares line through the four sizes from 10,000 to 300,000, drawn on to
very many points, with one standard error either way of where it ends."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study3
R = study3.R; F4 = study3.F4; SIZES = [n for n in study3.ASKED if R[n] is not None]
J = {'sizes': {str(n): [R[n]['r'], R[n]['rse'], R[n]['K']] for n in SIZES}, 'fit': list(F4) if F4 else None, 'plain': [1.0, 0.0], 'lean': [1.018, -0.64]}
SURF, INK, INK2, MUTED, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9'; BLUE = '#2a78d6'
WID, HGT = 900, 500; X0, X1, YB, YT = 84, 860, 400, 124; XLO, XHI = 0.0, 0.075; VLO, VHI = 0.97, 1.03; out = []
fx = lambda x: X0 + (X1 - X0) * (x - XLO) / (XHI - XLO); fy = lambda v: YB + (YT - YB) * (v - VLO) / (VHI - VLO)
def T(x, y, s, size=12, fill=INK2, anchor='start', weight='normal', cls=None): out.append('<text%s x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s" font-weight="%s">%s</text>' % (' class="%s"' % cls if cls else '', x, y, size, fill, anchor, weight, s))
out.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif">' % (WID, HGT, WID, HGT))
out.append('<rect id="surface" x="0" y="0" width="%d" height="%d" fill="%s"/>' % (WID, HGT, SURF))
title = 'TITLE'
if F4:
    below = [n for n in SIZES if R[n]['r'] < 1]; above = [n for n in SIZES if R[n]['r'] >= 1]
    if F4[0] <= -0.32 and below and above and max(below) < 30000 <= min(above): title = 'The smaller the cloud, the lower: below the theory under 30,000 points, above it over'
    elif F4[0] <= -0.32: title = 'The smaller the cloud, the lower its spread against the theory'
    elif F4[0] >= -0.18: title = 'No lean from 10,000 to 300,000 points: the spread stays on the theory&#8217;s line'
    else: title = 'A lean between the two readings: slope %.2f, give or take %.2f' % (F4[0], F4[1])
J['title'] = title; T(40, 32, title, 16, INK, 'start', '600')
T(40, 54, 'Discs of exactly n points: the spread of the count (variance &#215; n / mean&#178;) over what the theory gives, against n to the power &#8722;1/3.', 12, INK2)
T(40, 71, 'Bars: one standard error either way. The solid line is fitted to the four sizes from 10,000 to 300,000.', 12, INK2)
out.append('<circle class="key" cx="46" cy="98" r="5" fill="%s"/>' % BLUE); T(58, 102, 'the third sheet&#8217;s discs', 12, INK2)
out.append('<line x1="216" y1="98" x2="246" y2="98" stroke="%s" stroke-width="2"/>' % INK); T(254, 102, 'the line fitted', 12, INK2)
out.append('<line x1="356" y1="98" x2="386" y2="98" stroke="%s" stroke-width="1.5" stroke-dasharray="6 4"/>' % MUTED); T(394, 102, 'the two readings written beforehand', 12, INK2)
for v in (0.97, 0.98, 0.99, 1.00, 1.01, 1.02, 1.03):
    out.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>' % (X0, fy(v), X1, fy(v), GRID)); out.append('<text class="ytick" data-v="%.2f" x="%d" y="%.1f" font-size="11" fill="%s" text-anchor="end">%.2f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, v))
for n, lab in ((None, 'very many'), (300000, '300,000'), (100000, '100,000'), (30000, '30,000'), (10000, '10,000'), (3000, '3,000')):
    x = 0.0 if n is None else n ** (-1 / 3.0); out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1"/>' % (fx(x), YB, fx(x), YB + 5, MUTED)); out.append('<text class="xtick" data-n="%s" x="%.1f" y="%d" font-size="11" fill="%s" text-anchor="middle">%s</text>' % (n if n else 0, fx(x), YB + 20, MUTED, lab))
T((X0 + X1) / 2, YB + 42, 'points in the cloud (placed at n to the power &#8722;1/3)', 12, INK2, 'middle')
out.append('<line id="plain" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="1.5" stroke-dasharray="6 4"><title>the plain reading: r = 1 at every size</title></line>' % (fx(XLO), fy(1.0), fx(XHI), fy(1.0), MUTED))
out.append('<line id="lean" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="1.5" stroke-dasharray="6 4"><title>the lean read from the earlier clouds: r = 1.018 - 0.64 n^(-1/3)</title></line>' % (fx(XLO), fy(1.018), fx(XHI), fy(1.018 - 0.64 * XHI), MUTED))
T(fx(0.066), fy(1.0) - 7, 'plain', 11, MUTED, 'middle'); T(fx(0.047), fy(1.018 - 0.64 * 0.047) + 24, 'the lean read from the earlier clouds', 11, MUTED, 'end')
if F4:
    s, sse, a, ase, chi = F4; xr = 10000 ** (-1 / 3.0)
    out.append('<line id="fit" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="2"><title>the line fitted to the four sizes from 10,000 to 300,000: r = %.4f %+.3f n^(-1/3)</title></line>' % (fx(0), fy(a), fx(xr), fy(a + s * xr), INK, a, s))
    out.append('<line id="abar" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="2"/>' % (fx(0), fy(a - ase), fx(0), fy(a + ase), INK))
    out.append('<circle id="adot" cx="%.1f" cy="%.2f" r="5" fill="%s" stroke="%s" stroke-width="2"><title>where the fitted line ends, for very many points: %.4f, give or take %.4f</title></circle>' % (fx(0), fy(a), INK, SURF, a, ase))
    T(fx(0) + 10, fy(a + ase) - 6, '%.3f (%.3f)' % (a, ase), 11, INK2)
for n in SIZES:
    x = n ** (-1 / 3.0); r, se, K = J['sizes'][str(n)]
    out.append('<line class="bar" data-n="%d" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="2"/>' % (n, fx(x), fy(r - se), fx(x), fy(r + se), BLUE))
    out.append('<circle class="dot" data-n="%d" cx="%.1f" cy="%.2f" r="5" fill="%s" stroke="%s" stroke-width="2"><title>%s discs of %s points: %.4f, give or take %.4f</title></circle>' % (n, fx(x), fy(r), BLUE, SURF, format(K, ','), format(n, ','), r, se))
out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>' % (X0, YB, X1, YB, MUTED))
out.append('</svg>')
json.dump(J, open(os.path.join(HERE, 'lfig.json'), 'w'), indent=1)
open(os.path.join(HERE, 'lean.svg'), 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('lean.svg written: %d sizes%s' % (len(SIZES), '; slope %+.3f (%.3f), for very many points %.4f (%.4f)' % F4[:4] if F4 else ''))
