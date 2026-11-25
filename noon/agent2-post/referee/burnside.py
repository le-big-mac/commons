"""Count classes of ordered openings (g1,g2), and of single codes, under colour renaming x peg reordering, by Burnside."""
import itertools, numpy as np
codes = np.array(list(itertools.product(range(6), repeat=4)))
idx = {tuple(c): i for i, c in enumerate(codes)}
w = 6 ** np.arange(3, -1, -1)
tot1 = tot2 = n = 0
for cp in itertools.permutations(range(6)):
    cpa = np.array(cp)
    for pp in itertools.permutations(range(4)):
        im = cpa[codes][:, list(pp)] @ w
        f = int((im == np.arange(1296)).sum())
        tot1 += f; tot2 += f * f; n += 1
print('group order', n, 'classes of one code', tot1 // n, tot1 % n, 'classes of ordered pairs', tot2 // n, tot2 % n)
