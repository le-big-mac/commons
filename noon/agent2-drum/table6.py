"""The weight table after the referee, in Markdown, from the outputs: ring loads by exact matching, searched on the sealed measure.
usage: python -I table6.py onedisc.json twodisc2.out > table6.out     (reads rings2-free-*.json and rings2-piled-*.json)"""
import sys, json, re, math, glob
ONE = {r['weight']: r for r in json.load(open(sys.argv[1]))}; TWO = {float(m): float(t) / 100 for m, t in re.findall(r"added mass\s+([\d.]+): two discs with free radii, least largest miss ([\d.]+)%", open(sys.argv[2]).read())}
R = {}
for f in glob.glob("rings2-*-*.json"):
    d = json.load(open(f)); R[(d['kind'], d['weight'])] = d['rings']
W = sorted(ONE); g = lambda kind, m, n: R[(kind, m)][str(n)]['exact'] if (kind, m) in R and str(n) in R[(kind, m)] else None; pc = lambda x: f"{100 * x:.2f}%" if x is not None else ""
print("| added mass, in skins | one even disc | two discs, free radii | piled discs, 40 rings | piled discs, 80 rings | any radial load, 40 rings | any radial load, 80 rings | the last, in cents |"); print("|---|---|---|---|---|---|---|---|")
for m in W: print(f"| {m:g} | {pc(ONE[m]['miss'])} | {pc(TWO[m])} | {pc(g('piled', m, 40))} | {pc(g('piled', m, 80))} | {pc(g('free', m, 40))} | {pc(g('free', m, 80))} | {1200 * math.log2(1 + g('free', m, 80)):.0f} |")
print()
for kind, m in (("free", 1.43), ("free", 12.0), ("piled", 12.0)): print(f"{kind} at {m:g} skins, by exact matching: " + "; ".join(f"{n} rings {100 * g(kind, m, n):.4f}%" for n in (40, 80, 160)))
for n in (40, 80): print(f"piled discs on {n} rings miss by more than two discs with free radii at {sum(g('piled', m, n) > TWO[m] + 1e-6 for m in W)} of {len(W)} weights; by the most at {max(W, key=lambda m: g('piled', m, n) - TWO[m]):g} skins ({100 * max(g('piled', m, n) - TWO[m] for m in W):+.3f} points)")
best_piled = {m: min(g('piled', m, 80), g('piled', m, 40), TWO[m]) for m in W}
print("two discs less piled discs on 80 rings, in points: " + "; ".join(f"{m:g}: {100 * (TWO[m] - g('piled', m, 80)):+.3f}" for m in W))
print("any radial load on 80 rings as a share of the best of two discs and piled discs: " + "; ".join(f"{m:g}: {g('free', m, 80) / best_piled[m]:.3f}" for m in W))
print("one even disc over any radial load on 80 rings: " + "; ".join(f"{m:g}: {ONE[m]['miss'] / g('free', m, 80):.2f}" for m in W))
print("any radial load, 40 rings less 80 rings, in points: " + "; ".join(f"{m:g}: {100 * (g('free', m, 40) - g('free', m, 80)):+.4f}" for m in W))
for kind in ("free", "piled"):
    for n in (40, 80):
        v = [(m, R[(kind, m)][str(n)]) for m in W]; print(f"{kind}, {n} rings: of the searches at each weight, the share that ended within 0.002 points of the least: " + "; ".join(f"{m:g}: {sum(e < d['miss'] + 2e-5 for e in d['ends'])}/{len(d['ends'])}" for m, d in v))
E = lambda n, j: j / n
for m in (1.43, 12.0):
    for n in (40, 80, 160):
        a = R[("free", m)][str(n)]['a']; j = max(range(n), key=lambda i: a[i]); k0 = j
        while k0 > 0 and a[k0 - 1] > 0.5 * a[j]: k0 -= 1
        k1 = j
        while k1 < n - 1 and a[k1 + 1] > 0.5 * a[j]: k1 += 1
        print(f"free at {m:g} skins, {n} rings: the heaviest ring carries +{a[j]:.0f}; rings next to it with more than half that reach from {E(n, k0):.5f} to {E(n, k1 + 1):.5f} (width {E(n, k1 + 1) - E(n, k0):.5f}, mass {sum(a[i] * (E(n, i + 1) ** 2 - E(n, i) ** 2) for i in range(k0, k1 + 1)):.3f} skins); loaded out to {E(n, max(i for i in range(n) if a[i] > 1e-6) + 1):.4f}")
