"""Upper bound on what ANY strategy (unbounded memory) can earn against a fixed 3-state machine,
by solving the belief-state POMDP. Linear interpolation of a convex value function over-estimates,
so the grid answer is an upper bound on the true optimum."""
import sys, numpy as np
from ipd import M, PAY, payoff

def solve(m, eps, delta, n=240, tol=1e-10):
    assert m.n == 3
    pb = np.where(m.play[:, None] == np.arange(2), 1 - eps, eps)       # P(y | s)
    px = np.array([[1 - eps, eps], [eps, 1 - eps]])                    # P(x | a)
    # grid
    I, J = np.meshgrid(np.arange(n + 1), np.arange(n + 1), indexing="ij")
    ok = I + J <= n
    idx = -np.ones((n + 1, n + 1), dtype=np.int64); idx[ok] = np.arange(ok.sum())
    B = np.stack([I[ok], J[ok], n - I[ok] - J[ok]], 1) / n             # [G,3]
    G = len(B)
    # T[a][s,s'] = sum_x P(x|a)[nxt[s,x]==s']
    T = np.zeros((2, 3, 3))
    for a in (0, 1):
        for s in range(3):
            for x in (0, 1):
                T[a, s, m.nxt[s, x]] += px[a, x]
    R = np.zeros((2, 3))                                               # expected reward given a, s
    for a in (0, 1):
        for s in range(3):
            R[a, s] = sum(px[a, x] * pb[s, y] * PAY[x, y] for x in (0, 1) for y in (0, 1))
    interp = {}
    for a in (0, 1):
        for y in (0, 1):
            w = B * pb[:, y][None]                 # unnormalised posterior over s given y
            py = w.sum(1)
            nb = (w @ T[a]) / py[:, None]          # next belief
            p0 = np.clip(nb[:, 0] * n, 0, n); p1 = np.clip(nb[:, 1] * n, 0, n)
            i = np.minimum(np.floor(p0 + 1e-12).astype(int), n); j = np.minimum(np.floor(p1 + 1e-12).astype(int), n - i)
            u = np.clip(p0 - i, 0, 1); v = np.clip(p1 - j, 0, 1)
            lower = (u + v <= 1) | (i + j + 2 > n)
            v0 = np.where(lower, idx[i, j], idx[np.minimum(i + 1, n), np.minimum(j + 1, n)])
            v1 = idx[np.minimum(i + 1, n), j]; v2 = idx[i, np.minimum(j + 1, n)]
            w0 = np.where(lower, 1 - u - v, u + v - 1); w1 = np.where(lower, u, 1 - v); w2 = np.where(lower, v, 1 - u)
            # boundary safety: where a vertex is off-grid its weight is ~0
            for vv, ww in ((v0, w0), (v1, w1), (v2, w2)):
                bad = vv < 0; ww[bad] = 0; vv[bad] = 0
            s_ = w0 + w1 + w2
            interp[(a, y)] = (py, v0, v1, v2, w0 / s_, w1 / s_, w2 / s_)
    V = np.zeros(G)
    for it in range(100000):
        Q = np.empty((2, G))
        for a in (0, 1):
            q = (1 - delta) * (B @ R[a])
            for y in (0, 1):
                py, v0, v1, v2, w0, w1, w2 = interp[(a, y)]
                q = q + delta * py * (w0 * V[v0] + w1 * V[v1] + w2 * V[v2])
            Q[a] = q
        Vn = Q.max(0)
        d = np.abs(Vn - V).max(); V = Vn
        if d < tol: break
    return V[idx[n, 0]], it      # belief: state 0 for sure (start)

if __name__ == "__main__":
    zoo = [M("handshake", 0, [("D", 0, 1), ("D", 0, 2), ("C", 2, 0)]),
           M("shifty handshake", 0, [("D", 1, 2), ("D", 1, 0), ("C", 2, 1)]),
           M("stiffened wooer", 0, [("C", 0, 1), ("D", 1, 2), ("D", 1, 0)]),
           M("TF2T", 0, [("C", 0, 1), ("C", 0, 2), ("D", 0, 2)]),
           M("2TFT", 0, [("C", 0, 1), ("D", 2, 1), ("D", 0, 1)])]
    delta = 0.99
    for eps in (0.01, 0.05, 0.1):
        for m in zoo:
            self_ = payoff(m, m, eps, delta)[0]
            for n in (120, 240):
                ub, it = solve(m, eps, delta, n)
                print(f"eps {eps} {m.name:17s} self {self_:.4f}  best-response upper bound (grid {n}) {ub:.4f}  gap {ub - self_:+.4f}", flush=True)
