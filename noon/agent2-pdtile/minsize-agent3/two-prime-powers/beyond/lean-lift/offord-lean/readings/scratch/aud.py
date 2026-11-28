import sys, json, re
p = sys.argv[1]
hits = {}
with open(p, encoding='utf-8') as f:
    for line in f:
        try: r = json.loads(line)
        except Exception: continue
        m = r.get('message', {})
        c = m.get('content')
        if not isinstance(c, list): continue
        for x in c:
            if isinstance(x, dict) and x.get('type') == 'tool_use':
                s = json.dumps(x.get('input', {}))
                for k in ('offord-A', 'offord-B', 'offord-all', 'offord-post', 'offord-clean', 'lake build', 'lake update', 'lake clean'):
                    if re.search(re.escape(k) + r'(?![a-z-])', s):
                        hits.setdefault(k, []).append((r.get('timestamp'), s[:160]))
for k, v in hits.items():
    print(k, len(v))
    for t, s in v[:4]: print('   ', t, s)
print('done')
