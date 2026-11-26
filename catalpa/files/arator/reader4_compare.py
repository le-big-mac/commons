# The fourth reader's corrections (reader4_corrections.tsv: poem, line, the scanner's pattern then, the reader's pattern, class, sure or probable, text) set against the scans
# made after the mends of 26 Nov: how many of the corrected lines the scanner now reads as the reader did, and what each poem's share of dactyls would be if every
# remaining correction were applied.
import re, collections
rows = [l.rstrip('\n').split('\t') for l in open('/home/agent1/arator/late2_scans.tsv')]
key = lambda s: re.sub(r'[^a-z]', '', s.lower().replace('v', 'u'))
now = {(r[0], key(r[5])): r for r in rows}
C = [l.rstrip('\n').split('\t') for l in open('/home/agent1/arator/reader4_corrections.tsv')]
by = collections.defaultdict(lambda: [0, 0, 0]); left = collections.defaultdict(list)      # class -> [now as the reader, still different, line left out]
for poem, line, old, new, cls, how, text in C:
    r = now.get((poem, key(text)))
    if r is None: by[cls][2] += 1; continue
    if r[1][:4] == new[:4]: by[cls][0] += 1
    else: by[cls][1] += 1; left[poem].append((r, new, cls, how))
print('class                                  now as the reader   still different   line left out as damaged')
for cls, (a, b, c) in sorted(by.items(), key=lambda t: -sum(t[1])): print(f'  {cls:36s} {a:6d} {b:14d} {c:14d}')
print('  total', sum(v[0] for v in by.values()), sum(v[1] for v in by.values()), sum(v[2] for v in by.values()))
print('\npoem          lines scanned   share now   corrections still open (sure, probable)   share with the sure ones applied   with all applied')
for poem in ('juvencus', 'ausonius', 'prudentius', 'dracontius', 'corippus'):
    R = [r for r in rows if r[0] == poem and r[1] != 'NONE']; d = sum(r[1][:4].count('D') for r in R); n = 4 * len(R)
    sure = [x for x in left[poem] if x[3] == 'sure']; prob = [x for x in left[poem] if x[3] != 'sure']
    ds = d + sum(x[1][:4].count('D') - x[0][1][:4].count('D') for x in sure); da = ds + sum(x[1][:4].count('D') - x[0][1][:4].count('D') for x in prob)
    print(f'  {poem:11s} {len(R):6d}   {100 * d / n:6.2f}%   {len(sure):3d}, {len(prob):3d}   {100 * ds / n:6.2f}%   {100 * da / n:6.2f}%')
    for x in left[poem]: print(f'        {x[2]:34s} {x[3]:8s} scanner {x[0][1][:4]} reader {x[1][:4]}  {x[0][5][:70]}')
