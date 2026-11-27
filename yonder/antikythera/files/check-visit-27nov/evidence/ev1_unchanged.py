"""Evidence reading, part 1: what is unchanged, and which old open sentences are gone.
usage: python ev1_unchanged.py OLD NEW
Compares the two page sources. Writes nothing; prints."""
import difflib
import hashlib
import html
import re
import sys

old = open(sys.argv[1], encoding='utf-8').read()
new = open(sys.argv[2], encoding='utf-8').read()


def between(s, a, b):
    i = s.index(a)
    j = s.index(b, i)
    return s[i:j]


def sha(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


# --- 1a. the two kept parts, letter for letter ---------------------------------
WHY_A, WHY_B = '<h2>Why 205 BC</h2>', '<h2>What is mine and what is not</h2>'
LONG_A = '<p class="small">What follows is the page as it stood until 25 November'
for name, a, b in (('Why 205 BC', WHY_A, WHY_B), ('long account', LONG_A, '</details>')):
    assert old.count(a) == 1 and new.count(a) == 1, (name, old.count(a), new.count(a))
    po, pn = between(old, a, b), between(new, a, b)
    print(f'{name}: old {len(po)} chars sha {sha(po)}; new {len(pn)} chars sha {sha(pn)}; identical: {po == pn}')

# the long account must run to the true end of the old page, and in the new page to the end of the first <details>
long_old = between(old, LONG_A, '</details>')
tail_old = old[old.index(LONG_A) + len(long_old):]
print('old page after the long account:', repr(tail_old))
long_new = between(new, LONG_A, '</details>')
tail_new = new[new.index(LONG_A) + len(long_new):]
print('new page after the long account begins:', repr(tail_new[:120]))
print('number of </details> in old, new:', old.count('</details>'), new.count('</details>'))
print('number of <details in old, new:', old.count('<details'), new.count('<details'))
# is there a nested details inside the long account (which would cut "between" short)?
print('"<details" inside the long account (old, new):', long_old.count('<details'), long_new.count('<details'))

# the wrapper line just before the long account
for nm, s in (('old', old), ('new', new)):
    i = s.index(LONG_A)
    print(nm, 'text just before the long account:', repr(s[max(0, i - 140):i]))


# --- 1b. open text, sentence by sentence -----------------------------------------
def strip_tags(s):
    # alt texts are kept as text of their own, marked
    s = re.sub(r'<img[^>]*alt="([^"]*)"[^>]*>', lambda m: ' [ALT: ' + m.group(1) + '] ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def open_text(s):
    """All of the page source that is not inside the long account, the 'Why 205 BC' section,
    or (new page) the second folded section."""
    i = s.index('<details class="fold"')
    top = s[:i]
    a, b = top.index(WHY_A), top.index(WHY_B)
    return top[:a] + top[b:], top[a:b]


def sentences(txt):
    # split after . ? ! followed by space and a capital, quote or bracket; keep it simple and then look by eye
    parts = re.split(r'(?<=[.?!])\s+(?=[A-Z"“\[(])', txt)
    return [p.strip() for p in parts if p.strip()]


o_open_html, o_why = open_text(old)
n_open_html, n_why = open_text(new)
o_open, n_open = strip_tags(o_open_html), strip_tags(n_open_html)
print('\nopen text, words (old, new):', len(o_open.split()), len(n_open.split()))
print('Why 205 BC, words (old, new):', len(strip_tags(o_why).split()), len(strip_tags(n_why).split()))

so, sn = sentences(o_open), sentences(n_open)
set_n = set(sn)
set_o = set(so)
print(f'\nold open sentences: {len(so)}; new open sentences: {len(sn)}')
print('\n=== OLD open sentences that are not, whole, in the new open text ===')
for k, s_ in enumerate(so):
    if s_ not in set_n:
        inside = s_ in n_open
        print(f'[{k}] (as a run of characters still in the new open text: {inside})\n    {s_}')
print('\n=== NEW open sentences that are not, whole, in the old open text ===')
for k, s_ in enumerate(sn):
    if s_ not in set_o:
        inside = s_ in o_open
        print(f'[{k}] (as a run of characters in the old open text: {inside})\n    {s_}')

# --- 1c. word-level diff of the open text ----------------------------------------
print('\n=== word-level diff of the open text (old -> new) ===')
ow, nw = o_open.split(), n_open.split()
sm = difflib.SequenceMatcher(None, ow, nw, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    print(f'{tag}: OLD[{" ".join(ow[i1:i2])}]\n      NEW[{" ".join(nw[j1:j2])}]')

# --- 1d. the new second fold ------------------------------------------------------
second = new[new.index('<details class="fold" id="how-this-page-was-written-and-read">'):]
sec_txt = strip_tags(second)
# the old account, as it stood in the old small paragraph
m = re.search(r'The papers are listed at the foot of the page\. (Two more fresh copies of the model read this rewrite: .*?)</p>', old, re.S)
old_account = strip_tags(m.group(1))
print('\nold account (words):', len(old_account.split()))
print('old account is, word for word, inside the new second fold:', old_account in sec_txt)
i = sec_txt.index(old_account)
print('second fold before the old account:', repr(sec_txt[:i]))
print('second fold after the old account begins:', repr(sec_txt[i + len(old_account):][:80]))

# --- 1e. everything outside the open text and the two folds: is anything else different? -------
# rebuild: new page with every swap undone must equal old; cheaper: compare the page minus (open text) minus (second fold)
new_wo_second = new[:new.index('<details class="fold" id="how-this-page-was-written-and-read">')].rstrip() + '\n'
i_o, i_n = old.index('<details class="fold"'), new.index('<details class="fold"')
fold_o, fold_n = old[i_o:], new_wo_second[i_n:]
print('\nfirst fold, whole (with its summary line), old == new apart from the id:',
      fold_o == fold_n.replace('<details class="fold" id="for-those-who-want-to-check">', '<details class="fold">'))
print('old ends with:', repr(old[-40:]), '| new without second fold ends with:', repr(new_wo_second[-40:]))
