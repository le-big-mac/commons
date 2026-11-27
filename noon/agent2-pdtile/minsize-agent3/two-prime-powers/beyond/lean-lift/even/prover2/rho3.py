# Suggestion 4 of the referee: where the least value of rho_2 is attained.
# Uses the recursion of rho2.py.  A tree is "contracted" if each of its levels has a node with two nonempty children
# (every level live).  For m elements: the number of contracted trees, the least rho_2 over them, and at how many
# of them it is attained.
import sys
from fractions import Fraction as Fr
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from rho2 import trees, rho2

def live_set(t):
    # the set of levels (1 = the split of the root) at which some node has two nonempty children
    if t[0] == 'L': return frozenset()
    if t[0] == 'U': return frozenset(l + 1 for l in live_set(t[1]))
    return frozenset({1}) | frozenset(l + 1 for l in live_set(t[1])) | frozenset(l + 1 for l in live_set(t[2]))

for m in [int(x) for x in sys.argv[1:]]:
    n_all = n_con = 0; best = None; at = 0; best_all = None
    for t, dep in trees(m, m - 1):
        n_all += 1
        r = rho2(t, dep)
        if best_all is None or r < best_all: best_all = r
        if live_set(t) == frozenset(range(1, dep + 1)):
            if m == 2 and t == ('N', ('L', 1), ('L', 1)): continue     # the exceptional pair
            n_con += 1
            if best is None or r < best: best, at = r, 1
            elif r == best: at += 1
    print('m =', m, '| trees with at most', m - 1, 'levels:', n_all, '| contracted:', n_con, '| least rho_2:', best,
          '(over all trees:', best_all, ') | attained at', at, 'contracted trees', flush=True)
