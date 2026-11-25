"""after3.py: what the referee's report asked for, and what the third sheet left to look at. Nothing here was sealed.
    /usr/bin/python3 -I after3.py books-story books-new books-expand  ->  after3.out (printed), after3.json
P. the twenty-two texts on four footings        Q. by author        R. the stories with shortened forms written out
S. why the Bible saves most                     T. the sign for "in" after a dash     V. long words"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study, story
AUTHOR = {'hoover': 'Hoover', 'doctorow': 'Doctorow'}
def row(r):
    u = r['ueb']; sv = u['U'] - u['C']
    return dict(year=r['year'], title=r['title'], era=r['era'], folder=r['folder'], S=100 * sv / u['U'], L=100 * sv / (u['letters'] + u['words']), letters=100 * sv / u['letters'], word=sv / u['words'], lw=u['letters'] / u['words'], rate=1000 * story.short_forms(u['vocab']) / u['words'])
if __name__ == '__main__':
    st = study.load(sys.argv[1]); new = study.load(sys.argv[2]); ex = study.load(sys.argv[3]); out = {}
    rows = sorted([row(r) for r in st if r['era'] != 0] + [row(r) for r in new], key=lambda x: x['year'])
    print('P. The twenty-two texts (stories alone): share of all cells; share of letters and one space a word; cells saved in 100 letters; cells saved a word; letters a word; shortened forms in 1,000 words')
    for x in rows: print('   %d  %-32s %s  %.2f  %.2f  %.2f  %.3f  %.2f  %5.1f' % (x['year'], x['title'], 'added' if x['era'] > 3 else '     ', x['S'], x['L'], x['letters'], x['word'], x['lw'], x['rate']))
    groups = [('the eight texts before 1895', [x for x in rows if x['year'] < 1895]), ('the six of 1900 to 1926', [x for x in rows if 1895 <= x['year'] <= 1930]), ('the eight after 1970', [x for x in rows if x['year'] > 1970])]
    out['P'] = dict(rows=rows, ranges={})
    for key, name in (('S', 'share of all cells'), ('L', 'share of letters and spaces'), ('letters', 'cells saved in 100 letters'), ('word', 'cells saved a word')):
        rng = {g: (min(x[key] for x in xs), max(x[key] for x in xs), sum(x[key] for x in xs) / len(xs)) for g, xs in groups}; out['P']['ranges'][key] = rng
        a, c = rng['the eight texts before 1895'], rng['the eight after 1970']
        print('   %-28s before 1895: %.3f to %.3f (mean %.3f); 1900 to 1926: %.3f to %.3f; after 1970: %.3f to %.3f (mean %.3f); the lowest old text is %s the highest recent one' % (name, a[0], a[1], a[2], rng['the six of 1900 to 1926'][0], rng['the six of 1900 to 1926'][1], c[0], c[1], c[2], 'above' if a[0] > c[1] else 'BELOW'))
    print('\nQ. By author: the eighteen novels are fourteen authors. The mean share of all cells for each author of the first and last six')
    auth = {}
    for x in rows:
        if x['era'] in (1, 3): auth.setdefault((x['era'], AUTHOR.get(x['folder'].split('-')[0], x['title'])), []).append(x['S'])
    am = sorted((sum(v) / len(v), k) for k, v in auth.items())
    for v, (e, a) in am: print('   %.2f  %s (%s)' % (v, a, 'first six' if e == 1 else 'last six'))
    print('   six authors against two: the two lowest of the eight are the two recent authors, which chance gives once in %d' % (8 * 7 // 2)); out['Q'] = [(v, e, a) for v, (e, a) in am]
    print('\nR. With the shortened forms of speech written out (do not for don\'t, and so on; crude: \'d is always would)')
    m = lambda rs, e: sum(study.S(r) for r in rs if r['era'] == e) / 6
    a = [m(st, e) for e in (1, 2, 3)]; b = [m(ex, e) for e in (1, 2, 3)]
    print('   as printed: %.2f, %.2f, %.2f (first less last %.2f);  written out: %.2f, %.2f, %.2f (first less last %.2f): %.0f%% of the gap is the shortened forms' % (100 * a[0], 100 * a[1], 100 * a[2], 100 * (a[0] - a[2]), 100 * b[0], 100 * b[1], 100 * b[2], 100 * (b[0] - b[2]), 100 * (1 - (b[0] - b[2]) / (a[0] - a[2]))))
    lo1 = min((study.S(r), r['title']) for r in ex if r['era'] == 1); above = sorted((study.S(r), r['title']) for r in ex if r['era'] == 3 and study.S(r) > lo1[0])
    print('   written out, the lowest of the first six is %s at %.2f%%, and %d of the last six are above it: %s' % (lo1[1], 100 * lo1[0], len(above), ', '.join('%s %.2f' % (t, 100 * s) for s, t in above)))
    out['R'] = dict(printed=a, written=b, lowest_first=lo1, above=above)
    print('\nS. Why the Bible saves most: cells saved in 100,000 words, the Bible less the first six novels')
    P0 = study.pool([r for r in st if r['era'] == 0]); P1 = study.pool([r for r in st if r['era'] == 1]); d = {}
    def w(p, keys): return 1e5 * sum(p['by'].get(k, [0, 0])[1] for k in keys) / p['words']
    for name, keys in (('the', ['the|w', 'the|p']), ('and', ['and|w', 'and|p']), ('shall', ['shall|w']), ('th', ['th|p'])): d[name] = w(P0, keys) - w(P1, keys)
    rel = 'thyself rejoice rejoicing conceive conceiving deceive deceiving declare declaring perceive perceiving receive receiving'.split()
    relk = lambda p: [k for k in p['by'] if any(k.split('|')[0].startswith(s) for s in rel)]; d['the religious shortforms'] = w(P0, relk(P0)) - w(P1, relk(P1))
    d['lord, children, father'] = w(P0, ['lord|w', 'lord|p', 'children|w', 'father|w', 'father|p']) - w(P1, ['lord|w', 'lord|p', 'children|w', 'father|w', 'father|p'])
    tot = 1e5 * ((P0['U'] - P0['C']) / P0['words'] - (P1['U'] - P1['C']) / P1['words'])
    print('   in all %+.0f; of that: %s' % (tot, '; '.join('%s %+.0f' % kv for kv in d.items()))); out['S'] = dict(total=tot, parts=d)
    print('\nT. The translator uses the sign for "in" after a dash, where the rulebook spells it (the referee\'s finding). How often can that arise?')
    for e in (1, 2, 3):
        rs = [r for r in st if r['era'] == e]; W = sum(r['ueb']['words'] for r in rs); print('   era %d: the word "in" %.0f times in 100,000 words' % (e, 1e5 * sum(r['ueb']['vocab'].get('in', 0) for r in rs) / W), end='')
        print('')
    print('   (how many of those follow a dash is counted in dash.out, from the texts)')
    print('\nV. Long words: the share of a text\'s letters that stand in words of eight letters or more (the referee\'s reason for the Zen books)')
    def longshare(rs):
        tot = lng = 0
        for r in rs:
            for wd, k in r['ueb']['vocab'].items():
                n = sum(ch.isalpha() for ch in wd); tot += n * k; lng += n * k * (n >= 8)
        return 100 * lng / tot
    out['V'] = dict(sets=[longshare([r for r in st if r['era'] == e]) for e in (1, 2, 3)], each={r['folder']: longshare([r]) for r in st + new if r['era'] != 0})
    six = [out['V']['each'][r['folder']] for r in st if r['era'] == 1]
    print('   the first six novels %.1f%% (from %.1f%% to %.1f%%); the middle six %.1f%%; the last six %.1f%%' % (out['V']['sets'][0], min(six), max(six), out['V']['sets'][1], out['V']['sets'][2]))
    for r in new: print('   %-32s %.1f%%' % (r['title'], out['V']['each'][r['folder']]))
    json.dump(out, open(os.path.join(HERE, 'after3.json'), 'w'), indent=1)
