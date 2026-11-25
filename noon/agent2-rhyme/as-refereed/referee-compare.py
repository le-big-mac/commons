# referee-compare.py -- my program's answers to the questions of the referee's blind step (which allows no respelling), from the
# pair table.   python -I referee-compare.py DATA_DIR
import sys, os, csv, json, collections
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import rhyme as R, words as W
rows = list(csv.DictReader(open(os.path.join(here, 'out', 'pairs.tsv'), encoding='utf-8'), delimiter='\t')); J = R.Judge(sys.argv[1])
c = json.load(open(os.path.join(here, 'corpus.json'))); print('A. stanzas', sum(len(r['stanzas']) for r in c.values()), 'refused', sum(r['bad_blocks'] for r in c.values()), 'pairs', len(rows))
xa = lambda r: r['as'] != '' and r['ka'] == r['w1'] and r['ka2'] == r['w2']; xb = lambda r: r['bs'] != '' and r['kb'] == r['w1'] and r['kb2'] == r['w2']
def share(rs, ex, key): rs = [r for r in rs if ex(r)]; return '%.2f%% of %d' % (100 * sum(1 for r in rs if r[key] == '1') / len(rs), len(rs))
for name, ex, key in (('B. American', xa, 'as'), ('C. British', xb, 'bs')):
    print(name, 'all', share(rows, ex, key), '|', ' | '.join('%s %s' % (p, share([r for r in rows if r['poet'] == p], ex, key)) for p in ['pope', 'prior', 'shelley', 'housman', 'shakespeare']))
def either(rs):
    ev = [r for r in rs if xa(r) or xb(r)]; return '%.2f%% of %d' % (100 * sum(1 for r in ev if (xa(r) and r['as'] == '1') or (xb(r) and r['bs'] == '1')) / len(ev), len(ev))
print('D. either: all', either(rows), '|', ' | '.join('%s %s' % (g, either([r for r in rows if r['period'] == g])) for g in ['1415', '1516', '1617', '1718', '1819']))
both = [r for r in rows if xa(r) and xb(r) and r['as'] == '0' and r['bs'] == '0']
print('E.', ', '.join('%s %d' % x for x in collections.Counter('/'.join(sorted([r['w1'], r['w2']])) for r in both).most_common(15)))
for p in ['swift', 'finch', 'prior', 'pope', 'dryden']:
    out = []
    for r in rows:
        if r['poet'] != p or not (xa(r) or xb(r)) or (xa(r) and r['as'] == '1') or (xb(r) and r['bs'] == '1'): continue
        v = {}
        for w in (r['w1'], r['w2']):
            x = J.word(w); v[w] = set(s[0] for s in (x['sb'] or [])) | set({'IY': 'iy', 'EY': 'ey'}.get(s[0], s[0]) for s in (x['sa'] or []))
        a, b = r['w1'], r['w2']
        for s, t in ((a, b), (b, a)):
            if 'iy' in v[s] and 'ey' in v[t] and 'ea' in s and 'ea' not in t: out.append(s + '/' + t); break
    print('F.', p, len(out), ' '.join(out))
n = sh = lg = 0
def penult(w):
    for pr in J.A[w]:
        v = [s for ph, s in pr if s is not None]
        if len(v) < 2 or v[-2] != 1 or v[-1] == 1: return False
    return True
for r in rows:
    if xa(r) and penult(r['w1']) and penult(r['w2']): n += 1; sh += r['as'] == '1'; lg += r['al'] == '1'
print('G. double pairs %d; match from the last vowel %.2f%%; from the stressed vowel %.2f%%' % (n, 100 * sh / n, 100 * lg / n))
