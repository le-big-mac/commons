"""Checks every count in data.py against the text of the paper.   usage: python -I verify.py MENDEL.txt     (run from the folder holding data.py)"""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[0])))
import data
t = " ".join(open(sys.argv[1], encoding='utf-8').read().split()); ok = n = 0
for e in data.E:
    name, group, counts, parts, pat = e[:5]
    if pat is None: continue
    n += 1; m = re.search(pat, t)
    if not m: print("NOT FOUND:", name); continue
    got = tuple(int(g) for g in m.groups())
    if len(e) > 5 and e[5] == "swap": got = got[::-1]
    good = got == tuple(counts); ok += good; print(("ok       " if good else "DIFFERS  ") + name, "" if good else (counts, got))
m = re.search(data.PLANTS_PATTERN, t); n += 1
if m:
    got = [tuple(int(x) for x in m.groups()[4 * i: 4 * i + 4]) for i in range(10)]; good = got == data.PLANTS; ok += good; print(("ok       " if good else "DIFFERS  ") + "the table of ten plants", "" if good else got)
else: print("NOT FOUND: the table of ten plants")
print(f"{ok} of {n} passages found in the text with exactly the counts in data.py; {sum(len(e[2]) for e in data.E)} counts in all")
assert sum(data.K27_COUNTS) == 639 and sorted(data.K27_PARTS) == [1] * 8 + [2] * 12 + [4] * 6 + [8]
