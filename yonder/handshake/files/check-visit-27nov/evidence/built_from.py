"""Is the built candidate made of the candidate source, and the public built page of the old source? letters in order, tags and spaces apart.
usage: built_from.py SOURCE BUILT"""
import re, sys, html
src, built = (open(p, encoding='utf-8').read() for p in sys.argv[1:3])
letters = lambda h: ''.join(html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>', ' ', h, flags=re.S))).split())
body = built[built.index('<h1'):built.index('<footer')]
a, b = letters(src), letters(body)
b2 = b.replace('Seethepictureatfullsize.', '')
print(sys.argv[2], ': source', len(a), 'letters; built body', len(b), '; built body less the full-size links', len(b2), '; equal to the source:', a == b2)
