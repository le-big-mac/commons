"""Totals of the exhaustive runs of ref_lemma2.py (files lemma2_exh_*.out): contractible levels only."""
import glob, re
tot = [0] * 6; br = [0] * 6; p3 = [0] * 6; non = [0] * 6
files = sorted(f for f in glob.glob('lemma2_exh_*.out') if re.search(r'exh_\d+_\d+\.out$', f))
for fn in files:
    for line in open(fn):
        m = re.match(r"\s+\((.*)\) : (\d+), (\d+), (\d+), (\d+), (\d+), (\d+)", line)
        if not m: continue
        v = [int(x) for x in m.groups()[1:]]
        if 'NOT contractible' in m.group(1):
            non = [a + b for a, b in zip(non, v)]; continue
        tot = [a + b for a, b in zip(tot, v)]
        if "'branching'" in m.group(1): br = [a + b for a, b in zip(br, v)]
        if "'p=3'" in m.group(1): p3 = [a + b for a, b in zip(p3, v)]
names = 'pairs (multiset, contractible level), signings, bad for B, good for B-flat, VIOLATIONS, good for B and bad for B-flat'
print('groups:', ', '.join(re.search(r'exh_(\d+)_(\d+)', f).expand(r'Z_\1 (up to \2 elements)') for f in files))
print(names)
print('all contractible levels :', tot)
print('  the level branches    :', br)
print('  p = 3                 :', p3)
print('levels NOT contractible :', non, ' (the implication fails there in the fifth number of cases: the test has teeth)')
