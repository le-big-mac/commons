# second sheet, blind: generic symmetric-wedge solver (as flow.py) for: ngon k d | stadium a | lemon f e | cone f e
import numpy as np, sys, math, time
def solve(k, pfun, m, s=0.5, rstop=0.03):
    W = math.pi / k; th = np.linspace(0, W, m + 1); dth = W / m; p = pfun(th)
    wt = np.ones(m + 1); wt[0] = wt[-1] = 0.5; wt *= dth * 2 * k; i2 = 1.0 / dth ** 2
    def L(f):
        g = np.empty_like(f)
        g[1:-1] = (f[2:] - 2 * f[1:-1] + f[:-2]) * i2 + f[1:-1]
        g[0] = 2 * (f[1] - f[0]) * i2 + f[0]; g[-1] = 2 * (f[-2] - f[-1]) * i2 + f[-1]
        return g
    R = L(p); A0 = 0.5 * np.sum(wt * p * R); t = 0.0; Rs = []; dts = []
    while True:
        R = L(p)
        if R.min() <= 0: raise SystemExit('R<=0')
        A = 0.5 * np.sum(wt * p * R)
        if A < rstop ** 2 * A0: break
        dt = s * 1.5 * dth ** 2 * R.min() ** (4 / 3); Rs.append(R.astype(np.float32)); dts.append(dt)
        p = p - dt * R ** (-1 / 3); t += dt
    T = t + 0.75 * (A / math.pi) ** (2 / 3)
    w = R / (2 * math.pi * (A / math.pi) ** (1 / 3)); I = 3 * A ** (1 / 3) / (4 * math.pi ** (4 / 3)); Il = I
    for n in range(len(dts) - 1, -1, -1):
        Rn = Rs[n].astype(np.float64); a = Rn ** (-4 / 3) / 3
        w = w + dts[n] * L(a * w); I += dts[n] * np.sum(wt * w * w * 3 * a); Il += dts[n] / np.sum(wt * Rn ** (2 / 3))
    return T, A0, I * A0 / T ** 2, Il * A0 / T ** 2, len(dts)
kind = sys.argv[1]; x = float(sys.argv[2]); y = float(sys.argv[3]); m = int(sys.argv[4]); t0 = time.time()
if kind == 'ngon':
    k = int(x); f = lambda th: np.cos(th - math.pi / k) / math.cos(math.pi / k) + y
elif kind == 'stadium':      # segment of half-length x swollen by 1
    k = 2; f = lambda th: x * np.cos(th) + 1.0
elif kind in ('lemon', 'cone'):   # hull of a disc of radius 1-y and a point (two points for the lemon), swollen by y; tangent at x*(wedge)
    k = 2 if kind == 'lemon' else 1
    th0 = x * math.pi / k; b = (1 - y) / math.cos(th0); f = lambda th: np.maximum(1 - y, b * np.cos(th)) + y
if kind == 'tri3':       # equilateral triangle (inradius 1) + fans of radius x (1 - y cos 3 theta)
    k = 3; U = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0; f = lambda th: 2 * np.cos(th - math.pi / 3) + x * (1 + y / 8 * np.cos(3 * th) - U / 35 * np.cos(6 * th))
elif kind == 'trihex':   # triangle + x times the inverted triangle, swollen by y
    k = 3; f = lambda th: 2 * np.cos(th - math.pi / 3) + 2 * x * np.cos(th) + y
T, A0, Q, Ql, st = solve(k, f, m)
print('%-8s %-8g %-8g m=%4d steps=%7d area %.5f  T over the disc\'s %.5f  Q=%.5f  Qlow=%.5f  %.0fs' % (kind, x, y, m, st, A0, T * (math.pi / A0) ** (2 / 3) / 0.75, Q, Ql, time.time() - t0), flush=True)
