"""Totals of the confirming search for Conjecture E, from its output files.  usage: confirm_summary.py FOLDER"""
import re, glob, sys, os
d = sys.argv[1]; tot = 0; stopped = []; bad = 0; rows = 0
for f in sorted(glob.glob(os.path.join(d, 'confirm-exhaust-*.out'))):
    for line in open(f):
        m = re.match(r'exhaust n=(\d+) m=(\d+): (\d+) multisets containing 0( \(STOPPED[^)]*\)| \(all\)); without a good signing: (\d+)', line)
        if m:
            rows += 1; tot += int(m.group(3)); bad += int(m.group(5))
            if 'STOPPED' in m.group(4): stopped.append((int(m.group(1)), int(m.group(2))))
print('exhaustive part: every multiset containing 0 of 3 to 5 elements on the moduli 22, 26, 28, 32, 40, 42, 60, 64, 72, 96, 120:', rows, 'lines,', tot, 'multisets, without a good signing:', bad, '; stopped at the time limit (not all multisets of that size):', stopped)
ftot = fbad = seeds = ev = od = 0
for f in sorted(glob.glob(os.path.join(d, 'confirm-families-*.out'))):
    t = open(f).read()
    m = re.search(r'count=(\d+)', t); b = re.search(r'without a good signing \(three or more elements\): (\d+)', t)
    e = re.search(r"'even size': (\d+)", t); o = re.search(r"'odd size': (\d+)", t)
    if m and b: seeds += 1; ftot += int(m.group(1)); fbad += int(b.group(1)); ev += int(e.group(1)); od += int(o.group(1))
print('random and structured part (even n up to 2000, 3 to 14 elements):', seeds, 'seeds,', ftot, 'multisets (even size', ev, ', odd size', od, '), without a good signing:', fbad)
