"""Referee's checks of README facts, from the definitions (reads Noon's out/K-d3-Q5-all.out for the 72 openings only)."""
import itertools, sys
from collections import Counter, defaultdict
import numpy as np
def ans(g, c):
    b = sum(x == y for x, y in zip(g, c)); cg, cc = Counter(g), Counter(c)
    return (b, sum(min(cg[q], cc[q]) for q in cg) - b)
# 1. 3 pegs 4 colours: 112, 133, 423
codes34 = [''.join(p) for p in itertools.product('1234', repeat=3)]
rows = Counter(tuple(ans(g, c) for g in ('112', '133', '423')) for c in codes34)
print('3 pegs 4 colours, blind 112 133 423: distinct rows', len(rows), 'of', len(codes34), '; largest class', max(rows.values()))
# is two enough? (so that 3 is the least) -- every pair of blind guesses
best2 = min(max(Counter((ans(g1, c), ans(g2, c)) for c in codes34).values()) for g1 in codes34 for g2 in codes34)
print('  best two blind guesses leave a largest class of', best2, '(so two are not enough)' if best2 > 1 else '')
# 2. Table 4
codes = [''.join(p) for p in itertools.product('123456', repeat=4)]
quad = ['1123', '2445', '2562', '3356']
a1 = Counter(ans('1123', c) for c in codes)
print('answer to 1123 -> codes:', sorted(a1.items(), key=lambda x: -x[1]))
cl = Counter(tuple(ans(g, c) for g in quad) for c in codes)
print('four blind answers: classes', len(cl), 'largest', max(cl.values()), 'codes alone', sum(1 for v in cl.values() if v == 1))
# 3. the 72 openings that work at lag 3 with five guesses: check each, and count classes
idx = {c: i for i, c in enumerate(codes)}
A = np.array([[ans(g, c)[0] * 5 + ans(g, c)[1] for c in codes] for g in codes], dtype=np.int64)
quads = [l.split()[1:] for l in open('/home/agent2/post/out/K-d3-Q5-all.out') if l.startswith('yes')]
print('yes lines in K-d3-Q5-all.out:', len(quads), '; distinct', len(set(map(tuple, quads))))
def works(q):
    g = [idx[x] for x in q]
    key = (A[g[1]] * 25 + A[g[2]]) * 25 + A[g[3]]
    for a in np.unique(A[g[0]]):
        m = A[g[0]] == a; k = key[m]
        if len(np.unique(k)) == m.sum(): continue
        full = k[None, :] * 25 + A[:, m]                       # every fifth guess
        nd = np.array([len(np.unique(r)) for r in full])
        if nd.max() < m.sum(): return False
    return True
bad = [q for q in quads if not works(q)]
print('of them, fail my check:', len(bad))
D = np.array([[int(ch) - 1 for ch in c] for c in codes]); w = 6 ** np.arange(3, -1, -1)
G = [(np.array(cp)[D[:, list(pp)]] * w).sum(1) for pp in itertools.permutations(range(4)) for cp in itertools.permutations(range(6))]
canon = set(); firsts = Counter()
for q in quads:
    g = [idx[x] for x in q]
    best = min((int(im[g[0]]),) + tuple(sorted(int(im[x]) for x in g[1:])) for im in G)
    canon.add(best); firsts[''.join(sorted(Counter(q[0]).values().__iter__().__class__ and map(str, sorted(Counter(q[0]).values(), reverse=True))))] += 1
print('classes of (first guess; set of the other three) under renaming x reordering:', len(canon), '; shape of first guess (colour counts):', dict(firsts))
canon_unordered = set(min(tuple(sorted(int(im[x]) for x in [idx[y] for y in q])) for im in G) for q in quads)
print('classes if the four are taken as a plain set (forgetting which is first):', len(canon_unordered))
# 4. Burnside for ordered triples
fix = np.array([(im == np.arange(1296)).sum() for im in G], dtype=object)
print('classes of ordered lists of 1, 2, 3 codes:', sum(fix) // len(G), sum(f * f for f in fix) // len(G), sum(f ** 3 for f in fix) // len(G))
