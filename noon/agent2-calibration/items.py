"""Read the labelled expectations out of the sheets.   usage: python -I items.py SHEETSDIR items.json"""
import sys, re, os, json
items = []
for rnd in ('A', 'B'):
    for f in sorted(os.listdir(f"{sys.argv[1]}/{rnd}")):
        cur = None
        for line in open(f"{sys.argv[1]}/{rnd}/{f}", encoding='utf-8'):
            m = re.match(r"^([A-Z])(\d+)\.\s+(.*)", line)
            if m:
                cur = dict(id=m.group(1) + m.group(2), file=f[:-3], round=rnd, text=m.group(3).strip())
                items.append(cur)
            elif cur is not None and line.startswith('    ') and line.strip():
                cur['text'] += ' ' + line.strip()
            else:
                cur = None
for it in items:
    it['between'] = bool(re.search(r"\bbetween\b", it['text'], re.I))
json.dump(items, open(sys.argv[2], 'w'), indent=1)
print(len(items), "expectations in", len(set(i['file'] for i in items)), "files;", sum(i['between'] for i in items), "contain 'between'")
for it in items:
    print(f"{it['id']:4s} {it['file'][:22]:22s} {'B' if it['between'] else ' '} {it['text'][:120]}")
