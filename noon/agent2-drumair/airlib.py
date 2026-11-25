"""Air in the drum.  The membrane of the three earlier studies, with the stiffness of the air shut in behind it.
Modes with no nodal diameter change the cavity's volume and feel a pressure:  lap(u) + w^2 rho u = B * (integral of u over the unit disc).
Modes with nodal diameters are untouched.  B = rho0 c^2 a^4 / (V T).   "Tube": B is multiplied by x cot x, x = X w (the cavity as a closed
pipe carrying plane waves; x = depth * frequency / c).  No mass of moving air is in the model.
Two solvers: finite differences in rings (for searches; exact derivatives with B held fixed), and exact matching of Bessel functions with a
particular solution in each piece (for every figure reported)."""
import sys, math
sys.path.insert(0, "../drum12"); sys.path.insert(0, "../drum"); sys.path.insert(0, "../drumfree")
import numpy as np
from scipy.linalg import eigh_tridiagonal, solve_banded
from scipy.optimize import brentq
from scipy.special import jv, yv
import lib12 as L
import drum
# ---- the reference drum of the sealed sheet
RHO0, C = 1.2, 343.0; RADIUS, DEPTH, CAVITY_RADIUS, SKIN, F11 = 0.065, 0.125, 0.06, 0.25, 440.0
VOLUME = math.pi * CAVITY_RADIUS ** 2 * DEPTH
B0 = RHO0 * C * C * RADIUS ** 2 / (VOLUME * SKIN * (2 * math.pi * F11) ** 2)        # B = B0 * w11^2, w11 the load's (1,1) frequency in the model's units
X0 = 2 * math.pi * F11 * DEPTH / C                                                 # x = X0 * w / w11
def reference(w11, volume=1.0, depth=1.0):
    """(B, X) of the reference drum for a load whose (1,1) is at w11; volume and depth as multiples of the reference's"""
    return B0 * w11 ** 2 / volume, X0 * depth / w11
# ---- exact: pieces of even density, Bessel functions and a constant in each
def _G(w, edges, rho, B, X=None):
    """the mean-pressure consistency of a round mode at frequency w: zero at a mode with air.  Poles at the vacuum's round modes."""
    lam = w * w; Be = B if X is None else B * (X * w) / math.tan(X * w)
    k = w * math.sqrt(rho[0]); p = Be / (lam * rho[0]); ah, bh, ap, bp = 1.0, 0.0, 0.0, 0.0; Ih = Ip = 0.0; e0 = 0.0
    for i, e in enumerate(edges):
        J1e, Y1e = e * jv(1, k * e) / k, (e * yv(1, k * e) / k if i else 0.0); J10, Y10 = (e0 * jv(1, k * e0) / k, e0 * yv(1, k * e0) / k) if i else (0.0, 0.0)
        Ih += ah * (J1e - J10) + bh * (Y1e - Y10); Ip += ap * (J1e - J10) + bp * (Y1e - Y10) + p * (e * e - e0 * e0) / 2
        if i == len(edges) - 1: break
        J, Y, dJ, dY = jv(0, k * e), yv(0, k * e), -k * jv(1, k * e), -k * yv(1, k * e); Rh, dRh = ah * J + bh * Y, ah * dJ + bh * dY; Rp, dRp = ap * J + bp * Y + p, ap * dJ + bp * dY
        k = w * math.sqrt(rho[i + 1]); p = Be / (lam * rho[i + 1]); J, Y, dJ, dY = jv(0, k * e), yv(0, k * e), -k * jv(1, k * e), -k * yv(1, k * e); det = J * dY - Y * dJ
        ah, bh = (Rh * dY - Y * dRh) / det, (J * dRh - Rh * dJ) / det; Rp -= p; ap, bp = (Rp * dY - Y * dRp) / det, (J * dRp - Rp * dJ) / det; e0 = e
    Uh = ah * jv(0, k) + bh * yv(0, k); Up = ap * jv(0, k) + bp * yv(0, k) + p
    return 2 * math.pi * (-Up / Uh * Ih + Ip) - 1.0
def _H(w, edges, rho, B, X=None):
    """the same condition with its poles multiplied out: Uh(1) * G(w), and for the tube also times sin x.  Smooth in w; zero at every
    round mode of skin and air together (for the tube these include the cavity's own resonances, near x = pi, 2 pi, ...)."""
    lam = w * w; k = w * math.sqrt(rho[0]); p = 1.0 / (lam * rho[0]); ah, bh, ap, bp = 1.0, 0.0, 0.0, 0.0; Ih = Ip = 0.0; e0 = 0.0
    for i, e in enumerate(edges):
        J1e, Y1e = e * jv(1, k * e) / k, (e * yv(1, k * e) / k if i else 0.0); J10, Y10 = (e0 * jv(1, k * e0) / k, e0 * yv(1, k * e0) / k) if i else (0.0, 0.0)
        Ih += ah * (J1e - J10) + bh * (Y1e - Y10); Ip += ap * (J1e - J10) + bp * (Y1e - Y10) + p * (e * e - e0 * e0) / 2
        if i == len(edges) - 1: break
        J, Y, dJ, dY = jv(0, k * e), yv(0, k * e), -k * jv(1, k * e), -k * yv(1, k * e); Rh, dRh = ah * J + bh * Y, ah * dJ + bh * dY; Rp, dRp = ap * J + bp * Y + p, ap * dJ + bp * dY
        k = w * math.sqrt(rho[i + 1]); p = 1.0 / (lam * rho[i + 1]); J, Y, dJ, dY = jv(0, k * e), yv(0, k * e), -k * jv(1, k * e), -k * yv(1, k * e); det = J * dY - Y * dJ
        ah, bh = (Rh * dY - Y * dRh) / det, (J * dRh - Rh * dJ) / det; Rp -= p; ap, bp = (Rp * dY - Y * dRp) / det, (J * dRp - Rp * dJ) / det; e0 = e
    Uh = ah * jv(0, k) + bh * yv(0, k); Up = ap * jv(0, k) + bp * yv(0, k) + p; Q = 2 * math.pi * (Ip * Uh - Up * Ih)
    if X is None: return B * Q - Uh
    x = X * w; return B * x * math.cos(x) * Q - math.sin(x) * Uh
def _vac_round(edges, rho, count, step=0.001, wmax=60.0):
    roots = []; lo = 0.02
    while len(roots) < count and lo < wmax:
        ws = np.arange(lo, lo + 2.0 + step, step); f = L._rim(ws, 0, edges, rho); idx = np.nonzero(f[:-1] * f[1:] < 0)[0]
        roots += [brentq(L._rim, ws[i], ws[i + 1], args=(0, edges, rho), xtol=1e-13) for i in idx[:count - len(roots)]]; lo += 2.0
    return roots
def round_modes(edges, rho, B, count):
    """the first `count` round modes with air as a spring, exact: one root between each pair of the vacuum's round modes"""
    P = _vac_round(edges, rho, count + 1)
    if B == 0: return P[:count]
    return [brentq(_G, P[n] * (1 + 1e-10), P[n + 1] * (1 - 1e-10), args=(edges, rho, B), xtol=1e-13) for n in range(count)]
def tube_modes(edges, rho, B, X, wmax, step=0.002):
    """every round mode of skin and tube together below wmax, exact, by scanning the pole-free condition"""
    ws = np.arange(0.05, wmax + step, step); f = np.array([_H(w, edges, rho, B, X) for w in ws]); idx = np.nonzero(f[:-1] * f[1:] < 0)[0]
    return [brentq(_H, ws[i], ws[i + 1], args=(edges, rho, B, X), xtol=1e-13) for i in idx]
def vacuum(a, which):
    """absolute frequencies (model units) of the listed modes of a ring load, in a vacuum, exact"""
    edges, rho = L.pieces(np.where(np.asarray(a, float) < 1e-9, 0.0, a)); need = {}; out = {}
    for m, n in which: need[m] = max(need.get(m, 0), n)
    for m, cnt in need.items():
        roots = []; lo = 0.02
        while len(roots) < cnt and lo < 60:
            ws = np.arange(lo, lo + 2.0 + 0.001, 0.001); f = L._rim(ws, m, edges, rho); idx = np.nonzero(f[:-1] * f[1:] < 0)[0]
            roots += [brentq(L._rim, ws[i], ws[i + 1], args=(m, edges, rho), xtol=1e-13) for i in idx[:cnt - len(roots)]]; lo += 2.0
        for n in range(cnt): out[(m, n + 1)] = roots[n]
    return out
def with_air(edges, rho, which, B, vac=None):
    """absolute frequencies of the listed modes with air as a spring of strength B: {(m, n): w}"""
    if vac is None:
        need = {}; vac = {}
        for m, n in which: need[m] = max(need.get(m, 0), n)
        for m, cnt in need.items():
            roots = []; lo = 0.02
            while len(roots) < cnt and lo < 60:
                ws = np.arange(lo, lo + 2.0 + 0.001, 0.001); f = L._rim(ws, m, edges, rho); idx = np.nonzero(f[:-1] * f[1:] < 0)[0]
                roots += [brentq(L._rim, ws[i], ws[i + 1], args=(m, edges, rho), xtol=1e-13) for i in idx[:cnt - len(roots)]]; lo += 2.0
            for n in range(cnt): vac[(m, n + 1)] = roots[n]
    out = dict(vac); cnt0 = max([n for m, n in which if m == 0], default=0)
    if cnt0 and B:
        r = round_modes(edges, rho, B, cnt0)
        for n in range(cnt0): out[(0, n + 1)] = r[n]
    return {k: out[k] for k in which}
def load_pieces(a): return L.pieces(np.where(np.asarray(a, float) < 1e-9, 0.0, a))
def disc_pieces(s, k): return [float(k), 1.0], [float(s), 1.0]
# ---- finite differences in rings, for searches (B held fixed)
class AirSkin(L.Skin):
    """as lib12.Skin (misses of the listed modes against the first in the list), with air as a spring of strength B on the round modes.
    free=True: the first mode listed is (1,1) and the note is half of it (as libfree.FreeSkin)."""
    def __init__(self, rings, modes, B=0.0, per=50, free=False):
        super().__init__(rings, modes, per); self.B = float(B); self.h = 1.0 / self.N
        if free: self.T = self.T / self.T[0]
    def solve(self, a, grad=True):
        rho = 1.0 + np.repeat(a, self.per); sc = np.sqrt(self.r * rho); w = {}; g = {}
        for m, cnt in self.need.items():
            air = (m == 0 and self.B != 0)
            ev, vec = eigh_tridiagonal(self.diag[m] / sc ** 2, self.off / (sc[:-1] * sc[1:]), select='i', select_range=(0, cnt if air else cnt - 1))
            if not air:
                for n in range(cnt):
                    w[(m, n + 1)] = math.sqrt(ev[n])
                    if grad: g[(m, n + 1)] = -0.5 * (vec[:, n] ** 2 / rho).reshape(self.R, self.per).sum(axis=1)
                continue
            D = self.r * rho; beta = 2 * math.pi * self.h * self.B; ab = np.zeros((3, self.N)); ab[0, 1:] = self.off; ab[2, :-1] = self.off
            def gfun(lam, give=False):
                ab[1] = self.diag[0] - lam * D; y = solve_banded((1, 1), ab, self.r); return y if give else 1.0 + beta * float(self.r @ y)
            for n in range(cnt):
                # the tridiagonal eigenvalues are good to about 1e-9 of the largest, so the bracket stays 1e-6 (relative) clear of each pole;
                # a root nearer a pole than that belongs to a round mode that hardly moves the air, and is given the vacuum's value
                lo, hi = ev[n] * (1 + 1e-6), ev[n + 1] * (1 - 1e-6); glo, ghi = gfun(lo), gfun(hi); u = None
                if glo > 0: lam = ev[n]; u = vec[:, n] / sc
                elif ghi < 0: lam = ev[n + 1]; u = vec[:, n + 1] / sc
                else: lam = brentq(gfun, lo, hi, xtol=1e-13 * ev[n + 1], rtol=1e-14)
                w[(0, n + 1)] = math.sqrt(lam)
                if grad:
                    u = gfun(lam, True) if u is None else u; q = self.r * u * u; g[(0, n + 1)] = -0.5 * q.reshape(self.R, self.per).sum(axis=1) / float(q @ rho)
        W = np.array([w[k] for k in self.modes]); c = W[1:] / W[0] / self.T[1:] - 1; self.W = W
        if not grad: return c
        G = np.array([g[k] for k in self.modes]); return c, (c + 1)[:, None] * (G[1:] - G[0])
class RefSkin(L.Skin):
    """the reference drum itself: the air's strength follows the load, B = B0 * w11^2 / volume, inside every evaluation, and the
    derivatives carry that dependence.  (1,1) must be among the modes.  free=True as in AirSkin.  B of the last solve is kept in self.B."""
    def __init__(self, rings, modes, volume=1.0, per=50, free=False):
        super().__init__(rings, modes, per); self.volume = float(volume); self.h = 1.0 / self.N; self.B = None
        if free: self.T = self.T / self.T[0]
    def solve(self, a, grad=True):
        rho = 1.0 + np.repeat(a, self.per); sc = np.sqrt(self.r * rho); w = {}; g = {}
        for m, cnt in sorted(self.need.items(), key=lambda z: z[0] == 0):                      # the round modes last: they need (1,1)
            if m != 0:
                ev, vec = eigh_tridiagonal(self.diag[m] / sc ** 2, self.off / (sc[:-1] * sc[1:]), select='i', select_range=(0, cnt - 1))
                for n in range(cnt):
                    w[(m, n + 1)] = math.sqrt(ev[n])
                    if grad: g[(m, n + 1)] = -0.5 * (vec[:, n] ** 2 / rho).reshape(self.R, self.per).sum(axis=1)
                continue
            if (1, 1) not in w:
                ev1, vec1 = eigh_tridiagonal(self.diag1 / sc ** 2, self.off / (sc[:-1] * sc[1:]), select='i', select_range=(0, 0)); w11 = math.sqrt(ev1[0]); g11 = -0.5 * (vec1[:, 0] ** 2 / rho).reshape(self.R, self.per).sum(axis=1)
            else: w11 = w[(1, 1)]; g11 = g.get((1, 1))
            B = B0 * w11 ** 2 / self.volume; self.B = B
            ev, vec = eigh_tridiagonal(self.diag[0] / sc ** 2, self.off / (sc[:-1] * sc[1:]), select='i', select_range=(0, cnt))
            D = self.r * rho; beta = 2 * math.pi * self.h * B; ab = np.zeros((3, self.N)); ab[0, 1:] = self.off; ab[2, :-1] = self.off
            def gfun(lam, give=False):
                ab[1] = self.diag[0] - lam * D; y = solve_banded((1, 1), ab, self.r); return y if give else 1.0 + beta * float(self.r @ y)
            for n in range(cnt):
                lo, hi = ev[n] * (1 + 1e-6), ev[n + 1] * (1 - 1e-6); glo, ghi = gfun(lo), gfun(hi); u = None
                if glo > 0: lam = ev[n]; u = vec[:, n] / sc
                elif ghi < 0: lam = ev[n + 1]; u = vec[:, n + 1] / sc
                else: lam = brentq(gfun, lo, hi, xtol=1e-13 * ev[n + 1], rtol=1e-14)
                w[(0, n + 1)] = math.sqrt(lam)
                if grad:
                    u = gfun(lam, True) if u is None else u; q = self.r * u * u; den = float(q @ rho)
                    dlnw_dB = math.pi * self.h * float(self.r @ u) ** 2 / (lam * den)                # d ln w / dB at a fixed load
                    g[(0, n + 1)] = -0.5 * q.reshape(self.R, self.per).sum(axis=1) / den + dlnw_dB * 2 * B * g11
        W = np.array([w[k] for k in self.modes]); c = W[1:] / W[0] / self.T[1:] - 1; self.W = W
        if not grad: return c
        G = np.array([g[k] for k in self.modes]); return c, (c + 1)[:, None] * (G[1:] - G[0])
