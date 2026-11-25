# usage: search.py a|b seed seconds [nr] [cap_mass]
import numpy as np, sys, time, json
from scipy.optimize import minimize
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fem import *

which, seed, budget = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
nr = int(sys.argv[4]) if len(sys.argv) > 4 else 40
cap = float(sys.argv[5]) if len(sys.argv) > 5 else 4.0
P = 6
N = nr * P
fem = Fem(N)
edges = np.linspace(0, 1, nr + 1)
area = edges[1:] ** 2 - edges[:-1] ** 2
rng = np.random.default_rng(seed)
t0 = time.time()
cache = {}


def ratios(a):
    key = a.tobytes()
    if key in cache:
        return cache[key]
    rho = 1.0 + np.repeat(a, P)
    w, G = freqs(fem, rho, None, grads=True)
    g = {k: v.reshape(nr, P).sum(1) for k, v in G.items()}
    if which == "a":
        qs, ks, base, kb = OVER, KOVER, (1, 1), 2.0
    else:
        qs, ks, base, kb = [(1, 1)] + OVER, [2] + KOVER, (0, 1), 1.0
    r = np.array([kb * w[q] / (k * w[base]) for q, k in zip(qs, ks)])
    J = np.array([ri * (g[q] / w[q] - g[base] / w[base]) for ri, q in zip(r, qs)])
    cache.clear()
    cache[key] = (r, J)
    return r, J


def run(a0, corr):
    n = len(corr)
    x0 = np.append(a0, 0.0)
    r, _ = ratios(a0)
    x0[-1] = np.max(np.abs(r - 1 + corr))

    def cf(x):
        r, J = ratios(np.maximum(x[:-1], 0))
        e = r - 1 + corr
        return np.concatenate([x[-1] - e, x[-1] + e, [cap - area @ x[:-1]]])

    def cj(x):
        r, J = ratios(np.maximum(x[:-1], 0))
        o = np.ones((n, 1))
        return np.vstack([np.hstack([-J, o]), np.hstack([J, o]), np.append(-area, 0.0)[None, :]])

    res = minimize(lambda x: x[-1], x0, jac=lambda x: np.append(np.zeros(nr), 1.0), method="SLSQP",
                   bounds=[(0, 400)] * nr + [(0, None)], constraints=[dict(type="ineq", fun=cf, jac=cj)],
                   options=dict(maxiter=400, ftol=1e-10))
    a = np.maximum(res.x[:-1], 0)
    r, _ = ratios(a)
    return a, np.max(np.abs(r - 1 + corr))


def exact(a):
    w = rich(8 * nr, ring_rho(a))
    return report(w)


best = None
k = 0
while time.time() - t0 < budget:
    r = (edges[:-1] + edges[1:]) / 2
    kind = k % 4
    if kind == 0:
        a0 = rng.uniform(4, 14) * (r < rng.uniform(0.3, 0.5))
    elif kind == 1:
        a0 = rng.uniform(2, 20) * np.exp(-((r / rng.uniform(0.2, 0.6)) ** rng.choice([2, 4, 8])))
    elif kind == 2:
        a0 = rng.uniform(0, 8, nr) * (r < rng.uniform(0.3, 0.9))
    else:
        a0 = rng.uniform(3, 12) * (r < rng.uniform(0.25, 0.45)) + rng.uniform(0, 3) * (r > rng.uniform(0.5, 0.9))
    a0 = a0 * min(1.0, cap / max(area @ a0, 1e-9))
    k += 1
    try:
        nm = 7 if which == "a" else 8
        a, m = run(a0, np.zeros(nm))
        if best is None or m < best[1] * 1.5:
            # defect correction: make the coarse grid aim at the extrapolated ratios
            for it in range(2):
                ex = exact(a)
                rex = np.array(ex["ra"] if which == "a" else ex["rb"])
                rc, _ = ratios(a)
                a, m = run(a, rex - (rc - 1))
            ex = exact(a)
            me = ex["missA"] if which == "a" else ex["missB"]
            print("start %d kind %d: coarse %.5f%%  exact miss %.5f%%  place %.4f  mass %.3f  B %.4f  t=%.0fs" % (k, kind, 100 * m, 100 * me, ex["place"], area @ a, ex["B"], time.time() - t0), flush=True)
            if best is None or me < best[1]:
                best = (a, me, ex)
        else:
            print("start %d kind %d: coarse %.5f%% (not polished) t=%.0fs" % (k, kind, 100 * m, time.time() - t0), flush=True)
    except Exception as e:
        print("start", k, "failed", repr(e), flush=True)
a, me, ex = best
print("BEST %s seed %d nr %d cap %g: miss %.5f%% place %.4f mass %.3f B %.4f w11 %.4f" % (which, seed, nr, cap, 100 * me, ex["place"], area @ a, ex["B"], ex["w11"]))
print(" missA %.5f%% missB %.5f%%" % (100 * ex["missA"], 100 * ex["missB"]))
json.dump(dict(a=list(a), miss=me, place=ex["place"], B=ex["B"]), open("best-%s-%d-%d-%g.json" % (which, seed, nr, cap), "w"))
