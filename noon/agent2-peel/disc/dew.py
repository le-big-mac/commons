"""dew.py: the formulas of dtheory.py tried on the equation itself, and on points thrown in a disc.   python -I dew.py
dtheory.py says what the equation dT/d(-r) = (1/(3r)) T'' + noise of strength N r^(-1/3) (for each unit of angle and of radius)
gives at radius r, started level at the rim: the variance of the ring's mean, the mean squares of the parts that go as cos and sin of
m times the angle, and the variance round the ring. I worked those out with a pencil. Here the equation is simply stepped inward
on a ring of 256 places (nothing of dtheory is used in the stepping), 1,600 times over, and the same things are measured.
And the rule for clouds of exactly n points (a point at radius s adds s^(-2/3) to every ring inside it) is tried by throwing points."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dtheory as th
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail else ''))
# units in which D rho^(1/3) = 1: then dtheory's mode() is g_m / (2 pi) and the ring's mean has variance g_0 / (2 pi)
M, REPS = 256, 1600; dth = 2 * math.pi / M; rng = np.random.default_rng(11); T = np.zeros((REPS, M)); r = 1.0; marks = [0.9, 0.7, 0.5, 0.3, 0.1]; got = {}
theta = np.arange(M) * dth
while r > 0.1 - 1e-12:
    dr = min(0.2 * 3 * r * dth * dth, r - marks[0] if marks else 1.0, 2e-4)               # small enough for the stepping to be stable
    if dr <= 0: dr = 1e-9
    T += dr / (3 * r) * (np.roll(T, 1, axis=1) + np.roll(T, -1, axis=1) - 2 * T) / (dth * dth) + np.sqrt(r ** (-1 / 3.0) * dr / dth) * rng.standard_normal((REPS, M)); r -= dr
    if marks and r <= marks[0] + 1e-12:
        mean = T.mean(axis=1); loc = float(((T - mean[:, None]) ** 2).mean()); parts = {}
        for m in (1, 2, 3, 4):
            c = 2 * (T * np.cos(m * theta)).mean(axis=1); s = 2 * (T * np.sin(m * theta)).mean(axis=1); parts[m] = float(((c ** 2 + s ** 2) / 4).mean())
        got[marks[0]] = (float(mean.var()), loc, parts); marks.pop(0)
worst_mean = worst_loc = worst_part = 0
for rr in (0.9, 0.7, 0.5, 0.3, 0.1):
    vm, loc, parts = got[rr]; wm = th.g(0, rr) / (2 * math.pi)
    lam = [(2 - 2 * math.cos(m * dth)) / (dth * dth) for m in range(1, M)]          # on a ring of M places the m-th part dies as r^(lam/3), lam a little under m^2 for the high parts
    wl = sum(1.5 * (rr ** (2 / 3.0) - rr ** (2 * l / 3.0)) / (l - 1) for l in lam) / (2 * math.pi)
    worst_mean = max(worst_mean, abs(vm / wm - 1)); worst_loc = max(worst_loc, abs(loc / wl - 1)); worst_part = max(worst_part, max(abs(parts[m] / (th.g(m, rr) / (2 * math.pi)) - 1) for m in (1, 2, 3, 4)))
    print('   r = %.1f: ring\'s mean %.4f against %.4f; round the ring %.4f against %.4f; parts 1 to 4: %s against %s' % (rr, vm, wm, loc, wl, ', '.join('%.4f' % parts[m] for m in (1, 2, 3, 4)), ', '.join('%.4f' % (th.g(m, rr) / (2 * math.pi)) for m in (1, 2, 3, 4))))
ok('the equation stepped inward on a ring, 1,600 times: the variance of the ring\'s mean is within %.0f in 100 of (3/2)(1 - r^(2/3)) / (2 pi) at r = 0.9, 0.7, 0.5, 0.3 and 0.1 (1,600 rings: a variance good to 3.5 in 100)' % (100 * worst_mean), worst_mean < 0.10)
ok('   the variance round the ring is within %.1f in 100 of the sum of the parts\' formulas over the 255 parts a ring of 256 places holds (each dying at the rate the ring of places gives it)' % (100 * worst_loc), worst_loc < 0.03)
ok('   the first four parts are each within %.0f in 100 of g_m(r) / (2 pi) at the five radii (3,200 samples of each: good to 2.5 in 100)' % (100 * worst_part), worst_part < 0.08)
ok('   and the sum of all the parts near the rim is the level problem\'s formula: at r = 0.999, %.4f against sqrt(3 x 0.001 / (2 pi)) = %.4f' % (th.local(0.999, math.pi, d=1.0), math.sqrt(3 * 0.001 / (2 * math.pi))), abs(th.local(0.999, math.pi, d=1.0) / math.sqrt(3 * 0.001 / (2 * math.pi)) - 1) < 0.01)
# clouds of exactly n points, and of a number left to chance: sum over the points outside radius r of s^(-2/3)
n, trials = 500, 40000; rng = np.random.default_rng(5)
def sums(counts):
    out = np.zeros((len(counts), 2))
    for i, k in enumerate(counts):
        s = np.sqrt(rng.random(k)); f = s ** (-2 / 3.0); out[i] = (f[s > 0.8].sum(), f[s > 0.3].sum())
    return out
ex = sums([n] * trials); ch = sums(rng.poisson(n, trials)); ce = np.cov(ex.T); cc = np.cov(ch.T)
want_e = lambda r1, r2: n * (3 * th.tau(max(r1, r2)) - 2.25 * th.u(r1) * th.u(r2)); want_c = lambda r1, r2: n * 3 * th.tau(max(r1, r2))
re_ = [ce[0, 0] / want_e(0.8, 0.8), ce[1, 1] / want_e(0.3, 0.3), ce[0, 1] / want_e(0.8, 0.3)]; rc_ = [cc[0, 0] / want_c(0.8, 0.8), cc[1, 1] / want_c(0.3, 0.3), cc[0, 1] / want_c(0.8, 0.3)]
ok('points thrown in a disc, 40,000 times: with the number left to chance the variances and the covariance of the sums outside 0.8 and 0.3 are %s of n x 3 (1 - s^(2/3)), s the larger radius' % ', '.join('%.3f' % x for x in rc_), all(abs(x - 1) < 0.04 for x in rc_))
ok('   with exactly n points they are %s of n x [3 (1 - s^(2/3)) - (9/4) u(r1) u(r2)]' % ', '.join('%.3f' % x for x in re_), all(abs(x - 1) < 0.05 for x in re_))
ok('   and dtheory\'s two covariances are those rules with n c^2 = D_count rho^(1/3) / (4 pi): at (0.8, 0.3), n = 10^6, %.4f and %.4f' % (th.cov_chance(0.8, 0.3, 1e6, d=th.DC), th.cov_fixed(0.8, 0.3, 1e6, d=th.DC)),
   abs(th.cov_chance(0.8, 0.3, 1e6, d=th.DC) / (th.DC * (1e6 / math.pi) ** (1 / 3.0) / (4 * math.pi) * 3 * th.tau(0.8)) - 1) < 1e-12 and abs(th.cov_fixed(0.8, 0.3, 1e6, d=th.DC) / (th.DC * (1e6 / math.pi) ** (1 / 3.0) / (4 * math.pi) * (3 * th.tau(0.8) - 2.25 * th.u(0.8) * th.u(0.3))) - 1) < 1e-12)
ok('the numbers printed in the sheet are dtheory\'s: 11.54, 6.48, 2.40; 4.09, 3.01, 1.77; 0.505 and 0.187; 24.0, 25.0, 22.3; 5.13, 2.78, 1.35; 0.0648; 11.6',
   ['%.2f' % th.annulus(th.cov_chance, x, x, 1e6) for x in (0.2, 0.5, 0.8)] == ['11.54', '6.48', '2.40'] and ['%.2f' % th.annulus(th.cov_fixed, x, x, 1e6) for x in (0.2, 0.5, 0.8)] == ['4.09', '3.01', '1.77']
   and ['%.1f' % th.local(x, 1e6) for x in (0.3, 0.5, 0.7)] == ['24.0', '25.0', '22.3'] and ['%.2f' % th.mode(m, 0.5, 1e6) for m in (1, 2, 3)] == ['5.13', '2.78', '1.35'] and '%.4f' % (th.annulus(th.cov_chance, 0.5, 0.5, 1e6) / 100) == '0.0648' and '%.1f' % th.local(0.5, 1e5) == '11.6')
print('\n%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
