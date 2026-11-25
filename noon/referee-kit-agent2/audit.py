"""Which files and commands did a fresh instance use?  Prints tool names and paths only, never the transcript.
usage: python -I audit.py TASKSDIR 'ALLOWED-REGEX' id1 [id2 ...]
TASKSDIR is where the harness keeps the sub-agents' transcripts (one <id>.output each, JSON lines).
ALLOWED-REGEX is matched against every path that appears in a tool call; {k} in it becomes the agent's number (1, 2, ...).
Example:  python -I audit.py TASKSDIR '/home/me/birth/forecast/(brief\\.md|sheet\\.md|f{k}\\.json)$' ida idb idc"""
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

for k, i in enumerate(sys.argv[3:], 1):
    allowed = re.compile(sys.argv[2].replace('{k}', str(k)))
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
        paths = set(re.findall(r"/(?:home|srv|tmp|opt|etc|var|usr)/[^\s'\"),]*", arg))
        ok = all(allowed.match(p) for p in paths) and 'http' not in arg and name not in ('WebFetch', 'WebSearch', 'Agent')
        out.append(name + ':' + ('+'.join(sorted(p.split('/')[-1] for p in paths)) or 'no path') + ('' if ok else '  !CHECK: ' + arg[:140]))
    print(f"agent {k}: {len(calls)} tool calls: " + ' | '.join(out))
