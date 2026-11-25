# Referee, second step: full-circle (no symmetry) version of my support-function solver, for polygons given by
# side normals and support numbers.  Three figures for Q = I A / T^2:
#   (i)  I summed over the inside (my adjoint, as in flow.py)
#   (ii) the author's edge formula (3/2) <g, L^-1 g> with g from MY adjoint at t = 0
#   (iii) the edge formula with g = dT/dh of each side by finite differences of T alone (no adjoint at all)
import numpy as np, math, sys, time

def make(shape):
    if shape == 'cutsq':      # square with a corner cut off, corners (0,0)(1,0)(1,.1)(.1,1)(0,1), doubled, origin inside
        V = np.array([(0, 0), (1, 0), (1, 0.1), (0.1, 1), (0, 1)], float) * 2 - 0.9
        th = []; h = []
        for i in range(len(V)):
            a = V[i]; b = V[(i + 1) % len(V)]; d = b - a; n = np.array([d[1], -d[0]]) / np.hypot(*d)
            th.append(math.atan2(n[1], n[0]) % (2 * math.pi)); h.append(float(n @ a))
    elif shape == 'hex':      # hexagon with an incircle, normals at 0,40,110,170,230,300 degrees
        th = [math.radians(x) for x in (0, 40, 110, 170, 230, 300)]; h = [1.0] * 6
    elif shape == 'square':
        th = [math.radians(x) for x in (0, 90, 180, 270)]; h = [1.0] * 4
    elif shape == 'tri':      # a scalene triangle (control: must be at 4/3)
        th = [math.radians(x) for x in (0, 110, 230)]; h = [1.0] * 3
    o = np.argsort(th); return np.array(th)[o], np.array(h)[o]

def verts(th, h):
    n = len(th); V = []
    for i in range(n):
        j = (i + 1) % n
        Mx = np.array([[math.cos(th[i]), math.sin(th[i])], [math.cos(th[j]), math.sin(th[j])]])
        V.append(np.linalg.solve(Mx, [h[i], h[j]]))
    return np.array(V)

def area_len(th, h):
    V = verts(th, h); n = len(th)
    ell = np.array([np.hypot(*(V[i] - V[i - 1])) for i in range(n)])   # side i runs from V[i-1] to V[i]
    return 0.5 * np.sum(h * ell), ell

def K(x):   # Green's function of 1 + d^2/dtheta^2 on the circle, off cos and sin
    x = np.mod(x, 2 * math.pi)
    return -np.cos(x) / (4 * math.pi) + (math.pi - x) * np.sin(x) / (2 * math.pi)

def forward(th_e, h_e, M, eps, adjoint=False, s=0.5, stop=1e-3):
    th = 2 * math.pi * np.arange(M) / M; dth = 2 * math.pi / M
    V = verts(th_e, h_e - eps)
    p = np.max(V[:, 0:1] * np.cos(th)[None, :] + V[:, 1:2] * np.sin(th)[None, :], axis=0) + eps
    i2 = 1 / dth ** 2
    def L(f):
        g = np.empty_like(f)
        g[1:-1] = (f[2:] - 2 * f[1:-1] + f[:-2]) * i2 + f[1:-1]
        g[0] = (f[1] - 2 * f[0] + f[-1]) * i2 + f[0]
        g[-1] = (f[0] - 2 * f[-1] + f[-2]) * i2 + f[-1]
        return g
    R = L(p); A0 = 0.5 * np.sum(p * R) * dth
    t = 0.0; Rs = []; dts = []
    while True:
        R = L(p)
        if R.min() <= 0:
            raise SystemExit('R<=0 at step %d' % len(dts))
        A = 0.5 * np.sum(p * R) * dth
        if A < stop * A0:
            break
        dt = s * 1.5 * dth ** 2 * R.min() ** (4 / 3)
        if adjoint:
            Rs.append(R.astype(np.float32))
        dts.append(dt)
        p = p - dt * R ** (-1 / 3); t += dt
    T = t + 0.75 * (A / math.pi) ** (2 / 3)
    if not adjoint:
        return T, A0, None, None
    w = R / (2 * math.pi * (A / math.pi) ** (1 / 3))
    I = 3 * A ** (1 / 3) / (4 * math.pi ** (4 / 3))
    for n in range(len(dts) - 1, -1, -1):
        Rn = Rs[n].astype(np.float64); a = Rn ** (-4 / 3) / 3
        w = w + dts[n] * L(a * w)
        I += dts[n] * np.sum(w * w * 3 * a) * dth
    Iedge = 1.5 * (w @ K(th[:, None] - th[None, :]) @ w) * dth * dth
    return T, A0, I, Iedge

if __name__ == '__main__':
    shape = sys.argv[1]; M = int(sys.argv[2]); eps = float(sys.argv[3]); adj = len(sys.argv) > 4 and sys.argv[4] == 'adj'
    t0 = time.time()
    th_e, h_e = make(shape); A, ell = area_len(th_e, h_e)
    T, A0, I, Iedge = forward(th_e, h_e, M, eps, adjoint=adj)
    out = '%-6s M=%5d eps=%-7g A=%.6f (rounded %.6f) T/A^(2/3)*pi^(2/3)=%.6f' % (shape, M, eps, A, A0, T * (math.pi / A) ** (2 / 3))
    if adj:
        out += '  Q inside=%.5f  Q edge(my adjoint)=%.5f (both with the rounded area)' % (I * A0 / T ** 2, Iedge * A0 / T ** 2)
    d = 0.002; gam = []
    for e in range(len(th_e)):
        hp = h_e.copy(); hp[e] += d; hm = h_e.copy(); hm[e] -= d
        gam.append((forward(th_e, hp, M, eps)[0] - forward(th_e, hm, M, eps)[0]) / (2 * d))
    gam = np.array(gam); c = (2 / 3) * T / A; z = gam - c * ell
    KK = K(th_e[:, None] - th_e[None, :])
    Qe = 1.5 * (gam @ KK @ gam) * A / T ** 2; short = -1.5 * (z @ KK @ z) * A / T ** 2
    out += '\n   sides at %s deg; dT/dh over (2T/3A) x length: %s' % (np.round(np.degrees(th_e), 1).tolist(), np.round(gam / (c * ell), 5).tolist())
    out += '\n   Euler sum(gam h)/(4T/3)=%.6f  sum gam cos=%.2e sin=%.2e   Q edge (finite differences of T) = %.6f   shortfall below 4/3 = %.6f   %.0fs' % (
        gam @ h_e / (4 * T / 3), gam @ np.cos(th_e), gam @ np.sin(th_e), Qe, short, time.time() - t0)
    print(out, flush=True)
