"""Checks made after the sealed sheet was scored; none was registered.   usage: python -u after.py SECTION ARGS... OUT.json
W SET up|down      the weight walked up or down on 40 rings, each search starting from the answer before it (and from search12's answer)
N FAMILIES WEIGHT  more families of modes: all modes of harmonics 1 to FAMILIES (5: nine modes, 6: twelve, 7: sixteen, 8: twenty, 9: twenty-five, 10: thirty)
T                  how exactly the loads must be made
P SET WEIGHT       discs piled on discs (no ring heavier than one nearer the centre), 40 and 80 rings
2 SET WEIGHT       two even discs with free radii, by differential evolution"""
import sys, json, math, os, time
import numpy as np
import lib12 as L
SEC = sys.argv[1]; OUT = sys.argv[-1]; A = {}
def family(F): return [(m, (l - m + 1) // 2) for l in range(1, F + 1) for m in range(l - 1, -1, -2)]
def S(name, M, R=40): return np.array(json.load(open(f"s-{name}-{M:g}.json"))['rings'][str(R)]['a'])
def wmax_for(a, modes, R):
    sk = L.Skin(R, [(0, 1)] + [max(modes, key=lambda mn: mn[0] + 2 * mn[1])]); c = sk.solve(a, grad=False); top = (c[0] + 1) * sk.T[1]
    from scipy.linalg import eigh_tridiagonal
    rho = 1.0 + np.repeat(a, sk.per); sc = np.sqrt(sk.r * rho); w0 = math.sqrt(eigh_tridiagonal(sk.diag[0] / sc ** 2, sk.off / (sc[:-1] * sc[1:]), select='i', select_range=(0, 0))[0][0]); return 1.5 * top * w0 + 1
if SEC == 'W':
    name, way = sys.argv[2], sys.argv[3]; modes = L.SETS[name]; sk = L.Skin(40, modes); W = [1.0, 1.43, 1.6, 1.8, 2.0, 2.2, 2.4, 2.79, 4.0, 6.0, 9.6, 12.0]; order = W if way == "up" else W[::-1]; prev = None; A['walk'] = []
    for M in order:
        starts = []
        if prev is not None: starts.append(("the weight before", prev * min(1.0, M / sk.mass(prev))))
        if os.path.exists(f"s-{name}-{M:g}.json"): starts.append(("search12's answer", S(name, M)))
        if not starts: starts.append(("one disc", L.disc(sk, M / 0.16, 0.4)))
        best = None
        for nm, a0 in starts:
            a, f = L.slp(sk, a0, M)
            if best is None or f < best[0]: best = (f, a, nm)
        f, a, nm = best; prev = a; A['walk'].append(dict(weight=M, miss=f, a=a.tolist(), start=nm, D=L.D(a)))
        print(f"{name} {way:4s} {M:5.2f}: {100 * f:.4f}% from '{nm}'; D = {L.D(a):.1f}", flush=True); json.dump(A, open(OUT, "w"))
if SEC == 'N':
    F, M = int(sys.argv[2]), float(sys.argv[3]); modes = family(F); rng = np.random.default_rng(100 * F + int(M)); prev = None; A = dict(F=F, weight=M, modes=modes, rings={})
    for R in (40, 80):
        sk = L.Skin(R, modes); t0 = time.time(); seed = S("sixteen", M if M in (12.0, 4.0, 2.79, 6.0, 9.6) else 12.0, R); starts = [("the sixteen-mode load", seed * min(1.0, M / sk.mass(seed))), ("one disc", L.disc(sk, M / 0.16, 0.4))]
        if prev is not None: starts.append(("the answer with half as many rings", np.repeat(prev, 2)))
        for i in range(6): starts.append((f"shaken {i + 1}", seed * min(1.0, M / sk.mass(seed)) * np.exp(0.5 * rng.standard_normal(R))))
        for i in range(6):
            a0 = np.zeros(R)
            for _ in range(rng.integers(2, 7)): lo = rng.uniform(0, 0.7); a0 += rng.uniform(2, 60) * ((sk.E[:-1] >= lo) & (sk.E[:-1] < lo + rng.uniform(0.02, 0.2)))
            starts.append((f"random {i + 1}", a0))
        ends = []; best = None
        for nm, a0 in starts:
            a, f = L.slp(sk, a0, M); ends.append(f)
            if best is None or f < best[0]: best = (f, a, nm)
        for i in range(3):
            a, f = L.slp(sk, best[1] * np.exp(0.3 * rng.standard_normal(R)), M); ends.append(f)
            if f < best[0]: best = (f, a, f"the best, shaken {i + 1}")
        f, a, nm = best; prev = a; ex = L.exact_miss(a, modes) if True else None; r = L.exact_ratios(a, modes, wmax=wmax_for(a, modes, R))
        A['rings'][str(R)] = dict(miss=f, exact=ex, a=a.tolist(), ratios=r.tolist(), ends=ends, D=L.D(a), loaded_to=float(sk.E[np.max(np.nonzero(a > 1e-6)[0]) + 1]))
        print(f"{len(modes)} modes ({F} harmonics), {M:g} skins, {R} rings: least {100 * f:.4f}% ({100 * ex:.4f}% by exact matching) from '{nm}'; {sum(e < f + 2e-5 for e in ends)} of {len(ends)} within 0.002 points; loaded out to {A['rings'][str(R)]['loaded_to']:.3f}; D = {A['rings'][str(R)]['D']:.1f}; {time.time() - t0:.0f} s", flush=True); json.dump(A, open(OUT, "w"))
if SEC == 'R':
    name, M = sys.argv[2], float(sys.argv[3]); modes = L.SETS[name]; rng = np.random.default_rng(160 + int(M)); a80 = S(name, M, 80); sk = L.Skin(160, modes); t0 = time.time(); start = np.repeat(a80, 2); f0 = sk.miss(start)
    ends = [L.slp(sk, start, M)] + [L.slp(sk, start * np.exp(0.2 * rng.standard_normal(160)), M) for _ in range(3)]; a, f = min(ends, key=lambda z: z[1]); ex = L.exact_miss(a, modes)
    A = dict(set=name, weight=M, start=f0, miss=f, exact=ex, a=a.tolist(), ends=[e[1] for e in ends], moved=float(np.abs(a - start).max()))
    print(f"160 rings, {name}, {M:g} skins: the 80-ring answer split in two gives {100 * f0:.4f}%; after the search {100 * f:.4f}% ({100 * ex:.4f}% by exact matching); the four searches ended at " + ", ".join(f"{100 * e[1]:.4f}%" for e in ends) + f"; the largest change in any ring's load {A['moved']:.1f}; {time.time() - t0:.0f} s", flush=True); json.dump(A, open(OUT, "w"))
if SEC == 'I':
    from scipy.linalg import eigh_tridiagonal
    print("I. Are the tuned modes the lowest modes? Every mode (m up to 14, n up to 8) below the top harmonic plus a half, by finite differences"); A['intruders'] = []
    def spectrum(a):
        R = len(a); N = R * 50; h = 1.0 / N; r = (np.arange(N) + 0.5) * h; re = np.arange(N + 1) * h; rho = 1 + np.repeat(a, 50); sc = np.sqrt(r * rho); out = []; w01 = None
        for m in range(15):
            d = (re[:-1] + re[1:]) / (h * h) + m * m / r; d[-1] += re[-1] / (h * h); w = np.sqrt(eigh_tridiagonal(d / sc ** 2, -re[1:-1] / (h * h) / (sc[:-1] * sc[1:]), select='i', select_range=(0, 7))[0]); w01 = w[0] if m == 0 else w01
            out += [(w[j] / w01, m, j + 1) for j in range(8)]
        return sorted(out)
    cases = [("a plain skin", np.zeros(40), 7), ("nine modes, 1.43 skins", np.array(json.load(open("../drum/rings2-free-1.43.json"))['rings']['40']['a']), 5), ("twelve modes, 2.79 skins", S("twelve", 2.79), 6), ("twelve modes, 12 skins", S("twelve", 12), 6), ("sixteen modes, 4 skins", S("sixteen", 4), 7), ("sixteen modes, 12 skins", S("sixteen", 12), 7)]
    for F in (8, 9, 10):
        f = f"after-N-{F}-12.json"
        if os.path.exists(f): cases.append((f"{len(family(F))} modes, 12 skins", np.array(json.load(open(f))['rings']['40']['a']), F))
    for name, a, F in cases:
        sp = spectrum(a); fam = set(map(tuple, family(F))); low = [(x, m, n) for x, m, n in sp if x < F + 0.5]; out = [(x, m, n) for x, m, n in low if (m, n) not in fam]; inset = [(x, m, n) for x, m, n in low if (m, n) in fam]
        A['intruders'].append(dict(name=name, F=F, inset=len(inset), of=len(fam), intruders=[(float(x), m, n) for x, m, n in out]))
        print(f"   {name} ({F} harmonics): {len(inset)} of the set's {len(fam)} modes lie below {F + 0.5}; other modes below it: " + (", ".join(f"({m},{n}) at {x:.2f}" for x, m, n in out) if out else "none"), flush=True)
    json.dump(A, open(OUT, "w"))
if SEC == 'Q':
    from scipy.optimize import minimize
    print("Q. Another measure: the root mean square of the misses made least (40 rings; a gradient search from the least-largest-miss load and from one disc)"); A['rms'] = []
    for name, M in (("twelve", 2.79), ("sixteen", 4.0), ("sixteen", 12.0)):
        sk = L.Skin(40, L.SETS[name]); a0 = S(name, M); K = len(sk.modes) - 1
        def obj(a): c, J = sk.solve(a); return float(c @ c) / K * 1e4, 2e4 * (J.T @ c) / K
        best = None
        for start in (a0, L.disc(sk, M / 0.16, 0.4)):
            r = minimize(obj, sk.fit(start, M), jac=True, method='SLSQP', bounds=[(0, None)] * 40, constraints=[dict(type='ineq', fun=lambda a: M - a @ sk.A, jac=lambda a: -sk.A)], options=dict(maxiter=3000, ftol=1e-14))
            if best is None or r.fun < best.fun: best = r
        a = np.maximum(best.x, 0); c = sk.solve(a, grad=False); c0 = sk.solve(a0, grad=False); row = dict(set=name, weight=M, rms=float(np.sqrt(c @ c / K)), largest=float(np.abs(c).max()), D=L.D(a), rms0=float(np.sqrt(c0 @ c0 / K)), largest0=float(np.abs(c0).max()), D0=L.D(a0), a=a.tolist()); A['rms'].append(row)
        print(f"   {name}, {M:g} skins: least root-mean-square miss {100 * row['rms']:.3f}% (its largest miss {100 * row['largest']:.3f}%, D = {row['D']:.1f} cents); the least-largest-miss load has root mean square {100 * row['rms0']:.3f}%, largest {100 * row['largest0']:.3f}%, D = {row['D0']:.1f}", flush=True)
    json.dump(A, open(OUT, "w"))
if SEC == 'T':
    rng = np.random.default_rng(12); A['tol'] = []
    print("T. Each ring's load off by a random share (400 draws each; standard deviation given); the largest miss over the set's own modes")
    for name, M in (("twelve", 2.79), ("twelve", 12.0), ("sixteen", 4.0), ("sixteen", 12.0)):
        a = S(name, M); sk = L.Skin(40, L.SETS[name]); base = sk.miss(a); row = dict(set=name, weight=M, base=base)
        for eps in (0.01, 0.03):
            v = np.array([sk.miss(a * (1 + eps * rng.standard_normal(40))) for _ in range(400)]); row[str(eps)] = (float(np.median(v)), float(np.quantile(v, 0.9)), float(v.max()))
        b = np.concatenate([[a[0]], a[:-1]]); row['moved'] = sk.miss(b); A['tol'].append(row)
        print(f"   {name}, {M:g} skins: as found {100 * base:.2f}%; off by 1%: median {100 * row['0.01'][0]:.2f}%, worst {100 * row['0.01'][2]:.2f}%; off by 3%: median {100 * row['0.03'][0]:.2f}%, worst {100 * row['0.03'][2]:.2f}%; the whole load moved outward one ring: {100 * row['moved']:.2f}%", flush=True)
    json.dump(A, open(OUT, "w"))
if SEC == 'P':
    name, M = sys.argv[2], float(sys.argv[3]); modes = L.SETS[name]; rng = np.random.default_rng(7 + int(10 * M)); prev = None; A = dict(set=name, weight=M, rings={})
    for R in (40, 80):
        sk = L.Skin(R, modes); starts = [L.disc(sk, M / 0.16, 0.4), L.disc(sk, 0.9 * M / 0.19, 0.436) + L.disc(sk, 0.1 * M / 0.05, 0.224), S(name, M, R)] + ([np.repeat(prev, 2)] if prev is not None else []) + [rng.uniform(0, 30, R) * (sk.E[:-1] < rng.uniform(0.3, 0.9)) for _ in range(10)]
        ends = [L.slp(sk, a0, M, monotone=True) for a0 in starts]; a, f = min(ends, key=lambda z: z[1]); prev = a; A['rings'][str(R)] = dict(miss=f, exact=L.exact_miss(a, modes), a=a.tolist(), agree=sum(e[1] < f + 2e-5 for e in ends), n=len(ends))
        print(f"piled discs, {name}, {M:g} skins, {R} rings: least {100 * f:.4f}% ({100 * A['rings'][str(R)]['exact']:.4f}% by exact matching); {A['rings'][str(R)]['agree']} of {len(ends)} searches within 0.002 points", flush=True); json.dump(A, open(OUT, "w"))
if SEC == '2':
    from scipy.optimize import differential_evolution
    name, M = sys.argv[2], float(sys.argv[3]); modes = L.SETS[name]; N = 800; sk = L.Skin(N, modes, per=1)
    def g(y):
        ko, ki, share = max(y[0], y[1]), min(y[0], y[1]), y[2]; e = sk.E; a = sum(l * np.clip((np.minimum(k, e[1:]) ** 2 - e[:-1] ** 2) / sk.A, 0, 1) for l, k in ((share * M / ko ** 2, ko), ((1 - share) * M / ki ** 2, ki))); return sk.miss(a)
    best = None
    for seed in (4, 5):
        r = differential_evolution(g, [(0.2, 0.8), (0.05, 0.6), (0.0, 1.0)], seed=seed, tol=1e-7, maxiter=150, popsize=15)
        if best is None or r.fun < best.fun: best = r
    x = best.x; A = dict(set=name, weight=M, miss=float(best.fun), radii=[float(max(x[0], x[1])), float(min(x[0], x[1]))], share=float(x[2]))
    print(f"two discs with free radii, {name}, {M:g} skins: least {100 * best.fun:.3f}%; radii {max(x[0], x[1]):.3f} and {min(x[0], x[1]):.3f}; {100 * x[2]:.0f}% of the mass in the wider disc", flush=True); json.dump(A, open(OUT, "w"))
