"""Print title, year, open-access links and reconstructed abstract from an OpenAlex works JSON file.
usage: openalex_show.py FILE.json"""
import sys, json
d = json.load(open(sys.argv[1], encoding='utf-8'))
print('meta:', {k: v for k, v in d.get('meta', {}).items() if k in ('count', 'per_page')})
for w in sorted(d['results'], key=lambda w: w.get('publication_year') or 0):
    print('=' * 100)
    print(w.get('publication_year'), '|', w.get('title'), '|', w.get('doi'), '| cited by', w.get('cited_by_count'), '|', w.get('id'))
    oa = w.get('open_access') or {}
    print('  oa:', oa.get('oa_status'), oa.get('oa_url'))
    for loc in (w.get('locations') or []):
        src = (loc.get('source') or {}).get('display_name')
        if loc.get('pdf_url') or loc.get('is_oa'):
            print('  loc:', src, '| oa', loc.get('is_oa'), '|', loc.get('pdf_url') or loc.get('landing_page_url'))
    inv = w.get('abstract_inverted_index')
    if inv:
        pos = {}
        for word, ps in inv.items():
            for p in ps: pos[p] = word
        print('  ABSTRACT:', ' '.join(pos[i] for i in sorted(pos)))
    else:
        print('  (no abstract in this record)')
