"""Evidence reading 3: the new statements of the third candidate against the records (downloads read as data).
usage: python -I ev3_records.py"""
import re, os, sys, html
SRC = '/srv/commons/wikipedia-notes-agent3/'
def norm(s): return ' '.join(s.replace('**', '').replace('*', '').split())

print('== "In the words of 25 November": the sentences on the two rules, in the texts kept from 25 November and now')
now = norm(open(SRC + 'README.md', encoding='utf-8').read())
a = now.index('Its talk-page guideline says'); b = now.index('If you are an editor and one of these is worth mending')
rules = now[a:b].strip()
for f in ['README-as-read.md', 'README-as-reread.md', 'README-as-read-3.md', 'README-as-read-4.md']:
    t = norm(open(SRC + f, encoding='utf-8').read())
    print('  %-22s (file of %s) has the sentences as they stand now: %s' % (f, __import__('time').strftime('%d %b %H:%M UTC', __import__('time').gmtime(os.stat(SRC + f).st_mtime)), rules in t))
print('  the sentences now (%d words): %s ... %s' % (len(rules.split()), rules[:60], rules[-45:]))

print('\n== note 1, "An editor looking for them could start between 25 December 2022 and 17 December 2023": the changed cells in the samples')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def col(path, lang):
    t = open(path, encoding='utf-8').read(); best = None
    for m in re.finditer(r'\{\|.*?\n\|\}', t, flags=re.S):
        if 'Spanish' in m.group(0) and 'Icelandic' in m.group(0) and 'Turkish' in m.group(0): best = m.group(0)
    rows = re.split(r'\n\|-', best); heads = []
    for r in rows:
        hs = [l for l in r.split('\n') if l.startswith('!')]
        if hs and any('Spanish' in l for l in hs):
            for l in hs: heads += re.split(r'!!', l.lstrip('!'))
            break
    names = []
    for h in heads:
        mm = re.findall(r'\[\[([^\]|]*)(?:\|([^\]]*))?\]\]', h); names.append((mm[0][1] or mm[0][0]).strip() if mm else h.strip())
    k = names.index(lang); vals = {}
    for r in rows:
        lines = [l for l in r.strip().split('\n') if l.startswith('|') and not l.startswith('|}') and not l.startswith('|+')]
        if len(lines) < 2: continue
        letter = lines[0].lstrip('|').replace("'''", '').strip(); cells = []
        for l in lines[1:]: cells += [c.strip() for c in l.lstrip('|').split('||')]
        if k - 1 < len(cells):
            c = re.sub(r'<ref.*', '', cells[k - 1]); c = re.sub(r'\{\{.*?\}\}|<!--.*?-->', '', c); mm = re.search(r'\d+(?:\.\d+)?', c.replace('~0', '0'))
            vals[letter] = float(mm.group(0)) if mm else 0.0
    return vals
H = '/home/agent3/downloads/wiki-letter-frequency-history/rev_%d/page.wiki'
revs = [(1129452280, '25 Dec 2022'), (1190425789, '17 Dec 2023'), (1231481265, '28 Jun 2024'), (1263876077, '19 Dec 2024')]
today = '/home/agent3/downloads/wiki-Letter_frequency_/page.wiki'
changed = {'Spanish': 'e h k u w x y'.split(), 'French': 'h j y'.split(), 'Portuguese': 'e h j x'.split(), 'Italian': 'h u x'.split()}
by2023 = later = 0
for lang, letters in changed.items():
    cols = [col(H % r, lang) for r, d in revs] + [col(today, lang)]
    for L in letters:
        v = [c[L] for c in cols]
        first = next(i for i in range(len(v)) if abs(v[i] - v[-1]) < 1e-9 and all(abs(x - v[-1]) < 1e-9 for x in v[i:]))
        when = (['already in 2022'] + ['by ' + d for r, d in revs[1:]] + ['after 19 Dec 2024'])[first]
        if first == 1: by2023 += 1
        else: later += 1
        print('  %-10s %s : %s  -> today\'s value in place %s' % (lang, L, ' | '.join('%.3f' % x for x in v), when))
print('  columns of figures: %s | today' % ' | '.join(d for r, d in revs))
print('  of the 17 changed cells, today\'s value in place by 17 December 2023: %d ; only later: %d' % (by2023, later))

print('\n== note 2\'s fold label "both calculations, with their coordinates and land areas": what the old note gives')
n = norm(open(SRC + 'README.md', encoding='utf-8').read())
for s in ['120,609,390 km²', '120,661,207 km²', 'with areas given only as "X +" a number', '47.412° N, 2.493° W', '40.68° N, 1.59° E', 'Île Dumet 10 to 23 km from it and Nantes 63 to 76 km, by the article\'s coordinates and the paper\'s two calculations',
          'which are pages 4, 6 and 16 of the scan', 'lower by about 52,000 km² in the first calculation and 58,500 km² in the second']:
    print('  %-5s %s' % (s in n, s))
