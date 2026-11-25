"""study.py: the thirteen sealed lines of expectations.md scored from the per-book records, and the tables the write-up uses.
    /usr/bin/python3 -I study.py books   ->  study.out (printed), study.json"""
import collections, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import louis

UEB = 'en-ueb-g2.ctb'
SIGNS = {   # the 182 signs of Unified English Braille, by kind
    'letter-word': 'but can do every from go have just knowledge like more not people quite rather so that us very will it you as'.split(),
    'strong wordsign': 'child shall this which out still'.split(),
    'strong contraction': 'and for of the with'.split(),
    'strong groupsign': 'ch gh sh th wh ed er ou ow st ing ar'.split(),
    'lower wordsign': 'be enough were his in was'.split(),
    'lower groupsign': 'ea bb cc ff gg be con dis en in'.split(),
    'initial-letter': ('day ever father here know lord mother name one part question right some time under work young there character through where ought '
                       'upon word these those whose cannot had many spirit world their').split(),
    'final-letter': 'ound ance sion less ount ence ong ful tion ness ment ity'.split(),
    'shortform': ('about above according across after afternoon afterward again against almost already also although altogether always because before behind below '
                  'beneath beside between beyond blind braille children conceive conceiving could deceive deceiving declare declaring either first friend good great '
                  'herself him himself immediate its itself letter little much must myself necessary neither oneself ourselves paid perceive perceiving perhaps quick '
                  'receive receiving rejoice rejoicing said should such themselves thyself today together tomorrow tonight would your yourself yourselves').split(),
}
WORD_KINDS = ('letter-word', 'strong wordsign', 'lower wordsign')
LETTER_WORDS = [w for w in SIGNS['letter-word'] if w not in ('it', 'as')]      # the 21 whose word begins with the letter

def load(d):
    return [json.load(open(os.path.join(d, f))) for f in sorted(os.listdir(d)) if f.endswith('.json')]
def S(rec, code='ueb'): r = rec[code]; return (r['U'] - r['C']) / r['U']
def pool(recs, code='ueb'):
    """an era's books added together: units, words, cells, vocabulary"""
    by = collections.defaultdict(lambda: [0, 0]); vocab = collections.Counter(); U = C = W = 0
    for rec in recs:
        r = rec[code]; U += r['U']; C += r['C']; W += r['words']; vocab.update(r['vocab'])
        for k, v in r['by'].items(): by[k][0] += v[0]; by[k][1] += v[1]
    return dict(by=dict(by), vocab=vocab, U=U, C=C, words=W)
def per100k(p, label, what=1):
    """cells saved (what=1) or occurrences (what=0) per 100,000 words for one unit label such as 'which|w'"""
    return 1e5 * p['by'].get(label, [0, 0])[what] / p['words']
def occurs(p, sign, kind):
    """does this sign of UEB occur in the pooled books? (the sheet's rule)"""
    if kind in WORD_KINDS: return (sign + '|w') in p['by']
    if kind == 'shortform': return any(k.split('|')[0].startswith(sign) for k in p['by'])
    return (sign + '|p') in p['by'] or (sign + '|w') in p['by']
_cost = {}
def cost(word):
    if word not in _cost: _cost[word] = len(louis.translateString([UEB], word))
    return _cost[word]
def letter_words(p, names_out=None):
    """for each of the 21 letters: braille's word and its worth; the best other word beginning with the letter and its worth"""
    out = {}
    for w in LETTER_WORDS:
        L = w[0]; own = p['vocab'].get(w, 0) * (cost('x' + w) - 1 - 1); best = (None, 0)
        for cand, n in p['vocab'].items():
            if cand[0] != L or cand == w or len(cand) < 2 or not cand.isalpha(): continue
            if names_out is not None and cand in names_out: continue
            worth = n * (cost(cand) - 1)
            if worth > best[1]: best = (cand, worth)
        out[L] = dict(word=w, worth=own, best=best[0], best_worth=best[1])
    return out

if __name__ == '__main__':
    recs = load(sys.argv[1]); eras = {e: [r for r in recs if r['era'] == e] for e in (1, 2, 3)}; kjv = [r for r in recs if r['era'] == 0][0]; novels = eras[1] + eras[2] + eras[3]
    out = {}; lines = []
    def verdict(name, ok, odds, note):
        lines.append((name, ok, odds)); print('   %-4s %-6s (odds %.2f)  %s' % (name, 'HELD' if ok else 'FAILED', odds, note))
    print('The books: share of cells saved, UEB and EBAE (each against its own uncontracted form)')
    for e in (1, 2, 3):
        for r in sorted(eras[e], key=lambda r: r['year']): print('   era %d  %d  %-36s %7d words   UEB %.2f%%   EBAE %.2f%%   difference %.2f' % (e, r['year'], r['title'], r['ueb']['words'], 100 * S(r), 100 * S(r, 'ebae'), 100 * (S(r, 'ebae') - S(r))))
    print('   1611  %-36s %7d words   UEB %.2f%%   EBAE %.2f%%' % (kjv['title'], kjv['ueb']['words'], 100 * S(kjv), 100 * S(kjv, 'ebae')))
    mean = {e: sum(S(r) for r in eras[e]) / 6 for e in eras}; sd = {e: math.sqrt(sum((S(r) - mean[e]) ** 2 for r in eras[e]) / 5) for e in eras}
    for e in eras: print('   era %d mean %.2f%% (standard deviation among the six %.2f; standard error %.2f)' % (e, 100 * mean[e], 100 * sd[e], 100 * sd[e] / math.sqrt(6)))
    out['S'] = {r['folder']: (S(r), S(r, 'ebae')) for r in recs}; out['mean'] = mean; out['sd'] = sd
    P = {e: pool(eras[e]) for e in eras}; PE = {e: pool(eras[e], 'ebae') for e in eras}; PK = pool([kjv])
    print('\nThe sealed lines')
    lo, hi = min(S(r) for r in novels), max(S(r) for r in novels)
    verdict('B1', 0.19 <= lo and hi <= 0.25, 0.65, 'the eighteen novels run from %.2f%% to %.2f%%' % (100 * lo, 100 * hi))
    verdict('B2', mean[1] - mean[3] >= 0.005, 0.60, 'era 1 less era 3: %.2f points (standard error of the difference %.2f)' % (100 * (mean[1] - mean[3]), 100 * math.sqrt(sd[1] ** 2 / 6 + sd[3] ** 2 / 6)))
    verdict('B2b', mean[1] > mean[2] > mean[3], 0.45, 'means %.2f, %.2f, %.2f' % (100 * mean[1], 100 * mean[2], 100 * mean[3]))
    verdict('B3', S(kjv) > hi, 0.70, 'the Bible %.2f%%, the highest novel %.2f%%' % (100 * S(kjv), 100 * hi))
    diffs = [100 * (S(r, 'ebae') - S(r)) for r in novels]
    verdict('B4', all(1.2 <= d <= 3.0 for d in diffs), 0.70, 'EBAE less UEB runs from %.2f to %.2f points over the eighteen' % (min(diffs), max(diffs)))
    shares = {}
    for e in eras:
        tot = sum(v[1] for v in P[e]['by'].values()); top = sorted(P[e]['by'].items(), key=lambda kv: -kv[1][1])[:15]; shares[e] = sum(v[1] for _, v in top) / tot
    verdict('B5', all(0.43 <= shares[e] <= 0.55 for e in eras), 0.80, 'the fifteen largest units make %.1f%%, %.1f%%, %.1f%% of the saving in eras 1, 2, 3' % tuple(100 * shares[e] for e in (1, 2, 3)))
    fall = [(w, per100k(P[1], w + '|w'), per100k(P[3], w + '|w')) for w in 'which shall upon ought rather quite spirit lord much such'.split()]
    nf = sum(1 for w, a, b in fall if a > 0 and b <= 0.5 * a)
    verdict('B6a', nf >= 8, 0.60, '%d of ten fell by half or more: %s' % (nf, ', '.join('%s %.0f to %.0f' % x for x in fall)))
    rise = [(w, per100k(P[1], w + '|w'), per100k(P[3], w + '|w')) for w in 'just like people know right go'.split()]
    nr = sum(1 for w, a, b in rise if b >= 1.5 * a and b > 0)
    verdict('B6b', nr >= 4, 0.55, '%d of six rose by half or more: %s' % (nr, ', '.join('%s %.0f to %.0f' % x for x in rise)))
    never = {e: [(k, s) for k, ss in SIGNS.items() for s in ss if not occurs(P[e], s, k)] for e in eras}
    verdict('B7', len(never[3]) > len(never[1]), 0.70, 'signs that never occur: %d in era 1, %d in era 2, %d in era 3' % (len(never[1]), len(never[2]), len(never[3])))
    for e in eras: print('          era %d: %s' % (e, ', '.join(s for _, s in never[e]) or 'none'))
    LW = {e: letter_words(P[e]) for e in eras}; better = {e: [L for L, v in LW[e].items() if v['best_worth'] > v['worth']] for e in eras}
    verdict('B8', len(better[3]) >= 8, 0.70, 'in era 3 another word is worth more for %d of the 21 letters: %s' % (len(better[3]), ', '.join('%s (%s for %s)' % (L, LW[3][L]['best'], LW[3][L]['word']) for L in better[3])))
    gain = {e: sum(max(v['worth'], v['best_worth']) for v in LW[e].values()) / sum(v['worth'] for v in LW[e].values()) for e in eras}
    verdict('B9', gain[3] >= 1.2, 0.55, 'the best 21 are worth %.2f times braille\'s 21 in era 3 (%.2f in era 1, %.2f in era 2)' % (gain[3], gain[1], gain[2]))
    staack = dict([('and', 3785), ('for', 1243), ('of', 3521), ('the', 7650), ('with', 930), ('in', 4284), ('be', 801)])
    mine = {w: per100k(PE[2], w + '|w', 0) + per100k(PE[2], w + '|p', 0) for w in staack}; within = [w for w in staack if abs(mine[w] / staack[w] - 1) <= 0.35]
    verdict('R1', len(within) >= 5, 0.80, '%d of seven within 35%%: %s' % (len(within), ', '.join('%s %.0f (his %d)' % (w, mine[w], staack[w]) for w in staack)))
    r2 = 1e5 * (PE[2]['U'] - PE[2]['C']) / PE[2]['words']
    verdict('R2', 125000 <= r2 <= 145000, 0.75, 'era 2 in EBAE: %.0f cells saved per 100,000 words (in UEB %.0f); Staack 116,320' % (r2, 1e5 * (P[2]['U'] - P[2]['C']) / P[2]['words']))
    held = sum(ok for _, ok, _ in lines); brier = sum((o - ok) ** 2 for _, ok, o in lines) / len(lines)
    print('   %d of %d held; Brier score %.3f' % (held, len(lines), brier))
    out.update(shares=shares, fall=fall, rise=rise, never={e: [s for _, s in never[e]] for e in eras}, letter_words=LW, gain=gain, staack=mine, r2=r2, held=held, n=len(lines), brier=brier)
    json.dump(out, open(os.path.join(HERE, 'study.json'), 'w'), indent=1)
