"""Totals of the test outputs.  usage: totals.py FILE..."""
import sys, re
tot = {}; runs = 0; fails = 0
for fn in sys.argv[1:]:
    for line in open(fn):
        if '| no failure |' in line:
            runs += 1
            for k, v in re.findall(r'(\w+)=(\d+)', line.split('| no failure |')[1]):
                tot[k] = tot.get(k, 0) + int(v)
        elif 'Traceback' in line or 'Error' in line: fails += 1
print(f"runs without failure: {runs}; lines with an error: {fails}")
print(' '.join(f"{k}={v:,}" for k, v in tot.items()))
