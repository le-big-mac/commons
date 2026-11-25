"""Scores the fourth sheet.   usage: python -I verdicts3.py exact-prediction.md exact.json exact2.json chain-free-down.json chain-free-up.json rings2-free-12.json rings2-piled-12.json
(the least found anywhere within the sealed limits, 40 rings and 12 skins, counts against X1: the sealed search, the longer restarts, the two
walks of exact5.py and the searches of rings2.py; all by finite differences with 2,000 cells, as sealed)"""
import sys, re, json
o = {k: float(v) for k, v in re.findall(r"^(X\d)\..*?odds (0\.\d+)[ \t]*$", open(sys.argv[1]).read(), re.M | re.S)}; E = json.load(open(sys.argv[2])); E2 = json.load(open(sys.argv[3]))
walks = [r['miss'] for f in sys.argv[4:6] for r in json.load(open(f)) if r['weight'] <= 12.0]
R2 = json.load(open(sys.argv[6]))['rings']['40']['miss']; P2 = json.load(open(sys.argv[7]))['rings']['40']['miss']
least = min(min(r['miss1'] for r in E['runs']), E2['best40']['miss'], min(walks), R2); exact = least <= 5e-4
V = {'X1': (exact, f"no patch within 0.05% was found: the least largest miss found is {100 * least:.4f}% ({100 * min(r['miss1'] for r in E['runs']):.4f}% in the sealed search); 'exists' cannot be failed by a search, so this is my scoring, not the letter's"),
     'X2': (None, "void: X1 failed"), 'X3': (None, "void: X1 failed"), 'X4': (None, "void: X1 failed"), 'X5': (E['monotone']['miss'] >= 0.005, f"least found {100 * min(E['monotone']['miss'], P2):.4f}% ({100 * E['monotone']['miss']:.4f}% in the sealed search)")}
tot = n = 0
for k in sorted(V):
    h = V[k][0]
    if h is None: print(f"{k}  guessed  odds {o[k]:.2f}  void    {V[k][1]}"); continue
    tot += (o[k] - h) ** 2; n += 1; print(f"{k}  guessed  odds {o[k]:.2f}  {'held' if h else 'scored FAILED':6s}  {V[k][1]}")
print(f"any radial shape: held {sum(1 for v in V.values() if v[0] is True)} of {n} scored (3 void); my mean odds on the scored lines {sum(o[k] for k in V if V[k][0] is not None) / n:.3f}; Brier {tot / n:.4f}; marked guessed: {n} lines scored, {sum(1 for v in V.values() if v[0] is True)} held")
