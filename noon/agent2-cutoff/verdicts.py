"""Scores the nine sealed lines, and prints the tally by the sheet's own marks.   usage: python -I verdicts.py expectations.md results.json"""
import sys, re, json
text = open(sys.argv[1]).read(); odds = {k: float(v) for k, v in re.findall(r"^(T\d)\..*?odds (0\.\d+)[ \t]*$", text, re.M | re.S)}; R = json.load(open(sys.argv[2]))
marks = {k: ('guessed' if m.startswith('guessed') else 'remembered loosely' if m.startswith('remembered loosely') else 'remembered' if m.startswith('remembered') else 'worked') for k, m in re.findall(r"^(T\d)\. \(([a-z ]+)", text, re.M)}
G = ["astro-ph", "hep-th", "hep-ph", "gr-qc", "quant-ph", "maths", "cs.CL"]; a = R["astro-ph"]
V = {'T1': (a['ratio'] >= 3, f"{a['ratio']:.2f} ({a['after']} after, {a['before']} before)"), 'T2': (a['first60'] >= 0.4 * a['after'], f"{a['first60']} of {a['after']} ({100 * a['first60'] / a['after']:.0f}%)"),
     'T3': (R['hep-th']['ratio'] >= 1.5, f"{R['hep-th']['ratio']:.2f}"), 'T4': (R['quant-ph']['ratio'] >= 1.5, f"{R['quant-ph']['ratio']:.2f}"),
     'T5': (0.6 <= R['maths']['ratio'] <= 1.6, f"{R['maths']['ratio']:.2f}"), 'T6': (0.6 <= R['cs.CL']['ratio'] <= 2.0, f"{R['cs.CL']['ratio']:.2f}"),
     'T7': (max(G, key=lambda g: R[g]['ratio']) == 'astro-ph', "largest: " + max(G, key=lambda g: R[g]['ratio'])), 'T8': (all(R[g]['rush'] <= 1.5 for g in G), "largest before / an hour earlier: " + f"{max(R[g]['rush'] for g in G):.2f} ({max(G, key=lambda g: R[g]['rush'])})"),
     'T9': (R['busiest_January'][0] == '19:00' and R['busiest_April,'][0] == '18:00', f"{R['busiest_January'][0]} and {R['busiest_April,'][0]}")}
tot = 0
for k in sorted(V):
    h = bool(V[k][0]); tot += (odds[k] - h) ** 2; print(f"{k:3s} {marks[k]:18s} odds {odds[k]:.2f}  {'held' if h else 'FAILED':6s}  {V[k][1]}")
print(f"held {sum(bool(v[0]) for v in V.values())} of {len(V)}; my mean odds {sum(odds.values()) / len(odds):.3f}; Brier {tot / len(V):.4f}")
for m in ('worked', 'remembered', 'remembered loosely', 'guessed'):
    ks = [k for k in V if marks[k] == m]
    if ks: print(f"marked {m}: {len(ks)} lines, {sum(bool(V[k][0]) for k in ks)} held ({', '.join(sorted(ks))})")
