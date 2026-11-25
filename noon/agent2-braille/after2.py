"""after2.py: after the two sheets: my books beside two counts in print that I read only after the first sheet was scored.
    /usr/bin/python3 -I after2.py books  ->  after2.out (printed), after2.json
Kederis, Siems and Haynes (1965), American Grade 2, as John Lorimer reports them (1982): contractions take 31% off the cells in words,
26.5% when punctuation is counted too, and "probably a little below 25%" with the blanks between words. Lorimer's own Table 1 (1982),
British Grade 2, thirty samples of a thousand words of adult reading: in a million words 3,125,000 embossed cells in words, 1,350,000 saved
by contractions, 4,250,000 spaces in all against 5,655,000 uncontracted: "about 30%" of the cells in words and "almost 25%" of all space.
His Table 2: the first 14 contractions save half, 84 save nine tenths. Nothing here was sealed: I had seen my own totals."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study
if __name__ == '__main__':
    recs = study.load(sys.argv[1]); out = {}
    groups = [('the Bible of 1611', [r for r in recs if r['era'] == 0])] + [('era %d' % e, [r for r in recs if r['era'] == e]) for e in (1, 2, 3)]
    print('M. The American code (EBAE), pooled: the quantities of the counts of 1965 and 1982')
    print('   in print: Kederis 1965 (American): 31% of cells in words; a little below 25% of all space.  Lorimer 1982 (British): 1,350,000 cells saved in a million words; about 30% of cells in words; almost 25% of all space (24.85% from his table, which has no capital signs)')
    for name, rs in groups:
        p = study.pool(rs, 'ebae'); letters = sum(r['ebae']['letters'] for r in rs); caps = sum(sum(r['ebae']['caps'].values()) for r in rs)
        saved = p['U'] - p['C']; tot = sum(v[1] for v in p['by'].values()); ranked = sorted((v[1] for v in p['by'].values()), reverse=True)
        cum = 0; n90 = 0
        for v in ranked:
            cum += v; n90 += 1
            if cum >= 0.9 * tot: break
        row = dict(per_million=1e6 * saved / p['words'], in_words=saved / letters, total=saved / p['U'], total_nocaps=saved / (p['U'] - caps), top14=sum(ranked[:14]) / tot, n90=n90,
                   books=[(r['ebae']['U'] - r['ebae']['C']) / r['ebae']['U'] for r in rs])
        out[name] = row
        print('   %-18s %9.0f cells saved in a million words; %.1f%% of the letters; %.2f%% of all cells (%.2f%% with the capital signs taken out); the 14 largest units save %.1f%%; %d units save nine tenths'
              % (name, row['per_million'], 100 * row['in_words'], 100 * row['total'], 100 * row['total_nocaps'], 100 * row['top14'], row['n90']))
    for name, rs in groups[1:]:
        b = out[name]['books']; print('   %s, book by book, share of all cells in EBAE: %s; mean %.2f%%' % (name, ', '.join('%.2f' % (100 * x) for x in b), 100 * sum(b) / len(b)))
    print('\nN. The same in Unified English Braille (which has no joined words and nine fewer signs)')
    for name, rs in groups:
        p = study.pool(rs); letters = sum(r['ueb']['letters'] for r in rs); saved = p['U'] - p['C']; tot = sum(v[1] for v in p['by'].values()); ranked = sorted((v[1] for v in p['by'].values()), reverse=True)
        cum = 0; n90 = 0
        for v in ranked:
            cum += v; n90 += 1
            if cum >= 0.9 * tot: break
        signs = [(k, s) for k, ss in study.SIGNS.items() for s in ss]
        def worth(sign, kind):
            keys = [sign + '|w'] if kind in study.WORD_KINDS else [k for k in p['by'] if k.split('|')[0].startswith(sign)] if kind == 'shortform' else [sign + '|p', sign + '|w']
            return sum(p['by'].get(k, [0, 0])[1] for k in keys)
        weak = [s for k, s in signs if 1e3 * worth(s, k) / p['words'] < 1]
        out[name + ' ueb'] = dict(per_million=1e6 * saved / p['words'], in_words=saved / letters, top14=sum(ranked[:14]) / tot, n90=n90, weak=weak)
        print('   %-18s %9.0f cells saved in a million words; %.1f%% of the letters; the 14 largest units save %.1f%%; %d units save nine tenths; %d of the 182 signs save less than one cell in a thousand words'
              % (name, 1e6 * saved / p['words'], 100 * saved / letters, 100 * sum(ranked[:14]) / tot, n90, len(weak)))
    json.dump(out, open(os.path.join(HERE, 'after2%s.json' % ('-story' if 'story' in sys.argv[2:] else '')), 'w'), indent=1)
