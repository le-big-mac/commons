"""What the shaken restarts of exact6.py ended at.   usage: python -I shake-summary.py exact6-shake-*.out"""
import sys, re
ends = {}
for f in sys.argv[1:]:
    for m, t, t0 in re.findall(r"weight\s+([\d.]+), .*?: ([\d.]+)% \(the walks' answer ([\d.]+)%\)", open(f).read()): ends.setdefault((float(m), float(t0)), []).append(float(t))
for (m, t0), v in sorted(ends.items()):
    print(f"added mass {m:g}: {len(v)} shaken restarts; the walks' answer {t0:.4f}%; lowest end {min(v):.4f}%; {sum(abs(x - t0) < 0.002 for x in v)} ended within 0.002 points of the walks' answer, {sum(x < t0 - 0.002 for x in v)} below it, {sum(x > t0 + 0.002 for x in v)} above (the highest {max(v):.4f}%)")
