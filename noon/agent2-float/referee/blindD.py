"""Blind part D: robust 2-D search for all local minima (grid 0.004 in gnomonic coords + Nelder-Mead),
using a float evaluation that does not suffer cancellation near degenerate directions."""
import math, sys
from decimal import Decimal as D
import numpy as np
from scipy.optimize import minimize
from ref import h_dec, h_float, h_vec
from blindB import fold, kind, circle_test

out = open('/home/agent2/float/referee/blindD.out', 'a')


def P(*a):
    s = ' '.join(str(x) for x in a)
    print(s); out.write(s + '\n'); out.flush()


def h_rob(n, d):
    a, b, c = sorted((abs(float(x)) for x in n), reverse=True)
    p, q = b / a, c / a
    if p + q <= 2 * min(d, 1 - d):        # water plane cuts the four upright edges only: exact, no cancellation
        return (1 / math.sqrt(1 + p * p + q * q)) * ((1 - d) / 2 + (p * p + q * q) / (24 * d))
    if c == 0.0:
        return h_float((a, b), d)
    if p * q < 2e-3:
        return float(h_dec((D(a), D(b), D(c)), D(d)))
    return h_float((a, b, c), d)


def search(d, step=0.004, nrand=30, seed=1, maxgrid=40):
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
    gridmin = float(H.min()); ngrid = len(starts)
    k = np.unravel_index(np.argmin(H), H.shape)
    gridarg = fold((1.0, float(Pg[k]), float(Qg[k])))
    if len(starts) > maxgrid:
        idx = np.linspace(0, len(starts) - 1, maxgrid).astype(int)
        starts = [starts[i] for i in idx]
    rng = np.random.default_rng(seed)
    for _ in range(nrand):
        v = np.sort(np.abs(rng.normal(size=3)))[::-1]
        starts.append((v[1] / v[0], v[2] / v[0]))
    f = lambda x: h_rob((1.0, x[0], x[1]), d)
    found = []
    for s in starts:
        r = minimize(f, s, method='Nelder-Mead', options=dict(xatol=1e-9, fatol=1e-15, maxiter=800,
                     initial_simplex=[s, (s[0] + 0.01, s[1]), (s[0], s[1] + 0.01)]))
        u = fold((1.0, r.x[0], r.x[1]))
        hv = h_rob(u, d)
        for kk, (u2, h2, cnt) in enumerate(found):
            if max(abs(u[i] - u2[i]) for i in range(3)) < 2e-4:
                found[kk] = (u2, h2, cnt + 1)
                break
        else:
            found.append((u, hv, 1))
    found.sort(key=lambda t: t[1])
    return found, gridmin, gridarg, ngrid


if __name__ == '__main__':
    for d in [float(x) for x in sys.argv[1:]]:
        found, gridmin, gridarg, ngrid = search(d)
        P("\n=== d = %g : face %.12f edge %.12f corner %.12f ; grid(0.004) min %.12f at (%.4f,%.4f,%.4f); %d grid local minima; %d distinct end points" % (
            d, h_rob((1, 0, 0), d), h_rob((1, 1, 0), d), h_rob((1, 1, 1), d), gridmin, *gridarg, ngrid, len(found)))
        tie = math.sqrt(max(12 * d * (1 - d) - 1, 0)) / (12 * d)
        ties = [t for t in found if abs(t[1] - tie) < 5e-13 and t[0][1] / t[0][0] + t[0][2] / t[0][0] <= 2 * d + 1e-9]
        if ties:
            az = [math.degrees(math.atan2(t[0][2], t[0][1])) for t in ties]
            P("   %d end points on the exact-tie set (h=%.12f, tilt %.5f deg), azimuths %.2f..%.2f deg" % (
                len(ties), tie, math.degrees(math.acos(ties[0][0][0])), min(az), max(az)))
        for u, hv, cnt in found:
            if (u, hv, cnt) in ties:
                continue
            c3 = circle_test(u, d, 1e-3, 24); c5 = circle_test(u, d, 1e-5, 24)
            P("   up=(%.9f, %.9f, %.9f) h=%.12f hits=%d %s | min dh on circle r=1e-3: %+.2e, r=1e-5: %+.2e -> %s" % (
                u[0], u[1], u[2], hv, cnt, kind(u, 1e-6), c3, c5, 'local min' if (c3 > 0 and c5 > 0) else 'NOT a strict min'))
    out.close()
