# Referee's blind computation. Own geometry: polygon clip of a rotated rectangle by y <= 0.
import math, sys
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import solve_ivp

D = 917.0 / 1025.0


def sub(e, th, yc):
    """Area and centroid (lab frame) of the part of the rectangle below y = 0.
    Rectangle width e, height 1, centre (0, yc), rotated counter-clockwise by th."""
    c, s = math.cos(th), math.sin(th)
    P = [(u * c - v * s, u * s + v * c + yc) for u, v in
         ((-e / 2, -0.5), (e / 2, -0.5), (e / 2, 0.5), (-e / 2, 0.5))]
    Q = []
    for i in range(4):
        x1, y1 = P[i]
        x2, y2 = P[(i + 1) % 4]
        if y1 <= 0:
            Q.append((x1, y1))
        if (y1 <= 0) != (y2 <= 0):
            t = y1 / (y1 - y2)
            Q.append((x1 + t * (x2 - x1), 0.0))
    n = len(Q)
    if n < 3:
        return 0.0, 0.0, 0.0
    A = cx = cy = 0.0
    for i in range(n):
        x1, y1 = Q[i]
        x2, y2 = Q[(i + 1) % n]
        w = x1 * y2 - x2 * y1
        A += w
        cx += (x1 + x2) * w
        cy += (y1 + y2) * w
    A *= 0.5
    if abs(A) < 1e-300:
        return 0.0, 0.0, 0.0
    return A, cx / (6 * A), cy / (6 * A)


def float_at(e, th):
    """Height of centre so that submerged area = D*e; returns yc, h, xb."""
    R = 0.5 * math.hypot(e, 1.0)
    yc = brentq(lambda y: sub(e, th, y)[0] - D * e, -R, R, xtol=1e-15, rtol=1e-15)
    A, cx, cy = sub(e, th, yc)
    return yc, yc - cy, cx


def h(e, th):
    return float_at(e, th)[1]


def xb(e, th):
    return float_at(e, th)[2]


def minima(e, lo=0.0, hi=90.0, n=1801):
    """Local minima of h on [lo, hi] degrees, ends included; grid then refine."""
    ths = np.linspace(lo, hi, n)
    hs = np.array([h(e, math.radians(t)) for t in ths])
    out = []
    for i in range(n):
        l = hs[i - 1] if i > 0 else math.inf
        r = hs[i + 1] if i < n - 1 else math.inf
        if hs[i] < l and hs[i] < r:
            if 0 < i < n - 1:
                res = minimize_scalar(lambda t: h(e, math.radians(t)), bounds=(ths[i - 1], ths[i + 1]),
                                      method='bounded', options={'xatol': 1e-9})
                out.append((res.x, res.fun))
            else:
                out.append((ths[i], hs[i]))
    return out


def main():
    o = []
    P = lambda *a: (o.append(' '.join(str(x) for x in a)), print(*a))
    P('d =', D)
    # check: dh/dtheta = -xb ?
    e, t = 0.6, math.radians(23.0)
    dh = (h(e, t + 1e-6) - h(e, t - 1e-6)) / 2e-6
    P('check dh/dth', dh, ' -xb', -xb(e, t))

    # 1. thresholds. upright stable iff h(delta) > h(0); side stable iff h(90-delta) > h(90)
    dl = 2e-4
    f0 = lambda e: h(e, dl) - h(e, 0.0)
    e_up = brentq(f0, 0.6, 0.9, xtol=1e-12)
    f90 = lambda e: h(e, math.pi / 2 - dl) - h(e, math.pi / 2)
    e_side = brentq(f90, 1.1, 1.6, xtol=1e-12)
    P('1. upright stable for e >', round(e_up, 5), ' analytic sqrt(6d(1-d)) =', round(math.sqrt(6 * D * (1 - D)), 5))
    P('1. on side stable for e <', round(e_side, 5), ' analytic 1/sqrt(6d(1-d)) =', round(1 / math.sqrt(6 * D * (1 - D)), 5))
    # same via the sign of the slope of xb (delta 1e-5)
    g0 = lambda e: -xb(e, 1e-5)
    P('1b. upright via xb slope:', round(brentq(g0, 0.6, 0.9, xtol=1e-12), 6))
    g90 = lambda e: xb(e, math.pi / 2 - 1e-5)
    P('1b. side via xb slope:', round(brentq(g90, 1.1, 1.6, xtol=1e-12), 6))

    # 2. stable tilt at e = 0.745
    ms = minima(0.745)
    P('2. minima of h at e=0.745 (deg, h):', [(round(a, 4), round(b, 6)) for a, b in ms])

    # 3. smallest e with a stable tilt strictly in (0, 80).  g = dh/dth = -xb.  Lean branch: g<0 below the
    # minimum, >0 above it, <0 again past the maximum.  It ends where max of g over (0,80) falls to 0.
    def gmax(e, full=False):
        ths = np.linspace(0.5, 80.0, 1591)
        gs = np.array([-xb(e, math.radians(t)) for t in ths])
        i = int(np.argmax(gs))
        a, b = ths[max(i - 1, 0)], ths[min(i + 1, len(ths) - 1)]
        res = minimize_scalar(lambda t: xb(e, math.radians(t)), bounds=(a, b), method='bounded',
                              options={'xatol': 1e-10})
        return (res.x, -res.fun) if full else -res.fun
    for e in (0.72, 0.73, 0.735, 0.736, 0.737, 0.74):
        P('   e', e, 'argmax,max of dh/dth on (0.5,80):', gmax(e, True))
    e_fold = brentq(gmax, 0.72, 0.75, xtol=1e-10)
    th_fold, gm = gmax(e_fold, True)
    P('3. smallest e with a stable interior tilt:', round(e_fold, 6), ' tilt there (deg):', round(th_fold, 3), 'resid', gm)
    for de in (1e-5, 1e-4, 5e-4):
        P('   minima at e_fold +', de, ':', [(round(a, 4), round(b, 7)) for a, b in minima(e_fold + de)])
    P('   minima at e_fold - 1e-5:', [(round(a, 4), round(b, 7)) for a, b in minima(e_fold - 1e-5)])
    # tilt at which the top corner goes under, as function of e on the lean branch
    def corner_gap(e):
        m = [a for a, b in minima(e) if 0.01 < a < 80]
        if not m:
            return None
        t = math.radians(m[0])
        yc = float_at(e, t)[0]
        # highest corner on the low side: body point (-e/2, +1/2) or (e/2, 1/2); take min y of top corners
        ys = [u * math.sin(t) + 0.5 * math.cos(t) + yc for u in (-e / 2, e / 2)]
        return m[0], min(ys)
    for e in (0.7521, 0.75, 0.745, 0.74, 0.739, 0.738, 0.7375, 0.737, 0.7365, 0.7364, e_fold + 1e-6):
        P('   e', round(e, 6), 'lean tilt, height of lower top corner above water:', corner_gap(e))
    # e at which the lower top corner is exactly at the water on the lean branch
    try:
        ec = brentq(lambda e: corner_gap(e)[1], e_fold + 1e-6, 0.75, xtol=1e-9)
        P('   top corner reaches the water on the lean branch at e =', round(ec, 6), 'tilt', round(corner_gap(ec)[0], 4))
    except Exception as ex:
        P('   corner crossing not bracketed:', ex)

    # 4. energy set free
    ms = minima(0.5)
    P('4. minima of h at e=0.5:', [(round(a, 4), round(b, 7)) for a, b in ms])
    E = {}
    multi = []
    for k in range(5, 71):
        e = k / 100.0
        m = minima(e, n=361)
        if len(m) != 1 or abs(m[0][0] - 90) > 1e-6:
            multi.append((e, m))
        hend = min(m, key=lambda z: z[1])[1] if len(m) > 1 else m[0][1]
        E[e] = e * (h(e, 0.0) - h(e, math.pi / 2))
    P('4. energy at e=0.5:', E[0.5], ' formula (1-d)e(1-e)/2 =', (1 - D) * 0.25 / 2)
    eb = max(E, key=E.get)
    P('4. greatest at e =', eb, 'value', E[eb], ' neighbours', E[0.49], E[0.51])
    P('4. e in 0.05..0.70 where the minima are not just {90}:', multi)

    # dynamics
    def run(e, th0deg=1.0, T=40.0, rtol=1e-11, atol=1e-13):
        M = e
        I = M * (e * e + 1) / 12.0
        th0 = math.radians(th0deg)
        y0 = float_at(e, th0)[0]

        def rhs(t, s):
            y, th, vy, w = s
            A, cx, cy = sub(e, th, y)
            return [vy, w, (A / D - M) / M, cx * A / D / I]

        def energy(s):
            y, th, vy, w = s
            A, cx, cy = sub(e, th, y)
            return 0.5 * M * vy * vy + 0.5 * I * w * w + M * y - A * cy / D

        ev = lambda t, s: s[1] - math.pi / 2
        ev.direction = 1
        sol = solve_ivp(rhs, (0, T), [y0, th0, 0, 0], method='DOP853', rtol=rtol, atol=atol,
                        events=ev, dense_output=True, max_step=0.02)
        ts = np.linspace(0, T, 40001)
        S = sol.sol(ts)
        i = int(np.argmax(S[1]))
        t90 = sol.t_events[0][0] if len(sol.t_events[0]) else None
        E0, E1 = energy(S[:, 0]), energy(S[:, -1])
        return t90, math.degrees(S[1].max()), ts[i], math.degrees(S[1].min()), E1 - E0, S, ts

    t90, thmax, tmax, thmin, dE, S, ts = run(0.5)
    P('5. e=0.5: tilt first reaches 90 deg at t =', t90)
    P('6. e=0.5: greatest tilt in first 40 =', thmax, 'deg at t =', tmax, '; least tilt', thmin, '; energy drift', dE)
    P('   y range of the centre:', S[0].min(), S[0].max(), ' start y', S[0, 0])
    # looser tolerance as a control
    t90b, thmaxb, *_ = run(0.5, rtol=1e-8, atol=1e-10)
    P('   control rtol 1e-8: t90', t90b, 'max tilt', thmaxb)
    for a0 in (0.1, 0.5, 2.0, 5.0):
        r = run(0.5, th0deg=a0)
        P('   first tilt', a0, 'deg: t90', r[0], 'max tilt', r[1])
    open(sys.argv[1], 'w').write('\n'.join(o) + '\n')


if __name__ == '__main__':
    main()
