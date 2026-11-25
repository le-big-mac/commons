"""Scores the sealed sheet by its letter.   usage: python -I verdicts.py expectations.md > verdicts.out
(reads classes.json, my classes, and final.json, the referee's blind classes, which decide where the two differ)"""
import sys, re, json, os
sheet = open(sys.argv[1]).read(); lines = {k: (mark, float(o)) for k, mark, o in re.findall(r"^(W\d+)\. \((.*?)\).*?odds (0\.\d+)[ \t]*$", sheet, re.M | re.S)}
mine = json.load(open("classes.json")); ref = json.load(open("final.json")) if os.path.exists("final.json") else {}; cls = {k: ref.get(k, mine[k]) for k in mine}
val = {"found": 1.0, "found in part": 0.5, "not found": 0.0}; word = {1.0: "held", 0.5: "HALF", 0.0: "FAILED"}; tot = 0.0; by = {}; n_held = n_half = n_fail = 0
for k in sorted(mine, key=lambda s: int(s[1:])):
    mark, o = lines[k]; v = val[cls[k]]; tot += (o - v) ** 2; by.setdefault(mark, [0, 0, 0, 0]); by[mark][0] += 1; by[mark][1] += v == 1; by[mark][2] += v == 0.5; by[mark][3] += v == 0
    print(f"{k:4s} {mark:10s} odds {o:.2f}  {word[v]:6s}  {cls[k]}" + ("" if not ref else ("" if ref[k] == mine[k] else f" (the referee's class; mine was '{mine[k]}')")))
score = sum(val[c] for c in cls.values()); mark, o = lines["W17"]; h = score >= 10; tot += (o - h) ** 2; by.setdefault(mark, [0, 0, 0, 0]); by[mark][0] += 1; by[mark][1 if h else 3] += 1
print(f"W17  {mark:10s} odds {o:.2f}  {'held' if h else 'FAILED':6s}  found, counting a part as a half: {score:g} of 16 (sealed: at least ten)")
n = len(mine) + 1; held = sum(v[1] for v in by.values()); half = sum(v[2] for v in by.values()); failed = sum(v[3] for v in by.values())
print(f"\nheld {held}, half {half}, failed {failed}, of {n}; my mean odds {sum(lines[k][1] for k in list(mine) + ['W17']) / n:.3f}; Brier {tot / n:.4f} (a half counted as 0.5); had I said 0.5 on every line, {sum((0.5 - val[cls[k]]) ** 2 for k in mine) / n + 0.25 / n:.4f}")
print("by the sheet's own marks: " + "; ".join(f"marked {m}: {a} lines, {b} held, {c} half, {d} failed" for m, (a, b, c, d) in by.items()))
