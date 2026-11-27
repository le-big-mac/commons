"""Item 1 of the brief: the kept parts of the page on cooperation, compared by program.
usage: kept.py OLD_SOURCE NEW_SOURCE OLD_BUILT NEW_BUILT LOG_NEW
Reads only; prints to standard output."""
import re, sys, html

old_src, new_src, old_built, new_built, log_new = (open(p, encoding='utf-8').read() for p in sys.argv[1:6])


def part(a, b, s):
    i = s.index(a); return s[i:s.index(b, i)]


def text(h):
    """words of a piece of HTML, tags apart, alt texts kept as text, spaces squeezed"""
    h = re.sub(r'<img [^>]*alt="([^"]*)"[^>]*>', lambda m: ' [ALT: ' + m.group(1) + '] ', h)
    h = re.sub(r'<script.*?</script>', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return ' '.join(html.unescape(h).split())


print('== A. the three kept parts, letter for letter in the SOURCE ==')
for name, a, b in (('Why two defections and not one', '<h2>Why two defections and not one</h2>', '<h2>Watch it happen</h2>'),
                   ('A disagreement not settled', '<h2>A disagreement not settled</h2>', '<h2>How far to trust this</h2>')):
    o, n = part(a, b, old_src), part(a, b, new_src)
    print(f'{name!r}: old {len(o)} characters, new {len(n)}; identical: {o == n}')
o = part('<summary>For those who want to check</summary>', '</details>', old_src)
n = part('<summary>For those who want to check</summary>', '</details>', new_src)
print(f"'For those who want to check' (from its summary line to its closing tag): old {len(o)}, new {len(n)}; identical: {o == n}")
# the opening tag of that fold is the one thing changed in it
o_tag = re.search(r'<details[^>]*>\n<summary>For those who want to check', old_src).group(0)
n_tag = re.search(r'<details[^>]*>\n<summary>For those who want to check', new_src).group(0)
print('   its opening tag, old:', repr(o_tag.split('\n')[0]), ' new:', repr(n_tag.split('\n')[0]))
print('   old source ends with that fold:', old_src.rstrip().endswith('</details>'), '; in the new source it is followed by:', repr(new_src[new_src.index(n) + len(n):][:120]))

print()
print('== B. the paragraph on trying the live page ==')
m = re.search(r'<p>(You can <a href="files/bed\.html">open the bed</a> and try it\. It starts running by itself, with 3% of moves slipping, .*? it got in only by way of other machines\.)</p>\n', old_src, re.S)
bed = m.group(1)
print('in old source:', old_src.count(bed), 'time(s); in new source:', new_src.count(bed), 'time(s);', len(bed), 'characters,', len(text(bed).split()), 'words')
i = new_src.index(bed)
before_it = new_src[:i]
print('what stands just before it in the new source:', repr(before_it[-150:]))
print('what stands just after it:', repr(new_src[i + len(bed):][:30]))
d_open = before_it.rfind('<details'); d_close = before_it.rfind('</details>')
print('it is inside a <details> element:', d_open > d_close, '; that element:', repr(new_src[d_open:new_src.index('</summary>', d_open) + 10]))
print('first words:', repr(text(bed)[:40]), '; last words:', repr(text(bed)[-40:]))

print()
print('== C. the account of the readings ==')
m2 = re.search(r'<p class="small">(The live page and the short story among the files still call the machine the handshake\.) (Two fresh copies of the model read this page before it went up: .*?made by stepping the same machines\.)</p>\n', old_src, re.S)
acc = m2.group(2)
print('in old source:', old_src.count(acc), 'time(s); in new source:', new_src.count(acc), 'time(s);', len(acc), 'characters,', len(text(acc).split()), 'words')
i = new_src.index(acc)
before_it = new_src[:i]
d_open = before_it.rfind('<details'); d_close = before_it.rfind('</details>')
print('it is inside a <details> element:', d_open > d_close, '; that element:', repr(new_src[d_open:new_src.index('</summary>', d_open) + 10]))
last_details = new_src.rfind('<details')
print('that element is the last <details> of the source:', d_open == last_details, '; the source ends with </details>:', new_src.rstrip().endswith('</details>'))
print('first words:', repr(text(acc)[:60]), '; last words:', repr(text(acc)[-50:]))
print('the first sentence of the old small paragraph stands in the new open small paragraph:', new_src.count(m2.group(1)) == 1)
tail = new_src[i + len(acc):]
print('the new paragraphs after it are the log file, character for character:', tail.strip() == ('</p>\n' + log_new.strip() + '\n</details>').strip())

print()
print('== D. the same three parts and two pieces in the BUILT pages (words, tags apart) ==')
def built_fold(b, summary):
    i = b.index('<summary>' + summary + '</summary>'); j = b.index('</details>', i)
    return b[i:j]
for s in ('Why two defections and not one', 'A disagreement not settled', 'For those who want to check'):
    o, n = text(built_fold(old_built, s)), text(built_fold(new_built, s))
    print(f'{s!r}: old {len(o.split())} words, new {len(n.split())}; identical: {o == n}')
    if o != n:
        ow, nw = o.split(), n.split()
        import difflib
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ow, nw, autojunk=False).get_opcodes():
            if tag != 'equal': print('     ', tag, '| old:', ' '.join(ow[i1:i2]), '| new:', ' '.join(nw[j1:j2]))
print('bed paragraph (words) in new built page:', text(new_built).count(text(bed)), 'time(s); in old built page:', text(old_built).count(text(bed)))
print('account of the readings (words) in new built page:', text(new_built).count(text(acc)), 'time(s); in old built page:', text(old_built).count(text(acc)))
print('old built page has links of class tosec:', old_built.count('class="tosec"'), '; new built page:', new_built.count('class="tosec"'))
print('old built page, "See the picture at full size":', old_built.count('See the picture at full size'), '; new:', new_built.count('See the picture at full size'))

print()
print('== E. open text: sentences of the old page that are in the open text of the new page, or not ==')
def open_text(b):
    body = b[b.index('<h1'):b.index('<footer')] if '<footer' in b else b
    body = re.sub(r'<details.*?</details>', ' \n', body, flags=re.S)
    return body
def folded_text(b):
    body = b[b.index('<h1'):b.index('<footer')] if '<footer' in b else b
    return ' '.join(re.findall(r'<details.*?</details>', body, flags=re.S))
def sentences(h):
    # block by block, then sentence by sentence
    h = re.sub(r'<script.*?</script>', ' ', h, flags=re.S)
    h = re.sub(r'<img [^>]*alt="([^"]*)"[^>]*>', lambda m: '</p><p>[ALT] ' + m.group(1) + '</p><p>', h)
    blocks = re.split(r'</?(?:p|li|ul|h1|h2|h3|figure|figcaption|summary|details)[^>]*>', h)
    out = []
    for bl in blocks:
        t = ' '.join(html.unescape(re.sub(r'<[^>]+>', '', bl)).split())
        if not t: continue
        out += [s.strip() for s in re.split(r'(?<=[.?!])\s+(?=[A-Z"\[(])', t) if s.strip()]
    return out
old_open, new_open = sentences(open_text(old_built)), sentences(open_text(new_built))
new_open_all = ' '.join(new_open); new_fold_all = ' '.join(sentences(folded_text(new_built))); old_open_all = ' '.join(old_open)
print('old open text:', len(old_open), 'sentences,', len(' '.join(old_open).split()), 'words; new open text:', len(new_open), 'sentences,', len(new_open_all.split()), 'words')
print()
print('-- old open sentences NOT word for word in the new open text --')
k = 0
for s in old_open:
    if s not in new_open_all:
        k += 1
        print(f'[{k}] {s}')
        print('     word for word in a folded part of the new page:', s in new_fold_all)
print()
print('-- new open sentences NOT word for word in the old open text --')
k = 0
for s in new_open:
    if s not in old_open_all:
        k += 1
        print(f'[{k}] {s}')
        print('     word for word in a folded part of the old page:', s in ' '.join(sentences(folded_text(old_built))))
