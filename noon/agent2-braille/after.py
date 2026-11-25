"""after.py: what was looked at after the sealed lines were scored. Nothing here was predicted.
    /usr/bin/python3 -I after.py books   ->  after.out (printed), after.json
A. the decline taken apart: cells saved and cells uncontracted per 100,000 words, by era
B. the same share on other footings: letters only; words only (no stops, no capitals)
C. the books one by one, and era 2 split in two; era 3 by author
D. which signs lost and which gained between era 1 and era 3, and by kind of sign
E. the letter-words with names set aside
F. what the nine signs dropped from the American code cost, taken apart
G. the Bible: what makes it the highest
H. each sign's cells saved per 100,000 words in the four bodies of text (the page's table)"""
import collections, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study
from study import SIGNS, pool, per100k, S

def sign_saving(p, sign, kind):
    """cells saved per 100,000 words by one sign of UEB, in every unit that is the sign (for a shortform: that begins with its word)"""
    tot = 0
    for k, v in p['by'].items():
        span, wp = k.split('|')
        if kind in study.WORD_KINDS:
            if span == sign and wp == 'w': tot += v[1]
        elif kind == 'shortform':
            if span.startswith(sign): tot += v[1]
        elif kind in ('strong contraction', 'initial-letter'):
            if span == sign: tot += v[1]
        else:
            if span == sign and (wp == 'p' or kind != 'lower groupsign' or sign not in ('be', 'in')): tot += v[1]
    return 1e5 * tot / p['words']

if __name__ == '__main__':
    recs = study.load(sys.argv[1]); eras = {e: [r for r in recs if r['era'] == e] for e in (1, 2, 3)}; kjv = [r for r in recs if r['era'] == 0][0]
    P = {e: pool(eras[e]) for e in eras}; P[0] = pool([kjv]); PE = {e: pool(eras[e], 'ebae') for e in eras}; out = {}
    name = {0: 'the Bible of 1611', 1: 'era 1 (1813-1871)', 2: 'era 2 (1900-1926)', 3: 'era 3 (1991-2009)'}

    print('A. Per 100,000 words, pooled: cells uncontracted, cells saved, share saved; letters per word')
    out['A'] = {}
    for e in (0, 1, 2, 3):
        p = P[e]; W = p['words']; L = sum(r['ueb']['letters'] for r in (eras[e] if e else [kjv]))
        out['A'][e] = dict(U=1e5 * p['U'] / W, saved=1e5 * (p['U'] - p['C']) / W, share=(p['U'] - p['C']) / p['U'], letters=L / W)
        print('   %-20s %7.0f uncontracted   %7.0f saved   %.2f%%   %.2f letters a word' % (name[e], out['A'][e]['U'], out['A'][e]['saved'], 100 * out['A'][e]['share'], L / W))
    a1, a3 = out['A'][1], out['A'][3]
    print('   era 1 to era 3: the saving falls by %.0f cells per 100,000 words (%.1f%%) and the uncontracted text by %.0f (%.1f%%)' % (a1['saved'] - a3['saved'], 100 * (1 - a3['saved'] / a1['saved']), a1['U'] - a3['U'], 100 * (1 - a3['U'] / a1['U'])))
    print('   had the text kept era 1\'s length per word, era 3\'s share would be %.2f%%; had the saving kept era 1\'s size, %.2f%%' % (100 * a3['saved'] / a1['U'], 100 * a1['saved'] / a3['U']))

    print('\nB. The share on other footings (mean of the six books, and its standard error)')
    out['B'] = {}
    def stat(vals): m = sum(vals) / len(vals); return m, math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1) / len(vals))
    for label, f in (('all cells (the sealed measure)', lambda r: S(r)),
                     ('cells saved over letters', lambda r: (r['ueb']['U'] - r['ueb']['C']) / r['ueb']['letters']),
                     ('cells saved over letters and the spaces between words', lambda r: (r['ueb']['U'] - r['ueb']['C']) / (r['ueb']['letters'] + r['ueb']['words'])),
                     ('cells saved per word', lambda r: (r['ueb']['U'] - r['ueb']['C']) / r['ueb']['words'])):
        row = {e: stat([f(r) for r in eras[e]]) for e in eras}; out['B'][label] = row
        print('   %-56s ' % label + '   '.join('%.4f (%.4f)' % row[e] for e in (1, 2, 3)) + '   Bible %.4f' % f(kjv))

    print('\nC. Era 2 in two halves, and era 3 by author (share of all cells, UEB)')
    early = [S(r) for r in eras[2] if r['year'] <= 1920]; late = [S(r) for r in eras[2] if r['year'] > 1920]
    print('   era 2, 1900 to 1920 (Lord Jim, The Age of Innocence, Styles): %.2f%%;   1922 to 1926 (Babbitt, Gatsby, The Sun Also Rises): %.2f%%' % (100 * sum(early) / 3, 100 * sum(late) / 3))
    hv = [S(r) for r in eras[3] if r['folder'].startswith('hoover')]; dc = [S(r) for r in eras[3] if r['folder'].startswith('doctorow')]
    print('   era 3: Hoover\'s three %.2f%%; Doctorow\'s three %.2f%%' % (100 * sum(hv) / 3, 100 * sum(dc) / 3))
    allb = sorted(eras[1] + eras[2] + eras[3], key=lambda r: r['year']); n = len(allb); xs = [r['year'] for r in allb]; ys = [100 * S(r) for r in allb]
    mx, my = sum(xs) / n, sum(ys) / n; slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    resid = [y - my - slope * (x - mx) for x, y in zip(xs, ys)]; se = math.sqrt(sum(r * r for r in resid) / (n - 2) / sum((x - mx) ** 2 for x in xs))
    print('   a straight line through the eighteen: %.3f points a century (standard error %.3f)' % (100 * slope, 100 * se))
    out['C'] = dict(early=sum(early) / 3, late=sum(late) / 3, hoover=sum(hv) / 3, doctorow=sum(dc) / 3, slope_per_century=100 * slope, slope_se=100 * se)

    print('\nD. Signs between era 1 and era 3: cells saved per 100,000 words')
    table = []
    for kind, ss in SIGNS.items():
        for s in ss: table.append((kind, s, [sign_saving(P[e], s, kind) for e in (0, 1, 2, 3)]))
    covered = {e: sum(t[2][i] for t in table) for i, e in enumerate((0, 1, 2, 3))}
    print('   the 182 signs so counted cover %s of the cells saved in the Bible and eras 1, 2, 3' % ', '.join('%.1f%%' % (100 * covered[e] / out['A'][e]['saved']) for e in (0, 1, 2, 3)))
    bykind = collections.OrderedDict()
    for kind, s, v in table:
        k = bykind.setdefault(kind, [0, 0, 0, 0]);
        for i in range(4): k[i] += v[i]
    for kind, v in bykind.items(): print('   %-20s Bible %7.0f   era 1 %7.0f   era 2 %7.0f   era 3 %7.0f   change, era 1 to 3: %+6.0f' % (kind, v[0], v[1], v[2], v[3], v[3] - v[1]))
    losers = sorted(table, key=lambda t: t[2][3] - t[2][1])[:16]; gainers = sorted(table, key=lambda t: t[2][1] - t[2][3])[:16]
    print('   the largest losses: ' + '; '.join('%s %.0f to %.0f' % (s, v[1], v[3]) for _, s, v in losers))
    print('   the largest gains:  ' + '; '.join('%s %.0f to %.0f' % (s, v[1], v[3]) for _, s, v in gainers))
    out['D'] = dict(table=[(k, s, v) for k, s, v in table], bykind=bykind, covered=covered)

    print('\nE. The letter-words, names set aside (a name: a word of five or more occurrences, nine in ten of them with a capital)')
    out['E'] = {}
    for e in (1, 2, 3):
        caps = collections.Counter()
        for r in eras[e]: caps.update(r['ueb'].get('caps', {}))
        names = {w for w, n in P[e]['vocab'].items() if n >= 5 and caps.get(w, 0) >= 0.9 * n}
        lw = study.letter_words(P[e], names_out=names); better = [L for L, v in lw.items() if v['best_worth'] > v['worth']]
        gain = sum(max(v['worth'], v['best_worth']) for v in lw.values()) / sum(v['worth'] for v in lw.values()); out['E'][e] = dict(lw=lw, better=better, gain=gain)
        print('   era %d: another word is worth more for %d letters; the best 21 are worth %.2f times braille\'s' % (e, len(better), gain))
        print('      ' + '; '.join('%s: %s %.0f, best other %s %.0f' % (L, v['word'], 1e5 * v['worth'] / P[e]['words'], v['best'], 1e5 * v['best_worth'] / P[e]['words']) for L, v in lw.items()))

    print('\nF. The American code against UEB, era by era, per 100,000 words')
    out['F'] = {}
    for e in (1, 2, 3):
        pe, pu = PE[e], P[e]; d = lambda w, kind='w': per100k(pe, w + '|' + kind) - per100k(pu, w + '|' + kind)
        total = 1e5 * (pe['U'] - pe['C']) / pe['words'] - 1e5 * (pu['U'] - pu['C']) / pu['words']
        parts = collections.OrderedDict([('to', d('to')), ('by', d('by')), ('into', d('into')), ('and, for, of, the, with joined to the next word', sum(d(w) for w in ('and', 'for', 'of', 'the', 'with')))])
        out['F'][e] = dict(total=total, parts=parts)
        print('   era %d: EBAE saves %.0f more cells; of that: %s; the rest (a joined, ble, ation, ally, com, dd, o\'clock, and differences of rule) %.0f' % (e, total, '; '.join('%s %.0f' % kv for kv in parts.items()), total - sum(parts.values())))

    print('\nG. The Bible\'s largest units, beside era 1 (cells saved per 100,000 words)')
    top = sorted(P[0]['by'].items(), key=lambda kv: -kv[1][1])[:14]
    print('   ' + '; '.join('%s %.0f (era 1: %.0f)' % (k.replace('|w', '').replace('|p', ' in a word'), per100k(P[0], k), per100k(P[1], k)) for k, _ in top))
    out['G'] = [(k, per100k(P[0], k), per100k(P[1], k)) for k, _ in top]
    json.dump(out, open(os.path.join(HERE, 'after%s.json' % ('-story' if 'story' in sys.argv[2:] else '')), 'w'), indent=1)
    more_later = True

# ---- added after the first look at A to H (still nothing predicted)
def more(books_dir):
    """I. the shortened forms of speech (n't, 'll, 've, 'd, 're) by era, beside the whole-word signs they take the place of
    J. what has no sign: the whole words, and the strings of letters inside words, that would save most as one-cell signs
    K. the rest of the American code's advantage taken apart
    L. the fall from era 1 to era 3 with each book left out in turn"""
    import re, louis
    recs = study.load(books_dir); eras = {e: [r for r in recs if r['era'] == e] for e in (1, 2, 3)}; kjv = [r for r in recs if r['era'] == 0][0]
    P = {e: pool(eras[e]) for e in eras}; P[0] = pool([kjv]); PE = {e: pool(eras[e], 'ebae') for e in eras}; out = {}
    print('\nI. Shortened forms per 100,000 words, and the whole words whose signs they pass by (occurrences per 100,000 words)')
    out['I'] = {}
    for e in (1, 2, 3):
        v = P[e]['vocab']; W = P[e]['words']; f = lambda pred: 1e5 * sum(n for w, n in v.items() if pred(w)) / W
        row = collections.OrderedDict([("n't", f(lambda w: w.endswith("n't"))), ("'ll", f(lambda w: w.endswith("'ll"))), ("'ve", f(lambda w: w.endswith("'ve"))), ("'d", f(lambda w: w.endswith("'d"))), ("'re", f(lambda w: w.endswith("'re"))),
                                       ('not', f(lambda w: w == 'not')), ('will', f(lambda w: w == 'will')), ('have', f(lambda w: w == 'have')), ('would', f(lambda w: w == 'would')), ('had', f(lambda w: w == 'had'))])
        out['I'][e] = row; print('   era %d: ' % e + '; '.join('%s %.0f' % kv for kv in row.items()))
    print('\nJ. What has no sign: worth as a one-cell sign, in cells per 100,000 words (occurrences times one less than the cells it takes now)')
    out['J'] = {}
    for e in (1, 2, 3):
        v = P[e]['vocab']; W = P[e]['words']; words = []
        for w, n in v.items():
            if n < 20 or len(w) < 2: continue
            c = study.cost(w)
            if c > 1: words.append((1e5 * n * (c - 1) / W, w, c))
        words.sort(reverse=True); out['J'][e] = dict(words=words[:20])
        print('   era %d, whole words: ' % e + '; '.join('%s %.0f (%d cells now)' % (w, x, c) for x, w, c in words[:16]))
    print('   (strings inside words: see the per-book records; not done here)')
    print('\nK. The American code\'s advantage: the signs UEB dropped, in cells per 100,000 words more than UEB saves on the same letters')
    out['K'] = {}
    for e in (1, 2, 3):
        pe, pu = PE[e], P[e]; row = collections.OrderedDict()
        for s in ('ation', 'ble', 'com', 'dd', 'ally'):
            row[s] = per100k(pe, s + '|p') + per100k(pe, s + '|w')                 # what the sign saves in EBAE (UEB spells these with other signs or letters)
        row["o'clock (as a word)"] = 1e5 * 5 * P[e]['vocab'].get("o'clock", 0) / pu['words']
        out['K'][e] = row; print('   era %d (gross, in EBAE): ' % e + '; '.join('%s %.0f' % kv for kv in row.items()))
    print('\nL. Era 1 less era 3, in points of the share saved, with one book left out at a time')
    S1 = [S(r) for r in eras[1]]; S3 = [S(r) for r in eras[3]]; full = 100 * (sum(S1) / 6 - sum(S3) / 6); lo = []
    for i in range(6): lo.append(100 * ((sum(S1) - S1[i]) / 5 - sum(S3) / 6))
    for i in range(6): lo.append(100 * (sum(S1) / 6 - (sum(S3) - S3[i]) / 5))
    print('   all books: %.2f; with one left out: from %.2f to %.2f; the lowest book of era 1 (%.2f%%) is above the highest of era 3 (%.2f%%)' % (full, min(lo), max(lo), 100 * min(S1), 100 * max(S3)))
    out['L'] = dict(full=full, lo=min(lo), hi=max(lo), min1=min(S1), max3=max(S3))
    json.dump(out, open(os.path.join(HERE, 'after-more%s.json' % ('-story' if 'story' in sys.argv[2:] else '')), 'w'), indent=1)

if __name__ == '__main__':
    more(sys.argv[1])
