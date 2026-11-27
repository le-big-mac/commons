"""(R**): for each family F, which sets B0 in F have the property
     'for every signing eta, eta or its flip at B0 is good'   (so that at least half the signings are good)?
Reports families with no such B0, and whether a minimal / maximal / smallest / largest set always works.   usage: rstar_flip.py q1 .. qr"""
import sys, itertools
q = [int(t) for t in sys.argv[1:]]; r = len(q)
subsets = list(range(1, 1 << r))
def coef(B, D):
    v = 1
    for i in range(r):
        if D >> i & 1: v *= (-1 if B >> i & 1 else q[i])
    return v
C = {B: [coef(B, D) for D in range(1 << r)] for B in [0] + subsets}
pc = lambda v: bin(v).count('1')
nfam = 0; none = []; stats = {'every minimal set works': 0, 'some minimal set works': 0, 'every maximal set works': 0, 'some maximal set works': 0, 'every set works': 0}
ex = {}
for F in range(1, 1 << len(subsets)):
    fam = [subsets[b] for b in range(len(subsets)) if F >> b & 1]; nfam += 1; N = len(fam)
    bad = set()
    for signs in itertools.product((1, -1), repeat=N):
        if not all(C[0][D] + sum(s * C[B][D] for s, B in zip(signs, fam)) != 0 for D in range(1 << r)): bad.add(signs)
    works = []
    for k, B0 in enumerate(fam):
        if not any((s[:k] + (-s[k],) + s[k + 1:]) in bad for s in bad): works.append(B0)
    if not works: none.append(fam)
    mins = [B for B in fam if not any(B2 != B and B2 & B == B2 for B2 in fam)]
    maxs = [B for B in fam if not any(B2 != B and B2 & B == B for B2 in fam)]
    for name, cond in (('every minimal set works', all(B in works for B in mins)), ('some minimal set works', any(B in works for B in mins)),
                       ('every maximal set works', all(B in works for B in maxs)), ('some maximal set works', any(B in works for B in maxs)),
                       ('every set works', len(works) == N)):
        if cond: stats[name] += 1
        elif name not in ex: ex[name] = (fam, works)
print(f'q = {q}: nonempty families {nfam}; families with NO such B0: {len(none)} {none[:4]}')
print('   ', stats); print('    first exceptions:', ex)
