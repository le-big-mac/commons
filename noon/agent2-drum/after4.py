"""The fourth sheet's referee's controls, redone here with my own code (ringlib.py).   usage: python -u after4.py SECTIONS   (for example 1 or 2345)
1 a floor under the gaps; 2 how exactly the loads must be made; 3 the three even pieces as the README first printed them;
4 the first table's two discs as printed; 5 the ringed skin's modes by name, up to 6.7 times the lowest."""
import sys, json, math
import numpy as np
from scipy.optimize import brentq
from scipy.linalg import eigh_tridiagonal
import ringlib as L
SEC = sys.argv[1]; T = L.TARGET
def ratios_edges(edges, rho, which=L.NINE, wmax=14.0, step=0.002):
    need = {}; out = {}
    for m, k in which: need[m] = max(need.get(m, 0), k)
    for m, cnt in need.items():
        roots = []; w = 0.02; f0 = L._rim(w, m, edges, rho)
        while len(roots) < cnt and w < wmax:
            f1 = L._rim(w + step, m, edges, rho)
            if f0 * f1 < 0: roots.append(brentq(L._rim, w, w + step, args=(m, edges, rho), xtol=1e-13))
            w += step; f0 = f1
        out[m] = roots
    W = np.array([out[m][k - 1] for m, k in which]); return W / W[0]
miss_edges = lambda edges, rho: float(np.abs(ratios_edges(edges, rho)[1:] / T[1:] - 1).max())
def ring40(M): return np.array(json.load(open(f"rings2-free-{M:g}.json"))['rings']['40']['a'])
sk = L.Skin(40)
if '1' in SEC:
    print("1. A floor under the gaps: every ring inside a radius must carry at least so much (40 rings, the sealed measure, eleven starts each)")
    rng = np.random.default_rng(71)
    for M, inside, floors in ((1.43, 0.375, (0.0, 0.5, 1.0, 3.0)), (12.0, 0.4, (0.0, 10.0))):
        base = ring40(M)
        for fl in floors:
            lb = np.where(sk.E[:-1] < inside - 1e-9, fl, 0.0); starts = [base, L.disc(sk, M / 0.16, 0.4)] + [base * np.exp(0.4 * rng.standard_normal(40)) + rng.uniform(0, 2 * fl + 1, 40) * (sk.E[:-1] < inside) for _ in range(9)]
            ends = [L.slp(sk, a0, M, lb=lb) for a0 in starts]; a, f = min(ends, key=lambda z: z[1]); gaps = [j for j in range(40) if sk.E[j] < inside - 1e-9 and a[j] <= fl + 1e-6]
            print(f"   {M:5.2f} skins, at least +{fl:g} inside {inside}: least {100 * f:.4f}% ({100 * L.exact_miss(a):.4f}% by exact matching); {sum(e[1] < f + 2e-5 for e in ends)} of {len(ends)} searches within 0.002 points; rings left on the floor: {len(gaps)}; core about +{a[1]:.1f}", flush=True)
if '2' in SEC:
    print("2. How exactly must the load be made? The 40-ring load at 1.43 skins with every ring's load off by a random share (400 draws each; the weight is not held)")
    a = ring40(1.43); rng = np.random.default_rng(72); print(f"   as found: {100 * sk.miss(a):.4f}%")
    for eps in (0.01, 0.03):
        v = np.array([sk.miss(a * (1 + eps * rng.standard_normal(40))) for _ in range(400)]); print(f"   each ring off by {100 * eps:.0f}% (standard deviation): median miss {100 * np.median(v):.2f}%, nine draws in ten below {100 * np.quantile(v, 0.9):.2f}%, the worst {100 * v.max():.2f}%")
    j = int(np.argmax(a))
    for d in (-0.02, 0.02): b = a.copy(); b[j] *= 1 + d; print(f"   the heaviest ring alone {100 * d:+.0f}%: {100 * sk.miss(b):.2f}%")
    b = np.concatenate([[a[0]], a[:-1]]); print(f"   the whole load moved outward by one ring (a fortieth of the radius): {100 * sk.miss(b):.2f}%")
if '3' in SEC:
    print("3. The three even pieces at 1.43 skins, by exact matching")
    P = json.load(open("pieces2-1.43.json")); r = P['radii']; l = P['loads']; f = lambda r, l: miss_edges([r[0], r[1], r[2], r[3], r[4], 1.0], [1 + l[0], 1.0, 1 + l[1], 1.0, 1 + l[2], 1.0]); mass = lambda r, l: l[0] * r[0] ** 2 + l[1] * (r[2] ** 2 - r[1] ** 2) + l[2] * (r[4] ** 2 - r[3] ** 2)
    print("   at full precision: radii " + ", ".join(f"{x:.5f}" for x in r) + "; loads " + ", ".join(f"{x:.3f}" for x in l) + f": {100 * f(r, l):.4f}%; added mass {mass(r, l):.4f}")
    r3 = [round(x, 3) for x in r]; l1 = [round(x, 1) for x in l]
    print(f"   as the README first printed it (radii to three places, loads to one): {100 * f(r3, l1):.3f}%; added mass {mass(r3, l1):.4f}")
    print(f"   radii rounded alone: {100 * f(r3, l):.3f}%; loads rounded alone: {100 * f(r, l1):.3f}%")
    for d in (-0.001, 0.001): print(f"   the hoop's outer edge moved by {d:+.3f} of the radius: {100 * f([r[0], r[1], r[2] + d, r[3], r[4]], l):.3f}%; its inner edge: {100 * f([r[0], r[1] + d, r[2], r[3], r[4]], l):.3f}%")
if '4' in SEC:
    print("4. The first table's two discs (the sealed search of the third sheet), by exact matching")
    Lj = json.load(open("layers-2.json")); a, k = Lj['a'], Lj['k']; o = np.argsort(k); ki, ko = k[o[0]], k[o[1]]; ai, ao = a[o[0]], a[o[1]]
    print(f"   at full precision (+{ao:.3f} inside {ko:.4f} and +{ai:.3f} inside {ki:.4f}): {100 * miss_edges([ki, ko, 1.0], [1 + ao + ai, 1 + ao, 1.0]):.3f}%; as printed (+12.9 inside 0.438 and +5.6 inside 0.234): {100 * miss_edges([0.234, 0.438, 1.0], [1 + 12.9 + 5.6, 1 + 12.9, 1.0]):.3f}%")
if '5' in SEC:
    print("5. The 40-ring load at 1.43 skins: every mode up to 6.7 times the lowest, by name (finite differences, 2,000 cells)")
    a = ring40(1.43); N = 2000; h = 1.0 / N; r = (np.arange(N) + 0.5) * h; re = np.arange(N + 1) * h; rho = 1 + np.repeat(a, 50); sc = np.sqrt(r * rho); found = []; w01 = None
    for m in range(0, 9):
        d = (re[:-1] + re[1:]) / (h * h) + m * m / r; d[-1] += re[-1] / (h * h); ev = eigh_tridiagonal(d / sc ** 2, -re[1:-1] / (h * h) / (sc[:-1] * sc[1:]), select='i', select_range=(0, 5))[0]; w = np.sqrt(ev); w01 = w[0] if m == 0 else w01
        found += [(w[n] / w01, m, n + 1) for n in range(6) if w[n] / w01 < 6.7]
    print("   " + ", ".join(f"({m},{n}) {x:.3f}" for x, m, n in sorted(found)))
if '6' in SEC:
    print("6. For comparison, the best even disc made inexactly (exact matching, drum.py)")
    import drum
    s, k = 9.938, 0.4004; print(f"   as found: {100 * drum.miss(s, k):.2f}%")
    for d in (-0.03, -0.01, 0.01, 0.03): print(f"   its load {100 * d:+.0f}%: {100 * drum.miss(1 + (s - 1) * (1 + d), k):.2f}%")
    for d in (-0.025, -0.001, 0.001, 0.025): print(f"   its edge moved by {d:+.3f} of the radius: {100 * drum.miss(s, k + d):.2f}%")
