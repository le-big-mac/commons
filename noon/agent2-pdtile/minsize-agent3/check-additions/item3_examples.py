"""Item (3) of the paragraph added before section 8: how many of the 199 patterns have e >= 1, and the example "12 against 10".
usage: item3_examples.py OUT_DIR"""
import sys, json, glob, os, re
table = {}
for path in sorted(glob.glob(os.path.join(sys.argv[1], 'n*-multi-*.jsonl*'))):
    m = re.fullmatch(r'n(\d+)-p(\d+)-q(\d+)-multi-(cpsat|highs)\.jsonl(\.part)?', os.path.basename(path))
    if not m: continue
    for l in open(path):
        if l.startswith('{'):
            r = json.loads(l)
            if r['min'] is not None and not r['undecided']:
                table[r['n'], r['p'], r['q'], tuple(r['E']), tuple(r['F'])] = r['min']
sel = [(k, v) for k, v in table.items() if 0 in k[4] and any(a >= 1 and a not in k[3] and any(b not in k[4] for b in range(1, a)) for a in k[4])]
print('patterns of item (3):', len(sel), '| with e = 0:', sum(1 for k, v in sel if not k[3]), '| with e >= 1:', sum(1 for k, v in sel if k[3]))
ex = [(k, v) for k, v in sel if k[1:3] == (2, 3) and len(k[3]) == 1 and v == 12]
print('p = 2, q = 3, e = 1, minimum 12 (against p^e (p + q) = 10):', len(ex), 'patterns, e.g. (n, p, q, E, F), minimum:', ex[:3])
print('minimum equal to q p^(e+1):', sum(1 for k, v in sel if v == k[2] * k[1] ** (len(k[3]) + 1)), '| below:', sum(1 for k, v in sel if v < k[2] * k[1] ** (len(k[3]) + 1)), '| below p^e (p + q):', sum(1 for k, v in sel if v < k[1] ** len(k[3]) * (k[1] + k[2])))
