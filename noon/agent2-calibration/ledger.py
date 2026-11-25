"""Add one study's sealed odds to the running ledger.   usage: python -I ledger.py ledger.csv STUDY DATE scored.json
scored.json (written by a study's score.py) holds ids, outcome, mine, forecasters, median."""
import sys, json, csv, os
path, study, date, src = sys.argv[1:5]
S = json.load(open(src))
rows = []
if os.path.exists(path):
    rows = [r for r in csv.DictReader(open(path)) if r['study'] != study]
for j, i in enumerate(S['ids']):
    rows.append(dict(date=date, study=study, label=i, my_odds=f"{S['mine'][j]:.2f}", forecasters_median=f"{S['median'][j]:.2f}", forecasters=len(S['forecasters']), outcome=f"{S['outcome'][j]:g}"))
with open(path, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['date', 'study', 'label', 'my_odds', 'forecasters_median', 'forecasters', 'outcome'])
    w.writeheader(); w.writerows(rows)
import numpy as np
y = np.array([float(r['outcome']) for r in rows]); me = np.array([float(r['my_odds']) for r in rows]); fm = np.array([float(r['forecasters_median']) for r in rows])
print(f"ledger: {len(rows)} expectations in {len(set(r['study'] for r in rows))} studies; held {y.mean():.3f}; my mean odds {me.mean():.3f}, forecasters' {fm.mean():.3f}; "
      f"Brier mine {((me - y) ** 2).mean():.4f}, forecasters' {((fm - y) ** 2).mean():.4f}")
