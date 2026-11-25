"""Small follow-ups. Usage: python -I attack3.py DATADIR > attack3.out"""
import sys, math
sys.path.insert(0, '/home/agent2/birth/referee')
from reflib import *

D = sys.argv[1]
bb, _ = people(os.path.join(D, 'baseball-usa.csv'))
print('baseball, top month by births per day in Noon\'s four bands and others:')
for lo, hi in [(1900, 1939), (1940, 1959), (1960, 1979), (1980, 2005), (1900, 1949), (1950, 1989)]:
    rr = [r for r in bb if lo <= r[1][0] <= hi]
    c = month_counts(rr)
    pdv = per_day(c)
    mean = sum(pdv) / 12
    o = sorted(range(12), key=lambda i: -pdv[i])
    # step at 1 Aug: 18-31 Jul against 1-14 Aug
    b = sum(1 for r in rr if r[1][1] == 7 and r[1][2] >= 18)
    a = sum(1 for r in rr if r[1][1] == 8 and r[1][2] <= 14)
    print('   %d-%d n=%5d top %s %.2f, %s %.2f, %s %.2f | Aug-Oct %.1f | 18-31 Jul %d, 1-14 Aug %d, ratio %.2f (%.1f se)' % (
        lo, hi, len(rr), MN[o[0]], pdv[o[0]] / mean, MN[o[1]], pdv[o[1]] / mean, MN[o[2]], pdv[o[2]] / mean,
        share(c, [8, 9, 10]), b, a, a / b, (a - b) / math.sqrt(a + b)))
print('athletes born 1960 or later against controls born 1960 or later, and men only:')
for a, s, pol in [('football-spain', 1, 'politicians-spain'), ('football-brazil', 1, 'politicians-brazil'), ('football-germany', 1, 'politicians-germany'),
                  ('hockey-canada', 1, 'politicians-canada'), ('football-uk', 9, 'politicians-uk'), ('football-japan', 4, 'politicians-japan'),
                  ('baseball-usa', 8, 'house-usa')]:
    A, _ = people(os.path.join(D, a + '.csv'))
    C, _ = people(os.path.join(D, pol + '.csv'))
    A6 = [r for r in A if r[1][0] >= 1960]
    C6 = [r for r in C if r[1][0] >= 1960]
    Cm = [r for r in C if r[2] == 'M']
    Am = [r for r in A if r[2] == 'M']
    w = window(s)
    print('   %-17s %s athletes>=1960 %.1f (n=%d) control>=1960 %.1f (n=%d) | men: athletes %.1f (n=%d) control %.1f (n=%d)' % (
        a, wname(s), share(month_counts(A6), w), len(A6), share(month_counts(C6), w), len(C6),
        share(month_counts(Am), w), len(Am), share(month_counts(Cm), w), len(Cm)))
