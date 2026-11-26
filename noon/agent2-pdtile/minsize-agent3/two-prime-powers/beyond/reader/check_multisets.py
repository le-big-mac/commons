"""Reader's check of every multiset the note rests on: size and exact pattern.
  realised-M.jsonl, realised2-M.jsonl  (M = 36, 100, 225): 6 x 256 multisets
  out225/z225-*.jsonl: every multiset the Z_225 run returned
Reads only; writes nothing but its printout.   usage: check_multisets.py"""
import json, glob, sys, collections, itertools
sys.path.insert(0, '/home/agent3/pq2/rule/reader')
from pat import parse, pattern, divisors

R = '/home/agent3/pq2/rule/'
tot = bad = 0
sizes = {}
for kind in ('realised', 'realised2'):
    for M in (36, 100, 225):
        divs = [d for d in divisors(M) if d > 1]
        seen = set(); nbad = 0; att = collections.Counter()
        for l in open(f'{R}{kind}-{M}.jsonl'):
            r = json.loads(l); tot += 1
            v = parse(r['multiset'], M)
            ok = (r['M'] == M and sum(v) == r['size'] and pattern(v, M) == sorted(r['D']) and set(r['D']) <= set(divs))
            if not ok: nbad += 1; bad += 1; print('FAIL', kind, M, r['D'], r['size'], sum(v), pattern(v, M))
            seen.add(tuple(sorted(r['D']))); att[r['attempts']] += 1
            sizes[(kind, M, tuple(sorted(r['D'])))] = sum(v)
        allpats = {tuple(c) for k in range(len(divs) + 1) for c in itertools.combinations(divs, k)}
        print(f'{kind}-{M}.jsonl: {len(seen)} distinct patterns, all 256 present: {seen == allpats}; failures: {nbad}; '
              f'first attempt: {att[1]}; most attempts: {max(att)}')
print('multisets checked in the six files:', tot, '; failures:', bad)
json.dump({f'{k}|{M}|{",".join(map(str, D))}': s for (k, M, D), s in sizes.items()}, open(R + 'reader/realised-sizes.json', 'w'))

# the Z_225 run
M = 225
st = collections.Counter(); nm = 0; nbad = 0; last = {}
for f in sorted(glob.glob(R + 'out225/z225-*.jsonl')):
    n = 0
    for l in open(f):
        if not l.startswith('{'): continue
        r = json.loads(l); n += 1
        if r['multiset'] is not None:
            v = parse(r['multiset'], M); nm += 1
            if not (sum(v) == r['size'] and pattern(v, M) == sorted(r['D'])):
                nbad += 1; print('FAIL', f, r['D'], r['size'], sum(v), pattern(v, M))
            if r.get('upper_bound_given') is not None and r['size'] > r['upper_bound_given']: print('ABOVE THE GIVEN BOUND', r['D'])
        else:
            assert r['size'] is None
        last[tuple(r['D'])] = (r, f.split('/')[-1])
    print(f.split('/')[-1], n, 'lines')
print('Z_225 run: multisets checked:', nm, '; failures:', nbad, '; distinct patterns in the files:', len(last))
print('status of the last line for each pattern:', dict(collections.Counter(r['status'] for r, _ in last.values())))
print('which file holds the last line:', dict(collections.Counter(f for _, f in last.values())))
