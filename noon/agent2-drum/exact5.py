"""The weight table again, by continuation: at each weight the search starts from the answer at the weight before it
(scaled to fit), walking down from 12 skins or up from 1, as well as from the best one even disc of that weight.
usage: python -u exact5.py free|piled down|up OUT.json     (unregistered; a check on exact3.py's table, which used three starts a weight)"""
import json, sys
import numpy as np
from scipy.optimize import minimize
src = open(__file__.replace("exact5.py", "exact.py")).read(); ns = {}; exec(src[:src.index("rng = np.random.default_rng(40)")], ns)
RINGS, EDGE, AREA, cons, discs = ns['RINGS'], ns['EDGE'], ns['AREA'], ns['cons'], ns['discs']
WEIGHTS = [1.0, 1.1, 1.2, 1.3, 1.43, 1.7, 2.0, 2.79, 4.0, 6.0, 9.6, 12.0]
def minimax(a0, maxmass, monotone, iters=2000):
    x0 = np.concatenate([a0, [np.abs(cons(a0)[0]).max() * 1.05]])
    cs = [dict(type='ineq', fun=lambda x: x[-1] - cons(x[:-1])[0], jac=lambda x: np.hstack([-cons(x[:-1])[1], np.ones((8, 1))])), dict(type='ineq', fun=lambda x: x[-1] + cons(x[:-1])[0], jac=lambda x: np.hstack([cons(x[:-1])[1], np.ones((8, 1))])),
          dict(type='ineq', fun=lambda x: maxmass - x[:-1] @ AREA, jac=lambda x: np.concatenate([-AREA, [0.0]]))]
    if monotone:
        D = np.zeros((RINGS - 1, RINGS + 1)); D[np.arange(RINGS - 1), np.arange(RINGS - 1)] = 1; D[np.arange(RINGS - 1), np.arange(1, RINGS)] = -1; cs.append(dict(type='ineq', fun=lambda x: D @ x, jac=lambda x: D))
    r = minimize(lambda x: x[-1], x0, jac=lambda x: np.concatenate([np.zeros(RINGS), [1.0]]), bounds=[(0, None)] * RINGS + [(0, None)], constraints=cs, method='SLSQP', options=dict(maxiter=iters, ftol=1e-13)); return np.maximum(r.x[:-1], 0.0)
miss = lambda a: float(np.abs(ns['misses'](a)).max())
def onedisc(M):
    """the best one even disc of added mass M whose edge is on a ring's edge (so that it is exact on these rings)"""
    best = None
    for j in range(4, 33):
        k = EDGE[j]; a = discs([M / k ** 2], [k]); t = miss(a)
        if best is None or t < best[0]: best = (t, a, k)
    return best
kind, way = sys.argv[1], sys.argv[2]; mono = kind == "piled"; order = WEIGHTS[::-1] if way == "down" else WEIGHTS; prev = None; out = []
if way == "down": prev = np.array(json.load(open("exact.json"))['monotone']['a'] if mono else json.load(open("exact2.json"))['best40']['a'])
for M in order:
    t1, a1, k1 = onedisc(M); starts = [("one disc", a1)]
    if prev is not None:
        a0 = prev * min(1.0, M / float(prev @ AREA)); starts.append(("the weight before", a0))
    best = None
    for name, a0 in starts:
        if mono: a0 = np.maximum.accumulate(a0[::-1])[::-1]; a0 = a0 * min(1.0, M / float(a0 @ AREA))
        a = minimax(minimax(a0, M, mono), M, mono); t = miss(a)
        if t > miss(a0): a, t = a0, miss(a0)                      # a search that ends worse than it began keeps its start
        if best is None or t < best[0]: best = (t, a, name)
    t, a, name = best; prev = a; out.append(dict(weight=M, miss=t, a=a.tolist(), start=name, onedisc=t1, onedisc_k=float(k1)))
    print(f"{kind:5s} {way:4s} {M:5.2f}: {100 * t:.3f}% from '{name}' (used {float(a @ AREA):.2f}; loaded out to {EDGE[np.max(np.nonzero(a > 1e-6)[0]) + 1]:.3f}); the best one even disc on a ring's edge: {100 * t1:.3f}% (to {k1:.3f})", flush=True)
    json.dump(out, open(sys.argv[3], "w"))
