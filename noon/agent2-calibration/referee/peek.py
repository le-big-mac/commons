"""Print, for each transcript given, every tool call that mentions sheets/B or writes fN/A.json, in order, with the command text (trimmed)."""
import sys, json, re
def walk(o):
    if isinstance(o, dict):
        if o.get('type') == 'tool_use': yield o
        for v in o.values(): yield from walk(v)
    elif isinstance(o, list):
        for v in o: yield from walk(v)
for path in sys.argv[1:]:
    seen = set(); n = 0; print('==', path.split('/')[-1])
    for line in open(path, errors='replace'):
        try: o = json.loads(line)
        except Exception: continue
        for t in walk(o):
            if t.get('id') in seen: continue
            seen.add(t.get('id')); n += 1
            inp = t.get('input', {}); s = json.dumps(inp)
            paths = set(re.findall(r"/(?:home|srv|tmp|opt|etc|var|usr)/[^\s'\"\\]*", s))
            bad = [p for p in paths if not re.match(r"/home/agent2/calib/(sheets/[AB]|f\d|brief\.md)", p)]
            if 'sheets/B' in s and re.search(r'/f\d', s):
                cmd = str(inp.get('command') or inp.get('file_path') or '')
                print('  call %d %s: A.json at char %d, sheets/B at char %d, len %d :: %s' % (n, t.get('name'), cmd.find('A.json'), cmd.find('sheets/B'), len(cmd), re.sub(r'\s+', ' ', cmd)[-260:]))
            if bad: print('  call %d OUTSIDE: %s' % (n, bad))
            if t.get('name') not in ('Read', 'Bash', 'Write', 'Edit', 'Glob', 'Grep'): print('  call %d other tool: %s' % (n, t.get('name')))
    print('  total calls', n)
