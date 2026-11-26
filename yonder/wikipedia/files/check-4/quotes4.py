"""Check every quotation in the rewritten last paragraph of note 4 against its source.
Usage: python -I quotes4.py README.md PAGE.html PAGE.wiki PAPER.txt
Prints one line per quotation; short quotations only."""
import sys, re, html

readme = open(sys.argv[1], encoding='utf-8').read()
raw = open(sys.argv[2], 'rb').read().decode('utf-8')
wiki = open(sys.argv[3], encoding='utf-8').read()
paper = open(sys.argv[4], encoding='utf-8', errors='replace').read()

def strip(s):
    s = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', s)
    s = re.sub(r'(?i)<br\s*/?>', '\n', s)
    s = re.sub(r'(?i)</p>', '\n\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'[ \t]+', ' ', html.unescape(s))

page = strip(raw)
a = page.index('"King Mongkut\'s prediction surpassed')
b = page.index('[L. Robert Morris')
passage = page[a:b]
# left column of the paper's two-column text, joined
left = ' '.join(re.sub(r'\s{6,}.*$', '', l).strip() for l in paper.split('\n'))
left = re.sub(r'\s+', ' ', left)

checks = [
 ('page heading', 'Descendants of Danyell Broadley de West Morton', re.sub(r'\s+', ' ', page)),
 ('page title element', 'Descendants of Danyell Broadley of Bingley, Yorkshire', page),
 ('citation title', 'title= Descendants of Danyell Broadley de West Morton', wiki),
 ('citation format', "964-word excerpt from ''Siam then, the foreign colony in Bangkok before and after Anna'', Pasadena, California, 1981.", wiki),
 ('citation archive', 'https://web.archive.org/web/20150210165538/http://www.bradleyfoundation.org/genealogies/Bingley/tobg88.htm|archive-date= 2015-02-10', wiki),
 ('capture stamp in file', 'FILE ARCHIVED ON 16:55:38 Feb 10, 2015', raw),
 ('first line of passage, then a break and a second opening mark', '"King Mongkut\'s prediction surpassed those of European scientists. "In the 19th century', re.sub(r'\s+', ' ', passage)),
 ('attribution', '[L. Robert Morris, National Post, Toronto, Ontario, Canada, 22 December 2000]', page),
 ('pointer', 'See Bradley, W.L., "Siam Then, The Foreign Colony in Bangkok before and after Anna," Pasadena, Cailfornia, 1981.', page),
 ('two-seconds sentence', 'In fact, his calculations were better -- by about two seconds -- than those of the now exhausted French astronomers, who acknowledged his accuracy.', passage),
 ('article sentence', 'His calculations were better — by about two seconds — than those of the French astronomers, who acknowledged his accuracy.<ref name="orchiston2021" />', wiki),
 ('diary, first', 'the Rev. Dan Beach Bradley, wrote in his diary: "We heard the pipes', passage),
 ('diary, second', 'Bradley, again: "The gradual withdrawal', passage),
 ('death, page', 'He died on his birthday, Oct. 18, 1868.', passage),
 ('death, article', 'He died a month and a half after the eclipse, on 1 October 1868.<ref name=Montes-Bradley>', wiki),
 ('death, paper (left column joined)', 'He died on 1 October 1868, just two and half weeks before his 64th birthday.', left),
 ('lead', 'whose calculations were acknowledged as more precise than those of contemporary French astronomers. During', wiki),
]
for label, q, src in checks:
    print('%-64s %s  %r' % (label, 'found' if q in src else 'NOT FOUND', q[:80]))

print('"more precise" in passage:', passage.count('more precise'), '| "acknowledged" in passage:', passage.count('acknowledged'),
      '| "Siam Then" on page:', page.count('Siam Then'), '| bracketed attributions on page:', len(re.findall(r'\n\[[^\]\n]{5,200}\]', page)))
toks = passage.split()
print('words in quotation marks: %d by spaces, %d without the %d double hyphens' % (len(toks), len([t for t in toks if t != '--']), toks.count('--')))

# quotations in the README paragraph that should be in README too
para = [l for l in readme.split('\n') if l.startswith('**So, for an editor.**')][0]
print('paragraph words:', len(para.split()))
for q in re.findall(r'"([^"]{12,})"', para):
    where = [n for n, s in (('page', page), ('wikitext', wiki), ('paper', left)) if q in s or q.replace("'Siam Then ...'", '') in s]
    print('   quoted in paragraph: %-70r in: %s' % (q[:70], ', '.join(where) or '-'))
