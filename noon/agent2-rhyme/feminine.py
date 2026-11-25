# feminine.py -- an after-check, not sealed.  The main measure compares the last vowel and what follows, so a rhyme on two
# syllables (nature : creature) is judged on its unstressed ending alone.  Here, in the American dictionary (the one with stress):
# a pair is "double" if every listed pronunciation of both words has its primary stress on the last syllable but one; a double
# pair is asked to agree from the stressed vowel on; every other pair as before.   python -I feminine.py DATA_DIR corpus.json OUT_DIR
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rhyme as R, words as W
from poets import POETS, GROUPS
data, corpus, out = sys.argv[1], json.load(open(sys.argv[2], encoding='utf-8')), sys.argv[3]
J = R.Judge(data)
def penult(w):
    x = J.word(w)
    if not x['a'] or x['ra'].startswith('old'): return None
    ok = True
    for p in J.A[x['a']]:
        v = [s for ph, s in p if s is not None]
        if len(v) < 2 or v[-2] != 1 or v[-1] == 1: ok = False
    return ok
tot = collections.defaultdict(lambda: collections.Counter()); ex = collections.Counter()
for poet, r in corpus.items():
    for s in r['stanzas']:
        ws, sc = s['words'], s['scheme']
        for i in range(len(ws)):
            for j in range(i + 1, len(ws)):
                if sc[i] != sc[j]: continue
                p = J.pair(ws[i], ws[j])
                if p['as'] is None or p['olda']: continue
                dbl = penult(ws[i]) and penult(ws[j])
                for key in (poet, r['period'], 'all'):
                    t = tot[key]; t['n'] += 1; t['short'] += p['as']; t['double'] += bool(dbl)
                    if dbl: t['double_short'] += p['as']; t['double_long'] += p['al']
                    t['strict'] += (p['al'] if dbl else p['as'])
                if dbl and p['as'] and not p['al']: ex['/'.join(sorted([W.normal(ws[i]), W.normal(ws[j])]))] += 1
res = {k: dict(v) for k, v in tot.items()}; json.dump({'tot': res, 'hidden': ex.most_common(60)}, open(os.path.join(out, 'feminine.json'), 'w'), indent=0)
print('%-8s %7s %7s %8s | %7s %12s %12s | %s' % ('', 'in A', 'M_A', 'double', 'share', 'pass ending', 'pass in full', 'M_A with double rhymes judged in full'))
for k in ['all'] + GROUPS:
    t = tot[k]; print('%-8s %7d %6.2f%% %8d | %6.2f%% %11.2f%% %11.2f%% | %6.2f%%' % (k, t['n'], 100 * t['short'] / t['n'], t['double'], 100 * t['double'] / t['n'], 100 * t['double_short'] / max(1, t['double']), 100 * t['double_long'] / max(1, t['double']), 100 * t['strict'] / t['n']))
print('\ndouble rhymes that pass on their endings and fail in full (%d pairs, %d different): %s' % (sum(ex.values()), len(ex), ', '.join('%s %d' % x for x in ex.most_common(40))))
print('\nby poet, drop in M_A when double rhymes are judged in full: ' + ', '.join('%s %.1f' % (p, 100 * (tot[p]['short'] - tot[p]['strict']) / tot[p]['n']) for p in sorted(POETS, key=lambda p: -(tot[p]['short'] - tot[p]['strict']) / tot[p]['n'])[:12]))
