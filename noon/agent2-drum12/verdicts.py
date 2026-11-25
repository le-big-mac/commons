"""Scores the sealed sheet by its letter.   usage: python -I verdicts.py expectations.md > verdicts.out     (reads s-*.json, disc12.json)"""
import sys, re, json
sheet = open(sys.argv[1]).read(); lines = {k: (mark, float(o)) for k, mark, o in re.findall(r"^(T\d)\. \((.*?)\).*?odds (0\.\d+)[ \t]*$", sheet, re.M | re.S)}
S = lambda name, M: json.load(open(f"s-{name}-{M:g}.json"))['rings']['40']; D12 = json.load(open("disc12.json")); inside = lambda v, lo, hi: lo <= v <= hi
t12, t143, t16 = S("twelve", 12), S("twelve", 1.43), S("sixteen", 12); a = t12['a']; top = max(a)
rise = max(a[j] - min(a[:j]) for j in range(1, 40))          # the most by which a ring outweighs some ring nearer the centre
TW = [(0, 1), (1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3), (5, 1), (3, 2), (1, 3)]; miss = {mn: abs(r / (mn[0] + 2 * mn[1] - 1) - 1) for mn, r in zip(TW, t12['ratios'])}; big = max(v for k, v in miss.items() if k != (0, 1))
V = {
 'T1': (inside(100 * t12['exact'], 0.8, 2.5), f"the least found is {100 * t12['exact']:.3f}% (sealed: 0.8% to 2.5%)"),
 'T2': (inside(100 * t143['exact'], 1.5, 5.0), f"the least found is {100 * t143['exact']:.3f}% (sealed: 1.5% to 5%)"),
 'T3': (rise > 0.1 * top, f"the heaviest ring carries +{top:.0f}; some ring outweighs a ring nearer the centre by {rise:.0f}"),
 'T4': (miss[(1, 3)] >= 0.99 * big, f"(1,3) misses by {100 * miss[(1, 3)]:.3f}%; the largest miss is {100 * big:.3f}%, shared by " + ", ".join(f"({m},{n})" for (m, n), v in miss.items() if v >= 0.99 * big and (m, n) != (0, 1))),
 'T5': (inside(100 * t16['exact'], 2.0, 6.0), f"the least found is {100 * t16['exact']:.3f}% (sealed: 2% to 6%)"),
 'T6': (inside(100 * D12['T6']['miss'], 4.5, 8.0), f"largest miss {100 * D12['T6']['miss']:.3f}% at {D12['T6']['s']:.2f} times over {D12['T6']['k']:.4f} (sealed: 4.5% to 8%)"),
 'T7': (inside(D12['T7']['disc'], 28, 45) and inside(D12['T7']['ringed'], 9, 20), f"D = {D12['T7']['disc']:.1f} cents for the disc (sealed: 28 to 45) and {D12['T7']['ringed']:.1f} for the ringed load (sealed: 9 to 20)"),
 'T8': (t143['D'] < D12['T7']['ringed'], f"D = {t143['D']:.1f} cents for the twelve-mode load against {D12['T7']['ringed']:.1f} for the nine-mode load"),
 'T9': (t12['D'] < 10, f"D = {t12['D']:.1f} cents (sealed: below 10)"),
}
tot = 0.0; by = {}
for k in sorted(V):
    mark, o = lines[k]; h = V[k][0]; tot += (o - h) ** 2; m = mark.split(";")[0]; by.setdefault(m, [0, 0]); by[m][0] += 1; by[m][1] += h
    print(f"{k}  {m[:34]:34s} odds {o:.2f}  {'held' if h else 'FAILED'}  {V[k][1]}")
n = len(V); print(f"\nheld {sum(v[0] for v in V.values())} of {n}; my mean odds {sum(lines[k][1] for k in V) / n:.3f}; Brier {tot / n:.4f}; had I said 0.5 on every line, 0.2500")
print("by the sheet's own marks: " + "; ".join(f"marked {m}: {a} lines, {b} held" for m, (a, b) in by.items()))
