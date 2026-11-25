"""ripplecheck.py: two things the referee of the second addition said about the ripples, tried on fresh clouds.   python -I ripplecheck.py
(1) The sheet's ripple is taken from the raw depth, which carries the slope of the profile across the annulus. I had written that the
finite number of points therefore ADDS slope^2 h^2 / (3 x points) to a ripple's mean square (h the half-width). The referee: the
places of the points and their depths are not independent (more points in the outer half of the annulus on one side deepen the inner
half there), the cross term is -(4/3) of that, and the raw ripple is LOWERED by a third of it. Here each cloud's ripples are
computed both ways, from the raw depth and with the profile taken off first, and the difference set beside slope^2 h^2 / (3 points).
(2) A ripple's amplitude is a mean over the annulus, so its mean square should fall short of the single-radius formula by
D rho^(1/3) r^(-1/3) h / (6 pi), the same for every number of waves: the ripples with the profile taken off, at three widths.
400 clouds of exactly 100,000 points (seeds 12000001 on), by ../peel; nothing here is on the sheet."""
import math, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dtheory as th
N, CLOUDS, R, r0 = 100000, 400, 536870912.0, 0.5; A0 = 0.75 * 1.3259 * (N / math.pi) ** (2 / 3.0); G = 4 / 3.0 * A0 * r0 ** (1 / 3.0); HALVES = (0.004, 0.008, 0.016)
def one(i):
    out = subprocess.run([os.path.join(HERE, '..', 'peel'), 'disc', str(N), str(12000000 + i + 1), '-depths', '-'], capture_output=True, text=True).stdout
    a = np.array(out.split('\n', 1)[1].split(), dtype=float).reshape(-1, 3); rho = np.hypot(a[:, 0], a[:, 1]) / R; th_ = np.arctan2(a[:, 1], a[:, 0]); d = a[:, 2]; res = []
    for h in HALVES:
        m = np.abs(rho - r0) <= h; dd = d[m]; t = th_[m]; off = dd - A0 * (1 - rho[m] ** (4 / 3.0)); row = [m.sum()]
        for k in (1, 2, 3, 4):
            c, s = np.cos(k * t), np.sin(k * t)
            raw = ((2 * ((dd - dd.mean()) * c).mean()) ** 2 + (2 * ((dd - dd.mean()) * s).mean()) ** 2) / 4; cl = ((2 * ((off - off.mean()) * c).mean()) ** 2 + (2 * ((off - off.mean()) * s).mean()) ** 2) / 4; row += [raw, cl]
        res.append(row)
    return res
with ThreadPoolExecutor(max_workers=12) as ex: allr = np.array(list(ex.map(one, range(CLOUDS))))        # clouds x widths x (count, raw1, off1, raw2, off2, ...)
print('%d clouds of exactly %d points; the annulus at %.1f. Standard errors from the spread of the clouds.' % (CLOUDS, N, r0))
print('(1) raw ripple less ripple with the profile taken off, over slope^2 h^2 / (3 x points) [I had assumed +1; the referee says -1/3]:')
for j, h in enumerate(HALVES):
    cnt = allr[:, j, 0]; sp = G * G * h * h / (3 * cnt); diff = np.mean([allr[:, j, 1 + 2 * (k - 1)] - allr[:, j, 2 + 2 * (k - 1)] for k in (1, 2, 3, 4)], axis=0)
    print('   half-width %.3f: %.2f (%.2f)      [the slope part is %.4f; about %d points in the annulus]' % (h, diff.mean() / sp.mean(), diff.std(ddof=1) / math.sqrt(CLOUDS) / sp.mean(), sp.mean(), cnt.mean()))
print('(2) ripples with the profile taken off, over the single-radius formula, and over the formula less D rho^(1/3) r^(-1/3) h / (6 pi):')
for j, h in enumerate(HALVES):
    loss = th.D * (N / math.pi) ** (1 / 3.0) * r0 ** (-1 / 3.0) * h / (6 * math.pi); out = []
    for k in (1, 2, 3, 4):
        v = allr[:, j, 2 + 2 * (k - 1)]; out.append('%d: %.3f, %.3f (%.3f)' % (k, v.mean() / th.mode(k, r0, N), v.mean() / (th.mode(k, r0, N) - loss), v.std(ddof=1) / math.sqrt(CLOUDS) / th.mode(k, r0, N)))
    print('   half-width %.3f (the mean over the annulus takes off %.4f):  %s' % (h, loss, ';  '.join(out)))
w = allr[:, 0, 2::2].mean(axis=0) - allr[:, 2, 2::2].mean(axis=0); want = th.D * (N / math.pi) ** (1 / 3.0) * r0 ** (-1 / 3.0) * (0.016 - 0.004) / (6 * math.pi)
print('   narrowest less widest, the four ripples: %s; the formula says %.4f for each' % (', '.join('%.4f' % x for x in w), want))
