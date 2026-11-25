import json, statistics as st, sys
R = {'1': '/home/agent2/authors', '2': '/home/agent2/authors2'}


def ld(p):
    try:
        return json.load(open(p))
    except FileNotFoundError:
        return None


out = []


def P(*a):
    s = ' '.join(str(x) for x in a)
    out.append(s)
    print(s)


sheets = {}
for k, d in R.items():
    v = ld(d + '/results.json')['verdicts']
    c = ld(d + '/checker/verdicts.json')
    keys = list(v.keys())
    S = {'keys': keys, 'v': v, 'c': c}
    S['author_quick'] = ld(d + '/author/odds-quick.json')
    S['author_careful'] = ld(d + '/author/odds-careful.json')
    for i in (1, 2, 3):
        S['reader_f%d' % i] = ld(d + '/readers/f%d.json' % i)
        S['quick_f%d' % i] = ld(d + '/quick/f%d.json' % i)
    S['readers_median'] = {q: st.median([S['reader_f%d' % i][q] for i in (1, 2, 3)]) for q in keys}
    S['quick_median'] = {q: st.median([S['quick_f%d' % i][q] for i in (1, 2, 3)]) for q in keys}
    S['noon'] = ld(d + '/mine.json')
    sheets[k] = S

parties = ['author_quick', 'author_careful', 'readers_median', 'reader_f1', 'reader_f2', 'reader_f3',
           'quick_median', 'quick_f1', 'quick_f2', 'quick_f3', 'noon']


def pairs(party, which):
    r = []
    for k in which:
        S = sheets[k]
        if S[party] is None:
            continue
        for q in S['keys']:
            r.append((S[party][q], 1.0 if S['v'][q] else 0.0, k + q))
    return r


def brier(pp):
    return sum((p - o) ** 2 for p, o, _ in pp) / len(pp) if pp else float('nan')


P('1. BRIER SCORES (n in brackets)')
P('%-16s %14s %14s %14s' % ('party', 'sheet1', 'sheet2', 'both'))
for p in parties:
    row = []
    for w in (['1'], ['2'], ['1', '2']):
        pp = pairs(p, w)
        row.append('%.4f [%d]' % (brier(pp), len(pp)) if pp else '   -   ')
    P('%-16s %14s %14s %14s' % (p, *row))

P('')
P('2. CLOSER TO OUTCOME THAN CAREFUL READERS MEDIAN (both sheets; closer/tie/farther of n)')


def closer(a, b):
    w = t = l = 0
    n = 0
    for k in ('1', '2'):
        S = sheets[k]
        if S[a] is None or S[b] is None:
            continue
        for q in S['keys']:
            o = 1.0 if S['v'][q] else 0.0
            da = abs(S[a][q] - o)
            db = abs(S[b][q] - o)
            n += 1
            if da < db - 1e-12:
                w += 1
            elif abs(da - db) <= 1e-12:
                t += 1
            else:
                l += 1
    return w, t, l, n


for p in parties:
    if p == 'readers_median':
        continue
    P('%-16s closer %2d  tie %2d  farther %2d  of %2d' % (p, *closer(p, 'readers_median')))
P('author_quick vs quick_median: closer %d tie %d farther %d of %d' % closer('author_quick', 'quick_median'))
for k in ('1', '2'):
    pass

P('')
P('3. VERDICT AGREEMENT Noon vs checker')
tot = 0
agree = 0
for k in ('1', '2'):
    S = sheets[k]
    for q in S['keys']:
        tot += 1
        agree += (S['v'][q] == S['c'][q])
    P('sheet', k, 'keys same set:', set(S['v']) == set(S['c']), ' held:', sum(S['v'].values()), 'of', len(S['v']))
P('agree on', agree, 'of', tot)

P('')
P('4. LOWEST PROB GIVEN TO A HELD STATEMENT / HIGHEST GIVEN TO A FAILED ONE (both sheets)')
for p in parties:
    pp = pairs(p, ['1', '2'])
    held = [(x, n) for x, o, n in pp if o == 1]
    fail = [(x, n) for x, o, n in pp if o == 0]
    lo = min(held) if held else None
    hi = max(fail) if fail else None
    P('%-16s lowest-on-held %s   highest-on-failed %s' % (p, lo, hi))

open('/home/agent2/authors/referee/blind.out', 'w').write('\n'.join(out) + '\n')
