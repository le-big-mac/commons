# verdicts.py -- the fourteen sealed lines against the scores.   python -I verdicts.py OUT_DIR
import sys, os, json, csv, hashlib, collections
here = os.path.dirname(os.path.abspath(__file__)); out = sys.argv[1]
S = json.load(open(os.path.join(out, 'score.json'))); rows = list(csv.DictReader(open(os.path.join(out, 'pairs.tsv'), encoding='utf-8'), delimiter='\t'))
G = S['groups']; P = S['poets']; order = ['1415', '1516', '1617', '1718', '1819']
print('sha256 of expectations.md:', hashlib.sha256(open(os.path.join(here, 'expectations.md'), 'rb').read()).hexdigest()); print()
V = []
def line(n, kind, odds, held, what): V.append((n, kind, odds, held)); print('%2d. %-5s (%s, odds %.2f)  %s' % (n, 'HELD' if held else 'FELL', kind, odds, what))
ev = lambda sel: sum(1 for r in rows if r['ev'] == '1' and sel(r))
big = [p for p in P if P[p]['evaluable'] >= 1000]
line(1, 'read', 0.75, 76 <= S['all']['M_A'] <= 86, 'M_A for the whole corpus: %.2f%% (sealed: between 76 and 86)' % S['all']['M_A'])
line(2, 'read', 0.70, 86 <= G['1819']['M_B'] <= 94, 'M_B for the 1819 group: %.2f%% (sealed: between 86 and 94)' % G['1819']['M_B'])
Ms = [G[g]['M'] for g in order]
line(3, 'guessed', 0.70, Ms[4] == max(Ms), 'M by group, 1415 to 1819: ' + ', '.join('%.2f' % m for m in Ms) + ' (sealed: 1819 highest)')
line(4, 'guessed', 0.55, Ms[0] == min(Ms), 'the same figures (sealed: 1415 lowest)')
line(5, 'guessed', 0.30, all(Ms[i] <= Ms[i + 1] for i in range(4)), 'the same figures (sealed: never falling from one group to the next)')
def ea_ay(r):
    if r['ev'] != '1' or r['ok'] != '0' or r['cls'] != 'ey~iy': return False
    w = r['k1'] if r['v1'] == 'iy' else r['k2']; return 'ea' in w
rate = {p: 1000 * sum(1 for r in rows if r['poet'] == p and ea_ay(r)) / P[p]['evaluable'] for p in P}
top = sorted(big, key=lambda p: -rate[p])
line(6, 'read', 0.50, top[0] == 'swift', 'ea-ay pairs per thousand evaluable, poets with at least 1,000 evaluable: ' + ', '.join('%s %.1f' % (p, rate[p]) for p in top[:6]) + ' (sealed: Swift first)')
nm = sum(1 for r in rows if r['poet'] == 'milton' and ea_ay(r))
line(7, 'read', 0.60, nm == 0, 'Milton: %d ea-ay pairs in %d evaluable (sealed: none)' % (nm, P['milton']['evaluable']))
oi = collections.Counter(r['poet'] for r in rows if r['ev'] == '1' and r['ok'] == '0' and r['cls'] == 'ay~oy'); oi19 = sum(1 for r in rows if r['period'] == '1819' and r['ev'] == '1' and r['ok'] == '0' and r['cls'] == 'ay~oy')
line(8, 'read+guessed', 0.50, all(oi[p] >= 1 for p in ('dryden', 'pope', 'swift')) and oi19 == 0, 'join/line pairs: Dryden %d, Pope %d, Swift %d; in the 1819 group %d; all poets: %s (sealed: at least one each, none in 1819)' % (oi['dryden'], oi['pope'], oi['swift'], oi19, ', '.join('%s %d' % x for x in oi.most_common())))
LOVE = {'love', 'loves', 'loved', 'above', 'dove', 'doves', 'glove', 'gloves'}; MOVE = {'move', 'moves', 'moved', 'prove', 'proves', 'proved', 'remove', 'removes', 'removed', 'approve', 'approved', 'improve', 'improved', 'reprove', 'reproved'}
def lm(r):
    a, b = r['k1'] or r['w1'], r['k2'] or r['w2']; return (a in LOVE and b in MOVE) or (b in LOVE and a in MOVE)
c19 = sum(1 for r in rows if r['period'] == '1819' and lm(r)); c16 = sum(1 for r in rows if r['period'] == '1516' and lm(r)); r19 = 1000 * c19 / G['1819']['evaluable']; r16 = 1000 * c16 / G['1516']['evaluable']
line(9, 'guessed', 0.50, c19 >= 3 and r19 < r16 / 2, 'love/move pairs: %d in the 1819 group (%.2f per thousand evaluable), %d in the 1516 group (%.2f per thousand); by group: %s (sealed: at least three in 1819, and under half the 1516 rate)' % (c19, r19, c16, r16, ', '.join('%s %d' % (g, sum(1 for r in rows if r['period'] == g and lm(r))) for g in order)))
cl = [c for c in S['classes'] if c[0] != 'same vowel']
line(10, 'guessed', 0.40, cl[0][0] == 'ay~iy', 'commonest classes of failing pair with two different last vowels: ' + ', '.join('%s %d' % tuple(c) for c in cl[:5]) + ' (sealed: ay~iy first)')
d = S['all']['M_A'] - S['all']['M_A1']
line(11, 'guessed', 0.50, 1 <= d <= 5, 'M_A %.2f, M_A1 %.2f: %.2f points (sealed: between 1 and 5)' % (S['all']['M_A'], S['all']['M_A1'], d))
d = G['1819']['M_B'] - G['1819']['M_A']
line(12, 'guessed', 0.60, d >= 1, '1819 group: M_B %.2f, M_A %.2f: %+.2f points (sealed: B above A by at least 1)' % (G['1819']['M_B'], G['1819']['M_A'], d))
low = sorted(big, key=lambda p: P[p]['M'])
line(13, 'guessed', 0.55, low[0] in ('spenser', 'swift', 'shelley'), 'lowest M among poets with at least 1,000 evaluable: ' + ', '.join('%s %.2f' % (p, P[p]['M']) for p in low[:5]) + ' (sealed: Spenser, Swift or Shelley)')
g16 = G['1516']['M_A'] - G['1516']['M_Along']; g19 = G['1819']['M_A'] - G['1819']['M_Along']
line(14, 'guessed', 0.75, g16 > g19, 'short stem less long stem in A: 1516 group %.2f points, 1819 group %.2f points (sealed: more in 1516)' % (g16, g19))
h = sum(1 for v in V if v[3]); print('\n%d of %d held.' % (h, len(V)))
for k in ('read', 'guessed', 'read+guessed'): print('  %s: %d of %d' % (k, sum(1 for v in V if v[1] == k and v[3]), sum(1 for v in V if v[1] == k)))
print('  mean squared error of the odds (Brier): %.3f; had every line been given 0.5: 0.250' % (sum((v[2] - v[3]) ** 2 for v in V) / len(V)))
