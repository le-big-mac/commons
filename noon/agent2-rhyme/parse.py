# parse.py -- the Chicago Rhyming Poetry Corpus's gold files into rhyme pairs.   python -I parse.py GOLD_DIR RAW_DIR OUT.json
# A gold file is blocks of three lines: "POEMn w1 w2 ...", the stanza's rhyme scheme, and the scheme in the context of the poem.
# Pairs: every two end-words of a stanza that carry the same number in the stanza's own scheme (the first scheme line).
import sys, os, json, re, collections
gold, raw, out = sys.argv[1], sys.argv[2], sys.argv[3]
PERIODS = {}
for f in sorted(os.listdir(raw)):
    if f.endswith('.authors'):
        for a in open(os.path.join(raw, f), encoding='utf-8').read().split(): PERIODS[a] = f[:-8]
res = {}
for a in sorted(PERIODS):
    lines = open(os.path.join(gold, a + '.pgold'), encoding='utf-8', errors='replace').read().split('\n')
    blocks, cur = [], []
    for l in lines:
        if l.strip() == '':
            if cur: blocks.append(cur); cur = []
        else: cur.append(l.strip())
    if cur: blocks.append(cur)
    stanzas = []; bad = 0
    for b in blocks:
        if len(b) != 3 or not b[0].startswith('POEM'): bad += 1; continue
        head = b[0].split(); words = head[1:]; s1 = b[1].split(); s2 = b[2].split()
        if len(words) != len(s1) or len(words) != len(s2): bad += 1; continue
        stanzas.append({'poem': int(head[0][4:]), 'words': words, 'scheme': [int(x) for x in s1], 'inpoem': [int(x) for x in s2]})
    name = ''
    rp = os.path.join(raw, a + '.txt')
    if os.path.exists(rp):
        m = re.search(r'^AUTHOR\s+(.*)$', open(rp, encoding='utf-8', errors='replace').read(), re.M); name = m.group(1).strip() if m else ''
    res[a] = {'period': PERIODS[a], 'name': name, 'stanzas': stanzas, 'bad_blocks': bad}
json.dump(res, open(out, 'w', encoding='utf-8'))
for a, r in res.items():
    n = sum(len(s['words']) for s in r['stanzas']); pairs = 0
    for s in r['stanzas']:
        c = collections.Counter(s['scheme']); pairs += sum(k * (k - 1) // 2 for k in c.values())
    print('%-11s %-5s %-28s stanzas %5d  lines %6d  pairs %6d  poems %4d  bad blocks %d' % (a, r['period'], r['name'][:28], len(r['stanzas']), n, pairs, len({s['poem'] for s in r['stanzas']}), r['bad_blocks']))
