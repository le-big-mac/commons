"""Second round of attacks. Usage: python -I attack2.py DATADIR FORECASTDIR EXPECTATIONS > attack2.out"""
import sys, math, json, re
sys.path.insert(0, '/home/agent2/birth/referee')
from reflib import *

D, FD, EXP = sys.argv[1], sys.argv[2], sys.argv[3]
NAMES = ['football-spain', 'football-uk', 'football-japan', 'football-germany', 'football-brazil', 'hockey-canada', 'baseball-usa',
         'politicians-spain', 'politicians-uk', 'politicians-japan', 'politicians-germany', 'politicians-brazil',
         'politicians-canada', 'house-usa']
B, DG = {}, {}
for g in NAMES:
    B[g], DG[g] = people(os.path.join(D, g + '.csv'))


def P(*a):
    print(*a)


def band(recs, a, b):
    return [r for r in recs if a <= r[1][0] <= b]


def se(p, n):
    p /= 100.0
    return 100 * math.sqrt(p * (1 - p) / n) if n else float('nan')


def prof(recs):
    pdv = per_day(month_counts(recs))
    mean = sum(pdv) / 12
    return [100 * x / mean for x in pdv]


CUM = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]


def doy(m, d):
    return CUM[m - 1] + d


def fort(recs, m, d, k=14):
    """k days before the first day (m, d) of a year group against the k days from it. For 1 January: 18-31 Dec against 2-15 Jan."""
    if (m, d) == (1, 1):
        lo, hi = doy(12, 31) - k + 1, doy(12, 31)
        b = sum(1 for r in recs if lo <= doy(r[1][1], r[1][2]) <= hi and not (r[1][1] == 2 and r[1][2] == 29))
        a = sum(1 for r in recs if r[1][1] == 1 and 2 <= r[1][2] <= k + 1)
        return b, a
    c0 = doy(m, d)
    b = a = 0
    for r in recs:
        if r[1][1] == 2 and r[1][2] == 29:
            continue
        delta = (doy(r[1][1], r[1][2]) - c0) % 365
        if delta < k:
            a += 1
        elif delta >= 365 - k:
            b += 1
    return b, a


def fl(name, recs, m, d):
    b, a = fort(recs, m, d)
    z = (a - b) / math.sqrt(a + b) if a + b else float('nan')
    return '   %-46s before %4d after %4d ratio %.2f (%+.1f se from 1:1)' % (name, b, a, a / b if b else float('nan'), z)


P('## 1. fortnight before / after, corrected for 1 January (18-31 Dec against 2-15 Jan)')
for name, g, lo, hi, sex in [('Spain football', 'football-spain', 1900, 2005, None), ('Spain politicians', 'politicians-spain', 1900, 2005, None),
                             ('Brazil football', 'football-brazil', 1900, 2005, None), ('Brazil politicians', 'politicians-brazil', 1900, 2005, None),
                             ('Canada hockey', 'hockey-canada', 1900, 2005, None), ('Canada politicians', 'politicians-canada', 1900, 2005, None),
                             ('Germany football 1940-79', 'football-germany', 1940, 1979, None),
                             ('Germany football 1990-2005', 'football-germany', 1990, 2005, None),
                             ('Germany football 1990-2005 men', 'football-germany', 1990, 2005, 'M'),
                             ('Germany football 1990-2005 women', 'football-germany', 1990, 2005, 'F'),
                             ('Germany politicians', 'politicians-germany', 1900, 2005, None),
                             ('UK football all', 'football-uk', 1900, 2005, None), ('UK football 1900-1979', 'football-uk', 1900, 1979, None),
                             ('UK football 1980-1989', 'football-uk', 1980, 1989, None), ('UK football 1990-2005', 'football-uk', 1990, 2005, None),
                             ('UK football 1990-2005 men', 'football-uk', 1990, 2005, 'M'),
                             ('UK politicians', 'politicians-uk', 1900, 2005, None),
                             ('Japan football', 'football-japan', 1900, 2005, None), ('US baseball', 'baseball-usa', 1900, 2005, None)]:
    rr = band(B[g], lo, hi)
    if sex:
        rr = [r for r in rr if r[2] == sex]
    P(fl(name + ', at 1 Jan', rr, 1, 1))
pooled = B['politicians-spain'] + B['politicians-germany'] + B['politicians-canada'] + B['politicians-brazil']
P(fl('four Jan-country politicians pooled, at 1 Jan', pooled, 1, 1))
P('   UK football at 1 Sep by cohort:')
for lo, hi in [(1900, 1939), (1940, 1979), (1980, 1989), (1990, 2005)]:
    P(fl('UK football %d-%d, at 1 Sep' % (lo, hi), band(B['football-uk'], lo, hi), 9, 1))
P('   UK football profile (mean=100) by cohort:')
for lo, hi in [(1900, 1939), (1940, 1979), (1980, 1989), (1990, 2005)]:
    rr = band(B['football-uk'], lo, hi)
    P('     %d-%d n=%5d: %s' % (lo, hi, len(rr), ' '.join('%3.0f' % x for x in prof(rr))))
rr = B['politicians-uk']
P('     politicians n=%5d: %s' % (len(rr), ' '.join('%3.0f' % x for x in prof(rr))))

P()
P('## 2. Spain and Brazil by cohort: births per day by month (mean=100) and the step at 1 August')
for g in ('football-spain', 'football-brazil', 'hockey-canada'):
    for lo, hi in [(1900, 1939), (1940, 1959), (1960, 1979), (1980, 2005)]:
        rr = band(B[g], lo, hi)
        c = month_counts(rr)
        P('   %-16s %d-%d n=%5d: %s | Aug-Oct %.1f Jan-Mar %.1f' % (g, lo, hi, len(rr), ' '.join('%3.0f' % x for x in prof(rr)),
                                                                   share(c, [8, 9, 10]), share(c, [1, 2, 3])))
    P(fl(g + ' 1940-79, at 1 Aug', band(B[g], 1940, 1979), 8, 1))
    P(fl(g + ' 1940-79, at 1 Jan', band(B[g], 1940, 1979), 1, 1))
    P(fl(g + ' 1900-39, at 1 Jan', band(B[g], 1900, 1939), 1, 1))

P()
P('## 3. baseball by cohort and against the House')
bb = B['baseball-usa']
for lo, hi in [(1900, 1929), (1930, 1949), (1950, 1969), (1970, 1989), (1990, 2005), (1960, 1979), (1900, 2005)]:
    rr = band(bb, lo, hi)
    c = month_counts(rr)
    pr = prof(rr)
    order = sorted(range(12), key=lambda i: -pr[i])
    p = share(c, [8, 9, 10])
    P('   baseball %d-%d n=%5d: %s | Aug-Oct %.1f (se %.1f) | top %s %.0f, then %s %.0f, %s %.0f' % (
        lo, hi, len(rr), ' '.join('%3.0f' % x for x in pr), p, se(p, len(rr)), MN[order[0]], pr[order[0]], MN[order[1]], pr[order[1]],
        MN[order[2]], pr[order[2]]))
    P(fl('baseball %d-%d at 1 Aug' % (lo, hi), rr, 8, 1))
hs = B['house-usa']
hall, _ = people(os.path.join(D, 'house-usa.csv'), y0=1700, y1=2005)
for name, rr in [('House 1900-2005', hs), ('House 1700-2005', hall), ('House 1700-1899', band(hall, 1700, 1899)), ('House 1900-1939', band(hs, 1900, 1939)),
                 ('House 1940-2005', band(hs, 1940, 2005))]:
    c = month_counts(rr)
    n = sum(c)
    pr = prof(rr)
    P('   %-16s n=%5d: %s | Aug-Oct %.1f (se %.1f); one month\'s index has se about %.0f' % (
        name, n, ' '.join('%3.0f' % x for x in pr), share(c, [8, 9, 10]), se(share(c, [8, 9, 10]), n), 100 * math.sqrt(12.0 / n)))
cb, ch = month_counts(bb), month_counts(hs)
pb, ph = prof(bb), prof(hs)
P('   baseball / House, per-day index ratio by month (se from both counts):')
P('      ' + '  '.join('%s %.2f(%.2f)' % (MN[i], pb[i] / ph[i], (pb[i] / ph[i]) * math.sqrt(1.0 / cb[i] + 1.0 / ch[i])) for i in range(12)))
cha = month_counts(hall)
pha = prof(hall)
P('   baseball / House born 1700-2005:')
P('      ' + '  '.join('%s %.2f(%.2f)' % (MN[i], pb[i] / pha[i], (pb[i] / pha[i]) * math.sqrt(1.0 / cb[i] + 1.0 / cha[i])) for i in range(12)))
b0, h0 = band(bb, 1900, 1939), band(hs, 1900, 1939)
P('   born 1900-1939: baseball Aug-Oct %.2f (n=%d) House %.2f (n=%d)' % (share(month_counts(b0), [8, 9, 10]), len(b0), share(month_counts(h0), [8, 9, 10]), len(h0)))

P()
P('## 4. Japan, politicians: Jan-Mar and Apr-Jun by cohort; share of 1 Jan among those born in the years')
jp = B['politicians-japan']
for lo, hi in [(1900, 1919), (1920, 1939), (1940, 1959), (1960, 1979), (1980, 2005)]:
    rr = band(jp, lo, hi)
    c = month_counts(rr)
    P('   %d-%d n=%4d Jan-Mar %.1f Apr-Jun %.1f | %s' % (lo, hi, len(rr), share(c, [1, 2, 3]), share(c, [4, 5, 6]), ' '.join('%3.0f' % x for x in prof(rr))))
P('   1 January as a share of those born 1900-2005, every file:')
for g in NAMES:
    d = DG[g]
    P('      %-19s %d of %d = %.2f%%' % (g, d['jan1'], d['counted'] + d['jan1'], 100.0 * d['jan1'] / (d['counted'] + d['jan1'])))

P()
P('## 5. Germany: men and women at the two dates, by cohort')
ger = B['football-germany']
for lo, hi in [(1940, 1979), (1980, 1984), (1985, 1989), (1990, 1994), (1995, 2005)]:
    for sx in ('M', 'F'):
        rr = [r for r in band(ger, lo, hi) if r[2] == sx]
        if len(rr) < 300:
            continue
        c = month_counts(rr)
        ao, jm = share(c, [8, 9, 10]), share(c, [1, 2, 3])
        b1, a1 = fort(rr, 8, 1)
        b2, a2 = fort(rr, 1, 1)
        P('   %d-%d %s n=%5d Aug-Oct %.1f (se %.1f) Jan-Mar %.1f (se %.1f) | step at 1 Aug %d:%d (%.2f) | step at 1 Jan %d:%d (%.2f)' % (
            lo, hi, sx, len(rr), ao, se(ao, len(rr)), jm, se(jm, len(rr)), b1, a1, a1 / b1 if b1 else float('nan'), b2, a2, a2 / b2 if b2 else float('nan')))
P('   share of women by cohort: ' + '; '.join('%d-%d %.0f%%' % (lo, hi, 100.0 * sum(1 for r in band(ger, lo, hi) if r[2] == 'F') / max(1, len(band(ger, lo, hi))))
                                              for lo, hi in [(1940, 1979), (1980, 1984), (1985, 1989), (1990, 2005)]))
pg = B['politicians-germany']
for lo, hi in [(1900, 1939), (1940, 1979), (1980, 2005)]:
    rr = band(pg, lo, hi)
    c = month_counts(rr)
    P('   politicians %d-%d n=%5d Aug-Oct %.1f Jan-Mar %.1f (se %.1f)' % (lo, hi, len(rr), share(c, [8, 9, 10]), share(c, [1, 2, 3]), se(share(c, [1, 2, 3]), len(rr))))

P()
P('## 6. Brier arithmetic')
text = open(EXP, encoding='utf-8').read()
mine = {m.group(1): float(m.group(2)) for m in re.finditer(r'^(M\d+)\..*?odds (0\.\d+)\s*$', text, re.M | re.S)}
ids = ['M%d' % i for i in range(1, 12)]
F = [json.load(open(os.path.join(FD, 'f%d.json' % k))) for k in (1, 2, 3)]
y = {i: 1.0 for i in ids}
y['M4'] = 0.0
y['M10'] = 0.0
me = [mine[i] for i in ids]
med = [sorted(float(f[i]) for f in F)[1] for i in ids]
mean3 = [sum(float(f[i]) for f in F) / 3 for i in ids]
yy = [y[i] for i in ids]


def brier(p, yv):
    return sum((a - b) ** 2 for a, b in zip(p, yv)) / len(p)


P('   my odds parsed: ' + ' '.join('%s %.2f' % (i, mine[i]) for i in ids))
P('   median:         ' + ' '.join('%s %.2f' % (i, m) for i, m in zip(ids, med)))
P('   Brier: Noon %.4f; median of three %.4f; mean of three %.4f; each %s; constant 9/11 %.4f; mean of the three forecasters\' own scores %.4f' % (
    brier(me, yy), brier(med, yy), brier(mean3, yy), ', '.join('%.4f' % brier([float(f[i]) for i in ids], yy) for f in F),
    brier([9 / 11.0] * 11, yy), sum(brier([float(f[i]) for i in ids], yy) for f in F) / 3))
wins = sum(1 for a, b, t in zip(me, med, yy) if (a - t) ** 2 < (b - t) ** 2)
P('   expectations on which Noon was closer than the median: %d of 11' % wins)
for drop in ids:
    k = [j for j, i in enumerate(ids) if i != drop]
    a = brier([me[j] for j in k], [yy[j] for j in k])
    b = brier([med[j] for j in k], [yy[j] for j in k])
    P('   without %-3s Noon %.4f median %.4f  diff %+.4f' % (drop, a, b, a - b))
y2 = list(yy)
y2[9] = 1.0
P('   if August had come out on top (M10 held): Noon %.4f median %.4f' % (brier(me, y2), brier(med, y2)))
y3 = list(yy)
y3[6] = 0.0
P('   if M7 had failed (it held by 0.44 points, 0.4 se): Noon %.4f median %.4f' % (brier(me, y3), brier(med, y3)))
