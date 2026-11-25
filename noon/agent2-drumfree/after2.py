"""Checks added before the referee, none registered.   usage: python -u after2.py SECTION OUT.json
C: the base-fitting control of after.py B on loads that were not searched for this measure, to see that it can move
D: two discs with up to 1.43 skins from five more seeds of the search, each end printed
M: the local minima of the one-disc map (disc.json), five families"""
import sys, json, time
import numpy as np
import libfree as F
L = F.L; SEC = sys.argv[1]; A = {}
T = [L.target(m, n) for m, n in F.FIVE]
def fitted(r):
    return min(((max(abs(x / (c * t) - 1) for x, t in zip(r, T)), c) for c in np.arange(0.90, 1.1001, 0.00005)), key=lambda z: z[0])
if SEC == 'C':
    print("C. The base-fitting control on loads not searched for this measure: the eight modes from the second up against whole multiples of the best-fitting base")
    cases = []
    r, pl = F.disc_modes(9.77, 0.4, F.FIVE); cases.append(("the 1954 disc (9.77 times over 0.4)", r))
    r, pl = F.disc_modes(9.94, 0.400, F.FIVE); cases.append(("the first study's best disc (9.94 times over 0.400)", r))
    d = json.load(open("../drum/rings2-free-4.json")) if __import__('os').path.exists("../drum/rings2-free-4.json") else json.load(open("../drum/rings2-free-4.0.json"))
    rr = L.exact_ratios(np.array(d['rings']['40']['a']), F.FIVE); cases.append(("the first study's 40-ring load of 4 skins, lowest mode tuned", (2 * rr / rr[0] * rr[0]).tolist() if False else (2 * rr).tolist()))
    cases.append(("Raman's measured ratios", [2.00, 3.00, 3.00, 4.00, 4.00, 5.03, 5.08, 5.04]))
    A['cases'] = []
    for name, r in cases:
        r = [x * 2 / r[0] for x in r]; fixed = max(abs(x / t - 1) for x, t in zip(r, T)); t, c = fitted(r); A['cases'].append(dict(name=name, fixed=float(fixed), free=float(t), base=float(c)))
        print(f"   {name}: {100 * fixed:.3f}% with the base at half the second mode; {100 * t:.3f}% with the best-fitting base, which is {c:.4f} of that half")
if SEC == 'D':
    from scipy.optimize import differential_evolution
    print("D. Two discs, five families, up to 1.43 skins, 800 cells: five more seeds of the search", flush=True); M = 1.43; N = 800; sk = F.FreeSkin(N, F.FIVE, per=1); A['ends'] = []
    def load(y):
        ko, ki, share, frac = max(y[0], y[1]), min(y[0], y[1]), y[2], y[3]; e = sk.E; return sum(l * np.clip((np.minimum(k, e[1:]) ** 2 - e[:-1] ** 2) / sk.A, 0, 1) for l, k in ((share * frac * M / ko ** 2, ko), ((1 - share) * frac * M / ki ** 2, ki)))
    for seed in (11, 12, 13, 14, 15):
        t0 = time.time(); res = differential_evolution(lambda y: sk.miss(load(y)), [(0.2, 0.9), (0.05, 0.7), (0.0, 1.0), (0.1, 1.0)], seed=seed, tol=1e-7, maxiter=200, popsize=15); x = res.x
        A['ends'].append(dict(seed=seed, miss=float(res.fun), radii=[float(max(x[0], x[1])), float(min(x[0], x[1]))], used=float(x[3] * M)))
        print(f"   seed {seed}: {100 * res.fun:.4f}% with {x[3] * M:.3f} skins; radii {max(x[0], x[1]):.4f} and {min(x[0], x[1]):.4f}; {time.time() - t0:.0f} s", flush=True)
if SEC == 'M':
    D = json.load(open("disc.json"))['map']; s, k, Z = np.array(D['s']), np.array(D['k']), np.array(D['miss']); A['minima'] = []
    print(f"M. Local minima of the one-disc map, five families: {len(s)} weights per area from {s[0]:g} to {s[-1]:g} times the skin by {len(k)} radii from {k[0]:g} to {k[-1]:g}")
    for i in range(len(s)):
        for j in range(len(k)):
            nb = [Z[a, b] for a in range(max(0, i - 1), min(len(s), i + 2)) for b in range(max(0, j - 1), min(len(k), j + 2)) if (a, b) != (i, j)]
            if Z[i, j] < min(nb): A['minima'].append(dict(s=float(s[i]), k=float(k[j]), miss=float(Z[i, j]), edge=bool(i in (0, len(s) - 1) or j in (0, len(k) - 1))))
    for m in sorted(A['minima'], key=lambda m: m['miss']): print(f"   {100 * m['miss']:.2f}% at {m['s']:.2f} times over {m['k']:.4f}" + (" (on the map's edge)" if m['edge'] else ""))
    from scipy.optimize import minimize
    print("   polished from each of the map's minima below 10% (Nelder-Mead on the exact disc):"); A['polished'] = []
    for m in sorted(A['minima'], key=lambda m: m['miss']):
        if m['miss'] > 0.10: continue
        r = minimize(lambda x: F.disc_miss(min(60, max(1, x[0])), min(0.95, max(0.05, x[1])), F.FIVE)[0], [m['s'], m['k']], method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-10, maxiter=800))
        A['polished'].append(dict(s0=m['s'], k0=m['k'], s=float(r.x[0]), k=float(r.x[1]), miss=float(r.fun))); print(f"      from {m['s']:.2f} times over {m['k']:.4f}: ends at {100 * r.fun:.4f}% at {r.x[0]:.3f} times over {r.x[1]:.4f}", flush=True)
if SEC == 'V':
    from scipy.optimize import minimize_scalar
    print("V. The valley of the one-disc map: at each radius, the weight per area with the least overtone miss (exact disc, five families)", flush=True); A['valley'] = []
    for k in np.arange(0.30, 0.6501, 0.025):
        r = minimize_scalar(lambda x: F.disc_miss(x, k, F.FIVE)[0], bounds=(1.5, 30), method='bounded', options=dict(xatol=1e-4)); best = (r.fun, r.x)
        for lo, hi in ((1.5, 4), (4, 8), (8, 16), (16, 30)):
            r2 = minimize_scalar(lambda x: F.disc_miss(x, k, F.FIVE)[0], bounds=(lo, hi), method='bounded', options=dict(xatol=1e-4))
            if r2.fun < best[0]: best = (r2.fun, r2.x)
        pl = F.disc_miss(best[1], k, F.FIVE)[1]; A['valley'].append(dict(k=float(k), s=float(best[1]), miss=float(best[0]), place=float(pl), mass=float((best[1] - 1) * k * k)))
        print(f"   radius {k:.3f}: least {100 * best[0]:.2f}% at {best[1]:.2f} times the skin ({(best[1] - 1) * k * k:.2f} skins added); the lowest mode's place {pl:.3f}", flush=True)
if SEC == 'L':
    print("L. What the table's ring loads look like (rings of equal width; 'bare' is a load below 0.05 skins per area)"); BEST = json.load(open("best.json")); A['loads'] = []
    for key in ("five|1.43|40", "five|1.43|80", "five|4|40", "five|4|80", "five|12|40", "five|12|80", "seven|4|40", "seven|4|80", "seven|12|40", "seven|12|80"):
        a = np.array(BEST[key]['a']); n = len(a); E = np.arange(n + 1) / n; on = a > 0.05; last = int(np.nonzero(on)[0][-1]); h = int(a.argmax()); inner = on[:last + 1]; gaps = int(sum(1 for i in range(1, last + 1) if not inner[i] and inner[i - 1]))
        A['loads'].append(dict(key=key, end=float(E[last + 1]), heavy=float(a[h]), heavy_from=float(E[h]), heavy_to=float(E[h + 1]), gaps=gaps, loaded=int(on.sum()), centre=float(a[0])))
        print(f"   {key}: loaded out to {E[last + 1]:.4f}; {int(on.sum())} rings loaded, with {gaps} bare stretches inside; heaviest ring +{a[h]:.0f} from {E[h]:.4f} to {E[h + 1]:.4f}; the centre ring +{a[0]:.0f}")
if SEC == 'Q':
    print("Q. Another measure, on loads that were not searched for it: the root mean square of the misses (40 rings; finite differences)"); BEST = json.load(open("best.json")); A['rms'] = []
    for M in (1.43, 4.0, 12.0):
        free = np.array(BEST[f"five|{M:g}|40"]['a']); tuned = np.array(json.load(open(f"../drum/rings2-free-{M:g}.json"))['rings']['40']['a'])
        cf = F.FreeSkin(40, F.FIVE).solve(free, grad=False); ct = L.Skin(40, L.NINE).solve(tuned, grad=False); ct2 = F.FreeSkin(40, [(1, 1), (0, 1)] + F.FIVE[1:]).solve(tuned, grad=False)
        A['rms'].append(dict(weight=M, free=float(np.sqrt(np.mean(cf ** 2))), tuned=float(np.sqrt(np.mean(ct ** 2))), tuned_here=float(np.sqrt(np.mean(ct2 ** 2))), n_free=len(cf), n_tuned=len(ct)))
        print(f"   {M:g} skins: the lowest mode free, {len(cf)} misses: {100 * np.sqrt(np.mean(cf ** 2)):.3f}%; the lowest mode tuned, {len(ct)} misses against the lowest mode: {100 * np.sqrt(np.mean(ct ** 2)):.3f}%; the same load, {len(ct2)} misses against half the second mode: {100 * np.sqrt(np.mean(ct2 ** 2)):.3f}%")
if SEC == 'P':
    print("P. The discs as printed in the README, recomputed (exact for one disc; 800 cells for two)"); A['printed'] = []
    for s_, k_ in ((4.34, 0.504), (4.3, 0.50)):
        m, pl = F.disc_miss(s_, k_, F.FIVE); A['printed'].append(dict(what=f"one disc {s_} over {k_}", miss=float(m), place=float(pl))); print(f"   one disc, {s_} times over {k_}: {100 * m:.2f}%; place {pl:.3f}")
    sk = F.FreeSkin(800, F.FIVE, per=1); e = sk.E
    def two(outer, ko, inner, ki): return sum(l * np.clip((np.minimum(k, e[1:]) ** 2 - e[:-1] ** 2) / sk.A, 0, 1) for l, k in ((outer - 1, ko), (inner - outer, ki)))
    G = json.load(open("after-G.json"))['two1.43']
    for outer, ko, inner, ki in ((G['outer'], G['ko'], G['inner'], G['ki']), (6.30, 0.493, 8.12, 0.277), (6.3, 0.493, 8.1, 0.277), (6.3, 0.49, 8.1, 0.28)):
        a = two(outer, ko, inner, ki); m = sk.miss(a); A['printed'].append(dict(what=f"two discs {outer:.4g} to {ko:.4g}, {inner:.4g} inside {ki:.4g}", miss=float(m), used=float(sk.mass(a)))); print(f"   two discs, {outer:.4g} times to {ko:.4g} and {inner:.4g} inside {ki:.4g}: {100 * m:.2f}%; {sk.mass(a):.3f} skins")
json.dump(A, open(sys.argv[2], "w"))
