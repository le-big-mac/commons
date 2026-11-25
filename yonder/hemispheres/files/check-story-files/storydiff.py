import difflib, re
cur = open('/home/agent3/site/build/pages/hemispheres.html', encoding='utf-8').read()
first = open('/home/agent3/site/build/pages/hemispheres-story-as-first-read.html', encoding='utf-8').read()
def story(t):
    return t[:t.index('<details class="fold">')]
def sents(t):
    # split to sentences roughly
    t = re.sub(r'\n', ' \n', t)
    return [s for s in re.split(r'(?<=[.:?])\s+', t) if s.strip()]
a = sents(story(first)); b = sents(story(cur))
for l in difflib.unified_diff(a, b, 'as-first-read', 'current', lineterm='', n=0):
    print(l)
print('=== fold of as-first-read vs fold of current')
fa = first[first.index('<details class="fold">'):].splitlines()
fb = cur[cur.index('<details class="fold">'):].splitlines()
for l in difflib.unified_diff(fa, fb, 'as-first-read', 'current', lineterm='', n=0):
    print(l[:1500])
