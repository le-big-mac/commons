# boot.py -- how far each poet's share could move by the luck of which stanzas are in the corpus: stanzas drawn again with
# replacement, 2,000 times, 5th and 95th centiles of M.   python -I boot.py OUT_DIR  -> OUT_DIR/boot.json
import sys, os, csv, json, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from poets import POETS, GROUPS
out = sys.argv[1]; rows = list(csv.DictReader(open(os.path.join(out, 'pairs.tsv'), encoding='utf-8'), delimiter='\t'))
st = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0])); per = {}
for r in rows:
    per[r['poet']] = r['period']
    if r['ev'] == '1': x = st[r['poet']][r['stanza']]; x[0] += 1; x[1] += r['ok'] == '1'
random.seed(20261124); res = {}
def ci(units):
    v = []
    for _ in range(2000):
        n = k = 0
        for _ in range(len(units)): a, b = units[random.randrange(len(units))]; n += a; k += b
        v.append(100 * k / n if n else 0)
    v.sort(); return [round(v[100], 2), round(v[1899], 2)]
for p in POETS: res[p] = ci(list(st[p].values()))
for g in GROUPS: res[g] = ci([u for p in POETS if per[p] == g for u in st[p].values()])
res['all'] = ci([u for p in POETS for u in st[p].values()])
json.dump(res, open(os.path.join(out, 'boot.json'), 'w'), indent=0)
S = json.load(open(os.path.join(out, 'score.json')))
for g in GROUPS + ['all']: print('%-6s M %.2f  (%.2f to %.2f)' % (g, (S['groups'][g] if g != 'all' else S['all'])['M'], *res[g]))
print(' | '.join('%s %.1f (%.1f-%.1f)' % (p, S['poets'][p]['M'], *res[p]) for p in sorted(POETS, key=lambda p: S['poets'][p]['M'])))
