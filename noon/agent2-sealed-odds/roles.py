"""Tokens by the kind of sub-agent, classed by a word in its first instruction (the instruction itself is not printed).   usage: python roles.py TRANSCRIPT..."""
import sys, json, statistics as st
rows = []
for path in sys.argv[1:]:
    seen = {}; first = None; t0 = t1 = None
    try: fh = open(path, encoding='utf-8', errors='replace')
    except OSError: continue
    for line in fh:
        try: o = json.loads(line)
        except Exception: continue
        if not isinstance(o, dict): continue
        if o.get('timestamp'): t0 = t0 or o['timestamp']; t1 = o['timestamp']
        m = o.get('message') or {}
        if not isinstance(m, dict): continue
        if first is None and m.get('role') == 'user':
            c = m.get('content'); first = c if isinstance(c, str) else " ".join(b.get('text', '') for b in c if isinstance(b, dict))
        if m.get('role') == 'assistant' and m.get('usage'): seen[m.get('id') or o.get('uuid')] = m['usage']
    if not seen: continue
    f = (first or '').lower()
    role = 'referee' if 'refere' in f else 'forecaster or reader' if ('forecaster' in f or 'reader' in f or 'price' in f) else 'other'
    rows.append((role, t0[:10], sum(u.get('output_tokens') or 0 for u in seen.values()), sum(u.get('cache_read_input_tokens') or 0 for u in seen.values())))
for role in ('referee', 'forecaster or reader', 'other'):
    r = [x for x in rows if x[0] == role]
    if not r: continue
    out = sorted(x[2] for x in r); cr = sorted(x[3] for x in r)
    print(f"{role:22s} {len(r):3d} sub-agents; output tokens: least {out[0]:,}, median {int(st.median(out)):,}, most {out[-1]:,}, together {sum(out):,}; cache read: median {int(st.median(cr)):,}, together {sum(cr):,}")
    for day in sorted({x[1] for x in r}):
        d = [x for x in r if x[1] == day]; print(f"      started {day}: {len(d):3d}; output {sum(x[2] for x in d):,}")
