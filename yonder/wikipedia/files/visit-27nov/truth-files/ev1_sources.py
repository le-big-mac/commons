"""Evidence reading 1: strings of the open parts against the saved sources (read as data).
usage: python -I ev1_sources.py"""
import re, html, os, sys

def norm(s):
    s = s.replace('­', '')
    s = re.sub(r'-\s*\n\s*', '', s)          # join words hyphenated at line ends
    return re.sub(r'\s+', ' ', s)

def show(name, t, pats, n=110):
    for p in pats:
        ms = list(re.finditer(p, t, flags=re.I))
        print('  %-14s %-42r occurs %d' % (name, p, len(ms)))
        for m in ms[:6]:
            print('        ...%s...' % t[max(0, m.start() - n):m.end() + n])

print('== the 2021 paper (text saved by Catalpa)')
P = '/srv/commons/wander-agent1/lit/orchiston2021/'
for fn in ('o.txt', 'o_raw.txt'):
    t = norm(open(P + fn, encoding='utf-8', errors='replace').read())
    print(' ', fn, len(t), 'characters')
    show(fn, t, [r'two\s+seconds', r'\b2\s+seconds', r'by about two', r'\bseconds?\b', r'acknowledg\w*', r'more precise', r'1 October 1868',
                 r'report said more so', r'not particularly good', r'Ord,? 1868: ?12', r'Orchiston and Orchiston \(2017\)'])

print('\n== the archived web page (saved 26 November)')
raw = open('/home/agent3/downloads/wiki-bradley-excerpt-archive/page.html', encoding='utf-8', errors='replace').read()
t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', raw, flags=re.S | re.I)
t = norm(html.unescape(re.sub(r'<[^>]+>', ' ', t)))
show('capture', t, [r'two seconds', r'acknowledged', r'more precise', r'died on his birthday', r'National Post', r'Siam Then', r'wrote in his diary', r'Bradley, again'], 160)
i = t.find("King Mongkut's prediction surpassed"); j = t.find('Art and Design.', i)
print('  the passage: from character %d to %d; words by spaces: %d' % (i, j, len(t[i:j + 15].split())))
k = t.find('In fact, his calculations'); d1 = t.find('wrote in his diary'); d2 = t.find('Bradley, again')
print('  positions inside the passage: first diary quotation %d, second %d, the two-seconds sentence %d' % (d1 - i, d2 - i, k - i))

print('\n== the article (wikitext saved 25 November): the sentence, and the capture\'s sentence less four words')
w = open('/home/agent3/downloads/wiki-eclipse1868-25nov/page.wiki', encoding='utf-8').read()
a = 'His calculations were better — by about two seconds — than those of the French astronomers, who acknowledged his accuracy.'
b = 'In fact, his calculations were better -- by about two seconds -- than those of the now exhausted French astronomers, who acknowledged his accuracy.'
print('  article sentence in wikitext:', w.count(a), '; capture sentence in capture:', t.count(b))
b2 = b.replace('In fact, ', '').replace('now exhausted ', '').replace('--', '—'); b2 = b2[0].upper() + b2[1:]
print('  capture sentence without "In fact, " and "now exhausted ", dashes and capital made alike, equals the article\'s:', b2 == a)
for s in ['<ref name="orchiston2021" />', 'were acknowledged as more precise', 'the French expedition led by Pierre Janssen', 'invited', 'on 1 October 1868', '964-word excerpt',
          'https://web.archive.org/web/20150210165538/http://www.bradleyfoundation.org/genealogies/Bingley/tobg88.htm', 'archive-date= 2015-02-10']:
    print('  wikitext %-60r occurs %d' % (s[:60], w.count(s)))
m = re.search(r'who acknowledged his accuracy\.(<ref[^>]*>)', w); print('  the tag straight after the two-seconds sentence:', m.group(1) if m else None)
secs = [(mm.start(), mm.group(1).strip()) for mm in re.finditer(r'^=+([^=\n]+)=+\s*$', w, flags=re.M)]
def section_of(pos):
    s = '(lead)'
    for p, name in secs:
        if p < pos: s = name
    return s
print('  section of the two-seconds sentence:', section_of(w.index(a)), '; of "were acknowledged as more precise":', section_of(w.index('were acknowledged as more precise')),
      '; of "led by Pierre Janssen":', section_of(w.index('led by Pierre Janssen')), '; of "Guntur":', section_of(w.index('Guntur')))

print('\n== the hemispheres article (wikitext saved 21 and 25 November, identical)')
h = open('/home/agent3/downloads/landhemi-wiki/lw.wiki', encoding='utf-8').read()
for s in ['is centered in [[Metropolitan France]]', 'https://www.lecfc.fr/new/articles/176-article-15.pdf', '|date=2002', 'issue=173–174', 'pages=43–58', 'higher', 'absolute', 'maxim', 'Tarragon', 'Mediterranean']:
    print('  wikitext %-55r occurs %d' % (s, h.count(s)))
print('  order of the two references after the 2002 sentence: Affholder at', h.index('name="Affholder2002"'), ', Monmonier at', h.index('name="m509"'))

print('\n== Stephan\'s report (machine text, with faults): the quotations and their printed pages (scan page + 97)')
st = open('/home/agent3/downloads/stephan-1870/paper.txt', encoding='utf-8', errors='replace').read()
pages = st.split('\f')
print('  form feeds in the machine text:', len(pages) - 1)
for q in ["l'une par le Bureau des", "la composa", "fit offrir d'en prendre la conduite", "je décidai", "nous séparâmes de M. Janssen", "Pointe-de-Galles nous", "demande du Gouvernement français", "Mazulipatam"]:
    hits = [k + 1 for k, pg in enumerate(pages) if q in norm(pg)]
    print('  %-40r on scan pages %s = printed pages %s' % (q, hits, [x + 97 for x in hits]))
