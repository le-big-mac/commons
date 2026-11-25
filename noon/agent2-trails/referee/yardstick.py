"""Referee: probe the README's planner's yardstick -- 'no network of straight paths beats the line between the triangle and the Y'.
Random straight-segment networks on the 3 gates plus up to 3 free junctions; best candidates refined by Nelder-Mead on D + lambda* L."""
import numpy as np, itertools
from scipy.optimize import minimize
SQ3 = np.sqrt(3); GATES = np.array([[0, 0], [1, 0], [0.5, SQ3 / 2]])
lam = (2 / SQ3 - 1) / (3 - SQ3)                       # slope of the line: triangle and Y tie at this price of trail
def line_d(L): return 2 / SQ3 - (L - SQ3) * lam
def LD(free, edges):
    P = np.vstack([GATES, free.reshape(-1, 2)]); n = len(P)
    W = np.full((n, n), np.inf); np.fill_diagonal(W, 0); L = 0
    for i, j in edges:
        w = np.hypot(*(P[i] - P[j])); W[i, j] = W[j, i] = min(W[i, j], w); L += w
    for k in range(n):
        W = np.minimum(W, W[:, k:k + 1] + W[k:k + 1, :])
    return L, (W[0, 1] + W[0, 2] + W[1, 2]) / 3
rng = np.random.default_rng(1); best = []
for trial in range(60000):
    k = rng.integers(1, 4); n = 3 + k
    allE = list(itertools.combinations(range(n), 2))
    edges = [e for e in allE if rng.random() < rng.uniform(0.25, 0.7)]
    free = np.c_[rng.uniform(0, 1, k), rng.uniform(0, SQ3 / 2, k)].ravel()
    L, D = LD(free, edges)
    if not np.isfinite(D) or L > 3: continue
    best.append((D - line_d(L), L, D, free, edges))
best.sort(key=lambda t: t[0]); print(f"{len(best)} connected random networks with L <= 3; lowest D - line(L) before refinement: {best[0][0]:+.4f}")
res = []
for gap, L, D, free, edges in best[:150]:
    f = lambda x: (lambda LD_: LD_[1] + lam * LD_[0])(LD(x, edges))
    o = minimize(f, free, method='Nelder-Mead', options=dict(xatol=1e-7, fatol=1e-10, maxiter=6000))
    L2, D2 = LD(o.x, edges); res.append((D2 - line_d(L2), L2, D2))
res.sort(); print("after refinement, the five lowest (D - line(L), L, D):"); [print(f"   {g:+.6f}  L={L:.4f}  D={D:.4f}") for g, L, D in res[:5]]
