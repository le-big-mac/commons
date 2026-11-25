# usage: search2.py a|b|c START.json|rand cap minmass seconds [tube]
# a: seven overtones over the note; b: eight over the lowest; c: aimed (lowest at 1.10 notes, seven overtones)
import numpy as np, sys, os, time, json
from scipy.optimize import minimize
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fem import *

which, start, cap, minmass, budget = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
tube = len(sys.argv) > 6 and sys.argv[6] == "tube"
rmax = int(sys.argv[6][2:]) if len(sys.argv) > 6 and sys.argv[6].startswith("in") else 40
nr, P = 40, 6
fem = Fem(nr * P)
edges = np.linspace(0, 1, nr + 1)
area = edges[1:] ** 2 - edges[:-1] ** 2
X0 = 2 * np.pi * 440 * 0.125 / 343.0
t0 = time.time()
cache = {}
if which == "a":
    qs, ks, base, kb = OVER, KOVER, (1, 1), 2.0
elif which == "b":
    qs, ks, base, kb = [(1, 1)] + OVER, [2] + KOVER, (0, 1), 1.0
else:
    qs, ks, base, kb = [(0, 1)] + OVER, [1.10] + KOVER, (1, 1), 2.0


def ratios(a):
    key = a.tobytes()
    if key in cache:
        return cache[key]
    w, G = freqs(fem, 1.0 + np.repeat(a, P), None, grads=True)
    g = {k: v.reshape(nr, P).sum(1) for k, v in G.items()}
    r = np.array([kb * w[q] / (k * w[base]) for q, k in zip(qs, ks)])
    J = np.array([ri * (g[q] / w[q] - g[base] / w[base]) for ri, q in zip(r, qs)])
    cache.clear()
    cache[key] = (r, J)
    return r, J


def run(a0, corr):
    n = len(corr)
    r, _ = ratios(a0)
    x0 = np.append(a0, np.max(np.abs(r - 1 + corr)))

    def cf(x):
        r, J = ratios(np.maximum(x[:-1], 0))
        e = r - 1 + corr
        return np.concatenate([x[-1] - e, x[-1] + e, [cap - area @ x[:-1], area @ x[:-1] - minmass]])

    def cj(x):
        r, J = ratios(np.maximum(x[:-1], 0))
        o = np.ones((n, 1))
        return np.vstack([np.hstack([-J, o]), np.hstack([J, o]), np.append(-area, 0.0)[None, :], np.append(area, 0.0)[None, :]])

    res = minimize(lambda x: x[-1], x0, jac=lambda x: np.append(np.zeros(nr), 1.0), method="SLSQP",
                   bounds=[(0, 1000)] * rmax + [(0, 0)] * (nr - rmax) + [(0, None)], constraints=[dict(type="ineq", fun=cf, jac=cj)], options=dict(maxiter=300, ftol=1e-11))
    return np.maximum(res.x[:-1], 0)


def m0(a, B, Ns=320):
    f1, f2 = Fem(Ns), Fem(2 * Ns)
    l1 = f1.modes(ring_rho(a)(Ns), 0, 3, B)[0]
    l2 = f2.modes(ring_rho(a)(2 * Ns), 0, 3, B)[0]
    return np.sqrt((4 * l2 - l1) / 3)


def exact_ratios(a):
    """exact (Richardson) ratios in the order of qs; with the tube if asked"""
    w = rich(320, ring_rho(a))
    if tube:
        for n in (1, 2, 3):
            x_w = w[(0, n)]
            for it in range(80):
                x = X0 * x_w / w[(1, 1)]
                wn = m0(a, w["B"] * x / np.tan(x))[n - 1]
                if abs(wn - x_w) < 1e-9:
                    break
                x_w = 0.5 * (x_w + wn)
            w[(0, n)] = x_w
    return np.array([kb * w[q] / (k * w[base]) for q, k in zip(qs, ks)]), 2 * w[(0, 1)] / w[(1, 1)], w["B"]


def polish(a, rounds):
    corr = np.zeros(len(qs))
    hist = []
    for it in range(rounds):
        a = run(a, corr)
        rex, place, B = exact_ratios(a)
        rc, _ = ratios(a)
        corr = rex - rc
        hist.append((np.max(np.abs(rex - 1)), place, area @ a, B))
        print("   round %d: exact miss %.4f%% place %.4f mass %.3f B %.4f  worst mode %s  t=%.0fs" % (it, 100 * hist[-1][0], place, area @ a, B, qs[int(np.argmax(np.abs(rex - 1)))], time.time() - t0), flush=True)
        if time.time() - t0 > budget:
            break
    return a, hist


if start != "rand":
    j = json.load(open(start))
    a0 = np.maximum(np.array(j["a"]), 0)
    if area @ a0 < minmass:
        a0 = a0 * (minmass * 1.0001 / (area @ a0))
    rex, place, B = exact_ratios(a0)
    print("%s %s cap %g minmass %g tube %s: start exact miss %.4f%% place %.4f mass %.3f" % (which, os.path.basename(start), cap, minmass, tube, 100 * np.max(np.abs(rex - 1)), place, area @ a0), flush=True)
    a, hist = polish(a0, 6 if tube else 4)
    best = (a, hist[-1][0])
else:
    rng = np.random.default_rng(int(cap * 10 + minmass))
    best = None
    k = 0
    r = (edges[:-1] + edges[1:]) / 2
    while time.time() - t0 < budget:
        k += 1
        if k % 2:
            a0 = rng.uniform(5, 30) * (r < rng.uniform(0.35, 0.6))
        else:
            a0 = rng.uniform(0, 40, nr) * (r < rng.uniform(0.3, 0.7))
        a0 = a0 * rng.uniform(max(minmass, 2), cap) / (area @ a0)
        print("random start %d, mass %.2f" % (k, area @ a0), flush=True)
        a, hist = polish(a0, 2)
        if best is None or hist[-1][0] < best[1]:
            best = (a, hist[-1][0])
json.dump(dict(a=list(best[0]), miss=best[1]), open("s2-%s-%g-%g-%d.json" % (which, cap, minmass, rmax), "w"))
print("END %s %s cap %g minmass %g tube %s: best exact miss %.4f%% mass %.3f" % (which, os.path.basename(start), cap, minmass, tube, 100 * best[1], area @ best[0]))
