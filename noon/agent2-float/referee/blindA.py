"""Blind part A: thresholds (Q1, Q4abc), Q3 ring at 0.22, Q5 edge up."""
import math, sys
from decimal import Decimal as D
import numpy as np
from ref import h_dec, h_float

out = open('/home/agent2/float/referee/blindA.out', 'w')


def P(*a):
    s = ' '.join(str(x) for x in a)
    print(s); out.write(s + '\n'); out.flush()


S2, S3, S6 = D(2).sqrt(), D(3).sqrt(), D(6).sqrt()


def bis(test, lo, hi, it=50):
    """test(lo) != test(hi); returns the switching point."""
    tl = test(lo)
    assert tl != test(hi), (tl, lo, hi)
    for _ in range(it):
        mid = (lo + hi) / 2
        if test(mid) == tl:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------- Q1 square ----------
def sq_flat_min(d, eps=D('1e-8')):
    return h_dec((1, eps), d) > h_dec((1, 0), d)


def sq_corner_min(d, eps=D('1e-8')):
    return h_dec((1, 1 - eps), d) > h_dec((1, 1), d)


P("Q1 square: scan of local-min status (d: flat, corner)")
row = []
for i in range(4, 101):
    d = D(i) / 200
    row.append((float(d), sq_flat_min(d), sq_corner_min(d)))
chg = [row[0]] + [row[i] for i in range(1, len(row)) if row[i][1:] != row[i - 1][1:]]
for r in chg:
    P("   status changes at/after d=%.3f: flat=%s corner=%s" % r)
a = bis(sq_flat_min, D('0.15'), D('0.25'))
b = bis(sq_corner_min, D('0.25'), D('0.30'))
P("Q1 square flat local min up to d = %.12f   ((3-sqrt3)/6 = %.12f)" % (a, (3 - S3) / 6))
P("Q1 square corner local min from d = %.12f   (9/32 = %.12f)" % (b, D(9) / 32))

# ---------- Q4 cube thresholds ----------
E1 = (D(1) / S2, D(-1) / S2, D(0))
E2 = (D(1) / S6, D(1) / S6, D(-2) / S6)


def ring_dirs(center, e1, e2, r, m):
    """m directions at angular radius ~r around center (center unit, e1,e2 orthonormal tangent)."""
    res = []
    for k in range(m):
        ang = 2 * math.pi * k / m
        c, s = D(math.cos(ang)), D(math.sin(ang))
        res.append(tuple(center[i] + r * (c * e1[i] + s * e2[i]) for i in range(3)))
    return res


def cube_face_min(d, r=D('1e-8'), m=12):
    h0 = h_dec((1, 0, 0), d)
    return all(h_dec(n, d) > h0 for n in ring_dirs((D(1), D(0), D(0)), (D(0), D(1), D(0)), (D(0), D(0), D(1)), r, m))


CORNER = (1 / S3, 1 / S3, 1 / S3)


def cube_corner_min(d, r=D('1e-8'), m=12):
    h0 = h_dec((1, 1, 1), d)
    return all(h_dec(n, d) > h0 for n in ring_dirs(CORNER, E1, E2, r, m))


EDGE = (1 / S2, 1 / S2, D(0))


def cube_edge_curv(d, r=D('1e-6')):
    """second differences at edge up: along roll (1,-1,0) and along (0,0,1) towards a corner."""
    h0 = h_dec((1, 1, 0), d)
    a = h_dec((1 + r, 1 - r, 0), d)          # tilt angle ~ r
    b = h_dec((1, 1, r * S2), d)             # tilt angle ~ r
    return (a - h0) / (r * r) * 2, (b - h0) / (r * r) * 2


P("\nQ4 cube: scan of local-min status, step 0.005 (tiny radius 1e-8 rad, 12 directions)")
row = []
for i in range(4, 101):
    d = D(i) / 200
    row.append((float(d), cube_face_min(d), cube_corner_min(d)))
chg = [row[0]] + [row[i] for i in range(1, len(row)) if row[i][1:] != row[i - 1][1:]]
for r in chg:
    P("   status changes at/after d=%.3f: face=%s corner=%s" % r)
fa = bis(cube_face_min, D('0.15'), D('0.25'))
P("Q4a cube face up local min up to d = %.12f" % fa)
for r in ('1e-2', '1e-3', '1e-4', '1e-6', '1e-8'):
    cb = bis(lambda d: cube_corner_min(d, D(r), 36), D('0.12'), D('0.20'))
    fb = bis(lambda d: cube_face_min(d, D(r), 36), D('0.15'), D('0.25'))
    P("   test radius %s rad, 36 dirs: face-up threshold %.10f   corner-up threshold %.10f  (1/6 = 0.1666666667)" % (r, fb, cb))


def corner_vs_face(d):
    return h_dec((1, 1, 1), d) < h_dec((1, 0, 0), d)


c = bis(corner_vs_face, D('0.17'), D('0.30'))
P("Q4c corner up lower than face up from d = %.12f ; h there = %.12f" % (c, h_dec((1, 1, 1), c)))

# ---------- Q3 ring at 0.22 ----------
P("\nQ3 cube d=0.22: least h over theta<30deg at fixed azimuth (Decimal golden section after scan)")
d = D('0.22')
T30 = 1 / S3
cs = {0: (D(1), D(0)), 15: ((S6 + S2) / 4, (S6 - S2) / 4), 30: (S3 / 2, D(1) / 2), 45: (S2 / 2, S2 / 2)}
GR = (D(5).sqrt() - 1) / 2
for phi in (0, 15, 30, 45):
    c_, s_ = cs[phi]
    f = lambda t: h_dec((1, t * c_, t * s_), d)
    # scan in theta
    best = None
    N = 300
    vals = []
    for i in range(N + 1):
        th = math.radians(30.0) * i / N
        vals.append(h_float((1, math.tan(th) * float(c_), math.tan(th) * float(s_)), 0.22))
    locmins = [i for i in range(1, N) if vals[i] <= vals[i - 1] and vals[i] <= vals[i + 1]]
    i0 = min(range(N + 1), key=lambda i: vals[i])
    lo = D(math.tan(math.radians(30.0) * max(i0 - 1, 0) / N)); hi = D(math.tan(math.radians(30.0) * min(i0 + 1, N) / N))
    x1 = hi - GR * (hi - lo); x2 = lo + GR * (hi - lo); f1, f2 = f(x1), f(x2)
    for _ in range(110):
        if f1 < f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - GR * (hi - lo); f1 = f(x1)
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + GR * (hi - lo); f2 = f(x2)
    t = (lo + hi) / 2
    P("   phi=%2d: theta = %.9f deg  (tan^2 = %.12f)  h = %.12f   [grid local minima at theta(deg): %s; h(30deg)=%.9f]" % (
        phi, math.degrees(math.atan(float(t))), t * t, f(t), [round(30.0 * i / N, 2) for i in locmins], vals[N]))
P("   formula: tan^2 = 12d(1-d)-2 = %.12f, theta = %.9f deg, h = sqrt(12d(1-d)-1)/(12d) = %.12f ; face up h = %.12f" % (
    12 * d * (1 - d) - 2, math.degrees(math.atan(math.sqrt(float(12 * d * (1 - d) - 2)))), (12 * d * (1 - d) - 1).sqrt() / (12 * d), (1 - d) / 2))

# ---------- Q5 edge up ----------
P("\nQ5 cube edge up: curvature (2nd derivative per rad^2) along roll (1,-1,0) and towards corner (0,0,1)")
anymin = []
for i in list(range(4, 101, 4)) + [99, 100]:
    d = D(i) / 200
    ca, cb_ = cube_edge_curv(d)
    P("   d=%.3f  roll %+.6f   towards-corner %+.6f" % (d, ca, cb_))
neg = True
worst = None
for i in range(20, 501):
    d = D(i) / 1000
    ca, cb_ = cube_edge_curv(d)
    if ca > 0 and cb_ > 0:
        anymin.append(float(d))
    if worst is None or min(ca, cb_) > worst[1]:
        worst = (float(d), min(ca, cb_))
P("   densities 0.020..0.500 step 0.001 where both curvatures > 0:", anymin)
P("   largest (least negative) of min-curvature: d=%.3f value %.3e" % worst)
P("   at d=0.5 towards corner, h(eps)-h(0) for up=(1,1,eps*sqrt2) (tilt angle ~eps), and ratio to eps^3:")
h0 = h_dec((1, 1, 0), D('0.5'))
for e in ('1e-1', '1e-2', '1e-3', '1e-4', '1e-6'):
    e = D(e)
    dh = h_dec((1, 1, e * S2), D('0.5')) - h0
    P("      eps=%s  dh=%.6e  dh/eps^2=%.6e  dh/eps^3=%.8f   (predicted -1/24 = %.8f)" % (e, dh, dh / e / e, dh / e ** 3, -1 / 24))
P("   at d=0.5: roll curvature %.9f; h(edge)=%.12f h(corner)=%.12f h(face)=%.12f" % (
    cube_edge_curv(D('0.5'))[0], h0, h_dec((1, 1, 1), D('0.5')), h_dec((1, 0, 0), D('0.5'))))
P("   at d=0.499, 0.4999: towards-corner curvature %.6e, %.6e" % (cube_edge_curv(D('0.499'))[1], cube_edge_curv(D('0.4999'))[1]))
out.close()
