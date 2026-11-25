"""Blind part B: global search over directions (dense grid + refinement), Q2 and Q6."""
import math, sys
from decimal import Decimal as D
import numpy as np
from scipy.optimize import minimize
from ref import h_dec, h_float, h_vec

out = open('/home/agent2/float/referee/blindB.out', 'w')


def P(*a):
    s = ' '.join(str(x) for x in a)
    print(s); out.write(s + '\n'); out.flush()


def fold(n):
    a = sorted((abs(float(x)) for x in n), reverse=True)
    nm = math.sqrt(sum(x * x for x in a))
    return tuple(x / nm for x in a)


def kind(u, tol=2e-5):
    a, b, c = u
    if b < tol and c < tol: return 'face'
    if abs(a - b) < tol and c < tol: return 'edge'
    if abs(a - b) < tol and abs(b - c) < tol: return 'corner'
    if c < tol: return 'tilted, one comp 0 (plane through face normals)'
    if abs(b - c) < tol: return 'tilted, two smaller comps equal (diagonal plane, face side)'
    if abs(a - b) < tol: return 'tilted, two larger comps equal (diagonal plane, edge side)'
    return 'lopsided'


def tangent(u):
    u = np.array(u, float)
    t = np.array([0.0, 0.0, 1.0]) if abs(u[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    e1 = np.cross(u, t); e1 /= np.linalg.norm(e1)
    e2 = np.cross(u, e1)
    return e1, e2


def circle_test(u, d, r, m=36):
    """min over m directions at angular radius r of h - h(u), Decimal arithmetic."""
    e1, e2 = tangent(u)
    h0 = h_dec([D(float(x)) for x in u], D(str(d)))
    worst = None
    for k in range(m):
        ang = 2 * math.pi * k / m
        v = np.array(u) * math.cos(r) + math.sin(r) * (math.cos(ang) * e1 + math.sin(ang) * e2)
        dh = h_dec([D(float(x)) for x in v], D(str(d))) - h0
        if worst is None or dh < worst:
            worst = dh
    return float(worst)


def search(d, step=0.005, nrand=60, seed=1):
    g = np.arange(-0.05, 1.05, step) + 0.37 * step
    Pg, Qg = np.meshgrid(g, g, indexing='ij')
    H = h_vec(np.ones_like(Pg), Pg, Qg, d)
    C = H[1:-1, 1:-1]
    m = np.ones(C.shape, bool)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if (di, dj) != (0, 0):
                m &= C <= H[1 + di:H.shape[0] - 1 + di, 1 + dj:H.shape[1] - 1 + dj]
    ii, jj = np.nonzero(m)
    starts = [(float(Pg[i + 1, j + 1]), float(Qg[i + 1, j + 1])) for i, j in zip(ii, jj)]
    gridmin = float(H.min())
    ngrid = len(starts)
    # thin the starts (ring gives many)
    if len(starts) > 60:
        idx = np.linspace(0, len(starts) - 1, 60).astype(int)
        starts = [starts[i] for i in idx]
    rng = np.random.default_rng(seed)
    for _ in range(nrand):
        v = np.abs(rng.normal(size=3)); v = np.sort(v)[::-1]
        starts.append((v[1] / v[0], v[2] / v[0]))
    f = lambda x: h_float((1.0, x[0], x[1]), d)
    found = []
    for s in starts:
        r = minimize(f, s, method='Nelder-Mead', options=dict(xatol=1e-11, fatol=1e-16, maxiter=4000, initial_simplex=[s, (s[0] + 0.01, s[1]), (s[0], s[1] + 0.01)]))
        u = fold((1.0, r.x[0], r.x[1]))
        hv = h_float(u, d)
        for k, (u2, h2, cnt) in enumerate(found):
            if max(abs(u[i] - u2[i]) for i in range(3)) < 3e-5:
                found[k] = (u2, h2, cnt + 1)
                break
        else:
            found.append((u, hv, 1))
    found.sort(key=lambda t: t[1])
    return found, gridmin, ngrid


if __name__ == '__main__':
    dens = [float(x) for x in sys.argv[1:]] or [0.10, 0.20, 0.215, 0.22, 0.225, 0.23, 0.30, 0.40, 0.50]
    for d in dens:
        found, gridmin, ngrid = search(d)
        hf, he, hc = h_float((1, 0, 0), d), h_float((1, 1, 0), d), h_float((1, 1, 1), d)
        P("\n=== d = %g : face %.12f  edge %.12f  corner %.12f ; grid(0.005) min %.12f ; %d grid local minima" % (d, hf, he, hc, gridmin, ngrid))
        if len(found) > 12:
            hs = [t[1] for t in found]
            P("   %d distinct end points; h range %.15f .. %.15f (a continuum?)" % (len(found), min(hs), max(hs)))
            tilt = [math.degrees(math.acos(t[0][0])) for t in found if t[1] < min(hs) + 1e-9]
            P("   tilt from face among those within 1e-9 of lowest: %.6f .. %.6f deg (n=%d)" % (min(tilt), max(tilt), len(tilt)))
            show = found[:3] + [t for t in found if kind(t[0]) in ('face', 'edge', 'corner')]
        else:
            show = found
        for u, hv, cnt in show:
            c3 = circle_test(u, d, 1e-3); c5 = circle_test(u, d, 1e-5)
            P("   up=(%.9f, %.9f, %.9f) h=%.13f  hits=%d  %-28s  min dh on circle r=1e-3: %+.3e, r=1e-5: %+.3e -> %s" % (
                u[0], u[1], u[2], hv, cnt, kind(u), c3, c5, 'LOCAL MIN' if (c3 > 0 and c5 > 0) else ('degenerate/flat' if (c3 > -1e-13 and c5 > -1e-17) else 'not a min')))
    out.close()
