"""Forty more starts for the free radial load at 12 skins, each run long: does any end below the floor?   usage: python -u exact4.py SEED COUNT"""
import sys, numpy as np
from scipy.optimize import minimize
src = open(__file__.replace("exact4.py", "exact.py")).read(); ns = {}; exec(src[:src.index("rng = np.random.default_rng(40)")], ns)
RINGS, EDGE, AREA, cons = ns['RINGS'], ns['EDGE'], ns['AREA'], ns['cons']; rng = np.random.default_rng(int(sys.argv[1]))
def minimax(a0, iters=3000):
    x0 = np.concatenate([a0, [np.abs(cons(a0)[0]).max() * 1.05]])
    cs = [dict(type='ineq', fun=lambda x: x[-1] - cons(x[:-1])[0], jac=lambda x: np.hstack([-cons(x[:-1])[1], np.ones((8, 1))])), dict(type='ineq', fun=lambda x: x[-1] + cons(x[:-1])[0], jac=lambda x: np.hstack([cons(x[:-1])[1], np.ones((8, 1))])),
          dict(type='ineq', fun=lambda x: 12.0 - x[:-1] @ AREA, jac=lambda x: np.concatenate([-AREA, [0.0]]))]
    r = minimize(lambda x: x[-1], x0, jac=lambda x: np.concatenate([np.zeros(RINGS), [1.0]]), bounds=[(0, None)] * RINGS + [(0, None)], constraints=cs, method='SLSQP', options=dict(maxiter=iters, ftol=1e-13)); return np.maximum(r.x[:-1], 0.0)
out = []
for i in range(int(sys.argv[2])):
    kind = i % 3
    if kind == 0: a0 = rng.uniform(0, 30, RINGS) * (EDGE[:-1] < rng.uniform(0.3, 0.9))                       # rough loads out to a random radius
    elif kind == 1: a0 = rng.uniform(0, 60, RINGS) * (rng.random(RINGS) < 0.25)                               # a few heavy rings anywhere
    else: k = rng.uniform(0.3, 0.6); a0 = rng.uniform(3, 14) * np.clip(1 - (EDGE[:-1] / k) ** rng.uniform(1, 6), 0, None)
    a0 = a0 * min(1.0, 12.0 / max(float(a0 @ AREA), 1e-9)); a1 = minimax(minimax(a0)); t = float(np.abs(ns['misses'](a1)).max()); out.append(t)
    print(f"start {i + 1:2d} (kind {kind}): {100 * t:.4f}%; loaded out to {EDGE[np.max(np.nonzero(a1 > 1e-6)[0]) + 1]:.3f}; beyond 0.6: {100 * float(a1[EDGE[:-1] >= 0.6 - 1e-9] @ AREA[EDGE[:-1] >= 0.6 - 1e-9]) / max(float(a1 @ AREA), 1e-9):.0f}% of the mass", flush=True)
print(f"seed {sys.argv[1]}: least {100 * min(out):.4f}%, greatest {100 * max(out):.4f}%; within 0.005 points of the least: {sum(t < min(out) + 5e-5 for t in out)} of {len(out)}")
