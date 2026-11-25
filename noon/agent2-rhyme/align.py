# align.py -- the verse lines of each annotated stanza, found in the corpus's raw files.   python -I align.py RAW_DIR corpus.json OUT.json
# A raw file is AUTHOR / TITLE / RHYME lines and blocks of verse; the gold stanzas come from it in order.  Each gold stanza is
# matched to the next raw block whose end-words, cleaned in the same way, are the gold stanza's words.
import sys, os, json, re
raw, corpus, out = sys.argv[1], json.load(open(sys.argv[2], encoding='utf-8')), sys.argv[3]
def endword(line):
    t = re.sub(r"[^A-Za-z'\- ]", ' ', line).split()
    while t and not re.search('[A-Za-z]', t[-1]): t.pop()
    return re.sub(r"[^a-z]", '', t[-1].lower()) if t else ''
res = {}; tot = match = 0
for poet, r in corpus.items():
    blocks = []; cur = []; title = ''; titles = []
    for l in open(os.path.join(raw, poet + '.txt'), encoding='utf-8', errors='replace').read().split('\n'):
        s = l.strip()
        if s.startswith('TITLE'): title = s[5:].strip()
        if s == '' or s.startswith(('AUTHOR', 'TITLE', 'RHYME')):
            if cur: blocks.append((cur, title)); cur = []
            continue
        cur.append(re.sub(r'\s+', ' ', s))
    if cur: blocks.append((cur, title))
    ends = [tuple(endword(x) for x in b[0]) for b in blocks]
    pos = 0; lines = []
    for s in r['stanzas']:
        want = tuple(re.sub(r"[^a-z]", '', w.lower()) for w in s['words']); found = None
        for k in range(pos, min(pos + 60, len(blocks))):
            if ends[k] == want: found = k; break
        tot += 1
        if found is None: lines.append(None)
        else: lines.append({'lines': blocks[found][0], 'title': blocks[found][1]}); pos = found + 1; match += 1
    res[poet] = lines
    print('%-11s stanzas %5d  matched to their verses %5d' % (poet, len(r['stanzas']), sum(1 for x in lines if x)))
json.dump(res, open(out, 'w', encoding='utf-8'))
print('all: %d of %d stanzas matched' % (match, tot))
