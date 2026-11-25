"""Scores the sealed sheet by its letter.   usage: python -I verdicts.py expectations.md results.json > verdicts.out"""
import sys, re, json
sheet = open(sys.argv[1]).read(); R = json.load(open(sys.argv[2]))
lines = {k: (mark, float(o)) for k, mark, o in re.findall(r"^(R\d+)\. \((.*?)\).*?odds (0\.\d+)[ \t]*$", sheet, re.M | re.S)}
inside = lambda v, lo, hi: lo <= v <= hi
q5 = min(float(k) for k, v in R['R5'].items() if v >= 0.9); q11 = min(float(k) for k, v in R['R11'].items() if v >= 0.9); g = R['R9']; chain = [g[k] for k in ("0", "0.25", "0.5", "0.75", "1", "1.5")]
V = {
 'R1': (inside(R['R1'], 0.930, 0.938), f"P = {R['R1']:.4f} (sealed: 0.930 to 0.938)"),
 'R2': (inside(R['R2'], 0.62, 0.68), f"P = {R['R2']:.4f} (sealed: 0.62 to 0.68)"),
 'R3': (inside(R['R3'], 0.72, 0.77), f"P = {R['R3']:.4f} (sealed: 0.72 to 0.77)"),
 'R4': (all(abs(r['formula'] - r['steps']) <= 1e-8 for r in R['R4']), "largest difference between the formula and the step-by-step computation: " + f"{max(abs(r['formula'] - r['steps']) for r in R['R4']):.1e} (sealed: within 0.00000001)"),
 'R5': (inside(q5, 1.33, 1.45), f"the least edge is {q5:.2f}: P = {R['R5'][f'{q5 - 0.01:.2f}']:.4f} at {q5 - 0.01:.2f} and {R['R5'][f'{q5:.2f}']:.4f} at {q5:.2f} (sealed: 1.33 to 1.45)"),
 'R6': (inside(R['R6'], 0.26, 0.34), f"chance {R['R6']:.4f} (sealed: 0.26 to 0.34)"),
 'R7': (inside(g['0.25'], 0.915, 0.932) and g['0.25'] < g['0'], f"P = {g['0.25']:.4f} (sealed: 0.915 to 0.932), against {g['0']:.4f} at g = 0"),
 'R8': (inside(g['0.5'], 0.85, 0.91), f"P = {g['0.5']:.4f} (sealed: 0.85 to 0.91)"),
 'R9': (all(x > y for x, y in zip(chain, chain[1:])), "P = " + ", ".join(f"{x:.4f}" for x in chain)),
 'R10': (inside(R['R10']['N10000'], 0.54, 0.59) and abs(R['R10']['N10000'] - R['R10']['N1000']) <= 0.01, f"P = {R['R10']['N10000']:.4f} after 10,000 (sealed: 0.54 to 0.59) and {R['R10']['N1000']:.4f} after 1,000"),
 'R11': (inside(q11, 1.8, 2.8), f"the least edge is {q11:.2f}: P = {R['R11'][f'{q11 - 0.05:.2f}']:.4f} at {q11 - 0.05:.2f} and {R['R11'][f'{q11:.2f}']:.4f} at {q11:.2f} (sealed: 1.8 to 2.8)"),
 'R12': (inside(R['R12'], 0.76, 0.84), f"P = {R['R12']:.4f} (sealed: 0.76 to 0.84)"),
}
tot = 0.0; by = {}
for k in sorted(V, key=lambda s: int(s[1:])):
    mark, o = lines[k]; h = V[k][0]; tot += (o - h) ** 2; m = mark.split(";")[0]; by.setdefault(m, [0, 0]); by[m][0] += 1; by[m][1] += h
    print(f"{k:4s} {mark.split(';')[0]:14s} odds {o:.2f}  {'held' if h else 'FAILED'}  {V[k][1]}")
n = len(V); print(f"\nheld {sum(v[0] for v in V.values())} of {n}; my mean odds {sum(lines[k][1] for k in V) / n:.3f}; Brier {tot / n:.4f}; had I said 0.9 on every line, {sum((0.9 - v[0]) ** 2 for v in V.values()) / n:.4f}")
print("by the sheet's own marks: " + "; ".join(f"marked {m}: {a} lines, {b} held" for m, (a, b) in by.items()))
