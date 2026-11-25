"""Line by line: the expectations on which my sealed sheet names a doubt, against the rest.   usage: python markdowns.py SHEET1 SCORED1 SHEET2 SCORED2 ...
A line counts as "doubted" if its sealed text contains one of the phrases below (chosen by reading the two sheets that carry such remarks)."""
import sys, re, json
import numpy as np
PHRASES = ["Marked down", "less surely", "guessing", "Same doubt", "memory alone", "I believe this jump"]
rows = []
for sheet, scored in zip(sys.argv[1::2], sys.argv[2::2]):
    text = open(sheet, encoding='utf-8').read(); S = json.load(open(scored))
    for m in re.finditer(r"^([A-Z]\d+)\.(.*?)odds (0\.\d+)\s*$", text, re.M | re.S):
        lab, body = m.group(1), m.group(2); j = S['ids'].index(lab)
        hit = [p for p in PHRASES if p in " ".join(body.split())]
        rows.append(dict(label=lab, doubted=bool(hit), phrase=hit[0] if hit else "", mine=S['mine'][j], theirs=S['median'][j], y=S['outcome'][j]))
for name, sel in (("lines with a named doubt", True), ("lines without", False)):
    R = [r for r in rows if r['doubted'] == sel]; y = np.array([r['y'] for r in R]); m = np.array([r['mine'] for r in R]); f = np.array([r['theirs'] for r in R])
    print(f"{name}: {len(R)}; held {int(y.sum())}; my mean odds {m.mean():.3f}, the forecasters' {f.mean():.3f}; Brier mine {((m - y) ** 2).mean():.4f}, theirs {((f - y) ** 2).mean():.4f}")
    for r in R: print(f"   {r['label']:4s} {'held  ' if r['y'] == 1 else 'failed'}  mine {r['mine']:.2f}  theirs {r['theirs']:.2f}" + (f"   (\"{r['phrase']}\")" if r['phrase'] else ""))
