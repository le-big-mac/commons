"""The least largest miss against the weight allowed, for any radial load and for loads that may not increase outward.
usage: python -u exact3.py WEIGHT     (one weight a run; unregistered; after the fourth sheet)"""
import json, math, sys
import numpy as np
from scipy.optimize import minimize
src = open(__file__.replace("exact3.py", "exact.py")).read(); ns = {}; exec(src[:src.index("rng = np.random.default_rng(40)")], ns)
RINGS, EDGE, AREA, cons = ns['RINGS'], ns['EDGE'], ns['AREA'], ns['cons']
def minimax(a0, maxmass, monotone, iters=1500):
    x0 = np.concatenate([a0, [np.abs(cons(a0)[0]).max() * 1.05]])
    cs = [dict(type='ineq', fun=lambda x: x[-1] - cons(x[:-1])[0], jac=lambda x: np.hstack([-cons(x[:-1])[1], np.ones((8, 1))])), dict(type='ineq', fun=lambda x: x[-1] + cons(x[:-1])[0], jac=lambda x: np.hstack([cons(x[:-1])[1], np.ones((8, 1))])),
          dict(type='ineq', fun=lambda x: maxmass - x[:-1] @ AREA, jac=lambda x: np.concatenate([-AREA, [0.0]]))]
    if monotone:
        D = np.zeros((RINGS - 1, RINGS + 1)); D[np.arange(RINGS - 1), np.arange(RINGS - 1)] = 1; D[np.arange(RINGS - 1), np.arange(1, RINGS)] = -1; cs.append(dict(type='ineq', fun=lambda x: D @ x, jac=lambda x: D))
    r = minimize(lambda x: x[-1], x0, jac=lambda x: np.concatenate([np.zeros(RINGS), [1.0]]), bounds=[(0, None)] * RINGS + [(0, None)], constraints=cs, method='SLSQP', options=dict(maxiter=iters, ftol=1e-13)); return np.maximum(r.x[:-1], 0.0)
miss = lambda a: float(np.abs(ns['misses'](a)).max()); discs = ns['discs']; rng = np.random.default_rng(43)
for M in (float(sys.argv[1]),):
    res = []
    for mono in (False, True):
        best = None
        for trial in range(3):
            if trial == 0: a0 = discs([8.94], [0.4004])
            elif trial == 1: a0 = discs([12.94, 5.63], [0.438, 0.234])
            else: k = rng.uniform(0.3, 0.55); a0 = rng.uniform(3, 12) * np.clip(1 - (EDGE[:-1] / k) ** rng.uniform(1, 6), 0, None)
            a0 = a0 * min(1.0, M / float(a0 @ AREA))
            if mono: a0 = np.maximum.accumulate(a0[::-1])[::-1]; a0 = a0 * min(1.0, M / float(a0 @ AREA))
            a1 = minimax(minimax(a0, M, mono), M, mono); t = miss(a1)
            if best is None or t < best[0]: best = (t, a1)
        t, a = best; json.dump(dict(weight=M, monotone=mono, miss=t, a=a.tolist()), open(f"profile-{M:g}-{'piled' if mono else 'free'}.json", "w")); res.append(f"{100 * t:.3f}% (used {float(a @ AREA):.2f}; loaded out to {EDGE[np.max(np.nonzero(a > 1e-6)[0]) + 1] if (a > 1e-6).any() else 0:.3f}; {int((np.abs(np.diff(a)) > 0.05).sum())} steps)")
    print(f"   {M:5.2f}                 {res[0]:42s} {res[1]}", flush=True)
