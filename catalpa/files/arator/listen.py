# The listening piece: scans of the Aeneid and Arator line by line (and Juvencus, for the widest pair), from the same sixteen-poem lexicon as late2_run.py.
# Writes listen_scans.json: for each line its text, the scanner's pattern of five feet, how it was scanned, the lengths of its syllables, the word each syllable belongs to,
# and (for the Aeneid) the reference's pattern.   Run:  python3 -I listen.py
import sys, glob, re, collections, json; sys.path.insert(0, '/home/agent1/arator')
import scan, gold, arator, latinlib, late2
ORDER = ['aen', 'geo', 'met', 'lucan', 'thebaid', 'achilleid', 'vflaccus', 'juvenal']
NEW = ['juvencus', 'ausonius', 'prudentius', 'dracontius', 'corippus']
G = {}; BOOK = {}
for name in ORDER:
    files = sorted(glob.glob(f'/home/agent1/arator/gold/{name}[0-9]*.html'), key=lambda x: int(re.search(r'(\d+)\.html$', x).group(1)))
    G[name] = []; BOOK[name] = []
    for f in files:
        g = gold.load(f); G[name] += g; BOOK[name] += [(int(re.search(r'(\d+)\.html$', f).group(1)), i + 1) for i in range(len(g))]
A = arator.load(); LATE = latinlib.late()
T = collections.OrderedDict()
for name in ORDER: T[name] = [g['text'] for g in G[name]]
T['arator'] = [ln for b, ln in A]
for name, L in LATE.items(): T[name] = L
for name in NEW[:4]: T[name] = late2.load(name)
voc = late2.vocabulary([ln for L in T.values() for ln in L]); rep = {}
T['corippus'] = late2.restore_v(late2.load('corippus'), voc, rep)
lines = [ln for L in T.values() for ln in L]; owner = [name for name, L in T.items() for _ in L]
print(len(lines), 'lines in all'); sys.stdout.flush()
lex, scans = scan.learn(lines, rounds=4, verbose=True)
S = collections.defaultdict(list)
for o, sc in zip(owner, scans): S[o].append(sc)
out = {}
for name in ('aen', 'arator', 'juvencus'):
    rows = []
    for i, (ln, sc) in enumerate(zip(T[name], S[name])):
        r = dict(text=ln, pat=None, how='fail')
        if sc and sc.get('pat'):
            r.update(pat=''.join(sc['pat']), how=sc['how'], q=''.join(sc['q']), w=[s.w for s in sc['syls']], k=[s.k for s in sc['syls']], words=sc['words'], n_ok=sc['n_ok'], margin=round(sc['margin'], 2))
        if name == 'aen': r['ref'] = G['aen'][i]['pat']; r['book'], r['line'] = BOOK['aen'][i]
        if name == 'arator': r['book'] = A[i][0]
        rows.append(r)
    out[name] = rows
    ok = [r for r in rows if r['pat']]
    print(name, len(rows), 'lines;', len(ok), 'scanned;', sum(1 for r in ok if r['how'] == 'plain'), 'plain; dactyls in feet 1-4:', round(100 * sum(r['pat'][:4].count('D') for r in ok) / (4 * len(ok)), 2))
json.dump(out, open('/home/agent1/arator/listen_scans.json', 'w'), ensure_ascii=False)
print('written')
