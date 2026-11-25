"""Blind recomputation, written before reading anything of Noon's except expectations.md.
Usage: python -I blind.py DATADIR [rule]
"""
import sys
sys.path.insert(0, '/home/agent2/birth/referee')
from reflib import *

D = sys.argv[1]
RULE = sys.argv[2] if len(sys.argv) > 2 else 'first'


def P(*a):
    print(*a)


def load(name, **kw):
    return people(os.path.join(D, name + '.csv'), rule=RULE, **kw)


REG = ['football-spain', 'football-uk', 'football-japan', 'football-germany', 'football-brazil',
       'hockey-canada', 'baseball-usa', 'politicians-spain']
P('# blind.out -- referee, dedup rule for people with several dates: %s' % RULE)
P('# rules: one record per person, born 1900..2005, 1 January dropped; share = share of the remaining births')
P('# even-births baseline with 1 Jan out: Jan-Mar %.2f  Apr-Jun %.2f  Sep-Nov %.2f  Aug-Oct %.2f' % (
    even_share([1, 2, 3]), even_share([4, 5, 6]), even_share([9, 10, 11]), even_share([8, 9, 10])))
P()
P('## 1. people counted, eight registered groups')
G = {}
for g in REG:
    recs, diag = load(g)
    G[g] = recs
    P('%-18s counted %6d | rows %6d persons %6d multi-date %4d multi-sex %3d out-of-years %5d jan1-dropped %4d bad %d' % (
        g, diag['counted'], diag['rows'], diag['persons'], diag['multi_date'], diag['multi_sex'],
        diag['out_of_years'], diag['jan1'], diag['bad_dates']))
P()
P('## 2. M1..M11')


def q(g, months):
    return share(month_counts(G[g]), months)


def blocks(g, start):
    c = month_counts(G[g])
    return [(wname(s), share(c, window(s))) for s in [start, (start + 2) % 12 + 1, (start + 5) % 12 + 1, (start + 8) % 12 + 1]]


def fmtb(bl):
    return '  '.join('%s %.2f' % b for b in bl)


n = {g: len(G[g]) for g in G}
void = {g: n[g] < 1500 for g in G}

v = q('football-spain', [1, 2, 3])
P('M1  Spain football Jan-Mar = %.2f%% (n=%d); need >=28 -> %s' % (v, n['football-spain'], 'HELD' if v >= 28 else 'FAILED'))

bl = blocks('football-uk', 9)
v = bl[0][1]
ok = v >= 27 and v == max(b[1] for b in bl)
P('M2  UK football Sep-Nov = %.2f%% (n=%d); blocks: %s; need >=27 and largest -> %s' % (v, n['football-uk'], fmtb(bl), 'HELD' if ok else 'FAILED'))

bl = blocks('football-japan', 4)
v = bl[0][1]
ok = v >= 28 and v == max(b[1] for b in bl)
P('M3  Japan football Apr-Jun = %.2f%% (n=%d); blocks: %s; need >=28 and largest -> %s' % (v, n['football-japan'], fmtb(bl), 'HELD' if ok else 'FAILED'))

v = q('football-germany', [1, 2, 3])
P('M4  Germany football Jan-Mar = %.2f%% (n=%d); need >=28 -> %s' % (v, n['football-germany'], 'HELD' if v >= 28 else 'FAILED'))

v = q('football-brazil', [1, 2, 3])
P('M5  Brazil football Jan-Mar = %.2f%% (n=%d); need >=27 -> %s' % (v, n['football-brazil'], 'HELD' if v >= 27 else 'FAILED'))

bs = blocks('football-spain', 1)
bj = blocks('football-japan', 1)
cu = month_counts(G['football-uk'])
w12 = [(s, share(cu, window(s))) for s in range(1, 13)]
best = max(w12, key=lambda t: t[1])
pd_ = per_day(cu)
# per-day-adjusted version of the twelve windows as a side check
w12pd = [(s, sum(cu[m - 1] for m in window(s)) / sum((DIM[m - 1] - (1 if m == 1 else 0)) for m in window(s))) for s in range(1, 13)]
bestpd = max(w12pd, key=lambda t: t[1])
okS = max(bs, key=lambda b: b[1])[0] == 'Jan-Mar'
okJ = max(bj, key=lambda b: b[1])[0] == 'Apr-Jun'
okU = best[0] in (8, 9, 10)
P('M6  Spain calendar quarters: %s -> largest %s' % (fmtb(bs), max(bs, key=lambda b: b[1])[0]))
P('    Japan calendar quarters: %s -> largest %s' % (fmtb(bj), max(bj, key=lambda b: b[1])[0]))
P('    UK twelve windows: %s' % '  '.join('%s %.2f' % (wname(s), x) for s, x in w12))
P('    UK largest window starts %s (by share); by births/day starts %s' % (MN[best[0] - 1], MN[bestpd[0] - 1]))
P('    -> %s (Spain %s, Japan %s, UK %s)' % ('HELD' if (okS and okJ and okU) else 'FAILED', okS, okJ, okU))

young = [r for r in G['football-spain'] if r[1][0] >= 1980]
old = [r for r in G['football-spain'] if r[1][0] < 1960]
vy, vo = share(month_counts(young), [1, 2, 3]), share(month_counts(old), [1, 2, 3])
P('M7  Spain football Jan-Mar: born>=1980 %.2f%% (n=%d), born<1960 %.2f%% (n=%d), diff %.2f; need >=3 -> %s' % (
    vy, len(young), vo, len(old), vy - vo, 'HELD' if vy - vo >= 3 else 'FAILED'))

v = q('politicians-spain', [1, 2, 3])
P('M8  Spain politicians Jan-Mar = %.2f%% (n=%d); need within 1.5 of 24.5 (23.0..26.0) -> %s' % (
    v, n['politicians-spain'], 'HELD' if abs(v - 24.5) <= 1.5 else 'FAILED'))

gm = [r for r in G['football-germany'] if r[2] == 'M']
gf = [r for r in G['football-germany'] if r[2] == 'F']
go = [r for r in G['football-germany'] if r[2] not in ('M', 'F')]
vm, vf = share(month_counts(gm), [1, 2, 3]), share(month_counts(gf), [1, 2, 3])
P('M9  Germany football Jan-Mar: men %.2f%% (n=%d), women %.2f%% (n=%d), other/blank n=%d; need women < men -> %s' % (
    vm, len(gm), vf, len(gf), len(go), 'HELD' if vf < vm else 'FAILED'))

cb = month_counts(G['baseball-usa'])
pdb = per_day(cb)
order = sorted(range(12), key=lambda i: -pdb[i])
P('M10 US baseball births/day by month (Jan has 30 days, Feb 28.2425): %s' % '  '.join('%s %.1f' % (MN[i], pdb[i]) for i in range(12)))
P('    raw counts: %s' % '  '.join('%s %d' % (MN[i], cb[i]) for i in range(12)))
P('    top month %s, second %s (n=%d); need August top -> %s' % (MN[order[0]], MN[order[1]], n['baseball-usa'], 'HELD' if order[0] == 7 else 'FAILED'))

v = q('hockey-canada', [1, 2, 3])
P('M11 Canada hockey Jan-Mar = %.2f%% (n=%d); need >=28 -> %s' % (v, n['hockey-canada'], 'HELD' if v >= 28 else 'FAILED'))
P('    void rule (<1500 people): %s' % ', '.join('%s:%s' % (g, 'VOID' if void[g] else 'ok') for g in REG))

P()
P('## 3. controls: share in the three months after the dividing date')
CTRL = [('politicians-germany', 1), ('politicians-brazil', 1), ('politicians-canada', 1),
        ('politicians-uk', 9), ('politicians-japan', 4), ('house-usa', 8), ('politicians-spain', 1)]
for g, s in CTRL:
    recs, diag = load(g)
    c = month_counts(recs)
    v = share(c, window(s))
    ev = even_share(window(s))
    r60 = [r for r in recs if r[1][0] >= 1960]
    v60 = share(month_counts(r60), window(s))
    P('%-20s %s = %.2f%% (n=%d; even %.2f; diff %+.2f) | born>=1960: %.2f%% (n=%d) | multi-date %d jan1 %d' % (
        g, wname(s), v, len(recs), ev, v - ev, v60, len(r60), diag['multi_date'], diag['jan1']))

P()
P('## 4. German footballers by cohort: Aug-Oct and Jan-Mar')
for a, b in [(1940, 1979), (1980, 1984), (1985, 1989), (1990, 2005), (1900, 1939)]:
    rr = [r for r in G['football-germany'] if a <= r[1][0] <= b]
    c = month_counts(rr)
    P('%d-%d  n=%5d  Aug-Oct %.2f%%  Jan-Mar %.2f%%' % (a, b, len(rr), share(c, [8, 9, 10]), share(c, [1, 2, 3])))
