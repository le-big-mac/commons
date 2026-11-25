# coverage.py -- how many of the corpus's rhyme words and pairs each dictionary knows, and by what respelling.  No rhyme is scored here.
# python -I coverage.py DATA_DIR corpus.json
import sys, json, collections, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lexicon as L, words as W
data, corpus = sys.argv[1], json.load(open(sys.argv[2], encoding='utf-8'))
cmu, uk, bf, bad = L.load_all(data)
def load_beep(path):
    d = {}
    for l in open(path, encoding='latin-1'):
        if l.startswith('#') or not l.strip(): continue
        w, *ph = l.split()
        if not ph or not re.match(r"^[A-Z']+$", w): continue
        d.setdefault(w.lower(), []).append(ph)
    return d
beep = load_beep(os.path.join(data, 'beep', 'beep', 'beep-1.0'))
print('cmudict', len(cmu), 'beep', len(beep), 'britfone', len(bf))
tot = collections.Counter()
print('%-11s %6s | %s' % ('poet', 'pairs', 'pairs with both words found: cmu exact, cmu any rule, beep exact, beep any, britfone any | share of word tokens found only by an old-spelling rule (cmu)'))
oov = collections.Counter(); rules = collections.Counter(); oldex = collections.defaultdict(collections.Counter)
for a, r in corpus.items():
    n = 0; c = collections.Counter(); wt = 0; wold = 0
    for s in r['stanzas']:
        ws = s['words']; sc = s['scheme']
        for w in ws:
            k, rule = W.lookup(w, cmu); wt += 1
            if rule and rule.startswith('old:'): wold += 1
            if rule and rule != 'exact': oldex[rule][W.normal(w) + '>' + k] += 1
            if k is None: oov[W.normal(w)] += 1
            rules[rule] += 1
        for i in range(len(ws)):
            for j in range(i + 1, len(ws)):
                if sc[i] != sc[j]: continue
                n += 1
                for name, D in (('cmu', cmu), ('beep', beep), ('bf', bf)):
                    (k1, r1), (k2, r2) = W.lookup(ws[i], D), W.lookup(ws[j], D)
                    if k1 and k2:
                        c[name + '-any'] += 1
                        if r1 == 'exact' and r2 == 'exact': c[name + '-exact'] += 1
    tot.update(c); tot['n'] += n
    print('%-11s %6d | %5.1f%% %5.1f%% %5.1f%% %5.1f%% %5.1f%% | %4.1f%%' % (a, n, 100 * c['cmu-exact'] / n, 100 * c['cmu-any'] / n, 100 * c['beep-exact'] / n, 100 * c['beep-any'] / n, 100 * c['bf-any'] / n, 100 * wold / wt))
n = tot['n']; print('%-11s %6d | %5.1f%% %5.1f%% %5.1f%% %5.1f%% %5.1f%%' % ('all', n, 100 * tot['cmu-exact'] / n, 100 * tot['cmu-any'] / n, 100 * tot['beep-exact'] / n, 100 * tot['beep-any'] / n, 100 * tot['bf-any'] / n))
print('\nrules (word tokens, cmu):', rules.most_common())
print('\nmost frequent words not found in cmudict:', ' '.join('%s:%d' % x for x in oov.most_common(100)))
for rule, c in sorted(oldex.items(), key=lambda x: -sum(x[1].values()))[:30]: print('\n' + rule, sum(c.values()), ':', ' '.join('%s:%d' % x for x in c.most_common(22)))
