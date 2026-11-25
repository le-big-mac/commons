"""Scores the eight sealed lines, and prints the tally by the sheet's own marks.   usage: python -I verdicts.py expectations.md results.json"""
import sys, re, json
text = open(sys.argv[1]).read(); odds = {k: float(v) for k, v in re.findall(r"^(H\d)\..*?odds (0\.\d+)[ \t]*$", text, re.M | re.S)}; R = json.load(open(sys.argv[2]))
marks = {k: ('guessed' if m.startswith('guessed') else 'remembered' if m.startswith('remembered') else 'worked') for k, m in re.findall(r"^(H\d)\. \(([a-z]+)", text, re.M)}
V = {'H1': (R['H1'] <= 0.02, f"largest miss {R['H1']:.4f}"), 'H2': (R['H2'] > 0.95, f"smaller of the two shares {R['H2']:.4f}"), 'H3': (R['H3'] < 0.5, f"{R['H3']:.4f}"),
     'H4': (R['H4'] is not None and 0.62 <= R['H4'] <= 0.76, f"{R['H4']}"), 'H5': (0.26 <= R['H5'] <= 0.46, f"{R['H5']}"), 'H6': (R['H6'] < 0.5, f"{R['H6']:.4f}"),
     'H7': (R['H7'] <= 0.05, f"larger difference {R['H7']:.4f}"), 'H8': (R['H8'] >= 0.3, f"{R['H8']:+.3f}")}
tot = 0
for k in sorted(V):
    h = bool(V[k][0]); tot += (odds[k] - h) ** 2; print(f"{k:3s} {marks[k]:11s} odds {odds[k]:.2f}  {'held' if h else 'FAILED':6s}  {V[k][1]}")
print(f"held {sum(bool(v[0]) for v in V.values())} of {len(V)}; my mean odds {sum(odds.values()) / len(odds):.3f}; Brier {tot / len(V):.4f}")
for m in ('worked', 'remembered', 'guessed'):
    ks = [k for k in V if marks[k] == m]
    if ks: print(f"marked {m}: {len(ks)} lines, {sum(bool(V[k][0]) for k in ks)} held ({', '.join(sorted(ks))})")
