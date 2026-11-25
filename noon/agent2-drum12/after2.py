"""The referee's controls, redone here with my own code (not registered).   usage: python -u after2.py SECTION ARGS... OUT.json
W SET up|down RINGS   the weight walked up or down, over the wider list of weights, on 40 or 80 rings
O                     the ring near the rim in the table's twelve-mode loads
I                     strays, counted on the table's own loads (best.json), m up to 30 and n up to 10
T                     inexact making, on the table's own loads
D                     D under other settings: fundamental floated, modes up to 7.6, struck at 0.7, no roll-off
F                     a smooth load that makes the families coincide (the referee's): 4/(1+r^2)^2 - 1
2 SET WEIGHT          two discs whose total weight may be anything up to WEIGHT"""
import sys, json, math, os, time
import numpy as np
from scipy.linalg import eigh_tridiagonal
import lib12 as L
SEC = sys.argv[1]; OUT = sys.argv[-1]; A = {}
WW = [1.0, 1.43, 1.6, 1.8, 1.85, 1.9, 2.0, 2.2, 2.4, 2.79, 3.0, 3.2, 3.4, 3.6, 4.0, 6.0, 9.6, 12.0]
def B(key): return np.array(json.load(open("best.json"))[key]['a'])
def spectrum(a, mmax=30, nmax=10, per=50):
    R = len(a); N = R * per; h = 1.0 / N; r = (np.arange(N) + 0.5) * h; re = np.arange(N + 1) * h; rho = 1 + np.repeat(a, per); sc = np.sqrt(r * rho); out = []; w01 = None
    for m in range(mmax + 1):
        d = (re[:-1] + re[1:]) / (h * h) + m * m / r; d[-1] += re[-1] / (h * h); w = np.sqrt(eigh_tridiagonal(d / sc ** 2, -re[1:-1] / (h * h) / (sc[:-1] * sc[1:]), select='i', select_range=(0, nmax - 1))[0]); w01 = w[0] if m == 0 else w01
        out += [(w[j] / w01, m, j + 1) for j in range(nmax)]
    return sorted(out)
def family(F): return [(m, (l - m + 1) // 2) for l in range(1, F + 1) for m in range(l - 1, -1, -2)]
if SEC == 'W':
    name, way, R = sys.argv[2], sys.argv[3], int(sys.argv[4]); modes = L.SETS[name]; sk = L.Skin(R, modes); order = WW if way == "up" else WW[::-1]; prev = None; A['walk'] = []
    for M in order:
        starts = []
        if prev is not None: starts.append(("the weight before", prev * min(1.0, M / sk.mass(prev))))
        f = f"s-{name}-{M:g}.json"
        if os.path.exists(f) and str(R) in json.load(open(f))['rings']: starts.append(("the sealed search's answer", np.array(json.load(open(f))['rings'][str(R)]['a'])))
        if not starts: starts.append(("one disc", L.disc(sk, M / 0.16, 0.4)))
        best = None
        for nm, a0 in starts:
            a, fm = L.slp(sk, a0, M)
            if best is None or fm < best[0]: best = (fm, a, nm)
        fm, a, nm = best; prev = a; A['walk'].append(dict(weight=M, miss=fm, a=a.tolist(), start=nm))
        print(f"{name} {way:4s} {R} rings {M:5.2f}: {100 * fm:.4f}% from '{nm}'", flush=True); json.dump(A, open(OUT, "w"))
if SEC == 'O':
    print("O. The table's twelve-mode loads on 40 rings: weight lying beyond 0.45 of the radius, and the miss with that weight taken off (nothing else changed)"); sk = L.Skin(40, L.TWELVE); A['outer'] = []
    for M in WW:
        key = f"twelve|{M:g}|40"
        if key not in json.load(open("best.json")) or json.load(open("best.json"))[key] is None: continue
        a = B(key); out = float(a[18:] @ sk.A[18:]); b = a.copy(); b[18:] = 0; where = [f"{sk.E[j]:.3f} to {sk.E[j + 1]:.3f}" for j in range(18, 40) if a[j] > 1e-6]
        A['outer'].append(dict(weight=M, beyond=out, miss=sk.miss(a), without=sk.miss(b), rings=where)); print(f"   {M:g} skins: {out:.2f} skins beyond 0.45" + (f" (rings {', '.join(where)}); the miss is {100 * sk.miss(a):.2f}% with it and {100 * sk.miss(b):.2f}% without" if out > 1e-6 else ""), flush=True)
    for name in ("sixteen",):
        tot = [(M, float(B(f"{name}|{M:g}|40")[18:] @ sk.A[18:])) for M in WW if json.load(open("best.json")).get(f"{name}|{M:g}|40")]; print(f"   the sixteen-mode loads on 40 rings: the most weight beyond 0.45 at any weight is {max(t[1] for t in tot):.4f} skins"); A['outer16'] = tot
    json.dump(A, open(OUT, "w"))
if SEC == 'I':
    print("I. Strays on the table's own loads: every mode (m up to 30, n up to 10) below the top harmonic plus a half that is not of the set"); A['strays'] = []
    cases = [("twelve modes, 2.79 skins, 40 rings", B("twelve|2.79|40"), 6), ("twelve modes, 12 skins, 40 rings", B("twelve|12|40"), 6), ("twelve modes, 12 skins, 80 rings", B("twelve|12|80"), 6), ("sixteen modes, 4 skins, 40 rings", B("sixteen|4|40"), 7), ("sixteen modes, 4 skins, 80 rings", B("sixteen|4|80"), 7), ("sixteen modes, 12 skins, 40 rings", B("sixteen|12|40"), 7)]
    for F in (8, 9, 10): cases.append((f"{len(family(F))} modes, 12 skins, 40 rings", np.array(json.load(open(f"after-N-{F}-12.json"))['rings']['40']['a']), F))
    for name, a, F in cases:
        fam = set(family(F)); sp = spectrum(a); out = [(float(x), m, n) for x, m, n in sp if x < F + 0.5 and (m, n) not in fam]; top = max(x for x, m, n in sp if (m, n) in fam)
        A['strays'].append(dict(name=name, F=F, strays=out, top=float(top))); print(f"   {name}: " + (", ".join(f"({m},{n}) at {x:.3f}" for x, m, n in out) if out else "none") + f"; the set's own highest mode is at {top:.3f}", flush=True)
    json.dump(A, open(OUT, "w"))
if SEC == 'T':
    print("T. Inexact making, on the table's own loads (400 draws each)"); rng = np.random.default_rng(13); A['tol'] = []
    for name, key in (("twelve", "twelve|2.79|40"), ("twelve", "twelve|12|40"), ("sixteen", "sixteen|4|40"), ("sixteen", "sixteen|12|40")):
        a = B(key); sk = L.Skin(40, L.SETS[name]); row = dict(key=key, base=sk.miss(a))
        for eps in (0.01, 0.03): v = np.array([sk.miss(a * (1 + eps * rng.standard_normal(40))) for _ in range(400)]); row[str(eps)] = (float(np.median(v)), float(v.max()))
        row['out'] = sk.miss(np.concatenate([[a[0]], a[:-1]])); row['in'] = sk.miss(np.concatenate([a[1:], [0.0]])); A['tol'].append(row)
        print(f"   {key}: as found {100 * row['base']:.2f}%; each ring off by 1%: median {100 * row['0.01'][0]:.2f}%, worst {100 * row['0.01'][1]:.2f}%; by 3%: median {100 * row['0.03'][0]:.2f}%; the whole load moved one ring outward {100 * row['out']:.1f}%, inward {100 * row['in']:.1f}%", flush=True)
    json.dump(A, open(OUT, "w"))
if SEC == 'D':
    print("D. My ruler D under other settings (cents). As sealed: the lowest mode pinned, modes up to 6.6 times it, struck at half the radius, strengths as in my sound files")
    def Dvar(a, per=50, top=6.6, strike=0.5, floated=False, rolloff=True):
        P = L.struck(a, top=top, strike=strike, per=per); rows = []
        for p in P:
            s = p['strength'] if rolloff else p['strength'] / math.exp(-(p['ratio'] / 7.0) ** 2); t = 1.3 * p['ratio'] ** -0.8; rows.append((p['ratio'], s * s * t * (1 - math.exp(-1.2 / t))))
        def dist(f): return sum(e * abs(1200 * math.log2(x / f / max(1, round(x / f)))) for x, e in rows) / sum(e for x, e in rows)
        if not floated: return dist(1.0)
        return min(dist(f) for f in np.arange(0.94, 1.0601, 0.0005))
    N = 2000; e = np.arange(N + 1) / N; disc = 8.938 * np.clip((np.minimum(0.4004, e[1:]) ** 2 - e[:-1] ** 2) / (e[1:] ** 2 - e[:-1] ** 2), 0, 1); nine = next(np.array(r['a']) for r in json.load(open("../drum/chain-free-up.json")) if abs(r['weight'] - 1.43) < 1e-9)
    cases = [("the nine-mode even disc", disc, 1), ("nine-mode rings, 1.43 skins", nine, 50), ("twelve, 2.79 skins", B("twelve|2.79|40"), 50), ("twelve, 12 skins", B("twelve|12|40"), 50), ("sixteen, 4 skins", B("sixteen|4|40"), 50), ("sixteen, 12 skins", B("sixteen|12|40"), 50)]; A['D'] = {}
    for name, a, per in cases:
        row = dict(sealed=Dvar(a, per), floated=Dvar(a, per, floated=True), top76=Dvar(a, per, top=7.6), strike07=Dvar(a, per, strike=0.7), noroll=Dvar(a, per, rolloff=False)); A['D'][name] = row
        print(f"   {name}: as sealed {row['sealed']:.1f}; fundamental floated {row['floated']:.1f}; modes up to 7.6 {row['top76']:.1f}; struck at 0.7 {row['strike07']:.1f}; no roll-off {row['noroll']:.1f}", flush=True)
    P = L.struck(B("sixteen|4|40")); E = [(p, p['strength'] ** 2 * (1.3 * p['ratio'] ** -0.8) * (1 - math.exp(-1.2 / (1.3 * p['ratio'] ** -0.8)))) for p in P]; tot = sum(x for p, x in E); low4 = sum(x for p, x in sorted(E, key=lambda z: z[0]['ratio'])[:4]) / tot; hi = sum(x for p, x in E if p['ratio'] > 5.5) / tot
    A['weights16'] = dict(low4=low4, above55=hi, modes=len(P)); print(f"   the sixteen-mode skin of 4 skins, as sealed: {len(P)} modes below 6.6; {100 * low4:.0f}% of the weight is on the four lowest partials and {100 * hi:.1f}% on those above 5.5")
    json.dump(A, open(OUT, "w"))
if SEC == 'F':
    print("F. A smooth load that makes the families coincide: a(r) = 4/(1 + r^2)^2 - 1 (the flattened hemisphere; the referee's control)")
    N = 4000; r = (np.arange(N) + 0.5) / N; a = 4 / (1 + r * r) ** 2 - 1; sk = L.Skin(N, L.SIXTEEN, per=1); c = sk.solve(a, grad=False); ratios = np.concatenate([[1.0], (c + 1) * sk.T[1:]]); A = dict(mass=sk.mass(a), ratios=ratios.tolist(), miss=float(np.abs(c).max()))
    print(f"   added mass {sk.mass(a):.3f} skins; the sixteen ratios: " + ", ".join(f"{x:.3f}" for x in ratios)); print("   sqrt(l(l+1)/2) for l = 1 to 7: " + ", ".join(f"{math.sqrt(l * (l + 1) / 2):.3f}" for l in range(1, 8)) + f"; largest miss from whole multiples {100 * A['miss']:.1f}%"); json.dump(A, open(OUT, "w"))
if SEC == '2':
    from scipy.optimize import differential_evolution
    name, M = sys.argv[2], float(sys.argv[3]); modes = L.SETS[name]; N = 800; sk = L.Skin(N, modes, per=1)
    def loadof(y):
        ko, ki, share, frac = max(y[0], y[1]), min(y[0], y[1]), y[2], y[3]; e = sk.E; return sum(l * np.clip((np.minimum(k, e[1:]) ** 2 - e[:-1] ** 2) / sk.A, 0, 1) for l, k in ((share * frac * M / ko ** 2, ko), ((1 - share) * frac * M / ki ** 2, ki)))
    best = None
    for seed in (4, 5):
        r = differential_evolution(lambda y: sk.miss(loadof(y)), [(0.2, 0.8), (0.05, 0.6), (0.0, 1.0), (0.3, 1.0)], seed=seed, tol=1e-7, maxiter=200, popsize=15)
        if best is None or r.fun < best.fun: best = r
    x = best.x; A = dict(set=name, weight=M, miss=float(best.fun), radii=[float(max(x[0], x[1])), float(min(x[0], x[1]))], share=float(x[2]), used=float(x[3] * M))
    print(f"two discs, total weight free up to {M:g} skins, {name}: least {100 * best.fun:.3f}% with {x[3] * M:.2f} skins; radii {max(x[0], x[1]):.3f} and {min(x[0], x[1]):.3f}", flush=True); json.dump(A, open(OUT, "w"))
