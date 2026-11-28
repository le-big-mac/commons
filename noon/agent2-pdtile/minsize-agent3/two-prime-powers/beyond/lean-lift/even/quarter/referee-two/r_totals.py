#!/usr/bin/env python3
"""Referee: totals of the test outputs named on the command line."""
import re, sys
from fractions import Fraction as F
tot = {}; fails = 0; runs = 0; best = {}
for fn in sys.argv[1:]:
    for line in open(fn):
        if line.startswith(("lem", "exh")):
            runs += 1
            mm = re.search(r'failures=(\d+)', line); fails += int(mm.group(1))
            m = int(re.search(r' m=(\d+)', line).group(1))
            sh = F(re.search(r'largest bad share[ =](\S+)', line).group(1))
            if line.startswith("exh"):
                tot["exh multisets"] = tot.get("exh multisets", 0) + int(re.search(r'multisets=(\d+)', line).group(1))
                tot["exh signings"] = tot.get("exh signings", 0) + int(re.search(r'multisets=(\d+)', line).group(1)) * 2 ** m
            best[m] = max(best.get(m, F(0)), sh)
        elif line.startswith("   ") and ":" in line and "FAILURE" not in line:
            for part in line.strip().split(";"):
                k, v = part.rsplit(":", 1)
                tot[k.strip()] = tot.get(k.strip(), 0) + int(v)
        if "FAILURE" in line:
            print(line.rstrip())
print("runs:", runs, " failures:", fails)
for k in sorted(tot):
    print("  %s: %d" % (k, tot[k]))
print("largest bad share met, by m:", ", ".join("%d: %s" % (m, best[m]) for m in sorted(best)))
