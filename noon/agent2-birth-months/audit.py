"""Which files and commands did each forecaster use?  Prints tool names and paths only.   usage: python -I audit.py TASKSDIR id1 id2 id3"""
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
            calls.append((t.get('name'), str(inp.get('file_path') or inp.get('command') or inp.get('url') or inp.get('query') or inp.get('pattern') or inp).replace('\n', ' ')))
    out = []
    for name, arg in calls:
        paths = set(re.findall(r"/(?:home|srv|tmp|opt|etc)/[^\s'\"),]*", arg))
        ok = all(re.match(r"/home/agent2/birth/forecast/(brief\.md|sheet\.md|f%d\.json)$" % k, p) for p in paths) and name in ('Read', 'Write', 'Bash') and 'http' not in arg
        out.append(name + ':' + ('+'.join(sorted(p.split('/')[-1] for p in paths)) or 'no path') + ('' if ok else ' !CHECK: ' + arg[:120]))
    print(f"forecaster {k}: {len(calls)} tool calls: " + ' | '.join(out))
