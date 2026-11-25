"""ew.py: the three formulas of the sheet (expectations-2.md) tried on the equation itself.   python -I ew.py
The picture: dT/dy = nu T_xx + noise, the noise independent from place to place and from height to height, of strength D (so that
the mean of T over a stretch of length W, started level, has variance D y / W). The sheet says that then, started level,
  (ii)  the variance of T at a point is D sqrt(y / (2 pi nu)),
  (iii) the mean square difference between two points r apart is twice that times 1 - exp(-s^2) + s sqrt(pi) erfc(s), s = r / sqrt(8 nu y),
        which is half of twice the variance at s = 0.3497, that is at r = 0.5711 sqrt(y) when nu = 1/3 (the sheet, from my pencil, has 0.5715).
I worked these out with a pencil. Here the equation is simply stepped forward on a ring (no formula of mine is used in the stepping:
T_i += nu dt (T_i+1 - 2 T_i + T_i-1) + sqrt(D dt) x a standard normal draw, one site to the unit of length), many times over, and the
three things are measured. Then the same things are measured with nu = 1/3 and D = 1.1, about what the peeling shows."""
import math, sys
import numpy as np
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail else ''))
def shape(s): return 1 - math.exp(-s * s) + s * math.sqrt(math.pi) * math.erfc(s)
lo, hi = 0.0, 2.0
for _ in range(60):
    mid = (lo + hi) / 2
    if shape(mid) < 0.5: lo = mid
    else: hi = mid
SH = (lo + hi) / 2
ok('the shape 1 - exp(-s^2) + s sqrt(pi) erfc(s) is 0 at 0, 1 far out, and one half at s = %.4f; with nu = 1/3 that is r = %.4f sqrt(y)' % (SH, SH * math.sqrt(8 / 3.0)),
   shape(0) == 0 and abs(shape(6) - 1) < 1e-12 and abs(SH - 0.3497) < 5e-5 and abs(SH * math.sqrt(8 / 3.0) - 0.5715) < 5e-4)
ok('0.600 is sqrt(3 / (2 pi 1.3259)) = %.4f' % math.sqrt(3 / (2 * math.pi * 1.3259)), abs(math.sqrt(3 / (2 * math.pi * 1.3259)) - 0.600) < 5e-4)
def simulate(nu, D, L, steps, dt, reps, seed, at):
    rng = np.random.default_rng(seed); T = np.zeros((reps, L)); out = {}
    for n in range(1, steps + 1):
        T += nu * dt * (np.roll(T, 1, axis=1) + np.roll(T, -1, axis=1) - 2 * T) + math.sqrt(D * dt) * rng.standard_normal((reps, L))
        if n in at:
            m = T.mean(axis=1, keepdims=True); var = float(((T - m) ** 2).mean()); zero = float(m.var())
            lags = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256]; g = [float(((np.roll(T, -j, axis=1) - T) ** 2).mean()) for j in lags]
            out[n] = (var, zero, lags, g)
    return out
for nu, D, L, steps, reps, label in ((0.25, 1.0, 1024, 4000, 400, 'nu = 1/4, D = 1'), (1 / 3.0, 1.1, 1024, 4000, 400, 'nu = 1/3, D = 1.1')):
    dt = 0.5; at = (1000, 2000, 4000); res = simulate(nu, D, L, steps, dt, reps, 7, at)
    for n in at:
        y = n * dt; var, zero, lags, g = res[n]; want = D * math.sqrt(y / (2 * math.pi * nu)); wz = D * y / L
        # the sites of a ring L long: the variance about the ring's own mean is the variance at a point less that of the mean
        ok('%s, y = %d: variance at a point (about the ring\'s mean, plus the mean\'s) %.3f against D sqrt(y / (2 pi nu)) = %.3f (ratio %.3f)' % (label, y, var + zero, want, (var + zero) / want), abs((var + zero) / want - 1) < 0.03)
        ok('   the mean of the ring: variance %.4f against D y / L = %.4f (ratio %.2f; %d rings)' % (zero, wz, zero / wz, reps), abs(zero / wz - 1) < 0.25)
        plateau = 2 * (var + zero); i = next(k for k in range(len(g)) if g[k] >= plateau / 2); x0, x1 = math.log(lags[i - 1]), math.log(lags[i])
        rh = math.exp(x0 + (x1 - x0) * (plateau / 2 - g[i - 1]) / (g[i] - g[i - 1])); wr = SH * math.sqrt(8 * nu * y)
        worst = max(abs(g[k] / (2 * want * shape(lags[k] / math.sqrt(8 * nu * y))) - 1) for k in range(len(lags)) if lags[k] >= 16)
        off = [g[k] - 2 * want * shape(lags[k] / math.sqrt(8 * nu * y)) for k in range(len(lags)) if lags[k] <= 12]
        ok('   the reach (half of twice the variance): %.1f against %.4f sqrt(8 nu y) = %.1f (ratio %.3f); the whole curve from 16 to 256 apart is within %.1f in 100 of the formula; nearer than that it stands above the formula by %.2f to %.2f (the grain of the grid, which the formula has not)' % (
            rh, SH, wr, rh / wr, 100 * worst, min(off), max(off)), abs(rh / wr - 1) < 0.05 and worst < 0.05 and 0 < min(off) and max(off) < 0.6 * D)
print('\n%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
