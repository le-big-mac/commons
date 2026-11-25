# Referee: read the three forecasters' transcripts (data only) and list times and tool calls.
import json, sys
for path in sys.argv[1:]:
    first = last = None; calls = []; n_asst = 0; out_tokens = 0; prompt = None
    for line in open(path, encoding='utf-8', errors='replace'):
        try:
            d = json.loads(line)
        except Exception:
            continue
        ts = d.get('timestamp')
        if ts:
            first = first or ts; last = ts
        msg = d.get('message') or {}
        if d.get('type') == 'user' and prompt is None and isinstance(msg.get('content'), str):
            prompt = msg['content'][:160].replace('\n', ' ')
        if d.get('type') == 'assistant':
            n_asst += 1
            out_tokens += (msg.get('usage') or {}).get('output_tokens', 0) or 0
            for c in msg.get('content') or []:
                if isinstance(c, dict) and c.get('type') == 'tool_use':
                    inp = c.get('input') or {}
                    calls.append((ts, c.get('name'), (inp.get('file_path') or inp.get('command') or str(inp))[:700]))
    print("==", path.split('/')[-1]); print("   prompt:", prompt); print("   first", first, "last", last, "assistant records", n_asst, "output tokens (sum of usage)", out_tokens)
    for c in calls:
        print("   ", c[0], c[1], "|", c[2].replace('\n', ' \\n '))
