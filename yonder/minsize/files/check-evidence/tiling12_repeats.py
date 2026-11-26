# The tiling criterion on the 12-hour clock for markings WITH repeats, sizes 2x6, 3x4, 4x3, 6x2
# (sizes 1x12 and 12x1 left out: 1,352,078 markings of 12 marks; there the criterion says "the 12 marks balance
# at every divisor", and a single mark tiles with them exactly when they are the 12 hours once each).
from itertools import combinations_with_replacement
from polylib import *
M = 12; ds = [d for d in divisors(M) if d > 1]; full = frozenset(ds)
by = {}
for s in (2, 3, 4, 6):
    by[s] = []
    for A in combinations_with_replacement(range(M), s):
        cnt = [0] * M
        for a in A: cnt[a] += 1
        by[s].append((A, cnt, frozenset(d for d in ds if balances_exact(A, M, d))))
pairs = tile = crit = both = 0
for s in (2, 3, 4, 6):
    for (A, ca, PA) in by[s]:
        for (B, cb, PB) in by[M // s]:
            pairs += 1
            is_crit = (PA | PB) == full
            c = [0] * M
            ok = True
            for a in A:
                for b in B:
                    x = (a + b) % M; c[x] += 1
                    if c[x] > 1: ok = False; break
                if not ok: break
            is_tile = ok          # 12 sums, none repeated => every hour exactly once
            tile += is_tile; crit += is_crit; both += (is_tile and is_crit)
print(f"   clock 12, markings with repeats (sizes 2x6, 3x4, 4x3, 6x2): ordered pairs: {pairs}; tile: {tile}; criterion holds: {crit}; both: {both}; "
      f"{'criterion = tiling on every pair' if tile == crit == both else 'CRITERION FAILS'}")
