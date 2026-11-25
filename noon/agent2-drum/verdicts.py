"""Scores the six sealed lines, and prints the tally by the sheet's own marks.   usage: python -I verdicts.py expectations.md results.json"""
import sys, re, json
text = open(sys.argv[1]).read(); odds = {k: float(v) for k, v in re.findall(r"^(D\d)\..*?odds (0\.\d+)[ \t]*$", text, re.M | re.S)}; R = json.load(open(sys.argv[2]))
marks = {k: m.strip() for k, m in re.findall(r"^(D\d)\. \((worked|remembered loosely|remembered|guessed)", text, re.M)}
want = [1, 1.593, 2.136, 2.295, 2.653, 2.917, 3.155, 3.500, 3.598]; T = [1, 2, 3, 3, 4, 4, 5, 5, 5]; r = R['ratios']
V = {'D1': (all(abs(a - b) <= 0.002 for a, b in zip(R['unloaded'], want)), "largest difference " + f"{max(abs(a - b) for a, b in zip(R['unloaded'], want)):.4f}"),
     'D2': (R['best_miss'] <= 0.05, f"largest miss {100 * R['best_miss']:.2f}%"), 'D3': (0.3 <= R['best_k'] <= 0.5 and 5 <= R['best_s'] <= 15, f"k = {R['best_k']:.3f}, s = {R['best_s']:.2f}"),
     'D4': (all(x > 1.593 for x in R['d4']), "smallest " + f"{min(R['d4']):.4f}"),
     'D5': (abs(r[2] / r[3] - 1) <= 0.02 and abs(r[4] / r[5] - 1) <= 0.02, f"{100 * abs(r[2] / r[3] - 1):.2f}% and {100 * abs(r[4] / r[5] - 1):.2f}%"),
     'D6': (not all(abs(x / 6 - 1) <= 0.03 for x in R['next']), ", ".join(f"{100 * (x / 6 - 1):+.1f}%" for x in R['next']))}
tot = 0
for k in sorted(V):
    h = bool(V[k][0]); tot += (odds[k] - h) ** 2; print(f"{k:3s} {marks[k]:18s} odds {odds[k]:.2f}  {'held' if h else 'FAILED':6s}  {V[k][1]}")
print(f"held {sum(bool(v[0]) for v in V.values())} of {len(V)}; my mean odds {sum(odds.values()) / len(odds):.3f}; Brier {tot / len(V):.4f}")
for m in ('worked', 'remembered', 'remembered loosely', 'guessed'):
    ks = [k for k in V if marks[k] == m]
    if ks: print(f"marked {m}: {len(ks)} lines, {sum(bool(V[k][0]) for k in ks)} held ({', '.join(sorted(ks))})")
