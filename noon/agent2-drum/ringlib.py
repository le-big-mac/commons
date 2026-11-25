"""A second search, written after the fourth sheet's referee: any number of rings, the sealed measure itself (exact.py searched the
largest |ln(ratio/target)|, which is not quite the sealed |ratio/target - 1|), and sequential linear programming: at each step the
eight misses are made linear in the ring loads and a linear programme is solved inside a trust region."""
import math
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import linprog
NINE = [(0, 1), (1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]; TARGET = np.array([1, 2, 3, 3, 4, 4, 5, 5, 5], float); NEED = ((0, 3), (1, 2), (2, 2), (3, 1), (4, 1))
class Skin:
    def __init__(self, rings, per=50):
        self.R, self.per, self.N = rings, per, rings * per; N = self.N; h = 1.0 / N; self.E = np.arange(rings + 1) / rings; self.A = self.E[1:] ** 2 - self.E[:-1] ** 2
        self.r = (np.arange(N) + 0.5) * h; re = np.arange(N + 1) * h; self.off = -re[1:-1] / (h * h); self.diag = {}
        for m, _ in NEED: d = (re[:-1] + re[1:]) / (h * h) + m * m / self.r; d[-1] += re[-1] / (h * h); self.diag[m] = d
    def solve(self, a, grad=True):
        """the eight misses ratio/target - 1 and, if asked, their derivatives with respect to each ring's load"""
        rho = 1.0 + np.repeat(a, self.per); sc = np.sqrt(self.r * rho); w = {}; g = {}
        for m, cnt in NEED:
            ev, vec = eigh_tridiagonal(self.diag[m] / sc ** 2, self.off / (sc[:-1] * sc[1:]), select='i', select_range=(0, cnt - 1))
            for n in range(cnt):
                w[(m, n + 1)] = math.sqrt(ev[n])
                if grad: g[(m, n + 1)] = -0.5 * (vec[:, n] ** 2 / rho).reshape(self.R, self.per).sum(axis=1)
        W = np.array([w[k] for k in NINE]); c = W[1:] / W[0] / TARGET[1:] - 1
        if not grad: return c
        G = np.array([g[k] for k in NINE]); return c, (c + 1)[:, None] * (G[1:] - G[0])
    def miss(self, a): return float(np.abs(self.solve(a, grad=False)).max())
    def mass(self, a): return float(a @ self.A)
    def fit(self, a, M, lb=None, monotone=False):
        """a start made lawful: above the floor, not increasing outward if asked, and within the weight"""
        lb = np.zeros(self.R) if lb is None else lb; a = np.maximum(a, lb)
        if monotone: a = np.maximum.accumulate(a[::-1])[::-1]
        over = self.mass(a) - M
        if over > 0: a = lb + (a - lb) * (M - self.mass(lb)) / (self.mass(a) - self.mass(lb))
        return a
def slp(skin, a0, M, monotone=False, lb=None, iters=600, log=None):
    R = skin.R; lb = np.zeros(R) if lb is None else lb; a = skin.fit(a0, M, lb, monotone); c, J = skin.solve(a); f = float(np.abs(c).max()); S = M / 0.16; delta = 0.3 * S; cost = np.zeros(R + 1); cost[-1] = 1.0
    Dm = np.zeros((R - 1, R + 1)); Dm[np.arange(R - 1), np.arange(R - 1)] = -1; Dm[np.arange(R - 1), np.arange(1, R)] = 1
    for it in range(iters):
        A_ub = np.vstack([np.hstack([J, -np.ones((8, 1))]), np.hstack([-J, -np.ones((8, 1))]), np.concatenate([skin.A, [0.0]])[None, :]]); b_ub = np.concatenate([-c, c, [M - skin.mass(a)]])
        if monotone: A_ub = np.vstack([A_ub, Dm]); b_ub = np.concatenate([b_ub, a[:-1] - a[1:]])
        res = linprog(cost, A_ub=A_ub, b_ub=b_ub, bounds=[(max(lb[j] - a[j], -delta), delta) for j in range(R)] + [(0, None)], method='highs')
        if res.status != 0 or f - res.x[-1] < 1e-13:
            delta *= 0.5
            if delta < 1e-9 * S: break
            continue
        a1 = np.maximum(a + res.x[:R], lb); c1, J1 = skin.solve(a1); f1 = float(np.abs(c1).max())
        if f - f1 >= 0.1 * (f - res.x[-1]) and skin.mass(a1) <= M + 1e-9: a, c, J, f = a1, c1, J1, f1; delta = min(delta * 1.5, 2 * S)
        else: delta *= 0.5
        if log is not None and it % 50 == 0: print(f"      step {it}: {100 * f:.4f}%  trust {delta / S:.2e}", file=log, flush=True)
        if delta < 1e-9 * S: break
    return a, f
def split(a, times=2): return np.repeat(a, times)
def disc(skin, load, k): return load * np.clip((np.minimum(k, skin.E[1:]) ** 2 - skin.E[:-1] ** 2) / skin.A, 0, 1)
# exact matching of Bessel functions across every ring edge (as in bessel3.py), to check an answer with no grid
from scipy.special import jv, yv, jvp, yvp
from scipy.optimize import brentq
def _rim(w, m, edges, rho):
    k = w * math.sqrt(rho[0]); R, dR = jv(m, k * edges[0]), k * jvp(m, k * edges[0])
    for e0, e1, p in zip(edges[:-1], edges[1:], rho[1:]):
        k = w * math.sqrt(p); J, Y, dJ, dY = jv(m, k * e0), yv(m, k * e0), k * jvp(m, k * e0), k * yvp(m, k * e0); det = J * dY - Y * dJ; a, b = (R * dY - Y * dR) / det, (J * dR - R * dJ) / det
        R, dR = a * jv(m, k * e1) + b * yv(m, k * e1), k * (a * jvp(m, k * e1) + b * yvp(m, k * e1))
    return R
def exact_ratios(a, which=NINE, wmax=14.0, step=0.002):
    """the modes of a ringed load a (one load per equal ring from the centre) by exact matching; neighbouring rings of equal load are merged"""
    n = len(a); edges, rho = [], []
    for j in range(n):
        if rho and abs(rho[-1] - (1 + a[j])) < 1e-12: edges[-1] = (j + 1) / n
        else: edges.append((j + 1) / n); rho.append(1 + a[j])
    need = {}; out = {}
    for m, k in which: need[m] = max(need.get(m, 0), k)
    for m, cnt in need.items():
        roots = []; w = 0.02; f0 = _rim(w, m, edges, rho)
        while len(roots) < cnt and w < wmax:
            f1 = _rim(w + step, m, edges, rho)
            if f0 * f1 < 0: roots.append(brentq(_rim, w, w + step, args=(m, edges, rho), xtol=1e-13))
            w += step; f0 = f1
        out[m] = roots
    W = np.array([out[m][k - 1] for m, k in which]); return W / W[0]
def exact_miss(a): r = exact_ratios(a); return float(np.abs(r[1:] / TARGET[1:] - 1).max())
