"""What the 145 sealed lines show.   usage: python analyse.py lines.csv > analyse.out"""
import sys, csv
import numpy as np
R = [r for r in csv.DictReader(open(sys.argv[1]))]; S = [r for r in R if r['outcome'] != '']
o = lambda rows: np.array([float(r['odds']) for r in rows]); y = lambda rows: np.array([float(r['outcome']) for r in rows])
def line(name, rows):
    if not rows: return
    print(f"   {name:34s} {len(rows):4d} lines; held {int(y(rows).sum()):3d} ({y(rows).mean():.2f}); my mean odds {o(rows).mean():.3f}; Brier {((o(rows) - y(rows)) ** 2).mean():.3f}; a flat price at the share that held would score {y(rows).mean() * (1 - y(rows).mean()):.3f}")
print(f"{len(R)} sealed lines with odds; {len(S)} settled, {len(R) - len(S)} void or not settled")
print("1. All settled lines"); line("all", S)
print("2. By kind"); [line(k, [r for r in S if r['kind'] == k]) for k in ('sheet', 'follow-up', 'bet on my odds')]
print("3. By study, in order of time (all kinds)")
for st in dict.fromkeys(r['study'] for r in sorted(S, key=lambda r: int(r['order']))): line(st, [r for r in S if r['study'] == st])
print("4. Calibration: lines grouped by the odds I gave")
for lo, hi in ((0.0, 0.5), (0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.01)):
    rows = [r for r in S if lo <= float(r['odds']) < hi]
    if rows: print(f"   odds {lo:.2f} to {min(hi, 1.0):.2f}: {len(rows):3d} lines; my mean odds {o(rows).mean():.3f}; held {y(rows).mean():.3f} ({int(y(rows).sum())} of {len(rows)})")
print("5. The six sheets that three blind forecasters also priced")
L = [r for r in S if r['forecasters'] != '']; f = np.array([float(r['forecasters']) for r in L]); m, yy = o(L), y(L)
print(f"   {len(L)} lines; held {yy.mean():.3f}; my mean odds {m.mean():.3f}, theirs {f.mean():.3f}; Brier mine {((m - yy) ** 2).mean():.4f}, theirs {((f - yy) ** 2).mean():.4f}; closer to the outcome: mine {int((abs(m - yy) < abs(f - yy) - 1e-9).sum())}, theirs {int((abs(f - yy) < abs(m - yy) - 1e-9).sum())}, equal {int((abs(abs(m - yy) - abs(f - yy)) <= 1e-9).sum())}")
auc = lambda p: np.mean([(a > b) + 0.5 * (a == b) for a in p[yy == 1] for b in p[yy == 0]])
print(f"   held against failed, how often the held line had the higher odds: mine {auc(m):.2f}, theirs {auc(f):.2f}")
shift = f.mean() - m.mean(); print(f"   my odds moved up by {shift:.3f} (to their mean, capped at 0.99) would score {((np.minimum(m + shift, 0.99) - yy) ** 2).mean():.4f}")
for lo, hi in ((0.0, 0.6), (0.6, 0.8), (0.8, 0.9), (0.9, 1.01)):
    k = (f >= lo) & (f < hi)
    if k.any(): print(f"   their odds {lo:.2f} to {min(hi, 1.0):.2f}: {int(k.sum()):3d} lines; their mean {f[k].mean():.3f}; held {yy[k].mean():.3f}")
print("6. Lines whose own sealed text names a doubt, against the other lines of the same sheets")
files = {r['file'] for r in S if r['named_doubt']}
D = [r for r in S if r['file'] in files]
line("says 'marked down'", [r for r in D if r['named_doubt'] == 'marked down']); line("doubt worded otherwise", [r for r in D if r['named_doubt'] == 'other named doubt']); line("either", [r for r in D if r['named_doubt']]); line("neither, same sheets", [r for r in D if not r['named_doubt']])
print("   sheets: " + ", ".join(sorted(files)))
print("   lines: " + ", ".join(f"{r['label']} ({r['odds']}, {'held' if r['outcome'] == '1' else 'failed'}{', other' if r['named_doubt'] != 'marked down' else ''})" for r in D if r['named_doubt']))
print("7. Lines I marked as worked, remembered or guessed before sealing (only the last two sets carry the marks)")
for k in ('worked', 'remembered', 'guessed'): line(k, [r for r in S if r['marked'] == k])
print("8. Before and after the resolution of 21 November, about 21:00 (after the onset sheet): main sheets only")
line("sheets 1 to 7 (through onset)", [r for r in S if r['kind'] == 'sheet' and int(r['order']) <= 7]); line("sheets 8 to 10 (taffy, cannonballs, arctic)", [r for r in S if r['kind'] == 'sheet' and int(r['order']) >= 8])
print("9. Three broad groups of my odds")
for lo, hi, name in ((0.0, 0.6, "below 0.6"), (0.6, 0.8, "0.6 up to 0.8"), (0.8, 1.01, "0.8 and above")):
    rows = [r for r in S if lo <= float(r['odds']) < hi]; print(f"   {name:14s}: {len(rows):3d} lines; my mean odds {o(rows).mean():.3f}; held {y(rows).mean():.3f} ({int(y(rows).sum())} of {len(rows)})")
print("10. The lines that failed, by the odds I gave")
for r in sorted([r for r in S if r['outcome'] == '0'], key=lambda r: -float(r['odds'])): print(f"   {r['odds']}  {r['study']:20s} {r['label']:4s} {r['kind']:15s} {r['file']}")
print("11. Failures by kind of sheet: main sheets of the six studies the forecasters priced, the other four main sheets, follow-ups, bets")
fcs = {r['study'] for r in S if r['forecasters']}
line("six priced sheets", [r for r in S if r['kind'] == 'sheet' and r['study'] in fcs]); line("four other sheets", [r for r in S if r['kind'] == 'sheet' and r['study'] not in fcs])
print("12. The forecasters' gap, sheet by sheet")
for st in dict.fromkeys(r['study'] for r in sorted(L, key=lambda r: int(r['order']))):
    rows = [r for r in L if r['study'] == st]; ff = np.array([float(r['forecasters']) for r in rows]); mm, y2 = o(rows), y(rows)
    print(f"   {st:22s} {len(rows):3d} lines; held {int(y2.sum()):2d}; mine {((mm - y2) ** 2).mean():.4f} (mean odds {mm.mean():.3f}); theirs {((ff - y2) ** 2).mean():.4f} (mean odds {ff.mean():.3f}); closer: mine {int((abs(mm - y2) < abs(ff - y2) - 1e-9).sum())}, theirs {int((abs(ff - y2) < abs(mm - y2) - 1e-9).sum())}")
