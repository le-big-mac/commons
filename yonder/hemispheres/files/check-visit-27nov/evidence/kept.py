"""Kept parts and moved pieces: old source against new source, and new source against the page as built.
usage: python kept.py OLD_SRC NEW_SRC NEW_BUILT [OLD_BUILT]
Written independently of build/hemi_visit.py: the bounds are taken from the brief's words, not from that script's patterns."""
import re, sys, html, hashlib

old = open(sys.argv[1], encoding='utf-8').read()
new = open(sys.argv[2], encoding='utf-8').read()
built = open(sys.argv[3], encoding='utf-8').read()
old_built = open(sys.argv[4], encoding='utf-8').read() if len(sys.argv) > 4 else None


def sha(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


def between(s, a, b, include_b=False):
    assert s.count(a) == 1, (s.count(a), a)
    i = s.index(a)
    j = s.index(b, i)
    return s[i:j + (len(b) if include_b else 0)]


def text(s):
    """visible text: tags out (alt texts are kept apart), entities decoded, white space single"""
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r' ?<a class="fullsize"[^>]*>See the picture at full size\.</a>', '', s)   # the build adds these links; counted apart
    s = re.sub(r'</?(a|code|em|strong)\b[^>]*>', '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return ' '.join(html.unescape(s).split())


ok = True


def say(label, cond, extra=''):
    global ok
    ok = ok and bool(cond)
    print(('PASS  ' if cond else 'FAIL  ') + label + (('  ' + extra) if extra else ''))


print('== 1. the long account, from "What follows is the page as it stood until 25 November" to the end of its fold')
a = 'What follows is the page as it stood until 25 November'
lo, ln = between(old, a, '</details>'), between(new, a, '</details>')
say('long account identical byte for byte in old and new source', lo == ln, f'{len(lo)} characters, sha {sha(lo)} / {sha(ln)}')
# and the paragraph tag before it, and the whole <details> block but for its opening tag
lo2 = between(old, '<summary>For those who want to check</summary>', '</details>', True)
ln2 = between(new, '<summary>For those who want to check</summary>', '</details>', True)
say('whole fold "For those who want to check" from its <summary> to </details> identical', lo2 == ln2, f'{len(lo2)} characters')
print('      opening tag old:', re.search(r'<details[^>]*>\s*<summary>For those who want to check', old).group(0).split('\n')[0],
      '| new:', re.search(r'<details[^>]*>\s*<summary>For those who want to check', new).group(0).split('\n')[0])

print('== 2. "And woodpeckers"')
wo, wn = between(old, '<h2>And woodpeckers</h2>', '<h2>Turn it yourself</h2>'), between(new, '<h2>And woodpeckers</h2>', '<h2>Turn it yourself</h2>')
say('section "And woodpeckers" identical byte for byte', wo == wn, f'{len(wo)} characters, sha {sha(wo)}')

print('== 3. "The half with the most people"')
po, pn = between(old, '<h2>The half with the most people</h2>', '<h2>And woodpeckers</h2>'), between(new, '<h2>The half with the most people</h2>', '<h2>And woodpeckers</h2>')
say('sections differ', po != pn)
# the only difference: one "</p>\n<p>" where there was one space
import difflib
sm = difflib.SequenceMatcher(None, po, pn, autojunk=False)
ops = [(tag, po[i1:i2], pn[j1:j2]) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
print('      differences (old -> new):', [(t, o, n) for t, o, n in ops])
say('exactly one difference, a space replaced by a paragraph break', len(ops) == 1 and ops[0][1] in (' ', '') and ops[0][2].strip() in ('</p>\n<p>', '</p><p>') ,)
say('same text when tags are taken out', text(po) == text(pn))
i = pn.index('</p>\n<p>The population maps I used show')
print('      the break falls after:', repr(pn[i - 60:i]), '| before:', repr(pn[i + 8:i + 50]))

print('== 4. five moved pieces: once in old source, once in new source, once in the built page')
dates = 'Work of 21 November 2026, rewritten on 25 November to be shorter and plainer, and corrected in a few sentences on 26 November after a search for earlier work.'
caution = between(old, "And the move of the people's centre", 'just inside it.', True)
added26 = between(old, '<p>Added 26 November. ', '</p>', False)[3:]
on27 = between(old, '<p>On 27 November the dates under the title were moved', '</p>', False)[3:]
readings = between(old, 'Two fresh copies of the same model read this rewrite', 'prior-art.md</a>).', True)
for name, piece in (('dates line', dates), ('second caution', caution), ('"Added 26 November."', added26), ('"On 27 November the dates..."', on27), ('account of the readings', readings)):
    print(f'      {name}: {len(piece)} characters, {len(text(piece).split())} words; begins {text(piece)[:50]!r}; ends {text(piece)[-45:]!r}')
    say(f'{name}: once in old source', old.count(piece) == 1)
    say(f'{name}: once in new source', new.count(piece) == 1)
    say(f'{name}: once in the built page (as text)', text(built).count(text(piece)) == 1, f'count {text(built).count(text(piece))}')
    # no partial second copy: the first 60 characters of the piece occur once
    say(f'{name}: its first 100 characters occur once in new source', new.count(piece[:100]) == 1, f'count {new.count(piece[:100])}; first 60: count {new.count(piece[:60])} (the short caution in the open begins with the same 65 characters)' if name == 'second caution' else f'count {new.count(piece[:100])}')

print('== 5. where the moved pieces now stand (inside which <details>)')


def enclosing(s, piece):
    i = s.index(piece)
    stack = []
    for m in re.finditer(r'<details[^>]*>|</details>', s[:i]):
        if m.group(0).startswith('</'):
            stack.pop()
        else:
            stack.append(m.end())
    out = []
    for e in stack:
        mm = re.match(r'\s*<summary>(.*?)</summary>', s[e:], re.S)
        out.append(text(mm.group(1)) if mm else '?')
    return out


for name, piece in (('dates line', dates), ('second caution', caution), ('"Added 26 November."', added26), ('"On 27 November the dates..."', on27), ('account of the readings', readings)):
    print(f'      {name}: new source {enclosing(new, piece)}; built {enclosing(built, text(piece)[:100] if '<' not in piece[:100] else piece[:40])}')

print('== 6. the built page against the new source (text of the body, tags out)')
body = between(built, '<h1>', '<script>')
tb, tn = text(body), text(new)
say('built text == source text', tb == tn, f'{len(tb)} / {len(tn)} characters')
if tb != tn:
    sm = difflib.SequenceMatcher(None, tb, tn, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'equal':
            print('      ', tag, repr(tb[max(0, i1 - 40):i2 + 20]), '->', repr(tn[max(0, j1 - 40):j2 + 20]))
print('      full-size links: built', len(re.findall(r'class="fullsize"', built)), '| source', len(re.findall(r'class="fullsize"', new)), '| public page', len(re.findall(r'class="fullsize"', old_built or '')))
print('      links to sections (class tosec) in built:', [(m.group(1), text(m.group(2))) for m in re.finditer(r'<a class="tosec" href="([^"]*)">(.*?)</a>', built)])
ids = set(re.findall(r'id="([^"]*)"', built))
say('every section link points at an id that exists in the built page', all(m[1:] in ids for m in re.findall(r'<a class="tosec" href="([^"]*)"', built)))
alts_b = re.findall(r'alt="([^"]*)"', body)
alts_n = re.findall(r'alt="([^"]*)"', new)
alts_o = re.findall(r'alt="([^"]*)"', old)
say('alt texts: built == new source', alts_b == alts_n, f'{len(alts_b)} pictures')
say('alt texts: new source == old source', alts_n == alts_o)

if old_built:
    print('== 7. the page now public (built) against the old source')
    ob = between(old_built, '<h1>', '<footer>')
    ob = re.sub(r'<script.*?</script>', ' ', ob, flags=re.S)
    to_, ts = text(ob), text(old)
    say('public built text == old source text', to_ == ts, f'{len(to_)} / {len(ts)} characters')
    if to_ != ts:
        sm = difflib.SequenceMatcher(None, to_, ts, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != 'equal':
                print('      ', tag, repr(to_[max(0, i1 - 40):i2 + 20]), '->', repr(ts[max(0, j1 - 40):j2 + 20]))
    print('      folds in the public page:', [text(x) for x in re.findall(r'<summary>(.*?)</summary>', old_built, re.S)])
    print('      folds in the candidate  :', [text(x) for x in re.findall(r'<summary>(.*?)</summary>', built, re.S)])
    m1 = re.search(r'<meta name="description" content="([^"]*)"', old_built); m2 = re.search(r'<meta name="description" content="([^"]*)"', built)
    say('meta description unchanged', m1 and m2 and m1.group(1) == m2.group(1))
    print('      meta description:', m2.group(1) if m2 else None)

print('ALL PASS' if ok else 'SOME FAILED')
