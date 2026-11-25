"""facts.py: checks of what the write-up of the braille study says against the saved sources and my own records.
    /usr/bin/python3 -I facts.py ~/braille-data      (prints each check; exit status 1 if any fails)"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import study
def squeeze(s):
    """letters, digits and marks only, no white space: the scans run words together and break them at line ends"""
    return re.sub(r'\s+', '', s.replace('­', '').replace('’', "'").replace('“', '"').replace('”', '"'))
def rulebook_lists(text):
    """the nine lists at the head of sections 10.1 to 10.9 of the Rules of Unified English Braille"""
    heads = ['Alphabetic wordsigns', 'Strong wordsigns', 'Strong contractions', 'Strong groupsigns', 'Lower wordsigns', 'Lower groupsigns', 'Initial-letter contractions', 'Final-letter groupsigns', 'Shortforms']
    lines = text.split('\n'); starts = [max(i for i, l in enumerate(lines) if re.match(r'\s*10\.%d\s+%s\s*$' % (n + 1, re.escape(h)), l)) for n, h in enumerate(heads)]
    B = '[⠀-⣿]+'; out = []
    for n, a in enumerate(starts):
        words = []
        for l in lines[a + 1:]:
            if re.match(r'\s*10\.%d\.1\s' % (n + 1), l): break
            if n < 8:
                m = re.match(r'\s+%s\s+%s\s+([a-z]+)\b' % (B, B), l)
                if m: words.append(m.group(1))
            else: words += re.findall(r'%s ([a-z]+)\b' % B, l)      # two entries are printed without their "(see ...)"
        out.append(words)
    return out
if __name__ == '__main__':
    root = os.path.expanduser(sys.argv[1]); bad = 0; n = 0
    def check(ok, what):
        global bad, n
        n += 1; bad += not ok; print('%s  %s' % ('ok    ' if ok else 'FAILED', what))
    for q in json.load(open(os.path.join(HERE, 'quotes.json'))):
        src = open(os.path.join(root, q['source']), encoding='utf-8', errors='replace').read()
        if q['source'].endswith('.json'): src = re.sub(r'<[^>]+>', '', json.load(open(os.path.join(root, q['source'])))['message'].get('abstract', ''))
        check(squeeze(q['quote']) in squeeze(src), 'quoted words are in %s: "%s..."' % (q['source'], q['quote'][:60]))
    lists = rulebook_lists(open(os.path.join(root, 'rulebook', 'text.txt'), encoding='utf-8').read())
    kinds = ['letter-word', 'strong wordsign', 'strong contraction', 'strong groupsign', 'lower wordsign', 'lower groupsign', 'initial-letter', 'final-letter', 'shortform']
    for kind, words in zip(kinds, lists):
        mine = study.SIGNS[kind]
        check(sorted(mine) == sorted(words), 'my %d signs called %s are the rulebook\'s %d%s' % (len(mine), kind, len(words), '' if sorted(mine) == sorted(words) else ': mine only %s; the book only %s' % (sorted(set(mine) - set(words)), sorted(set(words) - set(mine)))))
    total = sum(len(v) for v in study.SIGNS.values()); cells_twice = [w for w in study.SIGNS['lower groupsign'] if w in study.SIGNS['lower wordsign']]
    check(total == 182, 'the nine lists hold %d entries (the words that stand in two lists, as a word and as a part of one: %s)' % (total, ', '.join(cells_twice)))
    # the README's figures, each computed here from the records and then looked for, as the README prints it
    import collections, lines, story
    readme = re.sub(r'\s+', ' ', open(os.path.join(HERE, 'README.md'), encoding='utf-8').read())
    def era_sets(d): recs = study.load(os.path.join(HERE, d)); return {e: [r for r in recs if r['era'] == e] for e in (0, 1, 2, 3)}
    eras = era_sets('books-story'); sent = era_sets('books'); wr = era_sets('books-expand'); S = study.S; m = lambda xs: sum(xs) / len(xs); c = lambda v: format(int(round(v)), ',')
    mean = {e: m([S(r) for r in eras[e]]) for e in eras}; ms = {e: m([S(r) for r in sent[e]]) for e in (1, 2, 3)}; mw = {e: m([S(r) for r in wr[e]]) for e in (1, 2, 3)}
    P = {e: study.pool(eras[e]) for e in eras}; PE = {e: study.pool(eras[e], 'ebae') for e in eras}
    def speech(fn):
        sp = json.load(open(os.path.join(HERE, fn))); g = {e: [r for r in sp if r['era'] == e] for e in (1, 2, 3)}
        return g, {e: m([1 - r['out'][1] / r['out'][0] for r in g[e]]) for e in g}, {e: m([1 - r['in'][1] / r['in'][0] for r in g[e]]) for e in g}, {e: m([r['in'][2] / (r['in'][2] + r['out'][2]) for r in g[e]]) for e in g}
    spe, out_, in_, share = speech('speech-story.json'); spe0, out0, in0, share0 = speech('speech.json')
    early = m([S(r) for r in eras[2] if r['year'] <= 1920]); late = m([S(r) for r in eras[2] if r['year'] > 1920])
    w = lambda e, k: study.per100k(P[e], k); n_t = lambda e: 1e5 * sum(v for k, v in P[e]['vocab'].items() if k.endswith("n't")) / P[e]['words']
    short = lambda e: sum(v[1] for k, v in P[e]['by'].items() if any(k.split('|')[0].startswith(x) for x in study.SIGNS['shortform'])) * 1e5 / P[e]['words']
    per = lambda p: 1e5 / p['words']; c3 = P[3]['C'] * per(P[3]); c3as1 = P[3]['U'] * per(P[3]) - (P[1]['U'] - P[1]['C']) * per(P[1])
    letters = lambda e: sum(r['ebae']['letters'] for r in eras[e]); sv = lambda e: PE[e]['U'] - PE[e]['C']; mil = lambda e: 1e6 * sv(e) / PE[e]['words']
    onlet = {e: m([(r['ueb']['U'] - r['ueb']['C']) / r['ueb']['letters'] for r in eras[e]]) for e in (1, 2, 3)}
    loo = [m([S(r) for r in eras[1] if r is not x]) - m([S(r) for r in eras[3] if r is not x]) for x in eras[1] + eras[3]]
    amer = sorted(1 - r['in'][1] / r['in'][0] for r in spe[2] if r['year'] > 1920); nofr = [r for r in spe[1] if 'Frankenstein' not in r['title']]
    lowJE = min(S(r) for r in wr[1]); above = sum(S(r) > lowJE for r in wr[3])
    a3 = json.load(open(os.path.join(HERE, 'after3.json'))); a2 = json.load(open(os.path.join(HERE, 'after2-story.json'))); weak = [len(a2['era %d ueb' % e]['weak']) for e in (1, 2, 3)]
    rl = json.load(open(os.path.join(HERE, 'ruler.json'))); th = json.load(open(os.path.join(HERE, 'third.json'))); ln = json.load(open(os.path.join(HERE, 'lines.json'))); sealed = json.load(open(os.path.join(HERE, 'lines-as-sealed.json')))
    rg = a3['P']['ranges']['letters']; old8, rec8 = rg['the eight texts before 1895'], rg['the eight after 1970']; rows = {x['folder']: x for x in a3['P']['rows']}
    Lm = {e: m([(r['ueb']['U'] - r['ueb']['C']) / (r['ueb']['letters'] + r['ueb']['words']) for r in eras[e]]) for e in (1, 3)}
    def gain(e):                                       # the best word for each letter, names set aside, against braille's own: worked here again from the records
        caps = collections.Counter()
        for r in eras[e]: caps.update(r['ueb'].get('caps', {}))
        names = {wd for wd, k in P[e]['vocab'].items() if k >= 5 and caps.get(wd, 0) >= 0.9 * k}; lw = study.letter_words(P[e], names_out=names)
        return sum(max(v['worth'], v['best_worth']) for v in lw.values()) / sum(v['worth'] for v in lw.values()), sum(v['best_worth'] > v['worth'] for v in lw.values())
    PEs = study.pool(sent[2], 'ebae'); be_units = study.per100k(PEs, 'be|w', 0) + study.per100k(PEs, 'be|p', 0)
    dash = [float(l.split(':')[2].split()[0]) for l in open(os.path.join(HERE, 'dash.out')) if l.startswith('era')]
    tr = {f: th['rows'][f] for f in th['rows']}; T = lambda f: '%.2f%% | %.2f%% | %.2f%%' % tuple(tr[f]['L'])
    claims = [
        ('the three means and the Bible, in brief', 'they save 23.7%% of the cells; in six of 1900 to 1926, %.1f%%; in six of 1991 to 2009, %.1f%%; in the Bible, %.1f%%' % (100 * mean[2], 100 * mean[3], 100 * mean[0]), '%.1f' % (100 * mean[1]) == '23.7'),
        ('the three means', 'The three means are %.2f%%, %.2f%% and %.2f%%' % (100 * mean[1], 100 * mean[2], 100 * mean[3]), True),
        ('no overlap between the first six and the last six', 'the lowest of the first is %.2f%%, the highest of the last %.2f%%' % (100 * min(S(r) for r in eras[1]), 100 * max(S(r) for r in eras[3])), min(S(r) for r in eras[1]) > max(S(r) for r in eras[3])),
        ('one book left out', 'leaving any one book out the gap stays between %.1f and %.1f points' % (100 * min(loo), 100 * max(loo)), True),
        ('the two halves of the middle six', 'average %.1f%%. Babbitt, The Great Gatsby and The Sun Also Rises (1922 to 1926) average %.1f%%' % (100 * early, 100 * late), True),
        ('written out', 'the three means are %.2f%%, %.2f%% and %.2f%%. The gap between the first six and the last goes from %.2f points to %.2f, the middle six and the last six come within %.2f, and three of the last six now save more than Jane Eyre' % (100 * mw[1], 100 * mw[2], 100 * mw[3], 100 * (mean[1] - mean[3]), 100 * (mw[1] - mw[3]), 100 * (mw[2] - mw[3])), above == 3 and 0.30 < 1 - (mw[1] - mw[3]) / (mean[1] - mean[3]) < 0.37),
        ('letters alone', 'against letters alone, the three means are %.1f%%, %.1f%% and %.1f%%' % (100 * onlet[1], 100 * onlet[2], 100 * onlet[3]), 0.15 < 1 - (1 - onlet[3] / onlet[1]) / (1 - mean[3] / mean[1]) < 0.25),
        ('which and not', '*which* %s to %d; *not* %s to %d' % (c(w(1, 'which|w')), round(w(3, 'which|w')), c(w(1, 'not|w')), round(w(3, 'not|w'))), True),
        ("n't", '%d in 100,000 words in the first six, %d in the last' % (round(n_t(1)), round(n_t(3))), True),
        ('just', '*just* %d to %s' % (round(w(1, 'just|w')), c(w(3, 'just|w'))), True),
        ('the shortened spellings fell by a fifth', 'down by a fifth', 0.17 < 1 - short(3) / short(1) < 0.25),
        ('narration and speech', 'from %.1f%% in the first six to %.1f%% in the last; inside them from %.1f%% to %.1f%%' % (100 * out_[1], 100 * out_[3], 100 * in_[1], 100 * in_[3]), True),
        ('the middle six', 'In the middle six, speech is at %.1f%% and narration at %.1f%%' % (100 * in_[2], 100 * out_[2]), True),
        ('the three American novels', '(%.1f%%, %.1f%%, %.1f%%)' % tuple(100 * x for x in sorted(amer, reverse=True)), in_[3] > in_[2]),
        ('less speech in the last six', '(%.0f%% of letters against %.0f%%)' % (100 * share[3], 100 * share[1]), share[3] < share[1]),
        ('without Frankenstein', 'Without it the first novels are %.1f%% inside and %.1f%% outside, with %.0f%% of their letters inside' % (100 * m([1 - r['in'][1] / r['in'][0] for r in nofr]), 100 * m([1 - r['out'][1] / r['out'][0] for r in nofr]), 100 * m([r['in'][2] / (r['in'][2] + r['out'][2]) for r in nofr])), True),
        ('signs that do little', '%d of the 182 signs fall short in the first six novels, %d in the middle six and %d in the last six' % tuple(weak), weak[0] < weak[1] < weak[2]),
        ('the Bible', 'It saves %s more cells in 100,000 words than the first six novels. *The* saves %s more there, *and* %s more, *shall* %s more and *th* %s more' % (c(a3['S']['total']), c(a3['S']['parts']['the']), c(a3['S']['parts']['and']), c(a3['S']['parts']['shall']), c(a3['S']['parts']['th'])), True),
        ('the Bible\'s religious words', 'add %d, and *lord*, *children* and *father* %s: together about a third of the lead' % (round(a3['S']['parts']['the religious shortforms']), c(a3['S']['parts']['lord, children, father'])), 0.30 < (a3['S']['parts']['the religious shortforms'] + a3['S']['parts']['lord, children, father']) / a3['S']['total'] < 0.40),
        ('the letter-words', 'worth %.2f times as much as braille\'s choices in the first six novels, %.2f times in the middle six and %.2f times in the last six' % (gain(1)[0], gain(2)[0], gain(3)[0]), True),
        ('how big', 'take about %s cells for 100,000 words. Had the signs saved what they save in the first six, they would take about %s' % (format(int(round(c3, -3)), ','), format(int(round(c3as1, -2)), ',')), 0.015 < c3 / c3as1 - 1 < 0.025),
        ('the two lines', '(r squared %.2f against %.2f), and with both in one fit the year\'s slope is %.2f points a century with a standard error of %.2f' % (ln['S']['r2_rate'], ln['S']['r2_year'], 100 * ln['S']['both'][0], 100 * ln['S']['both'][2]), True),
        ('the two lines as fitted before the sheet', 'the sheet quotes the fits before it, %.2f, %.2f and %.2f' % (sealed['S']['r2_rate'], sealed['S']['r2_year'], 100 * sealed['S']['both'][2]), True),
        ('Huckleberry Finn between the lines', 'it is %.2f above the shortened forms\' line and only %.2f below the year\'s' % (tr['twain-huck-finn-1884']['L'][0] - tr['twain-huck-finn-1884']['L'][2], tr['twain-huck-finn-1884']['L'][1] - tr['twain-huck-finn-1884']['L'][0]), True),
        ('Three Men in a Boat sits high', 'sits high, above Jane Eyre and Moby-Dick', tr['jerome-three-men-1889']['L'][0] > max(rows[f]['L'] for f in ('bronte-jane-eyre-1847', 'melville-moby-dick-1851')) and tr['jerome-three-men-1889']['L'][0] > 24.27),
        ('long words', 'Words of eight letters or more hold %.0f%% and %.0f%% of their letters, against %.0f%% in the first six novels' % (a3['V']['each']['hoover-zen-culture-1977'], a3['V']['each']['hoover-zen-experience-1980'], a3['V']['sets'][0]), True),
        ('the middle six on letters', 'three of the middle six (Lord Jim, The Age of Innocence, The Sun Also Rises) sit inside the old range', all(old8[0] < rows[f]['letters'] < old8[1] for f in ('conrad-lord-jim-1900', 'wharton-age-of-innocence-1920', 'hemingway-sun-1926')) and sum(old8[0] < x['letters'] for x in a3['P']['rows'] if x['era'] == 2) == 3 and all(a3['P']['ranges'][k]['the eight texts before 1895'][0] < a3['P']['ranges'][k]['the eight after 1970'][1] for k in ('S', 'L', 'word'))),
        ('the third sheet\'s measure', 'the first six novels average %.2f%% and the last six %.2f%%' % (100 * Lm[1], 100 * Lm[3]), True),
        ('Huckleberry Finn', '| Adventures of Huckleberry Finn, 1884 | %.1f | %s |' % (rows['twain-huck-finn-1884']['rate'], T('twain-huck-finn-1884')), tr['twain-huck-finn-1884']['L'][0] < 24.27),
        ('Three Men in a Boat', '| Three Men in a Boat, 1889 | %.1f | %s |' % (rows['jerome-three-men-1889']['rate'], T('jerome-three-men-1889')), True),
        ('Zen Culture', '| Zen Culture, 1977 | %.1f | %s |' % (rows['hoover-zen-culture-1977']['rate'], T('hoover-zen-culture-1977')), True),
        ('The Zen Experience', '| The Zen Experience, 1980 | %.1f | %s |' % (rows['hoover-zen-experience-1980']['rate'], T('hoover-zen-experience-1980')), th['held'] == 1 and th['n'] == 6),
        ('the Zen books\' long words', '(%.2f and %.2f letters a word, against %.2f in the first six novels)' % (rows['hoover-zen-culture-1977']['lw'], rows['hoover-zen-experience-1980']['lw'], sum(r['ueb']['letters'] for r in eras[1]) / P[1]['words']), True),
        ('and their saving a word', '(%.2f and %.2f cells a word, against %.2f)' % (rows['hoover-zen-culture-1977']['word'], rows['hoover-zen-experience-1980']['word'], m([(r['ueb']['U'] - r['ueb']['C']) / r['ueb']['words'] for r in eras[1]])), True),
        ('cells saved in 100 letters, old and recent', 'all eight texts from before 1895 (%.1f to %.1f) stand above all eight from after 1970 (%.1f to %.1f)' % (old8[0], old8[1], rec8[0], rec8[1]), 0.25 < old8[0] - rec8[1] < 0.35),
        ('the American code, cells in a million words', '%s, %s and %s cells in a million words in the first, middle and last six novels' % tuple(format(int(round(mil(e), -3)), ',') for e in (1, 2, 3)), [round(100 * (mil(e) / 1350000 - 1)) for e in (1, 2, 3)] == [9, 3, 2] and round(100 * (1 - mil(3) / mil(1))) == 6),
        ('the American code, shares', '%.1f%%, %.1f%% and %.1f%% of the letters; %.1f%%, %.1f%% and %.1f%% of all cells' % tuple([100 * sv(e) / letters(e) for e in (1, 2, 3)] + [100 * sv(e) / PE[e]['U'] for e in (1, 2, 3)]), True),
        ('the translator against the rulebook', 'print %s examples of contractions with their braille that my reader could take. The translator gives the rulebook\'s braille for %d. Of the rest, %d cannot be compared: in %d the print had italics that my text of the rulebook has lost, and %d show a word divided' % (format(rl['n'], ','), rl['same'], rl['emphasis'] + rl['divided'], rl['emphasis'], rl['divided']), len(rl['diff']) == 18 and rl['plain'] == ['captainess', 'lllittle']),
        ('in after a dash', '*in* follows a dash %.1f, %.1f and %.1f times in 100,000 words' % tuple(dash), True),
        ('the words of the eighteen novels', 'my own count of the words is %s' % format(sum(r['ueb']['words'] for e in (1, 2, 3) for r in sent[e]), ','), abs(sum(r['ueb']['words'] for e in (1, 2, 3) for r in sent[e]) / 2347129 - 1) < 0.001),
        ('the files as sent', 'where the three means are %.2f%%, %.2f%% and %.2f%%' % (100 * ms[1], 100 * ms[2], 100 * ms[3]), True),
        ('the mended reader\'s be', '*be* is %d against his 801' % round(be_units), abs(be_units / 801 - 1) > 0.35),
        ('B8', 'another word beats braille\'s for %d of the 21 letters in the first six novels and %d in the last' % (gain(1)[1], gain(3)[1]), True),
        ('the second sheet as scored', 'where narration goes from %.1f%% to %.1f%% and speech from %.1f%% to %.1f%%' % (100 * out0[1], 100 * out0[3], 100 * in0[1], 100 * in0[3]), True),
        ('D4 as scored', 'It is lower: %.1f%% against %.1f%%' % (100 * share0[3], 100 * share0[1]), True),
    ]
    for what, text, also in claims:
        check(re.sub(r'\s+', ' ', text) in readme and also, 'the README says, as computed here (%s): "%s"' % (what, text[:90]))
    counts = [open(os.path.join(HERE, f)).read().strip().splitlines()[-1] for f in ('verdicts-as-first-run.out', 'verdicts-2-as-first-run.out', 'verdicts-3-as-first-run.out')]
    check(counts[0].strip().startswith('12 of 13 held; Brier score 0.173') and counts[1].strip().startswith('3 of 5 held; Brier score 0.227') and counts[2].strip().startswith('1 of 6 held; Brier score 0.283') and 'sixteen held and eight failed' in readme, 'the three sheets as first run: %s' % ' | '.join(x.strip() for x in counts))
    print('%d of %d checks pass' % (n - bad, n)); sys.exit(1 if bad else 0)
