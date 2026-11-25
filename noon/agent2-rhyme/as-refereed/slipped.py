# slipped.py -- an after-check prompted by the referee's blind step: in some poems of the corpus's annotation files the scheme
# lines have slipped out of step with the word lines (blocks whose two lengths differ show it).  Here the scores with every
# such poem left out whole.   python -I slipped.py GOLD_DIR corpus.json OUT_DIR
import sys, os, json, csv, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from poets import POETS, GROUPS
gold, corpus, out = sys.argv[1], json.load(open(sys.argv[2], encoding='utf-8')), sys.argv[3]
bad = collections.defaultdict(set); nb = 0
for a in corpus:
    cur = []
    for l in open(os.path.join(gold, a + '.pgold'), encoding='utf-8', errors='replace').read().split('\n') + ['']:
        if l.strip() == '':
            if cur:
                ok = len(cur) == 3 and cur[0].startswith('POEM') and len(cur[0].split()) - 1 == len(cur[1].split()) == len(cur[2].split())
                if not ok:
                    nb += 1
                    if cur[0].startswith('POEM'): bad[a].add(int(cur[0].split()[0][4:]))
                    elif last is not None: bad[a].add(last)
                if cur[0].startswith('POEM'): last = int(cur[0].split()[0][4:])
            cur = []
        else: cur.append(l.strip())
    last = None
print('blocks refused: %d, in %d poems: %s' % (nb, sum(len(v) for v in bad.values()), '; '.join('%s %s' % (a, sorted(v)) for a, v in sorted(bad.items()))))
rows = list(csv.DictReader(open(os.path.join(out, 'pairs.tsv'), encoding='utf-8'), delimiter='\t'))
keep = [r for r in rows if corpus[r['poet']]['stanzas'][int(r['stanza'])]['poem'] not in bad[r['poet']]]
def M(rs): ev = [r for r in rs if r['ev'] == '1']; return 100 * sum(1 for r in ev if r['ok'] == '1') / len(ev), len(ev)
print('pairs: %d with every poem, %d with the %d slipped poems left out' % (len(rows), len(keep), sum(len(v) for v in bad.values())))
print('whole corpus: %.2f%% of %d; without them %.2f%% of %d' % (M(rows) + M(keep)))
for g in GROUPS: print('%s: %.2f%% of %d; without them %.2f%% of %d' % ((g,) + M([r for r in rows if r['period'] == g]) + M([r for r in keep if r['period'] == g])))
for p in sorted(bad): print('%s: %.2f%% of %d; without them %.2f%% of %d' % ((p,) + M([r for r in rows if r['poet'] == p]) + M([r for r in keep if r['poet'] == p])))
low = sorted([p for p in POETS if M([r for r in keep if r['poet'] == p])[1] >= 1000], key=lambda p: M([r for r in keep if r['poet'] == p])[0]); print('lowest among poets with 1,000 judged, without them: ' + ', '.join('%s %.2f' % (p, M([r for r in keep if r['poet'] == p])[0]) for p in low[:4]))
fam = collections.Counter(); famk = collections.Counter(); kk = {(r['poet'], r['stanza']) for r in keep}
for r in csv.DictReader(open(os.path.join(out, 'fails.tsv'), encoding='utf-8'), delimiter='\t'):
    if r['family'] == 'sea : way': fam[r['poet']] += 1; famk[r['poet']] += (r['poet'], r['stanza']) in kk
print('sea : way pairs, with and without them: ' + ', '.join('%s %d and %d (%.1f in a thousand of %d judged)' % (p, fam[p], famk[p], 1000 * famk[p] / M([r for r in keep if r['poet'] == p])[1], M([r for r in keep if r['poet'] == p])[1]) for p in ['finch', 'prior', 'swift', 'pope', 'dryden']))
