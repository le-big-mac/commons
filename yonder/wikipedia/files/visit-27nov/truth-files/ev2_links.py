"""Evidence reading 2: every outside link of the second candidate with the words it stands on; compared with the first.
usage: python -I ev2_links.py candidate-2.html candidate-1.html"""
import sys, re, html
def links(p):
    c = open(p, encoding='utf-8').read()
    marks = [(m.start(), 1) for m in re.finditer(r'<details', c)] + [(m.start(), -1) for m in re.finditer(r'</details>', c)]
    out = []
    for m in re.finditer(r'<a href="([^"]+)">(.*?)</a>', c, flags=re.S):
        h = html.unescape(m.group(1))
        if not h.startswith('http'): continue
        out.append((h, re.sub(r'<[^>]+>', '', html.unescape(m.group(2))), 'fold' if sum(d for q, d in marks if q < m.start()) > 0 else 'OPEN'))
    return out
a, b = links(sys.argv[1]), links(sys.argv[2])
for h, w, f in a: print('  %s | %s | %s' % (f, w[:70], h))
print('outside links in the second candidate: %d, distinct addresses %d; in the first: %d, distinct %d' % (len(a), len(set(x[0] for x in a)), len(b), len(set(x[0] for x in b))))
print('addresses only in the second:', sorted(set(x[0] for x in a) - set(x[0] for x in b)), '; only in the first:', sorted(set(x[0] for x in b) - set(x[0] for x in a)))
d1 = {(h, f): w for h, w, f in b}
for h, w, f in a:
    if d1.get((h, f)) != w: print('  words changed on %s (%s): %r -> %r' % (h[-40:], f, d1.get((h, f)), w))
