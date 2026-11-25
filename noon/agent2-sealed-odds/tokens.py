"""What a sub-agent used, from the usage records in its transcript (no text is printed).   usage: python tokens.py TRANSCRIPT...
Sums input, output and cache tokens over distinct assistant messages; prints first and last timestamps."""
import sys, json
T = {}
for path in sys.argv[1:]:
    seen = {}; ts = []
    try: fh = open(path, encoding='utf-8', errors='replace')
    except OSError: continue
    for line in fh:
        try: o = json.loads(line)
        except Exception: continue
        if not isinstance(o, dict): continue
        if o.get('timestamp'): ts.append(o['timestamp'])
        m = o.get('message') or {}
        if isinstance(m, dict) and m.get('role') == 'assistant' and m.get('usage'):
            seen[m.get('id') or o.get('uuid')] = m['usage']
    tot = {k: sum((u.get(k) or 0) for u in seen.values()) for k in ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')}
    if not seen: continue
    print(f"{path.split('/')[-1][:20]:20s} {ts[0][5:16] if ts else '':11s} to {ts[-1][5:16] if ts else '':11s} messages {len(seen):4d}  output {tot['output_tokens']:9,d}  input {tot['input_tokens']:8,d}  cache written {tot['cache_creation_input_tokens']:10,d}  cache read {tot['cache_read_input_tokens']:11,d}")
    for k, v in tot.items(): T[k] = T.get(k, 0) + v
print("together:", {k: f"{v:,}" for k, v in T.items()})
