# make-data.py -- everything the page shows, in one JSON.   python -I make-data.py DATA_DIR OUT_DIR corpus.json data.json
# No pronunciation from BEEP goes into the page (it is for research use only): verdicts and my own family names do; the endings
# shown for a failing pair are from the Carnegie Mellon dictionary alone.
import sys, os, csv, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rhyme as R, words as W
from poets import POETS, GROUPS
data, out, corpus, dest = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3], encoding='utf-8')), sys.argv[4]
S = json.load(open(os.path.join(out, 'score.json'))); B = json.load(open(os.path.join(out, 'boot.json'))); F = json.load(open(os.path.join(out, 'families.json')))
V = json.load(open(os.path.join(out, 'verses.json'), encoding='utf-8'))
rows = list(csv.DictReader(open(os.path.join(out, 'pairs.tsv'), encoding='utf-8'), delimiter='\t'))
fam = {(r['poet'], r['stanza'], r['i'], r['j']): r['family'] for r in csv.DictReader(open(os.path.join(out, 'fails.tsv'), encoding='utf-8'), delimiter='\t')}
J = R.Judge(data)
RESPELL = {'IY': 'ee', 'IH': 'i', 'EY': 'ay', 'EH': 'e', 'AE': 'a', 'AA': 'ah', 'AO': 'aw', 'OW': 'oh', 'UH': 'uu', 'UW': 'oo', 'AH': 'u', 'ER': 'er', 'AY': 'eye', 'AW': 'ow', 'OY': 'oy',
           'CH': 'ch', 'JH': 'j', 'TH': 'th', 'DH': 'dh', 'SH': 'sh', 'ZH': 'zh', 'HH': 'h', 'NG': 'ng', 'Y': 'y'}
def ending(stem): return '-'.join([RESPELL[stem[0]]] + ([''.join(RESPELL.get(p, p.lower()) for p in stem[1:])] if len(stem) > 1 else []))
def endings(w1, w2):
    """the two endings in the American dictionary that come nearest to rhyming, respelt; ('', '') if a word is not in it"""
    x, y = J.word(w1), J.word(w2)
    if not x['a'] or not y['a'] or x['ra'].startswith('old') or y['ra'].startswith('old'): return '', ''
    cost = lambda a, b: 4 * (a[1:] != b[1:]) + (a[0] != b[0])
    a, b = min(((a, b) for a in x['sa'] for b in y['sa']), key=lambda ab: cost(*ab)); return ending(a), ending(b)
order = sorted(POETS, key=lambda p: (POETS[p][1] or 1566, p)); pidx = {p: i for i, p in enumerate(order)}
D = {'poets': [], 'groups': [], 'families': [], 'all': None}
keys = ['pairs', 'evaluable', 'M', 'M_A', 'M_B', 'M_Along', 'M_A1', 'nA', 'nB', 'old_not_evaluable', 'unknown']
for p in order:
    m = S['poets'][p]; D['poets'].append({'id': p, 'name': POETS[p][0], 'born': POETS[p][1], 'group': corpus[p]['period'], 'lo': B[p][0], 'hi': B[p][1], **{k: m[k] for k in keys}})
for g in GROUPS: m = S['groups'][g]; D['groups'].append({'id': g, 'lo': B[g][0], 'hi': B[g][1], **{k: m[k] for k in keys}})
D['all'] = {'lo': B['all'][0], 'hi': B['all'][1], **{k: S['all'][k] for k in keys}}
for f in F['order']:
    D['families'].append({'name': f, 'total': F['total'][f], 'byPoet': [F['by_poet'][f][p][0] for p in order], 'byGroup': [F['by_group'][f][g][0] for g in GROUPS], 'top': F['top'][f][:8]})
lines = []; lidx = {}; titles = []; tidx = {}
import re
def tidy(s):
    """for showing only: a line number at the head of a line and note numbers stuck to words are taken off (the corpus's texts carry some)"""
    s = re.sub(r'\[\d+\]', '', s); s = re.sub(r'^\d+\s+(?=[A-Za-z\'"])', '', s); s = re.sub(r'\s+\d+$', '', s); return re.sub(r'(?<=[A-Za-z,;:.!?])\d+', '', s).strip()
def L(s):
    s = tidy(s)
    if s not in lidx: lidx[s] = len(lines); lines.append(s)
    return lidx[s]
def T(s):
    if s not in tidx: tidx[s] = len(titles); titles.append(s)
    return tidx[s]
fidx = {f: i for i, f in enumerate(F['order'])}; fails = []; noverse = 0
for r in rows:
    if r['ev'] != '1' or r['ok'] != '0': continue
    v = V[r['poet']][int(r['stanza'])]; e1, e2 = endings(r['w1'], r['w2'])
    if v is None: noverse += 1; l1 = l2 = -1; t = -1
    else: l1, l2, t = L(v['lines'][int(r['i'])]), L(v['lines'][int(r['j'])]), T(v['title'])
    fails.append([pidx[r['poet']], fidx[fam[(r['poet'], r['stanza'], r['i'], r['j'])]], r['w1'], r['w2'], l1, l2, t, e1, e2])
fails = [f for k, f in sorted(enumerate(fails), key=lambda kf: (kf[1][0], kf[0]))]                 # the oldest poet first, then as the corpus has them
D['fails'] = fails; D['lines'] = lines; D['titles'] = titles
# every distinct pair of rhyme words: how often, by which poets, and whether it still rhymes (1), does not (0), or cannot be judged (2)
agg = {}
for r in rows:
    k = tuple(sorted([r['w1'], r['w2']])); a = agg.setdefault(k, [0, set(), 2])
    a[0] += 1; a[1].add(pidx[r['poet']])
    if r['ev'] == '1': a[2] = int(r['ok'])
wl = sorted({w for k in agg for w in k}); widx = {w: i for i, w in enumerate(wl)}
D['words'] = wl; D['pairs'] = [[widx[a], widx[b], n, ok, ''.join('0123456789abcdefghijklmnopqrstuv'[i] for i in sorted(ps))] for (a, b), (n, ps, ok) in sorted(agg.items())]
D['counts'] = {'pairs': len(rows), 'evaluable': S['all']['evaluable'], 'failing': len(fails), 'failing_without_verse': noverse, 'distinct_pairs': len(agg), 'words': len(wl), 'stanzas': sum(len(c['stanzas']) for c in corpus.values())}
json.dump(D, open(dest, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('data.json: %d bytes; poets %d, families %d, failing pairs %d (%d without their verses), lines %d, titles %d, words %d, distinct pairs %d' % (os.path.getsize(dest), len(D['poets']), len(D['families']), len(fails), noverse, len(lines), len(titles), len(wl), len(agg)))
ex = [f for f in fails if {f[2], f[3]} == {'obey', 'tea'}]; print('obey/tea:', ex[0], '|', lines[ex[0][4]], '|', lines[ex[0][5]])
