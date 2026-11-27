"""Evidence reading 1: the Spanish column of the big table of "Letter frequency" in the two revisions compared and
in the nineteen sampled older revisions.  My own parser (not letterfreq.py); the wikitext is read as text only.
usage: python -I ev1_letters.py NOW.wiki OLD2022.wiki HISTORYDIR"""
import sys, re, os

def spanish(path):
    t = open(path, encoding='utf-8').read()
    # the table whose header row has both Spanish and Czech (the big table of other languages)
    best = None
    for m in re.finditer(r'\{\|.*?\n\|\}', t, flags=re.S):
        blk = m.group(0)
        if 'Spanish' in blk and 'Icelandic' in blk and 'Turkish' in blk: best = blk
    if best is None: return None
    rows = re.split(r'\n\|-', best)
    # header cells: lines starting with '!'
    heads = []
    for r in rows:
        hs = [l for l in r.split('\n') if l.startswith('!')]
        if hs and any('Spanish' in l for l in hs):
            for l in hs:
                for cell in re.split(r'!!', l.lstrip('!')):
                    heads.append(cell)
            break
    names = []
    for h in heads:
        mm = re.findall(r'\[\[([^\]|]*)(?:\|([^\]]*))?\]\]', h)
        names.append((mm[0][1] or mm[0][0]) if mm else h.strip())
    k = [i for i, n in enumerate(names) if n.strip() == 'Spanish']
    if len(k) != 1: return None
    k = k[0]                                  # index among header cells; first header cell is "Letter"
    total = 0.0; n = 0; vals = {}
    for r in rows:
        lines = [l for l in r.strip().split('\n') if l.startswith('|') and not l.startswith('|}') and not l.startswith('|+')]
        if len(lines) < 2: continue
        letter = re.sub(r"'''", '', lines[0].lstrip('|')).strip()
        cells = []
        for l in lines[1:]: cells += [c.strip() for c in l.lstrip('|').split('||')]
        if k - 1 >= len(cells): continue
        c = re.sub(r'<ref.*', '', cells[k - 1]); c = re.sub(r'\{\{.*?\}\}|<!--.*?-->', '', c)
        mm = re.search(r'\d+(?:\.\d+)?', c.replace('~0', '0'))
        v = float(mm.group(0)) if mm else 0.0
        vals[letter] = v; total += v; n += 1
    return total, n, vals, names

now = spanish(sys.argv[1]); old = spanish(sys.argv[2])
print('revision compared (20 November 2026): Spanish sums to %.3f over %d rows; columns %d' % (now[0], now[1], len(now[3]) - 1))
print('revision of 25 December 2022:         Spanish sums to %.3f over %d rows; columns %d' % (old[0], old[1], len(old[3]) - 1))
ch = [(L, old[2][L], now[2][L]) for L in now[2] if L in old[2] and abs(old[2][L] - now[2][L]) > 1e-9]
print('Spanish cells that differ:', '; '.join('%s %.3f -> %.3f' % c for c in ch), '| number', len(ch), '| net %+.3f' % sum(c[2] - c[1] for c in ch))
print('\nthe sampled older revisions (directory name = revision number), in order of number:')
ds = sorted((int(d.split('_')[1]), d) for d in os.listdir(sys.argv[3]) if d.startswith('rev_'))
print('number of sampled revisions on disk:', len(ds))
last100 = None
for rid, d in ds:
    r = spanish(os.path.join(sys.argv[3], d, 'page.wiki'))
    if r is None: print('  %d  (table not found)' % rid); continue
    ok = abs(r[0] - 100) < 0.0005
    if ok: last100 = rid
    print('  %d  Spanish %.3f %s' % (rid, r[0], '<-- adds up' if ok else ''))
print('latest sampled revision in which the Spanish column sums to 100.000:', last100)
