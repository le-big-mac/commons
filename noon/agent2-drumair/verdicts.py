"""Scores the sealed sheet by its letter.   usage: python -I verdicts.py expectations.md > verdicts.out
(reads ruler.json, named.json, discair-1.json, best-1.json, fit.json)"""
import sys, re, json
sheet = open(sys.argv[1]).read(); lines = {k: (mark, float(o)) for k, mark, o in re.findall(r"^(A\d+)\. \((.*?)\).*?odds (0\.\d+)[ \t]*$", sheet, re.M | re.S)}
J = lambda f: json.load(open(f)); inside = lambda v, lo, hi: lo <= v <= hi
pl = next(r for r in J("ruler.json")['plain'] if r['B'] == 1.0)['rise']; N = {r['name']: r for r in J("named.json")}
d54 = next(v for k, v in N.items() if k.startswith("the 1954 disc")); r4 = N["the first study's 40-ring load of 4 skins, lowest mode tuned"]
D1 = J("discair-1.json")['tuned']; B1 = J("best-1.json"); F = J("fit.json"); fr, ze = F['free'], F['zero']; lower = d54['reference']['place'] - d54['tube']['place']
V = {
 'A1': (inside(pl[0], 0.13, 0.173), f"the plain skin's lowest mode is raised by {100 * pl[0]:.2f}% (sealed: 13% to 17.3%)"),
 'A2': (inside(pl[1], 0.004, 0.010), f"its second round mode is raised by {100 * pl[1]:.2f}% (sealed: 0.4% to 1.0%)"),
 'A3': (inside(d54['reference']['place'], 1.15, 1.35), f"the 1954 disc's lowest mode on the reference drum is at {d54['reference']['place']:.4f} (sealed: 1.15 to 1.35)"),
 'A4': (inside(lower, 0.01, 0.06), f"with the tube it is at {d54['tube']['place']:.4f}, lower by {lower:.4f} (sealed: 0.01 to 0.06)"),
 'A5': (r4['reference']['place'] > 1.12, f"the first study's 4-skin load has its lowest mode at {r4['reference']['place']:.4f} (sealed: above 1.12)"),
 'A6': (D1['miss'] > 0.05, f"one disc, all nine modes, B = 1: the least largest miss is {100 * D1['miss']:.3f}% (sealed: above 5%)"),
 'A7': (B1["tuned|4|40"]['exact'] > 0.0058, f"40 rings, 4 skins, all nine modes, B = 1: the least found is {100 * B1['tuned|4|40']['exact']:.4f}% (sealed: above 0.58%)"),
 'A8': (B1["free|4|40"]['exact'] < 0.0010, f"the same with the lowest mode free: the least found is {100 * B1['free|4|40']['exact']:.4f}% (sealed: below 0.10%)"),
 'A9': (fr['diff'] < 0.04, f"the fit's largest relative difference is {100 * fr['diff']:.3f}% (sealed: below 4%)"),
 'A10': (fr['B'] > 0.3, f"the fitted B is {fr['B']:.3f} (sealed: above 0.3)"),
 'A11': (ze['diff'] >= 1.25 * fr['diff'], f"with B held at 0 the largest difference is {100 * ze['diff']:.3f}%, {ze['diff'] / fr['diff']:.2f} times the free fit's (sealed: at least 1.25 times)"),
 'A12': (inside(fr['k'], 0.35, 0.50) and inside(fr['s'], 6.25, 20), f"the fitted disc is {fr['s']:.2f} times the skin over {fr['k']:.4f} (sealed: 6.25 to 20 times over 0.35 to 0.50)"),
}
tot = 0.0; by = {}
for k in sorted(V, key=lambda s: int(s[1:])):
    mark, o = lines[k]; h = bool(V[k][0]); tot += (o - h) ** 2; by.setdefault(mark, [0, 0]); by[mark][0] += 1; by[mark][1] += h
    print(f"{k:4s} {mark:8s} odds {o:.2f}  {'held' if h else 'FAILED'}  {V[k][1]}")
n = len(V); print(f"\nheld {sum(bool(v[0]) for v in V.values())} of {n}; my mean odds {sum(lines[k][1] for k in V) / n:.3f}; Brier {tot / n:.4f}; had I said 0.5 on every line, 0.2500")
print("by the sheet's own marks: " + "; ".join(f"marked {m}: {a} lines, {b} held" for m, (a, b) in by.items()))
