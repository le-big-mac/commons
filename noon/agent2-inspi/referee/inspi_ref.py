#!/usr/bin/env python
"""Referee's own INSPI program, written from the rule only:
   repeat: FORWARD 1; RIGHT ANGLE; ANGLE += INC.
Turning is kept in exact whole degrees.  Positions are sums of unit vectors
(double precision; tolerance TOL for 'at the starting point'), and every
'position is zero / is not zero' decision at a state return is ALSO made
exactly, by reducing the heading-count polynomial modulo the 360th cyclotomic
polynomial (whole-number arithmetic)."""
import numpy as np, math, json, sys, time
from collections import Counter, defaultdict
from scipy.spatial import ConvexHull

TOL = 1e-9
U = np.exp(-1j * np.pi * np.arange(360) / 180.0)   # RIGHT = clockwise


def pdiv(num, den):
    num = list(num); out = []; n = len(den)
    for i in range(len(num) - n + 1):
        c = num[i]; out.append(c)
        if c:
            for j in range(n):
                num[i + j] -= c * den[j]
    return out, num[len(num) - n + 1:]


def cyclo(n, cache={}):
    if n in cache:
        return cache[n]
    num = [1] + [0] * (n - 1) + [-1]
    for d in range(1, n):
        if n % d == 0:
            num, rem = pdiv(num, cyclo(d))
            assert not any(rem)
    cache[n] = num
    return num


def reduction_table():
    PHI = cyclo(360)
    deg = len(PHI) - 1
    assert deg == 96
    low = PHI[::-1]
    R = np.zeros((360, deg), dtype=np.int64)
    r = [0] * deg; r[0] = 1
    for h in range(360):
        R[h] = r
        top = r[-1]
        r = [0] + r[:-1]
        if top:
            r = [r[i] - top * low[i] for i in range(deg)]
    assert r == [1] + [0] * (deg - 1)          # x^360 = 1 mod PHI
    return R


def exact_zero(R, headings_mod):
    c = np.bincount((-headings_mod) % 360, minlength=360).astype(np.int64)
    return not np.any(c @ R)


def simulate(inc, ang, N):
    k = np.arange(N, dtype=np.int64)
    turns = ang + k * inc                       # turn made after step k+1
    H = np.concatenate(([0], np.cumsum(turns)))  # H[n]: heading after n steps
    P = np.concatenate(([0j], np.cumsum(U[H[:-1] % 360])))  # P[n]: position after n steps
    return H, P


def diameter(pts, brute=False):
    z = pts
    if not brute and len(z) > 40:
        try:
            hull = ConvexHull(np.column_stack((z.real, z.imag)))
            z = z[hull.vertices]
        except Exception:
            z = pts
    d = np.abs(z[:, None] - z[None, :])
    return float(d.max())


def main():
    t0 = time.time()
    R = reduction_table()
    rows = []
    rng = np.random.default_rng(20261126)
    brute_checks = 0; brute_maxdiff = 0.0
    q6_hits = []
    for inc in range(1, 360):
        for ang in range(0, 360):
            N = 1440
            while True:
                H, P = simulate(inc, ang, N)
                n = np.arange(1, N + 1)
                ok = ((n * inc) % 360 == 0) & (H[1:] % 360 == 0)
                if ok.any():
                    n0 = int(n[np.argmax(ok)])
                    break
                assert N < 129600 * 2
                N *= 4
            D = P[n0]
            home = abs(D) < TOL
            ex = exact_zero(R, H[:n0] % 360)
            assert ex == home, (inc, ang, abs(D))
            rec = dict(inc=inc, ang=ang, n0=n0, home=bool(home), absD=float(abs(D)))
            if home:
                pts = P[1:n0 + 1]
                rec['diam'] = diameter(pts)
                if rng.random() < 0.004:
                    b = diameter(pts, brute=True)
                    brute_checks += 1
                    brute_maxdiff = max(brute_maxdiff, abs(b - rec['diam']))
                mid = np.abs(P[1:n0])
                at0 = np.nonzero(mid < TOL)[0] + 1
                rec['early_start_visits'] = int(len(at0))
                for m in at0:
                    if H[m] % 360 == 0:
                        q6_hits.append((inc, ang, int(m)))
                rec['mindist'] = float(mid.min()) if len(mid) else None
            else:
                M = int(math.ceil(n0 / abs(D))) + 2
                N2 = n0 * M
                H2, P2 = simulate(inc, ang, N2)
                # translation check
                mm = np.arange(0, M + 1)
                assert np.max(np.abs(P2[mm * n0] - mm * D)) < 1e-8
                a = np.abs(P2[1:])
                i = int(np.argmin(a))
                rec['mindist'] = float(a[i]); rec['mindist_step'] = i + 1
                rec['mindist_heading'] = int(H2[i + 1] % 360)
                rec['checked_steps'] = N2
                at0 = np.nonzero(a < TOL)[0] + 1
                rec['early_start_visits'] = int(len(at0))
                for m in at0:
                    if H2[m] % 360 == 0:
                        q6_hits.append((inc, ang, int(m)))
            rows.append(rec)
    out = dict(rows=rows, q6_hits=q6_hits, brute_checks=brute_checks,
               brute_maxdiff=brute_maxdiff, seconds=time.time() - t0, tol=TOL)
    json.dump(out, open(sys.argv[1], 'w'))
    print('done', len(rows), 'pairs in', round(time.time() - t0, 1), 's')


if __name__ == '__main__':
    main()
