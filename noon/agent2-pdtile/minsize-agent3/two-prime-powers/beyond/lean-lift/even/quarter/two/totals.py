#!/usr/bin/env python3
"""totals of the outputs of test_cells.py (tests.out, tests2.out)"""
import re, sys, ast
tot = {}
runs = 0
for fn in sys.argv[1:]:
    for line in open(fn):
        if 'NO FAILURE' not in line:
            continue
        runs += 1
        d = ast.literal_eval(re.search(r'\{.*?\}', line).group(0))
        for k, v in d.items():
            tot[k] = tot.get(k, 0) + v
print("runs:", runs, tot)
