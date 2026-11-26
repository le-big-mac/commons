"""Probe the saved wikitext (as data): print context around given needles.
Usage: python -I wiki_probe.py PAGE.wiki"""
import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
print('chars', len(s))
for needle, before, after in [('by about two seconds', 500, 900), ('Montes-Bradley', 900, 1600), ('acknowledged as more precise', 500, 300)]:
    for m in re.finditer(re.escape(needle), s):
        i = m.start()
        print('=== %r at %d' % (needle, i))
        print(s[max(0, i-before):i+after])
        print()
