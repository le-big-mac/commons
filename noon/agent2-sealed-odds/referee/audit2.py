"""Referee's own audit of a forecaster transcript (read only).  usage: audit2.py TRANSCRIPT [maxchars]
Prints, in order: timestamp, role, and for each content block its type; tool calls in full (bounded); sizes of tool results;
total characters of readable text / thinking; and where the strings named on the command line occur."""
import sys, json
path = sys.argv[1]; lim = int(sys.argv[2]) if len(sys.argv) > 2 else 700
n = 0; kinds = {}
first = last = None
for line in open(path, encoding='utf-8', errors='replace'):
    try:
        o = json.loads(line)
    except Exception:
        print('UNPARSEABLE LINE', len(line)); continue
    n += 1
    ts = o.get('timestamp', '')
    if ts:
        first = first or ts; last = ts
    msg = o.get('message') or {}
    role = msg.get('role') or o.get('type')
    c = msg.get('content')
    usage = msg.get('usage') or {}
    if isinstance(c, str):
        print(f"{ts[11:19]} {role:9s} STRING len {len(c)} :: {' '.join(c.split())[:lim]}")
        kinds['string'] = kinds.get('string', 0) + len(c)
        continue
    if not isinstance(c, list):
        print(f"{ts[11:19]} {role} (no content) type={o.get('type')} keys={list(o.keys())[:8]}")
        continue
    for b in c:
        t = b.get('type')
        if t == 'text':
            s = b.get('text', ''); kinds['text'] = kinds.get('text', 0) + len(s)
            print(f"{ts[11:19]} {role:9s} text len {len(s)} :: {' '.join(s.split())[:lim]}")
        elif t == 'thinking':
            s = b.get('thinking', '') or ''; kinds['thinking'] = kinds.get('thinking', 0) + len(s)
            sig = len(b.get('signature', '') or '')
            print(f"{ts[11:19]} {role:9s} thinking readable len {len(s)} signature len {sig} out_tokens {usage.get('output_tokens')} :: {' '.join(s.split())[:200]}")
        elif t == 'redacted_thinking':
            print(f"{ts[11:19]} {role:9s} redacted_thinking data len {len(b.get('data',''))}")
        elif t == 'tool_use':
            print(f"{ts[11:19]} {role:9s} TOOL_USE {b.get('name')} :: {json.dumps(b.get('input'))[:lim*3]}")
        elif t == 'tool_result':
            cc = b.get('content')
            s = cc if isinstance(cc, str) else json.dumps(cc)
            print(f"{ts[11:19]} {role:9s} tool_result len {len(s)} :: {' '.join(s.split())[:160]}")
        else:
            print(f"{ts[11:19]} {role:9s} block {t}")
print('records', n, 'first', first, 'last', last, 'chars by kind', kinds)
