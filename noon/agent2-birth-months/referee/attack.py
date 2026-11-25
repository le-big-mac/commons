"""Referee's attacks, after reading Noon's files. Usage: python -I attack.py DATADIR > attack.out"""
import sys, math
sys.path.insert(0, '/home/agent2/birth/referee')
from reflib import *

D = sys.argv[1]
ATH = [('football-spain', 1), ('football-uk', 9), ('football-japan', 4), ('football-germany', 1), ('football-brazil', 1),
       ('hockey-canada', 1), ('baseball-usa', 8)]
PAIR = [('football-spain', 1, 'politicians-spain'), ('football-brazil', 1, 'politicians-brazil'),
        ('football-germany', 1, 'politicians-germany'), ('hockey-canada', 1, 'politicians-canada'),
        ('football-uk', 9, 'politicians-uk'), ('football-japan', 4, 'politicians-japan'), ('baseball-usa', 8, 'house-usa')]
ALL = [a for a, _ in ATH] + [p for _, _, p in PAIR]


def L(name, **kw):
    return people(os.path.join(D, name + '.csv'), **kw)


def sh(recs, start):
    return share(month_counts(recs), window(start))


def se(p, n):
    p /= 100.0
    return 100 * math.sqrt(p * (1 - p) / n) if n else float('nan')


def P(*a):
    print(*a)


BASE = {g: L(g)[0] for g in ALL}

# ---------------------------------------------------------------- A
P('## A. definition changes: dedup rule x 1 January x first-of-month')
P('cols: SpainJFM UKSON JapanAMJ GerJFM BraJFM | M7diff | PolSpJFM | GerW GerM | bbAug/d bbSep/d top | CanJFM | verdicts M1..M11')
for label, kw in [('first, jan1 out (Noon)', dict(rule='first')), ('min', dict(rule='min')), ('max', dict(rule='max')),
                  ('unique (multi-date people dropped)', dict(rule='unique')),
                  ('first, jan1 IN', dict(rule='first', drop_jan1=False)),
                  ('first, all 1st-of-month out', dict(rule='first', drop_first_of_month=True))]:
    G = {g: L(g, **kw)[0] for g in ['football-spain', 'football-uk', 'football-japan', 'football-germany', 'football-brazil',
                                    'hockey-canada', 'baseball-usa', 'politicians-spain']}
    j1 = kw.get('drop_jan1', True)
    s1 = sh(G['football-spain'], 1)
    cu = month_counts(G['football-uk'])
    ub = [share(cu, window(s)) for s in (9, 12, 3, 6)]
    cj = month_counts(G['football-japan'])
    jb = [share(cj, window(s)) for s in (4, 7, 10, 1)]
    g4 = sh(G['football-germany'], 1)
    b5 = sh(G['football-brazil'], 1)
    cs = month_counts(G['football-spain'])
    sq = [share(cs, window(s)) for s in (1, 4, 7, 10)]
    jq = [share(cj, window(s)) for s in (1, 4, 7, 10)]
    u12 = [share(cu, window(s)) for s in range(1, 13)]
    ubest = u12.index(max(u12)) + 1
    yo = sh([r for r in G['football-spain'] if r[1][0] >= 1980], 1) - sh([r for r in G['football-spain'] if r[1][0] < 1960], 1)
    p8 = sh(G['politicians-spain'], 1)
    ev = even_share([1, 2, 3], jan1_out=j1)
    gw = sh([r for r in G['football-germany'] if r[2] == 'F'], 1)
    gm = sh([r for r in G['football-germany'] if r[2] == 'M'], 1)
    cb = month_counts(G['baseball-usa'])
    pd_ = per_day(cb, jan1_out=j1)
    top = MN[pd_.index(max(pd_))]
    c11 = sh(G['hockey-canada'], 1)
    v = [s1 >= 28, ub[0] >= 27 and ub[0] == max(ub), jb[0] >= 28 and jb[0] == max(jb), g4 >= 28, b5 >= 27,
         sq[0] == max(sq) and jq[1] == max(jq) and ubest in (8, 9, 10), yo >= 3, abs(p8 - ev) <= 1.5, gw < gm, top == 'Aug', c11 >= 28]
    P('%-36s %.2f %.2f %.2f %.2f %.2f | %+.2f | %.2f | %.2f %.2f | %.2f %.2f %s | %.2f | %s' % (
        label, s1, ub[0], jb[0], g4, b5, yo, p8, gw, gm, pd_[7], pd_[8], top, c11, ''.join('H' if x else 'F' for x in v)))

# ---------------------------------------------------------------- B
P()
P('## B. the same person in several files')
ids = {g: set(r[0] for r in BASE[g]) for g in ALL}
aths = [a for a, _ in ATH]
cnt = Counter()
for a in aths:
    for p in ids[a]:
        cnt[p] += 1
multi = set(p for p, k in cnt.items() if k > 1)
P('athlete rows counted (sum of seven groups): %d; distinct people: %d; in more than one athlete file: %d' % (
    sum(len(ids[a]) for a in aths), len(cnt), len(multi)))
for i, a in enumerate(aths):
    for b in aths[i + 1:]:
        k = len(ids[a] & ids[b])
        if k >= 20:
            P('   %s & %s: %d' % (a, b, k))
for a, s, pol in PAIR:
    P('   %s & %s: %d' % (a, pol, len(ids[a] & ids[pol])))
P('share of the cut-off quarter, all people vs people in one athlete file only vs those in several:')
for a, s in ATH:
    one = [r for r in BASE[a] if r[0] not in multi]
    sev = [r for r in BASE[a] if r[0] in multi]
    P('   %-17s %s all %.2f (n=%d) | single-country %.2f (n=%d) | several %.2f (n=%d)' % (
        a, wname(s), sh(BASE[a], s), len(BASE[a]), sh(one, s), len(one), sh(sev, s) if sev else float('nan'), len(sev)))

# ---------------------------------------------------------------- C
P()
P('## C. heaping of dates (even births: a first-of-month other than 1 Jan = 11/364.24 = 3.02%; any single day 0.27%)')
for g in ALL:
    recs = BASE[g]
    n = len(recs)
    first = sum(1 for r in recs if r[1][2] == 1)
    d15 = sum(1 for r in recs if r[1][2] == 15)
    md = Counter((r[1][1], r[1][2]) for r in recs)
    top = md.most_common(4)
    P('   %-19s n=%5d 1st-of-month %.2f%%  15th %.2f%% (even 3.29)  Jul-1 %d  Dec-31 %d  top days: %s' % (
        g, n, 100.0 * first / n, 100.0 * d15 / n, md[(7, 1)], md[(12, 31)],
        ', '.join('%s-%d:%d' % (MN[m - 1], d, k) for (m, d), k in top)))
nonmid = 0
for g in ALL:
    with open(os.path.join(D, g + '.csv'), encoding='utf-8') as f:
        next(f)
        for line in f:
            parts = line.split(',')
            if len(parts) > 1 and not parts[1].endswith('T00:00:00Z'):
                nonmid += 1
P('   rows whose time of day is not T00:00:00Z, all files: %d' % nonmid)

# ---------------------------------------------------------------- D
P()
P('## D. by sex: share of the cut-off quarter')
for a, s in ATH:
    m = [r for r in BASE[a] if r[2] == 'M']
    f = [r for r in BASE[a] if r[2] == 'F']
    o = [r for r in BASE[a] if r[2] not in ('M', 'F')]
    P('   %-17s %s men %.2f (n=%d, se %.2f) | women %.2f (n=%d, se %.2f) | other/blank n=%d' % (
        a, wname(s), sh(m, s), len(m), se(sh(m, s), len(m)), sh(f, s) if f else float('nan'), len(f),
        se(sh(f, s), len(f)) if f else float('nan'), len(o)))

# ---------------------------------------------------------------- E
P()
P('## E. is the politicians control fair? same years of birth')
BANDS = [(1900, 1919), (1920, 1939), (1940, 1959), (1960, 1979), (1980, 2005)]


def band(recs, a, b):
    return [r for r in recs if a <= r[1][0] <= b]


def chi_even(recs):
    c = month_counts(recs)
    n = sum(c)
    days = [DIM[i] - (1 if i == 0 else 0) for i in range(12)]
    T = sum(days)
    return sum((c[i] - n * days[i] / T) ** 2 / (n * days[i] / T) for i in range(12))


for a, s, pol in PAIR:
    A, C = BASE[a], BASE[pol]
    ya = sorted(r[1][0] for r in A)
    yc = sorted(r[1][0] for r in C)
    ev = even_share(window(s))
    pc = sh(C, s)
    P('%s vs %s (%s; even %.2f)' % (a, pol, wname(s), ev))
    P('   median year of birth: athletes %d, control %d; control born>=1980: %d of %d' % (
        ya[len(ya) // 2], yc[len(yc) // 2], sum(1 for y in yc if y >= 1980), len(yc)))
    P('   all years: athletes %.2f (n=%d) control %.2f (n=%d, se %.2f; %+.1f se from even; chi2 of 12 months vs even, 11 df = %.1f)' % (
        sh(A, s), len(A), pc, len(C), se(pc, len(C)), (pc - ev) / se(pc, len(C)), chi_even(C)))
    for lo, hi in [(1940, 1979), (1960, 2005), (1970, 2005), (1980, 2005)]:
        Ab, Cb = band(A, lo, hi), band(C, lo, hi)
        if not Cb:
            continue
        pa, pcb = sh(Ab, s), sh(Cb, s)
        d = pa - pcb
        sd = math.sqrt(se(pa, len(Ab)) ** 2 + se(pcb, len(Cb)) ** 2)
        P('   born %d-%d: athletes %.2f (n=%d) control %.2f (n=%d, se %.2f) difference %+.2f (se %.2f, %.1f se)' % (
            lo, hi, pa, len(Ab), pcb, len(Cb), se(pcb, len(Cb)), d, sd, d / sd))
    # control standardised to the athletes' distribution over five bands of birth year
    w, est, var = [], 0.0, 0.0
    ok = True
    for lo, hi in BANDS:
        Ab, Cb = band(A, lo, hi), band(C, lo, hi)
        wt = len(Ab) / len(A)
        if not Cb:
            ok = False
            continue
        pcb = sh(Cb, s)
        est += wt * pcb
        var += (wt * se(pcb, len(Cb))) ** 2
        w.append('%d-%d w=%.2f ctrl %.1f (n=%d)' % (lo, hi, wt, pcb, len(Cb)))
    P('   control reweighted to the athletes\' years of birth: %.2f (se %.2f)%s  [%s]' % (
        est, math.sqrt(var), '' if ok else ' (a band had no controls)', '; '.join(w)))

# ---------------------------------------------------------------- F
P()
P('## F. Germany')
GER = BASE['football-germany']


def row(recs, extra=''):
    c = month_counts(recs)
    n = sum(c)
    if n == 0:
        return 'n=0'
    w = [share(c, window(s)) for s in range(1, 13)]
    b = w.index(max(w)) + 1
    pdv = per_day(c)
    mean = sum(pdv) / 12
    return 'n=%5d Aug-Oct %5.1f Jan-Mar %5.1f Jul-Sep %5.1f | per-day index Jun %3.0f Jul %3.0f Aug %3.0f Dec %3.0f Jan %3.0f | largest window from %s %s' % (
        n, share(c, [8, 9, 10]), share(c, [1, 2, 3]), share(c, [7, 8, 9]), 100 * pdv[5] / mean, 100 * pdv[6] / mean,
        100 * pdv[7] / mean, 100 * pdv[11] / mean, 100 * pdv[0] / mean, MN[b - 1], extra)


P('F1. five-year bands of birth, all / men / women')
for lo in range(1900, 2005, 5):
    hi = lo + 4 if lo < 2000 else 2005
    rr = band(GER, lo, hi)
    P('   %d-%d all   %s' % (lo, hi, row(rr)))
    P('             men   %s' % row([r for r in rr if r[2] == 'M']))
    wm = [r for r in rr if r[2] == 'F']
    if len(wm) >= 100:
        P('             women %s' % row(wm))
P('F2. Noon\'s four bands, men and women apart')
for lo, hi in [(1900, 1939), (1940, 1979), (1980, 1984), (1985, 1989), (1990, 2005)]:
    rr = band(GER, lo, hi)
    P('   %d-%d men   %s' % (lo, hi, row([r for r in rr if r[2] == 'M'])))
    P('   %d-%d women %s' % (lo, hi, row([r for r in rr if r[2] == 'F'])))
P('F3. other placements of the cuts (old band / new band): Aug-Oct and Jan-Mar, all and men only')
for (a, b), (c_, d) in [((1940, 1979), (1990, 2005)), ((1940, 1969), (1995, 2005)), ((1950, 1974), (1985, 2005)),
                        ((1960, 1979), (1980, 2005)), ((1900, 1939), (1990, 2005)), ((1940, 1984), (1985, 2005)),
                        ((1970, 1979), (1990, 1999))]:
    o, nw = band(GER, a, b), band(GER, c_, d)
    om, nm = [r for r in o if r[2] == 'M'], [r for r in nw if r[2] == 'M']
    P('   old %d-%d: A-O %.1f J-M %.1f (men %.1f / %.1f, n=%d) | new %d-%d: A-O %.1f J-M %.1f (men %.1f / %.1f, n=%d)' % (
        a, b, share(month_counts(o), [8, 9, 10]), share(month_counts(o), [1, 2, 3]),
        share(month_counts(om), [8, 9, 10]), share(month_counts(om), [1, 2, 3]), len(om),
        c_, d, share(month_counts(nw), [8, 9, 10]), share(month_counts(nw), [1, 2, 3]),
        share(month_counts(nm), [8, 9, 10]), share(month_counts(nm), [1, 2, 3]), len(nm)))
P('F4. the same split where nothing is said to have changed (Aug-Oct / Jan-Mar / own cut-off quarter)')
for g, s in [('football-spain', 1), ('football-brazil', 1), ('hockey-canada', 1), ('football-uk', 9), ('football-japan', 4),
             ('baseball-usa', 8), ('politicians-germany', 1), ('politicians-spain', 1)]:
    out = []
    for lo, hi in [(1900, 1939), (1940, 1979), (1980, 1984), (1985, 1989), (1990, 2005)]:
        rr = band(BASE[g], lo, hi)
        if len(rr) < 150:
            out.append('%d-%d n=%d (too few)' % (lo, hi, len(rr)))
            continue
        c = month_counts(rr)
        w = [share(c, window(x)) for x in range(1, 13)]
        out.append('%d-%d n=%d: %.1f / %.1f / %.1f, largest from %s' % (lo, hi, len(rr), share(c, [8, 9, 10]), share(c, [1, 2, 3]),
                                                                       share(c, window(s)), MN[w.index(max(w))]))
    P('   %-19s %s' % (g, ' | '.join(out)))
P('F5. Germany 1940-1979, births per day by month (mean=100), footballers then politicians of the same years')
for g in ('football-germany', 'politicians-germany'):
    for lo, hi in [(1940, 1979), (1990, 2005)]:
        rr = band(BASE[g], lo, hi)
        if len(rr) < 100:
            P('   %-19s %d-%d n=%d too few' % (g, lo, hi, len(rr)))
            continue
        pdv = per_day(month_counts(rr))
        mean = sum(pdv) / 12
        P('   %-19s %d-%d n=%5d: %s' % (g, lo, hi, len(rr), ' '.join('%3.0f' % (100 * x / mean) for x in pdv)))

# ---------------------------------------------------------------- H
P()
P('## H. the fortnight before the dividing date against the fortnight after (counts; even births would give about 1:1)')
P('   REFEREE\'S OWN ERROR: the "2 Jan" rows below compare 20 Dec-1 Jan with 2-14 Jan, but 1 January is dropped, so "before" has')
P('   12 days against 13 and the ratios are about 8% too high. Use attack2.out section 1 (18-31 Dec against 2-15 Jan) instead.')


def doy(m, d):
    cum = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    return cum[m - 1] + d          # 29 Feb counted as day 60 = 1 Mar; irrelevant for the dates used


def fort(recs, m, d, k=14, skip_jan1=False):
    """count births in the k days before (m, d) and the k days from (m, d) on; (m,d) is the first day of the new year group"""
    c0 = doy(m, d)
    before = after = 0
    for r in recs:
        if r[1][1] == 2 and r[1][2] == 29:
            continue
        x = doy(r[1][1], r[1][2])
        delta = (x - c0) % 365
        if delta < k:
            after += 1
        elif delta >= 365 - k:
            before += 1
    return before, after


def fline(name, recs, m, d, k=14):
    b, a = fort(recs, m, d, k)
    z = (a - b) / math.sqrt(a + b) if a + b else float('nan')
    return '%-44s before %4d after %4d ratio %.2f (%.1f se from 1:1)' % (name, b, a, a / b if b else float('nan'), z)


P('   ' + fline('Spain football, 2 Jan (1 Jan is dropped)', BASE['football-spain'], 1, 2, 13))
P('   ' + fline('Spain politicians, 2 Jan', BASE['politicians-spain'], 1, 2, 13))
P('   ' + fline('Brazil football, 2 Jan', BASE['football-brazil'], 1, 2, 13))
P('   ' + fline('Brazil politicians, 2 Jan', BASE['politicians-brazil'], 1, 2, 13))
P('   ' + fline('Canada hockey, 2 Jan', BASE['hockey-canada'], 1, 2, 13))
P('   ' + fline('Canada politicians, 2 Jan', BASE['politicians-canada'], 1, 2, 13))
P('   ' + fline('UK football, 1 Sep', BASE['football-uk'], 9, 1))
P('   ' + fline('UK politicians, 1 Sep', BASE['politicians-uk'], 9, 1))
P('   ' + fline('Japan football, 1 Apr', BASE['football-japan'], 4, 1))
P('   ' + fline('Japan football, 2 Apr (school law)', BASE['football-japan'], 4, 2))
P('   ' + fline('Japan politicians, 2 Apr', BASE['politicians-japan'], 4, 2))
P('   ' + fline('US baseball, 1 Aug', BASE['baseball-usa'], 8, 1))
P('   ' + fline('US baseball born 1900-1929, 1 Aug', band(BASE['baseball-usa'], 1900, 1929), 8, 1))
P('   ' + fline('US baseball born 1950-2005, 1 Aug', band(BASE['baseball-usa'], 1950, 2005), 8, 1))
P('   ' + fline('US House, 1 Aug', BASE['house-usa'], 8, 1))
P('   ' + fline('Germany football 1940-79, 1 Aug', band(GER, 1940, 1979), 8, 1))
P('   ' + fline('Germany football 1940-79, 1 Jul (school)', band(GER, 1940, 1979), 7, 1))
P('   ' + fline('Germany football 1940-79, 2 Jan', band(GER, 1940, 1979), 1, 2, 13))
P('   ' + fline('Germany football 1990-2005, 1 Aug', band(GER, 1990, 2005), 8, 1))
P('   ' + fline('Germany football 1990-2005, 2 Jan', band(GER, 1990, 2005), 1, 2, 13))
P('   ' + fline('Germany football 1990-2005 men, 2 Jan', [r for r in band(GER, 1990, 2005) if r[2] == 'M'], 1, 2, 13))
P('   ' + fline('Germany football 1990-2005 women, 2 Jan', [r for r in band(GER, 1990, 2005) if r[2] == 'F'], 1, 2, 13))
P('   ' + fline('Germany politicians 1940-79, 1 Aug', band(BASE['politicians-germany'], 1940, 1979), 8, 1))
P('   ' + fline('Germany politicians, 2 Jan', BASE['politicians-germany'], 1, 2, 13))
jp = Counter((r[1][1], r[1][2]) for r in BASE['football-japan'])
P('   Japan football by day: ' + ' '.join('%s-%d:%d' % (MN[m - 1], d, jp[(m, d)]) for m, d in
                                            [(3, 28), (3, 29), (3, 30), (3, 31), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6)]))
uk = Counter((r[1][1], r[1][2]) for r in BASE['football-uk'])
P('   UK football by day:    ' + ' '.join('%s-%d:%d' % (MN[m - 1], d, uk[(m, d)]) for m, d in
                                            [(8, 28), (8, 29), (8, 30), (8, 31), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5)]))
bb = Counter((r[1][1], r[1][2]) for r in BASE['baseball-usa'])
P('   US baseball by day:    ' + ' '.join('%s-%d:%d' % (MN[m - 1], d, bb[(m, d)]) for m, d in
                                            [(7, 28), (7, 29), (7, 30), (7, 31), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5)]))
