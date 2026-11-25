# last step: the author's corner family through my own wedge solver (flow7.py's solve, copied):
# equilateral triangle, inradius 1; across each corner R = d (1 - s cos 3th - t cos 6th - u cos 9th), th from a side's normal
import numpy as np, sys, math, time
def solve(k, pfun, m, s=0.5, rstop=0.03):
    W = math.pi / k; th = np.linspace(0, W, m + 1); dth = W / m; p = pfun(th)
    wt = np.ones(m + 1); wt[0] = wt[-1] = 0.5; wt *= dth * 2 * k; i2 = 1.0 / dth ** 2
    def L(f):
        g = np.empty_like(f)
        g[1:-1] = (f[2:] - 2 * f[1:-1] + f[:-2]) * i2 + f[1:-1]
        g[0] = 2 * (f[1] - f[0]) * i2 + f[0]; g[-1] = 2 * (f[-2] - f[-1]) * i2 + f[-1]
        return g
    R = L(p); A0 = 0.5 * np.sum(wt * p * R); t = 0.0; Rs = []; dts = []; Rmin0 = R[1:].min(); R0 = R.copy()
    while True:
        R = L(p)
        if R.min() <= 0: raise SystemExit('R<=0')
        A = 0.5 * np.sum(wt * p * R)
        if A < rstop ** 2 * A0: break
        dt = s * 1.5 * dth ** 2 * R.min() ** (4 / 3); Rs.append(R.astype(np.float32)); dts.append(dt)
        p = p - dt * R ** (-1 / 3); t += dt
    T = t + 0.75 * (A / math.pi) ** (2 / 3)
    w = R / (2 * math.pi * (A / math.pi) ** (1 / 3)); I = 3 * A ** (1 / 3) / (4 * math.pi ** (4 / 3))
    for n in range(len(dts) - 1, -1, -1):
        Rn = Rs[n].astype(np.float64); a = Rn ** (-4 / 3) / 3
        w = w + dts[n] * L(a * w); I += dts[n] * np.sum(wt * w * w * 3 * a)
    return T, A0, I * A0 / T ** 2, R0
d, s, t, u = [float(v) for v in sys.argv[1:5]]; m = int(sys.argv[5]); t0 = time.time()
f = lambda th: 2 * np.cos(th - math.pi / 3) + d * (1 + s / 8 * np.cos(3 * th) + t / 35 * np.cos(6 * th) + u / 80 * np.cos(9 * th))
T, A0, Q, R0 = solve(3, f, m)
print('d=%-9g s=%-7g t=%-7g u=%-7g m=%4d  R beside a side %.3f, a quarter across %.3f, at the tip %.3f, least %.3f  T over the disc\'s %.5f  Q=%.5f  %.0fs' % (
    d, s, t, u, m, R0[1], R0[m // 4], R0[-1], R0[1:].min(), T * (math.pi / A0) ** (2 / 3) / 0.75, Q, time.time() - t0), flush=True)
