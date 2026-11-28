import sys, json
for p in sys.argv[1:]:
    first = last = None; head = None; n = 0
    with open(p, encoding='utf-8') as f:
        for line in f:
            try: r = json.loads(line)
            except Exception: continue
            n += 1
            t = r.get('timestamp')
            if t:
                if first is None: first = t
                last = t
            if head is None and r.get('type') == 'user':
                c = r.get('message', {}).get('content')
                if isinstance(c, list):
                    c = ' '.join(x.get('text', '') for x in c if isinstance(x, dict))
                head = (c or '')[:90]
    print(first, last, n, '|', head)
