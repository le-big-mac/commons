# Referee's own solver: radially loaded membrane, density 1+a(r), fixed rim.
# (1) finite-volume tridiagonal solver with gradients (for searching)
# (2) exact piecewise-Bessel matching (for checking)
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.special import jv, yv, jvp, yvp
from scipy.optimize import brentq, linprog

MODES = [(0, 1), (1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]
TARG = np.array([1, 2, 3, 3, 4, 4, 5, 5, 5.0])
NMAX = {0: 3, 1: 2, 2: 2, 3: 1, 4: 1}


class Drum:
    def __init__(self, edges, cells=10):
        # edges: ring boundaries 0=e0<e1<...<eK=1 ; each ring gets `cells` cells
        self.edges = np.asarray(edges, float)
        K = len(edges) - 1
        self.K = K
        self.cells = cells
        f = np.concatenate([np.linspace(edges[j], edges[j + 1], cells + 1)[:-1] for j in range(K)] + [[1.0]])
        self.rm = f[:-1]
        self.rp = f[1:]
        self.hc = self.rp - self.rm
        self.r = 0.5 * (self.rp + self.rm)
        self.ring = np.repeat(np.arange(K), cells)
        self.w = self.edges[1:] ** 2 - self.edges[:-1] ** 2  # mass weight of a ring
        # distance between cell centres
        dc = self.r[1:] - self.r[:-1]
        self.off = -self.rp[:-1] / dc
        d = np.zeros(len(self.r))
        d[:-1] += self.rp[:-1] / dc
        d[1:] += self.rp[:-1] / dc
        d[-1] += 1.0 / (1.0 - self.r[-1])
        self.d0 = d

    def lams(self, a, grad=False):
        rho = 1 + np.asarray(a, float)[self.ring]
        D = self.r * rho * self.hc
        sD = np.sqrt(D)
        e = self.off / (sD[:-1] * sD[1:])
        lam = {}
        g = {}
        for m in range(5):
            d = (self.d0 + m * m * self.hc / self.r) / D
            n = NMAX[m]
            if grad:
                wv, v = eigh_tridiagonal(d, e, select='i', select_range=(0, n - 1))
                for i in range(n):
                    lam[(m, i + 1)] = wv[i]
                    g[(m, i + 1)] = -wv[i] * (v[:, i] ** 2 / rho).reshape(self.K, self.cells).sum(1)
            else:
                wv = eigh_tridiagonal(d, e, eigvals_only=True, select='i', select_range=(0, n - 1))
                for i in range(n):
                    lam[(m, i + 1)] = wv[i]
        return (lam, g) if grad else lam

    def miss(self, a, grad=False):
        if grad:
            lam, g = self.lams(a, True)
        else:
            lam = self.lams(a)
        l0 = lam[(0, 1)]
        rat = np.array([np.sqrt(lam[k] / l0) for k in MODES])
        mis = rat[1:] / TARG[1:] - 1
        if not grad:
            return mis
        J = np.array([(rat[i] / TARG[i]) * 0.5 * (g[MODES[i]] / lam[MODES[i]] - g[(0, 1)] / l0) for i in range(1, 9)])
        return mis, J


def exact_freqs(edges, a, guesses=None, cells=40):
    """Exact frequencies by Bessel matching; brackets from a fine finite-volume solve."""
    edges = np.asarray(edges, float)
    a = np.asarray(a, float)
    # merge equal neighbours to keep conditioning good
    E = [edges[0]]
    A = []
    for j in range(len(a)):
        if A and a[j] == A[-1]:
            E[-1] = edges[j + 1]
        else:
            A.append(a[j])
            E.append(edges[j + 1])
    E = np.array(E)
    A = np.array(A)
    E[0] = 0.0
    dr = Drum(edges, cells)
    lam = dr.lams(a)
    out = {}
    for (m, n) in MODES:
        def f(om):
            k = om * np.sqrt(1 + A[0])
            c = np.array([1.0, 0.0])
            for j in range(len(A)):
                k = om * np.sqrt(1 + A[j])
                r1 = E[j + 1]
                x = k * r1
                u = c[0] * jv(m, x) + c[1] * yv(m, x)
                du = k * (c[0] * jvp(m, x) + c[1] * yvp(m, x))
                if j + 1 < len(A):
                    k2 = om * np.sqrt(1 + A[j + 1])
                    x2 = k2 * r1
                    Mx = np.array([[jv(m, x2), yv(m, x2)], [k2 * jvp(m, x2), k2 * yvp(m, x2)]])
                    c = np.linalg.solve(Mx, [u, du])
                    s = np.abs(c).max()
                    c = c / s
            return u
        om0 = np.sqrt(lam[(m, n)])
        lo, hi = om0 * (1 - 3e-3), om0 * (1 + 3e-3)
        flo, fhi = f(lo), f(hi)
        if flo * fhi > 0:
            lo, hi = om0 * (1 - 2e-2), om0 * (1 + 2e-2)
            flo, fhi = f(lo), f(hi)
        if flo * fhi > 0:
            out[(m, n)] = np.nan
        else:
            out[(m, n)] = brentq(f, lo, hi, xtol=1e-13, rtol=1e-13)
    return out, {k: np.sqrt(v) for k, v in lam.items()}


def exact_miss(edges, a, cells=40):
    ex, fv = exact_freqs(edges, a, cells=cells)
    r = np.array([ex[k] / ex[(0, 1)] for k in MODES])
    rf = np.array([fv[k] / fv[(0, 1)] for k in MODES])
    return np.abs(r[1:] / TARG[1:] - 1).max(), r, np.abs(rf[1:] / TARG[1:] - 1).max(), ex


def slp(dr, b0, M, mono=False, maxit=400, tlim=None, t0=None, amax=None):
    """Sequential LP with trust region for min max|miss|; variables are ring masses b=a*w."""
    import time
    K = dr.K
    w = dr.w
    b = np.clip(np.array(b0, float), 0, None)
    if b.sum() > M:
        b *= M / b.sum()
    mis, J = dr.miss(b / w, True)
    J = J / w
    f = np.abs(mis).max()
    Delta = 0.1 * max(M, 0.1)
    c = np.zeros(K + 1)
    c[-1] = 1
    for it in range(maxit):
        if tlim is not None and time.time() - t0 > tlim:
            break
        A = [np.hstack([J, -np.ones((8, 1))]), np.hstack([-J, -np.ones((8, 1))]), np.hstack([np.ones((1, K)), [[0.0]]])]
        bu = [-mis, mis, [M - b.sum()]]
        if mono:
            Mm = np.zeros((K - 1, K + 1))
            for j in range(K - 1):
                Mm[j, j + 1] = 1 / w[j + 1]
                Mm[j, j] = -1 / w[j]
            A.append(Mm)
            bu.append(-(b[1:] / w[1:] - b[:-1] / w[:-1]))
        A = np.vstack(A)
        bu = np.concatenate(bu)
        lo = np.maximum(-Delta, -b)
        hi = np.full(K, Delta)
        if amax is not None:
            hi = np.minimum(hi, amax * w - b)
        bounds = [(lo[j], hi[j]) for j in range(K)] + [(0, None)]
        res = linprog(c, A_ub=A, b_ub=bu, bounds=bounds, method='highs')
        if res.status != 0:
            Delta *= 0.4
            if Delta < 1e-9:
                break
            continue
        bn = np.clip(b + res.x[:K], 0, None)
        if mono:
            an = np.minimum.accumulate(bn / w)
            bn = an * w
        if bn.sum() > M:
            bn *= M / bn.sum()
        fn = np.abs(dr.miss(bn / w)).max()
        if fn < f * (1 - 1e-10):
            b = bn
            mis, J = dr.miss(b / w, True)
            J = J / w
            f = fn
            Delta = min(Delta * 1.6, M)
        else:
            Delta *= 0.4
            if Delta < 1e-9 * max(M, 1):
                break
    return b / w, f
