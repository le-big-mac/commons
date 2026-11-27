"""Lists, from my own transcript, the search requests made after a given UTC time, word for word.  usage: search_record.py TRANSCRIPT SINCE-ISO"""
import sys, json
qs = []
for line in open(sys.argv[1], encoding='utf-8', errors='replace'):
    try: o = json.loads(line)
    except Exception: continue
    if not isinstance(o, dict) or o.get('timestamp', '') < sys.argv[2]: continue
    m = o.get('message'); c = m.get('content') if isinstance(m, dict) else None
    if not isinstance(c, list): continue
    for b in c:
        if isinstance(b, dict) and b.get('type') == 'tool_use' and b.get('name') in ('WebSearch', 'WebFetch'):
            i = b.get('input', {}); qs.append((o['timestamp'][11:16], b['name'], i.get('query') or i.get('url'), i.get('mode', '')))
for t, n, q, mode in qs: print(f'{t}\t{n}\t{mode}\t{q}')
