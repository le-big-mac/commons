"""Scores the sealed sheet by its letter.   usage: python -I verdicts.py expectations.md > verdicts.out     (reads disc.json and best.json)"""
import sys, re, json
sheet = open(sys.argv[1]).read(); lines = {k: (mark, float(o)) for k, mark, o in re.findall(r"^(N\d+)\. \((.*?)\).*?odds (0\.\d+)[ \t]*$", sheet, re.M | re.S)}
D = json.load(open("disc.json")); B = json.load(open("best.json")); inside = lambda v, lo, hi: lo <= v <= hi; d = D['five']; r4 = B["five|4|40"]; s4 = B["seven|4|40"]; r12 = B["five|1.2|40"]; rm = D['raman']
V = {
 'N1': (inside(d['k'], 0.45, 0.55), f"the best disc's edge is at {d['k']:.4f} of the radius (sealed: 0.45 to 0.55)"),
 'N2': (inside(d['s'], 6.25, 16), f"its weight per area is {d['s']:.2f} times the skin's (sealed: 6.25 to 16)"),
 'N3': (d['miss'] < 0.025, f"its overtone miss is {100 * d['miss']:.3f}% (sealed: below 2.5%)"),
 'N4': (inside(d['place'], 1.05, 1.15), f"the lowest mode's place is {d['place']:.4f} (sealed: 1.05 to 1.15)"),
 'N5': (r4['exact'] < 0.004, f"the least found is {100 * r4['exact']:.4f}% (sealed: below 0.40%)"),
 'N6': (r4['place'] > 1.02, f"the lowest mode's place is {r4['place']:.4f} (sealed: above 1.02)"),
 'N7': (s4['exact'] < 0.008, f"the least found is {100 * s4['exact']:.4f}% (sealed: below 0.80%)"),
 'N8': (r12['exact'] < 0.01, f"the least found is {100 * r12['exact']:.4f}% (sealed: below 1%)"),
 'N9': (inside(rm['k'], 0.40, 0.55), f"the best-fitting disc's edge is at {rm['k']:.4f} (sealed: 0.40 to 0.55); it weighs {rm['s']:.2f} times the skin"),
 'N10': (rm['fit'] < 0.03, f"the fit's largest relative difference is {100 * rm['fit']:.3f}% (sealed: below 3%)"),
}
tot = 0.0; by = {}
for k in sorted(V, key=lambda s: int(s[1:])):
    mark, o = lines[k]; h = V[k][0]; tot += (o - h) ** 2; by.setdefault(mark, [0, 0]); by[mark][0] += 1; by[mark][1] += h
    print(f"{k:4s} {mark:8s} odds {o:.2f}  {'held' if h else 'FAILED'}  {V[k][1]}")
n = len(V); print(f"\nheld {sum(v[0] for v in V.values())} of {n}; my mean odds {sum(lines[k][1] for k in V) / n:.3f}; Brier {tot / n:.4f}; had I said 0.5 on every line, 0.2500")
print("by the sheet's own marks: " + "; ".join(f"marked {m}: {a} lines, {b} held" for m, (a, b) in by.items()))
