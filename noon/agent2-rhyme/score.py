# score.py -- every rhyme pair of the corpus judged in the two dictionaries.   python -I score.py DATA_DIR corpus.json OUT_DIR
# Writes OUT_DIR/pairs.tsv (one line a pair) and OUT_DIR/score.json (the tables), and prints the tables.
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rhyme as R, words as W
from poets import POETS, GROUPS
data, corpus, out = sys.argv[1], json.load(open(sys.argv[2], encoding='utf-8')), sys.argv[3]
J = R.Judge(data)
A2B = {'IY': 'iy', 'IH': 'ih', 'EY': 'ey', 'EH': 'eh', 'AE': 'ae', 'AA': 'aa', 'AO': 'ao', 'OW': 'ow', 'UH': 'uh', 'UW': 'uw', 'AH': 'ah', 'ER': 'er', 'AY': 'ay', 'AW': 'aw', 'OY': 'oy'}
def last_vowel(w):
    """the last vowel of a word in B's symbols (from B if the word is found there without an old respelling, else from A), by its first-listed pronunciation"""
    x = J.word(w)
    if x['b'] and not x['rb'].startswith('old'): return x['sb'][0][0], tuple(x['sb'][0][1:]), x['b']
    if x['a'] and not x['ra'].startswith('old'): return A2B[x['sa'][0][0]], tuple(p.lower() for p in x['sa'][0][1:]), x['a']
    return None, None, None
def stems(w):
    """every stem of a word in B's symbols (from B if found there without an old respelling, else from A) with, where A knows the word, whether its last vowel is stressed there"""
    x = J.word(w); st = None
    if x['a'] and not x['ra'].startswith('old'): st = max(s for p in J.A[x['a']][:1] for ph, s in p[-len(R.short_a(p)):][:1])
    if x['b'] and not x['rb'].startswith('old'): return [(s[0], tuple(s[1:])) for s in x['sb']], x['b'], st
    if x['a'] and not x['ra'].startswith('old'): return [(A2B[s[0]], tuple(p.lower() for p in s[1:])) for s in x['sa']], x['a'], st
    return [], None, st
def best(w1, w2):
    """for a failing pair: the two stems, one of each word, that are nearest (same consonants after the vowel if any two have; full vowels before the weak one)"""
    s1, k1, t1 = stems(w1); s2, k2, t2 = stems(w2)
    if not s1 or not s2: return None
    cost = lambda a, b: 4 * (a[1] != b[1]) + 2 * ((a[0] == 'ax') + (b[0] == 'ax')) + (a[0] != b[0])
    a, b = min(((a, b) for a in s1 for b in s2), key=lambda ab: cost(*ab)); return a, b, k1, k2, t1, t2
rows = []
for poet, r in corpus.items():
    for si, s in enumerate(r['stanzas']):
        ws, sc = s['words'], s['scheme']
        for i in range(len(ws)):
            for j in range(i + 1, len(ws)):
                if sc[i] != sc[j]: continue
                p = J.pair(ws[i], ws[j]); ea = p['as'] is not None and not p['olda']; eb = p['bs'] is not None and not p['oldb']
                adjacent = not any(sc[k] == sc[i] for k in range(i + 1, j))
                ev = ea or eb; ok = (ea and p['as']) or (eb and p['bs'])
                cls = ''; (v1, c1, k1), (v2, c2, k2) = last_vowel(ws[i]), last_vowel(ws[j])
                if ev and not ok: cls = '%s~%s' % tuple(sorted([v1, v2])) if v1 != v2 else 'same vowel'
                cls2 = ''; u1 = u2 = ''; d1 = d2 = ''; t1 = t2 = None
                if ev and not ok:
                    a, b, kk1, kk2, t1, t2 = best(ws[i], ws[j]); u1, u2 = a[0], b[0]; d1, d2 = ' '.join(a[1]), ' '.join(b[1])
                    cls2 = '%s~%s' % tuple(sorted([u1, u2])) if u1 != u2 else 'same vowel'
                rows.append({'poet': poet, 'period': r['period'], 'stanza': si, 'i': i, 'j': j, 'w1': W.normal(ws[i]), 'w2': W.normal(ws[j]), 'adjacent': adjacent,
                             'ea': ea, 'as': p['as'], 'al': p['al'], 'a1': p['a1'], 'eb': eb, 'bs': p['bs'], 'olda': p['olda'], 'oldb': p['oldb'], 'ev': ev, 'ok': bool(ok), 'cls': cls, 'cls2': cls2, 'u1': u1, 'u2': u2, 'd1': d1, 'd2': d2, 't1': '' if t1 is None else t1, 't2': '' if t2 is None else t2, 'v1': v1 or '', 'v2': v2 or '', 'k1': k1 or '', 'k2': k2 or '',
                             'ka': J.word(ws[i])['a'], 'kb': J.word(ws[i])['b'], 'ka2': J.word(ws[j])['a'], 'kb2': J.word(ws[j])['b']})
os.makedirs(out, exist_ok=True)
cols = ['poet', 'period', 'stanza', 'i', 'j', 'w1', 'w2', 'adjacent', 'ea', 'as', 'al', 'a1', 'eb', 'bs', 'ev', 'ok', 'cls', 'cls2', 'u1', 'u2', 'd1', 'd2', 't1', 't2', 'v1', 'v2', 'k1', 'k2', 'olda', 'oldb', 'ka', 'ka2', 'kb', 'kb2']
with open(os.path.join(out, 'pairs.tsv'), 'w', encoding='utf-8') as f:
    f.write('\t'.join(cols) + '\n')
    for r in rows: f.write('\t'.join('' if r[c] is None else str(int(r[c])) if isinstance(r[c], bool) else str(r[c]) for c in cols) + '\n')
def measures(rs):
    n = len(rs); ev = [r for r in rs if r['ev']]; a = [r for r in rs if r['ea']]; b = [r for r in rs if r['eb']]; both = [r for r in rs if r['ea'] and r['eb']]
    pc = lambda k, m: round(100 * k / m, 4) if m else None
    return {'pairs': n, 'evaluable': len(ev), 'M': pc(sum(r['ok'] for r in ev), len(ev)), 'nA': len(a), 'M_A': pc(sum(r['as'] for r in a), len(a)), 'M_A1': pc(sum(r['a1'] for r in a), len(a)),
            'M_Along': pc(sum(r['al'] for r in a), len(a)), 'nB': len(b), 'M_B': pc(sum(r['bs'] for r in b), len(b)),
            'nBoth': len(both), 'M_both': pc(sum(r['as'] or r['bs'] for r in both), len(both)), 'M_A_both': pc(sum(r['as'] for r in both), len(both)), 'M_B_both': pc(sum(r['bs'] for r in both), len(both)),
            'M_adjacent': pc(sum(r['ok'] for r in ev if r['adjacent']), sum(1 for r in ev if r['adjacent'])),
            'old_not_evaluable': sum(1 for r in rs if not r['ev'] and (r['olda'] or r['oldb'])), 'unknown': sum(1 for r in rs if not r['ev'] and not (r['olda'] or r['oldb']))}
res = {'all': measures(rows), 'groups': {g: measures([r for r in rows if r['period'] == g]) for g in GROUPS}, 'poets': {p: measures([r for r in rows if r['poet'] == p]) for p in POETS}}
fails = [r for r in rows if r['ev'] and not r['ok']]
res['classes'] = collections.Counter(r['cls'] for r in fails).most_common()
res['classes2'] = collections.Counter(r['cls2'] for r in fails).most_common()
res['classes_by_group'] = {g: collections.Counter(r['cls'] for r in fails if r['period'] == g).most_common(12) for g in GROUPS}
json.dump(res, open(os.path.join(out, 'score.json'), 'w', encoding='utf-8'), indent=1)
hdr = '%-12s %6s %6s %6s | %6s %6s %6s %6s | %6s %6s | %6s %6s | %s' % ('', 'pairs', 'evalu.', 'M', 'n in A', 'M_A', 'M_A1', 'A long', 'n in B', 'M_B', 'adjac.', 'both', 'not evaluable: old spelling, unknown word')
def line(name, m): return '%-12s %6d %6d %6s | %6d %6s %6s %6s | %6d %6s | %6s %6s | %d, %d' % (name, m['pairs'], m['evaluable'], m['M'], m['nA'], m['M_A'], m['M_A1'], m['M_Along'], m['nB'], m['M_B'], m['M_adjacent'], m['M_both'], m['old_not_evaluable'], m['unknown'])
print(hdr); print(line('all', res['all']))
for g in GROUPS: print(line(g, res['groups'][g]))
print()
for p in sorted(POETS, key=lambda p: (POETS[p][1] or 1565, p)): print(line(p + ' ' + str(POETS[p][1] or '?')[-4:], res['poets'][p]) if False else line(p, res['poets'][p]) + '   b. ' + str(POETS[p][1] or '?'))
print('\nfailing pairs:', len(fails), 'of', res['all']['evaluable'], 'evaluable. Classes (by first-listed pronunciations, as sealed):', ', '.join('%s %d' % x for x in res['classes'][:40]))
print('\nClasses by the nearest pair of listed pronunciations:', ', '.join('%s %d' % x for x in res['classes2'][:40]))
for g in GROUPS: print(g, ':', ', '.join('%s %d' % x for x in res['classes_by_group'][g]))
