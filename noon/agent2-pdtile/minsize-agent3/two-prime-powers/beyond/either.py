"""For each decided pattern in the three groups: is the least size the lower bound LB, the upper bound U, both, or neither?   usage: either.py"""
import json, glob, sys, collections
sys.path.insert(0, '/home/agent3/pq2/rule')
from lowerbound import LB
from algebra import closure
def exps(D, p, q):
    out = []
    for d in D:
        u = 0
        while d % p == 0: d //= p; u += 1
        v = 0
        while d % q == 0: d //= q; v += 1
        out.append(f'{u}{v}')
    return ' '.join(sorted(out))
def table(M):
    if M in (36, 100): return [(r['D'], r['size'], bool(r['by'])) for r in json.load(open(f'/home/agent3/pq2/note/rows-{M}.json'))]
    R = {}
    for f in sorted(glob.glob('out225/z225-*.jsonl')):
        for l in open(f):
            if l.startswith('{'): r = json.loads(l); R[tuple(r['D'])] = r
    return [(list(D), r['size'], r['status'] == 'optimal') for D, r in R.items()]
neither_all = {}
for M, p, q in ((36, 2, 3), (100, 2, 5), (225, 3, 5)):
    divs, mask, U, how = closure(p, q)
    c = collections.Counter(); neither = []
    for D, size, dec in table(M):
        if not dec: c['not decided'] += 1; continue
        lb, _ = LB(D, p, q); u = U[mask(D)]
        k = ('LB = least = U' if lb == size == u else 'least = LB < U' if size == lb else 'LB < least = U' if size == u else 'LB < least < U')
        c[k] += 1
        if k == 'LB < least < U': neither.append((exps(D, p, q), lb, size, u)); neither_all.setdefault(exps(D, p, q), []).append((M, lb, size, u))
    print(f'Z_{M}:', dict(c)); print('   neither:', neither)
print('patterns that are neither in some group, with what they are in each:')
for S, v in sorted(neither_all.items()): print('  ', S, v)
