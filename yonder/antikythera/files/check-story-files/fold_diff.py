import re, difflib, sys
new = open('/home/agent3/site/build/pages/antikythera.html', encoding='utf-8').read()
old = open('/home/agent3/site/build/pages/antikythera-before-story.html', encoding='utf-8').read()
i = new.index('<details class="fold">')
fold = new[i:]
story = new[:i]
def sents(t):
    # split on tags and sentence ends for a fine diff
    t = re.sub(r'\s+', ' ', t)
    parts = re.split(r'(?<=[.!?:])\s+|(?=<)|(?<=>)', t)
    return [p.strip() for p in parts if p and p.strip()]
a = sents(old); b = sents(fold)
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal': continue
    print('====', tag)
    for x in a[i1:i2]: print('  OLD:', x)
    for x in b[j1:j2]: print('  NEW:', x)
