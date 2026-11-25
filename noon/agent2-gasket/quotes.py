# quotes.py -- is every quotation in quotes.json in the fetched text it is said to come from?  (White space is not compared:
# the texts are machine conversions of PDFs, broken into lines.)   python -I quotes.py ~/gasket-data
import json, os, re, sys
here = os.path.dirname(os.path.abspath(__file__)); root = sys.argv[1]; q = json.load(open(os.path.join(here, 'quotes.json'), encoding='utf-8'))
norm = lambda s: re.sub(r'\s+', ' ', s).strip(); cache = {}; ok = 0
for e in q:
    t = cache.setdefault(e['file'], norm(open(os.path.join(root, e['file']), encoding='utf-8', errors='replace').read()))
    found = norm(e['text']) in t; ok += found; print(('found    ' if found else 'MISSING  ') + e['id'] + '  (' + e['file'] + ')')
print('\n%d of %d quotations found' % (ok, len(q))); sys.exit(0 if ok == len(q) else 1)
