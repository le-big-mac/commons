# expect.py -- figures for the page's tests, counted straight from pairs.tsv and fails.tsv (not from data.json).  python -I expect.py OUT_DIR expect.json
import sys, os, csv, json, collections
out = sys.argv[1]; rows = list(csv.DictReader(open(os.path.join(out, 'pairs.tsv'), encoding='utf-8'), delimiter='\t')); fails = list(csv.DictReader(open(os.path.join(out, 'fails.tsv'), encoding='utf-8'), delimiter='\t'))
E = {'partners': {}, 'fam_poet': {}, 'pair_fails': {}}
for w in ['love', 'tea', 'join', 'war', 'sea', 'eye', 'heaven', 'one', 'wind', 'prayer', 'dreary', 'great', 'come', 'was', 'majesty', 'xyzzy']:
    c = collections.Counter(); ok = {}; who = collections.defaultdict(set)
    for r in rows:
        if w in (r['w1'], r['w2']):
            o = r['w2'] if r['w1'] == w else r['w1']; c[o] += 1; who[o].add(r['poet'])
            if r['ev'] == '1': ok[o] = int(r['ok'])
    E['partners'][w] = sorted([[o, n, ok.get(o, 2), sorted(who[o])] for o, n in c.items()], key=lambda x: (-x[1], x[0]))
for r in fails: k = r['family'] + '|' + r['poet']; E['fam_poet'][k] = E['fam_poet'].get(k, 0) + 1
for a, b in [('obey', 'tea'), ('join', 'line'), ('love', 'move'), ('far', 'war'), ('is', 'this'), ('eye', 'majesty'), ('cat', 'dog')]:
    E['pair_fails'][a + '/' + b] = sum(1 for r in fails if {r['w1'], r['w2']} == {a, b})
E['n_fails'] = len(fails); E['n_pairs'] = len(rows); E['distinct'] = len({tuple(sorted([r['w1'], r['w2']])) for r in rows})
json.dump(E, open(sys.argv[2], 'w'))
print('expect.json written:', len(E['partners']), 'words,', len(E['fam_poet']), 'family-poet cells,', len(E['pair_fails']), 'pairs')
