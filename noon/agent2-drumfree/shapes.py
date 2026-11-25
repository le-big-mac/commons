"""Other shapes of load with the lowest mode free.   usage: python -u shapes.py piled|step|two SET WEIGHT OUT.json
piled: discs piled on discs (no ring heavier than one nearer the centre), 40 and 80 rings, the weight may be anything up to WEIGHT
step:  one smooth step (mass per area rising as a hyperbolic tangent; place, width and weight free up to WEIGHT), 1,000 cells
two:   two even discs with free radii and any total weight up to WEIGHT, 800 cells"""
import sys, json, math
import numpy as np
from scipy.optimize import minimize, differential_evolution
import libfree as F
L = F.L; kind, name, M = sys.argv[1], sys.argv[2], float(sys.argv[3]); modes = F.SETS[name]; A = dict(kind=kind, set=name, weight=M)
if kind == "piled":
    rng = np.random.default_rng(31 + int(10 * M)); prev = None; A['rings'] = {}
    for R in (40, 80):
        sk = F.FreeSkin(R, modes); starts = [L.disc(sk, M / 0.16, 0.4), L.disc(sk, M / 0.25, 0.5), L.disc(sk, 0.9 * M / 0.19, 0.436) + L.disc(sk, 0.1 * M / 0.05, 0.224)] + ([np.repeat(prev, 2)] if prev is not None else []) + [rng.uniform(0, 30, R) * (sk.E[:-1] < rng.uniform(0.3, 0.9)) for _ in range(10)]
        ends = [L.slp(sk, a0, M, monotone=True) for a0 in starts]; a, f = min(ends, key=lambda z: z[1]); prev = a; ex, pl = F.exact(a, modes); A['rings'][str(R)] = dict(miss=f, exact=ex, place=pl, a=a.tolist(), used=sk.mass(a), agree=sum(e[1] < f + 2e-5 for e in ends), n=len(ends))
        print(f"piled discs, {name}, up to {M:g} skins, {R} rings: least {100 * f:.4f}% ({100 * ex:.4f}% exact); used {sk.mass(a):.2f}; place {pl:.4f}; {A['rings'][str(R)]['agree']} of {len(ends)} searches within 0.002 points", flush=True)
if kind == "step":
    N = 1000; sk = F.FreeSkin(N, modes, per=1); r = sk.r
    def load(x):
        k, xi, frac = min(0.95, max(0.05, x[0])), min(1.0, max(0.003, x[1])), min(1.0, max(0.02, x[2])); shape = 0.5 * (1 - np.tanh((r - k) / xi)); return shape * frac * M / float(shape @ sk.A), (k, xi, frac)
    best = None
    for x0 in ((0.4, 0.09, 1.0), (0.49, 0.09, 1.0), (0.5, 0.2, 0.5), (0.55, 0.05, 0.6), (0.45, 0.01, 1.0), (0.5, 0.1, 0.3)):
        res = minimize(lambda x: sk.miss(load(x)[0]), x0, method='Nelder-Mead', options=dict(xatol=1e-5, fatol=1e-9, maxiter=600))
        if best is None or res.fun < best.fun: best = res
    a, (k, xi, frac) = load(best.x); A.update(miss=float(best.fun), k=float(k), xi=float(xi), used=float(frac * M), centre=float(1 + a[0]), place=F.place(a, per=1))
    print(f"one smooth step, {name}, up to {M:g} skins: least {100 * best.fun:.3f}% (centre {1 + a[0]:.2f} times the skin, half-way radius {k:.3f}, width {xi:.3f}, {frac * M:.2f} skins used); place {A['place']:.4f}", flush=True)
if kind == "two":
    N = 800; sk = F.FreeSkin(N, modes, per=1)
    def load(y):
        ko, ki, share, frac = max(y[0], y[1]), min(y[0], y[1]), y[2], y[3]; e = sk.E; return sum(l * np.clip((np.minimum(k, e[1:]) ** 2 - e[:-1] ** 2) / sk.A, 0, 1) for l, k in ((share * frac * M / ko ** 2, ko), ((1 - share) * frac * M / ki ** 2, ki)))
    best = None
    for seed in (4, 5):
        res = differential_evolution(lambda y: sk.miss(load(y)), [(0.2, 0.9), (0.05, 0.7), (0.0, 1.0), (0.1, 1.0)], seed=seed, tol=1e-7, maxiter=200, popsize=15)
        if best is None or res.fun < best.fun: best = res
    x = best.x; A.update(miss=float(best.fun), radii=[float(max(x[0], x[1])), float(min(x[0], x[1]))], share=float(x[2]), used=float(x[3] * M), place=F.place(load(x), per=1))
    print(f"two discs, {name}, up to {M:g} skins: least {100 * best.fun:.3f}% with {x[3] * M:.2f} skins; radii {max(x[0], x[1]):.3f} and {min(x[0], x[1]):.3f}; place {A['place']:.4f}", flush=True)
json.dump(A, open(sys.argv[4], "w"))
