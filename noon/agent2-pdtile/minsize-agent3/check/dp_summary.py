"""One table of everything the referee's tree recursion (dp.c) computed: reads the dp-*.out files in this folder."""
import glob, re, os
rows = []
for f in sorted(glob.glob('/home/agent3/minsize/check/dp-p*-q*-n*-*.out')):
    m = re.search(r'dp-p(\d+)-q(\d+)-n(\d+)-(multi|set)-S(\d+)\.out', f)
    p, q, n, kind, S = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4), int(m.group(5))
    L = open(f).read().splitlines()
    head = L[0]
    d = {}
    for l in L:
        if l.startswith('# 0 not in F'): d['thm'] = l[2:]
        if l.startswith('# F all'): d['all'] = l[2:]
        if l.startswith('# rest of 0 in F'): d['rule'] = l[2:]
        if l.startswith('# sets:'): d['sets'] = l[2:]
        if l.startswith("# author's"): d['auth'] = l[2:]
    nbad = sum(1 for l in L if l.startswith('# NOT AS EXPECTED'))
    # patterns whose formula is beyond the bound: is the lower bound still settled?  sizes are multiples of
    # step = p^e (times q if 0 in F); if formula - step <= bound, "none up to the bound" proves minimum >= formula.
    tight = loose = 0
    if kind == 'multi':
        import json
        for l in L:
            if l.startswith('#') or 'formula beyond' not in l: continue
            E, F, mm, form, a, v = [t.strip() for t in l.split('|')]
            E = json.loads(E); F = json.loads(F); form = int(form.split()[1])
            step = p ** len(E) * (q if 0 in F else 1)
            bound = int(re.search(r'none <= (\d+)', v).group(1))
            if form - step <= bound: tight += 1
            else: loose += 1
        d['beyond'] = f'of the patterns beyond the bound: least size proved >= formula (next smaller admissible size is within the bound) in {tight}; not settled in {loose}'
    rows.append((n, p, q, kind, S, head, d, nbad))
print('Everything the tree recursion computed (each least size has a witness checked by exact polynomial division).')
print('"beyond bound" = the formula exceeds the largest size searched and nothing smaller was found.\n')
for n, p, q, kind, S, head, d, nbad in sorted(rows, key=lambda r: (r[3], r[2], r[1], r[0], r[4])):
    print(f'order {p ** n * q} (p={p}, q={q}, n={n}), {kind}, sizes up to {S}:')
    for k in ('thm', 'all', 'rule', 'beyond', 'sets', 'auth'):
        if k in d: print('    ' + d[k])
    if nbad: print(f'    lines marked NOT AS EXPECTED: {nbad}')
