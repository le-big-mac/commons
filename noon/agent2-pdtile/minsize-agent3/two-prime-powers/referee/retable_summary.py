"""Summary of retable.py's outputs: the referee's decided values beside the author's files, Corollary P's bound, the up-set formula."""
import json, glob, collections
from lib import is_upset, corners, largest_upset_inside
for M in (36, 100):
    rs = []
    for f in sorted(glob.glob(f'out/retable-{M}-[0-9].jsonl')):
        rs += [json.loads(l) for l in open(f) if l.startswith('{')]
    dec = [r for r in rs if r['referee_status'] == 'optimal']
    c = collections.Counter()
    for r in rs:
        a = 'author proved' if (r['author_proved'] and r['author_min'] is not None) else ('author found, not proved' if r['author_min'] is not None else 'author found none')
        c[(a, r['verdict'])] += 1
    print(f'=== Z_{M}: {len(rs)} patterns; decided by the referee\'s programme: {len(dec)}')
    for k, v in sorted(c.items()): print('   ', k, v)
    below = []; atb = []; ups = 0; upeq = 0
    for r in dec:
        D = frozenset(r['D']); U = largest_upset_inside(M, D); lb = sum(M // x for x in corners(M, U))
        if r['referee_least'] < lb: below.append((r['D'], r['referee_least'], lb))
        if r['referee_least'] == lb and not is_upset(M, D): atb.append((r['D'], lb))
        if is_upset(M, D):
            ups += 1; upeq += (r['referee_least'] == sum(M // x for x in corners(M, D)))
    print('    decided values below the bound of Corollary P:', below, '; non-up-sets at the bound:', atb, '; up-sets decided:', ups, ', equal to the corner sum:', upeq)
    vals = collections.Counter(r['referee_least'] for r in dec)
    print('    distinct decided values:', len(vals), '; largest:', max(vals), 'at', [r['D'] for r in dec if r['referee_least'] == max(vals)])
    new = [(r['D'], r['author_min'], r['referee_least']) for r in dec if not (r['author_proved'] and r['author_min'] is not None)]
    print(f'    decided here and not in the author\'s files ({len(new)}): (pattern, author\'s found size, least size)')
    for t in new: print('      ', t)
    und = [(r['D'], r['author_min'], r['author_proved']) for r in rs if r['referee_status'] != 'optimal']
    print(f'    not decided here ({len(und)}): (pattern, author\'s found size, author proved)', und)
