"""Scores the two short sheets.   usage: python -I verdicts2.py graded-prediction.md layers-prediction.md after.json layers-2.json layers-3.json clash.out"""
import sys, re, json
def odds(path, letter): return {k: float(v) for k, v in re.findall(rf"^({letter}\d)\..*?odds (0\.\d+)[ \t]*$", open(path).read(), re.M | re.S)}
og, ol = odds(sys.argv[1], "G"), odds(sys.argv[2], "L"); A = json.load(open(sys.argv[3]))['graded']; L2 = json.load(open(sys.argv[4])); L3 = json.load(open(sys.argv[5]))
cl = {m.group(1): float(m.group(2)) for m in re.finditer(r"strokes-([a-z\-]+)\.wav\s+semitone clash ([0-9.]+)", open(sys.argv[6]).read())}
V = {'G1': (A['miss'] < 0.03157, f"{100 * A['miss']:.3f}% (at s = {A['s']:.0f}, the upper edge of the sealed range)"), 'G2': (A['k'] > 0.45, f"k = {A['k']:.3f}"), 'G3': (A['s'] > 12, f"s = {A['s']:.0f}"),
     'L1': (L2['miss'] < 0.02, f"{100 * L2['miss']:.3f}%"), 'L2': (L3['miss'] < 0.01, f"{100 * L3['miss']:.3f}%"), 'L3': (cl['three-layers'] < 0.585, f"{cl['three-layers']:.3f} (plain {cl['plain']:.3f}; even disc {cl['disc']:.3f}; two layers {cl['two-layers']:.3f})")}
for name, o in (("the graded patch", og), ("layers", ol)):
    tot = 0
    for k in sorted(o):
        h = bool(V[k][0]); tot += (o[k] - h) ** 2; print(f"{k}  guessed  odds {o[k]:.2f}  {'held' if h else 'FAILED':6s}  {V[k][1]}")
    print(f"{name}: held {sum(bool(V[k][0]) for k in o)} of {len(o)}; my mean odds {sum(o.values()) / len(o):.3f}; Brier {tot / len(o):.4f}; marked guessed: {len(o)} lines, {sum(bool(V[k][0]) for k in o)} held")
