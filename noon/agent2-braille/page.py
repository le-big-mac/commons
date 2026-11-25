"""page.py: the page of the braille study, built from the study's own records and the translator.
    /usr/bin/python3 -I page.py   ->  braille.html   (reads the records of the stories alone: study-story.json, speech-study-story.json, after-story.json)
Nothing on the page is typed by hand except its prose and the four sentences shown: every figure comes from the records."""
import json, os, sys, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import louis, cells, run

PASSAGES = [   # (label, credit, sentence)
    ('1813', 'Jane Austen, Pride and Prejudice', 'It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.'),
    ('1925', 'F. Scott Fitzgerald, The Great Gatsby', "In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since."),
    ('2008', 'Cory Doctorow, Little Brother (one sentence, quoted)', "I'm a senior at Cesar Chavez high in San Francisco's sunny Mission district, and that makes me one of the most surveilled people in the world."),
    ('1611', 'The King James Bible, Genesis 2:18', 'And the LORD God said, It is not good that the man should be alone; I will make him an help meet for him.'),
]
LOSERS = ['which', 'not', 'shall', 'will', 'would', 'should', 'upon', 'such', 'much']
GAINERS = ['just', 'like', 'people', 'about', 'out', 'you', 'was', 'it', 'right']
BIG = ['the', 'ing', 'ed']          # the three largest signs, which also gained: said in a sentence, since beside them every other bar is a sliver

def passage(text):
    """words of a sentence, each with its print letters (and which of them a sign replaces) and its braille; and the cell counts"""
    b1 = louis.translateString([cells.G1], text); b2, _, r2, _ = louis.translate([cells.UEB], text); n = len(text)
    bu = louis.translateString([cells.UEB], text, mode=louis.dotsIO | louis.ucBrl); assert len(bu) == len(b2)
    mark = [False] * n; i = 0
    while i < n:
        j = i + 1
        while j < n and r2[j] == r2[i]: j += 1
        if j - i > 1 and text[i:j].strip().isalpha(): mark[i:j] = [True] * (j - i)
        i = j
    words = []; i = 0
    while i < n:
        if text[i] == ' ': i += 1; continue
        j = i
        while j < n and text[j] != ' ': j += 1
        cellsb = bu[r2[i]:(r2[j] if j < n else len(bu))]
        words.append(dict(print=[[text[k], mark[k]] for k in range(i, j)], braille=cellsb)); i = j
    assert sum(len(w['braille']) for w in words) + len(words) - 1 == len(b2), 'the words\' cells and the spaces between them make the whole'
    return dict(words=words, U=len(b1), C=len(b2))

if __name__ == '__main__':
    st = json.load(open(os.path.join(HERE, 'study-story.json'))); sp = json.load(open(os.path.join(HERE, 'speech-study-story.json'))); af = json.load(open(os.path.join(HERE, 'after-story.json')))
    th = json.load(open(os.path.join(HERE, 'third.json'))); a3 = json.load(open(os.path.join(HERE, 'after3.json')))
    added = sorted((dict(title=b['title'], year=b['year'], rate=b['rate'], L=b['L']) for b in th['books']), key=lambda x: x['year'])
    six = lambda e: sum(x['L'] for x in a3['P']['rows'] if x['era'] == e) / 600
    books = [dict(era=e, title=t, year=y, s=st['S'][f][0]) for e, f, t, y in run.BOOKS]
    table = {(k, s): v for k, s, v in af['D']['table']}
    def sign(s):
        hits = [(k, v) for (k, x), v in table.items() if x == s and k != 'lower groupsign']; assert len(hits) == 1, (s, hits); return dict(sign=s, then=hits[0][1][1], now=hits[0][1][3])
    DATA = dict(books=books, mean={e: st['mean'][e] for e in ('1', '2', '3')}, never=st['never'], passages=[dict(label=l, credit=c, **passage(t)) for l, c, t in PASSAGES],
                losers=[sign(s) for s in LOSERS], gainers=[sign(s) for s in GAINERS], big=[sign(s) for s in BIG], added=added, sixL=dict(first=six(1), last=six(3)), held3=[th['held'], th['n']], speech=dict(out=sp['out'], ins=sp['ins'], share=sp['share']))
    page = open(os.path.join(HERE, 'page.src.html'), encoding='utf-8').read().replace('/*DATA*/', 'const DATA = ' + json.dumps(DATA, ensure_ascii=False) + ';')
    open(os.path.join(HERE, 'braille.html'), 'w', encoding='utf-8').write(page)
    for p in DATA['passages']: print('%s: %d cells letter for letter, %d with the signs, %.1f%% saved' % (p['label'], p['U'], p['C'], 100 * (1 - p['C'] / p['U'])))
    print('braille.html: %d bytes' % len(page.encode('utf-8')))
