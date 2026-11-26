"""Check that the quoted fragments in the replacements (and in the three added paragraphs as they stand) are exact
substrings of the sources on disk. Hyphenated line ends in the paper's text are joined first.

Run:  python3 -I quotes3.py
"""
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = '/srv/commons/wander-agent1/lit/orchiston2021/orchiston2021.pdf'
THAI = '/srv/commons/wander-agent1/lit/thammasat/thammasat.pdf'
WIKI = '/home/agent3/downloads/wiki-eclipse1868-25nov/page.wiki'


def pdftext(path, raw=True):
    args = ['pdftotext'] + (['-raw'] if raw else []) + [path, '-']
    return subprocess.run(args, capture_output=True, check=True).stdout.decode('utf-8')


def flat(t):
    t = re.sub(r'-\n\s*', '', t)          # join words broken at line ends
    return re.sub(r'\s+', ' ', t)


paper = flat(pdftext(PAPER))
paper_keep = re.sub(r'\s+', ' ', pdftext(PAPER))   # hyphens kept, for compounds
thai = re.sub(r'\s+', ' ', pdftext(THAI, raw=False))
wiki = re.sub(r'\s+', ' ', open(WIKI, encoding='utf-8').read())

checks = [
    ('paper', paper, 'in a very good humour, his calculations of the time of the eclipse having proved extremely '
                     'correct, (report said more so than those of the European observers)'),
    ('paper', paper, '(Ord, 1868: 12)'),
    ('paper', paper, 'The Thai solar eclipse calculation above is not particularly good'),
    ('paper', paper, 'Thai solar eclipse calculation'),
    ('paper', paper, 'not particularly good'),
    ('paper', paper, 'the European observers'),
    ('paper', paper, 'It has been researched by Orchiston and Orchiston (2017)'),
    ('paper', paper, 'his most distinguished guest was Sir Harry Ord'),
    ('paper', paper, 'Late that same afternoon'),
    ('paper', paper, 'Dr Dan Beach Bradley (1804‒1873; Lord, 1969)'),
    ('paper', paper, 'Mo Bradley and Thailand'),
    ('paper', paper, 'This was first contact according to King Rama IV’s calculation and prediction'),
    ('paper', paper, 'Journal of Astronomical History and Heritage, 24(2), 389–404 (2021)'),
    ('thai', thai, 'It was reported that he was greatly gratified to find that he was more correct by two seconds '
                   'in his calculations than were the French astronomers'),
    ('thai', thai, 'about only 2 or 3 seconds'),
    ('thai', thai, 'William Lee Bradley, Siam Then : The Foreign Colony in Bangkok before and after Anna'),
    ('thai', thai, '(Pasadena CA: William Carey Library, 1981), 149'),
    ('thai', thai, 'Thammasat Journal of History, Vol.8, No.2 (July - December 2021)'),
    ('thai', thai, 'The 1868 Solar Eclipse: Some Considerations about Its Sources and Historiography'),
    ('thai', thai, 'Research Article'),
    ('wiki', wiki, 'by about two seconds — than those of the French astronomers, who acknowledged his accuracy.'
                   '<ref name="orchiston2021" />'),
    ('wiki', wiki, 'were acknowledged as more precise'),
    ('wiki', wiki, 'on 1 October 1868.<ref name=Montes-Bradley>'),
    ('wiki', wiki, "964-word excerpt from ''Siam then, the foreign colony in Bangkok before and after Anna'', "
                   "Pasadena, California, 1981."),
    ('wiki', wiki, '|volume=24 |issue=2 |pages=389–404'),
]
bad = 0
for name, text, q in checks:
    n = text.count(q)
    if n == 0 and name == 'paper':
        n = paper_keep.count(q)
    print('%-5s %s  %s' % (name, 'found %d' % n if n else 'MISSING', q[:90]))
    bad += (n == 0)

print()
print('absent from the paper (all should be 0):')
for pat in [r'two seconds', r'2 seconds', r'\b2 ?s\b', r'\b2 sec', r'acknowledged (his|the King)', r'more accurate',
            r'accura', r'conced', r'prais', r'congratulat']:
    print('  %-28s %d' % (pat, len(re.findall(pat, paper, flags=re.I))))
print('every "second" in the paper:')
for m in re.finditer(r'second\w*', paper, flags=re.I):
    print('   ...' + paper[max(0, m.start() - 45):m.end() + 25] + '...')
print('every "acknowledg" in the paper:')
for m in re.finditer(r'acknowledg\w*', paper, flags=re.I):
    print('   ...' + paper[max(0, m.start() - 45):m.end() + 25] + '...')
lead = wiki[:wiki.find('==')]
print('references in the article before its first heading:', lead.count('<ref'))
print('pages in the Thai file:', subprocess.run(['pdfinfo', THAI], capture_output=True).stdout.decode().split('Pages:')[1].split()[0])
print('MISSING:', bad)
