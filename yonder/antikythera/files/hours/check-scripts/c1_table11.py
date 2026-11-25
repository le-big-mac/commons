"""Item 1: the checker's typing of Table 11 against hours.py's TABLE11 and against the paper's own column."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import own
# 1. my typed column against the rule
bad = [(c, n, dn, col, own.rule(n, dn)) for c, n, dn, col in own.T11 if own.rule(n, dn) != col % 24]
print('rule against the paper\'s column "Time of day (h)" (mod 24): mismatches', bad)
# 2. hours.py's string, parsed here as text (not imported)
src = open(os.path.join(os.path.dirname(HERE), 'hours.py')).read()
s = src.split('TABLE11 = """')[1].split('"""')[0]
items = [x.split() for x in s.replace('\n', ' ').split(';')]
theirs = [(a, int(b[:-1]), b[-1]) for a, b in items]
mine = [(c, n, dn) for c, n, dn, col in own.T11]
print('entries in hours.py:', len(theirs), '; in my typing:', len(mine), '; identical:', theirs == mine)
for a, b in zip(theirs, mine):
    if a != b: print('  DIFF', a, b)
print('lunar', sum(c.endswith('M') for c, *_ in mine), 'solar', sum(c.endswith('S') for c, *_ in mine))
print('the 18: lunar', sum(c.endswith('M') for c, *_ in mine if c not in own.OUT4), 'solar', sum(c.endswith('S') for c, *_ in mine if c not in own.OUT4))
