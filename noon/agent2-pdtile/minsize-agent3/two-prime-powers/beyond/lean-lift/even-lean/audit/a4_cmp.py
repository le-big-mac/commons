"""Compares Lean's printed values of csum / levelBad (A4_eval.out) with the expected ones (a4_expected.txt)."""
import sys

lean = {}
for line in open(sys.argv[1]):
    line = line.strip()
    if line.startswith('C'):
        cid, rest = line.split(' ', 1)
        lean[cid] = rest.replace(' ', '')
exp = {}
desc = {}
for line in open(sys.argv[2]):
    body, _, d = line.strip().partition('#')
    cid, rest = body.strip().split(' ', 1)
    exp[cid] = rest.replace(' ', '')
    desc[cid] = d.strip()
bad = [c for c in exp if lean.get(c) != exp[c]]
groups = {}
nonzero_at = 0
strict = 0
for c in exp:
    g = desc[c].split()[0]
    groups[g] = groups.get(g, 0) + 1
print(f"cases {len(exp)}, lines from Lean {len(lean)}, mismatches {len(bad)}; cases per group {groups}")
for c in bad:
    print("MISMATCH", c, desc[c], "\n  lean", lean.get(c), "\n  mine", exp[c])
