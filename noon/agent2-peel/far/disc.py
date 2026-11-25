"""disc.py: the equation of the addition carried over to the disc of finding 2.   python -I disc.py
The referee did this with a pencil in its second step (referee/report.md, item 5), as "a test and not a result"; I went through
each step with my own pencil and set it against the discs of the first study (../runs). It was worked out with those discs'
figures on the page, so it is not a prediction; but nothing in it is adjusted.
A disc of radius 1 with n points has density rho = n / pi. Where the front is a circle of radius r, the cell problem's unit of
length along the front is a = (r / rho)^(1/3) and across it b = a^2 / r (a parabola of the circle's curvature holds one point
in a by b). (1) Each b of radius adds alpha layers: the count is the integral of alpha dr / b = (3/4) alpha rho^(2/3).
(2) The mean depth round the ring, which is 2 pi r / a units long, gains variance D for each unit of height over that length:
D (dr / b) / (2 pi r / a) = D dr / (2 pi a), which sums to (3 / (4 pi)) D rho^(1/3). At the centre the ring has shrunk to
nothing, so that is the variance of the count: 0.1630 D n^(1/3), for clouds whose number of points is left to chance.
(3) My discs have exactly n points. Of D, the part (4/9) alpha^2 is the count of points (finding 8): a point at radius r adds
c r^(-2/3) layers to the count, with c the same for all. With the points independent the variance of what one point adds is
its mean square, 3 c^2; with their number fixed it is that less the square of its mean, 3 c^2 - (3/2)^2 c^2 = (3/4) c^2: a
quarter. So for clouds of exactly n points the variance of the count should be 0.1630 x [D - (3/4)(4/9) alpha^2] x n^(1/3)."""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__)); ALPHA = 1.3259
R = []
for name in ('discs-small.jsonl', 'large.jsonl'):
    R += [json.loads(l) for l in open(os.path.join(HERE, '..', 'runs', name)) if l.strip()]
R = [r for r in R if r['shape'] == 'disc']
geo = 3 / (4 * math.pi) * math.pi ** (-1 / 3.0); dens = 4 / 9.0 * ALPHA ** 2
print('the factor (3 / (4 pi)) pi^(-1/3) = %.4f; the part of D that is the count of points, (4/9) alpha^2 = %.3f; three quarters of it %.3f' % (geo, dens, 0.75 * dens))
print('the count itself by (1): (3/4) x 1.3259 x (n / pi)^(2/3) = %.0f at n = 10^8 (the discs: 99,880)' % (0.75 * ALPHA * (1e8 / math.pi) ** (2 / 3.0)))
for D, label in ((1.073, 'D = 1.073, as measured'), (1.081, 'D = 1.081, with the two small corrections')):
    print('%s: the variance of the count should be %.4f n^(1/3) for clouds of exactly n points (%.4f with the measured 0.757 for the count\'s part), and %.4f n^(1/3) if the number of points were left to chance' % (
        label, geo * (D - 0.75 * dens), geo * (D - 0.75 * 0.757), geo * D))
pred = geo * (1.073 - 0.75 * dens)
print('\n        n   clouds   variance of the count   over n^(1/3) (its standard error)   over the predicted %.4f' % pred)
num = den = 0; chi = 0; k = 0
for n in sorted(set(r['n'] for r in R)):
    v = [r['layers'] for r in R if r['n'] == n]; m = sum(v) / len(v); var = sum((x - m) ** 2 for x in v) / (len(v) - 1); q = var / n ** (1 / 3.0); se = q * math.sqrt(2.0 / (len(v) - 1))
    print('%9d   %5d   %10.3f              %.4f (%.4f)                    %.2f' % (n, len(v), var, q, se, q / pred))
    sp = pred * math.sqrt(2.0 / (len(v) - 1)); chi += ((q - pred) / sp) ** 2; k += 1; num += q / se ** 2 * 0 + (len(v) - 1) * q; den += (len(v) - 1)
print('weighing each size by its number of clouds, the variance over n^(1/3) is %.4f; predicted %.4f. (D is good to about 0.06, one standard error, from the resampling of study.out; so the prediction to about %.3f, 12 in 100.)' % (num / den, pred, geo * 0.06))
print('if the prediction were exact, the scatter of the %d sizes about it would have a chi-square of %.1f on %d' % (k, chi, k))
