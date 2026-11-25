"""Which files did each forecaster touch?  Reads the five transcripts the harness kept and prints only tool names and paths.
usage: python -I audit.py TASKSDIR id1 id2 id3 id4 id5"""
import sys, json, re
def walk(o):
    if isinstance(o, dict):
        if o.get('type') == 'tool_use':
            yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)
for k, i in enumerate(sys.argv[2:], 1):
    calls, seen = [], set()
    for line in open(f"{sys.argv[1]}/{i}.output", errors='replace'):
        try:
            o = json.loads(line)
        except Exception:
            continue
        for t in walk(o):
            if t.get('id') in seen:
                continue
            seen.add(t.get('id'))
            inp = t.get('input', {})
            calls.append((t.get('name'), str(inp.get('file_path') or inp.get('command') or inp.get('pattern') or inp.get('path') or inp).replace('\n', ' ')))
    kinds = []
    for name, arg in calls:
        paths = set(re.findall(r"/(?:home|srv|tmp|opt|etc)/[^\s'\"]*", arg))
        ok = all(re.match(r"/home/agent2/calib/(sheets/[AB]|f%d|brief\.md)" % k, p) for p in paths)
        lab = [n for n, hit in (('brief', any('brief.md' in p for p in paths)), ('A', any('/sheets/A' in p for p in paths)), ('write', any('/f%d' % k in p for p in paths)),
                                ('B', any('/sheets/B' in p for p in paths))) if hit]
        kinds.append(('+'.join(lab) if lab else 'none') + ('' if ok else '!OUTSIDE:' + ','.join(sorted(paths))))
    print(f"forecaster {k}: {len(calls)} tool calls: {' '.join(kinds)}")
