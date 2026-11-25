"""Positive control for the nested count used in wquad.c: on the five blind guesses of Noon's lag-4 strategy (replayed: every code sent by guess 10)
the five-level count must be 0; on the first four of them the four-level count must be 2 or more (wquad.c: no quad has U <= 1)."""
import itertools
from collections import Counter, defaultdict
codes = [''.join(p) for p in itertools.product('123456', repeat=4)]
def ans(g, c):
    b = sum(x == y for x, y in zip(g, c)); cg, cc = Counter(g), Counter(c)
    return (b, sum(min(cg[q], cc[q]) for q in cg) - b)
blind = [l.split(':')[1].strip() for l in open('/home/agent2/post/out/final/W-d4-Q10.out') if l.startswith('S ') and l.split()[2].startswith('-:')]
print('blind guesses of W-d4-Q10:', blind)
def U(gs):
    tree = defaultdict(int)
    for c in codes:
        if c in gs: continue
        tree[tuple(ans(g, c) for g in gs)] += 1
    level = {k: max(0, v - 1) for k, v in tree.items()}
    for depth in range(len(gs) - 1, 0, -1):
        up = defaultdict(int)
        for k, v in level.items(): up[k[:depth]] += v
        level = {k: max(0, v - 1) for k, v in up.items()}
    return sum(level.values())
print('five-level count on all five:', U(blind), '(0 means the code is always sent by guess lag+6)')
print('four-level count on the first four:', U(blind[:4]), '(needs 0 for lag 3 in 8, <=1 for lag 4 in 9)')
