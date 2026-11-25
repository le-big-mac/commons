"""Scores the six lines of the second sheet against all84.json.   usage: python -I verdicts2.py all84-prediction.md all84.json"""
import sys, re, json
odds = {k: float(v) for k, v in re.findall(r"^(Q\d+)\..*?odds (0\.\d+)[ \t]*$", open(sys.argv[1]).read(), re.M | re.S)}; R = json.load(open(sys.argv[2]))
V = {'Q1': (abs(R['sum'] - 41.6) <= 1.5, f"{R['sum']:.4f}"), 'Q2': (abs(R['max'] - 1.62) <= 0.02 and 'three characters: character 2, hybrid against constant, within H' in R['max_name'], f"{R['max']:.4f}; {R['max_name']}"),
     'Q3': (18 <= R['small'] <= 22, f"{R['small']}"), 'Q4': (1 <= R['lr'] <= 10, f"a factor of {R['lr']:.2f}"), 'Q5': (R['share_lr'] > 0.20, f"{100 * R['share_lr']:.1f}% of sets"), 'Q6': (R['share_small'] < 0.10, f"{100 * R['share_small']:.1f}% of sets")}
tot = 0
for k in sorted(V):
    h = bool(V[k][0]); tot += (odds[k] - h) ** 2; print(f"{k:4s} odds {odds[k]:.2f}  {'held' if h else 'FAILED':6s}  {V[k][1]}")
print(f"held {sum(bool(v[0]) for v in V.values())} of {len(V)}; my mean odds {sum(odds.values()) / len(odds):.3f}; Brier {tot / len(V):.4f}")
