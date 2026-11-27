"""Words that point up or down the page (above, below, foot, here ...), by the fold they stand in; and how many paragraphs
"dated 26 November" stand above the moved account's pointer "the paragraph above dated 26 November", on each page.
usage: python pointers.py PUBLIC_BUILT NEW_BUILT"""
import re, sys, html
for label, path in (('public page', sys.argv[1]), ('candidate', sys.argv[2])):
    s = open(path, encoding='utf-8').read()
    body = s[s.index('<h1>'):s.index('<footer>')]
    body = re.sub(r'<script.*?</script>', ' ', body, flags=re.S)
    m = re.search(r'the paragraph above dated 26 November', body)
    before = body[:m.start()]
    c = [re.sub(r'<[^>]+>', '', before[x.start():x.start() + 80]) for x in re.finditer(r'<p[^>]*>Added 26 November', before)]
    print(f'{label}: paragraphs above the pointer that begin "Added 26 November": {len(c)} {c}')
    if label != 'candidate':
        continue
    pos = 0; out = []
    for m in re.finditer(r'<details[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>', body, re.S):
        out.append(('open text', body[pos:m.start()])); out.append((re.sub(r'<[^>]+>', '', m.group(1)), m.group(2))); pos = m.end()
    out.append(('open text', body[pos:]))
    for where, chunk in out:
        t = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', chunk)).split())
        for m in re.finditer(r'\b(above|below|foot|further down|near the end|at the top|here)\b', t, re.I):
            print(f'[{where[:34]:34s}] ...{t[max(0, m.start() - 70):m.end() + 60]}...')
