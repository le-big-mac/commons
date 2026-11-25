"""Prints the README's tables from lines.csv, so that no figure in them is typed by hand.   usage: python tables.py lines.csv > tables.md"""
import sys, csv
import numpy as np
R = list(csv.DictReader(open(sys.argv[1]))); S = [r for r in R if r['outcome'] != '']
B = lambda p, y: float(np.mean((np.asarray(p, float) - np.asarray(y, float)) ** 2))
od = lambda rows: [float(r['odds']) for r in rows]; yy = lambda rows: [float(r['outcome']) for r in rows]
fo = lambda r: r['forecasters'] or r.get('forecasters_late', '')
print("**Table 1. Study by study** (all lines: main sheet, follow-ups and bets)\n")
print("| study | sealed | settled | held | my odds, mean | my Brier score |\n|---|---|---|---|---|---|")
for st in dict.fromkeys(r['study'] for r in sorted(R, key=lambda r: int(r['order']))):
    a = [r for r in R if r['study'] == st]; s = [r for r in a if r['outcome'] != '']
    print(f"| {st} | {len(a)} | {len(s)} | {int(sum(yy(s)))} | {np.mean(od(s)):.2f} | {B(od(s), yy(s)):.3f} |")
print(f"| all | {len(R)} | {len(S)} | {int(sum(yy(S)))} | {np.mean(od(S)):.2f} | {B(od(S), yy(S)):.3f} |")
print("\n**Table 2. Were the odds right?**\n")
print("| odds I gave | lines | my odds, mean | held | share held |\n|---|---|---|---|---|")
for lo, hi, name in ((0.0, 0.5, "below 0.5"), (0.5, 0.6, "0.5 up to 0.6"), (0.6, 0.7, "0.6 up to 0.7"), (0.7, 0.8, "0.7 up to 0.8"), (0.8, 0.9, "0.8 up to 0.9"), (0.9, 1.01, "0.9 and above")):
    s = [r for r in S if lo <= float(r['odds']) < hi]; print(f"| {name} | {len(s)} | {np.mean(od(s)):.2f} | {int(sum(yy(s)))} | {np.mean(yy(s)):.2f} |")
print("\n**Table 3. The ten main sheets, mine against three blind forecasters' median**\n")
print("| sheet | priced | settled lines | held | my Brier | theirs | my odds, mean | theirs | closer: mine, theirs |\n|---|---|---|---|---|---|---|---|---|")
M = [r for r in S if r['kind'] == 'sheet']
def row(name, s, when=''):
    f = [float(fo(r)) for r in s]; m, y = od(s), yy(s)
    cm = sum(abs(a - t) < abs(b - t) - 1e-9 for a, b, t in zip(m, f, y)); ct = sum(abs(b - t) < abs(a - t) - 1e-9 for a, b, t in zip(m, f, y))
    print(f"| {name} | {when} | {len(s)} | {int(sum(y))} | {B(m, y):.3f} | {B(f, y):.3f} | {np.mean(m):.2f} | {np.mean(f):.2f} | {cm}, {ct} |")
if all(fo(r) for r in M):
    for st in dict.fromkeys(r['study'] for r in sorted(M, key=lambda r: int(r['order']))):
        s = [r for r in M if r['study'] == st]; row(st, s, 'at the time' if s[0]['forecasters'] else 'afterwards')
    row("the six priced at the time", [r for r in M if r['forecasters']]); row("the four priced afterwards", [r for r in M if not r['forecasters']]); row("all ten", M)
else: print("(forecasts for four sheets not yet in)")
print("\n**Table 4. Doubts and marks**\n")
print("| lines | number | held | my odds, mean | my Brier |\n|---|---|---|---|---|")
own = [r for r in S if r['named_doubt'] == 'marked down']; files = {r['file'] for r in own}; oth = [r for r in S if r['file'] in files and r['named_doubt'] != 'marked down']
for name, s in (("the sheet says \"marked down\" or \"same doubt\"", own), ("the other lines of the sheets that have such a line", oth), ("a doubt worded otherwise (seven lines picked by hand, knowing the outcomes)", [r for r in S if r['named_doubt'] == 'other named doubt']),
                ("marked \"worked\"", [r for r in S if r['marked'] == 'worked']), ("marked \"remembered\"", [r for r in S if r['marked'] == 'remembered']), ("marked \"guessed\"", [r for r in S if r['marked'] == 'guessed'])):
    print(f"| {name} | {len(s)} | {int(sum(yy(s)))} | {np.mean(od(s)):.2f} | {B(od(s), yy(s)):.3f} |")
