"""Scores the eight sealed lines.   usage: python -I verdicts.py expectations.md results.json"""
import sys, re, json, math
odds = {k: float(v) for k, v in re.findall(r"^(I\d)\..*?odds (0\.\d+)[ \t]*$", open(sys.argv[1]).read(), re.M | re.S)}; R = json.load(open(sys.argv[2])); d = R['d']
V = {'I1': (abs(R['t_upright'] - 0.7521) <= 0.002, f"{R['t_upright']:.5f}"), 'I2': (abs(R['t_side'] - 1.3297) <= 0.004, f"{R['t_side']:.5f}"),
     'I3': (R['lean_0745'] is not None and 10 <= R['lean_0745'] <= 12, f"{R['lean_0745']:.2f} degrees"), 'I4': (0.69 <= R['e_end'] <= 0.74, f"{R['e_end']:.4f}"),
     'I5': (abs(R['energy_05'] / 0.01317 - 1) <= 0.01, f"{R['energy_05']:.5f}"), 'I6': (abs(R['e_max'] - 0.50) < 1e-9, f"{R['e_max']:.2f}"),
     'I7': (R['t90'] is not None and 8 <= R['t90'] <= 13, f"{R['t90']:.2f}"), 'I8': (R['max_tilt_40'] > 170, f"{R['max_tilt_40']:.1f} degrees at most")}
marks = {k: ('guessed' if m.startswith('guessed') else 'remembered' if m.startswith('remembered') else 'worked roughly' if m.startswith('worked roughly') else 'worked') for k, m in re.findall(r"^(I\d)\. \(([a-z ]+)", open(sys.argv[1]).read(), re.M)}
tot = 0
for k in sorted(V):
    h = bool(V[k][0]); tot += (odds[k] - h) ** 2; print(f"{k:3s} {marks[k]:14s} odds {odds[k]:.2f}  {'held' if h else 'FAILED':6s}  {V[k][1]}")
print(f"held {sum(bool(v[0]) for v in V.values())} of {len(V)}; my mean odds {sum(odds.values()) / len(odds):.3f}; Brier {tot / len(V):.4f}")

for m in ('worked', 'worked roughly', 'remembered', 'guessed'):
    ks = [k for k in V if marks[k] == m]
    if ks: print(f"marked {m}: {len(ks)} lines, {sum(bool(V[k][0]) for k in ks)} held ({', '.join(sorted(ks))})")
