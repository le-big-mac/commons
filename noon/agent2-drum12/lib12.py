"""A round skin loaded in equal rings: any list of modes with targets; the measure searched is the sealed one.
Finite differences (50 cells to a ring) with the exact derivative of each miss with respect to each ring's load; sequential linear
programming inside a trust region (as ../drum/ringlib.py, here for any number of modes); exact matching of Bessel functions across
every ring edge to check an answer with no grid; and D, the model-side distance of a struck skin's partials from whole multiples."""
import math
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import linprog, brentq
from scipy.special import jv, yv, jvp, yvp
NINE = [(0, 1), (1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]
TWELVE = NINE + [(5, 1), (3, 2), (1, 3)]; SIXTEEN = TWELVE + [(6, 1), (4, 2), (2, 3), (0, 4)]
SETS = {"nine": NINE, "twelve": TWELVE, "sixteen": SIXTEEN}
target = lambda m, n: float(m + 2 * n - 1)
class Skin:
    def __init__(self, rings, modes, per=50):
        self.R, self.per, self.N, self.modes = rings, per, rings * per, list(modes); N = self.N; h = 1.0 / N
        self.T = np.array([target(m, n) for m, n in self.modes]); self.need = {}
        for m, n in self.modes: self.need[m] = max(self.need.get(m, 0), n)
        self.E = np.arange(rings + 1) / rings; self.A = self.E[1:] ** 2 - self.E[:-1] ** 2
        self.r = (np.arange(N) + 0.5) * h; re = np.arange(N + 1) * h; self.off = -re[1:-1] / (h * h); self.diag = {}
        for m in self.need: d = (re[:-1] + re[1:]) / (h * h) + m * m / self.r; d[-1] += re[-1] / (h * h); self.diag[m] = d
    def solve(self, a, grad=True):
        rho = 1.0 + np.repeat(a, self.per); sc = np.sqrt(self.r * rho); w = {}; g = {}
        for m, cnt in self.need.items():
            ev, vec = eigh_tridiagonal(self.diag[m] / sc ** 2, self.off / (sc[:-1] * sc[1:]), select='i', select_range=(0, cnt - 1))
            for n in range(cnt):
                w[(m, n + 1)] = math.sqrt(ev[n])
                if grad: g[(m, n + 1)] = -0.5 * (vec[:, n] ** 2 / rho).reshape(self.R, self.per).sum(axis=1)
        W = np.array([w[k] for k in self.modes]); c = W[1:] / W[0] / self.T[1:] - 1
        if not grad: return c
        G = np.array([g[k] for k in self.modes]); return c, (c + 1)[:, None] * (G[1:] - G[0])
    def miss(self, a): return float(np.abs(self.solve(a, grad=False)).max())
    def mass(self, a): return float(a @ self.A)
    def fit(self, a, M, lb=None, monotone=False):
        lb = np.zeros(self.R) if lb is None else lb; a = np.maximum(a, lb)
        if monotone: a = np.maximum.accumulate(a[::-1])[::-1]
        if self.mass(a) > M: a = lb + (a - lb) * (M - self.mass(lb)) / (self.mass(a) - self.mass(lb))
        return a
def slp(skin, a0, M, monotone=False, lb=None, iters=700):
    R = skin.R; K = len(skin.modes) - 1; lb = np.zeros(R) if lb is None else lb; a = skin.fit(a0, M, lb, monotone); c, J = skin.solve(a); f = float(np.abs(c).max()); S = M / 0.16; delta = 0.3 * S
    cost = np.zeros(R + 1); cost[-1] = 1.0; ones = np.ones((K, 1)); Dm = np.zeros((R - 1, R + 1)); Dm[np.arange(R - 1), np.arange(R - 1)] = -1; Dm[np.arange(R - 1), np.arange(1, R)] = 1
    for it in range(iters):
        A_ub = np.vstack([np.hstack([J, -ones]), np.hstack([-J, -ones]), np.concatenate([skin.A, [0.0]])[None, :]]); b_ub = np.concatenate([-c, c, [M - skin.mass(a)]])
        if monotone: A_ub = np.vstack([A_ub, Dm]); b_ub = np.concatenate([b_ub, a[:-1] - a[1:]])
        res = linprog(cost, A_ub=A_ub, b_ub=b_ub, bounds=[(max(lb[j] - a[j], -delta), delta) for j in range(R)] + [(0, None)], method='highs')
        if res.status != 0 or f - res.x[-1] < 1e-13:
            delta *= 0.5
            if delta < 1e-9 * S: break
            continue
        a1 = np.maximum(a + res.x[:R], lb); c1, J1 = skin.solve(a1); f1 = float(np.abs(c1).max())
        if f - f1 >= 0.1 * (f - res.x[-1]) and skin.mass(a1) <= M + 1e-9: a, c, J, f = a1, c1, J1, f1; delta = min(delta * 1.5, 2 * S)
        else: delta *= 0.5
        if delta < 1e-9 * S: break
    return a, f
def disc(skin, load, k): return load * np.clip((np.minimum(k, skin.E[1:]) ** 2 - skin.E[:-1] ** 2) / skin.A, 0, 1)
# ---- exact matching of Bessel functions across every ring edge (w may be an array)
def _rim(w, m, edges, rho):
    k = w * math.sqrt(rho[0]); Rv, dR = jv(m, k * edges[0]), k * jvp(m, k * edges[0])
    for e0, e1, p in zip(edges[:-1], edges[1:], rho[1:]):
        k = w * math.sqrt(p); J, Y, dJ, dY = jv(m, k * e0), yv(m, k * e0), k * jvp(m, k * e0), k * yvp(m, k * e0); det = J * dY - Y * dJ; ca, cb = (Rv * dY - Y * dR) / det, (J * dR - Rv * dJ) / det
        Rv, dR = ca * jv(m, k * e1) + cb * yv(m, k * e1), k * (ca * jvp(m, k * e1) + cb * yvp(m, k * e1))
    return Rv
def pieces(a):
    n = len(a); edges, rho = [], []
    for j in range(n):
        if rho and abs(rho[-1] - (1 + a[j])) < 1e-12: edges[-1] = (j + 1) / n
        else: edges.append((j + 1) / n); rho.append(1 + a[j])
    return edges, rho
def exact_ratios(a, which, wmax=40.0, step=0.001):
    """scans the frequency upward in stretches of 2 until each number of nodal diameters has the modes it needs (made quicker after the
    referee's report: it used to scan to 16 every time; the roots found are the same)"""
    edges, rho = pieces(np.where(np.asarray(a) < 1e-9, 0.0, a)); need = {}; out = {}
    for m, n in which: need[m] = max(need.get(m, 0), n)
    for m, cnt in need.items():
        roots = []; lo = 0.02
        while len(roots) < cnt and lo < wmax:
            ws = np.arange(lo, lo + 2.0 + step, step); f = _rim(ws, m, edges, rho); idx = np.nonzero(f[:-1] * f[1:] < 0)[0]
            roots += [brentq(_rim, ws[i], ws[i + 1], args=(m, edges, rho), xtol=1e-13) for i in idx[:cnt - len(roots)]]; lo += 2.0
        if len(roots) < cnt: raise ValueError(f"only {len(roots)} of {cnt} modes found for m = {m}")
        out[m] = roots
    W = np.array([out[m][n - 1] for m, n in which]); return W / W[0]
def exact_miss(a, which):
    r = exact_ratios(a, which); T = np.array([target(m, n) for m, n in which]); return float(np.abs(r[1:] / T[1:] - 1).max())
# ---- the struck skin: every mode up to `top` times the lowest, with its strength when struck at `strike`, and D
def struck(a, top=6.6, strike=0.5, per=50):
    R = len(a); N = R * per; h = 1.0 / N; r = (np.arange(N) + 0.5) * h; re = np.arange(N + 1) * h; rho = 1 + np.repeat(a, per); sc = np.sqrt(r * rho); out = []; w01 = None
    for m in range(0, 10):
        d = (re[:-1] + re[1:]) / (h * h) + m * m / r; d[-1] += re[-1] / (h * h); ev, vec = eigh_tridiagonal(d / sc ** 2, -re[1:-1] / (h * h) / (sc[:-1] * sc[1:]), select='i', select_range=(0, 7)); w = np.sqrt(ev); w01 = w[0] if m == 0 else w01
        for j in range(8):
            ratio = w[j] / w01
            if ratio > top: break
            amp = float(np.interp(strike, r, vec[:, j] / sc)) / (2 if m == 0 else 1); out.append(dict(m=m, n=j + 1, ratio=float(ratio), strength=abs(amp) / math.sqrt(ratio) * math.exp(-(ratio / 7.0) ** 2)))
    return sorted(out, key=lambda x: x['ratio'])
def D(a, **kw):
    """the weighted mean distance, in cents, of the struck skin's partials from the nearest whole multiple of the lowest"""
    num = den = 0.0
    for p in struck(a, **kw):
        t = 1.3 * p['ratio'] ** -0.8; e = p['strength'] ** 2 * t * (1 - math.exp(-1.2 / t)); k = max(1, round(p['ratio'])); num += e * abs(1200 * math.log2(p['ratio'] / k)); den += e
    return num / den
