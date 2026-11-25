# families.py -- the failing pairs sorted into named families, and each family's rate by period and by poet.
# python -I families.py OUT_DIR       (reads OUT_DIR/pairs.tsv and score.json; writes OUT_DIR/families.json)
# The families were drawn up AFTER the scores were seen: they describe, they were not sealed.  First rule that fits wins.
import sys, os, csv, json, re, collections, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from poets import POETS, GROUPS
out = sys.argv[1]; rows = list(csv.DictReader(open(os.path.join(out, 'pairs.tsv'), encoding='utf-8'), delimiter='\t'))
LITTLE = {'have', 'hath', 'are', 'said', 'says', 'saith', 'shall', 'were', 'wert'}
WA = re.compile(r'^(wa|wha|qua|swa|dwa|squa|thwa)|(?<=[a-z])(wa|qua)')            # war, what, quarrel, swan, reward
def has_wa(w): return bool(WA.search(w)) and w not in ('away', 'always', 'wave', 'waves', 'wake', 'awake', 'wait', 'way', 'ways', 'wade', 'wane', 'waste', 'wail')
def family(r):
    c, a, b = r['cls2'], r['k1'] or r['w1'], r['k2'] or r['w2']; u = {r['u1']: a, r['u2']: b}; t = {a: r['t1'], b: r['t2']}
    weak = lambda w: t[w] == '0'; full = lambda w: t[w] in ('1', '2')
    if c in ('ay~iy', 'ay~ih'):
        other = u.get('iy') or u.get('ih')
        if weak(other) or (t[other] == '' and re.search(r'(y|ie|ies|ee)$', other) and len(other) >= 6): return 'eye : majesty'
    if c != 'same vowel' and ((weak(a) and full(b)) or (weak(b) and full(a))): return 'dress : idleness'
    if a in LITTLE or b in LITTLE: return 'have : grave'
    if c in ('aa~ao', 'ae~oh', 'aa~oh', 'ao~ea', 'ae~ao', 'aa~ae', 'ae~ax', 'aa~ax', 'ao~oh', 'ah~oh') and has_wa(a) != has_wa(b): return 'war : far'
    if c == 'ah~uw' and 'ov' in a and 'ov' in b: return 'love : move'
    if c == 'ah~ow' and 'ov' in a and 'ov' in b: return 'love : grove'
    if c in ('ah~uh', 'ah~uw', 'uh~uw') and all(re.search(r'oo|ud|ould', w) for w in (a, b)): return 'blood : good : food'
    if c in ('ah~ow', 'ah~uw', 'ow~uw') and all(re.search(r'(ome|omb|oom|um|umb)(s|es|d)?$', w) for w in (a, b)): return 'come : home : tomb'
    if c in ('ah~ow', 'ah~oh', 'oh~ow') and all(re.search(r'(one|own|on|un|oan|onne)(s|es|d)?$', w) for w in (a, b)): return 'one : gone : alone'
    if c == 'ah~oh' and all(re.search(r'ngu?e?s?$', w) for w in (a, b)): return 'tongue : song'
    if c == 'oh~ow': return 'lost : most'
    if c == 'ey~iy':
        iy = u['iy']; ey = u['ey']
        if 'ea' in iy and 'ea' in ey: return 'great : seat'
        if re.search(r'ea|ei|e[a-z]e$|e[a-z]es$', iy): return 'sea : way'
    if c == 'ay~oy': return 'join : line'
    if c == 'eh~iy': return 'death : beneath'
    if c in ('ea~ia', 'ea~er', 'er~ia'): return 'fear : there'
    if c == 'aw~ow': return 'now : know'
    if c == 'ao~er': return 'word : sword'
    if c in ('aa~ey', 'ae~ey') and all(re.search(r'(ast|aste|ac[e]?d|ass|ace)s?$', w) for w in (a, b)): return 'last : taste'
    if c == 'ao~ua': return 'moor : more'
    if c == 'eh~ih': return 'wit : yet'
    if c == 'same vowel': return 'is : this'
    return 'other'
ORDER = ['eye : majesty', 'dress : idleness', 'is : this', 'love : move', 'love : grove', 'blood : good : food', 'come : home : tomb', 'one : gone : alone', 'tongue : song', 'lost : most',
         'sea : way', 'great : seat', 'death : beneath', 'join : line', 'war : far', 'fear : there', 'now : know', 'word : sword', 'have : grave', 'last : taste', 'moor : more', 'wit : yet', 'other']
fails = [r for r in rows if r['ev'] == '1' and r['ok'] == '0']
for r in fails: r['fam'] = family(r)
S = json.load(open(os.path.join(out, 'score.json')))
res = {'order': ORDER, 'total': {}, 'by_group': {}, 'by_poet': {}, 'top': {}, 'poets_having': {}}
for f in ORDER:
    fr = [r for r in fails if r['fam'] == f]; res['total'][f] = len(fr)
    res['by_group'][f] = {g: [sum(1 for r in fr if r['period'] == g), round(1000 * sum(1 for r in fr if r['period'] == g) / S['groups'][g]['evaluable'], 4)] for g in GROUPS}
    res['by_poet'][f] = {p: [sum(1 for r in fr if r['poet'] == p), round(1000 * sum(1 for r in fr if r['poet'] == p) / S['poets'][p]['evaluable'], 4)] for p in POETS}
    res['top'][f] = collections.Counter('/'.join(sorted([r['w1'], r['w2']])) for r in fr).most_common(12)
    res['poets_having'][f] = sum(1 for p in POETS if res['by_poet'][f][p][0] > 0)
json.dump(res, open(os.path.join(out, 'families.json'), 'w', encoding='utf-8'), indent=1)
with open(os.path.join(out, 'fails.tsv'), 'w', encoding='utf-8') as fo:
    fo.write('poet\tperiod\tstanza\ti\tj\tw1\tw2\tcls2\tfamily\n')
    for r in fails: fo.write('\t'.join([r['poet'], r['period'], r['stanza'], r['i'], r['j'], r['w1'], r['w2'], r['cls2'], r['fam']]) + '\n')
print('%d failing pairs of %d evaluable. Per thousand evaluable pairs in each period group:' % (len(fails), S['all']['evaluable']))
print('%-22s %5s | %s | poets | commonest pairs' % ('family', 'pairs', ' '.join('%6s' % g for g in GROUPS)))
for f in ORDER:
    print('%-22s %5d | %s | %5d | %s' % (f, res['total'][f], ' '.join('%6.1f' % res['by_group'][f][g][1] for g in GROUPS), res['poets_having'][f], ', '.join('%s %d' % x for x in res['top'][f][:7])))
