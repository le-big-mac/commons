# quotes.py -- is every quotation in quotes.json in the fetched text it is said to come from?  White space and hyphens at line
# ends are not compared (the texts are machine conversions); a paper in two columns is looked for in two conversions of it.   python -I quotes.py ~/comb-data
import json, os, re, sys
here = os.path.dirname(os.path.abspath(__file__)); root = sys.argv[1]; q = json.load(open(os.path.join(here, 'quotes.json'), encoding='utf-8'))
norm = lambda s: re.sub(r'-\s+', '', re.sub(r'\s+', ' ', s)).replace(' ', '').strip(); cache = {}; ok = 0
for e in q:
    pieces = e.get('pieces') or [e.get('as_scanned') or e['text']]                 # a sentence broken by a table is looked for in its pieces; one misread by the scan, as scanned
    where = [f for f in e['files'] if all(norm(x) in cache.setdefault(f, norm(open(os.path.join(root, f), encoding='utf-8', errors='replace').read())) for x in pieces)]
    ok += bool(where); print(('found    ' if where else 'MISSING  ') + e['id'] + '  (' + (where[0] if where else ' or '.join(e['files'])) + ')')
print('\n%d of %d quotations found' % (ok, len(q))); sys.exit(0 if ok == len(q) else 1)
