"""Probe the raw archived page (as data): capture markers, title, and the raw bytes
around the sentence quoted in the note. Usage: python -I raw_probe.py PAGE.html"""
import sys, re
raw = open(sys.argv[1], 'rb').read()
s = raw.decode('utf-8', errors='replace')
print('bytes', len(raw), 'replacement chars', s.count('�'))
for m in re.finditer(r'<title>(.*?)</title>', s, re.S | re.I):
    print('TITLE:', repr(m.group(1)))
for pat in [r'FILE ARCHIVED ON[^\n]{0,120}', r'web\.archive\.org/web/(\d{8,14})[a-z_]*/(http[^"\'\s<>]{0,150})', r'wbinfo[^\n]{0,200}', r'__wm\.wombat\([^\n]{0,200}', r'timestamp[^\n]{0,80}', r'<meta[^>]{0,200}>']:
    seen = {}
    for m in re.finditer(pat, s):
        k = m.group(0)
        seen[k] = seen.get(k, 0) + 1
    print('--', pat)
    for k, v in list(seen.items())[:25]:
        print('   %3d x %r' % (v, k[:260]))
i = s.find('In fact, his calculations')
print('index of sentence', i)
print(repr(s[i-250:i+400]))
j = s.find('King Mongkut')
print(repr(s[j-900:j+200]))
k = s.find('L. Robert Morris')
print(repr(s[k-400:k+400]))
