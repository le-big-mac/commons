# Referee's own solver: affine curve shortening flow in support-function form,
#   p_t = -(p + p'')^(-1/3)   (theta = direction of the outward normal, R = p + p'' = radius of curvature)
# on a symmetric wedge [th0, th0+W] with mirror symmetry at both ends, plus the
# backward (adjoint) equation for the sensitivity G of the vanishing time T:
#   dT = sum over the front of G * (area pushed out),  w = G R,  w_t = -(a w + (a w)''),  a = R^(-4/3)/3
# Outputs T, I = integral over K of G^2 dA, both scaled to area pi, and Q = I A / T^2.
import numpy as np, sys, math, time

def p0(shape, th, eps):
    if shape in ('triangle', 'square', 'hexagon', 'rtriangle', 'disc'):
        k = {'triangle': 3, 'square': 4, 'hexagon': 6, 'rtriangle': 3, 'disc': 3}[shape]
        if shape == 'disc':
            return np.ones_like(th), k
        if shape == 'rtriangle':
            return 2.0 * np.cos(th - math.pi / 3) + 0.25, k   # inradius 1, swollen by 1/4
        # sharp polygon, inradius 1, corners rounded INWARD with radius eps (area loss O(eps^2))
        return (1 - eps) / math.cos(math.pi / k) * np.cos(th - math.pi / k) + eps, k
    if shape == 'halfdisc':   # {x>=0, x^2+y^2<=1}, th in [0, pi]
        yc = math.sqrt((1 - eps) ** 2 - eps ** 2); thc = math.atan2(yc, eps)
        p = np.where(th <= thc, 1 - eps, eps * np.cos(th) + yc * np.sin(th)) + eps
        return p, 1
    if shape == 'quarter':    # {x,y>=0, x^2+y^2<=1}, th in [pi/4, 5pi/4]
        yc = math.sqrt((1 - eps) ** 2 - eps ** 2); thc = math.atan2(yc, eps)
        v1 = eps * np.cos(th) + yc * np.sin(th); v2 = eps * np.cos(th) + eps * np.sin(th)
        p = np.where(th <= thc, 1 - eps, np.maximum(v1, v2)) + eps
        return p, 1
    raise SystemExit('shape?')

def solve(shape, m, eps, s=0.5, rstop=0.03):
    k = {'triangle': 3, 'square': 4, 'hexagon': 6, 'rtriangle': 3, 'disc': 3}.get(shape, 1)
    W = math.pi / k
    th0 = math.pi / 4 if shape == 'quarter' else 0.0
    th = th0 + np.linspace(0, W, m + 1); dth = W / m
    p, k = p0(shape, th, eps); pinit = p.copy()
    wt = np.ones(m + 1); wt[0] = wt[-1] = 0.5; wt *= dth * 2 * k
    i2 = 1.0 / dth ** 2
    def L(f):
        g = np.empty_like(f)
        g[1:-1] = (f[2:] - 2 * f[1:-1] + f[:-2]) * i2 + f[1:-1]
        g[0] = 2 * (f[1] - f[0]) * i2 + f[0]
        g[-1] = 2 * (f[-2] - f[-1]) * i2 + f[-1]
        return g
    R = L(p)
    if shape in ('halfdisc', 'quarter', 'triangle', 'square', 'hexagon'):
        R = np.maximum(R, eps * 0.999)        # rounding error in the corner arcs only
    A0 = 0.5 * np.sum(wt * p * R)
    t = 0.0; Rs = []; dts = []
    A = A0
    while True:
        R = L(p)
        if R.min() <= 0:
            raise SystemExit('R<=0 at t=%g step %d' % (t, len(dts)))
        A = 0.5 * np.sum(wt * p * R)
        if A < rstop ** 2 * A0:
            break
        dt = s * 1.5 * dth ** 2 * R.min() ** (4 / 3)
        Rs.append(R.astype(np.float32)); dts.append(dt)
        p = p - dt * R ** (-1 / 3)
        t += dt
    T = t + 0.75 * (A / math.pi) ** (2 / 3)
    ecc = R.max() / R.min()
    # adjoint, backward
    g = 1.0 / (2 * math.pi * (A / math.pi) ** (1 / 3))
    w = g * R
    I = 3 * A ** (1 / 3) / (4 * math.pi ** (4 / 3))
    Ilow = I       # the lower bound: integral of dt / Omega
    chk = 0.0
    for n in range(len(dts) - 1, -1, -1):
        Rn = Rs[n].astype(np.float64)
        a = Rn ** (-4 / 3) / 3
        w = w + dts[n] * L(a * w)
        I += dts[n] * np.sum(wt * w * w * 3 * a)
        Om = np.sum(wt * Rn ** (2 / 3))
        Ilow += dts[n] / Om
        c = np.sum(wt * w * Rn ** (-1 / 3))
        chk = max(chk, abs(c - 1))
    sc = math.pi / A0
    return dict(shape=shape, m=m, eps=eps, steps=len(dts), A0=A0, T=T * sc ** (2 / 3), I=I * sc ** (1 / 3),
                Q=I * A0 / T ** 2, Qlow=Ilow * A0 / T ** 2, chk=chk, ecc=ecc, euler=float(np.sum(wt * w * pinit) / (4 * T / 3)), edge=float(w[0] * wt[0] * 2 if shape != "quarter" else 0),
                gmin=float((w / Rs[0]).min() * A0 ** (1 / 3)), gmax=float((w / Rs[0]).max() * A0 ** (1 / 3)))

if __name__ == '__main__':
    shape = sys.argv[1]; m = int(sys.argv[2]); eps = float(sys.argv[3])
    t0 = time.time()
    r = solve(shape, m, eps)
    print('%-9s m=%4d eps=%-7g steps=%8d A0=%.6f T=%.6f I=%.6f Q=%.5f Qlow=%.5f chk=%.1e ecc=%.4f g0[%.4f,%.4f] %.0fs' % (
        r['shape'], r['m'], r['eps'], r['steps'], r['A0'], r['T'], r['I'], r['Q'], r['Qlow'], r['chk'], r['ecc'],
        r['gmin'], r['gmax'], time.time() - t0), flush=True)
    print('   Euler test: (sum over the start curve of G p ds) / (4T/3) = %.5f   [1 if the adjoint is right];  A0*G_edge/(2T/3)=%.5f' % (r['euler'], r['edge'] * 0 + (r['edge'] / (2 * math.pi / {'triangle': 3, 'square': 4, 'hexagon': 6, 'rtriangle': 3, 'disc': 3}.get(shape, 1) ) ) ), flush=True)
