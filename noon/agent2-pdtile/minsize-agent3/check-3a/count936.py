"""Recount the audit's 936 from its compare.out: by triple (p, q, n) and by group.
usage: count936.py COMPARE.OUT"""
import sys, re, collections
rows = [l.split(' | ') for l in open(sys.argv[1]).read().splitlines() if l.startswith('Z_')]
by_group = collections.OrderedDict(); tot = 0
for r in rows:
    g = r[0]; pats = int(r[2].split()[0]); m = re.match(r'(\d+) of (\d+) attempted \((\d+) not attempted; (\d+) with the window', r[9])
    settled, attempted, notatt, window = map(int, m.groups()); mism = int(r[10])
    assert settled == attempted and attempted + notatt == pats
    by_group.setdefault(g, []).append((r[1], pats, settled, notatt, mism)); tot += settled
print('rows (triples p,q,n):', len(rows), ' groups:', len(by_group), ' settled, summed over triples:', tot)
once = sum(v[0][2] for v in by_group.values())
twice = [g for g, v in by_group.items() if len(v) > 1]
print('settled, each group counted once:', once, ' groups that appear under two triples:', len(twice), twice)
print('complete groups (every pattern settled):', [g for g, v in by_group.items() if all(x[3] == 0 for x in v)])
print('incomplete groups:', [(g, v[0][2], v[0][1]) for g, v in by_group.items() if any(x[3] for x in v)])
print('mismatches:', sum(x[4] for v in by_group.values() for x in v))
for g in twice:
    v = by_group[g]; print(' ', g, [x[0] for x in v], 'patterns', [x[1] for x in v])
