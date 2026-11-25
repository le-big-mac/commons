# Brute-force depth straight from the definition, to check peel.c on small cases.
# A remaining point p is on the layer iff some parabola y = c-(x-a)^2/2 through p has no
# remaining point strictly below it: for all q,  y_q >= y_p + a(x_q-x_p) - (x_q-x_p)^2/2 ... i.e.
# there is a (the parabola's slope at p is s):  y_q - y_p + (x_q-x_p)^2/2 >= s (x_q-x_p) for all q.
import sys
import numpy as np
fn, W, periodic = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
d = np.loadtxt(fn, ndmin=2)
x, y, dep = d[:, 0], d[:, 1], d[:, 2].astype(int)
N = len(x)
K = 8 if periodic else 0
alive = np.ones(N, bool)
bd = np.zeros(N, int)
layer = 0
while alive.any():
    layer += 1
    idx = np.where(alive)[0]
    X = np.concatenate([x[idx] + k * W for k in range(-K, K + 1)])
    Y = np.concatenate([y[idx] for k in range(-K, K + 1)])
    on = []
    for i in idx:
        dx = X - x[i]
        g = Y - y[i] + dx * dx / 2
        r = dx > 0
        l = dx < 0
        hi = np.min(g[r] / dx[r]) if r.any() else np.inf
        lo = np.max(g[l] / dx[l]) if l.any() else -np.inf
        if lo < hi:
            on.append(i)
    assert on
    for i in on:
        alive[i] = False
        bd[i] = layer
print(fn, "N", N, "layers", layer, "mismatches", int((bd != dep).sum()))
