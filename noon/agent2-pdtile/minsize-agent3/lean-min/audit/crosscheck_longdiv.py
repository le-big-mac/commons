"""The C enumerator finds patterns from a table of remainders (division is linear).  Here every multiset of
small size is divided by every Phi_d by long division in Python, one at a time, and the number of multisets
of each size with each pattern is compared with what the C enumerator counted (outA/group<M>.json)."""
import itertools
import json
from collections import Counter

from cyc import pattern
from tables import divs

total = 0
for M, smax in [(2, 12), (3, 10), (5, 7), (6, 7), (10, 5), (12, 5), (15, 4), (18, 4), (20, 4), (24, 4), (28, 3), (48, 2)]:
    A = json.load(open(f'outA/group{M}.json'))
    ds = divs(M)
    assert ds == A['divisors']
    idx = {d: i for i, d in enumerate(ds)}
    mine = Counter()
    n = 0
    for s in range(0, smax + 1):
        for c in itertools.combinations_with_replacement(range(M), s):
            w = [0] * M
            for a in c:
                w[a] += 1
            mask = sum(1 << idx[d] for d in pattern(M, w))
            mine[(mask, s)] += 1
            n += 1
    theirs = Counter()
    for k, v in A['patterns'].items():
        for s in range(0, smax + 1):
            if v['counts'][s]:
                theirs[(int(k), s)] = v['counts'][s]
    assert mine == theirs, M
    total += n
    print(f"Z_{M}: sizes 0..{smax}: {n} multisets divided one by one; counts by (pattern, size) equal to the C enumerator's: {len(mine)} entries")
print("total:", total)
