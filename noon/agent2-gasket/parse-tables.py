# parse-tables.py -- the 42 packings of the paper's Tables A and B, read by script from the text of the PDF:
# root quadruple, type (carried down from the first packing of each group of three), the size of the sporadic set and its
# largest member as the paper prints them.   python -I parse-tables.py ~/gasket-data/hkrs/paper.txt > packings.json
import re, sys, json
lines = open(sys.argv[1], encoding='utf-8', errors='replace').read().split('\n')
a = next(i for i, l in enumerate(lines) if 'Table A.' in l); b = next(i for i, l in enumerate(lines) if 'Figure A.' in l and i > a)
out = []; cur = None
for l in lines[a:b]:
    l = l.replace('−', '-'); m = re.match(r'\s*\((-?\d+), (-?\d+), (-?\d+), (-?\d+)\)(.*)$', l)
    if not m: continue
    root = [int(x) for x in m.groups()[:4]]; rest = m.group(5)
    t = re.match(r'\s*\((\d+), (\d+), (-?\d+)(?:, (-?\d+))?\)', rest)
    if t: cur = [int(x) for x in t.groups() if x is not None]; rest = rest[t.end():]
    nums = re.findall(r'\d+(?:\.\d+)?', rest); ratio, mx, cnt = float(nums[-1]), int(nums[-2]), int(nums[-3])
    out.append({'root': root, 'type': cur, 'sporadic': cnt, 'largest': mx, 'ratio': ratio})
json.dump(out, sys.stdout, indent=0); sys.stderr.write('%d packings\n' % len(out))
