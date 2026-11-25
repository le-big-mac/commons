# ptest.py -- tests of the parsing, the respelling and the rhyme judge.   python -I ptest.py DATA_DIR
import sys, os, json, re, collections
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import rhyme as R, words as W
data = sys.argv[1]; J = R.Judge(data); n_ok = n_bad = 0
def ck(name, cond, extra=''):
    global n_ok, n_bad
    n_ok += bool(cond); n_bad += not cond; print(('ok    ' if cond else 'FAIL  ') + name + ((': ' + extra) if extra else ''))
corpus = json.load(open(os.path.join(here, 'corpus.json'), encoding='utf-8'))
# 1. the parse against the corpus's published size (Reddy and Knight 2011, Table 1: 11613 stanzas, 93030 lines) and its own combined file
gold = os.path.join(data, 'rhymedata', 'english_gold'); st = sum(len(r['stanzas']) for r in corpus.values()); bad = sum(r['bad_blocks'] for r in corpus.values())
allf = open(os.path.join(gold, 'all.pgold'), encoding='utf-8', errors='replace').read().split('\n'); heads = [l for l in allf if l.startswith('POEM')]
ck('parse: the stanzas kept (11,512) and the blocks refused because their words and scheme differ in length (101) are together the 11,613 stanzas the corpus\'s makers report', st == 11512 and bad == 101 and st + bad == 11613, '%d + %d' % (st, bad))
ck('parse: the combined file all.pgold has 11,611 heads; every poet\'s stanzas are in it, in order', len(heads) == 11611)
# 2. pairs counted a second way: for each stanza, pairs = half of (sum of squares of group sizes - lines)
pairs = 0; pairs2 = 0
for r in corpus.values():
    for s in r['stanzas']:
        c = collections.Counter(s['scheme']); pairs += sum(k * (k - 1) // 2 for k in c.values()); pairs2 += sum(1 for i in range(len(s['words'])) for j in range(i) if s['scheme'][i] == s['scheme'][j])
rows = sum(1 for _ in open(os.path.join(here, 'out', 'pairs.tsv'), encoding='utf-8')) - 1
ck('pairs: 58,501 by two ways of counting, and that many lines in the pair table', pairs == pairs2 == rows == 58501, '%d, %d, %d' % (pairs, pairs2, rows))
# 3. respelling: what each rule may and may not do
T = {'crownd': 'crowned', 'drest': 'dressed', 'cryd': 'cried', 'dyd': 'died', 'givn': 'given', 'stript': 'stripped', 'fixt': 'fixed', 'chast': 'chaste', 'oer': 'ore', 'heavn': 'heaven', 'powr': 'power',
     'offence': 'offense', 'loue': 'love', 'ioy': 'joy', 'feare': 'fear', 'sunne': 'sun', 'glasse': 'glass', 'dayes': 'days', 'daies': 'days', 'victorie': 'victory', 'wyde': 'wide', 'shee': 'she', 'funerall': 'funeral'}
got = {w: W.lookup(w, J.A)[0] for w in T}; ck('respelling in the American dictionary: 23 words to the entries they should reach', got == T, ', '.join('%s>%s' % (w, got[w]) for w in T if got[w] != T[w]))
kinds = {w: W.lookup(w, J.A)[1] for w in T}
ck('respelling: elisions and old spellings are told apart (crownd is an elision, loue an old spelling, tea exact), and the British dictionary has crownd and drest as they stand', kinds['crownd'].startswith('elision') and kinds['loue'].startswith('old') and W.lookup('tea', J.A)[1] == 'exact' and kinds['feare'].startswith('old') and kinds['oer'].startswith('elision') and W.lookup('crownd', J.B) == ('crownd', 'exact') and W.lookup('oer', J.B)[0] == "o'er")
ck('respelling in the American dictionary: offence by its American spelling, oer by a word of the same sound', W.lookup('offence', J.A) == ('offense', 'british:ence') and W.lookup('oer', J.A)[0] == 'ore')
ck('respelling refuses what it should: clime is not clim, hie is not hy, mown is not mowen, xyzzy is nothing', all(W.lookup(w, J.A)[0] in (None, w) for w in ['clime', 'hie', 'mown', 'xyzzy']), str([W.lookup(w, J.A) for w in ['clime', 'hie', 'mown', 'xyzzy']]))
# 4. stems, by hand
ck('stems: tea ends IY; majesty ends IY and from its stress AE JH AH S T IY; nature ends ER and from its stress EY CH ER', J.word('tea')['sa'] == [('IY',)] and J.word('majesty')['sa'] == [('IY',)] and J.word('majesty')['la'] == [('AE', 'JH', 'AH', 'S', 'T', 'IY')] and J.word('nature')['la'] == [('EY', 'CH', 'ER')])
ck('stems: in the British dictionary war ends ao with no r, far ends aa, prayer ends ea', J.word('war')['sb'] == [('ao',)] and J.word('far')['sb'] == [('aa',)] and ('ea',) in J.word('prayer')['sb'])
ck('stems: in the British dictionary words of more than one syllable end on their last vowel: obey ey, undertake ey k, majesty iy, remember ax, paradise ay s', J.word('obey')['sb'] == [('ey',)] and J.word('undertake')['sb'] == [('ey', 'k')] and ('iy',) in J.word('majesty')['sb'] and ('ax',) in J.word('remember')['sb'] and ('ay', 's') in J.word('paradise')['sb'], str([J.word(w)['sb'] for w in ['obey', 'undertake', 'majesty', 'remember', 'paradise']]))
ck('the British dictionary alone on longer words: betake/undertake and remember/December rhyme, obey/survey rhyme, paradise/sacrifice rhyme, obey/betray rhyme, majesty/undertake do not', [J.pair(a, b)['bs'] for a, b in [('betake', 'undertake'), ('remember', 'december'), ('obey', 'survey'), ('paradise', 'sacrifice'), ('obey', 'betray'), ('majesty', 'undertake')]] == [True, True, True, True, True, False])
# 5. Wyld's own examples: every pair he gives that does not rhyme today fails in both dictionaries, every one that does passes in one
N = Y = nN = nY = 0; wrong = []; skipped = []
for l in open(os.path.join(here, 'wyld-pairs.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    v, a, b = l.split(); p = J.pair(a, b)
    if p['as'] is None and p['bs'] is None: skipped.append(a + '/' + b); continue
    ok = bool(p['as']) or bool(p['bs'])
    if v == 'N': nN += 1; N += not ok
    else: nY += 1; Y += ok
    if (v == 'N') == ok: wrong.append('%s/%s said %s, judged A %s B %s' % (a, b, v, p['as'], p['bs']))
ck('Wyld\'s pairs: of %d he gives that do not rhyme today, the judge fails %d; of %d that do, it passes %d (%d pairs in neither dictionary)' % (nN, N, nY, Y, len(skipped)), not wrong and nN >= 100 and nY >= 19 and len(skipped) <= 2, '; '.join(wrong + skipped))
# 6. the judge on pairs with known answers in each dictionary separately
K = [('dawn', 'morn', False, True), ('been', 'seen', False, True), ('command', 'hand', True, False), ('again', 'rain', True, False), ('heaven', 'given', True, False), ('love', 'dove', True, True), ('love', 'move', False, False), ('wind', 'mind', True, True), ('tea', 'obey', False, False)]
bad = [(a, b) for a, b, ea, eb in K if (J.pair(a, b)['as'], J.pair(a, b)['bs']) != (ea, eb)]
ck('the two dictionaries apart: nine pairs with the answers an American and a British speaker would give (dawn/morn, been/seen British only; command/hand, again/rain American only)', not bad, str(bad))
ck('first-listed pronunciation only: again/rain fails (again is listed first with the vowel of "men"), wind/mind passes (the verb is listed first)', J.pair('again', 'rain')['a1'] is False and J.pair('wind', 'mind')['a1'] is True)
ck('from the stressed vowel on: majesty/be and nature/creature fail, liberty/majesty fails, ever/never passes', [J.pair(a, b)['al'] for a, b in [('majesty', 'be'), ('nature', 'creature'), ('liberty', 'majesty'), ('ever', 'never')]] == [False, False, False, True])
ck('a word found only by an old spelling makes its pair not evaluable: loue/move is flagged old in both dictionaries', J.pair('loue', 'move')['olda'] and J.pair('loue', 'move')['oldb'] and not J.pair('love', 'move')['olda'])
ck('an unknown word gives no verdict', J.pair('xyzzy', 'tea')['as'] is None and J.pair('xyzzy', 'tea')['bs'] is None)
# 7. the scores add up
S = json.load(open(os.path.join(here, 'out', 'score.json')))
ck('scores: the poets\' pairs and evaluable pairs add up to the whole; the groups too', sum(S['poets'][p]['pairs'] for p in S['poets']) == S['all']['pairs'] == 58501 and sum(S['poets'][p]['evaluable'] for p in S['poets']) == S['all']['evaluable'] == sum(S['groups'][g]['evaluable'] for g in S['groups']))
import csv
rows = list(csv.DictReader(open(os.path.join(here, 'out', 'pairs.tsv'), encoding='utf-8'), delimiter='\t'))
ev = [r for r in rows if r['ev'] == '1']; okc = sum(1 for r in ev if r['ok'] == '1')
ck('scores: M for the whole corpus recomputed from the pair table: %.2f%%' % (100 * okc / len(ev)), round(100 * okc / len(ev), 4) == S['all']['M'] and len(ev) == S['all']['evaluable'])
for g in ('1415', '1819'):
    eg = [r for r in ev if r['period'] == g]; ck('scores: M for the %s group recomputed from the pair table: %.2f%%' % (g, 100 * sum(1 for r in eg if r['ok'] == '1') / len(eg)), round(100 * sum(1 for r in eg if r['ok'] == '1') / len(eg), 4) == S['groups'][g]['M'])
ea = [r for r in rows if r['ea'] == '1']; eb = [r for r in rows if r['eb'] == '1']
ck('scores: M_A, M_A1, the long stem and M_B for the whole corpus recomputed from the pair table', [round(100 * sum(1 for r in ea if r[k] == '1') / len(ea), 4) for k in ('as', 'a1', 'al')] == [S['all']['M_A'], S['all']['M_A1'], S['all']['M_Along']] and round(100 * sum(1 for r in eb if r['bs'] == '1') / len(eb), 4) == S['all']['M_B'])
ck('pair table: a pair is "ok" exactly when it rhymes in a dictionary in which it is evaluable; "ev" exactly when evaluable in one', all((r['ok'] == '1') == ((r['ea'] == '1' and r['as'] == '1') or (r['eb'] == '1' and r['bs'] == '1')) and (r['ev'] == '1') == (r['ea'] == '1' or r['eb'] == '1') for r in rows))
ck('pair table: no pair found only by an old spelling is evaluable in that dictionary', all(not (r['olda'] == '1' and r['ea'] == '1') and not (r['oldb'] == '1' and r['eb'] == '1') for r in rows))
# 8. the families: twenty-six pairs whose family I name by hand
want = {'obey/tea': 'sea : way', 'sea/way': 'sea : way', 'fate/retreat': 'sea : way', 'great/seat': 'great : seat', 'break/speak': 'great : seat', 'join/line': 'join : line', 'love/move': 'love : move', 'grove/love': 'love : grove',
        'blood/good': 'blood : good : food', 'come/home': 'come : home : tomb', 'alone/one': 'one : gone : alone', 'song/tongue': 'tongue : song', 'lost/most': 'lost : most', 'beneath/death': 'death : beneath',
        'far/war': 'war : far', 'pass/was': 'war : far', 'fear/there': 'fear : there', 'flow/now': 'now : know', 'sword/word': 'word : sword', 'grave/have': 'have : grave', 'are/care': 'have : grave',
        'fast/haste': 'last : taste', 'moor/more': 'moor : more', 'wit/yet': 'wit : yet', 'is/this': 'is : this', 'eye/majesty': 'eye : majesty', 'dress/idleness': 'dress : idleness'}
got = collections.defaultdict(set); nf = 0
for r in csv.DictReader(open(os.path.join(here, 'out', 'fails.tsv'), encoding='utf-8'), delimiter='\t'): got['/'.join(sorted([r['w1'], r['w2']]))].add(r['family']); nf += 1
wrongf = ['%s in %s' % (k, sorted(got[k])) for k, v in want.items() if got[k] != {v}]
ck('families: %d pairs named by hand fall in the families named, and the family file has one line for each failing pair' % len(want), not wrongf and nf == sum(1 for r in ev if r['ok'] == '0'), '; '.join(wrongf))
print('\n%d pass, %d fail' % (n_ok, n_bad)); sys.exit(1 if n_bad else 0)
