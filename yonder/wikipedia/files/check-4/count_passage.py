"""Count the words of the quoted Mongkut passage on the archived page, several ways;
compare the page's sentence with the article's; look at the page's layout conventions.
Usage: python -I count_passage.py PAGE.html PAGE.wiki
Prints counts and short quotations only."""
import sys, re, html

raw = open(sys.argv[1], 'rb').read().decode('utf-8')
wiki = open(sys.argv[2], encoding='utf-8').read()

def strip(s):
    s = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', s)
    s = re.sub(r'(?i)<br\s*/?>', '\n', s)
    s = re.sub(r'(?i)</p>', '\n\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(s)

# --- the passage ---
a = raw.index('"King Mongkut\'s prediction surpassed')
b = raw.index('[L. Robert Morris')
c = raw.index('See Bradley, W.L.')
d = raw.index('</blockquote>', c)
passage_html = raw[a:b]
passage = strip(passage_html)
attrib = strip(raw[b:c]).strip()
pointer = strip(raw[c:d]).strip()
print('ATTRIBUTION as printed:', repr(attrib))
print('POINTER as printed    :', repr(pointer))
print('html between attribution and pointer:', repr(raw[b + len('[L. Robert Morris, National Post, Toronto, Ontario, Canada, 22 December 2000]'):c]))

def words(t, mode):
    toks = t.split()
    if mode == 'ws':            # whitespace tokens, '--' counted as a token
        return len(toks)
    if mode == 'ws_nodash':     # whitespace tokens that contain a letter or digit
        return len([x for x in toks if re.search(r'[A-Za-z0-9]', x)])
    if mode == 'alnum_runs':    # runs of letters/digits/apostrophes (hyphenated words split)
        return len(re.findall(r"[A-Za-z0-9']+", t))
    if mode == 'word_like':     # MS-Word-like: whitespace tokens (same as ws)
        return len(toks)

lines = [l for l in passage.split('\n') if l.strip()]
print('passage paragraphs (lines):', len(lines))
print('first line:', repr(lines[0]))
print('second line starts:', repr(lines[1][:60]))
print('last line ends:', repr(lines[-1][-60:]))
print('double-quote marks in passage:', passage.count('"'))
head = lines[0]
body = '\n'.join(lines[1:])
for label, t in [('whole quoted passage (headline line + body)', passage),
                 ('body without the first line', body),
                 ('passage + attribution', passage + ' ' + attrib),
                 ('passage + attribution + pointer', passage + ' ' + attrib + ' ' + pointer),
                 ('body + attribution', body + ' ' + attrib),
                 ('body + attribution + pointer', body + ' ' + attrib + ' ' + pointer)]:
    print('%-48s ws=%d  ws_nodash=%d  alnum_runs=%d  chars=%d' % (label, words(t, 'ws'), words(t, 'ws_nodash'), words(t, 'alnum_runs'), len(t)))
print('headline words:', words(head, 'ws'), '| attribution words:', words(attrib, 'ws'), '| pointer words:', words(pointer, 'ws'))
print("count of ' -- ' in passage:", passage.count(' -- '))

# quoted-within-quoted: diary quotations inside the piece
for m in re.finditer(r'(wrote in his diary: |Bradley, again: )"', passage):
    st = m.end()
    en = passage.index('"', st)
    q = passage[st:en]
    print('inner quotation introduced by %r: %d words; starts %r ... ends %r' % (m.group(1), len(q.split()), q[:40], q[-60:]))
i2 = passage.index('In fact, his calculations')
print('two-seconds sentence lies inside an inner quotation?',
      any(passage.index('"', m.end()) > i2 > m.end() for m in re.finditer(r'(wrote in his diary: |Bradley, again: )"', passage)))

# --- the sentence ---
m = re.search(r'In fact, his calculations[^.]*\.', passage)
page_sent = m.group(0)
print('PAGE SENTENCE:', repr(page_sent))
m = re.search(r'His calculations were better[^.]*\.', wiki)
art_sent = m.group(0)
print('ARTICLE SENTENCE:', repr(art_sent))
print('article sentence non-ASCII:', sorted({(ch, hex(ord(ch))) for ch in art_sent if ord(ch) > 127}))
print('page sentence non-ASCII:', sorted({(ch, hex(ord(ch))) for ch in page_sent if ord(ch) > 127}))
derived = page_sent.replace('In fact, ', '', 1).replace('now exhausted ', '', 1)
print('page sentence minus "In fact, " and "now exhausted ":', repr(derived))
norm = derived.replace(' -- ', ' — ')
norm = norm[0].upper() + norm[1:]
print('after capital and dash normalisation equals article sentence:', norm == art_sent)
import difflib
for tag, i1, i2_, j1, j2 in difflib.SequenceMatcher(None, page_sent, art_sent, autojunk=False).get_opcodes():
    if tag != 'equal':
        print('   diff', tag, repr(page_sent[i1:i2_]), '->', repr(art_sent[j1:j2]))

# --- what the README quotes ---
if len(sys.argv) > 3:
    readme = open(sys.argv[3], encoding='utf-8').read()
    for q in [page_sent,
              'L. Robert Morris, National Post, Toronto, Ontario, Canada, 22 December 2000',
              "King Mongkut's prediction surpassed those of European scientists",
              'Descendants of Danyell Broadley of Bingley, Yorkshire',
              "See Bradley, W.L., 'Siam Then ...'"]:
        print('README has %r: %d time(s); page (stripped) has it: %s' % (q[:70], readme.count(q), q in strip(raw)))

# --- death, other phrases the article shares with the passage ---
for needle in ['He died', 'chills and fever', 'birthday', 'six minutes', 'invited', 'Janssen', 'exact second']:
    for mm in re.finditer(re.escape(needle), passage):
        print('PASSAGE %r: ...%s...' % (needle, passage[max(0, mm.start()-80):mm.end()+80].replace('\n', ' / ')))
for needle in ['He died', 'chills and fever']:
    for mm in re.finditer(re.escape(needle), wiki):
        print('ARTICLE %r: ...%s...' % (needle, wiki[max(0, mm.start()-90):mm.end()+70].replace('\n', ' / ')))

# --- layout conventions on the page ---
txt = strip(raw)
print('--- bracketed attributions on the page:')
for mm in re.finditer(r'\n\[([^\]\n]{5,200})\]', txt):
    print('   [', mm.group(1), ']')
print('--- lines beginning "See ":')
for mm in re.finditer(r'(?m)^\s*See [^\n]{0,160}', txt):
    print('   ', mm.group(0).strip())
print('--- occurrences of "Siam Then" on page:', len(re.findall(r'Siam Then', txt, re.I)), '| "W.L." :', len(re.findall(r'W\.\s?L\.', txt)), '| "William Lee":', txt.count('William Lee'), '| "excerpt":', len(re.findall('excerpt', txt, re.I)), '| "964":', txt.count('964'))
print('--- headings:')
for mm in re.finditer(r'(?is)<(h[1-6])[^>]*>(.*?)</\1>', raw):
    print('   ', mm.group(1), repr(strip(mm.group(2)).strip()))
print('--- tail of page text:')
tail = [l.strip() for l in txt.split('\n') if l.strip()]
for l in tail[-14:]:
    print('   ', l[:200])
for needle in ['2006', 'Montes', 'Foundation', 'Revised', 'updated', 'Last']:
    for mm in re.finditer(needle, txt):
        print('   %r: ...%s...' % (needle, txt[max(0, mm.start()-60):mm.end()+60].replace('\n', ' / ')))
