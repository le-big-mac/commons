"""Upper bound on the payoff of ANY strategy against a fixed S-state machine (any S), via value iteration on a
Freudenthal-triangulated grid over the belief simplex (Lovejoy 1991). Piecewise-linear interpolation of a
convex value function over-estimates, so each grid gives a valid upper bound; finer grids tighten it."""
import sys, itertools, numpy as np
from ipd import FSM, M, PAY, payoff, canonical

def grid_points(S, n):
    # all nonincreasing integer vectors v with v0 = n, v_{S-1} >= 0  <->  compositions
    pts = []
    def rec(prefix, last):
        if len(prefix) == S: pts.append(prefix); return
        for v in range(last, -1, -1): rec(prefix + [v], v)
    rec([n], n)
    return np.array(pts, dtype=np.int64)

def solve(m, eps, delta, n, tol=1e-9):
    m = canonical(m); S = m.n
    V_ = grid_points(S, n); G = len(V_)
    base = n + 2
    powv = base ** np.arange(S)[::-1]
    keys = V_ @ powv; order = np.argsort(keys); skeys = keys[order]
    B = (V_ - np.concatenate([V_[:, 1:], np.zeros((G, 1), dtype=np.int64)], 1)) / n
    pb = np.where(m.play[:, None] == np.arange(2), 1 - eps, eps)
    px = np.array([[1 - eps, eps], [eps, 1 - eps]])
    T = np.zeros((2, S, S)); R = np.zeros((2, S))
    for a in (0, 1):
        for s in range(S):
            for x in (0, 1):
                T[a, s, m.nxt[s, x]] += px[a, x]
                for y in (0, 1): R[a, s] += px[a, x] * pb[s, y] * PAY[x, y]
    interp = {}
    for a in (0, 1):
        for y in (0, 1):
            w = B * pb[:, y][None]; py = w.sum(1)
            nb = (w @ T[a]) / py[:, None]
            x = n * np.cumsum(nb[:, ::-1], 1)[:, ::-1]
            x[:, 0] = n
            v = np.floor(x + 1e-9).astype(np.int64); d = np.clip(x - v, 0, 1); d[:, 0] = 0
            perm = np.argsort(-d, axis=1, kind="stable")
            ds = np.take_along_axis(d, perm, 1)
            lam = np.concatenate([1 - ds[:, :1], ds[:, :-1] - ds[:, 1:], ds[:, -1:]], 1)   # S+1 weights
            idxs = np.empty((G, S + 1), dtype=np.int64); cur = v.copy()
            for k in range(S + 1):
                if k > 0:
                    np.add.at(cur, (np.arange(G), perm[:, k - 1]), 1)
                kk = cur @ powv
                pos = np.clip(np.searchsorted(skeys, kk), 0, G - 1)
                found = skeys[pos] == kk
                assert (found | (lam[:, k] < 1e-7)).all(), "off-grid vertex with weight"
                lam[~found, k] = 0
                idxs[:, k] = order[pos]
            lam /= lam.sum(1, keepdims=True)
            interp[(a, y)] = (py, idxs, lam)
    V = np.zeros(G)
    for it in range(200000):
        Q = []
        for a in (0, 1):
            q = (1 - delta) * (B @ R[a])
            for y in (0, 1):
                py, idxs, lam = interp[(a, y)]
                q = q + delta * py * (lam * V[idxs]).sum(1)
            Q.append(q)
        Vn = np.maximum(Q[0], Q[1]); dlt = np.abs(Vn - V).max(); V = Vn
        if dlt < tol: break
    start = np.zeros(S, dtype=np.int64); start[0] = n       # belief = state 0: v = (n,0,...,0)
    return V[order[np.searchsorted(skeys, start @ powv)]], G

if __name__ == "__main__":
    eps, delta = 0.05, 0.99
    tests = [(M("handshake", 0, [("D", 0, 1), ("D", 0, 2), ("C", 2, 0)]), (60, 120)),
             (M("free-pass wooer (4)", 0, [("C", 0, 1), ("C", 1, 2), ("D", 2, 3), ("D", 2, 1)]), (20, 40, 60)),
             (M("five-state", 0, [("C", 0, 1), ("C", 1, 2), ("D", 2, 3), ("D", 2, 4), ("D", 1, 0)]), (12, 20, 30))]
    for m, ns in tests:
        s = payoff(m, m, eps, delta)[0]
        for n in ns:
            ub, G = solve(m, eps, delta, n)
            print(f"{m.name:22s} self {s:.4f}  grid {n:3d} ({G} pts)  upper bound {ub:.4f}  gap {ub - s:+.4f}", flush=True)
