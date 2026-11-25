"""Scores the six sealed lines about the correction against recal.out.   usage: python recal-score.py recal-prediction.md recal.out"""
import sys, re
odds = dict(re.findall(r"^(Y\d)\..*?odds (0\.\d+)[ \t]*$", open(sys.argv[1]).read(), re.M | re.S)); out = open(sys.argv[2]).read()
both, shift = out.split("shift only:")
g = lambda pat, txt: re.search(pat, txt)
sealed = float(g(r"all 142 lines: sealed (\d\.\d+)", both).group(1)); c1 = float(g(r"all 142 lines: sealed \d\.\d+, corrected (\d\.\d+)", both).group(1)); c2 = float(g(r"all 142 lines: sealed \d\.\d+, corrected (\d\.\d+)", shift).group(1))
nb = int(g(r"score better corrected: (\d+) of 10", both).group(1)); worst = g(r"harmed most: (.*?) \(", both).group(1)
c66, f66 = map(float, g(r"forecasters priced: sealed \d\.\d+, corrected (\d\.\d+), forecasters (\d\.\d+)", both).groups()); b = float(g(r"b = (\d\.\d+); scores", both).group(1))
V = dict(Y1=(c1 < sealed, f"{c1:.4f} against {sealed:.4f}"), Y2=(c2 < sealed, f"{c2:.4f} against {sealed:.4f}"), Y3=(nb >= 6, f"{nb} of 10"), Y4=(c66 > f66, f"{c66:.4f} against {f66:.4f}"), Y5=(b > 1, f"b = {b:.3f}"), Y6=(worst == "arctic circle", worst))
tot = 0
for k in sorted(V):
    p = float(odds[k]); h = V[k][0]; tot += (p - h) ** 2; print(f"{k}  odds {p:.2f}  {'held' if h else 'FAILED':6s}  {V[k][1]}")
print(f"held {sum(v[0] for v in V.values())} of {len(V)}; my mean odds {sum(map(float, odds.values())) / len(odds):.3f}; Brier {tot / len(V):.4f}")
