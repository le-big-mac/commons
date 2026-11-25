# after.py -- checks made after the scores, none sealed.   python -I after.py OUT_DIR
import sys, os, csv, json, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from poets import POETS, GROUPS
out = sys.argv[1]; rows = list(csv.DictReader(open(os.path.join(out, 'pairs.tsv'), encoding='utf-8'), delimiter='\t'))
fam = {(r['poet'], r['stanza'], r['i'], r['j']): r['family'] for r in csv.DictReader(open(os.path.join(out, 'fails.tsv'), encoding='utf-8'), delimiter='\t')}
S = json.load(open(os.path.join(out, 'score.json'))); ev = [r for r in rows if r['ev'] == '1']
# 1. every estimate on file of "the share that still rhyme", whole corpus
A = S['all']; fm = json.load(open(os.path.join(out, 'feminine.json')))['tot']['all']
est = [('either dictionary, last vowel on, any listed pronunciation (the main measure)', A['M']), ('the same, only pairs both dictionaries judge', A['M_both']), ('the same, only neighbouring lines of a group', A['M_adjacent']),
       ('American alone', A['M_A']), ('British alone', A['M_B']), ('American, two-syllable rhymes judged in full', 100 * fm['strict'] / fm['n']), ('American, first-listed pronunciations only', A['M_A1']), ('American, from the stressed vowel on', A['M_Along'])]
print('1. Estimates of the share that still rhyme, whole corpus:'); [print('   %6.2f%%  %s' % (v, n)) for n, v in est]
# 2. each different pair of words counted once for each poet
d = {}
for r in ev: d[(r['poet'], tuple(sorted([r['w1'], r['w2']])))] = r['ok'] == '1'
print('\n2. Each different pair of words counted once a poet: %.2f%% of %d (all pairs: %.2f%% of %d)' % (100 * sum(d.values()) / len(d), len(d), A['M'], len(ev)))
per = {p: corpus_period for p, corpus_period in {r['poet']: r['period'] for r in rows}.items()}
for g in GROUPS:
    k = [v for (p, w), v in d.items() if per[p] == g]; print('   %s: %.2f%% of %d' % (g, 100 * sum(k) / len(k), len(k)))
# 3. three families by group, with the luck of the stanzas (2,000 redrawings; 5th and 95th centiles), and by poet within the group born 1631 to 1688
random.seed(7); st = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.Counter()))
for r in ev:
    c = st[r['period']][(r['poet'], r['stanza'])]; c['n'] += 1
    f = fam.get((r['poet'], r['stanza'], r['i'], r['j']))
    if f: c[f] += 1
print('\n3. Failing pairs per thousand judged, by group, with the 5th and 95th centiles of 2,000 redrawings of the stanzas:')
for f in ['sea : way', 'join : line', 'love : move', 'now : know']:
    line = []
    for g in GROUPS:
        units = list(st[g].values()); n = sum(u['n'] for u in units); k = sum(u[f] for u in units); v = []
        for _ in range(2000):
            a = b = 0
            for _ in range(len(units)): u = units[random.randrange(len(units))]; a += u['n']; b += u[f]
            v.append(1000 * b / a)
        v.sort(); line.append('%s %.1f (%.1f to %.1f)' % (g, 1000 * k / n, v[100], v[1899]))
    print('   %-12s %s' % (f, '; '.join(line)))
F = json.load(open(os.path.join(out, 'families.json')))
for f in ['sea : way', 'join : line']: print('   %s in the group born 1631 to 1688, by poet: %s' % (f, ', '.join('%s %d (%.1f)' % (p, F['by_poet'][f][p][0], F['by_poet'][f][p][1]) for p in ['dryden', 'finch', 'prior', 'swift', 'pope'])))
ps = collections.Counter(tuple(sorted([r['w1'], r['w2']])) for r in ev if fam.get((r['poet'], r['stanza'], r['i'], r['j'])) == 'sea : way' and r['poet'] in ('finch', 'prior', 'swift'))
print('   sea : way in Finch, Prior and Swift: %d pairs, %d different' % (sum(ps.values()), len(ps)))
# 4. the last group, pairs both dictionaries judge
b = [r for r in rows if r['period'] == '1819' and r['ea'] == '1' and r['eb'] == '1']
ay = collections.Counter('/'.join(sorted([r['w1'], r['w2']])) for r in b if r['as'] == '1' and r['bs'] == '0'); by = collections.Counter('/'.join(sorted([r['w1'], r['w2']])) for r in b if r['as'] == '0' and r['bs'] == '1')
print('\n4. The group born 1859 to 1887, %d pairs both dictionaries judge: American only %d (%s); British only %d (%s)' % (len(b), sum(ay.values()), ', '.join('%s %d' % x for x in ay.most_common(8)), sum(by.values()), ', '.join('%s %d' % x for x in by.most_common(8))))
# 5. how many pairs are judged only thanks to a rule for elisions or British spellings
ex = lambda r, k1, k2, v: r[v] != '' and r[k1] == r['w1'] and r[k2] == r['w2']
exact = sum(1 for r in rows if ex(r, 'ka', 'ka2', 'as') or ex(r, 'kb', 'kb2', 'bs')); print('\n5. Pairs judged with both words found as spelt in some dictionary: %d; judged in all: %d; so %d are judged by a rule for elisions or British spellings' % (exact, len(ev), len(ev) - exact))
# 6. one stanza and one poet
th = [r for r in ev if r['poet'] == 'thomas']; th2 = [r for r in th if 'silently' not in (r['w1'], r['w2'])]
print('\n6. Edward Thomas with his stanza of "silently" left out: %.1f%% of %d (with it: %.1f%% of %d). The earliest group is More for %d of its %d judged pairs.' % (100 * sum(1 for r in th2 if r['ok'] == '1') / len(th2), len(th2), 100 * sum(1 for r in th if r['ok'] == '1') / len(th), len(th), S['poets']['more']['evaluable'], S['groups']['1415']['evaluable']))
g19 = [r for r in ev if r['period'] == '1819' and not (r['poet'] == 'thomas' and 'silently' in (r['w1'], r['w2']))]; print('   The last group without that stanza: %.2f%% of %d.' % (100 * sum(1 for r in g19 if r['ok'] == '1') / len(g19), len(g19)))
