# Referee: list the author's own tool calls between two times (from the session transcript; data only).
import json, sys
path, t0, t1 = sys.argv[1], sys.argv[2], sys.argv[3]
for line in open(path, encoding='utf-8', errors='replace'):
    try:
        d = json.loads(line)
    except Exception:
        continue
    ts = d.get('timestamp') or ''
    if not (t0 <= ts <= t1) or d.get('type') != 'assistant':
        continue
    for c in (d.get('message') or {}).get('content') or []:
        if isinstance(c, dict) and c.get('type') == 'tool_use':
            inp = c.get('input') or {}
            s = inp.get('command') or inp.get('file_path') or inp.get('description') or str(inp)
            print(ts[11:19], c.get('name'), '|', s[:330].replace('\n', ' \\n '))
