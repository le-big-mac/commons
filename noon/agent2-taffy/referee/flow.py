# Referee's own implementation of the model flow defined in expectations.md.
# usage: flow.py "<device>" n periods [h] [dmax] [sigma] [radius] [cx] [interp]
import sys, time, json
import numpy as np
from words import parse, cyc, period

def rods(n, move, u):
    P = np.array([[k + 1.0, 0.0] for k in range(n)])
    V = np.zeros((n, 2))
    i, cw = move
    th = np.pi * (u - np.sin(2 * np.pi * u) / (2 * np.pi))
    dth = np.pi * (1 - np.cos(2 * np.pi * u))
    s = -1.0 if cw else 1.0
    mid = np.array([i + 0.5, 0.0])
    for idx, a0 in ((i - 1, np.pi), (i, 0.0)):
        a = a0 + s * th
        P[idx] = mid + 0.5 * np.array([np.cos(a), np.sin(a)])
        V[idx] = 0.5 * s * dth * np.array([-np.sin(a), np.cos(a)])
    return P, V

def vel(X, n, move, u, sig2):
    P, V = rods(n, move, u)
    G = [np.exp(-((X[:, 0] - P[j, 0]) ** 2 + (X[:, 1] - P[j, 1]) ** 2) / (2 * sig2)) for j in range(n)]
    out = np.zeros_like(X)
    i = move[0]
    for a in (i - 1, i):
        W = G[a].copy()
        den = 1.0
        for j in range(n):
            if j != a:
                W *= (1.0 - G[j])
                d = P[a] - P[j]
                den *= 1.0 - np.exp(-(d @ d) / (2 * sig2))
        W /= den
        out[:, 0] += W * V[a, 0]
        out[:, 1] += W * V[a, 1]
    return out

def refine(X, dmax):
    while True:
        d = np.roll(X, -1, axis=0) - X
        seg = np.hypot(d[:, 0], d[:, 1])
        idx = np.nonzero(seg > dmax)[0]
        if len(idx) == 0:
            return X
        mids = X[idx] + 0.5 * d[idx]
        X = np.insert(X, idx + 1, mids, axis=0)

def length(X):
    d = np.roll(X, -1, axis=0) - X
    return float(np.hypot(d[:, 0], d[:, 1]).sum())

def word_of(X, n):
    # crossings of the upward rays {x=j, y>0}; right->left = +j, left->right = -j
    Y = np.roll(X, -1, axis=0)
    events = []
    for j in range(1, n + 1):
        a = X[:, 0] - j; b = Y[:, 0] - j
        cr = np.nonzero((a > 0) != (b > 0))[0]
        if len(cr) == 0:
            continue
        tt = a[cr] / (a[cr] - b[cr])
        yc = X[cr, 1] + tt * (Y[cr, 1] - X[cr, 1])
        up = yc > 0
        for k, sgn in zip(cr[up], np.where(a[cr][up] > 0, 1, -1)):
            events.append((int(k), int(sgn) * j))
    events.sort()
    return cyc([e[1] for e in events])

def same_cyclic(w1, w2):
    if len(w1) != len(w2):
        return False
    if len(w1) == 0:
        return True
    s = ",".join(map(str, w1 + w1)) + ","
    t = ",".join(map(str, w2)) + ","
    # match at token boundary
    return ("," + s).find("," + t) >= 0

def run(dev, n, periods, h=0.005, dmax=0.01, sigma=0.35, radius=0.8, cx=1.5, words=True, verbose=True):
    moves = parse(dev)
    sig2 = sigma * sigma
    N0 = int(np.ceil(2 * np.pi * radius / dmax)) + 1
    a = 2 * np.pi * np.arange(N0) / N0
    X = np.stack([cx + radius * np.cos(a), radius * np.sin(a)], axis=1)
    X = refine(X, dmax)
    nsteps = int(round(1.0 / h))
    L = [length(X)]
    w_alg = word_of(X, n)
    topo = []
    t0 = time.time()
    for k in range(1, periods + 1):
        for mv in moves:
            for st in range(nsteps):
                u = st * h
                k1 = vel(X, n, mv, u, sig2)
                k2 = vel(X + 0.5 * h * k1, n, mv, u + 0.5 * h, sig2)
                k3 = vel(X + 0.5 * h * k2, n, mv, u + 0.5 * h, sig2)
                k4 = vel(X + h * k3, n, mv, u + h, sig2)
                X = X + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
                X = refine(X, dmax)
        L.append(length(X))
        if words:
            w_alg = period(w_alg, n, moves)
            w_sim = word_of(X, n)
            ok = same_cyclic(w_alg, w_sim)
            topo.append((len(w_alg), len(w_sim), ok))
        if verbose:
            print(f"  period {k}: L={L[-1]:.5f} N={len(X)} ratio={L[-1]/L[-2]:.5f} "
                  f"{'word alg/sim/match=' + str(topo[-1]) if words else ''} t={time.time()-t0:.0f}s", flush=True)
    return L, topo, X

if __name__ == "__main__":
    dev = sys.argv[1]; n = int(sys.argv[2]); periods = int(sys.argv[3])
    h = float(sys.argv[4]) if len(sys.argv) > 4 else 0.005
    dmax = float(sys.argv[5]) if len(sys.argv) > 5 else 0.01
    sigma = float(sys.argv[6]) if len(sys.argv) > 6 else 0.35
    radius = float(sys.argv[7]) if len(sys.argv) > 7 else 0.8
    cx = float(sys.argv[8]) if len(sys.argv) > 8 else 1.5
    print(f"device {dev} n={n} periods={periods} h={h} dmax={dmax} sigma={sigma} radius={radius} cx={cx}", flush=True)
    L, topo, X = run(dev, n, periods, h, dmax, sigma, radius, cx)
    print("L:", " ".join(f"{v:.5f}" for v in L))
    print("ratios:", " ".join(f"{L[i+1]/L[i]:.5f}" for i in range(len(L) - 1)))
