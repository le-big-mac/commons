"""Referee: direction-resolved analysis of footstep maps, for both implementations.

For each run prints
  - per edge: mean path of A->B and of B->A (footstep-weighted perpendicular offset in bins along the edge),
    their largest separation, separation at mid-route, and the share of footsteps on common cells
  - per gate: how far from the gate the two OUTBOUND routes stay together, and how far the two INBOUND routes do
"""
import sys
import numpy as np

NB = 50


def load(fn):
    """-> gates (3,2), h, dict {(a,b): (x, y, w)} of footstep clouds, scalar extras"""
    d = np.load(fn)
    out = {}
    if 'foot6' in d.files:                                # Noon's instrumented copy: [iy, ix], nodes at lo + i h
        h = float(d['h']); lo = d['lo']; gates = d['gates']
        for k, (a, b) in enumerate(d['pairs']):
            F = d['foot6'][k]
            iy, ix = np.nonzero(F)
            out[(int(a), int(b))] = (lo[0] + ix * h, lo[1] + iy * h, F[iy, ix])
        det = float(d['detour'])
    else:                                                 # referee's blind code: [ix, iy], cell centres
        h = float(d['h']); x0 = float(d['x0']); y0 = float(d['y0'])
        gates = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])
        P = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]
        for k, (a, b) in enumerate(P):
            F = d['foot'][k]
            ix, iy = np.nonzero(F)
            out[(a, b)] = (x0 + (ix + 0.5) * h, y0 + (iy + 0.5) * h, F[ix, iy])
        det = float(d['mean_detour'])
    return gates, h, out, det, float(d['cap'])


def profile(cloud, A, B, C):
    """footstep-weighted mean and sd of the perpendicular offset (positive towards C) in NB bins of s along A->B"""
    x, y, w = cloud
    ax = (B - A) / np.linalg.norm(B - A)
    nr = np.array([-ax[1], ax[0]])
    if np.dot(C - A, nr) < 0:
        nr = -nr
    s = ((x - A[0]) * ax[0] + (y - A[1]) * ax[1]) / np.linalg.norm(B - A)
    p = (x - A[0]) * nr[0] + (y - A[1]) * nr[1]
    b = np.floor(s * NB).astype(int)
    ok = (b >= 0) & (b < NB)
    sw = np.bincount(b[ok], w[ok], NB); sp = np.bincount(b[ok], w[ok] * p[ok], NB); sp2 = np.bincount(b[ok], w[ok] * p[ok] ** 2, NB)
    mu = sp / np.maximum(sw, 1e-12)
    sd = np.sqrt(np.maximum(sp2 / np.maximum(sw, 1e-12) - mu ** 2, 0))
    return mu, sd


def overlap(c1, c2, h, mask=None):
    """share of footsteps (each map normalised to 1) falling on common cells: sum of min(p1, p2)"""
    def key(c):
        return np.round(c[0] / h).astype(int) * 100000 + np.round(c[1] / h).astype(int)
    k1, k2 = key(c1), key(c2)
    w1, w2 = c1[2].astype(float), c2[2].astype(float)
    if mask is not None:
        m1, m2 = mask(c1), mask(c2)
        k1, w1, k2, w2 = k1[m1], w1[m1], k2[m2], w2[m2]
    w1 = w1 / w1.sum(); w2 = w2 / w2.sum()
    d1 = dict(zip(k1.tolist(), w1.tolist()))
    return sum(min(v, d1.get(k, 0.0)) for k, v in zip(k2.tolist(), w2.tolist()))


def together(c1, c2, g, h, tol_cells=2.0, rmax=0.6, dr=0.02):
    """distance from gate g up to which the footstep centroids of two routes (in rings round g) stay within tol"""
    def cent(c, r0):
        r = np.hypot(c[0] - g[0], c[1] - g[1])
        m = (r >= r0) & (r < r0 + dr)
        if c[2][m].sum() <= 0:
            return None
        return np.array([np.average(c[0][m], weights=c[2][m]), np.average(c[1][m], weights=c[2][m])])
    r0 = dr
    while r0 < rmax:
        a, b = cent(c1, r0), cent(c2, r0)
        if a is None or b is None or np.hypot(*(a - b)) > tol_cells * h:
            return r0
        r0 += dr
    return rmax


def analyse(fn, verbose=True):
    gates, h, cl, det, cap = load(fn)
    res = dict(cap=cap, det=det)
    seps_mid, seps_max, ovs, ovmids, skew = [], [], [], [], []
    for a, b in [(0, 1), (0, 2), (1, 2)]:
        c = 3 - a - b
        A, B, C = gates[a], gates[b], gates[c]
        mu_f, sd_f = profile(cl[(a, b)], A, B, C)
        mu_b, sd_b = profile(cl[(b, a)], A, B, C)
        d = np.abs(mu_f - mu_b)
        mid = slice(NB // 2 - 1, NB // 2 + 1)
        seps_mid.append(d[mid].mean()); seps_max.append(d[3:-3].max())
        ovs.append(overlap(cl[(a, b)], cl[(b, a)], h))
        ax = (B - A) / np.linalg.norm(B - A)
        def midhalf(cc, A=A, ax=ax, Lab=np.linalg.norm(B - A)):
            s = ((cc[0] - A[0]) * ax[0] + (cc[1] - A[1]) * ax[1]) / Lab
            return (s > 0.25) & (s < 0.75)
        ovmids.append(overlap(cl[(a, b)], cl[(b, a)], h, midhalf))
        # skewness of each path in its own direction of travel: offset at 1/4 of the way minus offset at 3/4 of the way
        q1, q3 = NB // 4, 3 * NB // 4
        skew.append((mu_f[q1] - mu_f[q3], mu_b[q3] - mu_b[q1]))
        res[f'mu_{a}{b}'] = mu_f; res[f'mu_{b}{a}'] = mu_b
    out_tog, in_tog = [], []
    for g in range(3):
        o = [k for k in range(3) if k != g]
        out_tog.append(together(cl[(g, o[0])], cl[(g, o[1])], gates[g], h))
        in_tog.append(together(cl[(o[0], g)], cl[(o[1], g)], gates[g], h))
    res.update(sep_mid=np.mean(seps_mid), sep_max=np.mean(seps_max), ov=np.mean(ovs), ovmid=np.mean(ovmids),
               skew=np.array(skew), out_tog=np.array(out_tog), in_tog=np.array(in_tog),
               seps_max=np.array(seps_max), ovs=np.array(ovs))
    if verbose:
        print(f"{fn.split('/')[-1]:34s} cap {cap:.1f} detour {det:.4f} | out vs back: sep at mid-route {res['sep_mid']:.4f}, largest sep {res['sep_max']:.4f} "
              f"({res['sep_max'] / h:.1f} cells; per edge {np.round(res['seps_max'], 3)}), common-cell share {res['ov']:.3f} (middle half {res['ovmid']:.3f}) | "
              f"offset at 1/4 minus at 3/4 of own journey {np.round(res['skew'].mean(), 4)} | "
              f"two OUTBOUND routes together for {np.round(res['out_tog'], 2)} from the gate; two INBOUND for {np.round(res['in_tog'], 2)}")
    return res


if __name__ == '__main__':
    for fn in sys.argv[1:]:
        analyse(fn)
