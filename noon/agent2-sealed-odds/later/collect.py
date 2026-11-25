"""Gather every sealed line with odds from the scorecards of the studies published after the report of 22 November.
usage: python -I collect.py > collect.out      Writes lines.csv: study, sheet, label, mark, odds, outcome (1 held, 0 failed, 0.5 half)."""
import re, csv, os, sys
H = os.path.expanduser
SHEETS = [("Mendel's peas", "peas", "verdicts.out"), ("Mendel's peas", "peas", "verdicts2.out"), ("calved ice", "calve", "verdicts.out"), ("hawks and doves", "hawk", "verdicts.out"),
          ("the arXiv's boundary", "cutoff", "verdicts.out"), ("a drumskin", "drum", "verdicts.out"), ("a drumskin", "drum", "verdicts2.out"), ("a drumskin", "drum", "verdicts3.out"), ("outselling", "outsell", "verdicts.out"),
          ("beyond the ninth mode", "drum12", "verdicts.out"), ("the note not sounded", "drumfree", "verdicts.out"), ("air in the drum", "drumair", "verdicts.out"),
          ("who already knew", "prior", "verdicts.out"), ("Mastermind by post", "post", "verdicts.out"), ("Mastermind by post", "post", "verdicts2.out")]
rows = []; odd = []; void = []
for study, folder, f in SHEETS:
    path = H(f"~/{folder}/{f}"); n = 0
    for line in open(path):
        m = re.match(r"^(\S+)\s+(.*?)\s*odds (\d\.\d+)\s+(?:scored\s+)?(\S+)", line)
        if not m: 
            if re.match(r"^[A-Z]\d", line): odd.append((folder, f, line.strip()[:90]))
            continue
        label, mark, odds, word = m.group(1), m.group(2).strip(), float(m.group(3)), m.group(4).lower()
        out = {"held": 1.0, "failed": 0.0, "half": 0.5}.get(word)
        if out is None: (void if word == "void" else odd).append((folder, f, line.strip()[:90])); continue
        rows.append(dict(study=study, sheet=f"{folder}/{f}", label=label, mark=(mark.split()[0] if mark else "none"), odds=odds, outcome=out)); n += 1
    print(f"{study:24s} {folder + '/' + f:24s} {n:3d} lines")
w = csv.DictWriter(open("lines.csv", "w", newline=""), fieldnames=["study", "sheet", "label", "mark", "odds", "outcome"]); w.writeheader(); w.writerows(rows)
print(f"\n{len(rows)} settled lines in {len(SHEETS)} sheets of {len({r['study'] for r in rows})} studies; marks: " + ", ".join(f"{k} {sum(1 for r in rows if r['mark'] == k)}" for k in sorted({r['mark'] for r in rows})))
print(f"void, and so not settled: {len(void)} (" + ", ".join(v[2].split()[0] for v in void) + f" of {void[0][0]}/{void[0][1]})" if void else "void: none")
print("lines that begin like a sealed line and were not taken:"); [print("  ", o) for o in odd] if odd else print("   none")
