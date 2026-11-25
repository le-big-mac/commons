# mended.py -- an after-check prompted by the referee: the shares with the ruler's known leniencies taken out.  Nothing sealed is
# rescored by this; the scores of record are score.out.   python -I mended.py DATA_DIR corpus.json
# Taken out: four odd entries of the British dictionary (die as "d ay iy", none as "n ow n", wear as "w ia", put as "p ah t");
# old spellings that are other words' entries (pas, gras, doe, wast, bene) and nine wrong respellings, all made not judged;
# and, in a second figure, a word rhymed with itself.
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rhyme as R, words as W
from poets import POETS, GROUPS
data, corpus = sys.argv[1], json.load(open(sys.argv[2], encoding='utf-8'))
J = R.Judge(data)
ODD = {'die': ('iy',), 'none': ('ow', 'n'), 'wear': ('ia',), 'put': ('ah', 't')}                 # the stem of each odd entry, from its last vowel
for w, stem in ODD.items():
    before = len(J.B[w]); J.B[w] = [p for p in J.B[w] if R.short_b(p) != stem]; assert len(J.B[w]) == before - 1 and J.B[w], w
FALSE = {'pas', 'gras', 'doe', 'wast', 'bene', 'hond', 'mand', 'bost', 'uprist', 'limd', 'flead', 'brast', 'prowd', 'creast'}
tot = collections.defaultdict(collections.Counter)
for poet, r in corpus.items():
    for s in r['stanzas']:
        ws, sc = s['words'], s['scheme']
        for i in range(len(ws)):
            for j in range(i + 1, len(ws)):
                if sc[i] != sc[j]: continue
                a, b = W.normal(ws[i]), W.normal(ws[j]); p = J.pair(ws[i], ws[j])
                ea = p['as'] is not None and not p['olda']; eb = p['bs'] is not None and not p['oldb']
                ev0 = ea or eb; ok0 = (ea and p['as']) or (eb and p['bs'])
                ev = ev0 and a not in FALSE and b not in FALSE
                for key in (poet, r['period'], 'all'):
                    t = tot[key]; t['ev0'] += ev0; t['ok0'] += bool(ev0 and ok0); t['ev'] += ev; t['ok'] += bool(ev and ok0)
                    if ev and a != b: t['ev2'] += 1; t['ok2'] += bool(ok0)
print('%-10s %22s %24s %30s' % ('', 'odd entries taken out', 'and the false friends', 'and a word with itself'))
for k in ['all'] + GROUPS: t = tot[k]; print('%-10s %8.2f%% of %6d %12.2f%% of %6d %16.2f%% of %6d' % (k, 100 * t['ok0'] / t['ev0'], t['ev0'], 100 * t['ok'] / t['ev'], t['ev'], 100 * t['ok2'] / t['ev2'], t['ev2']))
low = sorted([p for p in POETS if tot[p]['ev2'] >= 1000], key=lambda p: tot[p]['ok2'] / tot[p]['ev2']); hi = sorted(POETS, key=lambda p: -tot[p]['ok2'] / tot[p]['ev2'])
print('lowest among poets with 1,000 judged, all three taken out: ' + ', '.join('%s %.2f' % (p, 100 * tot[p]['ok2'] / tot[p]['ev2']) for p in low[:4]) + '; highest: ' + ', '.join('%s %.2f' % (p, 100 * tot[p]['ok2'] / tot[p]['ev2']) for p in hi[:3]))
