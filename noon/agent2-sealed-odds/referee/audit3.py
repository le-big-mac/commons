"""Referee: what else was in a forecaster's context, and what it cost.  usage: audit3.py TRANSCRIPT [show]
Lists attachments (type and bounded content), the system text, all distinct tool calls with timestamps, sums usage by distinct
API message id, and searches every readable string for result strings."""
import sys, json, re
path = sys.argv[1]; show = len(sys.argv) > 2
recs = []
for line in open(path, encoding='utf-8', errors='replace'):
    try: recs.append(json.loads(line))
    except Exception: pass
# attachments
print('--- attachments')
for o in recs:
    if o.get('type') == 'attachment':
        a = o.get('attachment') or {}
        s = json.dumps(a)
        print('  ', o.get('timestamp', '')[11:19], a.get('type'), 'len', len(s), '::', ' '.join(s.split())[:(1500 if show else 220)])
# request shapes / system text
print('--- other record types')
types = {}
for o in recs: types[o.get('type')] = types.get(o.get('type'), 0) + 1
print('  ', types)
# usage by message id
seen = {}
calls = []
for o in recs:
    m = o.get('message') or {}
    if m.get('role') == 'assistant':
        mid = m.get('id') or o.get('uuid')
        u = m.get('usage') or {}
        if u: seen[mid] = u
        for b in m.get('content') or []:
            if isinstance(b, dict) and b.get('type') == 'tool_use':
                calls.append((o.get('timestamp', '')[11:19], b.get('id'), b.get('name'), json.dumps(b.get('input'))))
tot = {}
for u in seen.values():
    for k in ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens'):
        tot[k] = tot.get(k, 0) + (u.get(k) or 0)
print('--- usage summed over', len(seen), 'distinct assistant messages:', tot)
print('    output tokens per message:', [u.get('output_tokens') for u in seen.values()])
ids = {}
for t, i, n, inp in calls: ids.setdefault(i, (t, n, inp))
print('--- distinct tool calls:', len(ids))
for i, (t, n, inp) in ids.items():
    paths = re.findall(r"/[A-Za-z0-9_./%-]+", inp)
    print('  ', t, n, sorted(set(paths)))
# search all readable strings
blob = []
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('signature', 'data'): continue
            walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
    elif isinstance(o, str): blob.append(o)
for o in recs: walk(o)
text = '\n'.join(blob)
print('--- readable characters:', len(text))
for s in ['0.1496', '0.2253', '146 times', '0.470', '0.47', 'wrong from order 3', '80 sequences', 'sixteen', 'never even stable', '0.2265', '0.225 and 0.23',
          'ring', 'four of six', 'Four of my six', 'failed', 'held', 'srv/commons', 'NOTES.md', 'notes-to-owner', 'README', 'lines.csv', 'again-prediction', 'recal',
          'collect.py', 'arctic', 'aztec', 'A1', '0.184', '0.131', 'counter', 'pencil', '33', 'end of its interval', '0.707', '82.6', '0.949']:
    idx = [m.start() for m in re.finditer(re.escape(s), text)]
    ctx = ''
    if idx and show:
        ctx = ' | '.join(' '.join(text[max(0, i - 50): i + 60].split()) for i in idx[:3])
    print(f'   {s!r:28s} {len(idx):4d}  {ctx[:400]}')
