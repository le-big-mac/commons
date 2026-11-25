"""Referee's own solver: radial membrane, density rho(r)=1+a(r), fixed rim.
FEM (linear, lumped mass) for searching; exact Bessel matching for checking."""
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.special import jv, yv, jvp, yvp
from scipy.optimize import brentq

NEED = {0: 3, 1: 2, 2: 2, 3: 1, 4: 1}
SEVEN = [((2, 1), 3), ((0, 2), 3), ((3, 1), 4), ((1, 2), 4), ((4, 1), 5), ((2, 2), 5), ((0, 3), 5)]
EXTRA7 = [((5, 1), 6), ((3, 2), 6), ((1, 3), 6), ((6, 1), 7), ((4, 2), 7), ((2, 3), 7), ((0, 4), 7)]


class Fem:
    def __init__(self, N):
        self.N = N
        h = 1.0 / N
        r = np.arange(N + 1) * h
        self.h, self.r = h, r
        re, rp = r[:-1], r[1:]
        self.mL = h * (2 * re + rp) / 6
        self.mR = h * (re + 2 * rp) / 6
        self.kE = (re + rp) / 2 / h
        with np.errstate(divide='ignore', invalid='ignore'):
            lg = np.log(rp / re)
            self.cL = rp / h * lg - 1
            self.cR = 1 - re / h * lg
        self.cL[0] = 0.0
        self.cR[0] = 1.0

    def modes(self, rho_e, m, n):
        """lowest n eigenvalues (omega^2) and d(lambda)/d(rho_e) (n x N)."""
        N = self.N
        Md = np.zeros(N + 1); Md[:-1] += rho_e * self.mL; Md[1:] += rho_e * self.mR
        Kd = np.zeros(N + 1); Kd[:-1] += self.kE; Kd[1:] += self.kE
        if m > 0:
            Kd[:-1] += m * m * self.cL; Kd[1:] += m * m * self.cR
            lo = 1
        else:
            lo = 0
        s = 1 / np.sqrt(Md[lo:N])
        d = Kd[lo:N] * s * s
        e = -self.kE[lo:N - 1] * s[:-1] * s[1:]
        w, v = eigh_tridiagonal(d, e, select='i', select_range=(0, n - 1))
        u = np.zeros((n, N + 1))
        u[:, lo:N] = (v * s[:, None]).T
        g = -w[:, None] * (u[:, :-1] ** 2 * self.mL + u[:, 1:] ** 2 * self.mR)
        return w, g


def rho_elements(fem, edges, rho):
    """element densities for rings with outer edges `edges` (last =1); fractional at cut elements."""
    N = fem.N
    out = np.zeros(N)
    lo = 0.0
    r = fem.r
    for e_, p in zip(edges, rho):
        # weight by area overlap of each element with [lo, e_]
        a = np.clip(r[:-1], lo, e_); b = np.clip(r[1:], lo, e_)
        out += p * (b * b - a * a) / (r[1:] ** 2 - r[:-1] ** 2)
        lo = e_
    return out


def fem_freqs(fem, rho_e, need=NEED, grad=False):
    f = {}; G = {}
    for m, n in need.items():
        w, g = fem.modes(rho_e, m, n)
        for i in range(n):
            f[(m, i + 1)] = np.sqrt(w[i])
            if grad:
                G[(m, i + 1)] = g[i] / (2 * np.sqrt(w[i]))
    return (f, G) if grad else f


def exact_F(edges, rho, m, w):
    k = w * np.sqrt(rho[0]); x = k * edges[0]
    u = jv(m, x); du = k * jvp(m, x)
    for j in range(1, len(rho)):
        k = w * np.sqrt(rho[j]); x = k * edges[j - 1]
        A = np.pi * x / 2 * (u * yvp(m, x) - du / k * yv(m, x))
        B = np.pi * x / 2 * (du / k * jv(m, x) - u * jvp(m, x))
        x = k * edges[j]
        u = A * jv(m, x) + B * yv(m, x); du = k * (A * jvp(m, x) + B * yvp(m, x))
    return u


def exact_freqs(edges, rho, need=NEED, N=1600):
    """exact matching; FEM gives the brackets and the mode count."""
    edges = np.asarray(edges, float); rho = np.asarray(rho, float)
    # merge equal neighbours
    ke = [edges[0]]; kr = [rho[0]]
    for e_, p in zip(edges[1:], rho[1:]):
        if abs(p - kr[-1]) < 1e-13:
            ke[-1] = e_
        else:
            ke.append(e_); kr.append(p)
    edges, rho = np.array(ke), np.array(kr)
    fem = Fem(N)
    g = fem_freqs(fem, rho_elements(fem, edges, rho), need)
    out = {}
    for (m, n), w0 in g.items():
        d = 5e-4
        while True:
            a, b = w0 * (1 - d), w0 * (1 + d)
            if exact_F(edges, rho, m, a) * exact_F(edges, rho, m, b) < 0:
                break
            d *= 2
            if d > 0.03:
                raise RuntimeError('no bracket %s' % ((m, n),))
        out[(m, n)] = brentq(lambda w: exact_F(edges, rho, m, w), a, b, xtol=1e-13, rtol=1e-13)
    return out


def misses(f, targets=SEVEN, with_low=False):
    note = f[(1, 1)] / 2
    ms = [f[k] / (t * note) - 1 for k, t in targets]
    if with_low:
        ms.append(f[(0, 1)] / note - 1)
    return np.array(ms), f[(0, 1)] / note
