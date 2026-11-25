"""dfig.py: the three plates of the disc test, disc.svg, and the numbers drawn on them, dfig.json.   python -I dfig.py
All for discs of a million points. Left: the variance from cloud to cloud of the ring's mean depth, by radius, for clouds whose number
of points is left to chance and for clouds of exactly a million, with the two predicted curves. Middle: the variance of depth round a
ring (exactly a million points), with the predicted curve and, for contrast, what the level problem's law would give. Right: the mean
squares of the first three parts (cos and sin of once, twice and three times the angle), with their predicted curves."""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dtheory as th
from dlib import RAD, K, load, var
N = 10 ** 6; CH, EX = load('chance', N), load('exact', N)
J = {'radii': RAD, 'chance': [var(CH['Q'][:, k]) for k in range(19)], 'exact': [var(EX['Q'][:, k]) for k in range(19)], 'round': [float(EX['V'][:, k].mean()) for k in range(19)],
     'parts': {str(m): [float(EX['P'][m][:, k].mean()) for k in range(19)] for m in (1, 2, 3)}}
json.dump(J, open(os.path.join(HERE, 'dfig.json'), 'w'), indent=1)
SURF, INK, INK2, MUTED, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9'; BLUE, ORANGE = '#2a78d6', '#eb6834'; RAMP = ['#86b6ef', '#2a78d6', '#0d366b']
WID, HGT = 1120, 450; out = []
def T(x, y, s, size=12, fill=INK2, anchor='start', weight='normal'): out.append('<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s" font-weight="%s">%s</text>' % (x, y, size, fill, anchor, weight, s))
out.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="system-ui, -apple-system, Segoe UI, Helvetica, Arial, sans-serif">' % (WID, HGT, WID, HGT))
out.append('<rect id="surface" x="0" y="0" width="%d" height="%d" fill="%s"/>' % (WID, HGT, SURF))
GR = [i / 200.0 for i in range(1, 200)]
def plate(pid, x0, title, sub, ymax, yticks, fmt):
    x1 = x0 + 290; y0, y1 = 385, 125
    fx = lambda r: x0 + (x1 - x0) * r; fy = lambda v: y0 + (y1 - y0) * v / ymax
    out.append('<g id="%s">' % pid); T(x0 - 36, 28, title, 15, INK, 'start', '600'); T(x0 - 36, 48, sub, 12, INK2)
    for v in yticks:
        out.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>' % (x0, fy(v), x1, fy(v), GRID)); out.append('<text class="ytick" data-v="%g" x="%d" y="%.1f" font-size="11" fill="%s" text-anchor="end">%s</text>' % (v, x0 - 8, fy(v) + 4, MUTED, fmt % v))
    for r in (0, 0.25, 0.5, 0.75, 1):
        out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1"/>' % (fx(r), y0, fx(r), y0 + 5, MUTED)); out.append('<text class="xtick" data-v="%g" x="%.1f" y="%d" font-size="11" fill="%s" text-anchor="middle">%g</text>' % (r, fx(r), y0 + 19, MUTED, r))
    T((x0 + x1) / 2, y0 + 40, 'radius (the rim is at 1)', 12, INK2, 'middle')
    return fx, fy
def curve(cid, fx, fy, f, dash=None, colour=INK, title=''):
    out.append('<polyline id="%s" points="%s" fill="none" stroke="%s" stroke-width="2"%s><title>%s</title></polyline>' % (cid, ' '.join('%.1f,%.1f' % (fx(r), fy(f(r))) for r in GR), colour, ' stroke-dasharray="%s"' % dash if dash else '', title))
def dots(cls, fx, fy, vals, colour, what):
    for r, v in zip(RAD, vals): out.append('<circle class="%s" cx="%.2f" cy="%.2f" r="4" fill="%s" stroke="%s" stroke-width="1.5"><title>%s, radius %.2f: %.2f</title></circle>' % (cls, fx(r), fy(v), colour, SURF, what, r, v))
def key(x, y, colour, label, line=False, dash=None):
    if line: out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"%s/>' % (x, y, x + 22, y, colour, ' stroke-dasharray="%s"' % dash if dash else '')); T(x + 28, y + 4, label, 12, INK2)
    else: out.append('<circle class="key" cx="%d" cy="%d" r="4" fill="%s"/>' % (x + 4, y, colour)); T(x + 14, y + 4, label, 12, INK2)
# left
fx, fy = plate('left', 60, 'A ring\'s mean depth, cloud to cloud', 'Its variance across 2,000 clouds of a million points.', 18.0, (0, 3, 6, 9, 12, 15, 18), '%d')
curve('pred-chance', fx, fy, lambda r: th.annulus(th.cov_chance, r, r, N) if 0.01 < r < 0.99 else th.cov_chance(r, r, N), title='predicted, number of points left to chance: 0.1630 D n^(1/3) (1 - r^(2/3))')
curve('pred-exact', fx, fy, lambda r: th.annulus(th.cov_fixed, r, r, N) if 0.01 < r < 0.99 else th.cov_fixed(r, r, N), title='predicted, exactly n points')
dots('chance', fx, fy, J['chance'], BLUE, 'number left to chance'); dots('exact', fx, fy, J['exact'], ORANGE, 'exactly a million points')
key(60, 76, BLUE, 'number of points left to chance'); key(60, 96, ORANGE, 'exactly a million'); key(190, 96, INK, 'predicted', line=True)
T(fx(0.44), fy(th.cov_chance(0.44, 0.44, N)) - 14, 'left to chance', 11, INK2); T(fx(0.30), fy(th.cov_fixed(0.30, 0.30, N)) + 26, 'exactly a million', 11, INK2)
out.append('</g>')
# middle
fx, fy = plate('middle', 425, 'Depth round a ring: its spread', 'Variance about the ring\'s own mean; exactly a million.', 50.0, (0, 10, 20, 30, 40, 50), '%d')
curve('pred-round', fx, fy, lambda r: th.local(r, N, mmax=400), title='predicted: twice the sum of the parts')
curve('level', fx, fy, lambda r: 0.65 * math.sqrt(0.75 * th.ALPHA * (N / math.pi) ** (2 / 3.0) * th.u(r)), dash='6 4', colour=MUTED, title='what the level problem\'s law would give: 0.65 x sqrt(depth)')
dots('round', fx, fy, J['round'], BLUE, 'variance round the ring')
key(425, 76, BLUE, 'measured'); key(505, 76, INK, 'predicted', line=True); key(425, 96, MUTED, 'the level problem\'s law, for contrast', line=True, dash='6 4')
out.append('</g>')
# right
fx, fy = plate('right', 790, 'The ripples round a ring, one by one', 'Mean square of the part with 1, 2, 3 waves round.', 7.0, (0, 1, 2, 3, 4, 5, 6, 7), '%d')
for i, m in enumerate((1, 2, 3)):
    curve('pred-part%d' % m, fx, fy, lambda r, m=m: th.mode(m, r, N), title='predicted, %d round: dies as r^(%d/3) on the way in' % (m, m * m)); dots('part%d' % m, fx, fy, J['parts'][str(m)], RAMP[i], '%d round' % m)
    key(790 + i * 62, 76, RAMP[i], '%d round' % m)
key(790 + 3 * 62, 76, INK, 'predicted', line=True)
T(fx(0.33), fy(th.mode(1, 0.30, N)) - 12, '1 round', 11, INK2); T(fx(0.52), fy(th.mode(2, 0.5, N)) - 12, '2', 11, INK2); T(fx(0.70), fy(th.mode(3, 0.7, N)) - 11, '3', 11, INK2)
out.append('</g></svg>')
open(os.path.join(HERE, 'disc.svg'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('disc.svg: %d bytes; 19 radii; left %d + %d dots, middle %d, right %d' % (len('\n'.join(out)), len(J['chance']), len(J['exact']), len(J['round']), 3 * 19))
