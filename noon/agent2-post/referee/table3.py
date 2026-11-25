"""From cmp.out (the referee's plain ruler.c): least T with YES, for each small board, question and lag; compared with README Table 3."""
import re, collections
mine = collections.defaultdict(dict)
for l in open('cmp.out'):
    p, c, _, d, _, T, m, noon, me = l.split()
    mine[(int(p), int(c), m, int(d))][int(T)] = me.split('=')[1]
tab = {}
for l in open('/home/agent2/post/README.md'):
    f = [x.strip() for x in l.strip().strip('|').split('|')]
    if len(f) == 12 and f[0].isdigit():
        p, c = int(f[0]), int(f[1]); v = list(map(int, f[3:]))
        tab[(p, c)] = dict(K=v[0:4], Kblind=v[4], W=v[5:9])
ok = bad = unk = 0; notes = []
for (p, c), row in sorted(tab.items()):
    for m in 'KW':
        for d in range(4):
            r = mine.get((p, c, m, d))
            if not r: continue
            want = row[m][d]
            yes_at = r.get(want); no_before = r.get(want - 1, 'NO' if want - 1 < min(r) else None)
            if yes_at == 'YES' and no_before == 'NO': ok += 1
            elif yes_at in ('YES', 'NO') and no_before in ('YES', 'NO'): bad += 1; notes.append((p, c, m, d, want, r))
            else: unk += 1; notes.append(('not settled by my ruler', p, c, m, d, want))
    for d in (4, 5):   # blind column: K at lag 5 (five or fewer guesses are all blind there)
        pass
    r = mine.get((p, c, 'K', 5))
    if r:
        want = row['Kblind']
        if r.get(want) == 'YES' and r.get(want - 1, 'NO') == 'NO': ok += 1
        else: bad += 1; notes.append(('blind', p, c, want, r))
print('Table 3 entries reproduced by the referee ruler:', ok, '; contradicted:', bad, '; not settled (timeout):', unk)
for n in notes: print('  ', n)
