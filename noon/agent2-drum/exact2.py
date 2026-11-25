"""Checks made after the fourth sheet: is the floor found by exact.py real?   usage: python -u exact2.py exact.json
(a) the best free patch polished with more iterations; (b) which limits bind there; (c) the same search with the weight limit raised,
with 80 rings, and with thinning allowed (a ring may be as light as a tenth of the bare skin)."""
import sys, json, math
import numpy as np
from scipy.optimize import minimize
src = open(__file__.replace("exact2.py", "exact.py")).read(); ns = {}; exec(src[:src.index("rng = np.random.default_rng(40)")], ns)      # the functions of exact.py, without its run
E = json.load(open(sys.argv[1]))
def setup(rings, maxmass):
    ns['RINGS'] = rings; ns['EDGE'] = np.arange(rings + 1) / rings; ns['AREA'] = ns['EDGE'][1:] ** 2 - ns['EDGE'][:-1] ** 2; ns['MAXMASS'] = maxmass; ns['cache'].clear()
def minimax_lb(a0, lower, iters=1500):
    R = ns['RINGS']; cons = ns['cons']; AREA = ns['AREA']; MAX = ns['MAXMASS']
    x0 = np.concatenate([a0, [np.abs(cons(a0)[0]).max() * 1.05]])
    cs = [dict(type='ineq', fun=lambda x: x[-1] - cons(x[:-1])[0], jac=lambda x: np.hstack([-cons(x[:-1])[1], np.ones((8, 1))])), dict(type='ineq', fun=lambda x: x[-1] + cons(x[:-1])[0], jac=lambda x: np.hstack([cons(x[:-1])[1], np.ones((8, 1))])),
          dict(type='ineq', fun=lambda x: MAX - x[:-1] @ AREA, jac=lambda x: np.concatenate([-AREA, [0.0]]))]
    r = minimize(lambda x: x[-1], x0, jac=lambda x: np.concatenate([np.zeros(R), [1.0]]), bounds=[(lower, None)] * R + [(0, None)], constraints=cs, method='SLSQP', options=dict(maxiter=iters, ftol=1e-13)); return np.maximum(r.x[:-1], lower)
miss = lambda a, N=None: float(np.abs(ns['misses'](a, N or 50 * ns['RINGS'])).max())
runs = sorted([r for r in E['runs']], key=lambda r: r['miss1'])
print(f"exact.py's twelve starts ended at largest misses from {100 * runs[0]['miss1']:.4f}% to {100 * runs[-1]['miss1']:.4f}%")
setup(40, 12.0); starts = {}
# (a) polish: rerun the minimax from each of the three best end points is not possible (only the misses were kept), so restart from scratch with more iterations
rng = np.random.default_rng(41); best = None
for trial in range(6):
    k = rng.uniform(0.3, 0.6); a0 = rng.uniform(3, 14) * np.clip(1 - (ns['EDGE'][:-1] / k) ** rng.uniform(1, 6), 0, None) + rng.uniform(0, 1.5, 40) * (rng.random(40) < 0.3)
    a1 = minimax_lb(a0, 0.0); a1 = minimax_lb(a1, 0.0); t = miss(a1); print(f"(a) restart {trial + 1}, 3,000 iterations at most: {100 * t:.4f}%; added mass {float(a1 @ ns['AREA']):.2f}", flush=True)
    if best is None or t < best[0]: best = (t, a1)
t, a = best; AREA = ns['AREA']; EDGE = ns['EDGE']; c = ns['cons'](a)[0]
print(f"(b) at the best ({100 * t:.4f}%): added mass {float(a @ AREA):.2f} of 12 allowed; rings with no load {int((a < 1e-6).sum())} of 40; misses of the eight ratios, in %: " + " ".join(f"{100 * (math.exp(x) - 1):+.3f}" for x in c))
print("    load by ring from the centre: " + " ".join(f"{x:.2f}" for x in a)); W = ns['solve'](a, 8000, grad=False); print(f"    with 8,000 cells: {100 * np.abs(W[1:] / W[0] / ns['TARGET'][1:] - 1).max():.4f}%")
out = dict(best40=dict(miss=t, a=a.tolist()))
for label, rings, maxmass, lower in (("(c1) weight limit 50 skins", 40, 50.0, 0.0), ("(c2) 80 rings", 80, 12.0, 0.0), ("(c3) thinning allowed, down to a tenth of the bare skin", 40, 12.0, -0.9)):
    setup(rings, maxmass); a0 = np.repeat(a, rings // 40); a1 = minimax_lb(a0, lower); a1 = minimax_lb(a1, lower); tt = miss(a1)
    print(f"{label}: {100 * tt:.4f}%; added mass {float(a1 @ ns['AREA']):.2f}; lightest ring {a1.min():+.2f}", flush=True); out[label] = dict(miss=tt, a=a1.tolist())
json.dump(out, open("exact2.json", "w"))
