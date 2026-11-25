# Referee: independent U by the *naming* rule (greedy matching on the laminar family), not the recursion.
import sys, itertools
from collections import defaultdict, Counter
codes = [''.join(p) for p in itertools.product('123456', repeat=4)]
def ans(a, b):
    bl = sum(x == y for x, y in zip(a, b))
    ca, cb = Counter(a), Counter(b)
    return (bl, sum(min(ca[c], cb[c]) for c in '123456') - bl)
def U(qs):
    rest = [c for c in codes if c not in qs]
    j = len(qs)
    if j == 0: return len(rest)
    sig = {c: tuple(ans(q, c) for q in qs) for c in rest}
    named = set()
    # finest level first: each class at each level names one still-unnamed code of its own, if any
    for lev in range(j, 0, -1):
        cl = defaultdict(list)
        for c in rest: cl[sig[c][:lev]].append(c)
        for k, v in cl.items():
            for c in v:
                if c not in named:
                    named.add(c); break
    return len(rest) - len(named)
for line in sys.argv[1:]:
    qs = line.split(',')
    print(' '.join(qs), [U(qs[:k]) for k in range(1, len(qs) + 1)])
