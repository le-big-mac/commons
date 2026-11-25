"""Save a sub-agent's final reply word for word.   usage: python -I extract-report.py TASK.output 'MARKER' OUT.md
Reads the task's JSONL transcript, takes the last assistant text that contains MARKER, writes it to OUT.md and
prints only its length and first line (the transcript itself is too long to read)."""
import sys, json
best = None
for line in open(sys.argv[1], errors='replace'):
    try: o = json.loads(line)
    except Exception: continue
    m = o.get('message') or {}
    if m.get('role') != 'assistant': continue
    c = m.get('content')
    for b in (c if isinstance(c, list) else [dict(type='text', text=c or '')]):
        if isinstance(b, dict) and b.get('type') == 'text' and sys.argv[2] in b.get('text', ''):
            best = b['text']
if best is None: sys.exit("marker not found")
open(sys.argv[3], 'w').write(best.rstrip() + "\n")
print(len(best), "characters;", best.splitlines()[0][:80])
