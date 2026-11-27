"""Second candidate of the page on cooperation: the kept parts, the reordered opening, the full list, and what differs from the first candidate.
usage: second.py PUBLIC_SOURCE CANDIDATE1_SOURCE CANDIDATE2_SOURCE PUBLIC_BUILT CANDIDATE2_BUILT LOG2
Reads only; prints to standard output."""
import re, sys, html, difflib

pub, c1, c2, pub_built, c2_built, log2 = (open(p, encoding='utf-8').read() for p in sys.argv[1:7])


def part(a, b, s):
    i = s.index(a); return s[i:s.index(b, i)]


def text(h):
    h = re.sub(r'<img [^>]*alt="([^"]*)"[^>]*>', lambda m: ' [ALT: ' + m.group(1) + '] ', h)
    h = re.sub(r'<script.*?</script>', ' ', h, flags=re.S)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', h)).split())


letters = lambda h: ''.join(text(h).split())

print('== A. kept parts, public source against second candidate, letter for letter ==')
for name, a, b in (('Why two defections and not one', '<h2>Why two defections and not one</h2>', '<h2>Watch it happen</h2>'),
                   ('A disagreement not settled', '<h2>A disagreement not settled</h2>', '<h2>How far to trust this</h2>'),
                   ('For those who want to check', '<summary>For those who want to check</summary>', '</details>')):
    o, n = part(a, b, pub), part(a, b, c2)
    print(f'{name!r}: {len(o)} and {len(n)} characters; identical: {o == n}')
bed = re.search(r'<p>(You can <a href="files/bed\.html">open the bed</a> and try it\. It starts running by itself, with 3% of moves slipping, .*? it got in only by way of other machines\.)</p>\n', pub, re.S).group(1)
acc = re.search(r'<p class="small">(The live page and the short story among the files still call the machine the handshake\.) (Two fresh copies of the model read this page before it went up: .*?made by stepping the same machines\.)</p>\n', pub, re.S).group(2)
for name, piece in (('the paragraph on trying the live page', bed), ('the account of the readings', acc)):
    i = c2.index(piece); d_open = c2[:i].rfind('<details'); d_close = c2[:i].rfind('</details>')
    print(f'{name}: in second candidate {c2.count(piece)} time(s); inside a fold: {d_open > d_close}; fold heading: {re.search(r"<summary>(.*?)</summary>", c2[d_open:]).group(1)!r}')
tail = c2[c2.index(acc) + len(acc):]
print('what follows the account is the second log file, character for character:', tail.strip() == ('</p>\n' + log2.strip() + '\n</details>').strip())

print()
print('== B. the opening ==')
old_lede = re.search(r'<p class="lede">(.*?)</p>', pub, re.S).group(1)
split = lambda t: [s.strip() for s in re.split(r'(?<=[.?])\s+(?=[A-Z])', t) if s.strip()]
old_s = split(old_lede)
p1 = re.search(r'<p class="lede">(.*?)</p>', c2, re.S).group(1)
rest = c2[c2.index('<p class="lede">'):c2.index('<h2>The machine</h2>')]
paras = re.findall(r'<p[^>]*>(.*?)</p>', rest, re.S)
print('paragraphs before "The machine":', len(paras))
for k, p in enumerate(paras): print(f'  paragraph {k + 1}: {len(text(p).split())} words; begins {text(p)[:50]!r}')
print('old opening, sentence by sentence:')
for k, s in enumerate(old_s): print(f'  [{k + 1}] {s}')
new1 = split(p1)
print('first new paragraph is old sentences in the order:', [old_s.index(s) + 1 if s in old_s else None for s in new1], '(None = not word for word an old sentence)')
p2, p3 = text(paras[1]), text(paras[2])
print('third new paragraph is old sentences:', [old_s.index(s) + 1 if s in old_s else None for s in split(p3)])
print('second new paragraph, sentence by sentence against the old:')
for s in split(p2):
    print('   ', 'OLD ' if s in old_s else 'NEW ', s)
# what was added inside the old sentence 5/6
o56 = [s for s in old_s if s.startswith('I let a hundred')][0]
n56 = [s for s in split(p2) if s.startswith('I let a hundred')][0]
print('the old sentence "I let a hundred..." less its full stop is the start of the new one:', n56.startswith(o56[:-1]), '; what was added:', repr(n56[len(o56) - 1:]))

print()
print('== C. the list of what was already known ==')
def ul_after(s, marker):
    i = s.index(marker); j = s.index('<ul>', i); k = s.index('</ul>', j) + len('</ul>\n')
    return s[j:k]
pub_list = ul_after(pub, '<p>Nearly all of it.</p>')
c1_list = ul_after(c1, '<p>Nearly all of it.</p>')
short = ul_after(c2, '<p>Nearly all of it.</p>')
full = ul_after(c2, '<summary>The same list in full, with what each found and how much of each I read</summary>')
print('full list in the second candidate == the first candidate\'s list, character for character:', full == c1_list, '; it stands', c2.count(full), 'time(s)')
print('the full list is inside the fold headed:', repr(re.search(r'<summary>(.*?)</summary>', c2[c2[:c2.index(full)].rfind('<details'):]).group(1)))
a, b = text(pub_list).split(), text(full).split()
print('full list against the public page\'s list, word by word:')
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag != 'equal': print('    ', tag, '| public:', ' '.join(a[i1:i2]), '| now:', ' '.join(b[j1:j2]))
print('short lines against full lines (what each short line leaves out):')
sl = re.findall(r'<li>(.*?)</li>', short, re.S); fl = re.findall(r'<li>(.*?)</li>', full, re.S)
for s, f in zip(sl, fl):
    ts, tf = text(s), text(f)
    print('  SHORT:', ts)
    if ts == tf: print('      (the same as the full line)')
    else:
        aw, bw = tf.split(), ts.split()
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, aw, bw, autojunk=False).get_opcodes():
            if tag != 'equal': print('      ', tag, '| full:', ' '.join(aw[i1:i2]), '| short:', ' '.join(bw[j1:j2]))

print()
print('== D. first candidate to second, sentence by sentence (all of the page, folds included) ==')
def sentences(h):
    h = re.sub(r'<img [^>]*alt="([^"]*)"[^>]*>', lambda m: '</p><p>[ALT] ' + m.group(1) + '</p><p>', h)
    out = []
    for bl in re.split(r'</?(?:p|li|ul|h1|h2|h3|figure|figcaption|summary|details)[^>]*>', h):
        t = ' '.join(html.unescape(re.sub(r'<[^>]+>', '', bl)).split())
        if t: out += [s.strip() for s in re.split(r'(?<=[.?!])\s+(?=[A-Z"\[(])', t) if s.strip()]
    return out
s1, s2 = sentences(c1), sentences(c2)
from collections import Counter
k1, k2 = Counter(s1), Counter(s2)
print('-- in the first candidate, not (or fewer times) in the second --')
for s in dict.fromkeys(s1):
    if k1[s] > k2[s]: print(f'   [{k1[s]}->{k2[s]}] {s}')
print('-- in the second candidate, not (or fewer times) in the first --')
for s in dict.fromkeys(s2):
    if k2[s] > k1[s]: print(f'   [{k1[s]}->{k2[s]}] {s}')

print()
print('== E. the built second candidate ==')
body = c2_built[c2_built.index('<h1'):c2_built.index('<footer')]
b2 = letters(body).replace('Seethepictureatfullsize.', '')
print('built body less the full-size links == second candidate source, letters in order:', letters(c2) == b2)
print('folded sections, in order:', re.findall(r'<details[^>]*>\n?<summary>(.*?)</summary>', c2_built))
open_part = re.sub(r'<details.*?</details>', ' ', body, flags=re.S)
names = re.findall(r'<h2[^>]*>(.*?)</h2>', c2_built) + re.findall(r'<summary>(.*?)</summary>', c2_built)
for n in names:
    q = '"' + n + '"'
    total = text(open_part).count(q); linked = len(re.findall(r'<a class="tosec"[^>]*>' + re.escape(q) + '</a>', open_part))
    if total: print(f'   open text names {q}: {total} time(s), of which a link: {linked}')
for href in sorted(set(re.findall(r'class="tosec" href="#([^"]+)"', c2_built))): print('   link target', href, 'exists:', ('id="' + href + '"') in c2_built)
print('"See the picture at full size" in the built page:', c2_built.count('See the picture at full size'), '; in the public built page:', pub_built.count('See the picture at full size'))
fold1 = c2_built[c2_built.index('<summary>Why two defections and not one</summary>'):]; fold1 = fold1[:fold1.index('</details>')]
print('the fold "Why two defections and not one" has the full-size link:', 'See the picture at full size' in fold1)

print()
print('== F. open text of the public page not word for word in the open text of the second candidate ==')
def open_sents(b):
    bb = b[b.index('<h1'):b.index('<footer')]
    return sentences(re.sub(r'<script.*?</script>', ' ', re.sub(r'<details.*?</details>', ' \n', bb, flags=re.S), flags=re.S))
def fold_sents(b):
    bb = b[b.index('<h1'):b.index('<footer')]
    return ' '.join(sentences(' '.join(re.findall(r'<details.*?</details>', bb, flags=re.S))))
po, no = open_sents(pub_built), open_sents(c2_built)
no_all = ' '.join(no); nf = fold_sents(c2_built)
print('public open text:', len(' '.join(po).split()), 'words; second candidate open text:', len(no_all.split()), 'words')
k = 0
for s in po:
    if s not in no_all:
        k += 1; print(f'[{k}] {s}\n      word for word in a fold of the second candidate: {s in nf}')
