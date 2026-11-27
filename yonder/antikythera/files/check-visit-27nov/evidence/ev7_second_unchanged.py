"""Second evidence reading, structure: what the second candidate keeps and what it changes.
usage: python ev7_second_unchanged.py PUBLIC CAND1 CAND2
Prints; writes nothing."""
import difflib
import html
import re
import sys

pub, c1, c2 = (open(p, encoding='utf-8').read() for p in sys.argv[1:4])
WHY_A, WHY_B = '<h2>Why 205 BC</h2>', '<h2>What is mine and what is not</h2>'
LONG_A = '<p class="small">What follows is the page as it stood until 25 November'


def between(s, a, b):
    i = s.index(a)
    return s[i:s.index(b, i)]


def text(h):
    h = re.sub(r'<img[^>]*alt="([^"]*)"[^>]*>', lambda m: ' [ALT: ' + m.group(1) + '] ', h)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', h)).split())


def worddiff(a, b, label):
    aw, bw = a.split(), b.split()
    sm = difflib.SequenceMatcher(None, aw, bw, autojunk=False)
    n = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        n += 1
        print(f'  {label} {tag}: OLD[{" ".join(aw[i1:i2])}]\n  {" " * len(label)} {" " * len(tag)}  NEW[{" ".join(bw[j1:j2])}]')
    return n


print('=== the long account, public page against second candidate (source, letter for letter) ===')
lp, l2 = between(pub, LONG_A, '</details>'), between(c2, LONG_A, '</details>')
sm = difflib.SequenceMatcher(None, lp, l2, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
print('number of places that differ:', len(ops))
for tag, i1, i2, j1, j2 in ops:
    print(f'  {tag}: public[{lp[i1:i2]!r}] candidate[{l2[j1:j2]!r}]  in: ...{l2[max(0, j1 - 90):j2 + 90]}...')
print('"<details" inside the long account:', l2.count('<details'), '| the first candidate\'s long account == the public one:', between(c1, LONG_A, '</details>') == lp)

print('\n=== "Why 205 BC", public page against second candidate ===')
wp, w2 = between(pub, WHY_A, WHY_B), between(c2, WHY_A, WHY_B)
sm = difflib.SequenceMatcher(None, wp, w2, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
print('number of places that differ:', len(ops))
for tag, i1, i2, j1, j2 in ops:
    print(f'  {tag}: public[{wp[i1:i2]!r}] candidate[{w2[j1:j2]!r}]  in: ...{w2[max(0, j1 - 60):j2 + 40]}...')


def open_text(s):
    top = s[:s.index('<details class="fold"')] if '<details class="fold"' in s else s
    # the small fold inside the open text is part of the open text for this count, marked
    a, b = top.index(WHY_A), top.index(WHY_B)
    return top[:a] + top[b:]


# the second candidate has a small fold inside the open text: find the first LARGE fold instead
def split_open(s):
    i = s.index('<details class="fold" id="for-those-who-want-to-check">') if 'id="for-those-who-want-to-check"' in s else s.index('<details class="fold">')
    top = s[:i]
    a, b = top.index(WHY_A), top.index(WHY_B)
    return top[:a] + top[b:]


op, o1, o2 = text(split_open(pub)), text(split_open(c1)), text(split_open(c2))
print('\nopen text in words (public, first candidate, second candidate):', len(op.split()), len(o1.split()), len(o2.split()))
small = re.search(r'<details class="fold small-fold"[^>]*>(.*?)</details>', split_open(c2), flags=re.S)
print('of the second candidate\'s, behind the small heading "What others had already found":', len(text(small.group(1)).split()), 'words')

print('\n=== open text, word by word: PUBLIC -> SECOND CANDIDATE ===')
n = worddiff(op, o2, 'pub->2')
print('places:', n)
print('\n=== open text, word by word: FIRST CANDIDATE -> SECOND CANDIDATE ===')
n = worddiff(o1, o2, '1->2')
print('places:', n)

print('\n=== the new folded section ===')
sec = c2[c2.index('<details class="fold" id="how-this-page-was-written-and-read">'):]
m = re.search(r'The papers are listed at the foot of the page\. (Two more fresh copies of the model read this rewrite: .*?)</p>', pub, re.S)
old_account = m.group(1)
print('the old account (source, letter for letter) is in the new fold:', old_account in sec, f'({len(text(old_account).split())} words)')
print('first candidate\'s fold up to its "Later on 27 November" == second candidate\'s:',
      c1[c1.index('<details class="fold" id="how-this-page-was-written-and-read">'):].split('<p>Later on 27 November')[0] == sec.split('<p>Later on 27 November')[0])

print('\n=== everything else ===')
# the second candidate with its open text, "Why 205 BC", the one word and the new fold set aside must equal the public page so treated
def rest(s):
    s = s.replace('<details class="fold" id="for-those-who-want-to-check">', '<details class="fold">')
    i = s.index('<details class="fold">')
    tail = s[i:]
    if 'id="how-this-page-was-written-and-read"' in tail:
        tail = tail[:tail.index('<details class="fold" id="how-this-page-was-written-and-read">')].rstrip() + '\n'
    return tail
print('the first large fold, whole, differs from the public one only in that word:', rest(c2).replace('in months without a solar glyph all passed', 'in months without a glyph all passed') == rest(pub))
for w in ('788', '992', '144 years', '13 of the 41', '27 of 38', '2,231', '262', '98°', '0.12'):
    print(f'   {w!r} in the open text of: public {op.count(w)}, first candidate {o1.count(w)}, second candidate {o2.count(w)}')
