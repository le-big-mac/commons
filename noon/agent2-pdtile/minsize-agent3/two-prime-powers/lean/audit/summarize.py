"""Summarise runs/Z*.tsv: per group, what was covered and whether every check passed."""
import glob, re, sys, collections
rows = []
for f in sorted(glob.glob('runs/Z*.tsv'), key=lambda s: (int(re.search(r'Z(\d+)', s).group(1)), s)):
    for line in open(f, encoding='utf-8'):
        if line.startswith('#') or line.startswith('M\t') or not line.strip():
            continue
        p = line.rstrip('\n').split('\t')
        rows.append(dict(M=int(p[0]), D=p[1], corners=p[2], B=int(p[3]), method=p[4].split('(')[0], S=int(p[5]),
                         L=int(p[6]), R=int(p[7]), a=p[8], nb=int(p[9]), minb=p[10], b=p[11], nc=int(p[12]),
                         minc=p[13], clow=p[14], cfound=p[15], wit=p[16], cov=p[17], heads=p[4]))
byM = collections.defaultdict(list)
for r in rows:
    byM[r['M']].append(r)
print('M | up-sets D | plain: all multisets up to size | lattice: sizes reached (min..max over D) | multisets with all Phi_d, d in D, dividing (largest set compared) | (a) | (b) | (c) | D with (b),(c) complete / all | largest B')
tot_heads = 0
for M in sorted(byM):
    rs = byM[M]
    Ds = sorted(set(r['D'] for r in rs))
    plain = [r for r in rs if r['method'] == 'plain']
    lat = [r for r in rs if r['method'] == 'lattice']
    best = {}
    for r in rs:                      # the furthest run for each D
        if r['D'] not in best or r['S'] > best[r['D']]['S']:
            best[r['D']] = r
    complete = sum(1 for D in Ds if best[D]['cov'] == 'complete')
    found = sum(1 for D in Ds if best[D]['cfound'] == 'found')
    a = all(r['a'] == 'OK' for r in rs); b = all(r['b'] == 'OK' for r in rs)
    c = all(r['clow'] == 'OK' and r['wit'] == 'OK' and r['cfound'] != 'MISSING' for r in rs)
    for r in lat:
        m = re.search(r',(\d+) heads', r['heads'])
        tot_heads += int(m.group(1))
    print('%d | %d | %s | %s | %d | %s | %s | %s | %d / %d (least size found by search for %d) | %d' % (
        M, len(Ds), ('%d (%d multisets)' % (plain[0]['S'], max(r['L'] for r in plain))) if plain else '-',
        ('%d..%d' % (min(best[D]['S'] for D in Ds if best[D]['method'] == 'lattice'), max(best[D]['S'] for D in Ds if best[D]['method'] == 'lattice'))) if lat else '-',
        max(r['L'] for r in rs if r['D'] != '[]') if len(Ds) > 1 else rs[0]['L'], 'OK' if a else 'FAIL', 'OK' if b else 'FAIL', 'OK' if c else 'FAIL',
        complete, len(Ds), found, max(r['B'] for r in rs)))
print()
print('total (M, D, method) runs: %d; lattice heads tried in all: %d' % (len(rows), tot_heads))
print('not complete (size reached < B - 1):')
for M in sorted(byM):
    rs = byM[M]
    best = {}
    for r in rs:
        if r['D'] not in best or r['S'] > best[r['D']]['S']:
            best[r['D']] = r
    for D, r in best.items():
        if r['cov'] != 'complete':
            print('   M=%d D=%s corners=%s B=%d reached S=%d' % (M, D, r['corners'], r['B'], r['S']))
