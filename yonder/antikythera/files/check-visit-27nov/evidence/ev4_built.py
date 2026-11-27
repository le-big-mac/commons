"""Evidence reading: the candidate as built against the public copy as built, fold by fold; the list under
"What is mine and what is not"; where the section links fall.
usage: python ev4_built.py PUBLIC_INDEX PREVIEW_INDEX OLD_SOURCE NEW_SOURCE
Prints; writes nothing."""
import html
import re
import sys

pub, pre, old_src, new_src = (open(p, encoding='utf-8').read() for p in sys.argv[1:5])


def letters(h):
    h = re.sub(r'<script>.*?</script>', ' ', h, flags=re.S)
    return ''.join(html.unescape(re.sub(r'<[^>]+>', ' ', h)).split())


def text(h):
    h = re.sub(r'<script>.*?</script>', ' ', h, flags=re.S)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', h)).split())


def folds(h):
    out = {}
    for m in re.finditer(r'<details class="fold"[^>]*>\n<summary>(.*?)</summary>(.*?)</details>', h, flags=re.S):
        out[m.group(1)] = m.group(2)
    return out


fp, fn = folds(pub), folds(pre)
print('folds in the public copy:', list(fp)); print('folds in the preview:    ', list(fn))
for name in fp:
    a, b = fp[name], fn[name]
    print(f'"{name}": letters in order identical (tags and spaces apart): {letters(a) == letters(b)} ({len(letters(a))} letters); '
          f'section links inside it in the preview: {len(re.findall("class=.tosec.", b))}; other differences in tags: '
          f'{sorted(set(re.findall(r"<[^>]+>", b)) - set(re.findall(r"<[^>]+>", a)))[:12]}')
    print('    alt texts identical:', re.findall(r'alt="([^"]*)"', a) == re.findall(r'alt="([^"]*)"', b), '| hrefs identical:', re.findall(r'href="([^"]*)"', a) == re.findall(r'href="([^"]*)"', b))
name = 'How this page was written and read'
print(f'"{name}": section links inside it:', re.findall(r'<a class="tosec" href="#([^"]*)">', fn[name]))
open_pre = re.sub(r'<details class="fold".*?</details>', ' [FOLD] ', pre, flags=re.S)
print('section links in the open text of the preview:', re.findall(r'<a class="tosec" href="#([^"]*)">', open_pre))
print('ids in the preview that the links need:', {i: (f'id="{i}"' in pre) for i in set(re.findall(r'<a class="tosec" href="#([^"]*)">', pre))})
print('TODO left in the preview:', re.findall(r'[^.>]*TODO[^.<]*', text(pre)))

print('\n--- "What is mine and what is not": the old paragraph against the new list ---')
o = old_src[old_src.index('<h2>What is mine and what is not</h2>'):old_src.index('<h2>How far to trust this</h2>')]
n = new_src[new_src.index('<h2>What is mine and what is not</h2>'):new_src.index('<h2>How far to trust this</h2>')]
to, tn = text(o), text(n)
ADD = ' of the day or night engraved beside the dial\'s marks'
print('new text has the added words once:', tn.count(ADD))
print('new text with the added words taken out == old text:', tn.replace(ADD, '') == to)
items = re.findall(r'<li>(.*?)</li>', n, flags=re.S)
print('list items:', len(items), '| each is one sentence of the old paragraph (after taking the added words out):',
      [it.replace(ADD, '') in to for it in items], '| sentences per item:', [len(re.findall(r'[.](?:\s|$)', it)) for it in items])

print('\n--- the three places that said "at the foot of the page" ---')
print('old source:', old_src.count('at the foot of the page'), '+ "at the foot," in the line under the title:', old_src.count('is at the foot, under'), '| new source, open text:', new_src[:new_src.index('<details')].count('at the foot'))
long_new = new_src[new_src.index('<details class="fold" id="for-those-who-want-to-check">'):new_src.index('<details class="fold" id="how-this-page-was-written-and-read">')]
for what in ('<h2>What I got wrong on the way</h2>', '<h2>Sources and files</h2>', 'Three of the 37 expectations failed', 'Two of the eight expectations for the hours failed'):
    print(f'in the fold "For those who want to check": {what!r}: {long_new.count(what)}')
print('links in that fold:', re.findall(r'<a href="([^"]*)">(.*?)</a>', long_new))
print('"longer account" in the new open text (folds apart, "Why 205 BC" apart):',
      text(re.sub(r'<h2>Why 205 BC</h2>.*?(?=<h2>)', ' ', new_src[:new_src.index('<details')], flags=re.S)).count('longer account'),
      '| in "Why 205 BC":', text(new_src[new_src.index('<h2>Why 205 BC</h2>'):new_src.index('<h2>What is mine')]).count('longer account'))
print('"2,231" in the new open text:', new_src[:new_src.index('<details')].count('2,231'), '| "two thousand two hundred":', new_src[:new_src.index('<details')].count('two thousand two hundred'))
