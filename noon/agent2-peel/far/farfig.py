"""farfig.py: the two plates of the addition, far.svg, and the numbers drawn on them, farfig.json.   python -I farfig.py
Left: the variance of depth over the square root of depth, by height (what C of after.out lists), with the level that the
wander of the mean predicts (0.600 D) and the curve a front of the other kind would follow from 4,000 up.
Right: for four heights (2,000, 8,000, 32,000 and 128,000), the mean square difference of depth between two columns over twice the variance, against the
distance over the square root of the height; and the curve the picture gives with nothing fitted.
Runs study.py silently for its windows and functions, as after.py does."""
import contextlib, io, json, math, os, runpy
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()): G = runpy.run_path(os.path.join(HERE, 'study.py'))
W, LONG, LOW, TALL, THICK, pool, wander, K600, SNAP, hs, gcurve, LAGS, wcol = (G[k] for k in ('W', 'LONG', 'LOW', 'TALL', 'THICK', 'pool', 'wander', 'K600', 'SNAP', 'hs', 'gcurve', 'LAGS', 'wcol'))
def shape(s): return 1 - math.exp(-s * s) + s * math.sqrt(math.pi) * math.erfc(s)
# ---- the numbers ----
y, mu, v = pool(W, TALL); v = v - THICK; left = []
h = 500
while h <= TALL:
    n = max(2, int(0.01 * h)); left.append({'height': h, 'ratio': float(v[h - n:h].mean() / math.sqrt(mu[h - n:h].mean()))}); h *= 2
level = K600 * wander(W)[0]; r4 = next(p['ratio'] for p in left if p['height'] == 4000)
right = []
for k, hh in enumerate(hs):
    if k % 16 == 0 and hh >= 1000:
        g, plateau = gcurve(k); right.append({'height': hh, 'points': [{'r': j * wcol, 'x': j * wcol / math.sqrt(hh + 2), 'g': float(g[i] / plateau)} for i, j in enumerate(LAGS)]})
right.sort(key=lambda c: c['height'])
json.dump({'left': left, 'level': level, 'other_from': 4000, 'other_at_4000': r4, 'right': right}, open(os.path.join(HERE, 'farfig.json'), 'w'), indent=1)
# ---- the drawing ----
SURF, INK, INK2, MUTED, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9'
BLUE, ORANGE = '#2a78d6', '#eb6834'; RAMP = ['#86b6ef', '#3987e5', '#1c5cab', '#0d366b']
WID, HGT = 1000, 470; out = []
def T(x, y_, s, size=12, fill=INK2, anchor='start', weight='normal'): out.append('<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s" font-weight="%s">%s</text>' % (x, y_, size, fill, anchor, weight, s))
out.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif">' % (WID, HGT, WID, HGT))
out.append('<rect id="surface" x="0" y="0" width="%d" height="%d" fill="%s"/>' % (WID, HGT, SURF))
# left plate
AX0, AX1, AY0, AY1 = 70, 460, 400, 110; LX0, LX1, LY0, LY1 = 400.0, 160000.0, 0.4, 1.2
def lx(hv): return AX0 + (AX1 - AX0) * (math.log(hv) - math.log(LX0)) / (math.log(LX1) - math.log(LX0))
def ly(rv): return AY0 + (AY1 - AY0) * (rv - LY0) / (LY1 - LY0)
out.append('<g id="left">')
T(AX0 - 50, 30, 'Variance of depth ÷ √depth, by height', 15, INK, 'start', '600')
T(AX0 - 50, 50, '27 windows, 88 thousand million points. It does not climb.', 12, INK2)
for rv in (0.4, 0.6, 0.8, 1.0, 1.2):
    out.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>' % (AX0, ly(rv), AX1, ly(rv), GRID)); out.append('<text class="ytick" data-v="%.1f" x="%d" y="%.1f" font-size="11" fill="%s" text-anchor="end">%.1f</text>' % (rv, AX0 - 8, ly(rv) + 4, MUTED, rv))
for hv in (500, 2000, 8000, 32000, 128000):
    out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1"/>' % (lx(hv), AY0, lx(hv), AY0 + 5, MUTED)); out.append('<text class="xtick" data-v="%d" x="%.1f" y="%d" font-size="11" fill="%s" text-anchor="middle">%s</text>' % (hv, lx(hv), AY0 + 19, MUTED, format(hv, ',')))
T((AX0 + AX1) / 2, AY0 + 40, 'height above the floor', 12, INK2, 'middle')
pts = ' '.join('%.1f,%.1f' % (lx(4000 * 2 ** (i / 8.0)), ly(r4 * (2 ** (i / 8.0)) ** (1 / 6.0))) for i in range(0, 41))
out.append('<polyline id="other" points="%s" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="6 4"><title>what a variance growing as the two-thirds power of the height would give, starting from the measured value at 4,000</title></polyline>' % (pts, ORANGE))
out.append('<line id="level" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2"><title>0.600 D = %.3f, from how fast a window\'s mean depth wanders</title></line>' % (lx(500), ly(level), lx(128000), ly(level), INK, level))
out.append('<polyline id="measured-line" points="%s" fill="none" stroke="%s" stroke-width="2"/>' % (' '.join('%.1f,%.1f' % (lx(p['height']), ly(p['ratio'])) for p in left), BLUE))
for p in left: out.append('<circle class="measured" cx="%.2f" cy="%.2f" r="4.5" fill="%s" stroke="%s" stroke-width="2"><title>height %s: %.3f</title></circle>' % (lx(p['height']), ly(p['ratio']), BLUE, SURF, format(p['height'], ','), p['ratio']))
out.append('<circle cx="%d" cy="78" r="4.5" fill="%s"/>' % (AX0 + 6, BLUE)); T(AX0 + 16, 82, 'measured', 12, INK2)
out.append('<line x1="%d" y1="78" x2="%d" y2="78" stroke="%s" stroke-width="2"/>' % (AX0 + 84, AX0 + 106, INK)); T(AX0 + 112, 82, 'predicted from the wander', 12, INK2)
out.append('<line x1="%d" y1="78" x2="%d" y2="78" stroke="%s" stroke-width="2" stroke-dasharray="6 4"/>' % (AX0 + 284, AX0 + 306, ORANGE)); T(AX0 + 312, 82, 'the other kind of front', 12, INK2)
T(lx(128000) - 4, ly(r4 * 32 ** (1 / 6.0)) - 10, 'variance as height to the 2/3', 11, INK2, 'end')
T(lx(600), ly(level) + 18, 'measured, and 0.600 × D = %.3f' % level, 11, INK2)
out.append('</g>')
# right plate
BX0, BX1, BY0, BY1 = 580, 970, 400, 110; RX0, RX1, RY0, RY1 = 0.004, 300.0, 0.0, 1.2
def rx(xv): return BX0 + (BX1 - BX0) * (math.log(xv) - math.log(RX0)) / (math.log(RX1) - math.log(RX0))
def ry(gv): return BY0 + (BY1 - BY0) * (gv - RY0) / (RY1 - RY0)
out.append('<g id="right">')
T(BX0 - 50, 30, 'How alike two columns are, by distance ÷ √height', 15, INK, 'start', '600')
T(BX0 - 50, 50, 'Mean square difference ÷ twice the variance. Four heights, one curve.', 12, INK2)
for gv in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2):
    out.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>' % (BX0, ry(gv), BX1, ry(gv), GRID)); out.append('<text class="ytick" data-v="%.1f" x="%d" y="%.1f" font-size="11" fill="%s" text-anchor="end">%.1f</text>' % (gv, BX0 - 8, ry(gv) + 4, MUTED, gv))
for xv in (0.01, 0.1, 1, 10, 100):
    out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1"/>' % (rx(xv), BY0, rx(xv), BY0 + 5, MUTED)); out.append('<text class="xtick" data-v="%g" x="%.1f" y="%d" font-size="11" fill="%s" text-anchor="middle">%g</text>' % (xv, rx(xv), BY0 + 19, MUTED, xv))
T((BX0 + BX1) / 2, BY0 + 40, 'distance between the columns ÷ √height', 12, INK2, 'middle')
pts = ' '.join('%.1f,%.1f' % (rx(xv), ry(shape(xv / math.sqrt(8 / 3.0)))) for xv in [RX0 * (RX1 / RX0) ** (i / 200.0) for i in range(201)])
out.append('<polyline id="theory" points="%s" fill="none" stroke="%s" stroke-width="2"><title>1 - exp(-s^2) + s sqrt(pi) erfc(s), s = distance / sqrt(8 height / 3): nothing fitted</title></polyline>' % (pts, INK))
for i, c in enumerate(right):
    for p in c['points']: out.append('<circle class="curve h%d" cx="%.2f" cy="%.2f" r="3" fill="%s" stroke="%s" stroke-width="1"><title>height %s, %d apart: %.3f</title></circle>' % (c['height'], rx(p['x']), ry(p['g']), RAMP[i], SURF, format(c['height'], ','), p['r'], p['g']))
T(BX0, 82, 'height', 12, INK2)
for i, c in enumerate(right):
    out.append('<circle class="key" cx="%d" cy="78" r="4" fill="%s"/>' % (BX0 + 52 + i * 62, RAMP[i])); T(BX0 + 60 + i * 62, 82, format(int(round(c['height'], -3)), ','), 11, INK2)
out.append('<line x1="%d" y1="78" x2="%d" y2="78" stroke="%s" stroke-width="2"/>' % (BX0 + 308, BX0 + 330, INK)); T(BX0 + 336, 82, 'predicted', 12, INK2)
T(rx(0.5715) + 8, ry(0.5) + 16, 'half way at 0.57', 11, INK2)
out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1" stroke-dasharray="2 3"/>' % (rx(0.5715), ry(0.5), rx(0.5715), BY0, MUTED))
out.append('</g></svg>')
open(os.path.join(HERE, 'far.svg'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('far.svg: %d bytes; left %d points, level %.3f; right %d heights of %d points' % (len('\n'.join(out)), len(left), level, len(right), len(right[0]['points'])))
