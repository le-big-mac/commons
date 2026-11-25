"""Is the least found by the two walks (exact5.py) the least there is?  Shake the best answer and search again.
usage: python -u exact6.py shake WEIGHT PART     PART 0: the answer moved by one ring either way and stretched by 0.92, 0.96, 1.04, 1.08;
                                                 PART 1, 2, ...: five copies with each ring's load multiplied by a random factor (seed 60 + PART)
       python -u exact6.py fine                  from the best answer at 12 skins: 8,000 cells; 80 rings; weight limits 24 and 50; thinning allowed
(unregistered; one process each, one thread)"""
import json, sys
import numpy as np
from scipy.optimize import minimize
src = open(__file__.replace("exact6.py", "exact.py")).read(); ns = {}; exec(src[:src.index("rng = np.random.default_rng(40)")], ns)
def setup(rings, maxmass): ns['RINGS'] = rings; ns['EDGE'] = np.arange(rings + 1) / rings; ns['AREA'] = ns['EDGE'][1:] ** 2 - ns['EDGE'][:-1] ** 2; ns['MAXMASS'] = maxmass; ns['cache'].clear()
def minimax(a0, lower=0.0, iters=2000):
    R = ns['RINGS']; cons = ns['cons']; AREA = ns['AREA']; MAX = ns['MAXMASS']; x0 = np.concatenate([a0, [np.abs(cons(a0)[0]).max() * 1.05]])
    cs = [dict(type='ineq', fun=lambda x: x[-1] - cons(x[:-1])[0], jac=lambda x: np.hstack([-cons(x[:-1])[1], np.ones((8, 1))])), dict(type='ineq', fun=lambda x: x[-1] + cons(x[:-1])[0], jac=lambda x: np.hstack([cons(x[:-1])[1], np.ones((8, 1))])),
          dict(type='ineq', fun=lambda x: MAX - x[:-1] @ AREA, jac=lambda x: np.concatenate([-AREA, [0.0]]))]
    r = minimize(lambda x: x[-1], x0, jac=lambda x: np.concatenate([np.zeros(R), [1.0]]), bounds=[(lower, None)] * R + [(0, None)], constraints=cs, method='SLSQP', options=dict(maxiter=iters, ftol=1e-13)); return np.maximum(r.x[:-1], lower)
miss = lambda a, N=None: float(np.abs(ns['misses'](a, N or 50 * ns['RINGS'])).max())
def best_of_chains(M):
    rows = [r for w in ("down", "up") for r in json.load(open(f"chain-free-{w}.json")) if abs(r['weight'] - M) < 1e-9]; r = min(rows, key=lambda r: r['miss']); return np.array(r['a']), r['miss']
def stretched(a, f):
    """the same load with every radius multiplied by f, averaged back onto the 40 rings by area"""
    N = 2000; r = (np.arange(N) + 0.5) / N; src_ring = np.floor(r / f * 40).astype(int); v = np.where(src_ring < 40, a[np.minimum(src_ring, 39)], 0.0); return (v * r).reshape(40, 50).sum(axis=1) / r.reshape(40, 50).sum(axis=1)
if sys.argv[1] == "shake":
    M = float(sys.argv[2]); part = int(sys.argv[3]); setup(40, M); a, t0 = best_of_chains(M); AREA = ns['AREA']; starts = []
    if part == 0: starts = [("moved one ring inward", np.concatenate([a[1:], [0.0]])), ("moved one ring outward", np.concatenate([[a[0]], a[:-1]]))] + [(f"stretched by {f}", stretched(a, f)) for f in (0.92, 0.96, 1.04, 1.08)]
    else:
        rng = np.random.default_rng(60 + part); starts = [(f"shaken {part}.{i + 1}", a * np.exp(0.4 * rng.standard_normal(40)) + (rng.random(40) < 0.15) * rng.uniform(0, 0.3 * a.max(), 40)) for i in range(5)]
    best = (t0, a, "the walks' answer")
    for name, a0 in starts:
        a0 = a0 * min(1.0, M / float(a0 @ AREA)); a1 = minimax(minimax(a0)); t = miss(a1); print(f"weight {M:5.2f}, {name}: {100 * t:.4f}% (the walks' answer {100 * t0:.4f}%)", flush=True)
        if t < best[0]: best = (t, a1, name)
    json.dump(dict(weight=M, miss=best[0], a=best[1].tolist(), start=best[2]), open(f"shake-{M:g}-{part}.json", "w"))
else:
    a, t0 = best_of_chains(12.0); setup(40, 12.0); out = {}
    print(f"the walks' answer at 12 skins: {100 * t0:.4f}% with 2,000 cells; {100 * miss(a, 8000):.4f}% with 8,000", flush=True)
    for label, rings, maxmass, lower in (("80 rings", 80, 12.0, 0.0), ("weight limit 24 skins", 40, 24.0, 0.0), ("weight limit 50 skins", 40, 50.0, 0.0), ("thinning allowed, down to a tenth of the bare skin", 40, 12.0, -0.9)):
        setup(rings, maxmass); a1 = minimax(minimax(np.repeat(a, rings // 40), lower), lower); t = miss(a1); out[label] = dict(miss=t, a=a1.tolist())
        print(f"{label}: {100 * t:.4f}%; added mass {float(a1 @ ns['AREA']):.2f}; lightest ring {a1.min():+.2f}; loaded out to {ns['EDGE'][np.max(np.nonzero(a1 > 1e-6)[0]) + 1]:.4f}", flush=True); json.dump(out, open("fine.json", "w"))
