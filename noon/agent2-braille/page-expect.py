"""page-expect.py: what the page ought to show, worked out apart from page.py: the sentences straight through the translator,
and the figures straight from the study's records.     /usr/bin/python3 -I page-expect.py  ->  page-expect.json"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import louis, page, run
st = json.load(open(os.path.join(HERE, 'study-story.json'))); sp = json.load(open(os.path.join(HERE, 'speech-study-story.json'))); recs = {f: json.load(open(os.path.join(HERE, 'books-story', f + '.json'))) for _, f, _, _ in run.BOOKS}
out = dict(passages=[], books=[], mean={}, signs={}, speech={})
for label, credit, text in page.PASSAGES:
    u = len(louis.translateString(['en-ueb-g1.ctb'], text)); braille = louis.translateString(['en-ueb-g2.ctb'], text, mode=louis.dotsIO | louis.ucBrl)
    out['passages'].append(dict(label=label, words=text.split(' '), U=u, C=len(braille), braille=[w for w in braille.split('⠀')]))
for e, f, t, y in run.BOOKS:
    r = recs[f]['ueb']; out['books'].append(dict(era=e, title=t, year=y, s=(r['U'] - r['C']) / r['U']))
for e in (1, 2, 3):
    b = [x['s'] for x in out['books'] if x['era'] == e]; out['mean'][str(e)] = sum(b) / len(b)
def per100k(era, keys):
    rs = [recs[f]['ueb'] for ee, f, _, _ in run.BOOKS if ee == era]; return 1e5 * sum(r['by'].get(k, [0, 0])[1] for r in rs for k in keys) / sum(r['words'] for r in rs)
WORD = set('which not shall will just like people out you was it'.split())
for s in page.LOSERS + page.GAINERS + page.BIG:
    if s in WORD: keys = lambda r, s=s: [s + '|w']
    elif s in ('would', 'should', 'such', 'much', 'about'): keys = None
    else: keys = lambda r, s=s: [s + '|w', s + '|p']
    vals = []
    for era in (1, 3):
        rs = [recs[f]['ueb'] for ee, f, _, _ in run.BOOKS if ee == era]; W = sum(r['words'] for r in rs)
        if keys is None: tot = sum(v[1] for r in rs for k, v in r['by'].items() if k.split('|')[0].startswith(s))
        else: tot = sum(r['by'].get(k, [0, 0])[1] for r in rs for k in keys(r))
        vals.append(1e5 * tot / W)
    out['signs'][s] = vals
out['speech'] = dict(out=sp['out'], ins=sp['ins'], share=sp['share']); out['never'] = st['never']
import story
def L(r): u = r['ueb']; return (u['U'] - u['C']) / (u['letters'] + u['words'])
out['added'] = [dict(title=t, year=y, rate=1000 * story.short_forms(json.load(open(os.path.join(HERE, 'books-new', f + '.json')))['ueb']['vocab']) / json.load(open(os.path.join(HERE, 'books-new', f + '.json')))['ueb']['words'], L=L(json.load(open(os.path.join(HERE, 'books-new', f + '.json'))))) for e, f, t, y in run.NEW]
out['sixL'] = [sum(L(recs[f]) for e, f, _, _ in run.BOOKS if e == era) / 6 for era in (1, 3)]
out['held3'] = sum(1 for l in open(os.path.join(HERE, 'verdicts-3-as-first-run.out')) if ' HELD ' in l)
json.dump(out, open(os.path.join(HERE, 'page-expect.json'), 'w'), ensure_ascii=False, indent=1); print('page-expect.json:', len(out['passages']), 'sentences,', len(out['books']), 'books,', len(out['signs']), 'signs')
