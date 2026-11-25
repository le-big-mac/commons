"""zfig.py: the plate of the fifth sheet's first part, swing.svg, and the numbers on it, zfig.json.   python -I zfig.py
Discs of 83 to 120 points: what is left of the variance of the count when 0.08227 n^(1/3) is taken off (B), against the number of
points. Dots: the fifth sheet's six sizes (blue) and the fourth sheet's 100 points (orange), one standard error either way. Solid
curve: what a smooth quantity taken to a whole number gives (ruler5.py's model, fixed before the clouds were peeled), at every size
from 80 to 124. Dashed: the level run that a count with no term of its own would give (the fourth sheet's straight line).
Along the top, the mean count that the model expects at each size: whole numbers and halves are marked."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study5, study4, ruler5
C5 = study5.C5; G = ruler5.gamma100(); NS = list(range(80, 125)); CURVE = {n: ruler5.swing_model(n, G) - C5 * n ** (1 / 3.0) for n in NS}; LEVEL = {n: ruler5.line_of(n) - C5 * n ** (1 / 3.0) for n in NS}
DOTS = {n: (study5.R['disc-%d' % n]['B'], study5.R['disc-%d' % n]['vse'], study5.R['disc-%d' % n]['K'], 5) for n in study5.LAT if study5.R.get('disc-%d' % n) is not None}
if study4.R.get(100) is not None: DOTS[100] = (study4.R[100]['B'], study4.R[100]['vse'], study4.R[100]['K'], 4)
J = {'dots': {str(n): list(v) for n, v in sorted(DOTS.items())}, 'curve': {str(n): CURVE[n] for n in NS}, 'level': {str(n): LEVEL[n] for n in NS}, 'gamma': G}
SURF, INK, INK2, MUTED, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9'; BLUE, ORANGE = '#2a78d6', '#eb6834'
WID, HGT = 900, 520; X0, X1, YB, YT = 84, 860, 420, 150; XLO, XHI = 80, 124; VLO, VHI = -0.055, -0.020; out = []
fx = lambda x: X0 + (X1 - X0) * (x - XLO) / (XHI - XLO); fy = lambda v: YB + (YT - YB) * (v - VLO) / (VHI - VLO)
def T(x, y, s, size=12, fill=INK2, anchor='start', weight='normal'): out.append('<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s" font-weight="%s">%s</text>' % (x, y, size, fill, anchor, weight, s))
out.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif">' % (WID, HGT, WID, HGT))
out.append('<rect id="surface" x="0" y="0" width="%d" height="%d" fill="%s"/>' % (WID, HGT, SURF))
six = [n for n in study5.LAT if n in DOTS]; title = 'The six sizes are not all there'
if len(six) == 6:
    Z = (DOTS[90][0] + DOTS[105][0] + DOTS[120][0]) / 3 - (DOTS[83][0] + DOTS[98][0] + DOTS[113][0]) / 3; Ze = math.sqrt(sum(DOTS[n][1] ** 2 for n in six)) / 3; J['Z'] = [Z, Ze]
    if Z >= 0.008: title = 'A count in whole layers: its variance swings as the mean passes whole numbers and halves'
    elif Z <= 0.004: title = 'No swing: the variance runs level as the mean count passes whole numbers and halves'
    else: title = 'A swing smaller than a rounded quantity&#8217;s: %.4f, give or take %.4f, where it gives 0.0131' % (Z, Ze)
J['title'] = title; T(40, 32, title, 16, INK, 'start', '600')
T(40, 54, 'Discs of exactly n points: the variance of the count less 0.08227&#183;n^(1/3), against n. Bars: one standard error either way.', 12, INK2)
T(40, 71, 'The curve was fixed before the blue clouds were peeled: a smooth quantity taken to the nearest whole number.', 12, INK2)
out.append('<circle class="key" cx="46" cy="98" r="5" fill="%s"/>' % BLUE); T(58, 102, 'the fifth sheet&#8217;s discs', 12, INK2)
out.append('<circle class="key" cx="216" cy="98" r="5" fill="%s"/>' % ORANGE); T(228, 102, 'the fourth sheet&#8217;s 100 points (the curve&#8217;s source)', 12, INK2)
out.append('<line x1="580" y1="98" x2="610" y2="98" stroke="%s" stroke-width="2"/>' % INK); T(618, 102, 'a rounded quantity', 12, INK2)
out.append('<line x1="756" y1="98" x2="786" y2="98" stroke="%s" stroke-width="1.5" stroke-dasharray="6 4"/>' % MUTED); T(794, 102, 'a level run', 12, INK2)
for k in range(8):
    v = -0.055 + 0.005 * k; out.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>' % (X0, fy(v), X1, fy(v), GRID)); out.append('<text class="ytick" data-v="%.3f" x="%d" y="%.1f" font-size="11" fill="%s" text-anchor="end">&#8722;%.3f</text>' % (v, X0 - 8, fy(v) + 4, MUTED, -v))
for n in range(80, 125, 5): out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1"/>' % (fx(n), YB, fx(n), YB + 5, MUTED)); out.append('<text class="xtick" data-n="%d" x="%.1f" y="%d" font-size="11" fill="%s" text-anchor="middle">%d</text>' % (n, fx(n), YB + 20, MUTED, n))
T((X0 + X1) / 2, YB + 42, 'points in the cloud', 12, INK2, 'middle')
T(X0, YT - 28, 'the mean count expected at each size (whole numbers and halves marked):', 11, MUTED, 'start')
for h in range(18, 24):      # the mean counts 9.0, 9.5, ... 11.5: where the model's mean passes them
    m = h / 2.0; n = min((abs(ruler5.mean_of(x / 20.0) - m), x / 20.0) for x in range(80 * 20, 124 * 20 + 1))[1]
    if 80.5 <= n <= 123.5: out.append('<line class="mtick" data-m="%.1f" x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1"/>' % (m, fx(n), YT - 8, fx(n), YT, MUTED)); out.append('<text class="mlab" data-m="%.1f" x="%.1f" y="%d" font-size="11" fill="%s" text-anchor="middle">%s</text>' % (m, fx(n), YT - 12, MUTED, ('%d' % m) if h % 2 == 0 else ('%.1f' % m)))
out.append('<polyline id="level" fill="none" stroke="%s" stroke-width="1.5" stroke-dasharray="6 4" points="%s"/>' % (MUTED, ' '.join('%.1f,%.2f' % (fx(n), fy(LEVEL[n])) for n in NS)))
out.append('<polyline id="curve" fill="none" stroke="%s" stroke-width="2" points="%s"/>' % (INK, ' '.join('%.1f,%.2f' % (fx(n), fy(CURVE[n])) for n in NS)))
for n, (B, se, K, sheet) in sorted(DOTS.items()):
    col = ORANGE if sheet == 4 else BLUE
    out.append('<line class="bar" data-n="%d" x1="%.1f" y1="%.2f" x2="%.1f" y2="%.2f" stroke="%s" stroke-width="2"/>' % (n, fx(n), fy(B - se), fx(n), fy(B + se), col))
    out.append('<circle class="dot" data-n="%d" cx="%.1f" cy="%.2f" r="5" fill="%s" stroke="%s" stroke-width="2"><title>%s discs of %d points: %.4f, give or take %.4f; a rounded quantity gives %.4f, a level run %.4f</title></circle>' % (n, fx(n), fy(B), col, SURF, format(K, ','), n, B, se, CURVE[n], LEVEL[n]))
out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>' % (X0, YB, X1, YB, MUTED))
out.append('</svg>')
json.dump(J, open(os.path.join(HERE, 'zfig.json'), 'w'), indent=1)
open(os.path.join(HERE, 'swing.svg'), 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('swing.svg written: %d dots' % len(DOTS))
